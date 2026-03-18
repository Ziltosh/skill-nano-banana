# CLI Contract: Image Text Overlay

**Date**: 2026-03-18

## Modification du skill `/generate-image`

### Invocation (mise à jour)

```
/generate-image "<prompt>" [--text <text>] [--style <style-name>] [--model <model>] [--include <tag>] [--images <path1> ...]
```

### Nouvel argument

| Argument   | Required | Description                                              |
| ---------- | -------- | -------------------------------------------------------- |
| `--text`   | No       | Texte à afficher sur l'image, casse préservée            |

### Script sous-jacent (mise à jour)

```bash
python src/generate.py "<prompt>" [--text "<text>"] [--style <style-name>] [--model <model>] [--include <tag>] [--images <path1> ...]
```

### Output (stdout, JSON) — mise à jour

**Succès** :
```json
{
  "success": true,
  "path": "/absolute/path/to/out/generated-image.png",
  "prompt": "le prompt enrichi envoyé à l'API",
  "style": "ghibli",
  "text": "VACANCES 2026"
}
```

Le champ `text` est présent uniquement si `--text` a été fourni (non vide).

**Erreur** : Inchangé (mêmes codes d'erreur existants).

### Exit Codes

Inchangés par rapport au contrat existant.

### Exemples

```bash
# Texte en majuscules
python src/generate.py "un logo" --text "ACME CORP"

# Texte mixte avec style
python src/generate.py "un poster" --text "Concert 2026" --style pixel-art

# Sans texte (comportement existant inchangé)
python src/generate.py "un paysage"

# Texte vide (ignoré, comme si --text absent)
python src/generate.py "un paysage" --text ""
```
