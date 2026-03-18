# Implementation Plan: Gemini Image Generation Skill

**Branch**: `001-gemini-image-skill` | **Date**: 2026-03-18 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-gemini-image-skill/spec.md`

## Summary

Skill Claude Code `/generate-image` permettant de générer des images via
l'API Gemini (`gemini-2.5-flash-image`). Le script Python reçoit un prompt
texte, optionnellement des chemins d'images de référence et un style
prédéfini, appelle l'API, sauvegarde l'image dans `out/` avec un nom
intelligent, et journalise la génération. Un second skill `/create-style`
permet d'ajouter des presets de style personnalisés.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: google-genai, Pillow, python-dotenv
**Storage**: Fichiers locaux (JSON, JSON Lines, PNG)
**Testing**: pytest + unittest.mock
**Target Platform**: macOS (usage local via Claude Code)
**Project Type**: CLI / Skill Claude Code
**Performance Goals**: < 30s de traitement local (hors latence API)
**Constraints**: Nécessite facturation Google Cloud activée (pas de tier gratuit pour l'image generation)
**Scale/Scope**: Usage personnel, mono-utilisateur

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence |
| --------- | ------ | -------- |
| I. Skill-First Design | PASS | Deux skills définis : `/generate-image` et `/create-style`. Entrée texte, sortie fichier. Images du chat transmises via sauvegarde temporaire par Claude. |
| II. Sécurité & Configuration | PASS | Clé API dans `.env`, `.env.example` documenté, `.gitignore` configuré. Erreurs API capturées avec messages lisibles. |
| III. Tests Standard | PASS | pytest + mocks de l'API Gemini. Tests unitaires pour slugification, gestion des styles, parsing d'arguments. |
| IV. Simplicité | PASS | 3 dépendances (google-genai, Pillow, python-dotenv). Un script par skill. Pas d'abstraction prématurée. |

**Post-Phase 1 re-check**: PASS — la conception reste alignée.

## Project Structure

### Documentation (this feature)

```text
specs/001-gemini-image-skill/
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
.claude/
└── commands/
    ├── generate-image.md      # Skill Claude Code (génération)
    └── create-style.md        # Skill Claude Code (création de style)

src/
├── generate.py                # Script principal de génération
├── create_style.py            # Script de création de style
├── config.py                  # Chargement .env, validation clé API
├── styles.py                  # Lecture/écriture styles.json
├── slugify.py                 # Slugification des noms de fichiers
└── history.py                 # Écriture dans history.jsonl

tests/
├── test_generate.py           # Tests génération (avec mocks API)
├── test_create_style.py       # Tests création de style
├── test_config.py             # Tests configuration
├── test_styles.py             # Tests gestion des styles
├── test_slugify.py            # Tests slugification
└── test_history.py            # Tests historique

styles.json                    # Presets de style (versionné)
.env                           # Clé API (gitignored)
.env.example                   # Template de configuration
out/                           # Dossier de sortie (gitignored)
├── history.jsonl              # Log des générations
└── *.png                      # Images générées
pyproject.toml                 # Configuration projet Python/uv
```

**Structure Decision**: Single project, structure plate dans `src/`.
Chaque fichier a une responsabilité unique. Pas de sous-packages —
le projet est suffisamment petit pour rester plat.

## Complexity Tracking

Aucune violation de constitution détectée. Pas de justification nécessaire.
