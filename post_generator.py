import os
import feedparser
import random
from datetime import datetime
from groq import Groq

client = Groq(api_key=os.environ.get("GEMINI_API_KEY"))

feed_url = "https://www.animenewsnetwork.com/news/rss.xml"
feed = feedparser.parse(feed_url)

for i in range(min(3, len(feed.entries))):
    entry = feed.entries[i]
    # Guardamos o título original em inglês
    original_title = entry.title
    link = entry.link
    
    # 1. Ajuste da Imagem: Usamos palavras-chave de anime no Unsplash
    # Isso aumenta muito a chance de vir algo relacionado a desenho/japão
    img_id = random.randint(1, 1000)
    image_url = f"https://source.unsplash.com/featured/1200x600?anime,manga,japan&sig={img_id}"
    # Se o Source Unsplash falhar, esta é uma alternativa de anime estável:
    # image_url = f"https://images.unsplash.com/photo-1578632292335-df3abbb0d586?auto=format&fit=crop&w=1200&q=80"

    try:
        # 2. Novo Prompt: Agora pedimos para a IA traduzir o título também!
        prompt = f"""
        Traduza o título e escreva um post curto em Português.
        Título original: {original_title}
        Fonte: {link}
        
        REGRAS:
        1. A primeira linha da sua resposta deve ser o título traduzido.
        2. A segunda linha deve ser o código: ![anime]({image_url})
        3. O restante deve ser o corpo do texto em português.
        """

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        
        resposta_ia = chat_completion.choices[0].message.content
        
        # Separar o título traduzido do resto do conteúdo
        linhas = resposta_ia.split('\n')
        titulo_traduzido = linhas[0].replace('#', '').strip() # Limpa possíveis títulos em Markdown
        conteudo_ia = '\n'.join(linhas[1:])

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
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(metadata + conteudo_ia)
            
        print(f"✅ Traduzido e Gerado: {titulo_traduzido}")

    except Exception as e:
        print(f"❌ Erro: {e}")
