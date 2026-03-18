# Tasks: Image Aspect Ratio & Size

**Input**: Design documents from `/specs/004-image-ratio-size/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Included (constitution Principle III requires unit tests for all business logic).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Purpose**: No setup needed — project structure and dependencies already exist. No new dependencies required.

(No tasks — skip to Phase 2)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Modifications aux modules utilitaires partagés, nécessaires avant l'implémentation des user stories.

- [x] T001 [P] Add `ratio` and `size` parameters to `log_generation()` function in src/history.py — optional string parameters (default None), added to the JSON entry dict
- [x] T002 [P] Add unit tests for `ratio` and `size` fields in log entries in tests/test_history.py — test that values are correctly written when provided and null when omitted

**Checkpoint**: history.py accepte les paramètres `ratio` et `size` et les journalise correctement.

---

## Phase 3: User Story 1 - Choisir l'aspect ratio (Priority: P1) 🎯 MVP

**Goal**: L'utilisateur peut utiliser `--ratio 1:1` pour contrôler l'aspect ratio. Par défaut 16:9.

**Independent Test**: Exécuter `python src/generate.py "un logo" --ratio 1:1` et vérifier que l'API reçoit le ratio. Exécuter sans `--ratio` et vérifier que 16:9 est utilisé par défaut.

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T003 [P] [US1] Add test for `--ratio` argument parsing in tests/test_generate.py
- [x] T004 [P] [US1] Add test for valid ratio passed to ImageConfig in tests/test_generate.py
- [x] T005 [P] [US1] Add test for default ratio (16:9) in tests/test_generate.py
- [x] T006 [P] [US1] Add test for invalid ratio error in tests/test_generate.py
- [x] T007 [P] [US1] Add test for ratio in result dict in tests/test_generate.py
- [x] T008 [P] [US1] Add test for ratio logged in history in tests/test_generate.py

### Implementation for User Story 1

- [x] T009 [US1] Define SUPPORTED_RATIOS constant and DEFAULT_RATIO in src/generate.py
- [x] T010 [US1] Add `--ratio` argument to `parse_args()` in src/generate.py
- [x] T011 [US1] Add `ratio` parameter to `generate_image()` function signature in src/generate.py
- [x] T012 [US1] Add ratio validation in `generate_image()` in src/generate.py
- [x] T013 [US1] Add `image_config=types.ImageConfig(aspect_ratio=ratio)` to GenerateContentConfig in src/generate.py
- [x] T014 [US1] Pass `ratio` to all `log_generation()` calls in src/generate.py
- [x] T015 [US1] Add `ratio` field to result dict in src/generate.py
- [x] T016 [US1] Wire `--ratio` argument in `main()` function in src/generate.py

**Checkpoint**: US1 complète — `--ratio` fonctionne avec validation et défaut 16:9.

---

## Phase 4: User Story 2 - Choisir la taille (Priority: P2)

**Goal**: L'utilisateur peut utiliser `--size 4k` pour contrôler la résolution. Par défaut 1k. Mapping minuscule → majuscule pour l'API.

**Independent Test**: Exécuter `python src/generate.py "un paysage" --size 4k` et vérifier que l'API reçoit "4K".

### Tests for User Story 2

- [x] T017 [P] [US2] Add test for `--size` argument parsing in tests/test_generate.py
- [x] T018 [P] [US2] Add test for valid size passed to ImageConfig in tests/test_generate.py
- [x] T019 [P] [US2] Add test for default size (1k) in tests/test_generate.py
- [x] T020 [P] [US2] Add test for invalid size error in tests/test_generate.py
- [x] T021 [P] [US2] Add test for size in result dict in tests/test_generate.py
- [x] T022 [P] [US2] Add test for size logged in history in tests/test_generate.py

### Implementation for User Story 2

- [x] T023 [US2] Define SUPPORTED_SIZES constant, DEFAULT_SIZE, and SIZE_MAP in src/generate.py
- [x] T024 [US2] Add `--size` argument to `parse_args()` in src/generate.py
- [x] T025 [US2] Add `size` parameter to `generate_image()` function signature in src/generate.py
- [x] T026 [US2] Add size validation in `generate_image()` in src/generate.py
- [x] T027 [US2] Update ImageConfig to include image_size in src/generate.py
- [x] T028 [US2] Pass `size` to all `log_generation()` calls in src/generate.py
- [x] T029 [US2] Add `size` field to result dict in src/generate.py
- [x] T030 [US2] Wire `--size` argument in `main()` function in src/generate.py

**Checkpoint**: US2 complète — `--size` fonctionne avec mapping et défaut 1k.

---

## Phase 5: User Story 3 - Combiner ratio, taille et autres options (Priority: P3)

**Goal**: Tous les flags fonctionnent ensemble sans conflit.

### Tests for User Story 3

- [x] T031 [P] [US3] Add test for ratio + size + style combined in tests/test_generate.py
- [x] T032 [P] [US3] Add test for ratio + size + text combined in tests/test_generate.py

**Checkpoint**: US3 complète — toutes les combinaisons fonctionnent.

---

## Phase 6: Polish & Cross-Cutting Concerns

- [x] T033 Run all existing tests to verify no regression: 115 passed, 0 failed
- [ ] T034 Run quickstart.md validation — execute examples manually

---

## Notes

- Total: 34 tasks, 33 completed, 1 manual validation remaining
- 115 tests pass, 0 regressions
