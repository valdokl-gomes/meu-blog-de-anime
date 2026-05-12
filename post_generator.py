import os
from google import genai
import feedparser
from datetime import datetime
import time

# Configuração
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# Fonte de notícias
feed_url = "https://www.animenewsnetwork.com/news/rss.xml"
feed = feedparser.parse(feed_url)

if len(feed.entries) > 0:
    entry = feed.entries[0]
    title_news = entry.title
    link_news = entry.link

    prompt = f"Escreva um post curto de blog em Português sobre: {title_news}. Fonte: {link_news}. Use Markdown."

    try:
        # Usando o modelo 8b, que tem cotas mais flexíveis
        response = client.models.generate_content(
            model="gemini-1.5-flash-8b", 
            contents=prompt
        )
        
        conteudo_post = response.text

        os.makedirs("content/posts", exist_ok=True)
        filename = f"content/posts/{datetime.now().strftime('%Y-%m-%d-%H%M%S')}.md"
        
        metadata = f"---\ntitle: \"{title_news}\"\ndate: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S-03:00')}\ndraft: false\n---\n\n"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(metadata + conteudo_post)
        
        print(f"Sucesso! Post gerado: {title_news}")

    except Exception as e:
        print(f"Erro na API: {e}")
        exit(1)
else:
    print("Feed vazio.")
    exit(1)
