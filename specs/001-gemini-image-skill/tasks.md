# Tasks: Gemini Image Generation Skill

**Input**: Design documents from `/specs/001-gemini-image-skill/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Included (Constitution §III requires standard testing with mocks).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Purpose**: Project initialization and basic structure

- [x] T001 Initialize Python project with `uv init`, configure `pyproject.toml` with dependencies: google-genai, Pillow, python-dotenv, pytest
- [x] T002 [P] Create `.env.example` with `GEMINI_API_KEY=your_key_here` and add `.env` to `.gitignore`
- [x] T003 [P] Create `styles.json` with 4 initial presets (ghibli, pixel-art, photo-realistic, watercolor) per data-model.md
- [x] T004 [P] Add `out/` to `.gitignore`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core modules that ALL user stories depend on

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Implement config module in `src/config.py`: load `.env`, validate `GEMINI_API_KEY` presence, return API key or raise clear error
- [x] T006 [P] Implement slugify module in `src/slugify.py`: normalize Unicode to ASCII, lowercase, replace non-alphanum with hyphens, truncate to 50 chars, handle collision with numeric suffix
- [x] T007 [P] Implement styles module in `src/styles.py`: load `styles.json`, get style by name, list available styles, add/replace style with optional force flag
- [x] T008 [P] Implement history module in `src/history.py`: append GenerationLogEntry as JSON line to `out/history.jsonl`, create file if absent
- [x] T009 [P] Write unit tests for config in `tests/test_config.py`: test missing key, valid key, empty key
- [x] T010 [P] Write unit tests for slugify in `tests/test_slugify.py`: test basic slugification, Unicode, truncation, collision suffix
- [x] T011 [P] Write unit tests for styles in `tests/test_styles.py`: test load, get existing, get missing, list, add new, replace with force
- [x] T012 [P] Write unit tests for history in `tests/test_history.py`: test append entry, create file, verify JSON Lines format

**Checkpoint**: Foundation ready — all utility modules tested and working

---

## Phase 3: User Story 1 — Générer une image depuis un prompt texte (Priority: P1) MVP

**Goal**: L'utilisateur génère une image à partir d'un prompt texte via `/generate-image`

**Independent Test**: Invoquer `/generate-image "un chat"` → un fichier `out/un-chat.png` est créé, le chemin est affiché, une entrée apparaît dans `history.jsonl`

### Tests for User Story 1

- [x] T013 [P] [US1] Write unit tests for generate in `tests/test_generate.py`: mock Gemini API response, test prompt-only generation, test output file creation, test slug naming, test history logging, test error handling (missing key, API error, content blocked, empty prompt)

### Implementation for User Story 1

- [x] T014 [US1] Implement main generation script in `src/generate.py`: parse CLI args (prompt, --style, --images), call Gemini API with `gemini-2.5-flash-image` model, save image to `out/` with slugified name, log to history, output JSON result to stdout. Handle all error codes per cli-contract.md
- [x] T015 [US1] Create Claude Code skill command in `.claude/commands/generate-image.md`: instructions for Claude to run `python src/generate.py "$ARGUMENTS"`, display result path on success, display error message on failure

**Checkpoint**: User Story 1 fully functional — text-to-image generation works end-to-end

---

## Phase 4: User Story 2 — Générer avec des images de référence (Priority: P2)

**Goal**: L'utilisateur fournit des images dans le chat et génère une image transformée

**Independent Test**: Partager une image dans le chat, invoquer `/generate-image "transforme en aquarelle"` → l'image générée reflète la référence

### Tests for User Story 2

- [x] T016 [P] [US2] Write unit tests for image reference handling in `tests/test_generate_images.py`: test with `--images` flag, test PIL.Image loading from paths, test API call includes reference images, test fallback to text-only when no images

### Implementation for User Story 2

- [x] T017 [US2] Extend `src/generate.py` to handle `--images` flag: load image files as PIL.Image, include in Gemini API `contents` array alongside prompt text
- [x] T018 [US2] Update `.claude/commands/generate-image.md`: add instructions for Claude to detect images in chat context, save them to temporary files, and pass their paths via `--images` flag

**Checkpoint**: User Stories 1 AND 2 work independently — text-only and image-reference generation

---

## Phase 5: User Story 3 — Appliquer un style prédéfini (Priority: P3)

**Goal**: L'utilisateur applique un style via `--style` pour enrichir le prompt

**Independent Test**: Invoquer `/generate-image "un château" --style ghibli` → le prompt envoyé à l'API contient la phrase du style ghibli

### Tests for User Story 3

- [x] T019 [P] [US3] Write unit tests for style application in `tests/test_generate_styles.py`: test prompt enrichment with style, test unknown style error listing available styles, test generation without style (no enrichment)

### Implementation for User Story 3

- [x] T020 [US3] Extend `src/generate.py` to handle `--style` flag: look up style in styles.json via styles module, concatenate style prompt_text to user prompt before API call, error with available styles list if style not found

**Checkpoint**: Style presets functional — user can apply any of the 4 built-in styles

---

## Phase 6: User Story 4 — Créer un nouveau style personnalisé (Priority: P4)

**Goal**: L'utilisateur crée un nouveau preset de style via `/create-style`

**Independent Test**: Invoquer `/create-style "mon-style" "description"` → le style est ajouté à `styles.json` et utilisable via `--style mon-style`

### Tests for User Story 4

- [x] T021 [P] [US4] Write unit tests for create_style in `tests/test_create_style.py`: test create new style, test conflict detection (existing style), test replace with force, test missing arguments, test invalid name format

### Implementation for User Story 4

- [x] T022 [US4] Implement create style script in `src/create_style.py`: parse CLI args (name, description, --force), validate name format (kebab-case), check for conflicts, add/replace via styles module, output JSON result to stdout per cli-contract.md
- [x] T023 [US4] Create Claude Code skill command in `.claude/commands/create-style.md`: instructions for Claude to run `python src/create_style.py "$ARGUMENTS"`, handle conflict by asking user confirmation then re-run with `--force`

**Checkpoint**: Full style lifecycle — create, apply, and replace styles

---

## Phase 7: User Story 5 — Historique des générations (Priority: P5)

**Goal**: Chaque génération est automatiquement journalisée dans un fichier lisible

**Independent Test**: Générer plusieurs images, ouvrir `out/history.jsonl`, vérifier que toutes les entrées sont présentes avec date, prompt, style, chemin, statut

### Implementation for User Story 5

- [x] T024 [US5] Verify history logging is complete in `src/generate.py`: ensure both success and failure cases write to history, include all fields (timestamp, prompt, style, output, success, error)

**Checkpoint**: All user stories functional — generation, references, styles, custom styles, and history

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T025 [P] Run full test suite with `uv run pytest -v` and fix any failures
- [x] T026 [P] Validate quickstart.md flow end-to-end: install → configure → generate → verify
- [x] T027 Add `__init__.py` files if needed for proper Python module resolution in `src/`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - US1 (Phase 3): No story dependencies — MVP
  - US2 (Phase 4): Extends US1's `generate.py` — execute after US1
  - US3 (Phase 5): Extends US1's `generate.py` — can run parallel to US2
  - US4 (Phase 6): Depends on styles module (Phase 2) — can run parallel to US2/US3
  - US5 (Phase 7): History already implemented in Phase 2 — verification only
- **Polish (Phase 8)**: Depends on all user stories being complete

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Utility modules (Phase 2) before story scripts
- Story script before skill command file
- Core implementation before integration

### Parallel Opportunities

- T002, T003, T004 can all run in parallel (Setup phase)
- T005-T012 foundational modules and their tests can run in parallel (different files)
- T013 (US1 tests) can run in parallel with other US1 prep
- US3 and US4 can run in parallel (different scripts, different skill files)

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational modules
3. Complete Phase 3: User Story 1 (generate-image basic)
4. **STOP and VALIDATE**: Test `/generate-image "test"` end-to-end
5. Deploy/demo if ready

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add US1 → Text-to-image works (MVP!)
3. Add US2 → Image references work
4. Add US3 → Style presets work
5. Add US4 → Custom styles work
6. Add US5 → History verified
7. Polish → All tests green, quickstart validated

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story
- Each user story is independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
