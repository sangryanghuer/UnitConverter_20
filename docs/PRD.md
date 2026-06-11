# UnitConverter_20 — PRD (SSOT)

**버전:** 0.1.0  
**최종 갱신:** 2026-06-11  
**저장소:** https://github.com/sangryanghuer/UnitConverter_20  
**문제 정의:** [Report/01.UnitConvertor_ProblemDefinition_Report.md](../Report/01.UnitConvertor_ProblemDefinition_Report.md)

> 본 문서는 `UnitConverter_20` 저장소의 **단일 진실 원천(SSOT)** 이다.  
> Mom Test · Report · README · `.cursorrules` · `src/` · `tests/` · `web/` 내용을 취합·정리했다.

---

## 1. 제품 개요

수업 중 길이 단위 변환 질문에 **한 번에** 답할 수 있는 Unit Converter.  
Mom Test → PRD → TDD(ARRR) 순으로 요구사항을 고정하고, Cursor로 RED→GREEN→REFACTOR를 진행한다.

| 항목 | 내용 |
|------|------|
| **입력** | `단위:값` (예: `meter:2.5`) 또는 Entity `(unit, value)` |
| **출력** | 등록 **4단위**(`meter`, `feet`, `yard`, `cubit`) 변환 결과 |
| **앵커** | `meter = 1` — 모든 값을 meter로 통일 후 대상 단위로 환산 |
| **Entity API** | `convert_units(unit, value)` → `{ status, conversions, failed_fields }` |
| **Harness** | `validate_lines(grid)` — `grid = {"unit", "value"}` → `convert_units` 위임 |

---

## 2. 문제 정의 (Mom Test)

### 2.1 페르소나

수업 중 선생님이 **feet·yard·cubit** 등 **길이 단위 변환**을 **즉석에서** 물어보는 환경의 **학습자**.  
비율을 **머릿속에 두기 어렵고**, 질문할 때마다 **검색·계산·침묵**으로 버틴다.

### 2.2 진짜 문제 (한 문장)

> 수업 중 선생님이 길이 단위 변환을 물을 때마다 **단위·비율이 기억나지 않아 매번 막히고**, 검색·계산에 **5분 넘게** 걸리거나 **침묵**하게 되며 **스트레스와 창피함**을 겪는다.

### 2.3 Mom Test 증거 → FR

| # | 과거 행동 (증거) | FR |
|---|------------------|-----|
| ① | **2.5m→feet** 질문에 **검색 5분+** — 1m 기준만 있어 **계산기로 2.5배** | FR-CONV-02 |
| ② | **1 cubit=? meter** 질문에 **침묵** → 창피; 수업 후 **0.4572m** 검색 | FR-CONV-03 |
| ③ | **feet·yard·cubit** 질문 **반복**, **매번** 비율 기억 실패 | FR-CONV-04 |
| — | 음수·unknown unit 입력 검증 | FR-CONV-01 |

### 2.4 Pain Points

| # | Pain |
|---|------|
| P1 | feet·yard·cubit 비율 **기억 실패** |
| P2 | 수업 중 **즉답 압박** (5분+ 스트레스) |
| P3 | 검색 결과 **1m 기준만** → 수동 배율 계산 |
| P4 | **침묵·창피** (cubit 등 모를 때) |

---

## 3. 범위

### 3.1 v0.1 (현재)

- 길이 **4단위** 등록·변환
- Entity `convert_units` + pytest TDD
- Golden Master 승인 테스트 (소수 4자리)
- Harness adapter `validate_lines`
- 레거시 CLI (`UnitConverter.py`) · Web UI (`web/` + `src/web_server.py`)

### 3.2 범위 외 (후속 Track)

| 항목 | 사유 |
|------|------|
| 면적·무게·온도 등 다른 카테고리 | Mom Test pain은 **수업 길이 단위**만 |
| JSON/YAML 설정 · 동적 단위 등록 · CSV/JSON 출력 | 기억·즉답 pain과 무직접 |
| Boundary/Control 전체 · 풀 모바일 UX | 후속 Track A |
| CI·배포 | 세션 범위 외 |
| OCP/SRP 대규모 리팩터 · 설정 외부화 | 원본 실습 후속 |

