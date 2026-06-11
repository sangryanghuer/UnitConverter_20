#########################################################################################################################

# UnitConverter_20

![unit-converter](./unit-converter.jpg)

수업 중 길이 단위 변환 질문에 **한 번에** 답할 수 있는 Unit Converter.  
Mom Test → PRD → TDD(ARRR) 순으로 요구사항을 고정하고, Cursor로 RED→GREEN→REFACTOR를 진행한다.

**요구사항 SSOT:** [docs/PRD.md](docs/PRD.md)

---

## Overview

- 입력 `단위:값`(예: `meter:2.5`)을 받아 **등록 4단위**(`meter`, `feet`, `yard`, `cubit`)로 변환 결과를 반환한다.
- **앵커:** `meter = 1` — 모든 값을 meter로 통일한 뒤 대상 단위로 환산한다.
- Entity API(PRD): `convert_units(unit, value)` → `{ status, conversions, failed_fields }`
- Test Loop Harness: `validate_lines(grid)` — `grid = {"unit", "value"}` → `convert_units` 위임 (MagicSquare 호환)

### Mom Test → FR (요약)

| Mom Test | FR | Test ID |
|----------|-----|---------|
| 입력 검증(음수·unknown unit) | FR-CONV-01 | D-CONV-01 |
| `meter:2.5` golden · 전 단위 | FR-CONV-02 | D-CONV-GM-01 |
| `cubit:1` · 전 단위 | FR-CONV-03 | D-CONV-02 |
| `feet`/`yard` 입력 · 전 단위 | FR-CONV-04 | D-CONV-03 |

---

## 프로젝트 구조

```
UnitConverter_20/
├── docs/PRD.md              # SSOT — FR, 상수, golden
├── .cursorrules             # 도메인·API·TDD 규칙
├── .cursor/commands/        # ARRR 슬래시 커맨드
├── .cursor/skills/          # TDD·문서 Skill
├── src/
│   ├── convert_units.py     # Entity (PRD API)
│   ├── validate_lines.py    # Harness adapter → convert_units
│   └── web_server.py        # Web UI 로컬 서버
├── web/                     # HTML UI (index.html, app.js, style.css)
├── tests/
│   └── test_validate_lines.py
├── pyproject.toml           # pytest (pythonpath = ["src"])
├── UnitConverter.py         # 레거시 CLI (후속 통합)
├── Report/                  # 세션 보고서 NN.REPORT.md
└── Prompting/               # Transcript Export
```

---

## Dual-Track TDD

| Track | Layer | 대상 | Test ID 예 | 상태 |
|-------|-------|------|------------|------|
| **B (Logic)** | Entity | `validate_lines` / `convert_units` | D-CONV-01, D-CONV-GM-01, … | **진행 중** |
| **A (UI)** | Boundary | `단위:값` 파싱·출력·흐름 | U-IN-01~05, U-OUT-01, U-FLOW-02 | 후속 |

Track B: Domain Mock 금지 · golden **소수 4자리**(PRD).

---

## 변환 상수 (v0.1)

| 상수 | 값 |
|------|-----|
| `FEET_PER_METER` | 3.28084 |
| `YARDS_PER_METER` | 1.09361 |
| `METERS_PER_CUBIT` | 0.4572 |

**공식:** `meters = value × meters_per_unit[unit]` → `target = meters / meters_per_unit[target]`

### Golden 예시 (`meter`, 2.5)

| unit | 기대값 |
|------|--------|
| meter | 2.5 |
| feet | 8.2021 |
| yard | 2.7340 |
| cubit | 5.4681 |

---

## 설치 · 실행

### 가상환경

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate   # macOS/Linux
pip install pytest
```

### pytest (Test Loop)

```bash
pytest tests/test_validate_lines.py -v
pytest tests/ -v
```

> `pythonpath = ["src"]` — 로컬 `src/`가 다른 프로젝트 `validate_lines`보다 우선 import된다.

### 레거시 CLI

```bash
python UnitConverter.py
```

입력 예: `meter:2.5` → feet / yard 등 출력 (cubit·PRD golden과 정합은 후속).

### Web UI (HTML)

```bash
python src/web_server.py
```

브라우저에서 **http://127.0.0.1:8080** 접속.  
단위·값 입력 후 **변환** — Entity `convert_units` API(`/api/convert`)로 4단위 결과 표시.

추가 패키지 없음(stdlib `http.server`만 사용).

---

## Cursor ARRR 커맨드

슬래시명만 입력 (추가 질문 없음).

| 커맨드 | Phase | 역할 |
|--------|-------|------|
| `/red-test-plan` | Ask | C2C·테스트 플랜 (파일 없음) |
| `/red-skeleton` | RED | tests/ 골격·본문 |
| `/tdd-red` | RED | 실패 테스트 추가 |
| `/golden-master` | RED | golden 회귀 |
| `/green-minimal` | Run | src/ 최소 구현 |
| `/refactor-smell` | Refine | 스멜 분석 |
| `/refactor-safe` | Refine | 안전 리팩터 |
| `/export-session` | Export | Report + Transcript |

Skill: `.cursor/skills/magic-square-tdd/SKILL.md` · `.cursor/skills/magic-square-docs/SKILL.md`

---

## TDD 규칙 (요약)

- **RED:** `tests/`만 · assert 완화·skip·xfail 금지
- **GREEN:** `src/`만 · 테스트 변경 금지
- **REFACTOR:** pytest 전체 통과 유지
- 응답 첫 줄: `Phase: RED` / `Phase: GREEN` / `Phase: REFACTOR`

---

## 범위

### v0.1 (현재)

- 길이 4단위 · Entity 변환 · pytest TDD Harness

### 후속 (PRD 범위 외)

- GUI / Boundary 전체 · JSON·YAML 설정 · 동적 단위 등록 · CSV/JSON 출력

---

## 품질 · 추가 요구사항 (원본 실습)

- OCP · SRP · 입력 검증(음수, 형식, unknown unit)
- 설정 외부화 · 동적 단위 등록 · 출력 포맷(JSON/CSV/표) — **후속 Track**

---

## 문서 · 세션 기록

| 경로 | 내용 |
|------|------|
| [docs/PRD.md](docs/PRD.md) | FR · SC · Test ID · golden |
| [Report/](Report/) | 세션 요약 보고서 |
| [Prompting/](Prompting/) | Cursor Transcript Export |
| [Prompt/](Prompt/) | Mom Test · 워크북 |

---

## 생성형 AI 실습 (6시간)

1. 문제 코드 및 기본 요구사항 분석 (0.5h)
2. 기본·품질 요구사항 구현 (2h) — OCP/SRP/입력 검증
3. TC 구현 (0.5h)
4. 추가 요구사항 구현 (2h)
5. 회고 및 발표 (1h)

---

## 저장소

https://github.com/sangryanghuer/UnitConverter_20
