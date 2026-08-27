name: Test NikosTV Bot

on:
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Recuperer le code
        uses: actions/checkout@v4

      - name: Installer Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Tester Xtream et Telegram
        env:
          XTREAM_URL: ${{ secrets.XTREAM_URL }}
          XTREAM_USER: ${{ secrets.XTREAM_USER }}
          XTREAM_PASS: ${{ secrets.XTREAM_PASS }}
          TELEGRAM_TOKEN: ${{ secrets.TELEGRAM_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
        run: python test_bot.py
