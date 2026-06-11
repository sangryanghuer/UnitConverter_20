# Refactor Smell — 냄새 식별 (분석만)

`src/`·`tests/`를 읽고 **코드 스멜 목록**만 산출한다.  
파일을 **수정하지 않는다**. GREEN·RED 구현도 하지 않는다.

추가 인자 없이 `/refactor-smell` 만으로 동작한다.  
분석 대상은 **워크스페이스·채팅 TDD 단계**에서 자동 추출한다. **추가 입력·질문 금지.**

SSOT: `.cursorrules` · `docs/PRD.md`

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시:

```
Phase: REFACTOR | Mode: smell
```

이어서 한국어로 진행한다.

---

## SSOT (읽기 전용)

| 우선순위 | 문서 | 용도 |
|----------|------|------|
| 1 | `src/validate_lines.py` | 스멜 후보 |
| 2 | `tests/test_validate_lines.py` | 테스트 중복·헬퍼 |
| 3 | `.cursorrules` | API·4단위·TDD 불변 |
| 4 | `docs/PRD.md` | FR·상수 SSOT |

---

## 수정 범위

| 허용 | 금지 |
|------|------|
| 채팅 **스멜 표** 출력 | `src/`·`tests/` **수정** |
| SSOT 읽기 | `/refactor-safe` 적용 |
| | RED / GREEN |
| | 브랜치·commit |

---

## 스멜 체크리스트 (UnitConverter)

| ID | 스멜 | 탐지 힌트 |
|----|------|-----------|
| S01 | Magic Number | `3.28084`, `0.4572` 등 PRD 상수 리터럴 반복 |
| S02 | Duplicated Logic | meter 환산·단위별 나눗셈 복붙 |
| S03 | Long Function | `validate_lines` 검증+변환 다중 책임 |
| S04 | Dead Code | 미사용 분기·변수 |
| S05 | 테스트 중복 | 동일 `grid` Arrange 반복 |
| S06 | 불명확 이름 | `x`, `tmp`, `data` |
| S07 | API 불일치 | Harness `failed_lines` vs PRD `failed_fields` 혼용 |

해당 없으면 “없음”.

---

## 출력 형식 (필수)

```markdown
Phase: REFACTOR | Mode: smell

## 스멜 목록
| ID | 위치 | 스멜 | 설명 | 심각도 | 권장 조치 |
| … | … | … | … | H/M/L | … |

## 불변 계약 (리팩터 시 유지)
- `validate_lines(grid) -> {status, failed_lines}`
- PRD golden·status 정책 (테스트 고정값)

## 권장 순서
1. …

/refactor-safe 로 넘길 준비됐다
```

마지막 줄 **한 줄로 그대로** 출력.

---

## 워크플로

```
/green-minimal → /golden-master (선택) → /refactor-smell → /refactor-safe
```

스멜 단계는 **코드 변경 없음**.