---

## 4. 아키텍처 (ECB)

| 계층 | 책임 | 구현 (현재) |
|------|------|-------------|
| **Boundary** | `단위:값` 문자열 파싱 · HTTP 요청 처리 · UI | `UnitConverter.py` (`_parse_unit_value`), `src/web_server.py` (`POST /api/convert`), `web/app.js` |
| **Entity** | 순수 변환·검증 | `src/convert_units.py` |
| **Control** | 흐름·출력 포맷 조율 | CLI `main()`, Web form submit (부분) |
| **Harness** | Test Loop 진입점 (MagicSquare 호환) | `src/validate_lines.py` → `convert_units` 위임 |

Boundary 파싱 실패(콜론 없음, 숫자 아님)는 Entity 호출 전 처리 가능.  
음수·unknown unit은 Entity에서 `invalid` 반환.

### Dual-Track TDD

| Track | Layer | 대상 | Test ID | 상태 |
|-------|-------|------|---------|------|
| **B (Logic)** | Entity | `convert_units` / `validate_lines` | D-CONV-01, D-CONV-GM-01, D-CONV-02, D-CONV-03 | **완료** (8 passed) |
| **A (UI)** | Boundary | `단위:값` 파싱·출력·흐름 | U-IN-01~05, U-OUT-01, U-FLOW-02 | 후속 |

Track B: **Domain Mock 금지** · golden **소수 4자리**.

---

## 5. 도메인 · 마법 상수

### 5.1 앵커 · 공식

- **앵커:** `meter = 1` (`meters_per_unit["meter"] = 1`)
- **공식:** `meters = value × meters_per_unit[unit]` → `target = meters / meters_per_unit[target]`
- **반올림:** 결과는 **소수 4자리** (`round(..., 4)`)

### 5.2 고정 변환 상수 (SSOT)

| 상수명 | 값 | 의미 | 출처 |
|--------|-----|------|------|
| `FEET_PER_METER` | **3.28084** | 1 meter = 3.28084 feet | README |
| `YARDS_PER_METER` | **1.09361** | 1 meter = 1.09361 yard | README |
| `METERS_PER_CUBIT` | **0.4572** | 1 cubit = 0.4572 meter | Mom Test |

### 5.3 등록 단위 레지스트리

| unit | meters_per_unit (1 unit = N meter) | 사용 상수 |
|------|-------------------------------------|-----------|
| `meter` | 1 | (앵커) |
| `feet` | 1 / 3.28084 | `FEET_PER_METER` |
| `yard` | 1 / 1.09361 | `YARDS_PER_METER` |
| `cubit` | 0.4572 | `METERS_PER_CUBIT` |

구현: `REGISTERED_UNITS`, `METERS_PER_UNIT` in `src/convert_units.py`.

---

## 6. API 계약

### 6.1 Entity — `convert_units(unit, value) -> dict`

```python
from convert_units import convert_units

result = convert_units(unit, value)
# result["status"]        → "success" | "invalid"
# result["conversions"]   → dict[str, float]  (success: 4단위 전부)
# result["failed_fields"] → list[str]         (invalid: ["value"] | ["unit"]; success: [])
```

| status | 조건 | conversions | failed_fields |
|--------|------|-------------|---------------|
| `invalid` | `value < 0` | `{}` | `["value"]` |
| `invalid` | unknown `unit` | `{}` | `["unit"]` |
| `success` | 등록 단위 + `value ≥ 0` | 4단위 전부 | `[]` |

### 6.2 Harness — `validate_lines(grid) -> dict`

```python
# grid = {"unit": str, "value": float}
# 반환: convert_units(grid["unit"], grid["value"]) 와 동일 (thin adapter)
```

| Harness (레거시 명칭) | PRD Entity |
|----------------------|------------|
| `pass` | `success` |
| `fail` | `invalid` |
| `failed_lines` | `failed_fields` |

### 6.3 Boundary — Web API

