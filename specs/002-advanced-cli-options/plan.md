# Implementation Plan: Options CLI avancées

**Branch**: `002-advanced-cli-options` | **Date**: 2026-03-18 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-advanced-cli-options/spec.md`

## Summary

Ajout de trois améliorations au skill `/generate-image` : (1) validation
stricte des arguments CLI avant exécution, (2) option `--model` pour
choisir le modèle Gemini via un système d'alias configurables dans
`models.json`, (3) option `--include` pour injecter des packs de
ressources (images + prompt contextuel) depuis des dossiers dédiés.

## Technical Context

**Language/Version**: Python 3.11+ (existant)
**Primary Dependencies**: google-genai, Pillow, python-dotenv (existant — aucune nouvelle dépendance)
**Storage**: Fichiers locaux JSON (models.json, resources/*/meta.json)
**Testing**: pytest + unittest.mock (existant)
**Target Platform**: macOS (usage local via Claude Code)
**Project Type**: CLI / Skill Claude Code
**Performance Goals**: Validation des arguments < 100ms, pas de latence ajoutée
**Constraints**: Rétrocompatibilité totale avec les commandes existantes
**Scale/Scope**: Usage personnel, mono-utilisateur

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence |
| --------- | ------ | -------- |
| I. Skill-First Design | PASS | Les nouvelles options s'intègrent dans les skills existants (`/generate-image`). Pas de nouveau point d'entrée. |
| II. Sécurité & Configuration | PASS | Pas de nouvelles données sensibles. Les modèles et ressources sont des fichiers de configuration locaux. |
| III. Tests Standard | PASS | Tests unitaires prévus pour validation d'arguments, résolution de modèles, chargement de ressources. Mocks API maintenus. |
| IV. Simplicité | PASS | Aucune nouvelle dépendance. `models.json` suit le même pattern que `styles.json`. `meta.json` minimaliste (un seul champ). argparse déjà utilisé. |

**Post-Phase 1 re-check**: PASS — la conception reste alignée.

## Project Structure

### Documentation (this feature)

```text
specs/002-advanced-cli-options/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── cli-contract.md
└── tasks.md              # (à générer via /speckit.tasks)
```

### Source Code (repository root)

```text
src/
├── generate.py            # MODIFIÉ: nouveau parsing args, --model, --include
├── config.py              # EXISTANT: inchangé
├── slugify.py             # EXISTANT: inchangé
├── styles.py              # EXISTANT: inchangé
├── history.py             # EXISTANT: inchangé
├── create_style.py        # EXISTANT: inchangé
├── models.py              # NOUVEAU: chargement models.json, résolution alias
└── resources.py           # NOUVEAU: chargement ressources par tag, lecture meta.json

tests/
├── test_generate.py       # MODIFIÉ: tests validation args, --model, --include
├── test_models.py         # NOUVEAU: tests résolution modèles
├── test_resources.py      # NOUVEAU: tests chargement ressources
└── ... (existants inchangés)

models.json                # NOUVEAU: mapping alias → identifiant modèle
resources/                 # NOUVEAU: dossiers de ressources par tag
├── face-kim/              # Exemple
│   ├── meta.json          # {"prompt": "cette personne doit apparaître"}
│   ├── photo1.png
│   └── photo2.jpg
└── ...

.claude/commands/
└── generate-image.md      # MODIFIÉ: documentation --model et --include
```

**Structure Decision**: Extension de la structure plate existante dans `src/`.
Deux nouveaux modules (`models.py`, `resources.py`) suivent le même pattern
que `styles.py`. Pas de réorganisation.

## Complexity Tracking

Aucune violation de constitution. Pas de justification nécessaire.
