import os
import google.generativeai as genai
import feedparser
from datetime import datetime

# Configuração usando a biblioteca estável
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Seleção do modelo
model = genai.GenerativeModel('gemini-1.5-flash')

# Fonte de Notícias
feed_url = "https://www.animenewsnetwork.com/news/rss.xml"
feed = feedparser.parse(feed_url)

if len(feed.entries) > 0:
    entry = feed.entries[0]
    title = entry.title
    link = entry.link
    
    print(f"Processando: {title}")

    prompt = f"Escreva um post curto de blog em Português sobre: {title}. Fonte: {link}. Use Markdown."

    try:
        # Gerando o conteúdo
        response = model.generate_content(prompt)
        
        # Pasta de destino
        os.makedirs("content/posts", exist_ok=True)
        
        # Nome do arquivo seguro
        filename = f"content/posts/{datetime.now().strftime('%Y%m%d_%H%M')}.md"
        
        metadata = f"---\ntitle: \"{title}\"\ndate: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S-03:00')}\ndraft: false\n---\n\n"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(metadata + response.text)
        
        print("✅ Post gerado com sucesso!")

    except Exception as e:
        print(f"❌ Erro na API: {e}")
        exit(1)
else:
    print("Feed vazio.")
    exit(1)
