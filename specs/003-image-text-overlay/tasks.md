# Tasks: Image Text Overlay

**Input**: Design documents from `/specs/003-image-text-overlay/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Included (constitution Principle III requires unit tests for all business logic).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Purpose**: No setup needed — project structure and dependencies already exist. This feature requires no new dependencies.

(No tasks — skip to Phase 2)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Modifications aux modules utilitaires partagés, nécessaires avant l'implémentation des user stories.

- [x] T001 [P] Add `text` parameter to `log_generation()` function in src/history.py — optional string parameter (default None), added to the JSON entry dict
- [x] T002 [P] Add unit test for `text` field in log entry in tests/test_history.py — test that `text` value is correctly written to history.jsonl when provided, and null when omitted

**Checkpoint**: history.py accepte le paramètre `text` et le journalise correctement.

---

## Phase 3: User Story 1 - Ajouter du texte sur une image générée (Priority: P1) 🎯 MVP

**Goal**: L'utilisateur peut utiliser `--text "MON TEXTE"` pour que le texte apparaisse sur l'image générée, casse préservée.

**Independent Test**: Exécuter `python src/generate.py "un logo" --text "ACME"` et vérifier que l'image contient le texte en majuscules. Exécuter sans `--text` et vérifier que le comportement est inchangé.

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T003 [P] [US1] Add test for `--text` argument parsing in tests/test_generate.py — test parse_args with `--text "Hello"`, verify args.text == "Hello"; test without --text, verify args.text is None
- [x] T004 [P] [US1] Add test for text prompt enrichment in tests/test_generate.py — mock API, call generate_image with text="ACME CORP", verify the prompt sent to API contains the text instruction with exact casing; call without text, verify no text instruction in prompt
- [x] T005 [P] [US1] Add test for empty text ignored in tests/test_generate.py — call generate_image with text="", verify prompt has no text instruction (same as text=None)
- [x] T006 [P] [US1] Add test for text field in result dict in tests/test_generate.py — mock API, call generate_image with text="HELLO", verify result["text"] == "HELLO"; call without text, verify "text" key is absent or None
- [x] T007 [P] [US1] Add test for text logged in history in tests/test_generate.py — mock API, call generate_image with text="TEST", verify history.jsonl entry contains "text": "TEST"

### Implementation for User Story 1

- [x] T008 [US1] Add `--text` argument to `parse_args()` in src/generate.py — optional string argument with help text
- [x] T009 [US1] Add `text` parameter to `generate_image()` function signature in src/generate.py — optional string parameter (default None)
- [x] T010 [US1] Implement text prompt injection in `generate_image()` in src/generate.py — if text is non-empty, insert instruction `Write the exact text "{text}" on the image, preserving the exact capitalization` into enriched_prompt after user prompt and before resource prompts/style
- [x] T011 [US1] Pass `text` to all `log_generation()` calls in src/generate.py — add text=text parameter to every log_generation call (success and error paths)
- [x] T012 [US1] Add `text` field to result dict in src/generate.py — include `"text": text` in the success result dict when text is provided
- [x] T013 [US1] Wire `--text` argument in `main()` function in src/generate.py — pass args.text to generate_image() call

**Checkpoint**: US1 complète — `python src/generate.py "un logo" --text "ACME"` fonctionne, tests passent.

---

## Phase 4: User Story 2 - Combiner texte avec style et autres options (Priority: P2)

**Goal**: Le flag `--text` fonctionne correctement en combinaison avec `--style`, `--model`, `--include`, `--images`.

**Independent Test**: Exécuter `python src/generate.py "un poster" --text "CONCERT" --style ghibli` et vérifier que le style ET le texte sont présents.

### Tests for User Story 2

- [x] T014 [P] [US2] Add test for text combined with style in tests/test_generate_styles.py — mock API, call generate_image with text="Bienvenue" and style="ghibli", verify enriched prompt contains both text instruction and style text, in correct order (text before style)
- [x] T015 [P] [US2] Add test for text combined with include tags in tests/test_generate_resources.py — mock API, call generate_image with text="HELLO" and include_tags, verify prompt contains text instruction, resource prompts, and correct ordering

### Implementation for User Story 2

(No additional implementation needed — the prompt enrichment order implemented in T010 already handles combination with style, model, include, and images. These tests validate the existing behavior.)

**Checkpoint**: US2 complète — tous les tests de combinaison passent.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Validation finale et nettoyage.

- [x] T016 Run all existing tests to verify no regression: 96 passed, 0 failed
- [ ] T017 Run quickstart.md validation — execute examples from specs/003-image-text-overlay/quickstart.md manually

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 2 (Foundational)**: No dependencies — can start immediately
- **Phase 3 (US1)**: Depends on Phase 2 (T001 for history.py changes)
- **Phase 4 (US2)**: Depends on Phase 3 (US1 implementation)
- **Phase 5 (Polish)**: Depends on Phase 3 + Phase 4

### User Story Dependencies

- **User Story 1 (P1)**: Depends on T001 (history.py text param) — core feature
- **User Story 2 (P2)**: Depends on US1 completion — validates combinations

### Within Each User Story

- Tests written FIRST and FAIL before implementation
- Implementation tasks are sequential (argparse → function sig → logic → logging → result → wiring)

### Parallel Opportunities

- T001 and T002 can run in parallel (different files)
- T003, T004, T005, T006, T007 can all run in parallel (same file but independent test methods)
- T014 and T015 can run in parallel (independent test methods)

---

## Parallel Example: User Story 1

```bash
# Launch all tests for US1 together (they should FAIL initially):
Task: T003 "Add test for --text argument parsing in tests/test_generate.py"
Task: T004 "Add test for text prompt enrichment in tests/test_generate.py"
Task: T005 "Add test for empty text ignored in tests/test_generate.py"
Task: T006 "Add test for text field in result dict in tests/test_generate.py"
Task: T007 "Add test for text logged in history in tests/test_generate.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 2: Foundational (T001-T002)
2. Complete Phase 3: User Story 1 tests (T003-T007) — verify they FAIL
3. Complete Phase 3: User Story 1 implementation (T008-T013)
4. **STOP and VALIDATE**: Run tests, verify all pass
5. Feature is usable with `--text` flag

### Incremental Delivery

1. T001-T002 → history.py ready
2. T003-T013 → US1 complete → `--text` works standalone (MVP!)
3. T014-T015 → US2 complete → combinations validated
4. T016-T017 → Polish → full regression check

---

## Notes

- [P] tasks = different files or independent test methods, no dependencies
- [Story] label maps task to specific user story for traceability
- Total: 17 tasks (2 foundational, 5+6 US1, 2 US2, 2 polish)
- Only 2 source files modified: src/generate.py, src/history.py
- Only 2 test files modified: tests/test_generate.py, tests/test_history.py
