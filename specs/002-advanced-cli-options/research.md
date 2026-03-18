# Research: Options CLI avancées

**Date**: 2026-03-18
**Branch**: `002-advanced-cli-options`

## Decision 1: Validation des arguments CLI

**Decision**: Utiliser `argparse` (déjà en place) avec `exit_on_error=False`
pour capturer les erreurs et les reformuler en JSON propre.

**Rationale**:
- argparse est déjà utilisé dans `generate.py` et `create_style.py`
- `exit_on_error=False` (Python 3.9+) permet de capturer les erreurs
  au lieu de quitter brutalement, pour retourner un JSON d'erreur
- Pas de nouvelle dépendance (Constitution §IV)

**Alternatives considered**:
- `click` : plus ergonomique mais ajoute une dépendance
- `typer` : idem, dépendance superflue
- parsing manuel : fragile et non-standard

## Decision 2: Structure de models.json

**Decision**: Même pattern que `styles.json` — objet JSON plat avec
un champ spécial `_default` pour le modèle par défaut.

**Rationale**:
- Cohérence avec `styles.json` (même pattern = moins de charge cognitive)
- Le champ `_default` est simple et sans ambiguïté
- Format : `{"flash": "gemini-2.5-flash-image", "pro": "gemini-3-pro-image-preview", "_default": "flash"}`

**Alternatives considered**:
- Objet imbriqué avec `default: true` sur chaque entrée : plus complexe
- TOML/YAML : dépendance supplémentaire

## Decision 3: Chargement des ressources par tag

**Decision**: Scanner le dossier `resources/<tag>/` pour les fichiers
image (PNG, JPG, WEBP) et lire optionnellement `meta.json`.

**Rationale**:
- Convention simple : un dossier = un tag
- Formats filtrés par extension (pas de parsing de type MIME)
- `meta.json` optionnel avec un seul champ `prompt` (clarification spec)
- Utilisation de `pathlib.Path.glob()` pour lister les images

**Alternatives considered**:
- Registre centralisé des tags : over-engineering pour un usage personnel
- Détection automatique de type MIME : plus robuste mais plus lent

## Decision 4: Ordre d'enrichissement du prompt

**Decision**: Le prompt final est construit dans cet ordre :
1. Prompt utilisateur original
2. Prompt contextuel des `--include` (meta.json)
3. Phrase de style `--style`

**Rationale**:
- Le prompt utilisateur est l'intention principale
- Les ressources ajoutent du contexte (personnes, lieux)
- Le style est la couche esthétique finale
- Cet ordre produit des prompts naturels

**Alternatives considered**:
- Style avant include : moins intuitif
- Tout concaténer sans ordre : résultats imprévisibles
