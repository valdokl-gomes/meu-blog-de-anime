import os
import feedparser
import random
import re
from datetime import datetime
from groq import Groq

client = Groq(api_key=os.environ.get("GEMINI_API_KEY"))

feed_url = "https://www.animenewsnetwork.com/news/rss.xml"
feed = feedparser.parse(feed_url)

for i in range(min(3, len(feed.entries))):
    entry = feed.entries[i]
    original_title = entry.title
    link = entry.link
    
    # Gerar ID aleatório para a imagem não repetir
    img_id = random.randint(1, 5000)
    # Picsum é muito mais estável que o Unsplash Source antigo
    image_url = f"https://picsum.photos/seed/{img_id}/1200/600"

    try:
        prompt = f"""
        Traduza o título para Português e escreva um post curto sobre a notícia.
        Título original: {original_title}
        Link da fonte: {link}
        
        REGRAS:
        1. A primeira linha deve ser apenas o TITULO TRADUZIDO.
        2. O restante deve ser o corpo do texto em Português.
        """

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        
        resposta_ia = chat_completion.choices[0].message.content
        linhas = resposta_ia.strip().split('\n')
        
        # Pega a primeira linha como título e limpa caracteres de Markdown (# ou *)
        titulo_traduzido = re.sub(r'[#\*]', '', linhas[0]).strip()
        conteudo_ia = '\n'.join(linhas[1:]).strip()

        os.makedirs("content/posts", exist_ok=True)
        filename = f"content/posts/post_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}.md"
        
        metadata = (
            f"---\n"
            f"title: \"{titulo_traduzido}\"\n"
            f"date: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}\n"
            f"featured_image: \"{image_url}\"\n"
            f"draft: false\n"
            f"---\n\n"
        )
        
        # Colocamos a imagem com uma tag HTML simples para garantir que o Hugo não a bloqueie
        corpo_final = f'<img src="{image_url}" alt="Anime News" style="width:100%; border-radius:8px;"><br>\n\n' + conteudo_ia
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(metadata + corpo_final)
            
        print(f"✅ Post gerado: {titulo_traduzido}")

    except Exception as e:
        print(f"❌ Erro ao processar: {e}")
