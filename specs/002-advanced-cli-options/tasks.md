# Tasks: Options CLI avancées

**Input**: Design documents from `/specs/002-advanced-cli-options/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Included (Constitution §III requires standard testing with mocks).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Purpose**: New configuration files and directory structure

- [x] T001 Create `models.json` at project root with initial models: flash (gemini-2.5-flash-image, default), pro (gemini-3-pro-image-preview), nano (gemini-3.1-flash-image-preview)
- [x] T002 [P] Create `resources/` directory at project root with a `.gitkeep` file
- [x] T003 [P] Add `resources/` entry to `.gitignore` comment explaining it may contain personal images

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: New modules that user stories depend on

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Implement models module in `src/models.py`: load `models.json`, get model_id by alias, list available models with default marker, get default model. Same pattern as `src/styles.py`
- [x] T005 [P] Implement resources module in `src/resources.py`: list available tags (subdirectories of `resources/`), load images from tag directory (filter .png/.jpg/.jpeg/.webp), read optional `meta.json` for prompt field, validate tag exists and has images
- [x] T006 [P] Write unit tests for models in `tests/test_models.py`: test load, get existing alias, get missing alias, list with default marker, get default model, fallback when models.json absent
- [x] T007 [P] Write unit tests for resources in `tests/test_resources.py`: test list tags, load images from tag, read meta.json prompt, missing tag error, empty tag error, meta.json absent (images only), invalid image extensions filtered

**Checkpoint**: Foundation ready — models and resources modules tested

---

## Phase 3: User Story 1 — Valider les arguments avant exécution (Priority: P1) MVP

**Goal**: Tous les arguments CLI sont validés avant tout appel réseau. Erreurs claires avec liste des flags disponibles.

**Independent Test**: Invoquer avec `--unknown-flag`, `--style` sans valeur, ou sans prompt → erreur JSON avant tout appel API

### Tests for User Story 1

- [x] T008 [P] [US1] Write unit tests for argument validation in `tests/test_args_validation.py`: test valid args parsed correctly, test unknown flag error with available flags list, test missing value for --style error, test missing prompt shows usage, test --model and --include accepted without error, test all flags combinable in any order

### Implementation for User Story 1

- [x] T009 [US1] Refactor `parse_args()` in `src/generate.py`: add `--model` (optional string), add `--include` (repeatable string list), use `exit_on_error=False` to catch errors and return JSON error with code INVALID_ARGS and exit code 3. Include usage examples in error messages per cli-contract.md
- [x] T010 [US1] Update existing tests in `tests/test_generate.py` to pass with new argument structure (add --model and --include to parse_args tests)

**Checkpoint**: Argument validation working — invalid args produce clear errors before any API call

---

## Phase 4: User Story 2 — Choisir le modèle de génération (Priority: P2)

**Goal**: L'utilisateur choisit le modèle via `--model <alias>`, avec fallback au modèle par défaut

**Independent Test**: Invoquer avec `--model pro` → l'API est appelée avec le bon model_id. Invoquer avec `--model inexistant` → erreur avec liste des modèles

### Tests for User Story 2

- [x] T011 [P] [US2] Write unit tests for model selection in `tests/test_generate_model.py`: test --model pro uses correct model_id, test no --model uses default, test unknown model error lists available models, test model_id passed to API call (mock verification)

### Implementation for User Story 2

- [x] T012 [US2] Extend `generate_image()` in `src/generate.py`: resolve model alias via models module before API call, pass resolved model_id to `client.models.generate_content(model=...)`, add model field to success response JSON, handle UNKNOWN_MODEL error with exit code 4
- [x] T013 [US2] Update history logging in `src/generate.py`: include model used in log entry (add to `log_generation` call)

**Checkpoint**: Model selection working — user can switch models via `--model`

---

## Phase 5: User Story 3 — Inclure des ressources par tag (Priority: P3)

**Goal**: L'utilisateur inclut des packs de ressources via `--include <tag>`, images et prompt contextuel injectés

**Independent Test**: Créer `resources/test-tag/` avec images et meta.json, invoquer avec `--include test-tag` → images envoyées à l'API et prompt enrichi

### Tests for User Story 3

- [x] T014 [P] [US3] Write unit tests for resource inclusion in `tests/test_generate_resources.py`: test --include loads images from tag directory, test --include enriches prompt with meta.json prompt, test --include without meta.json sends images only, test unknown tag error lists available tags, test empty tag error, test multiple --include combines resources, test --include + --images combines both sources, test --include + --style cumulates enrichments

### Implementation for User Story 3

- [x] T015 [US3] Extend `generate_image()` in `src/generate.py`: resolve each --include tag via resources module, load images and add to contents array, prepend meta.json prompts to enriched prompt (after user prompt, before style), handle UNKNOWN_TAG and EMPTY_RESOURCES errors with exit code 4
- [x] T016 [US3] Update `.claude/commands/generate-image.md`: add documentation for `--model` and `--include` flags with examples, update usage syntax

**Checkpoint**: All user stories functional — validation, model selection, and resource inclusion

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and cleanup

- [x] T017 [P] Run full test suite with `uv run pytest -v` and fix any failures
- [x] T018 [P] Validate quickstart.md flow: create test resources, test all new flags
- [x] T019 Update `src/history.py` to accept optional `model` parameter and update `log_generation()` signature if needed

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup — BLOCKS all user stories
- **US1 (Phase 3)**: Depends on Foundational — refactors generate.py args
- **US2 (Phase 4)**: Depends on US1 (needs --model in parse_args) + models module
- **US3 (Phase 5)**: Depends on US1 (needs --include in parse_args) + resources module. Can run parallel to US2
- **Polish (Phase 6)**: Depends on all user stories

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Module (models.py/resources.py) before generate.py integration
- Core implementation before skill command update

### Parallel Opportunities

- T002, T003 can run in parallel (Setup)
- T004-T007 foundational modules and tests can run in parallel (different files)
- T008 (US1 tests) can run in parallel with US1 prep
- US2 and US3 can run in parallel after US1 (different modules)
- T017, T018 can run in parallel (Polish)

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (models.json, resources/)
2. Complete Phase 2: Foundational modules (models.py, resources.py + tests)
3. Complete Phase 3: US1 — argument validation
4. **STOP and VALIDATE**: Test with invalid args → clear errors

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add US1 → Argument validation works (MVP)
3. Add US2 → Model selection works
4. Add US3 → Resource inclusion works
5. Polish → All tests green, quickstart validated

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story
- Each user story is independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Rétrocompatibilité: les commandes existantes (sans --model/--include) DOIVENT continuer à fonctionner
