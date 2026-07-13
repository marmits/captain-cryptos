# 🚀 Captain Cryptos — Lightweight Crypto Assistant

Assistant crypto léger auto-hébergé avec Docker.

Objectif :

> Recevoir automatiquement un rapport crypto quotidien sur Discord et détecter des opportunités / mouvements de marché sans faire tourner une grosse IA locale.

Pensé pour :

- Ubuntu
- Docker / Docker Compose
- VPS
- VM Proxmox
- faible consommation ressources
- exécution 24/7

---

# ✨ Fonctionnalités

## 📊 Rapport crypto Discord

Le bot envoie automatiquement un rapport complet :

- ✅ au démarrage du container
- ✅ tous les jours à **07:30**
- ✅ prix **EUR + USD**
- ✅ Fear & Greed Index
- ✅ contexte macro crypto
- ✅ score opportunité
- ✅ date / heure du rapport

### Détails

- ✔ Rapport au démarrage container
- ✔ Rapport quotidien 07:30
- ✔ Alertes toutes les 30 min
- ✔ Pump >= +10%
- ✔ Dump <= -7%
- ✔ Anti-spam
- ✔ Reset automatique
- ✔ Macro contexte crypto
- ✔ Score opportunité
- ✔ Docker autonome
- ✔ Pas besoin de cron
- ✔ Redémarrage auto VPS


Exemple :

```txt
📊 Rapport Crypto
🕒 15/06/2026 • 07:30

🌍 Marché
Fear & Greed : 18 (Extreme Fear)

🟢 Contexte
Marché en peur extrême.
DCA progressif renforcé possible.

📈 Macro

₿ BTC dominance : 56.58%
→ BTC reste dominant

💵 Stable dominance : 11.53%
→ Beaucoup de liquidités en attente

📊 Volume global : 51.2B $
→ Activité correcte

━━━━━━━━━━━━━━
BTC
💰 Prix : 55 333 € / 64 013 $
📈 24h : -0.38%
📊 7j : +3.47%
🎯 Score : 78/100
➡ 🟡 Contexte plutôt favorable
````

---

## 🚨 Alertes marché automatiques

Le bot vérifie le marché toutes les :

```txt
30 minutes
```

### 🚀 Pump

Détection :

```txt
>= +10% en 24h
```

Exemple :

```txt
🚀 HYPE

Forte hausse détectée

💰 Prix : 52 € / 61 $
📈 24h : +11.4%

➡ Prudence FOMO
```

---

### 🚨 Dump

Détection :

```txt
<= -7% en 24h
```

Exemple :

```txt
🚨 BTC

Forte baisse détectée

➡ Possible zone de DCA progressif
```

---

## 🔇 Anti-spam Discord

Le projet mémorise les alertes envoyées dans :

```txt
data/state.json
```

Évite :

```txt
🚀 HYPE
🚀 HYPE
🚀 HYPE
```

toutes les 30 minutes.

### Reset automatique

Quand une crypto revient en zone normale :

```txt
-7% < variation < +10%
```

le système réarme automatiquement les alertes.

Exemple :

```txt
HYPE +12%
→ alerte envoyée

HYPE +4%
→ reset

HYPE +11%
→ nouvelle alerte possible
```

---

## 🌍 Macro contexte crypto

Le rapport intègre :

### Fear & Greed Index

Sentiment global du marché :

```txt
0 → peur extrême
100 → euphorie extrême
```

Exemple :

```txt
Fear = 18
→ marché stressé
→ DCA progressif potentiellement plus intéressant
```

---

### ₿ BTC Dominance

Part du marché détenue par Bitcoin.

Permet d’estimer si :

```txt
BTC domine
ou
altcoins dominent
```

Lecture simple :

```txt
> 55%
→ BTC reste fort

< 53%
→ rotation altcoins possible
```

---

### 💵 Stablecoin Dominance

Mesure les liquidités encore en attente :

```txt
USDT
USDC
DAI
FDUSD
USDe
```

Lecture :

```txt
élevée
→ cash encore disponible

faible
→ marché déjà très investi
```

---

### 📊 Volume global marché

Mesure l’activité du marché crypto.

Exemple :

```txt
volume élevé
→ mouvements plus crédibles

