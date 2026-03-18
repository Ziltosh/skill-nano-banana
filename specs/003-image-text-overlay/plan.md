# Implementation Plan: Image Text Overlay

**Branch**: `003-image-text-overlay` | **Date**: 2026-03-18 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/003-image-text-overlay/spec.md`

## Summary

Ajouter un flag optionnel `--text` à la commande `/generate-image` pour insérer du texte sur l'image générée. Le texte est injecté dans le prompt envoyé à l'API Gemini via une instruction explicite qui demande d'écrire le texte exact (casse préservée) sur l'image. Aucune superposition en post-traitement.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: google-genai, Pillow, python-dotenv (existants — aucune nouvelle dépendance)
**Storage**: Fichier `out/history.jsonl` (ajout du champ `text`)
**Testing**: pytest + mocks de l'API Gemini
**Target Platform**: macOS (usage local via Claude Code)
**Project Type**: CLI / Skill Claude Code
**Performance Goals**: N/A (identique au comportement existant)
**Constraints**: Aucune contrainte supplémentaire
**Scale/Scope**: Modification mineure d'un seul fichier source + tests

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principe | Statut | Justification |
|----------|--------|---------------|
| I. Skill-First Design | OK | Le flag `--text` est ajouté au skill existant `/generate-image` |
| II. Sécurité & Configuration | OK | Aucune nouvelle donnée sensible, utilise la clé API existante |
| III. Tests Standard | OK | Tests unitaires prévus pour le nouveau flag et l'enrichissement du prompt |
| IV. Simplicité | OK | Modification mineure, pas de nouvelle dépendance, pas de sur-ingénierie |

Aucune violation. Gate passé.

## Project Structure

### Documentation (this feature)

```text
specs/003-image-text-overlay/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── cli-contract.md
└── tasks.md             # Phase 2 output (/speckit.tasks)
```

### Source Code (repository root)

```text
src/
├── generate.py          # Modification : ajout flag --text + enrichissement prompt
├── history.py           # Modification : ajout paramètre text au log
├── config.py            # Inchangé
├── models.py            # Inchangé
├── resources.py         # Inchangé
├── slugify.py           # Inchangé
├── styles.py            # Inchangé
└── create_style.py      # Inchangé

tests/
├── test_generate.py     # Ajout tests pour --text
└── test_history.py      # Ajout test pour champ text dans le log
```

**Structure Decision**: Structure existante conservée. Seuls `generate.py` et `history.py` sont modifiés. Aucun nouveau fichier source.
