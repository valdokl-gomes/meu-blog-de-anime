import os
import google.generativeai as genai
import feedparser
from datetime import datetime

# Configuração forçando a versão estável
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Fonte de Notícias
feed_url = "https://www.animenewsnetwork.com/news/rss.xml"
feed = feedparser.parse(feed_url)

if len(feed.entries) > 0:
    entry = feed.entries[0]
    title = entry.title
    link = entry.link
    
    print(f"Processando: {title}")

    # Seleção do modelo com o caminho completo
    # Usamos o 1.5-flash que é o mais rápido
    model = genai.GenerativeModel('models/gemini-1.5-flash')

    prompt = f"Escreva um post curto de blog em Português sobre: {title}. Fonte: {link}. Use Markdown."

    try:
        # Gerando o conteúdo
        response = model.generate_content(prompt)
        
        # Se a resposta falhou ou foi bloqueada
        if not response.text:
            print("IA não gerou texto (pode ser filtro de segurança).")
            exit(1)

        os.makedirs("content/posts", exist_ok=True)
        
        # Nome do arquivo simples
        filename = f"content/posts/{datetime.now().strftime('%Y%m%d_%H%M')}.md"
        
        metadata = f"---\ntitle: \"{title}\"\ndate: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S-03:00')}\ndraft: false\n---\n\n"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(metadata + response.text)
        
        print("✅ SUCESSO! Post gerado.")

    except Exception as e:
        # Se der erro 404 de novo, vamos tentar listar os modelos para debug
        print(f"❌ Erro: {e}")
        exit(1)
else:
    print("Feed vazio.")
    exit(1)
