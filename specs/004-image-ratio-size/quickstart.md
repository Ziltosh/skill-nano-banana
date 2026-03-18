# Quickstart: Image Aspect Ratio & Size

## Prérequis

- Python 3.11+
- Clé API Gemini dans `.env`
- Dépendances installées (`uv sync`)

## Utilisation

### Ratio par défaut (16:9)

```bash
python src/generate.py "un paysage de montagne"
```

### Choisir un ratio

```bash
python src/generate.py "un logo" --ratio 1:1
python src/generate.py "une story Instagram" --ratio 9:16
```

### Choisir une taille

```bash
python src/generate.py "un fond d'écran" --size 4k
python src/generate.py "un aperçu" --size 1k
```

### Combiner ratio et taille

```bash
python src/generate.py "un poster" --ratio 9:16 --size 2k --style ghibli
```

## Vérification

1. Générer une image sans flags → vérifier qu'elle est en 16:9
2. Générer avec `--ratio 1:1` → vérifier qu'elle est carrée
3. Générer avec `--size 4k` → vérifier la résolution
4. Vérifier dans `out/history.jsonl` que les champs `ratio` et `size` sont journalisés
