# 🚀 Captain Cryptos — Crypto Assistant V1

Assistant crypto léger auto-hébergé avec Docker.

Objectif :

> Recevoir automatiquement un rapport crypto quotidien sur Discord et détecter des opportunités / mouvements de marché sans faire tourner de grosse IA locale.

Projet pensé pour :

- Ubuntu
- Docker / Docker Compose
- VM Proxmox
- faible consommation ressources
- exécution 24/7

---

# ✨ Fonctionnalités

## Rapport quotidien Discord

Tous les jours à **07:30** :

- Fear & Greed Index
- Prix EUR + USD
- variation 24h
- variation 7 jours
- score opportunité personnalisé

Exemple :

```txt
📊 Rapport Crypto

🌍 Marché
Fear & Greed : 18 (Extreme Fear)

━━━━━━━━━━━━━━
BTC
💰 Prix : 55 756 € / 64 504 $
📈 24h : +1.11%
📊 7j : +2.71%
🎯 Score : 74/100
➡ 🟢 DCA progressif intéressant
````

---

## Alertes marché

Vérification automatique toutes les **30 minutes**.

### 🚀 Pump

Détection :

```txt
+10% ou plus en 24h
```

Exemple :

```txt
🚀 HYPE

Forte hausse détectée

💰 Prix : 52 € / 61 $
📈 24h : +11.4%

➡ Prudence FOMO
```

### 🚨 Dump

Détection :

```txt
-7% ou plus en 24h
```

Exemple :

```txt
🚨 BTC

Forte baisse détectée

➡ Possible zone de DCA progressif
```

---

## Anti-spam Discord

Le projet mémorise les alertes déjà envoyées via :

```txt
data/state.json
```

Évite :

```txt
🚀 HYPE
🚀 HYPE
🚀 HYPE
```

toutes les 30 min.

---

## Résistance API

Gestion des erreurs :

* API indisponible
* timeout
* CoinGecko rate limit (429)

Le container continue de tourner.

---

# 📂 Architecture du projet

```txt
MVP_crypto/
│
├── app/
│   ├── alerts.py
│   ├── config.py
│   ├── discord_notify.py
│   ├── main.py
│   ├── market.py
│   ├── report.py
│   └── scoring.py
│
├── data/
│   └── state.json
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Rôle des fichiers

### `main.py`

Scheduler principal.

Responsable de :

* démarrage
* rapport quotidien
* alertes périodiques

---

### `market.py`

Connexion APIs :

* CoinGecko
* Fear & Greed Index

Responsable de :

* prix crypto
* formatage EUR/USD
* données marché

---

### `report.py`

Construit le rapport Discord.

---

### `alerts.py`

Détection :

* pump
* dump

- anti-doublon.

---

### `scoring.py`

Calcule le **score opportunité**.

But :

> aider à éviter FOMO et améliorer le timing DCA.

---

### `discord_notify.py`

Envoi des messages Discord via webhook.

---

### `config.py`

Configuration globale :

* watchlist
* horaires
* seuils alertes

---

# ⚙️ Configuration

Créer :

```txt
.env
```

Exemple :

```env
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/xxx

WATCHLIST=bitcoin,ethereum,hyperliquid,akash-network,aethir

REPORT_HOUR=07

TZ=Europe/Paris
```

---

# 🐳 Lancement Docker

Build + démarrage :

```bash
docker compose up -d --build
```

Voir logs :

```bash
docker logs -f crypto-assistant
```

Containers actifs :

```bash
docker ps
```

Restart :

```bash
docker restart crypto-assistant
```

Stop :

```bash
docker compose down
```

---

# 🔧 Variables importantes

## Modifier heure du rapport

Dans :

```env
REPORT_HOUR=08
```

→ rapport envoyé à :

```txt
08:30
```

---

## Modifier cryptos surveillées

Exemple :

```env
WATCHLIST=bitcoin,ethereum,solana
```

---

# 🧠 Score Opportunité

Score :

```txt
0 → mauvais timing
100 → contexte plus favorable
```

Le score prend en compte :

* Fear & Greed
* variation 24h
* variation 7 jours
* distance au plus haut historique
* bonus stabilité BTC/ETH

Exemple :

```txt
🎯 Score : 82/100
➡ 🟢 DCA progressif intéressant
```

---

# 📖 Glossaire Crypto

## DCA

**Dollar Cost Averaging**

Acheter progressivement au lieu d’investir tout d’un coup.

Exemple :

```txt
100 €/mois en BTC
```

Plutôt que :

```txt
1200 € en une fois
```

---

## FOMO

**Fear Of Missing Out**

Acheter dans la panique d’un pump :

```txt
"ça monte vite je vais rater le train"
```

Souvent mauvais timing.

---

## ATH

**All Time High**

Plus haut prix historique d’une crypto.

Exemple :

```txt
BTC ATH ≈ 109k $
```

---

## Fear & Greed Index

Indice de sentiment du marché.

Échelle :

```txt
0 → peur extrême
100 → euphorie extrême
```

En général :

```txt
Fear élevé
→ souvent plus intéressant pour DCA

Greed élevé
→ prudence FOMO
```

---

## Pump

Hausse rapide :

```txt
+10% en quelques heures
```

---

## Dump

Baisse rapide :

```txt
-10%
```

---

## Altcoin

Toute crypto autre que BTC.

Exemple :

```txt
ETH
AKT
ATH
HYPE
```

---

## Bull Market

Marché haussier.

Le marché monte sur plusieurs mois.

---

## Bear Market

Marché baissier.

Correction longue.

---

## HODL

Garder ses cryptos longtemps malgré volatilité.

---

## Perpetuals / Perps

Trading avec :

* Long
* Short
* Levier

Très risqué.

Exemple :

Hyperliquid.

---

# 🛣️ Roadmap

## V1 ✅

* rapport Discord
* alertes marché
* score opportunité
* EUR/USD
* Docker
* anti-spam

## V2

* score plus intelligent
* historique SQLite
* tendances IA crypto
* alertes personnalisées
* résumé marché automatique

## V3 (agentique)

Assistant analyste crypto autonome.


