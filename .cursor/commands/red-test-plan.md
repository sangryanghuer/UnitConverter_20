# RED Test Plan — ARRR A단계 (Ask = RED ③)

`validate_lines` / `convert_units` TDD 사이클의 **ARRR A단계(Ask)** 전용 커맨드.  
**C2C 설계표·테스트 플랜만** 작성한다. 테스트·구현 **파일은 생성하지 않는다**.

추가 인자 없이 `/red-test-plan` 만으로 동작한다.  
세션 주제·Test ID·대상 FR은 **현재 채팅 맥락**과 **`docs/PRD.md`**(없으면 `.cursorrules` API·도메인)에서 자동 추출한다.  
**추가 입력·질문 금지** — 정보가 부족하면 SSOT·채팅에서 추론하고 “추론 근거” 한 줄만 명시한다.

SSOT: `docs/PRD.md` · `.cursorrules` · `.cursor/commands/export-session.md`

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시 (값은 세션에 맞게 채움):

```
Phase: red | Layer: entity | Track: Logic
```

| 필드 | 값 | 기본 |
|------|-----|------|
| `Phase` | `red` | 고정 |
| `Layer` | `entity` \| `boundary` | Logic Track → `entity` |
| `Track` | `Logic` \| `UI` | Entity 변환·검증 → `Logic` |

이어서 한국어로 진행한다.

**Track A (boundary):** 본 커맨드 출력 구조는 동일하다. `Layer: boundary`, `Track: UI`로 선언만 바꾸면 재사용 가능하다 (`단위:값` 파싱 등 — 세션 범위 외면 플랜에 명시).

---

## SSOT (읽기 전용)

실행 시 아래를 **읽고** 플랜에 반영한다. **파일을 수정·생성하지 않는다.**

| 우선순위 | 문서 | 용도 |
|----------|------|------|
| 1 | `docs/PRD.md` | FR-CONV-* 인용, Test ID (`D-CONV-*`), golden·상수 |
| 2 | `.cursorrules` | 도메인, API 계약, TDD 규칙 |
| 3 | `tests/test_validate_lines.py` | 기존 Test ID·헬퍼·정책(중복 방지) |
| 4 | 현재 채팅 | 세션 주제, 이번 RED 묶음 범위 |

PRD에 FR·Test ID가 없으면 채팅·`.cursorrules`에서 **다음 미커버 행위 1묶음**을 추론하고, 플랜에 “추론 근거” 한 줄을 명시한다.

---

## 수정 범위

| 허용 | 금지 |
|------|------|
| 채팅 응답으로 **4블록 표** 출력 | `tests/`·`src/` **파일 생성·수정** |
| SSOT **읽기** | `src/` 수정 (구현·시그니처·docstring 포함) |
| | GREEN / REFACTOR 작업 |
| | `pytest.skip`, `xfail`, `@pytest.mark.skip` |
| | assert 완화·삭제를 전제로 한 플랜 |
| | 테스트 본문·스켈레톤 코드 작성 (`/red-skeleton` 역할) |
| | `pytest` 실행·브랜치·commit |

---

## 자동 추출 규칙

1. **세션 주제** — 채팅 최근 턴·PRD·미완 TDD 항목에서 1문장으로 고정.
2. **Layer / Track** — `validate_lines`·`convert_units` 등 Entity면 `entity` + `Logic`.
3. **Test ID** — PRD 명명: `D-CONV-01`, `D-CONV-GM-01`, `D-CONV-02`, `D-CONV-03`. 기존 테스트와 **중복 금지**.
4. **RED 묶음** — 한 턴에 실패시킬 **한 가지 행위**(또는 동일 정책 한 묶음)만.

---

## C2C 규칙 (Rule 1~3)

| Rule | 내용 |
|------|------|
| **Rule 1** | PRD **FR**을 그대로 인용 (예: `FR-CONV-01 invalid — 음수·unknown unit`) |
| **Rule 2** | 해당 FR에 대응하는 **To-Do 1개**만 (동사로 시작, 구현 가능한 한 행위) |
| **Rule 3** | **Test ID** + **Given / When / Then** (각 1문장, 관측 가능한 결과) |

---

## 출력 4블록 (필수, 표 형식)

### 블록 1 — C2C (Rule 1~3)

| PRD FR (인용) | To-Do (1개) | Test ID | Given | When | Then |
|---------------|-------------|---------|-------|------|------|
| … | … | … | … | … | … |

### 블록 2 — Track B 표 (Logic Track 기본)

| Test ID | 대상 함수 | Given → Then | Invariant | Expected RED Failure |
|---------|-----------|--------------|-----------|----------------------|
| … | `validate_lines` | … | … | … |

| 열 | 작성 요령 |
|----|-----------|
| **Given → Then** | `grid={"unit", "value"}` → `status` / `failed_lines` (또는 PRD `conversions`) |
| **Invariant** | `meter=1` 앵커, 4단위 키, PRD 상수·소수 4자리 golden |
| **Expected RED Failure** | 스텁 시 `TypeError`, `AssertionError: status` 등 한 줄 |

### 블록 3 — 테스트 플랜

| 항목 | 내용 |
|------|------|
| **파일 경로** | `tests/test_validate_lines.py` |
| **함수명** | 예: `test_negative_value_is_fail` |
| **conftest / 픽스처** | `grid` 리터럴·헬퍼 **이름만** |
| **pytest 명령** | `pytest tests/test_validate_lines.py::test_... -v` |
| **RED 묶음 범위** | 이번 Test ID 목록 (1묶음) |

### 블록 4 — ECB·Mock 점검

| 점검 항목 | Logic Track (`entity`) | 비고 |
|-----------|------------------------|------|
| **ECB 분류** | **Entity** — 순수 변환·검증 | Boundary 파싱은 범위 외 |
| **Domain Mock** | **금지** — Entity mock/patch 없음 | |
| **E001~E005 emit** | **금지** | |
| **외부 의존** | 없음 (`grid` in → dict out) | |

---

## 보고 형식 (템플릿)

```markdown
Phase: red | Layer: entity | Track: Logic

## 1. C2C (Rule 1~3)
| PRD FR (인용) | To-Do (1개) | Test ID | Given | When | Then |
| … | … | … | … | … | … |

## 2. Track B 표
| Test ID | 대상 함수 | Given → Then | Invariant | Expected RED Failure |
| … | … | … | … | … |

## 3. 테스트 플랜
| 항목 | 내용 |
| … | … |

## 4. ECB·Mock 점검
| 점검 항목 | Logic Track | 비고 |
| … | … | … |

/red-skeleton 으로 넘길 준비됐다
```

마지막 줄은 **한 줄로 그대로** 출력한다.

---

## 참고 (도메인·API)

- **앵커**: `meter = 1` · **단위**: `meter`, `feet`, `yard`, `cubit`
- **Harness**: `validate_lines(grid)` — `grid = {"unit": str, "value": float}`
- **반환**: `{status: pass|fail|incomplete, failed_lines: [...]}`
- **PRD Entity**: `convert_units` — `pass`↔`success`, `fail`↔`invalid`, `failed_lines`↔`failed_fields`
- **golden**: PRD § FR · SC · Test ID (소수 4자리)

---

## 워크플로 (ARRR)

```
A  Ask      →  /red-test-plan
R  RED      →  /red-skeleton · /tdd-red · /golden-master
R  Run      →  /green-minimal
R  Refine   →  /refactor-smell · /refactor-safe
Export       →  /export-session
```

Skill: `.cursor/skills/magic-square-tdd/SKILL.md`
