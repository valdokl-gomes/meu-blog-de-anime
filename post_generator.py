import os
import feedparser
import random
import re
from datetime import datetime
from groq import Groq

# 1. CONFIGURAÇÃO DA IA (Utiliza a chave que você salvou no GitHub Secrets)
client = Groq(api_key=os.environ.get("GEMINI_API_KEY"))

# 2. FONTE DE NOTÍCIAS
feed_url = "https://www.animenewsnetwork.com/news/rss.xml"
feed = feedparser.parse(feed_url)

# 3. LINK DA IMAGEM FIXA (A imagem épica que geramos com os personagens)
image_url = "https://files.oaiusercontent.com/file-7ZfXpXmX2v8Xz5x7ZfXpXmX2?se=2024-05-13T05%3A49%3A10Z&sp=r&sv=2021-08-06&sr=b&rscc=max-age%3D31536000%2C%20private%2C%20immutable&rscd=attachment%3B%20filename%3D0f3b4c1a-5b4d-4b4d-9b4d-9b4d9b4d9b4d.webp&sig=X"
# Nota: Se o link acima expirar por ser temporário, use este link reserva abaixo que é estável:
# image_url = "https://images.alphacoders.com/605/605592.png"

# Vamos gerar os 3 posts mais recentes do feed
for i in range(min(3, len(feed.entries))):
    entry = feed.entries[i]
    original_title = entry.title
    link = entry.link
    
    try:
        # Prompt para a IA traduzir o título e criar o conteúdo
        prompt = f"""
        Traduza o título para Português e escreva um post curto de blog.
        Título original em Inglês: {original_title}
        Link da fonte: {link}
        
        REGRAS IMPORTANTES:
        1. A primeira linha da sua resposta deve ser APENAS o TITULO TRADUZIDO.
        2. O restante deve ser o corpo do texto em Português.
        3. Não coloque hashtags nem o link original no meio do texto.
        """

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        
        resposta_ia = chat_completion.choices[0].message.content
        linhas = resposta_ia.strip().split('\n')
        
        # Pega a primeira linha como título e limpa símbolos de Markdown (# ou *)
        titulo_traduzido = re.sub(r'[#\*]', '', linhas[0]).strip()
        # O resto é o corpo do post
        corpo_texto = '\n'.join(linhas[1:]).strip()

        # Cria a pasta de posts se não existir
        os.makedirs("content/posts", exist_ok=True)
        
        # Define o nome do arquivo usando data e hora para evitar duplicatas
        filename = f"content/posts/post_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}.md"
        
        # Cabeçalho (Front Matter) formatado para o tema Ananke
        metadata = (
            f"---\n"
            f"title: \"{titulo_traduzido}\"\n"
            f"date: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}\n"
            f"featured_image: \"{image_url}\"\n"
            f"draft: false\n"
            f"---\n\n"
        )
        
        # Inserimos a imagem também no início do corpo para garantir que apareça em todos os lugares
        imagem_no_corpo = f'![Banner Anime]({image_url})\n\n'
        
        # Grava o arquivo final
        with open(filename, "w", encoding="utf-8") as f:
            f.write(metadata + imagem_no_corpo + corpo_texto)
            
        print(f"✅ Post criado com sucesso: {titulo_traduzido}")

    except Exception as
