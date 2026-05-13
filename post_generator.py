import os
import feedparser
import random
from datetime import datetime
from groq import Groq

client = Groq(api_key=os.environ.get("GEMINI_API_KEY"))

feed_url = "https://www.animenewsnetwork.com/news/rss.xml"
feed = feedparser.parse(feed_url)

if len(feed.entries) > 0:
    entry = feed.entries[0]
    title = entry.title
    link = entry.link
    
    # Gerar o link da imagem antes de chamar a IA
    img_id = random.randint(1, 5000)
    image_url = f"https://picsum.photos/seed/{img_id}/1200/600"

    try:
        # Mudamos o prompt para a IA já incluir o Markdown da imagem no texto
        prompt = f"""
        Escreva um post de blog em Português sobre: {title}. 
        Fonte: {link}.
        
        REGRAS:
        1. Comece o texto obrigatoriamente com este código exato: ![imagem]({image_url})
        2. Use Markdown para o resto do post.
        """

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        
        conteudo_da_ia = chat_completion.choices[0].message.content

        os.makedirs("content/posts", exist_ok=True)
        filename = f"content/posts/{datetime.now().strftime('%Y%m%d_%H%M')}.md"
        
        # O cabeçalho fica simples, a imagem vem no 'conteudo_da_ia'
        metadata = (
            f"---\n"
            f"title: \"{title}\"\n"
            f"date: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S-03:00')}\n"
            f"featured_image: \"{image_url}\"\n"
            f"draft: false\n"
            f"---\n\n"
        )
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(metadata + conteudo_da_ia)
        
        print(f"✅ SUCESSO! IA gerou o post com imagem imbuída.")

    except Exception as e:
        print(f"❌ Erro: {e}")
