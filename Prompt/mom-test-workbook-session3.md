# MagicSquare_1004 세션 3 워크북 — UnitConverter_20

**일자:** 2026-06-11  
**Mom Test 자가 채점:** 10 / 10

---

## Mom Test 결과

### 페르소나
수업 중 선생님이 **feet·yard·cubit** 등 **길이 단위 변환**을 **즉석에서** 물어보는 환경의 **학습자**. 비율을 **머릿속에 두기 어렵고**, 질문할 때마다 **검색·계산·침묵**으로 버틴다.

### 진짜 문제 (한 문장)
수업 중 선생님이 길이 단위 변환을 물을 때마다 **단위·비율이 기억나지 않아 매번 막히고**, 검색·계산에 **5분 넘게** 걸리거나 **침묵**하게 되며 **스트레스와 창피함**을 겪는다.

### Mom Test 증거 3줄
1. **2.5m→feet** 질문에 **검색 5분+** — 결과는 **1m 기준**만 있어 **계산기로 2.5배** 계산 후에야 답함.
2. **1 cubit=? meter** 질문에 **침묵** → 다른 학생이 답 → **창피**; 수업 후 검색해 **0.4572m**를 알았지만 **머릿속만** 기억.
3. **feet·yard·cubit** 질문이 **반복**되는데, **매번** 비율이 기억나지 않아 막힘(생소 단위만이 아님).

### Mom Test 채점 체크리스트

| 항목 | 충족 |
|------|------|
| 미래 가정("~하면 좋겠다") 없음 | ✓ |
| 과거 행동·시간·실수 구체성 있음 | ✓ |
| 진짜 문제에 솔루션名(TDD/PyQt/Cursor) 없음 | ✓ |
| 표면 문제와 진짜 문제가 분리됨 | ✓ |

---

## 1) 주제 한 문장 (Mom Test 기반, 솔루션 최소화)

> **수업 중 길이 단위 변환 질문에 답할 때, 비율 기억 실패·검색·수동 계산·침묵으로 겪는 시간·불안·창피가 반복되는지 과거 행동으로 확인한다.**

---

## 2) R-G-I-O

**SSOT:** [docs/PRD.md](../docs/PRD.md)

| | 내용 |
|---|------|
| **Role** | **Entity** — `convert_units(unit, value)` 순수 변환. **Boundary** — `단위:값` 파싱. **Control** — 흐름·출력(후속). |
| **Goal** | meter 기준 **등록 4단위**(meter/feet/yard/cubit) 변환 결과를 **한 번에** `{ status, conversions, failed_fields }`로 반환한다. |
| **Input** | Entity: `unit: str`, `value: float` (`value ≥ 0`, 등록 unit). Boundary: `meter:2.5`, `cubit:1` 등 문자열 파싱. |
| **Output** | `status`: `"success"` \| `"invalid"` · `conversions`: 4단위 dict (success) · `failed_fields`: `[]` \| `["value"]` \| `["unit"]` (`validate_lines`의 `failed_lines` 대응) |

### Entity API

```python
result = convert_units(unit, value)
# result["status"]        → "success" | "invalid"
# result["conversions"]   → {"meter", "feet", "yard", "cubit"}
# result["failed_fields"] → list[str]
```

### 기준 단위 · 변환 상수 (마법 상수)

MagicSquare **34** ↔ **meter = 1** + `FEET_PER_METER` / `YARDS_PER_METER` / `METERS_PER_CUBIT`.  
→ [docs/PRD.md § 기준 단위 · 변환 상수](../docs/PRD.md#기준-단위--변환-상수-마법-상수)

---

## 3) 성공 기준 · FR · Test ID (Mom Test 증거 연결)

| SC | 성공 기준 | Mom Test | FR | Test ID |
|----|-----------|----------|-----|---------|
| — | `value < 0` 또는 unknown unit → `invalid`, `failed_fields` 채움 | README 검증 | FR-CONV-01 | D-CONV-01 |
| **SC-1** | `meter:2.5` → 전 단위 golden, `status=success` | ① 5분+·1m·계산기 | FR-CONV-02 | D-CONV-GM-01 |
| **SC-2** | `cubit:1` → 전 단위, `status=success` | ② 침묵·0.4572m | FR-CONV-03 | D-CONV-02 |
| **SC-3** | `feet` 또는 `yard` 입력 → 4단위 한 번에 | ③ 매번 막힘·기억 | FR-CONV-04 | D-CONV-03 |

---

## 4) 표면 문제 — 이번 프로젝트에서 하지 않을 것

| 표면 (X) | 진짜 문제와의 관계 |
|----------|-------------------|
| 면적·무게·온도 등 **다른 카테고리** | Mom Test pain은 **수업 길이 단위**에서만 확인 |
| **풀 모바일 UI**(키패드·전 탭) | pain은 **기억·즉답**; 꾸미기는 표면 |
| JSON·동적 등록·CSV 출력 | README 후속; **기억·매번 막힘**과 무직접 |
| "앱 만들기""TDD 하기" | **방법·솔루션 이름**이지 진짜 문제 아님 |
| 검색/API 품질 개선 | 과거 pain은 **내 기억·계산** 쪽 |

**진짜 문제:** 비율 기억 실패 → 매번 막힘 → 시간·침묵·창피  
**표면 문제:** 그 외 범위·기술·카테고리 확장

---

## 8계층 — 이번 세션에서 만드는 것만

| 계층 | 산출 |
|------|------|
| **Rule** | `.cursorrules` — meter 기준 4단위, `convert_units` 계약, RED→GREEN→REFACTOR |
| **Command** | `/red-test-plan`, `/tdd-red`, `/green-minimal`, `/refactor-safe`, `/export-session` |
| **(Skill)** | `.cursor/skills/unit-converter-tdd/SKILL.md` — FR-CONV-* ↔ D-CONV-* |
| **Test Loop** | `tests/test_convert_units.py` + `src/convert_units.py` |

**이번 세션에서 만들지 않음:** GUI Track, Control/Boundary 전체 ECB, 설정 외부화, 배포·CI.

---

## 보완 인터뷰 (채점 후)

**Q (수정):** feet·yard는 cubit처럼 침묵했어, 아니면 검색·계산이 필요했어?  
**A:** 매번 막혀, 단위가 잘 기억이 안 남.

**Q9 (수정안):** 길이 단위(feet, yard, cubit) 변환 질문을 받을 때, 비율이 기억 안 나서 막힌 적이 있어? 가장 최근에는 어떤 단위였고, 그때 몇 분 정도 걸렸어?
