# GREEN Minimal — ARRR Run (최소 구현)

직전 RED(`/red-skeleton` · `/tdd-red` · `/golden-master`)가 실패하던 테스트를 **최소 구현**으로 통과시킨다.  
`src/`만 수정한다. REFACTOR·테스트 변경은 하지 않는다.

추가 인자 없이 `/green-minimal` 만으로 동작한다.  
대상 Test ID·함수는 **채팅·`tests/`·직전 RED 보고**에서 자동 추출한다. **추가 입력·질문 금지.**

SSOT: `docs/PRD.md` · `.cursorrules`

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시:

```
Phase: GREEN
```

이어서 한국어로 진행한다.

---

## SSOT (읽기)

| 우선순위 | 문서 | 용도 |
|----------|------|------|
| 1 | 직전 RED 보고·실패 `pytest` | 통과 대상 Test ID·assert |
| 2 | `tests/test_validate_lines.py` | 변경 금지 — 기대값 확인 |
| 3 | `docs/PRD.md` | FR·status·golden |
| 4 | `.cursorrules` | API·GREEN 규칙 |

---

## 수정 범위

| 허용 | 금지 |
|------|------|
| `src/` **최소 구현** (`src/validate_lines.py`) | `tests/` 수정 |
| RED 묶음 통과에 필요한 코드만 | REFACTOR |
| `pytest` 실행·보고 | assert 완화를 위한 테스트 변경 |
| | RED+GREEN 한 턴 혼합 |
| | 플랜 밖 행위 선구현 |
| | 브랜치·commit |

---

## 자동 추출 규칙

1. **대상 테스트** — 최근 RED에서 추가·실패한 `test_*`.
2. **최소 범위** — 해당 assert만 만족. 미RED 행위는 구현하지 않음.
3. **정책** — 테스트에 적힌 `status`·`failed_lines` 그대로 따름.

---

## 구현 원칙

1. **Fake it** — 하드코딩·최소 분기로 통과 가능하면 우선 허용.
2. **한 묶음** — 이번 RED만 녹색. 전체 스위트 실패 0 유지.
3. **계약** — 반환 dict에 `status`, `failed_lines` 키 유지.

---

## pytest

```bash
pytest tests/test_validate_lines.py -v
```

**기대:** RED 대상 **PASSED**, 전체 **0 failed**.

---

## 보고 형식

```markdown
Phase: GREEN

## 대상 RED
- Test ID: D-CONV-01
- 함수: `test_d_conv_01`

## 변경 파일
- `src/validate_lines.py`: (한 줄)

## 구현 요약
- …

## pytest 결과
- 명령: `pytest tests/test_validate_lines.py -v`
- 결과: PASSED (N passed)

## 다음 단계
- `/red-test-plan` → 다음 RED
- `/golden-master` (회귀 고정)
- `/refactor-smell` → `/refactor-safe`
```

---

## 참고

- GREEN은 **방금 RED한 행위**만 구현한다.
- PRD 상수·golden: `docs/PRD.md` § 기준 단위 · FR · SC · Test ID
