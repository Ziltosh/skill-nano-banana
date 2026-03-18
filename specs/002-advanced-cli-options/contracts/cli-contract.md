# CLI Contract: Options CLI avancées

**Date**: 2026-03-18

## Updated Skill: `/generate-image`

### Invocation

```
/generate-image "<prompt>" [--style <name>] [--model <alias>] [--include <tag>]... [--images <path>]...
```

### Arguments (updated)

| Argument      | Required | Repeatable | Description                                |
| ------------- | -------- | ---------- | ------------------------------------------ |
| `<prompt>`    | Yes      | No         | Description textuelle de l'image           |
| `--style`     | No       | No         | Nom d'un preset de style                   |
| `--model`     | No       | No         | Alias d'un modèle configuré dans models.json |
| `--include`   | No       | Yes        | Tag de ressources à inclure                |
| `--images`    | No       | Yes        | Chemins d'images de référence (chat)       |

### Validation Errors (new)

Retournées AVANT tout appel API. Exit code 3.

**Flag inconnu** :
```json
{
  "success": false,
  "error": "Unknown flag '--foo'. Available flags: --style, --model, --include, --images",
  "code": "INVALID_ARGS"
}
```

**Valeur manquante** :
```json
{
  "success": false,
  "error": "Flag '--style' requires a value",
  "code": "INVALID_ARGS"
}
```

**Prompt manquant** :
```json
{
  "success": false,
  "error": "A prompt is required.\nUsage: generate-image \"<prompt>\" [--style <name>] [--model <alias>] [--include <tag>]\nExample: generate-image \"a cat on the moon\" --style ghibli",
  "code": "INVALID_ARGS"
}
```

### Model Errors (new)

**Alias inconnu** :
```json
{
  "success": false,
  "error": "Unknown model 'xxx'. Available models: flash (default), pro, nano",
  "code": "UNKNOWN_MODEL"
}
```

### Resource Errors (new)

**Tag inexistant** :
```json
{
  "success": false,
  "error": "Resource tag 'xxx' not found. Available tags: face-kim, landscape-ref",
  "code": "UNKNOWN_TAG"
}
```

**Dossier vide** :
```json
{
  "success": false,
  "error": "Resource tag 'xxx' has no images (expected .png, .jpg, .webp files)",
  "code": "EMPTY_RESOURCES"
}
```

### Exit Codes (updated)

| Code | Meaning                              |
| ---- | ------------------------------------ |
| 0    | Succès, image générée                |
| 1    | Erreur de configuration (.env)       |
| 2    | Erreur API Gemini                    |
| 3    | Erreur d'arguments / validation      |
| 4    | Erreur de ressources (tag, modèle)   |

### Success Response (updated)

```json
{
  "success": true,
  "path": "/absolute/path/to/out/image.png",
  "prompt": "le prompt enrichi complet",
  "style": "ghibli",
  "model": "gemini-2.5-flash-image"
}
```

Le champ `model` est ajouté pour traçabilité.
