# CLI Contract: Nano Banana Skills

**Date**: 2026-03-18

## Skill: `/generate-image`

### Invocation

```
/generate-image "<prompt>" [--style <style-name>]
```

### Arguments

| Argument      | Required | Description                              |
| ------------- | -------- | ---------------------------------------- |
| `<prompt>`    | Yes      | Description textuelle de l'image à générer |
| `--style`     | No       | Nom d'un preset de style à appliquer     |

### Underlying Script

```bash
python src/generate.py "<prompt>" [--style <style-name>] [--images <path1> <path2> ...]
```

Le flag `--images` est ajouté automatiquement par le skill quand Claude
détecte des images dans le contexte du chat et les sauvegarde en fichiers
temporaires.

### Output (stdout, JSON)

**Succès** :
```json
{
  "success": true,
  "path": "/absolute/path/to/out/generated-image.png",
  "prompt": "le prompt enrichi envoyé à l'API",
  "style": "ghibli"
}
```

**Erreur** :
```json
{
  "success": false,
  "error": "Message d'erreur lisible",
  "code": "API_ERROR|MISSING_KEY|INVALID_KEY|CONTENT_BLOCKED|NETWORK_ERROR"
}
```

### Exit Codes

| Code | Meaning                         |
| ---- | ------------------------------- |
| 0    | Succès, image générée           |
| 1    | Erreur de configuration (.env)  |
| 2    | Erreur API Gemini               |
| 3    | Erreur d'entrée (prompt vide)   |

---

## Skill: `/create-style`

### Invocation

```
/create-style "<style-name>" "<style-description>"
```

### Arguments

| Argument             | Required | Description                           |
| -------------------- | -------- | ------------------------------------- |
| `<style-name>`       | Yes      | Nom du style en kebab-case            |
| `<style-description>`| Yes      | Phrase de style à concaténer au prompt |

### Underlying Script

```bash
python src/create_style.py "<style-name>" "<style-description>" [--force]
```

Le flag `--force` est ajouté par le skill si l'utilisateur confirme
l'écrasement d'un style existant.

### Output (stdout, JSON)

**Succès (création)** :
```json
{
  "success": true,
  "action": "created",
  "name": "cyberpunk-neon",
  "prompt_text": "cyberpunk style with bright neons..."
}
```

**Conflit (style existant, sans --force)** :
```json
{
  "success": false,
  "error": "Style 'ghibli' already exists",
  "code": "STYLE_EXISTS",
  "existing_prompt": "in the style of Studio Ghibli..."
}
```

**Succès (écrasement avec --force)** :
```json
{
  "success": true,
  "action": "replaced",
  "name": "ghibli",
  "prompt_text": "new description..."
}
```

### Exit Codes

| Code | Meaning                           |
| ---- | --------------------------------- |
| 0    | Succès                            |
| 1    | Erreur d'arguments                |
| 2    | Conflit (style existant)          |
