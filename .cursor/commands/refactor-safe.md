# Refactor Safe — 안전 리팩터 (REFACTOR)

`/refactor-smell` 목록(또는 채팅)에서 **한 건**만 안전하게 리팩터한다.  
**전체 pytest 통과**를 유지한다.

추가 인자 없이 `/refactor-safe` 만으로 동작한다.  
대상 스멜은 **직전 smell 표·워크스페이스**에서 자동 추출한다. **추가 입력·질문 금지.**

SSOT: `.cursorrules` · `docs/PRD.md`

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시:

```
Phase: REFACTOR | Mode: safe
```

이어서 한국어로 진행한다.

---

## 수정 범위

| 허용 | 금지 |
|------|------|
| `src/` 구조·이름·중복 제거 | **행위 변경** (새 FR·status 규칙) |
| `tests/` — 동작 동일 리네임·헬퍼 | assert·기대값 변경 |
| 한 턴 **리팩터 1건** | RED / GREEN |
| 리팩터 전후 `pytest` 전체 | skip / xfail |
| | smell 표 없는 대규모 재설계 |
| | 브랜치·commit |

---

## 자동 추출 규칙

1. **한 건** — 스멜 표 **맨 위 1건** (심각도·안전성).
2. **불변** — `validate_lines(grid)` 시그니처·테스트 기대값.
3. **회귀** — `pytest tests/ -v` **0 failed**. 실패 시 롤백·보고.

---

## 안전 리팩터 패턴 (허용)

- PRD 상수명 추출 (`FEET_PER_METER`, `METERS_PER_CUBIT`)
- `_to_meters`, `_from_meters` private 헬퍼
- `meters_per_unit` 레지스트리 dict
- 테스트 Arrange 헬퍼 공유 (기대값 불변)

---

## pytest

```bash
pytest tests/ -v
```

**기대: 전체 PASSED.**

---

## 보고 형식

```markdown
Phase: REFACTOR | Mode: safe

## 대상 스멜
- ID: S02 — …

## 변경 파일
- `src/validate_lines.py`: …

## 리팩터 요약
- …

## pytest 결과
- PASSED (N passed)

## 남은 스멜
- …

## 다음 단계
- `/refactor-safe` 반복 또는 `/red-test-plan`
```

---

## 참고

- 리팩터 ≠ 설계 변경 — 테스트가 정의한 행위 유지.
- 골든 없으면 `/golden-master` 선행 권장.
