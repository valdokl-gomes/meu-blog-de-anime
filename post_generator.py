import os
import google.generativeai as genai
import feedparser
from datetime import datetime

# Configuração da IA
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# Nova fonte de notícias (Anime News Network é bem estável)
feed_url = "https://www.animenewsnetwork.com/news/rss.xml"
feed = feedparser.parse(feed_url)

# Verifica se o feed não está vazio
if len(feed.entries) > 0:
    entry = feed.entries[0]
    title_news = entry.title
    link_news = entry.link

    # Prompt para a IA
    prompt = f"""
    Você é um redator de um blog de animes chamado 'Anime News AI'.
    Com base na notícia: "{title_news}" (Link: {link_news}),
    escreva um post de blog em Português do Brasil de forma original.
    Use Markdown, inclua títulos (##) e um tom empolgante.
    """

    response = model.generate_content(prompt)
    conteudo_post = response.text

    # Criar a pasta se não existir e salvar o arquivo
    filename = f"content/posts/{datetime.now().strftime('%Y-%m-%d-%H%M%S')}.md"
    metadata = f"""---
title: "{title_news}"
date: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S-03:00')}
draft: false
---

"""
    # Garante que o diretório existe
    os.makedirs("content/posts", exist_ok=True)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(metadata + conteudo_post)
    
    print(f"Sucesso! Post gerado: {title_news}")
else:
    print("Erro: Não foi possível ler o feed de notícias agora.")
    exit(1)
