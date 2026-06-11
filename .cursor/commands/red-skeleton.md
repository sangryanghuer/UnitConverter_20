# RED Skeleton — ARRR RED ④ (테스트 골격·본문)

`/red-test-plan` 산출물(C2C·Track B·테스트 플랜)을 바탕으로 **실패하는 RED 테스트 골격·본문**을 `tests/`에 작성한다.  
`src/`는 건드리지 않는다. GREEN·REFACTOR는 수행하지 않는다.

추가 인자 없이 `/red-skeleton` 만으로 동작한다.  
Test ID·함수명·Assert는 **직전 `/red-test-plan` 응답**(또는 채팅 RED 묶음)에서 자동 추출한다.  
**추가 입력·질문 금지** — 플랜 없으면 SSOT에서 한 RED 묶음만 추론한다.

SSOT: `docs/PRD.md` · `.cursorrules`

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시 (`/red-test-plan`과 동일 Layer·Track):

```
Phase: red | Layer: entity | Track: Logic
```

이어서 한국어로 진행한다.

---

## 선행 조건

- 직전 턴 또는 같은 세션에 **`/red-test-plan` 4블록**이 있어야 한다.
- 플랜 없으면 SSOT를 읽고 **한 RED 묶음**만 추론한 뒤, “플랜 미확인 — 추론 적용”을 명시한다.

---

## 수정 범위

| 허용 | 금지 |
|------|------|
| `tests/` **생성·수정** | `src/` 수정 |
| Test ID 주석·docstring·함수명 | assert 완화·삭제 |
| 플랜 명시 conftest·픽스처만 | `pytest.skip`, `xfail`, `@pytest.mark.skip` |
| RED 대상 `pytest` 실행·보고 | GREEN / REFACTOR |
| | Domain Mock (Entity patch) |
| | 플랜 밖 Test ID·행위 추가 |
| | 브랜치·commit |

---

## Test ID → 코드 매핑

| 항목 | 규칙 |
|------|------|
| **함수명** | `D-CONV-01` → `test_d_conv_01` (하이픈→언더스코어, 소문자) |
| **Test ID** | docstring: `Test ID: D-CONV-01` |
| **FR** | docstring: `FR: FR-CONV-01` |
| **AAA 주석** | `# Arrange` / `# Act` / `# Assert` 필수 |

---

## AAA 절차 (Logic Track)

1. **Arrange** — `grid = {"unit": str, "value": float}`. PRD 등록 단위·golden 입력.
2. **Act** — `result = validate_lines(grid)` 한 번.
3. **Assert** — `status`, `failed_lines` (한 가지 행위만). golden은 **소수 4자리**.

---

## pytest

```bash
pytest tests/test_validate_lines.py::test_d_conv_01 -v
```

**기대: FAILED** — 스텁(`...` / `None`) 또는 미구현.

통과하면 RED 아님 → assert·플랜 재검토. `src/` 우회 금지.

---

## 보고 형식

```markdown
Phase: red | Layer: entity | Track: Logic

## 반영한 플랜
- RED 묶음: D-CONV-01 (FR-CONV-01)
- 출처: /red-test-plan (또는 추론)

## 변경 파일
- `tests/test_validate_lines.py`: `test_d_conv_01` 추가

## 테스트 요약
- Given / When / Then: …

## pytest 결과
- 명령: `pytest …`
- 결과: FAILED — (메시지 한 줄)

## 다음 단계
- `/green-minimal` — `src/validate_lines.py` 최소 구현
```

---

## 워크플로 (ARRR)

```
/red-test-plan → /red-skeleton → /green-minimal
              ↘ /tdd-red (선택)
              ↘ /golden-master (회귀 RED)
```

---

## 참고 (API)

- `validate_lines(grid) -> {status, failed_lines}`
- `status`: `"pass"` | `"fail"` | `"incomplete"`
- PRD: `convert_units` — `success` / `invalid` / `failed_fields` / `conversions`
