---
name: magic-square-tdd
description: >-
  UnitConverter_20 ARRR TDD 워크플로. validate_lines / convert_units
  RED→GREEN→REFACTOR, C2C 설계표, ECB·Mock 규칙, 커맨드(/red-test-plan,
  /red-skeleton, /tdd-red, /green-minimal, /golden-master, /refactor-smell,
  /refactor-safe) 연계. TDD·pytest·길이 단위 변환 Entity 작업 시 적용.
---

# UnitConverter_20 TDD Skill

meter 기준 4단위 변환 Entity TDD를 **ARRR** 순서로 진행한다.

## ARRR 맵

| 단계 | 의미 | 커맨드 | 수정 범위 |
|------|------|--------|-----------|
| **A** Ask | C2C·테스트 플랜 | `/red-test-plan` | 없음 (채팅만) |
| **R** RED | 실패 테스트 | `/red-skeleton`, `/tdd-red`, `/golden-master` | `tests/` |
| **R** Run | 최소 구현 | `/green-minimal` | `src/` |
| **R** Refine | 리팩터 | `/refactor-smell`, `/refactor-safe` | `src/`·`tests/` (행위 불변) |

모든 커맨드는 **슬래시명만**으로 동작. 추가 질문 금지.

## SSOT 우선순위

1. `docs/PRD.md` — FR-CONV-*, Test ID (`D-CONV-*`), golden·상수
2. `.cursorrules` — 도메인, API, TDD Phase
3. `tests/test_validate_lines.py` — 고정 정책
4. 채팅 — 세션 주제, RED 묶음

## 도메인 (요약)

- **앵커**: `meter = 1`
- **단위**: `meter`, `feet`, `yard`, `cubit`
- **상수**: PRD — `FEET_PER_METER`, `YARDS_PER_METER`, `METERS_PER_CUBIT`
- **Harness**: `validate_lines(grid)` — `grid = {"unit", "value"}`
- **반환 (Harness)**: `{status: pass|fail|incomplete, failed_lines: [...]}`
- **PRD Entity**: `convert_units(unit, value)` — `{status, conversions, failed_fields}`

## Phase 선언 (응답 첫 줄)

| 작업 | 선언 |
|------|------|
| 플랜 | `Phase: red \| Layer: entity \| Track: Logic` |
| RED skeleton | `Phase: red \| Layer: entity \| Track: Logic` |
| RED (`/tdd-red`) | `Phase: RED` |
| 골든 RED | `Phase: RED \| Kind: golden-master` |
| GREEN | `Phase: GREEN` |
| 스멜 | `Phase: REFACTOR \| Mode: smell` |
| 안전 리팩터 | `Phase: REFACTOR \| Mode: safe` |

**한 턴에 한 Phase.** RED+GREEN 혼합 금지.

## Test ID (PRD)

| Test ID | FR | 설명 |
|---------|-----|------|
| `D-CONV-01` | FR-CONV-01 | invalid — 음수·unknown unit |
| `D-CONV-GM-01` | FR-CONV-02 | `meter:2.5` golden |
| `D-CONV-02` | FR-CONV-03 | `cubit:1` golden |
| `D-CONV-03` | FR-CONV-04 | feet/yard 입력 |

함수명: `D-CONV-01` → `test_d_conv_01`

## ECB·Mock (Logic Track)

- 검증 대상: **Entity** (`validate_lines` / `convert_units`)
- **Domain Mock 금지**
- **E001~E005 emit 금지**
- Boundary(`단위:값` 파싱): 세션 범위 외

## TDD 불변 규칙

- RED: `tests/`만, assert 완화·skip·xfail 금지
- GREEN: `src/`만, 테스트 변경 금지
- REFACTOR: pytest 전체 통과, 행위 불변
- golden: **소수 4자리** (PRD)

## 권장 사이클

```
/red-test-plan → /red-skeleton → /green-minimal
     ↑                                    |
     └──────── /refactor-safe ← /refactor-smell
                    ↑
            /golden-master (선택)
/export-session
```

## pytest

```bash
pytest tests/test_validate_lines.py -v
pytest tests/ -v   # 리팩터 후
```

## 커맨드 위치

`.cursor/commands/` — `red-test-plan`, `red-skeleton`, `tdd-red`, `green-minimal`, `golden-master`, `refactor-smell`, `refactor-safe`, `export-session`

## 문서 Skill

`.cursor/skills/magic-square-docs/SKILL.md`
