# Création et intégration du bot Discord – Captain Cryptos V1

## Objectif

Créer un bot Discord permettant d’exécuter manuellement :

```text
!report
```

afin de générer le même rapport crypto que celui envoyé automatiquement tous les jours à **07:30**.

---

# 1. Créer l’application Discord

Ouvrir :

https://discord.com/developers/applications

### Étapes

1. Cliquer sur **New Application**
2. Donner un nom :

```text
Captain Cryptos
```

3. Cliquer sur **Create**

---

# 2. Créer le bot Discord

Dans le menu gauche :

```text
Bot
```

Puis :

### Ajouter un bot

Cliquer sur :

```text
Add Bot
```

Confirmer.

---

## Récupérer le token

Dans :

```text
Bot
```

Cliquer sur :

```text
Reset Token
```

ou :

```text
Copy Token
```

Copier le token.

⚠️ **Ne jamais commit ce token dans Git.**

---

# 3. Activer les intents nécessaires

Toujours dans :

```text
Bot
```

Activer :

✅ **MESSAGE CONTENT INTENT**

Sans cela :

```text
!report
```

ne fonctionnera pas.

Sauvegarder les changements.

---

# 4. Inviter le bot sur le serveur Discord

Dans le menu :

```text
OAuth2
→ URL Generator
```

### Cocher les scopes

#### Scopes

```text
bot
applications.commands
```

#### Bot Permissions

Cocher au minimum :

```text
View Channels
Send Messages
Read Message History
```

(optionnel)

```text
Use Slash Commands
```

---

### Générer l’URL d’invitation

Copier l’URL générée automatiquement en bas de page.

L’ouvrir dans le navigateur.

Choisir le serveur Discord :

```text
Marmits
```

Puis :

```text
Autoriser
```

Valider le captcha.

---

# 5. Ajouter le token dans le projet

Ajouter dans `.env` :

```env
DISCORD_BOT_TOKEN=xxxxxxxxxxxxxxxx
```

---

# 6. Ajouter le token dans `config.py`

Ajouter :

```python
DISCORD_BOT_TOKEN = os.getenv(
    "DISCORD_BOT_TOKEN"
)
```

---

# 7. Ajouter `discord.py`

Dans :

```text
requirements.txt
```

Ajouter :

```text
discord.py
```

Puis rebuild Docker :

```bash
docker compose build
docker compose up -d
```

---

# 8. Créer `bot.py`

Créer :

```text
app/bot.py
```

Fonction principale :

* connexion Discord
* commande :

```text
!report
```

* réutilisation du moteur existant :

```python
build_report()
```

afin d’envoyer exactement le même rapport que celui de 07:30.

---

# 9. Autoriser uniquement le salon `#cryptos`

## Bloquer le bot globalement

Dans Discord :

```text
Paramètres du serveur
→ Rôles
→ Captain Cryptos
→ Permissions
```

Désactiver :

```text
Voir les salons
```

---

## Autoriser uniquement `#cryptos`

Dans :

```text
#cryptos
→ Modifier le salon
→ Permissions
```

Ajouter :

```text
Captain Cryptos
```

Autoriser :

```text
Voir le salon
Envoyer des messages
Lire l’historique
```

Résultat :

```text
#cryptos          ✅
#full-stack       ❌
#wiki-feeds       ❌
#mxo              ❌
```

---

# 10. Lancer automatiquement le bot dans Docker

Créer :

```text
start.sh
```

Contenu :

```bash
#!/bin/sh

echo "🚀 Démarrage Captain Cryptos"

python -u app/main.py &
python -u app/bot.py &

wait
```

Rendre exécutable :

```bash
chmod +x start.sh
```

---

## Modifier le Dockerfile

Ajouter :

```dockerfile
COPY start.sh .
RUN chmod +x start.sh

CMD ["sh", "start.sh"]
```

---

## Rebuild

```bash
docker compose down
docker compose build --no-cache
docker compose up -d
```

---

# 11. Vérifier les logs

```bash
docker logs -f crypto-assistant
```

Logs attendus :

```text
🚀 Démarrage Captain Cryptos
Crypto assistant démarré
Discord status: 204
✅ Bot connecté : Captain Cryptos#6120
```

### Signification

#### `Discord status: 204`

Webhook Discord OK.

#### `Bot connecté`

Bot Discord opérationnel.

---

# 12. Tester le bot

Dans le salon :

```text
#cryptos
```

Exécuter :

```text
!report
```

Le bot doit générer :

* rapport Fear & Greed
* dominance BTC
* watchlist crypto
* scores opportunité

identiques au rapport automatique quotidien.

---

# Résultat final

Captain Cryptos V1 dispose :

✅ Rapport quotidien 07:30
✅ Rapport au démarrage Docker
✅ Alertes marché (pump/dump)
✅ Bot Discord autonome
✅ Commande `!report`
✅ Auto-start Docker
✅ Restriction au salon `#cryptos`
