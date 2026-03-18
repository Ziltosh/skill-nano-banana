# CLI Contract: Combine Multiple Styles

**Date**: 2026-03-18

## Modification du skill `/generate-image`

### Invocation (mise à jour)

```
/generate-image "<prompt>" [--style <style1>] [--style <style2>] ... [--text <text>] [--ratio <ratio>] [--size <size>] [--model <model>] [--include <tag>] [--images <path1> ...]
```

### Argument modifié

| Argument   | Required | Repeatable | Description                                              |
| ---------- | -------- | ---------- | -------------------------------------------------------- |
| `--style`  | No       | **Yes**    | Nom d'un preset de style à appliquer (répétable)        |

### Script sous-jacent (mise à jour)

```bash
python src/generate.py "<prompt>" [--style <style1>] [--style <style2>] ...
```

### Output (stdout, JSON) — mise à jour

**Succès (multiples styles)** :
```json
{
  "success": true,
  "path": "/absolute/path/to/out/image.png",
  "prompt": "prompt enrichi avec les deux styles",
  "style": ["ghibli", "pixel-art"],
  "model": "gemini-2.0-flash-exp",
  "text": null,
  "ratio": "16:9",
  "size": "1k"
}
```

**Succès (un seul style)** :
```json
{
  "success": true,
  "style": ["ghibli"]
}
```

**Succès (aucun style)** :
```json
{
  "success": true,
  "style": null
}
```

**Erreur (style inconnu)** :
```json
{
  "success": false,
  "error": "Unknown style 'inexistant'. Available styles: ghibli, pixel-art, photo-realistic, watercolor",
  "code": "UNKNOWN_STYLE"
}
```

### Exemples

```bash
# Un seul style (rétrocompatible)
python src/generate.py "un chat" --style ghibli

# Deux styles combinés
python src/generate.py "une miniature YouTube" --style ghibli --style pixel-art

# Trois styles
python src/generate.py "un poster" --style ghibli --style pixel-art --style watercolor

# Combiné avec tous les flags
python src/generate.py "un poster" --style ghibli --style pixel-art --text "CONCERT" --ratio 9:16 --size 2k
```
