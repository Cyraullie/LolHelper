#!/bin/bash

echo "📦 Deploy en cours..."

cd /home/pi/bots/lolhelper || exit

echo "🔄 Git pull..."
git pull origin main

echo "🐍 Activation venv..."
source venv/bin/activate

echo "📦 Installation dépendances..."
pip install -r requirements.txt

echo "🔁 Restart bot..."
sudo systemctl restart lolhelper

echo "✅ Deploy terminé"