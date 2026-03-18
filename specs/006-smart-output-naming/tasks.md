# Tasks: Smart Output Naming

**Input**: Design documents from `/specs/006-smart-output-naming/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Inclus (Constitution Principe III : tests unitaires obligatoires).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Foundational (Blocking Prerequisites)

**Purpose**: Nouvelles fonctions utilitaires dans `slugify.py` nécessaires à toutes les user stories.

**⚠️ CRITICAL**: Toutes les user stories dépendent de ces fonctions.

- [X] T001 [P] Add `STOP_WORDS` constant (FR + EN, ~120 words) and `extract_keywords(text: str, max_words: int = 4) -> str` function in `src/slugify.py`
- [X] T002 [P] Add `strip_image_extension(name: str) -> str` function in `src/slugify.py` — strips known image extensions (.png, .jpg, .jpeg, .gif, .webp) from end of string
- [X] T003 [P] Add tests for `extract_keywords()` in `tests/test_slugify.py` — cover: prompt court, prompt long (>4 mots-clés), prompt uniquement stop words (fallback vide), prompt mixte FR/EN, prompt 1-2 mots
- [X] T004 [P] Add tests for `strip_image_extension()` in `tests/test_slugify.py` — cover: nom avec .png, nom avec .jpg, nom sans extension, nom avec .v2 (non image, conservé), nom avec .jpeg

**Checkpoint**: Fonctions utilitaires prêtes et testées, les user stories peuvent commencer.

---

## Phase 2: User Story 1 - Nom basé sur l'image de référence unique (Priority: P1) 🎯 MVP

**Goal**: Quand une seule image est fournie via `--images`, le fichier de sortie reprend le nom de base de cette image.

**Independent Test**: Exécuter `generate "modifie" --images mon-logo.png` et vérifier que la sortie est `out/mon-logo.png`.

### Tests for User Story 1

- [X] T005 [P] [US1] Add test in `tests/test_generate_images.py` — single reference image: output filename matches image basename (slugified)
- [X] T006 [P] [US1] Add test in `tests/test_generate_images.py` — single reference image with special chars in name: slugified correctly
- [X] T007 [P] [US1] Add test in `tests/test_generate_images.py` — single reference image in subdirectory: only basename used, not path

### Implementation for User Story 1

- [X] T008 [US1] Add `name: str | None = None` parameter to `generate_image()` function signature in `src/generate.py`
- [X] T009 [US1] Replace naming logic (lines 228-230) in `src/generate.py` with 3-level resolution: if `name` → `slugify(strip_image_extension(name))`, elif single `image_paths` → `slugify(Path(image_paths[0]).stem)`, else → `slugify(extract_keywords(prompt))`
- [X] T010 [US1] Add import for `extract_keywords`, `strip_image_extension` from `src.slugify` in `src/generate.py`

**Checkpoint**: Génération avec une seule image de référence produit un fichier nommé d'après l'image.

---

## Phase 3: User Story 2 - Forçage du nom via --name (Priority: P1)

**Goal**: Le paramètre `--name` permet de forcer le nom du fichier de sortie, avec la priorité la plus haute.

**Independent Test**: Exécuter `generate "un chat" --name "resultat"` et vérifier que la sortie est `out/resultat.png`.

### Tests for User Story 2

- [X] T011 [P] [US2] Add test in `tests/test_generate.py` — `--name` forces output filename
- [X] T012 [P] [US2] Add test in `tests/test_generate.py` — `--name` takes priority over single `--images`
- [X] T013 [P] [US2] Add test in `tests/test_generate.py` — `--name` with image extension stripped (e.g., "logo.png" → "logo")
- [X] T014 [P] [US2] Add test in `tests/test_args_validation.py` — `--name ""` (empty) returns error with code `INVALID_ARGS`
- [X] T015 [P] [US2] Add test in `tests/test_args_validation.py` — `--name "@#$"` (only special chars, empty after slugify) returns error with code `INVALID_ARGS`

### Implementation for User Story 2

- [X] T016 [US2] Add `--name` argument to `parse_args()` in `src/generate.py`
- [X] T017 [US2] Pass `args.name` to `generate_image()` call in `main()` in `src/generate.py`
- [X] T018 [US2] Add validation in `generate_image()` in `src/generate.py` — if `name` is provided but empty or produces empty slug after `slugify(strip_image_extension(name))`, return error `{"success": False, "error": "...", "code": "INVALID_ARGS"}`

**Checkpoint**: Le paramètre `--name` fonctionne et a la priorité maximale.

---

## Phase 4: User Story 3 - Nom court par extraction de mots-clés (Priority: P2)

**Goal**: Quand le nom est basé sur le prompt (pas de `--name`, pas d'image unique), le système extrait 3-4 mots-clés au lieu de slugifier tout le prompt.

**Independent Test**: Exécuter `generate "un magnifique paysage de montagne enneigée"` et vérifier un nom court comme `paysage-montagne-enneigee.png`.

### Tests for User Story 3

- [X] T019 [P] [US3] Add test in `tests/test_generate.py` — prompt without images: output named with keywords (not full slug)
- [X] T020 [P] [US3] Add test in `tests/test_generate.py` — long prompt (200+ chars): output name has max 4 keywords
- [X] T021 [P] [US3] Add test in `tests/test_generate.py` — multiple reference images: output named with prompt keywords (not image names)
- [X] T022 [P] [US3] Add test in `tests/test_generate.py` — prompt with only stop words: output named `image.png` (fallback)

### Implementation for User Story 3

No additional implementation needed — the resolution logic from T009 already calls `extract_keywords(prompt)` for the fallback case. This phase validates behavior through tests.

**Checkpoint**: Tous les cas de nommage fonctionnent : `--name`, image unique, mots-clés du prompt.

---

## Phase 5: User Story 4 - Rétrocompatibilité sans image de référence (Priority: P2)

**Goal**: Vérifier que le comportement sans image de référence fonctionne avec la nouvelle logique de mots-clés.

**Independent Test**: Exécuter `generate "un paysage"` sans `--images` ni `--name` et vérifier le nom basé sur les mots-clés.

### Tests for User Story 4

- [X] T023 [US4] Add test in `tests/test_generate.py` — no images, no name: output named with prompt keywords (verifies new behavior replaces old slug)

### Implementation for User Story 4

No additional implementation needed — covered by the resolution logic from T009.

**Checkpoint**: Rétrocompatibilité vérifiée.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Nettoyage et vérification finale.

- [X] T024 Verify all existing tests still pass by running `cd src && pytest` from project root
- [X] T025 Run `ruff check .` from `src/` to verify code style compliance

---

## Dependencies & Execution Order

### Phase Dependencies

- **Foundational (Phase 1)**: Pas de dépendance — peut commencer immédiatement
- **US1 (Phase 2)**: Dépend de Phase 1 (T001, T002)
- **US2 (Phase 3)**: Dépend de Phase 2 (T008, T009, T010 — le paramètre `name` doit exister)
- **US3 (Phase 4)**: Dépend de Phase 2 (T009 — la logique `extract_keywords` doit être branchée)
- **US4 (Phase 5)**: Dépend de Phase 4
- **Polish (Phase 6)**: Dépend de toutes les phases précédentes

### User Story Dependencies

- **US1 (P1)**: Peut commencer après Phase 1 — implémente la logique de résolution
- **US2 (P1)**: Peut commencer après US1 — ajoute `--name` au-dessus de la logique existante
- **US3 (P2)**: Peut commencer après US1 — vérifie le fallback mots-clés
- **US4 (P2)**: Peut commencer après US3 — validation rétrocompatibilité

### Within Each User Story

- Tests écrits en premier (Constitution Principe III)
- Implémentation ensuite
- Validation au checkpoint

### Parallel Opportunities

- T001 et T002 en parallèle (fonctions indépendantes dans `slugify.py`)
- T003 et T004 en parallèle (tests indépendants)
- T005, T006, T007 en parallèle (tests US1 indépendants)
- T011, T012, T013, T014, T015 en parallèle (tests US2 indépendants)
- T019, T020, T021, T022 en parallèle (tests US3 indépendants)

---

## Parallel Example: Phase 1 (Foundational)

```bash
# Fonctions utilitaires en parallèle :
Task T001: "Add extract_keywords() in src/slugify.py"
Task T002: "Add strip_image_extension() in src/slugify.py"

# Tests en parallèle (après T001/T002) :
Task T003: "Tests for extract_keywords() in tests/test_slugify.py"
Task T004: "Tests for strip_image_extension() in tests/test_slugify.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Foundational (T001-T004)
2. Complete Phase 2: US1 — Single image naming (T005-T010)
3. **STOP and VALIDATE**: Tester avec une image de référence unique
4. Livrable MVP fonctionnel

### Incremental Delivery

1. Phase 1 → Fonctions utilitaires prêtes
2. + US1 → Nommage par image de référence (MVP!)
3. + US2 → Paramètre `--name` pour forçage
4. + US3 + US4 → Mots-clés du prompt pour tous les cas
5. Phase 6 → Validation finale

---

## Notes

- [P] tasks = fichiers différents, pas de dépendances
- [Story] label associe chaque tâche à une user story
- Constitution Principe III : tests obligatoires, API Gemini mockée
- Aucune nouvelle dépendance Python (Principe IV)
- Commit après chaque phase ou groupe logique
