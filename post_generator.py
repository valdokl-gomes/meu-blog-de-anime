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

# 3. CAMINHO DA SUA IMAGEM (Agora que está na pasta certa)
image_url = "/images/banner-anime.png"

for i in range(min(3, len(feed.entries))):
    entry = feed.entries[i]
    original_title = entry.title
    link = entry.link
    
    try:
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
        
        # Limpa o título de símbolos
        titulo_traduzido = re.sub(r'[#\*]', '', linhas[0]).strip()
        corpo_texto = '\n'.join(linhas[1:]).strip()

        os.makedirs("content/posts", exist_ok=True)
        # Gerando nome de arquivo único com timestamp
        filename = f"content/posts/noticia_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}.md"
        
        metadata = (
            f"---\n"
            f"title: \"{titulo_traduzido}\"\n"
            f"date: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}\n"
            f"featured_image: \"{image_url}\"\n"
            f"draft: false\n"
            f"---\n\n"
        )
        
        # Inserindo a imagem via HTML para garantir que o tema Ananke mostre no corpo
        imagem_html = f'<img src="{image_url}" alt="Banner Anime" style="width:100%; border-radius:12px;"><br><br>\n\n'
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(metadata + imagem_html + corpo_texto)
            
        print(f"✅ Notícia '{titulo_traduzido}' criada com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao processar notícia {i}: {e}")
