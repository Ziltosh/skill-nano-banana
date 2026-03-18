# Implementation Plan: Combine Multiple Styles

**Branch**: `005-combine-styles` | **Date**: 2026-03-18 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/005-combine-styles/spec.md`

## Summary

Rendre le flag `--style` répétable pour combiner plusieurs styles sur une même génération. Les textes des styles sont concaténés dans le prompt. Le champ `style` dans le résultat JSON et l'historique passe de string à liste de strings.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: google-genai, Pillow, python-dotenv (existants — aucune nouvelle dépendance)
**Storage**: Fichier `out/history.jsonl` (champ `style` : string → list[string])
**Testing**: pytest + mocks de l'API Gemini
**Target Platform**: macOS (usage local via Claude Code)
**Project Type**: CLI / Skill Claude Code
**Performance Goals**: N/A
**Constraints**: Rétrocompatibilité : l'usage avec un seul `--style` ou sans doit fonctionner identiquement
**Scale/Scope**: Modification ciblée de `generate.py` et `history.py`

## Constitution Check

| Principe | Statut | Justification |
|----------|--------|---------------|
| I. Skill-First Design | OK | Modification du skill existant `/generate-image` |
| II. Sécurité & Configuration | OK | Aucune donnée sensible |
| III. Tests Standard | OK | Tests unitaires prévus |
| IV. Simplicité | OK | 0 nouvelle dépendance, changement mineur d'argparse |

Aucune violation. Gate passé.

## Project Structure

### Documentation (this feature)

```text
specs/005-combine-styles/
├── plan.md
├── research.md
├── data-model.md
├── contracts/
│   └── cli-contract.md
├── quickstart.md
└── tasks.md
```

### Source Code (repository root)

```text
src/
├── generate.py          # Modification : --style repeatable, boucle de validation, concaténation
├── history.py           # Modification : champ style de str|None à list[str]|None
└── ...                  # Inchangés

tests/
├── test_generate.py     # Ajout tests multi-styles
├── test_generate_styles.py  # Ajout tests combinaison
└── test_history.py      # Ajout test champ style liste
```

**Structure Decision**: Structure existante conservée. Seuls `generate.py` et `history.py` sont modifiés.
