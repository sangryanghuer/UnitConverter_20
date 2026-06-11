# Golden Master — 회귀 고정 (RED)

PRD **golden** 입력으로 `validate_lines` 회귀를 고정하는 RED 테스트를 `tests/`에 추가한다.  
`src/`는 수정하지 않는다. GREEN·REFACTOR는 수행하지 않는다.

추가 인자 없이 `/golden-master` 만으로 동작한다.  
골든 케이스·Test ID는 **`docs/PRD.md`·채팅·`.cursorrules`** 에서 자동 추출한다. **추가 입력·질문 금지.**

SSOT: `docs/PRD.md` · `.cursorrules`

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시:

```
Phase: RED | Kind: golden-master
```

이어서 한국어로 진행한다.

---

## SSOT (읽기)

| 우선순위 | 문서 | 용도 |
|----------|------|------|
| 1 | `docs/PRD.md` | `D-CONV-GM-01` (`meter`, 2.5), `D-CONV-02` (`cubit`, 1) golden 표 |
| 2 | `.cursorrules` | 4단위·소수 4자리 |
| 3 | `tests/test_validate_lines.py` | 중복 방지 |
| 4 | 채팅 | 이번 회귀 대상 |

PRD 미명시 시 기본 골든: **`grid = {"unit": "meter", "value": 2.5}`** → `pass`, 4단위 golden (PRD 표).

---

## 수정 범위

| 허용 | 금지 |
|------|------|
| `tests/` — 골든 RED 추가 | `src/` 수정 |
| tests/ 헬퍼 (golden grid·기대 dict) | GREEN / REFACTOR |
| Test ID docstring | assert 완화 |
| `pytest` 실행·보고 | golden을 `src/`에 하드코딩 |
| | skip / xfail |
| | 브랜치·commit |

---

## 자동 추출 규칙

1. **회귀 유형** — 미커버 시: `meter:2.5` → `status=="pass"`, 4단위 golden, `failed_lines==[]`.
2. **Test ID** — `D-CONV-GM-01` (PRD 우선).
3. **한 묶음** — 골든 `pass` 1건 또는 채팅 단일 회귀 1건.

---

## AAA 절차

1. **Arrange** — `grid = {"unit": "meter", "value": 2.5}` (또는 PRD 케이스).
2. **Act** — `result = validate_lines(grid)`.
3. **Assert** — `status=="pass"`, `failed_lines==[]`, 변환 golden **소수 4자리** (PRD 표: meter 2.5, feet 8.2021, yard 2.7340, cubit 5.4681 — Harness가 `conversions` 키를 쓰면 PRD `convert_units` 계약에 맞춤).

골든 기대값은 **tests/에만** 둔다.

---

## pytest

```bash
pytest tests/test_validate_lines.py::test_d_conv_gm_01 -v
```

**기대: FAILED** — `pass` / golden 미구현.

---

## 보고 형식

```markdown
Phase: RED | Kind: golden-master

## 추가한 테스트
- Test ID: D-CONV-GM-01
- `test_d_conv_gm_01`: meter 2.5 → pass + golden

## 골든 입력
- grid: `{"unit": "meter", "value": 2.5}`

## pytest 결과
- 명령: `pytest …`
- 결과: FAILED — (한 줄)

## 다음 단계
- `/green-minimal` — golden 최소 구현
```

---

## 워크플로

```
/green-minimal (invalid 등) → /golden-master (pass 회귀) → /green-minimal
```

리팩터 전 회귀 안전망. `/refactor-safe` 전 추가 권장.

---

## 참고 (PRD golden, `meter`, 2.5)

| unit | 기대값 (4자리) |
|------|----------------|
| meter | 2.5 |
| feet | 8.2021 |
| yard | 2.7340 |
| cubit | 5.4681 |
