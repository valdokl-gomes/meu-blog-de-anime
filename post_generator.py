import os
import feedparser
import re
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
    
    print(f"Processando com Groq: {title}")

    try:
        # Prompt atualizado para incluir a imagem
        prompt = f"""
        Escreva um post de blog curto e entusiasmado em Português sobre a notícia: {title}. 
        Fonte original: {link}. 
        
        REGRAS IMPORTANTES:
        1. Use Markdown.
        2. No final do texto, escolha UMA palavra-chave em inglês que defina o anime ou tema da notícia e escreva EXATAMENTE assim: KEYWORD: [palavra].
        """

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        
        resposta_completa = chat_completion.choices[0].message.content

        # Extrair a palavra-chave para a imagem (ou usar 'anime' como padrão)
        match = re.search(r"KEYWORD: (\w+)", resposta_completa)
        keyword = match.group(1) if match else "anime"
        
        # Limpar o texto para não mostrar a palavra-chave no post
        conteudo = re.sub(r"KEYWORD: \w+", "", resposta_completa).strip()

        # Link da imagem dinâmica
        image_url = f"https://source.unsplash.com/1600x900/?{keyword},anime"

        os.makedirs("content/posts", exist_ok=True)
        filename = f"content/posts/{datetime.now().strftime('%Y%m%d_%H%M')}.md"
        
        # Metadata com imagem destacada para o tema Ananke
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
        
        print(f"✅ SUCESSO! Imagem gerada para a categoria: {keyword}")

    except Exception as e:
        print(f"❌ Erro na Groq: {e}")
        exit(1)
else:
    print("Feed vazio.")
    exit(1)
