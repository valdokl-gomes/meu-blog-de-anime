import os
from google import genai
import feedparser
from datetime import datetime
import time

# 1. Configuração do Cliente
# Usamos a nova biblioteca 'google-genai' que instalamos no workflow
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# 2. Fonte de Notícias (RSS do Anime News Network - muito estável)
feed_url = "https://www.animenewsnetwork.com/news/rss.xml?ann-edition=w"
feed = feedparser.parse(feed_url)

def generate_post():
    if len(feed.entries) > 0:
        # Pegamos a notícia mais recente
        entry = feed.entries[0]
        title = entry.title
        link = entry.link
        
        print(f"Lendo notícia: {title}")

        # Prompt direto e focado para evitar erros de processamento
        prompt = f"Escreva um post de blog curto (max 300 palavras) em Português sobre: {title}. Fonte: {link}. Use Markdown com títulos ## e um tom empolgante para otakus."

        try:
            # 3. Chamada da IA com o caminho de modelo COMPLETO (evita erro 404)
            response = client.models.generate_content(
                model="models/gemini-1.5-flash", 
                contents=prompt
            )
            
            if not response.text:
                print("Erro: A IA retornou um texto vazio.")
                return

            # 4. Organização dos arquivos para o Hugo
            # Cria a pasta content/posts se ela não existir
            os.makedirs("content/posts", exist_ok=True)
            
            # Limpa o título para o nome do arquivo não ter erro
            clean_title = "".join(x for x in title if x.isalnum() or x==' ')[:30].replace(' ', '_')
            filename = f"content/posts/{datetime.now().strftime('%Y%m%d_%H%M')}_{clean_title}.md"
            
            # Formatação do Frontmatter (metadados que o Hugo exige)
            metadata = (
                "---\n"
                f"title: \"{title}\"\n"
                f"date: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S-03:00')}\n"
                "draft: false\n"
                "---\n\n"
            )
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(metadata + response.text)
            
            print(f"✅ Sucesso! Post gerado em: {filename}")

        except Exception as e:
            print(f"❌ Erro na chamada da API: {e}")
            # Se for erro de cota, o programa avisa
            if "429" in str(e):
                print("Dica: Você atingiu o limite de requisições. Espere alguns minutos.")
            exit(1)
    else:
        print("❌ Erro: Não foi possível carregar o feed de notícias.")
        exit(1)

if __name__ == "__main__":
    generate_post()
