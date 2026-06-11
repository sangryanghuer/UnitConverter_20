# TDD RED — validate_lines

`validate_lines(grid)` TDD 사이클의 **RED 단계 전용** 커맨드.  
한 턴에 **실패하는 테스트 하나(또는 한 묶음)** 만 추가한다. GREEN·REFACTOR는 수행하지 않는다.

SSOT: `docs/PRD.md` · 루트 `.cursorrules`

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시:

```
Phase: RED
```

이어서 한국어로 진행한다.

---

## 수정 범위

| 허용 | 금지 |
|------|------|
| `tests/` 아래 파일만 | `src/` 수정 (구현·시그니처·docstring 변경 포함) |
| | assert 완화·삭제 (`==` → `in`, 조건 제거, `pytest.approx`로 기준 낮추기 등) |
| | `pytest.skip`, `xfail`, `@pytest.mark.skip` |
| | GREEN / REFACTOR 작업을 같은 턴에 섞기 |

---

## AAA 절차

각 테스트는 **Arrange → Act → Assert** 순서로 작성한다.

1. **Arrange** — `grid` 입력 준비. 리터럴·헬퍼 사용.
   - `grid`: `{"unit": str, "value": float}` — PRD Entity 입력 `(unit, value)`에 대응
   - 등록 단위: `meter`, `feet`, `yard`, `cubit` (4종)
   - 앵커·상수: PRD § 기준 단위 · 변환 상수 (`meter = 1`, `FEET_PER_METER` 등)
   - Test ID 주석 권장: `# D-CONV-01` …

2. **Act** — `result = validate_lines(grid)` 한 번 호출.

3. **Assert** — API 계약 검증:
   - `result["status"]` ∈ `"pass"` | `"fail"` | `"incomplete"`
   - `result["failed_lines"]`는 `list[str]` (예: `["unit"]`, `["value"]`)
   - 이번 RED가 고정하는 **한 가지 행위**만 assert (여러 케이스를 한 테스트에 우겨 넣지 않음)
   - golden 수치 assert 시 **소수 4자리**까지 (PRD golden 표)

RED 직후 `pytest`는 **반드시 실패**해야 한다 (구현 스텁 `...` → 미구현·`None` 반환 포함).

---

## pytest 예시

`tests/test_validate_lines.py`에 추가하는 형태:

```python
def test_negative_value_is_fail():  # D-CONV-01
    # Arrange
    grid = {"unit": "meter", "value": -1.0}

    # Act
    result = validate_lines(grid)

    # Assert
    assert result["status"] == "fail"
    assert result["failed_lines"] == ["value"]
```

실행:

```bash
pytest tests/test_validate_lines.py -v
```

기대: **FAILED** (아직 `src/validate_lines.py` 미구현).

---

## 보고 형식

RED 작업 후 아래 순서로 보고한다.

```markdown
Phase: RED

## 추가한 테스트
- `test_...` (D-CONV-XX): (한 줄 — 무엇을 검증하는지)

## Arrange 요약
- grid: `{"unit": "...", "value": ...}`

## Assert 요약
- status: ...
- failed_lines: ...

## pytest 결과
- 명령: `pytest tests/test_validate_lines.py -v`
- 결과: FAILED — (실패 메시지 한 줄)

## 다음 단계
- GREEN: `src/validate_lines.py`에서 위 테스트를 통과시킬 최소 구현
```

---

## 참고 (계약)

| status | 조건 (요약) | failed_lines |
|--------|-------------|--------------|
| `pass` | 등록 단위 + `value ≥ 0`, golden 충족 | `[]` |
| `fail` | 입력은 완전하나 invalid (`value < 0`, unknown `unit`, 수치 불일치 등) | `["value"]`, `["unit"]` 등 |
| `incomplete` | 아직 판정 불가 — **이 RED 테스트에서 정책을 명시적으로 고정** | 테스트에서 고정 |

PRD `convert_units`와 이름만 다름: `pass`↔`success`, `fail`↔`invalid`, `failed_lines`↔`failed_fields`.