volume faible
→ marché calme
```

---

# 🧠 Score opportunité

Score :

```txt
0 → mauvais timing
100 → contexte plus favorable
```

Le score prend en compte :

* Fear & Greed
* variation 24h
* variation 7 jours
* distance au plus haut historique (ATH)
* bonus stabilité BTC/ETH

Exemple :

```txt
🎯 Score : 82/100
➡ 🟢 DCA progressif intéressant
```

Le score n’est **pas un conseil financier**.

Il sert à :

> réduire le FOMO et améliorer le timing DCA.

---

# ⚙️ Architecture

```txt
captain-cryptos/
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
├── .env.example
└── README.md
```

---

## 📂 Rôle des fichiers

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
* Alternative.me Fear & Greed

Responsable de :

* prix crypto
* macro contexte
* formatage EUR/USD

---

### `report.py`

Construit le rapport Discord :

* mise en forme
* contexte marché
* macro lecture
* score opportunité

---

### `alerts.py`

Détection :

* pump
* dump
* anti-spam
* reset automatique

---

### `scoring.py`

Calcule le score opportunité.

---

### `discord_notify.py`

Envoi des messages Discord via webhook.

---

### `config.py`

Configuration globale :

* watchlist
* horaires
* seuils alertes
* timezone

---

# ⚙️ Configuration

Créer :

```txt
.env
```

Exemple :

```env
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/xxx

WATCHLIST=bitcoin,ethereum,hyperliquid,solana,ripple,akash-network,aethir

REPORT_HOUR=07

TZ=Europe/Paris
```

---

## `.env.example`

À versionner dans Git :

```env
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/xxx

WATCHLIST=bitcoin,ethereum,hyperliquid,solana,ripple,akash-network,aethir

REPORT_HOUR=07

TZ=Europe/Paris
```

---

# 🐳 Docker

### Build + démarrage

```bash
docker compose up -d --build
```

---

### Logs

```bash
docker logs -f crypto-assistant
```

---

### Restart

```bash
docker restart crypto-assistant
```

---

### Stop

```bash
docker compose down
```

---

## 🔁 Fonctionnement autonome

Une fois lancé :

```bash
docker compose up -d
```

Le bot fonctionne seul :

* rapport immédiat au démarrage
* rapport quotidien 07:30
* alertes marché toutes les 30 min

Grâce à :

```yaml
restart: unless-stopped
```

le container redémarre automatiquement après reboot VPS.

### Aucun cron requis

Le scheduler est intégré directement dans :

```txt
main.py
```

---

# 🔧 Personnalisation

## Modifier heure du rapport

Dans :

```env
REPORT_HOUR=08
```

↓

rapport envoyé à :

```txt
08:30
```

---

## Modifier cryptos surveillées

Exemple :

```env
WATCHLIST=bitcoin,ethereum,solana,ripple
```

---

## Modifier seuils alertes

Dans :

```txt
app/config.py
```

Exemple :

```python
PUMP_THRESHOLD = 8
DUMP_THRESHOLD = -5
```

---

# 📖 Glossaire Crypto

## DCA

**Dollar Cost Averaging**

Acheter progressivement.

Exemple :

```txt
100 €/mois BTC
```

au lieu de :

```txt
1200 € d’un coup
```

---

## FOMO

**Fear Of Missing Out**

Acheter dans l’émotion.

Exemple :

```txt
“ça pump je vais rater le train”
```

---

## ATH

**All Time High**

Plus haut historique.

---

## Pump

Hausse rapide :

```txt
+10%
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

Marché haussier long.

---

## Bear Market

Marché baissier long.

---

## HODL

Conserver ses cryptos long terme.

---

## Perpetuals / Perps

Trading :

* Long
* Short
* Levier

Très risqué.

Exemple :

```txt
Hyperliquid
```

---

# 🛣️ Roadmap

## V1 ✅

* rapport Discord
* alertes marché
* score opportunité
* EUR/USD
* macro contexte
* Docker
* anti-spam
* reset automatique

---

## V2

* historique SQLite
* score plus intelligent
* alertes personnalisées
* watchlist dynamique
* résumé marché enrichi

---

## V3 (agentique)

Assistant analyste crypto autonome.

