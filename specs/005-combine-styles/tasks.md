# Tasks: Combine Multiple Styles

**Input**: Design documents from `/specs/005-combine-styles/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Included (constitution Principle III).

**Organization**: Tasks grouped by user story.

## Format: `[ID] [P?] [Story] Description`

---

## Phase 2: Foundational (Blocking Prerequisites)

- [x] T001 [P] Change `style` parameter type in src/history.py
- [x] T002 [P] Update history tests in tests/test_history.py
- [x] T003 [P] Update all existing tests passing `style=` as string in tests/test_generate_styles.py, tests/test_generate_resources.py, tests/test_generate.py, tests/test_args_validation.py

---

## Phase 3: User Story 1 - Appliquer plusieurs styles (Priority: P1)

### Tests for User Story 1

- [x] T004 [P] [US1] Test repeatable `--style` parsing in tests/test_generate.py
- [x] T005 [P] [US1] Test multi-style prompt enrichment in tests/test_generate_styles.py
- [x] T006 [P] [US1] Test single style backward compat in tests/test_generate_styles.py
- [x] T007 [P] [US1] Test no style backward compat in tests/test_generate_styles.py
- [x] T008 [P] [US1] Test invalid style in multi-style list in tests/test_generate_styles.py
- [x] T009 [P] [US1] Test style list in result dict in tests/test_generate.py
- [x] T010 [P] [US1] Test style list logged in history in tests/test_generate.py

### Implementation for User Story 1

- [x] T011 [US1] Change `--style` to `action="append"` in src/generate.py
- [x] T012 [US1] Change `style` type to `list[str] | None` in src/generate.py
- [x] T013 [US1] Replace single style lookup with validation loop in src/generate.py
- [x] T014 [US1] Update all `log_generation()` calls in src/generate.py
- [x] T015 [US1] Update result dict `style` field in src/generate.py
- [x] T016 [US1] Wire in `main()` in src/generate.py

---

## Phase 4: User Story 2

- [x] T017 [P] [US2] Test multi-style + text + ratio + size in tests/test_generate.py

---

## Phase 5: Polish

- [x] T018 Run all tests: 122 passed, 0 failed
- [ ] T019 Run quickstart.md validation manually

---

## Notes

- 122 tests pass, 0 regressions
- Also updated tests/test_args_validation.py (analysis finding I1/I2)
