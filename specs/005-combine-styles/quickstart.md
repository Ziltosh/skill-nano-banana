# Quickstart: Combine Multiple Styles

## Prérequis

- Python 3.11+
- Clé API Gemini dans `.env`
- Dépendances installées (`uv sync`)

## Utilisation

### Un seul style (comportement existant)

```bash
python src/generate.py "un château" --style ghibli
```

### Combiner deux styles

```bash
python src/generate.py "une miniature YouTube" --style ghibli --style pixel-art
```

### Combiner avec tous les flags

```bash
python src/generate.py "un poster" --style ghibli --style watercolor --text "CONCERT" --ratio 9:16 --size 2k
```

## Vérification

1. Générer avec un seul `--style` → vérifier que le comportement est identique à avant
2. Générer avec deux `--style` → vérifier que le prompt contient les deux textes de style
3. Vérifier dans `out/history.jsonl` que le champ `style` est une liste
4. Tester avec un style invalide parmi des valides → vérifier le message d'erreur
