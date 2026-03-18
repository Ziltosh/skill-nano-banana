# Data Model: Smart Output Naming

## Entités modifiées

### OutputName (logique de résolution du nom)

Pas une entité persistée, mais la logique de résolution qui détermine le slug final.

**Entrées** :
- `name: str | None` — valeur du paramètre `--name` (nouveau)
- `image_paths: list[str]` — chemins des images de référence (`--images`)
- `prompt: str` — texte du prompt utilisateur

**Règle de résolution** (par ordre de priorité) :
1. Si `name` est fourni et non vide → `slugify(strip_image_extension(name))`
2. Si `image_paths` contient exactement 1 élément → `slugify(Path(image_paths[0]).stem)`
3. Sinon → `slugify(extract_keywords(prompt))`

**Sortie** : `slug: str` passé à `unique_path(output_dir, slug)`

### Fonctions ajoutées dans `slugify.py`

| Fonction | Signature | Description |
|----------|-----------|-------------|
| `extract_keywords` | `(text: str, max_words: int = 4) -> str` | Filtre les stop words FR/EN, retourne les N premiers mots-clés joints par des espaces |
| `strip_image_extension` | `(name: str) -> str` | Retire l'extension image connue (.png, .jpg, etc.) si présente en fin de chaîne |

### Paramètre CLI ajouté

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--name` | `str` | `None` | Nom forcé pour le fichier de sortie |

### history.jsonl

Aucun changement de schéma. Le champ `output` reflète déjà le chemin complet du fichier, qui contiendra désormais le nom résolu par la nouvelle logique.
