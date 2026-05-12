import os
from google import genai
import feedparser
from datetime import datetime

# Configuração do Cliente
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# Fonte de Notícias
feed_url = "https://www.animenewsnetwork.com/news/rss.xml?ann-edition=w"
feed = feedparser.parse(feed_url)

if len(feed.entries) > 0:
    entry = feed.entries[0]
    title = entry.title
    link = entry.link
    
    print(f"Lendo notícia: {title}")

    prompt = f"Escreva um post de blog em Português sobre o anime: {title}. Fonte: {link}. Use Markdown."

    try:
        # Trocando para o modelo PRO que tem endpoints mais estáveis
        response = client.models.generate_content(
            model="gemini-1.5-pro", 
            contents=prompt
        )
        
        if not response.text:
            print("Erro: Resposta vazia.")
            exit(1)

        os.makedirs("content/posts", exist_ok=True)
        
        clean_title = "".join(x for x in title if x.isalnum() or x==' ')[:30].replace(' ', '_')
        filename = f"content/posts/{datetime.now().strftime('%Y%m%d_%H%M')}_{clean_title}.md"
        
        metadata = f"---\ntitle: \"{title}\"\ndate: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S-03:00')}\ndraft: false\n---\n\n"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(metadata + response.text)
        
        print(f"✅ Sucesso total! Post criado.")

    except Exception as e:
        print(f"❌ Erro crítico: {e}")
        exit(1)
else:
    print("Feed vazio.")
    exit(1)