| 항목 | 내용 |
|------|------|
| **Endpoint** | `POST /api/convert` |
| **Request** | `{"unit": str, "value": number}` (JSON) |
| **Response** | `convert_units` 결과와 동일 JSON |
| **파싱 실패** | HTTP 400, `{status:"invalid", failed_fields:["parse"], conversions:{}}` |
| **서버** | `python src/web_server.py` → http://127.0.0.1:8080 |

### 6.4 Boundary — CLI

| 항목 | 내용 |
|------|------|
| **실행** | `python UnitConverter.py` |
| **입력** | `unit:value` (예: `meter:2.5`) |
| **파싱 오류** | 형식 오류·숫자 오류 메시지 후 종료 |
| **Entity 오류** | `invalid` → 사용자 메시지 (음수 / unknown unit) |
| **성공** | 4단위 변환 결과 stdout |

---

## 7. 기능 요구사항 (FR) · 성공 기준 (SC) · Test ID

| FR | 설명 | SC | Test ID | 테스트 파일 |
|----|------|-----|---------|-------------|
| **FR-CONV-01** | invalid — 음수·unknown unit | — | D-CONV-01 | `tests/test_validate_lines.py` |
| **FR-CONV-02** | success — `meter:2.5` golden, 전 단위 | SC-1 | D-CONV-GM-01 | `test_d_conv_gm_01`, `tests/entity/test_fr_conv_02.py` |
| **FR-CONV-03** | success — `cubit:1`, 전 단위 | SC-2 | D-CONV-02 | `test_d_conv_02`, `tests/entity/test_fr_conv_03.py` |
| **FR-CONV-04** | success — `feet`/`yard` 입력, 전 단위 | SC-3 | D-CONV-03 | `test_d_conv_03`, `tests/entity/test_fr_conv_04.py` |

### 7.1 Golden — FR-CONV-02 (`meter`, 2.5)

| unit | 기대값 (4자리) | 승인 파일 |
|------|----------------|-----------|
| meter | 2.5000 | `tests/golden/rd_conv_02_g1_step_a.approved.txt` |
| feet | 8.2021 | |
| yard | 2.7340 | |
| cubit | 5.4681 | |

### 7.2 Golden — FR-CONV-03 (`cubit`, 1)

| unit | 기대값 (4자리) | 승인 파일 |
|------|----------------|-----------|
| meter | 0.4572 | `tests/golden/fr_conv_03_g1_step_a.approved.txt` |
| feet | 1.5000 | |
| yard | 0.5000 | |
| cubit | 1.0000 | |

### 7.3 Golden — FR-CONV-04 (`feet`, 1)

| unit | 기대값 (4자리) | 승인 파일 |
|------|----------------|-----------|
| meter | 0.3048 | `tests/golden/fr_conv_04_g1_step_a.approved.txt` |
| feet | 1.0000 | |
| yard | 0.3333 | |
| cubit | 0.6667 | |

### 7.4 Golden Master 포맷

`tests/_approval.py` — `format_convert_units_result()` 고정 포맷:

```
status:success
failed_fields:
conversions:
meter:2.5000
feet:8.2021
yard:2.7340
cubit:5.4681
```

갱신: `UPDATE_GOLDEN=1 pytest <test> -v`

---

## 8. 구현 현황 (코드베이스 스냅샷)

| 구성요소 | 파일 | 상태 |
|----------|------|------|
| Entity | `src/convert_units.py` | ✅ 구현 (`_to_meters`, `_from_meters`, `_convert_all_units`, `_invalid_response`, `_success_response`) |
| Harness | `src/validate_lines.py` | ✅ adapter |
| CLI Boundary | `UnitConverter.py` | ✅ `convert_units` 연동 |
| Web Boundary | `src/web_server.py`, `web/*` | ✅ POST `/api/convert`, teal 모바일 look & feel |
| 단위 테스트 | `tests/test_validate_lines.py` | ✅ 5 tests (D-CONV-01~03, GM-01) |
| Golden 테스트 | `tests/entity/test_fr_conv_*.py` | ✅ 3 tests |
| 승인 harness | `tests/_approval.py` | ✅ |
| pytest 설정 | `pyproject.toml` | ✅ `pythonpath = ["src"]` |

