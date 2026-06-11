# UnitConverter_20 — ARRR 체크리스트

| 항목 | 내용 |
|------|------|
| **세션** | {주제} |
| **일자** | {YYYY-MM-DD} |
| **RED 묶음** | {예: D-CONV-01} |

## A — Ask (`/red-test-plan`)

| # | 항목 | 완료 |
|---|------|------|
| A1 | C2C 표 (FR-CONV → To-Do → GWT) | ☐ |
| A2 | Track B 표 (Invariant, Expected RED Failure) | ☐ |
| A3 | 테스트 플랜 (경로, 함수명, pytest 명령) | ☐ |
| A4 | ECB·Mock (Domain Mock 금지, E001~E005 금지) | ☐ |

## R — RED (`/red-skeleton`, `/tdd-red`, `/golden-master`)

| # | 항목 | 완료 |
|---|------|------|
| R1 | Test ID·docstring (D-CONV-*) | ☐ |
| R2 | AAA — `grid={"unit","value"}` | ☐ |
| R3 | `pytest` **FAILED** 확인 | ☐ |
| R4 | `src/` 미수정 | ☐ |

## R — Run (`/green-minimal`)

| # | 항목 | 완료 |
|---|------|------|
| G1 | `src/` 최소 구현만 | ☐ |
| G2 | `tests/` 미수정 | ☐ |
| G3 | `pytest` **PASSED** | ☐ |

## R — Refine (`/refactor-smell`, `/refactor-safe`)

| # | 항목 | 완료 |
|---|------|------|
| F1 | 스멜 목록 | ☐ |
| F2 | 안전 리팩터 1건 | ☐ |
| F3 | `pytest tests/` 전체 PASSED | ☐ |
| F4 | `/golden-master` 회귀 (있으면) | ☐ |

## Export (`/export-session`)

| # | 항목 | 완료 |
|---|------|------|
| E1 | `Report/NN.REPORT.md` | ☐ |
| E2 | `Prompting/NN.Export-Transcript.md` | ☐ |

## 메모

- {블로커·다음 RED — 예: D-CONV-GM-01}

*본 문서는 docs/checklists/{NN}.ARRR-checklist.md — {세션} handoff 체크리스트입니다.*
