import os
from google import genai
import feedparser
from datetime import datetime

# Configuração da nova biblioteca do Google
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# Fonte de notícias
feed_url = "https://www.animenewsnetwork.com/news/rss.xml"
feed = feedparser.parse(feed_url)

if len(feed.entries) > 0:
    entry = feed.entries[0]
    title_news = entry.title
    link_news = entry.link

    # Prompt otimizado
    prompt = f"""Escreva um post de blog em Português sobre a notícia: {title_news}. 
    Fonte original: {link_news}. 
    Use Markdown, títulos chamativos e um tom animado para fãs de anime."""

    # Chamada atualizada para o modelo Gemini 2.0 Flash
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    
    conteudo_post = response.text

    # Garante que a pasta existe e salva o arquivo
    os.makedirs("content/posts", exist_ok=True)
    filename = f"content/posts/{datetime.now().strftime('%Y-%m-%d-%H%M%S')}.md"
    
    metadata = f"""---
title: "{title_news}"
date: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S-03:00')}
draft: false
---

"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(metadata + conteudo_post)
    
    print(f"Sucesso! Post gerado: {title_news}")
else:
    print("Nenhuma notícia encontrada no feed.")
    exit(1)
