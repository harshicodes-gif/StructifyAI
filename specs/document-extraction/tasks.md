# Tasks: Document Extraction

**Input**: Design documents from `specs/document-extraction/`

**Prerequisites**: plan.md, spec.md

**Tests**: Include focused pytest coverage for extraction behavior that can run without external services.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel because it touches different files or has no dependency on incomplete work
- **[Story]**: Maps the task to a user story from spec.md
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Confirm the existing project quality gates and document extraction entry points are ready.

- [ ] T001 Verify required dependencies for OCR, parsing, validation, storage, and quality checks in requirements.txt
- [ ] T002 Verify GitLab CI runs formatting, linting, flake8, type checks, tests, coverage, security scans, semgrep, changelog validation, quality checks, dead-code checks, and build checks in .gitlab-ci.yml
- [ ] T003 [P] Verify pre-commit hooks include ruff, black, pyupgrade, mypy, flake8, bandit, gitleaks, semgrep, and prettier in .pre-commit-config.yaml

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared document processing contracts and validation that all user stories depend on.

- [ ] T004 Review document field schema and validation behavior in backend/schemas/maintenance.py
- [ ] T005 Review extraction orchestration and error handling in backend/services/extraction_service.py
- [ ] T006 [P] Review OCR adapter behavior and offline assumptions in backend/ocr/easyocr_engine.py
- [ ] T007 [P] Review local model extraction fallback behavior in backend/llm/llama_engine.py and backend/services/rule_based_parser.py
- [ ] T008 Review SQLite persistence behavior in backend/database/sqlite.py

**Checkpoint**: Foundation ready for independently testable user stories.

---

## Phase 3: User Story 1 - Extract a Supported Document (Priority: P1) MVP

**Goal**: Users can upload a supported document and receive normalized text plus structured output.

**Independent Test**: Upload or simulate a representative supported document and verify structured fields are returned.

### Tests for User Story 1

- [ ] T009 [P] [US1] Add parser coverage for maintenance-style extracted text in tests/test_rule_based_parser.py
- [ ] T010 [P] [US1] Add upload validation coverage for supported and unsupported file types in tests/test_basic.py

### Implementation for User Story 1

- [ ] T011 [US1] Confirm supported file type filtering in frontend/components/uploader.py
- [ ] T012 [US1] Confirm upload page routes supported files into extraction in frontend/pages/upload.py
- [ ] T013 [US1] Confirm extraction service normalizes OCR text before structured parsing in backend/services/extraction_service.py
- [ ] T014 [US1] Confirm structured output is displayed without requiring cloud services in frontend/pages/upload.py

**Checkpoint**: User Story 1 is functional and testable independently.

---

## Phase 4: User Story 2 - Validate and Store Results (Priority: P2)

**Goal**: Only validated structured records are stored in local history.

**Independent Test**: Process valid and invalid extraction results and verify only valid records are persisted.

### Tests for User Story 2

- [ ] T015 [P] [US2] Add validation success and failure coverage for backend/schemas/maintenance.py in tests/test_basic.py
- [ ] T016 [P] [US2] Add local persistence coverage for backend/database/sqlite.py in tests/test_basic.py

### Implementation for User Story 2

- [ ] T017 [US2] Confirm validation happens before persistence in backend/services/extraction_service.py
- [ ] T018 [US2] Confirm failed validation is surfaced to users without storing invalid data in frontend/pages/upload.py
- [ ] T019 [US2] Confirm stored records include source metadata and processing timestamp in backend/database/sqlite.py

**Checkpoint**: User Stories 1 and 2 work independently.

---

## Phase 5: User Story 3 - Search and Export Extracted Records (Priority: P3)

**Goal**: Users can search local history and export stored structured records as JSON.

**Independent Test**: Store multiple records, search by a known field, and export one result as parseable JSON.

### Tests for User Story 3

- [ ] T020 [P] [US3] Add search behavior coverage for stored records in tests/test_basic.py
- [ ] T021 [P] [US3] Add JSON export behavior coverage for frontend/pages/history.py or backend/database/sqlite.py in tests/test_basic.py

### Implementation for User Story 3

- [ ] T022 [US3] Confirm history search filters meaningful document fields in frontend/pages/history.py
- [ ] T023 [US3] Confirm analytics/history views read from local validated records in frontend/pages/analytics.py and frontend/pages/history.py
- [ ] T024 [US3] Confirm exported records are valid JSON in frontend/pages/history.py

**Checkpoint**: All user stories are independently functional.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final quality and compliance checks.

- [ ] T025 [P] Run python -m black --check .
- [ ] T026 [P] Run python -m ruff check .
- [ ] T027 [P] Run python -m flake8 .
- [ ] T028 [P] Run semgrep --config=.semgrep.yml --error .
- [ ] T029 Run python -m pytest --cov=. --cov-report=term-missing --cov-report=xml --cov-fail-under=1
- [ ] T030 Run python -m compileall .

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup completion and blocks user stories.
- **User Stories (Phase 3+)**: Depend on Foundational completion.
- **Polish (Phase 6)**: Depends on desired user stories being complete.

### User Story Dependencies

- **User Story 1 (P1)**: Starts after Foundational; no dependency on other stories.
- **User Story 2 (P2)**: Starts after Foundational; uses the extraction output from US1 but remains testable with direct service inputs.
- **User Story 3 (P3)**: Starts after Foundational; depends on stored validated records from US2 for full end-to-end validation.

### Parallel Opportunities

- T003, T006, and T007 can run in parallel during setup/foundation review.
- Test tasks within each user story can run in parallel.
- Final quality commands T025 through T028 can run in parallel in CI.

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 and Phase 2.
2. Complete Phase 3.
3. Validate a supported upload returns structured output.

### Incremental Delivery

1. Deliver extraction output for supported files.
2. Add validation and local storage guarantees.
3. Add search and JSON export for stored records.
4. Run all quality and compliance checks.
