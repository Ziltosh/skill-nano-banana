# Data Model: Options CLI avancées

**Date**: 2026-03-18
**Branch**: `002-advanced-cli-options`

## New Entities

### ModelConfig

Représente un modèle de génération configurable par alias.

| Field      | Type   | Description                                          |
| ---------- | ------ | ---------------------------------------------------- |
| alias      | string | Nom court du modèle (ex: "flash", "pro")             |
| model_id   | string | Identifiant complet du modèle API (ex: "gemini-2.5-flash-image") |

**Storage**: Fichier `models.json` à la racine du projet.
**Format**:
```json
{
  "flash": "gemini-2.5-flash-image",
  "pro": "gemini-3-pro-image-preview",
  "nano": "gemini-3.1-flash-image-preview",
  "_default": "flash"
}
```

**Règles**:
- L'alias DOIT être en kebab-case (lettres minuscules, chiffres, tirets)
- Le champ `_default` DOIT contenir un alias existant dans le fichier
- Si `models.json` est absent, le modèle `gemini-2.5-flash-image` est utilisé en fallback

---

### ResourceTag

Représente un pack de ressources identifié par un tag.

| Field      | Type     | Description                                        |
| ---------- | -------- | -------------------------------------------------- |
| tag        | string   | Identifiant du pack (nom du dossier, kebab-case)   |
| images     | list     | Chemins des fichiers image (PNG, JPG, WEBP)        |
| prompt     | string?  | Prompt contextuel depuis meta.json (null si absent) |

**Storage**: Sous-dossier de `resources/` à la racine du projet.
**Structure**:
```
resources/
└── face-kim/
    ├── meta.json          # optionnel: {"prompt": "texte contextuel"}
    ├── photo1.png
    ├── photo2.jpg
    └── photo3.webp
```

**Règles**:
- Le tag correspond au nom du dossier sous `resources/`
- Seuls les fichiers avec extensions `.png`, `.jpg`, `.jpeg`, `.webp` sont chargés
- `meta.json` est optionnel — si absent, seules les images sont envoyées
- `meta.json` contient un seul champ `prompt` (string)
- Un dossier vide (sans images) produit une erreur

## Modified Entities

### GenerationRequest (from feature 001)

Ajout de champs :

| Field          | Type     | Description                                    |
| -------------- | -------- | ---------------------------------------------- |
| model          | string?  | Alias du modèle à utiliser (null = défaut)     |
| include_tags   | list     | Liste des tags de ressources à inclure         |

### CLI Arguments (formalized)

Structure complète des arguments acceptés par `generate.py` :

| Argument       | Required | Type       | Description                              |
| -------------- | -------- | ---------- | ---------------------------------------- |
| `prompt`       | Yes      | positional | Description textuelle de l'image         |
| `--style`      | No       | string     | Nom du preset de style                   |
| `--model`      | No       | string     | Alias du modèle                          |
| `--include`    | No       | string[]   | Tags de ressources (répétable)           |
| `--images`     | No       | string[]   | Chemins d'images de référence (chat)     |

## Prompt Enrichment Order

Le prompt final est construit par concaténation dans cet ordre :

1. **Prompt utilisateur** (obligatoire)
2. **Prompts contextuels** des `--include` tags (meta.json, dans l'ordre des tags)
3. **Phrase de style** du `--style` preset

Séparateur : `, ` (virgule espace)
