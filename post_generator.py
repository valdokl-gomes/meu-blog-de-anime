import os
import google.generativeai as genai
import feedparser
from datetime import datetime

# Configuração da IA
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# Feed de notícias (RSS da Crunchyroll)
feed_url = "https://www.crunchyroll.com/newsfeeds/rss/news"
feed = feedparser.parse(feed_url)

# Pega apenas a notícia mais recente para postar
entry = feed.entries[0]
title_news = entry.title
link_news = entry.link

# Prompt para a IA
prompt = f"""
Você é um redator de um blog de animes chamado 'Anime News AI'.
Com base no título da notícia: "{title_news}" e no link {link_news},
escreva um post de blog em Português do Brasil.
O post deve ter:
1. Um título chamativo em Markdown (#).
2. Três parágrafos envolventes sobre o assunto.
3. Uma conclusão chamando os leitores para comentar.
Use formatação Markdown. Não invente fatos, apenas comente a notícia.
"""

response = model.generate_content(prompt)
conteudo_post = response.text

# Criar o arquivo para o Hugo
filename = f"content/posts/{datetime.now().strftime('%Y-%m-%d-%H%M%S')}.md"
metadata = f"""---
title: "{title_news}"
date: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S-03:00')}
draft: false
---

"""

with open(filename, "w", encoding="utf-8") as f:
    f.write(metadata + conteudo_post)

print(f"Post gerado: {filename}")
