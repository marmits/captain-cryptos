# Instructions
## Discord
Créer un Webhooks sur discord.
- Clique droit sur le serveur
- Paramètres du serveur -> intégrations -> webhook
- Choisir le salon de destination.
- Créer/Compléter `.env` (Ex: `.env.exemple`)

https://discord.com/api/webhooks/xxx/xxx-xxx

## Docker
* `docker compose down`
* `docker compose up -d --build`
	- Rebuild l’image Docker. (si modifications)
* `docker logs -f crypto-assistant` => affiche ce que la salon discord recevra.

---
→ Rapport complet Discord au demarrage container et à 7h30 tous les jours

+ Toutes les 30 min (alertes)

→ seulement si :

- pump >= +10%
- dump <= -7%
---


## Contextes MACRO avec api gratuites (utilisés dans les scripts)

- Fear & Greed `api.alternative.me`
  > Niveau de peur ou d’euphorie du marché. Sentiment marché pour éviter FOMO ou panique
- Bitcoin Dominance `api.coingecko.com`
  > part du marché détenue par BTC. 
- Stablecoin dominance `api.coingecko.com`
  > Combien d’argent attend “sur le banc”.
- Volume marché total `api.coingecko.com`
  > Si le marché est actif ou calme

### à voir :
- Funding Rate (excellent mais plus trading)
  > Si trop de gens sont long ou short.
- Open Interest
  > Quantité de levier ouvert. => surchauffe, liquidations possibles
- Macro marché global (US)
  > Dollar Index (DXY) => dollar fort : crypto souffre
- Taux FED 
  > Si restrictive => risque baisse

