# Implementation Plan: Image Aspect Ratio & Size

**Branch**: `004-image-ratio-size` | **Date**: 2026-03-18 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/004-image-ratio-size/spec.md`

## Summary

Ajouter les flags `--ratio` et `--size` à la commande `/generate-image` pour contrôler l'aspect ratio (16:9 par défaut) et la résolution (1k par défaut, supporte 2k et 4k). Les paramètres sont transmis à l'API Gemini via `types.ImageConfig` dans la configuration de génération.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: google-genai, Pillow, python-dotenv (existants — aucune nouvelle dépendance)
**Storage**: Fichier `out/history.jsonl` (ajout des champs `ratio` et `size`)
**Testing**: pytest + mocks de l'API Gemini
**Target Platform**: macOS (usage local via Claude Code)
**Project Type**: CLI / Skill Claude Code
**Performance Goals**: N/A (identique au comportement existant)
**Constraints**: Aucune contrainte supplémentaire
**Scale/Scope**: Modification mineure de `generate.py` et `history.py` + tests

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principe | Statut | Justification |
|----------|--------|---------------|
| I. Skill-First Design | OK | Flags ajoutés au skill existant `/generate-image` |
| II. Sécurité & Configuration | OK | Aucune donnée sensible ajoutée |
| III. Tests Standard | OK | Tests unitaires prévus pour les nouveaux flags et la validation |
| IV. Simplicité | OK | 0 nouvelle dépendance, modification ciblée de 2 fichiers |

Aucune violation. Gate passé.

## Project Structure

### Documentation (this feature)

```text
specs/004-image-ratio-size/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── cli-contract.md
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks)
```

### Source Code (repository root)

```text
src/
├── generate.py          # Modification : ajout flags --ratio, --size + ImageConfig
├── history.py           # Modification : ajout paramètres ratio et size au log
├── config.py            # Inchangé
├── models.py            # Inchangé
├── resources.py         # Inchangé
├── slugify.py           # Inchangé
├── styles.py            # Inchangé
└── create_style.py      # Inchangé

tests/
├── test_generate.py     # Ajout tests pour --ratio, --size
└── test_history.py      # Ajout test pour champs ratio/size dans le log
```

**Structure Decision**: Structure existante conservée. Seuls `generate.py` et `history.py` sont modifiés.
