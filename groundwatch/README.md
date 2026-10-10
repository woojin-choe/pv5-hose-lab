# PV5 GroundWatch — 공모전 제안서

같은 도로를 반복 측정해 지하 공동의 변화를 찾는 PV5 지하안전 순찰차. 팀 「한 명이라도 살릴 수 있다면」.

## 결과물

| 파일 | 내용 |
|---|---|
| `PV5_GroundWatch.pptx` | 편집 가능한 27장 제안서, 장마다 발표자 노트와 출처 포함 |
| `PV5_GroundWatch.pdf` | 제출·공유용 PDF (PowerPoint로 내보냄, 글꼴 포함) |
| `renders/slide-01.png` … `slide-27.png` | 27장 전체 렌더링 이미지 |
| `images/` | 슬라이드에 쓴 일러스트·목업·아이콘 원본 PNG |
| `speaker-notes.md` | 발표자 노트 전체(출처 링크 포함) |
| `fonts/` | Pretendard(SIL OFL 1.1). PPTX를 편집할 PC에 설치하면 렌더와 같은 모양으로 보입니다 |

## 다시 만들기

```bash
cd groundwatch/build
npm install          # pptxgenjs, sharp, react, react-dom, react-icons
./build.sh           # 에셋 → PPTX → PowerPoint PDF → 슬라이드 PNG
./build.sh --skip-assets   # 에셋을 다시 그리지 않을 때
```

- `assets.js`: 모든 일러스트를 SVG로 그려 `images/`에 저장합니다. 실제 사진·로고는 쓰지 않습니다.
- `deck.js`: 27장 구성과 발표자 노트를 만듭니다.
- PDF 변환에 Microsoft PowerPoint(macOS)와 PyMuPDF가 필요합니다.

## 표기 규칙

- `[가설]` 사업·운영 가정, 인터뷰와 파일럿으로 검증
- `[실증 필요]` 차량·장비 시험으로 확인
- `[추가 확인 필요]` 공식 자료 확인 전
- `[예시]` 화면·수치 설명용

작성 기준일 2026.10.10.
