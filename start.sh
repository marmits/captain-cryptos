#!/bin/sh

echo "🚀 Démarrage Captain Cryptos"

python -u app/main.py &
python -u app/bot.py &

wait
