# Livrables finaux — AI Sentiment Analyzer

Ce document associe le contenu du dépôt aux livrables demandés dans l'énoncé.

## 1. Code source complet

Le code est organisé en deux applications :

- `backend/` : API FastAPI, validation Pydantic, services Gemini et Text-Processing, tests Pytest.
- `frontend/` : interface React + TypeScript + Tailwind CSS.

Le fichier `.env` réel n'est pas livré et n'est pas suivi par Git. Seuls les fichiers `.env.example` sont fournis.

## 2. Documentation de l'architecture et du fonctionnement

- [Architecture SOA](ARCHITECTURE.md) — composants, responsabilités et diagramme Mermaid.
- [Guide d'installation](SETUP.md) — installation et démarrage local.
- [README principal](../README.md) — présentation, technologies et commandes principales.

## 3. Description du service Web REST

- [Documentation REST](API.md) — endpoints, requêtes JSON, réponses et codes d'erreur.
- Swagger interactif : `http://localhost:8000/docs` lorsque FastAPI est lancé.

Endpoints principaux :

| Méthode | Endpoint | Fonction |
|---|---|---|
| GET | `/` | Vérifie que l'API fonctionne |
| GET | `/api/health` | Vérifie l'état du backend |
| POST | `/api/analyze` | Analyse avec Google Gemini |
| POST | `/api/analyze/public` | Analyse avec le service public de comparaison |

## 4. Résultats des tests

- [Rapport de tests](TEST_REPORT.md)
- Suite automatisée : `10 passed` lors de la dernière exécution.
- Les appels aux fournisseurs externes sont mockés dans les tests automatisés.
- La compilation de production du frontend passe avec `npm run build`.

Commande de vérification :

```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest -v

cd ..\frontend
npm run build
```

## 5. Captures d'écran à fournir

Le dossier [screenshots](screenshots/README.md) indique les captures à prendre depuis l'application réelle :

1. Tableau de bord initial.
2. Résultat Gemini positif.
3. Résultat de l'API publique.
4. Mode Compare avec les deux résultats.
5. Liste des endpoints dans Swagger.
6. Requête réussie dans Swagger.
7. Erreur de validation pour texte vide ou trop long.

Les captures doivent être prises après le démarrage de FastAPI et de Vite. Aucune image externe ne doit être utilisée comme preuve du fonctionnement du projet.

## 6. Démonstration proposée

### Introduction — 30 secondes

Présenter l'objectif : analyser automatiquement le sentiment d'un texte avec Google Gemini via un backend FastAPI.

### Architecture — 1 minute

Expliquer le chemin : React → FastAPI → Gemini, puis le retour JSON vers React. Mentionner que la clé API reste uniquement côté backend.

### Fonctionnement — 1 à 2 minutes

Tester successivement :

- Texte positif : `This product is excellent and I love it.`
- Texte négatif : `The service is terrible and disappointing.`
- Texte neutre : `The store opens at nine o'clock.`

Présenter les modes Gemini, Public API et Compare.

### REST et validation — 1 minute

Ouvrir Swagger, montrer `POST /api/analyze`, puis tester un texte vide ou de plus de 5 000 caractères pour obtenir une réponse `422`.

### Conclusion — 30 secondes

Rappeler les concepts SOA : services indépendants, communication REST/JSON, séparation des responsabilités, validation et gestion des erreurs.

## Checklist de remise

- [x] Code source backend et frontend
- [x] Documentation architecture
- [x] Description du service REST
- [x] Tests automatisés et rapport
- [ ] Captures d'écran réelles ajoutées dans `docs/screenshots/`
- [ ] Démonstration effectuée avec les services externes disponibles
- [x] Clés et fichiers `.env` exclus du dépôt Git
