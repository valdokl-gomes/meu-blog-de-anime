import os
from google import genai
import feedparser
from datetime import datetime

# Configuração simples
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# Usando um feed mais leve
feed_url = "https://www.animenewsnetwork.com/news/rss.xml?ann-edition=w"
feed = feedparser.parse(feed_url)

if len(feed.entries) > 0:
    # Pegamos a segunda ou terceira notícia para evitar problemas de cache
    entry = feed.entries[1] 
    title = entry.title
    link = entry.link

    prompt = f"Escreva um post de blog curto e empolgante em Português sobre: {title}. Link da fonte: {link}. Use Markdown."

    try:
        # Voltamos ao modelo padrão mas com a chave nova
        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            contents=prompt
        )
        
        # Garante que a pasta existe
        os.makedirs("content/posts", exist_ok=True)
        
        # Nome do arquivo sem caracteres especiais
        clean_title = "".join(x for x in title if x.isalnum())[:20]
        filename = f"content/posts/{datetime.now().strftime('%Y%m%d')}_{clean_title}.md"
        
        metadata = f"---\ntitle: \"{title}\"\ndate: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S-03:00')}\ndraft: false\n---\n\n"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(metadata + response.text)
        
        print(f"Sucesso total: {title}")

    except Exception as e:
        print(f"Erro detectado: {e}")
        exit(1)
else:
    print("O feed de notícias retornou vazio.")
    exit(1)