**pytest:** `tests/` 전체 **8 passed** (Report/06 기준).

---

## 9. 프로젝트 구조

```
UnitConverter_20/
├── docs/PRD.md                          # 본 문서 (SSOT)
├── .cursorrules                         # 도메인·API·TDD 규칙
├── .cursor/commands/                    # ARRR 슬래시 커맨드
├── .cursor/skills/                      # TDD·문서 Skill
├── src/
│   ├── convert_units.py                 # Entity (PRD API)
│   ├── validate_lines.py                # Harness adapter
│   └── web_server.py                    # Web Boundary
├── web/                                 # HTML UI (index.html, app.js, style.css)
├── tests/
│   ├── test_validate_lines.py           # FR 단위·golden 테스트
│   ├── entity/test_fr_conv_*.py         # Golden Master 승인
│   ├── _approval.py                     # 승인 포맷·비교
│   └── golden/*.approved.txt            # Golden 기준 파일
├── UnitConverter.py                     # CLI Boundary
├── pyproject.toml                       # pytest
├── Report/                              # 세션 보고서
├── Prompting/                           # Transcript Export
└── Prompt/                              # Mom Test · 워크북
```

---

## 10. TDD · 품질 규칙

### 10.1 ARRR 사이클

| Phase | 수정 범위 | 금지 |
|-------|-----------|------|
| **RED** | `tests/`만 | `src/` 구현, assert 완화·skip·xfail |
| **GREEN** | `src/`만 | 테스트 변경 |
| **REFACTOR** | `src/`·`tests/` | 행위 불변, pytest 전체 통과 |

한 턴에 한 Phase. AI 응답 첫 줄: `Phase: RED` / `Phase: GREEN` / `Phase: REFACTOR`.

### 10.2 Cursor 커맨드

| 커맨드 | Phase | 역할 |
|--------|-------|------|
| `/red-test-plan` | Ask | C2C·테스트 플랜 |
| `/red-skeleton` | RED | tests/ 골격 |
| `/tdd-red` | RED | 실패 테스트 추가 |
| `/golden-master` | RED | golden 회귀 |
| `/green-minimal` | Run | src/ 최소 구현 |
| `/refactor-smell` | Refine | 스멜 분석 |
| `/refactor-safe` | Refine | 안전 리팩터 |
| `/export-session` | Export | Report + Transcript |

### 10.3 실행

```bash
pip install pytest
pytest tests/ -v
python UnitConverter.py
python src/web_server.py   # http://127.0.0.1:8080
```

---

## 11. R-G-I-O 요약

| | 내용 |
|---|------|
| **Role** | Entity `convert_units` · Boundary 파싱/UI · Control 흐름(후속) |
| **Goal** | meter 기준 4단위 변환 결과를 **한 번에** 구조화 반환 |
| **Input** | `unit: str`, `value: float` (`value ≥ 0`, 등록 unit) |
| **Output** | `{ status, conversions, failed_fields }` |

---

## 12. 관련 문서

| 경로 | 내용 |
|------|------|
| [Report/01.UnitConvertor_ProblemDefinition_Report.md](../Report/01.UnitConvertor_ProblemDefinition_Report.md) | Mom Test 문제 정의 |
| [Report/01.REPORT.md](../Report/01.REPORT.md) ~ [06.REPORT.md](../Report/06.REPORT.md) | 세션별 ARRR 보고서 |
| [Prompt/mom-test-interview.md](../Prompt/mom-test-interview.md) | Mom Test Q&A 원문 |
| [Prompt/mom-test-workbook-session3.md](../Prompt/mom-test-workbook-session3.md) | Mom Test 워크북 |
| [Prompting/](../Prompting/) | Cursor Transcript Export |
| [README.md](../README.md) | 설치·실행·개요 |

---

## 13. 변경 이력

| 버전 | 일자 | 내용 |
|------|------|------|
| 0.1.0 | 2026-06-11 | Mom Test 문제 정의 · Entity API · FR/golden · 구현·테스트 취합 SSOT |
