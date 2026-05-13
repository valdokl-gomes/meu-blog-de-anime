import os
import feedparser
import re
import random
from datetime import datetime
from groq import Groq

# Configuração da Groq
client = Groq(api_key=os.environ.get("GEMINI_API_KEY"))

# Fonte de Notícias
feed_url = "https://www.animenewsnetwork.com/news/rss.xml"
feed = feedparser.parse(feed_url)

if len(feed.entries) > 0:
    entry = feed.entries[0]
    title = entry.title
    link = entry.link
    
    print(f"Processando: {title}")

    try:
        prompt = f"""
        Escreva um post de blog curto em Português sobre: {title}. 
        Fonte: {link}. Use Markdown.
        No final, adicione apenas uma palavra-chave simples em inglês sobre o tema assim: KEYWORD: [palavra]
        """

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        
        resposta = chat_completion.choices[0].message.content

        # Extrair palavra-chave e limpar o texto
        match = re.search(r"KEYWORD:\s*(\w+)", resposta)
        keyword = match.group(1) if match else "anime"
        conteudo = re.sub(r"KEYWORD:.*", "", resposta).strip()

        # Gerador de link de imagem aleatória com base no tema (Picsum ou Unsplash)
        # Usamos um ID aleatório para a imagem não ser sempre a mesma
        img_id = random.randint(1, 1000)
        image_url = f"https://images.unsplash.com/photo-1578632292335-df3abbb0d586?auto=format&fit=crop&w=1600&q=80" 
        # Nota: O link acima é uma imagem padrão de anime de alta qualidade. 
        # Se quiser algo dinâmico que sempre mude:
        image_url = f"https://picsum.photos/seed/{img_id}/1600/900"

        os.makedirs("content/posts", exist_ok=True)
        filename = f"content/posts/{datetime.now().strftime('%Y%m%d_%H%M')}.md"
        
        # O segredo para o tema Ananke: featured_image
        metadata = (
            f"---\n"
            f"title: \"{title}\"\n"
            f"date: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S-03:00')}\n"
            f"featured_image: \"{image_url}\"\n"
            f"draft: false\n"
            f"---\n\n"
        )
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(metadata + conteudo)
        
        print("✅ Sucesso!")

    except Exception as e:
        print(f"❌ Erro: {e}")
        exit(1)
# Gerar ID aleatório para a imagem
        img_id = random.randint(1, 5000)
        image_url = f"https://picsum.photos/seed/{img_id}/1600/900"

        os.makedirs("content/posts", exist_ok=True)
        filename = f"content/posts/{datetime.now().strftime('%Y%m%d_%H%M')}.md"
        
        # 1. Montamos o cabeçalho (Front Matter)
        metadata = (
            f"---\n"
            f"title: \"{title}\"\n"
            f"date: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S-03:00')}\n"
            f"featured_image: \"{image_url}\"\n"
            f"draft: false\n"
            f"---\n\n"
        )
        
        # 2. Criamos a linha da imagem em Markdown para o corpo do post
        # IMPORTANTE: Esta linha PRECISA estar aqui para a imagem aparecer na página
        imagem_no_corpo = f"![Imagem de Destaque]({image_url})\n\n"
        
        # 3. Juntamos TUDO: Cabeçalho + Imagem + Texto da IA
        conteudo_final = metadata + imagem_no_corpo + conteudo
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(conteudo_final)
        
        print(f"✅ SUCESSO! Post gerado com imagem no corpo.")
