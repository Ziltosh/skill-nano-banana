# Research: Gemini Image Generation Skill

**Date**: 2026-03-18
**Branch**: `001-gemini-image-skill`

## Decision 1: Gemini Model for Image Generation

**Decision**: Utiliser `gemini-2.5-flash-image` comme modèle principal.

**Rationale**:
- Modèle stable GA, bon rapport qualité/prix ($0.039/image)
- Supporte texte-vers-image ET image-vers-image (édition avec références)
- Accepte jusqu'à 10 images de référence en entrée
- Retourne les images inline en tant qu'objets PIL.Image
- Haute limite de débit : 300 RPM, 10 000 RPD (tier 1)

**Alternatives considered**:
- `imagen-4.0-generate-001` : meilleure qualité photoréaliste mais ne supporte pas l'image-to-image avec contexte conversationnel
- `gemini-3-pro-image-preview` : qualité supérieure mais 3.4x plus cher, en preview
- `gemini-2.0-flash-exp-image-generation` : expérimental, pas garanti stable

## Decision 2: Python SDK

**Decision**: Utiliser `google-genai` (nouveau SDK).

**Rationale**:
- Le SDK `google-generativeai` est deprecated depuis novembre 2025
- `google-genai` est le SDK officiel actuel
- API simple : `client.models.generate_content()` avec `response_modalities=["Text", "Image"]`
- Retourne directement des objets PIL.Image via `part.as_image()`
- Installation : `uv add google-genai Pillow`

**Alternatives considered**:
- `google-generativeai` : deprecated, ne pas utiliser
- Appels HTTP directs : inutilement complexe quand un SDK existe

## Decision 3: Mécanisme d'accès aux images du chat

**Decision**: Le skill (fichier .md) instruit Claude de sauvegarder les images du contexte en fichiers temporaires, puis passe leurs chemins au script Python.

**Rationale**:
- Les skills Claude Code n'ont PAS d'accès programmatique aux images du chat
- La variable `$ARGUMENTS` ne contient que du texte
- MAIS : Claude lui-même peut voir les images dans la conversation et les écrire sur disque via son outil Write
- Flow : Claude sauvegarde les images → passe les chemins au script → le script les charge avec PIL

**Alternatives considered**:
- Demander à l'utilisateur de passer des chemins de fichiers manuellement : mauvaise UX, contre l'esprit de la spec
- Encoder les images en base64 dans les arguments : trop volumineux, risque de dépassement

## Decision 4: Format du skill Claude Code

**Decision**: Utiliser le format `.claude/commands/generate-image.md` (ancien format commandes slash).

**Rationale**:
- Le projet utilise déjà `.claude/commands/` pour les commandes speckit
- Cohérence avec la structure existante
- Le format `.claude/skills/SKILL.md` (nouveau) est aussi valide mais ajouterait un dossier supplémentaire
- Les deux formats sont équivalents fonctionnellement

**Alternatives considered**:
- `.claude/skills/generate-image/SKILL.md` : format plus récent mais pas nécessaire ici, ajoute de la complexité structurelle

## Decision 5: Stockage des styles

**Decision**: Fichier JSON unique `styles.json` à la racine du projet.

**Rationale**:
- Format simple, lisible, éditable manuellement
- Un seul fichier à gérer (principe de simplicité)
- Structure : `{"nom-style": "phrase de style en anglais"}`
- Facile à charger en Python avec `json.load()`

**Alternatives considered**:
- YAML : dépendance supplémentaire (PyYAML), pas justifié pour un simple key-value
- TOML : même problème, over-engineering
- Un fichier par style : dispersion inutile

## Decision 6: Format de l'historique

**Decision**: Fichier JSON Lines (`history.jsonl`) dans le dossier `out/`.

**Rationale**:
- Format append-only naturel (une ligne JSON par entrée)
- Lisible directement par un humain ou par Claude
- Facile à parser programmatiquement si besoin futur
- Pas de risque de corruption (chaque ligne est indépendante)
- Emplacement dans `out/` : proximité logique avec les images générées

**Alternatives considered**:
- CSV : moins structuré, problèmes d'échappement avec les prompts contenant des virgules
- JSON array : risque de corruption si le processus est interrompu en pleine écriture
- SQLite : over-engineering pour un log simple

## Decision 7: Slugification des noms de fichiers

**Decision**: Slugifier le prompt en gardant les 50 premiers caractères, convertis en kebab-case ASCII.

**Rationale**:
- Lisible et descriptif (ex: `un-chat-astronaute-sur-la-lune.png`)
- Limite de longueur pour éviter les noms de fichiers trop longs
- Suffixe numérique si collision (ex: `un-chat-2.png`)
- Implémentation simple avec `re.sub` et `unicodedata.normalize`

**Alternatives considered**:
- UUID : illisible, contre la spec (FR-005)
- Timestamp seul : pas descriptif
- Hash du prompt : illisible
