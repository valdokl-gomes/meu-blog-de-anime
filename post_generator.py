import os
import feedparser
import random
from datetime import datetime
from groq import Groq

client = Groq(api_key=os.environ.get("GEMINI_API_KEY"))

feed_url = "https://www.animenewsnetwork.com/news/rss.xml"
feed = feedparser.parse(feed_url)

# Pegamos as 3 notícias mais recentes para dar volume ao blog
for i in range(min(3, len(feed.entries))):
    entry = feed.entries[i]
    title = entry.title
    link = entry.link
    
    img_id = random.randint(1, 5000)
    # Usando o Unsplash via busca direta, que o Ananke aceita melhor
    image_url = f"https://images.unsplash.com/photo-1578632292335-df3abbb0d586?auto=format&fit=crop&w=1200&q=80&sig={img_id}"

    try:
        prompt = f"Escreva um post curto em Português sobre: {title}. Fonte: {link}. Não repita o título no corpo."
        
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        
        conteudo_ia = chat_completion.choices[0].message.content
        
        os.makedirs("content/posts", exist_ok=True)
        # Nome do ficheiro único
        filename = f"content/posts/post_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}.md"
        
        # O SEGREDO: Tiramos o fuso horário manual para não conflitar com o GitHub
        data_atual = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        
        metadata = (
            f"---\n"
            f"title: \"{title}\"\n"
            f"date: {data_atual}\n"
            f"featured_image: \"{image_url}\"\n"
            f"thumbnail: \"{image_url}\"\n"
            f"draft: false\n"
            f"---\n\n"
        )
        
        # Forçamos a imagem no corpo com HTML puro (infalível)
        corpo_final = f'<img src="{image_url}" style="width:100%; border-radius:10px;"><br><br>\n\n' + conteudo_ia
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(metadata + corpo_final)
            
        print(f"✅ Gerado: {title}")

    except Exception as e:
        print(f"❌ Erro: {e}")
