import os
import feedparser
import re
from datetime import datetime
from groq import Groq

# 1. CONFIGURAÇÃO DA IA
client = Groq(api_key=os.environ.get("GEMINI_API_KEY"))

# 2. FONTE DE NOTÍCIAS
feed_url = "https://www.animenewsnetwork.com/news/rss.xml"
feed = feedparser.parse(feed_url)

# 3. CAMINHO DA SUA IMAGEM (Relativo)
image_url = "images/banner-anime.png"

for i in range(min(3, len(feed.entries))):
    entry = feed.entries[i]
    original_title = entry.title
    link = entry.link
    
    try:
        prompt = f"Traduza para Português e resuma: {original_title}. Regras: 1a linha título, resto corpo."
        
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        
        resposta_ia = chat_completion.choices[0].message.content
        linhas = resposta_ia.strip().split('\n')
        
        titulo_traduzido = re.sub(r'[#\*]', '', linhas[0]).strip()
        corpo_texto = '\n'.join(linhas[1:]).strip()

        os.makedirs("content/posts", exist_ok=True)
        filename = f"content/posts/noticia_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}.md"
        
        metadata = (
            f"---\n"
            f"title: \"{titulo_traduzido}\"\n"
            f"date: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}\n"
            f"featured_image: \"{image_url}\"\n"
            f"draft: false\n"
            f"---\n\n"
        )
        
        imagem_html = f'<img src="../../{image_url}" alt="Banner Anime" style="width:100%; border-radius:12px;"><br><br>\n\n'
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(metadata + imagem_html + corpo_texto)
            
        print(f"Sucesso no post {i}")

    except Exception as e:
        print(f"Erro: {e}")
