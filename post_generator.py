import os
import feedparser
import random
import re
from datetime import datetime
from groq import Groq

# 1. CONFIGURAÇÃO DA IA
client = Groq(api_key=os.environ.get("GEMINI_API_KEY"))

# 2. FONTE DE NOTÍCIAS
feed_url = "https://www.animenewsnetwork.com/news/rss.xml"
feed = feedparser.parse(feed_url)

# 3. LINK PERMANENTE (Imagem de alta qualidade que não expira)
image_url = "https://wallpaperaccess.com/full/137326.jpg"

# Vamos processar as 3 notícias mais recentes
for i in range(min(3, len(feed.entries))):
    entry = feed.entries[i]
    original_title = entry.title
    link = entry.link
    
    try:
        # Prompt para a IA traduzir o título e criar o resumo
        prompt = f"""
        Traduza o título para Português e escreva um post curto de blog.
        Título original em Inglês: {original_title}
        Link da fonte: {link}
        
        REGRAS:
        1. A primeira linha deve ser APENAS o TITULO TRADUZIDO.
        2. O restante deve ser o corpo do texto em Português.
        """

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        
        resposta_ia = chat_completion.choices[0].message.content
        linhas = resposta_ia.strip().split('\n')
        
        # Limpa o título (remove # ou *)
        titulo_traduzido = re.sub(r'[#\*]', '', linhas[0]).strip()
        corpo_texto = '\n'.join(linhas[1:]).strip()

        os.makedirs("content/posts", exist_ok=True)
        filename = f"content/posts/noticia_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}.md"
        
        # Cabeçalho do Hugo (Front Matter)
        metadata = (
            f"---\n"
            f"title: \"{titulo_traduzido}\"\n"
            f"date: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}\n"
            f"featured_image: \"{image_url}\"\n"
            f"draft: false\n"
            f"---\n\n"
        )
        
        # HTML para garantir que a imagem aparece no corpo do texto
        imagem_html = f'<img src="{image_url}" style="width:100%; border-radius:10px;"><br><br>\n\n'
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(metadata + imagem_html + corpo_texto)
            
        print(f"✅ Gerado: {titulo_traduzido}")

    except Exception as e:
        print(f"❌ Erro na notícia {i}: {e}")
