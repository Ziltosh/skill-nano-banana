# Data Model: Gemini Image Generation Skill

**Date**: 2026-03-18
**Branch**: `001-gemini-image-skill`

## Entities

### StylePreset

Représente un style prédéfini applicable à un prompt de génération.

| Field       | Type   | Description                                          |
| ----------- | ------ | ---------------------------------------------------- |
| name        | string | Identifiant unique du style (kebab-case, ex: "ghibli") |
| prompt_text | string | Phrase de style concaténée au prompt utilisateur     |

**Storage**: Fichier `styles.json` à la racine du projet.
**Format**: Objet JSON plat `{ "name": "prompt_text", ... }`

**Styles initiaux** :
- `ghibli` → "in the style of Studio Ghibli animation, soft watercolor textures, whimsical and dreamlike atmosphere"
- `pixel-art` → "as detailed pixel art, retro 16-bit video game style, crisp pixels"
- `photo-realistic` → "photorealistic, ultra-detailed, professional photography, natural lighting"
- `watercolor` → "as a traditional watercolor painting, soft edges, paper texture, fluid colors"

**Règles** :
- Le nom DOIT être unique (clé du JSON)
- Le nom DOIT être en kebab-case (lettres minuscules, chiffres, tirets)
- Le prompt_text DOIT être en anglais (langue de l'API Gemini)

---

### GenerationLogEntry

Représente une entrée dans l'historique des générations.

| Field      | Type     | Description                                        |
| ---------- | -------- | -------------------------------------------------- |
| timestamp  | string   | Date/heure ISO 8601 (ex: "2026-03-18T14:30:00")   |
| prompt     | string   | Prompt texte original de l'utilisateur             |
| style      | string?  | Nom du style appliqué (null si aucun)              |
| output     | string   | Chemin relatif du fichier généré (ex: "out/chat.png") |
| success    | boolean  | True si la génération a réussi                     |
| error      | string?  | Message d'erreur si échec (null si succès)         |

**Storage**: Fichier `out/history.jsonl` (JSON Lines, une entrée par ligne).
**Règles** :
- Append-only : on ne modifie jamais les entrées existantes
- Trié chronologiquement par construction (append séquentiel)

---

### GeneratedImage

Fichier image résultant d'une génération réussie.

| Field     | Type   | Description                                    |
| --------- | ------ | ---------------------------------------------- |
| filename  | string | Nom du fichier (slug du prompt + extension)    |
| format    | string | Format de l'image (PNG par défaut)             |
| directory | string | Toujours `out/` à la racine du projet          |

**Règles de nommage** :
1. Slugifier le prompt : normaliser Unicode → ASCII, lowercase, remplacer espaces/ponctuation par `-`, tronquer à 50 caractères
2. Ajouter l'extension `.png`
3. Si le fichier existe, ajouter un suffixe numérique : `slug-2.png`, `slug-3.png`, etc.

## File Layout

```text
project-root/
├── .env                  # GEMINI_API_KEY=xxx (gitignored)
├── .env.example          # GEMINI_API_KEY=your_key_here
├── styles.json           # Style presets (versionné)
├── out/                  # Dossier de sortie (gitignored)
│   ├── history.jsonl     # Log des générations
│   ├── un-chat.png       # Image générée
│   └── un-chat-2.png     # Collision résolue
└── src/
    └── ...               # Code source Python
```

## State Transitions

Aucune machine à états complexe. Le flux est linéaire :

1. **Input** → Prompt texte + (optionnel) images de référence + (optionnel) style
2. **Processing** → Enrichissement du prompt avec style → Appel API Gemini
3. **Output** → Sauvegarde image dans `out/` → Log dans `history.jsonl` → Retour chemin à l'utilisateur

En cas d'erreur à l'étape 2 ou 3 :
- Log l'échec dans `history.jsonl` (success=false, error=message)
- Aucun fichier partiel dans `out/`
- Message d'erreur retourné à l'utilisateur
