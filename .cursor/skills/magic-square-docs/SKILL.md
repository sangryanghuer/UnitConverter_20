---
name: magic-square-docs
description: >-
  UnitConverter_20 세션 문서화. Report/NN.REPORT.md,
  Prompting/NN.Export-Transcript.md, ARRR 체크리스트 작성.
  /export-session 또는 세션 마감·실습 기록 시 적용.
---

# UnitConverter_20 Docs Skill

세션 산출물을 **번호 규칙**에 맞게 기록한다.

SSOT: `.cursor/commands/export-session.md` · `.cursorrules` · `docs/PRD.md`

## 생성 대상

| 종류 | 경로 | 템플릿 |
|------|------|--------|
| 보고서 | `Report/NN.REPORT.md` | `templates/report-template.md` |
| Transcript | `Prompting/NN.Export-Transcript.md` | `templates/transcript-template.md` |
| 체크리스트 | `docs/checklists/NN.ARRR-checklist.md` | `templates/checklist-template.md` |

`NN` = 2자리 (`01`, `02`, …). 기존 최대 번호 + 1.

## 번호 규칙

1. `Report/`, `Prompting/`, `docs/checklists/`에서 기존 `NN.*` 확인
2. 가장 큰 번호 + 1
3. 기존 파일 **덮어쓰기 금지**

## /export-session 절차

1. 다음 `NN` 결정
2. `Report/NN.REPORT.md` + `Prompting/NN.Export-Transcript.md` **둘 다** 생성
3. 경로·번호·한 줄 요약 보고

추가 입력·질문 금지 — 채팅·워크스페이스에서 자동 추출.

## 보고서 필수 섹션

- 제목: `# UnitConverter_20 — {세션 주제}`
- 메타 표: 프로젝트, 단계(ARRR), 보고서 생성일, 목적
- 1. 요약 / 2. 핵심 결정·산출물 / 3. 다음 단계
- Transcript 링크: `Prompting/NN.Export-Transcript.md`
- 푸터: `*본 문서는 Report/NN.REPORT.md — …입니다.*`

## Transcript 필수

- `_Exported on {날짜} from Cursor_`
- **User** / **Cursor** 턴 전문 (요약 아님)
- 생성·변경 파일 표
- 푸터: `*본 문서는 Prompting/NN.Export-Transcript.md — …입니다.*`

## ARRR 체크리스트

실습 마감·handoff 시 `docs/checklists/NN.ARRR-checklist.md` (선택).

템플릿: `templates/checklist-template.md`

## 프로젝트명

- 문서 제목·메타: **UnitConverter_20**
- SSOT: `docs/PRD.md`

## 금지

- 번호 없는 `REPORT.md` 단독 저장
- 보고서만·Transcript만 생성
- 구현·pytest·commit (문서 Skill 범위 밖 — 사용자 요청 시만)

## 관련 Skill

TDD: `.cursor/skills/magic-square-tdd/SKILL.md`
