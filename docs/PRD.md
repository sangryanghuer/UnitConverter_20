# UnitConverter_20 — PRD (SSOT)

**버전:** 0.1.0  
**Entity API:** `convert_units`

---

## Mom Test → FR 연결

| Mom Test 증거 | FR |
|---------------|-----|
| ① 2.5m→feet, 5분+ 검색·계산 | FR-CONV-02 |
| ② cubit 침묵, 0.4572m | FR-CONV-03 |
| ③ 매번 막힘, 전 단위 필요 | FR-CONV-04 |
| README 입력 검증 | FR-CONV-01 |

---

## 기준 단위 · 변환 상수 (마법 상수)

판정·계산의 기준은 **meter = 1**(앵커)과 **고정 변환 비율**이다.

| 개념 | UnitConverter_20 |
|------|------------------|
| **앵커** | **meter = 1** (공통 기준) |
| **고정값** | 모든 단위 → **동일 meter량**으로 환산 |
| **검증** | `convert_units`: success / invalid + golden 수치 |

### 기준 단위 (앵커)

- **meter** — `meters_per_unit["meter"] = 1`
- 모든 변환은 먼저 meter로 통일한 뒤, 대상 단위로 나눈다.

### 고정 변환 상수 (v0.1, SSOT)

| 상수명 | 값 | 의미 | 출처 |
|--------|-----|------|------|
| `FEET_PER_METER` | **3.28084** | 1 meter = 3.28084 feet | README |
| `YARDS_PER_METER` | **1.09361** | 1 meter = 1.09361 yard | README |
| `METERS_PER_CUBIT` | **0.4572** | 1 cubit = 0.4572 meter | Mom Test |

Entity 내부 환산:

- `meters_per_unit["feet"]` = 1 / `FEET_PER_METER`
- `meters_per_unit["yard"]` = 1 / `YARDS_PER_METER`
- `meters_per_unit["cubit"]` = `METERS_PER_CUBIT`

**변환 공식:** `meters = value × meters_per_unit[unit]` → `target = meters / meters_per_unit[target]`

테스트(golden)는 위 상수로 계산한 값과 **소수 4자리**까지 일치해야 한다.

---

## Entity 계약 — `convert_units`

MagicSquare `validate_lines(grid)`와 동일한 **구조화 반환** 패턴.

```python
from convert_units import convert_units

result = convert_units(unit, value)
# result["status"]       → "success" | "invalid"
# result["conversions"]  → dict[str, float]  (success일 때만 채움)
# result["failed_fields"] → list[str]       (invalid일 때 원인; success면 [])
```

### Boundary → Entity

| 계층 | 책임 |
|------|------|
| **Boundary** | `단위:값` 문자열 파싱 → `(unit: str, value: float)` 또는 invalid |
| **Entity** | `convert_units(unit, value)` — 순수 변환·검증 |
| **Control** | Boundary 결과를 Entity에 전달, 출력 포맷 (후속) |

Boundary 파싱 실패(콜론 없음, 숫자 아님)는 Entity 호출 전 처리 가능.  
음수·unknown unit은 Entity에서 `invalid` 반환.

---

## 등록 단위 (v0.1)

위 **기준 단위 · 변환 상수**를 Entity 레지스트리에 등록한다.

| unit | meters_per_unit (1 unit = N meter) | 사용 상수 |
|------|-------------------------------------|-----------|
| `meter` | 1 | (앵커) |
| `feet` | 1 / 3.28084 | `FEET_PER_METER` |
| `yard` | 1 / 1.09361 | `YARDS_PER_METER` |
| `cubit` | 0.4572 | `METERS_PER_CUBIT` |

---

## status 규칙

| status | 조건 | conversions | failed_fields |
|--------|------|---------------|---------------|
| `invalid` | `value < 0`, unknown `unit` | `{}` | `["value"]`, `["unit"]` 등 |
| `success` | 등록 단위 + `value ≥ 0` | 4단위 전부 | `[]` |

`validate_lines`의 `incomplete`/`fail`에 대응: 입력·단위 오류 → `invalid`; 변환 성공 → `success`.  
(수치 오차 검증은 Test Loop에서 golden 비교.)

---

## FR · SC · Test ID

| FR | 설명 | SC | Test ID |
|----|------|-----|---------|
| **FR-CONV-01** | invalid — 음수·unknown unit | — | D-CONV-01 |
| **FR-CONV-02** | success — `meter:2.5` golden, 전 단위 | SC-1 | D-CONV-GM-01 |
| **FR-CONV-03** | success — `cubit:1`, 전 단위 | SC-2 | D-CONV-02 |
| **FR-CONV-04** | success — `feet`/`yard` 입력, 전 단위 | SC-3 | D-CONV-03 |

### Golden 기대값 (FR-CONV-02, `meter`, 2.5)

| unit | 기대값 (소수 4자리) |
|------|---------------------|
| meter | 2.5 |
| feet | 8.2021 |
| yard | 2.7340 |
| cubit | 5.4681 |

### Golden 기대값 (FR-CONV-03, `cubit`, 1)

| unit | 기대값 (소수 4자리) |
|------|---------------------|
| meter | 0.4572 |
| feet | 1.4990 |
| yard | 0.5000 |
| cubit | 1.0 |

---

## 이번 세션 범위 외

- 면적·무게 등 다른 카테고리
- JSON/YAML 설정, 동적 등록, CSV/JSON 출력
- Web UI (look & feel는 후속 Track)
