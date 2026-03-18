# CLI Contract: Image Aspect Ratio & Size

**Date**: 2026-03-18

## Modification du skill `/generate-image`

### Invocation (mise à jour)

```
/generate-image "<prompt>" [--ratio <ratio>] [--size <size>] [--text <text>] [--style <style-name>] [--model <model>] [--include <tag>] [--images <path1> ...]
```

### Nouveaux arguments

| Argument   | Required | Default | Description                                              |
| ---------- | -------- | ------- | -------------------------------------------------------- |
| `--ratio`  | No       | 16:9    | Aspect ratio de l'image (ex: 16:9, 9:16, 1:1, 4:3)     |
| `--size`   | No       | 1k      | Résolution de l'image (1k, 2k, 4k)                      |

### Ratios supportés

`16:9`, `9:16`, `1:1`, `4:3`, `3:4`, `3:2`, `2:3`, `4:5`, `5:4`

### Tailles supportées

`1k`, `2k`, `4k`

### Output (stdout, JSON) — mise à jour

**Succès** :
```json
{
  "success": true,
  "path": "/absolute/path/to/out/generated-image.png",
  "prompt": "le prompt enrichi envoyé à l'API",
  "style": "ghibli",
  "text": "HELLO",
  "ratio": "16:9",
  "size": "1k"
}
```

Les champs `ratio` et `size` sont toujours présents dans le résultat (valeur par défaut ou explicite).

**Erreur (ratio/taille invalide)** :
```json
{
  "success": false,
  "error": "Unknown ratio '7:3'. Available ratios: 16:9, 9:16, 1:1, 4:3, 3:4, 3:2, 2:3, 4:5, 5:4",
  "code": "INVALID_RATIO"
}
```

```json
{
  "success": false,
  "error": "Unknown size '8k'. Available sizes: 1k, 2k, 4k",
  "code": "INVALID_SIZE"
}
```

### Exit Codes (mise à jour)

| Code | Meaning                              |
| ---- | ------------------------------------ |
| 0    | Succès                               |
| 1    | Erreur de configuration (.env)       |
| 2    | Erreur API Gemini                    |
| 3    | Erreur d'entrée (prompt vide)        |
| 4    | Erreur de validation (ratio/taille/modèle/tag invalide) |

### Exemples

```bash
# Défauts (16:9, 1k)
python src/generate.py "un paysage"

# Ratio carré
python src/generate.py "un logo" --ratio 1:1

# Haute résolution portrait
python src/generate.py "un portrait" --ratio 9:16 --size 4k

# Tout combiné
python src/generate.py "un poster" --ratio 9:16 --size 2k --style ghibli --text "CONCERT"
```
