# Quickstart: Image Text Overlay

## Prérequis

- Python 3.11+
- Clé API Gemini dans `.env` (cf. `.env.example`)
- Dépendances installées (`uv sync`)

## Utilisation

### Ajouter du texte sur une image

```bash
python src/generate.py "un coucher de soleil" --text "VACANCES 2026"
```

Le texte "VACANCES 2026" apparaîtra en majuscules sur l'image générée.

### Combiner avec un style

```bash
python src/generate.py "un château" --text "Bienvenue" --style ghibli
```

### Sans texte (comportement existant)

```bash
python src/generate.py "un paysage"
```

## Vérification

1. Vérifier que l'image est créée dans `out/`
2. Ouvrir l'image et vérifier visuellement que le texte est présent avec la bonne casse
3. Vérifier dans `out/history.jsonl` que le champ `text` est journalisé
