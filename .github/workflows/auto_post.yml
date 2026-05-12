name: Auto Post Anime News

on:
  schedule:
    - cron: '0 12 * * *'
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: pip install google-generativeai feedparser # Voltamos para a estável
      - name: Run Generator
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        run: python post_generator.py
      - name: Commit and Push
        run: |
          git config --global user.name "AutoBot"
          git config --global user.email "bot@github.com"
          git add .
          git commit -m "Novo post automático de anime" || exit 0
          git push
