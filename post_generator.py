import os
import feedparser
from datetime import datetime
from groq import Groq

# Configuração da Groq (Usando o Secret que você já tem)
client = Groq(api_key=os.environ.get("GEMINI_API_KEY"))

# Fonte de Notícias
feed_url = "https://www.animenewsnetwork.com/news/rss.xml"
feed = feedparser.parse(feed_url)

if len(feed.entries) > 0:
    entry = feed.entries[0]
    title = entry.title
    link = entry.link
    
    print(f"Processando com Groq: {title}")

    try:
        # Chamada para o modelo Llama 3 (muito bom para português)
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Escreva um post de blog curto em Português sobre: {title}. Fonte: {link}. Use Markdown.",
                }
            ],
            model="llama-3.3-70b-versatile", # Modelo potente e grátis
        )
        
        conteudo = chat_completion.choices[0].message.content

        os.makedirs("content/posts", exist_ok=True)
        filename = f"content/posts/{datetime.now().strftime('%Y%m%d_%H%M')}.md"
        
        metadata = f"---\ntitle: \"{title}\"\ndate: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S-03:00')}\ndraft: false\n---\n\n"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(metadata + conteudo)
        
        print("✅ SUCESSO com Groq!")

    except Exception as e:
        print(f"❌ Erro na Groq: {e}")
        exit(1)
else:
    print("Feed vazio.")
    exit(1)
