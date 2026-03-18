# Quickstart: Nano Banana

## Prérequis

- Python 3.11+
- `uv` installé ([docs](https://docs.astral.sh/uv/))
- Une clé API Google Gemini (avec facturation activée pour la génération d'images)

## Installation

```bash
# Cloner le repo
git clone <repo-url>
cd skill-nano-banana

# Installer les dépendances
uv sync

# Configurer la clé API
cp .env.example .env
# Éditer .env et ajouter votre clé GEMINI_API_KEY
```

## Utilisation

### Générer une image

Dans une conversation Claude Code, dans le répertoire du projet :

```
/generate-image "un chat astronaute sur la lune"
```

L'image est sauvegardée dans `out/` avec un nom dérivé du prompt.

### Appliquer un style

```
/generate-image "un château médiéval" --style ghibli
```

Styles disponibles : `ghibli`, `pixel-art`, `photo-realistic`, `watercolor`

### Transformer une image existante

1. Partagez une image dans le chat
2. Invoquez la commande avec un prompt de transformation :

```
/generate-image "transforme cette image en pixel art"
```

### Créer un style personnalisé

```
/create-style "cyberpunk" "cyberpunk style with bright neon lights, dark background, wet surface reflections"
```

Le style est immédiatement utilisable via `--style cyberpunk`.

## Structure des fichiers

```
out/                  # Images générées (gitignored)
├── history.jsonl     # Historique des générations
└── *.png             # Images
styles.json           # Presets de style
.env                  # Clé API (gitignored)
```

## Vérification

Pour vérifier que tout fonctionne :

1. Vérifier que `.env` contient `GEMINI_API_KEY=...`
2. Lancer `/generate-image "test"` dans Claude Code
3. Vérifier qu'un fichier `out/test.png` a été créé
4. Vérifier qu'une entrée apparaît dans `out/history.jsonl`

## Tests

```bash
uv run pytest
```
