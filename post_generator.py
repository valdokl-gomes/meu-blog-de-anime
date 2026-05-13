import os
import feedparser
import random
import re
from datetime import datetime
from groq import Groq

# Configuração da IA
client = Groq(api_key=os.environ.get("GEMINI_API_KEY"))

# Link das notícias (RSS)
feed_url = "https://www.animenewsnetwork.com/news/rss.xml"
feed = feedparser.parse(feed_url)

# Link da imagem fixa de anime (Alta Qualidade)
# Você pode trocar esse link por qualquer outro se quiser mudar o banner depois
image_url = "https://wallpaperaccess.com/full/137326.jpg"

# Vamos processar as 3 notícias mais recentes
for i in range(min(3, len(feed.entries))):
    entry = feed.entries[i]
    original_title = entry.title
    link = entry.link
    
    try:
        # Prompt para a IA traduzir e criar o texto
        prompt = f"""
        Traduza o título para Português e escreva um post curto de blog.
        Título original: {original_title}
        Fonte: {link}
        
        REGRAS:
        1. A primeira linha deve ser APENAS o título traduzido.
        2. O resto deve ser o corpo do texto em Português.
        3. Não use hashtags ou links no corpo do texto.
        """

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        
        resposta_ia = chat_completion.choices[0].message.content
        linhas = resposta_ia.strip().split('\n')
        
        # Limpa o título de símbolos como # ou *
        titulo_traduzido = re.sub(r'[#\*]', '', linhas[0]).strip()
        corpo_texto = '\n'.join(linhas[1:]).strip()

        # Criar a pasta se não existir
        os.makedirs("content/posts", exist_ok=True)
        
        # Nome do arquivo com data e hora para não repetir
        filename = f"content/posts/post_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}.md"
        
        # Montagem do arquivo Hugo
        metadata = (
            f"---\n"
            f"title: \"{titulo_traduzido}\"\n"
            f"date: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}\n"
            f"featured_image: \"{image_url}\"\n"
            f"draft: false\n"
            f"---\n\n"
        )
        
        # Inserindo a imagem no corpo do texto para garantir visibilidade
        imagem_html = f'<img src="{image_url}" style="width:100%; border-radius:10px;"><br><br>\n\n'
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(metadata + imagem_html + corpo_texto)
            
        print(f"✅ Sucesso: {titulo_traduzido}")

    except Exception as e:
        print(f"❌ Erro na notícia {i}: {e}")
