# Implementation Plan: Smart Output Naming

**Branch**: `006-smart-output-naming` | **Date**: 2026-03-18 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/006-smart-output-naming/spec.md`

## Summary

Améliorer le nommage des fichiers de sortie avec une logique à 3 niveaux de priorité : `--name` (forçage manuel) > nom de l'image de référence unique > extraction de mots-clés du prompt. Remplace le slug brut tronqué actuel par un nommage intelligent et lisible.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: google-genai, Pillow, python-dotenv (existants — aucune nouvelle dépendance)
**Storage**: Fichiers PNG dans `out/`, historique `out/history.jsonl`
**Testing**: pytest + mocks
**Target Platform**: macOS (usage local via Claude Code)
**Project Type**: CLI / Skill Claude Code
**Performance Goals**: N/A (opération locale instantanée)
**Constraints**: Noms de fichiers compatibles tous OS, max ~50 caractères
**Scale/Scope**: Usage personnel, pas de contraintes de volumétrie

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principe | Statut | Notes |
|----------|--------|-------|
| I. Skill-First Design | **PASS** | Le skill `/generate-image` reste le point d'entrée, `--name` est un nouveau flag CLI. Fichiers dans `out/`. |
| II. Sécurité & Configuration | **PASS** | Aucune donnée sensible ajoutée, pas de nouvelle variable d'environnement. |
| III. Tests Standard | **PASS** | Tests unitaires prévus pour `extract_keywords()`, nommage conditionnel, et `--name` validation. Pas d'appel API. |
| IV. Simplicité | **PASS** | Pas de nouvelle dépendance. Logique de mots-clés = liste de stop words + filtrage simple. Pas de NLP. |

## Project Structure

### Documentation (this feature)

```text
specs/006-smart-output-naming/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── cli-contract.md
└── tasks.md             # Phase 2 output (via /speckit.tasks)
```

### Source Code (repository root)

```text
src/
├── generate.py          # MODIFIER: ajouter param name, logique de nommage
├── slugify.py           # MODIFIER: ajouter extract_keywords()
├── config.py            # inchangé
├── history.py           # inchangé
├── models.py            # inchangé
├── resources.py         # inchangé
└── styles.py            # inchangé

tests/
├── test_slugify.py      # MODIFIER: tests pour extract_keywords()
├── test_generate.py     # MODIFIER: tests pour --name et nommage par image
├── test_generate_images.py  # MODIFIER: vérifier nommage avec images de référence
└── test_args_validation.py  # MODIFIER: tests validation --name
```

**Structure Decision**: Projet monolithique existant, pas de restructuration nécessaire. Les modifications portent sur 2 fichiers sources (`slugify.py`, `generate.py`) et 4 fichiers de tests.
