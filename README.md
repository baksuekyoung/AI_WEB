# 🍽️ 오늘 뭐 먹지? (WhatEat)

> AI가 오늘 기분에 딱 맞는 점심 메뉴를 추천해드립니다!

---

## 🔗 배포 URL
https://whateat.vercel.app

---

## 🛠️ 기술 스택

| 구분 | 기술 |
|------|------|
| Frontend | HTML, CSS, JavaScript (Vanilla) |
| Backend | Python (Vercel Serverless Functions) |
| AI | OpenAI GPT-4o-mini |
| 배포 | Vercel + GitHub 연동 |

---

## 📁 프로젝트 구조

```
whateat/
├── index.html          # 메인 페이지 (전체 섹션 포함)
├── css/
│   └── style.css       # 스타일 (반응형 포함)
├── js/
│   └── main.js         # 인터랙션 & fetch 호출
├── api/
│   └── recommend.py    # Vercel Serverless Function
├── requirements.txt    # Python 패키지
├── vercel.json         # Vercel 배포 설정
└── README.md
```

---

## ⚙️ 환경 변수 설정

Vercel 대시보드에서 아래 환경 변수를 추가하세요:

```
OPENAI_API_KEY = sk-xxxxxxxxxxxxxxxx
```

**설정 경로:**
Vercel 대시보드 → 프로젝트 선택 → Settings → Environment Variables

> ⚠️ API 키는 절대 코드에 직접 넣지 마세요!

---

## 🚀 로컬 실행 방법

```bash
# 1. Vercel CLI 설치
npm install -g vercel

# 2. 로컬 환경 변수 파일 생성
echo "OPENAI_API_KEY=sk-your-key-here" > .env.local

# 3. 로컬 서버 실행
vercel dev

# 4. 브라우저에서 접속
# http://localhost:3000
```

---

## 📦 배포 방법

```bash
# 1. GitHub에 push
git add .
git commit -m "deploy"
git push origin main

# 2. Vercel이 자동으로 감지하여 재배포
```

---

## 🧪 AI 기능 테스트 케이스

| 테스트 | 입력 | 기대 결과 |
|--------|------|-----------|
| ✅ 정상 | 피곤함 / 한식 / 혼밥 | 추천 메뉴 + 이유 표시 |
| ⚠️ 빈 입력 | 기분 미선택 | 경고 메시지 표시 |
| 🔄 로딩 | 정상 입력 후 대기 | 스피너 + 안내 문구 |
| ❌ API 오류 | 키 오류 등 | 오류 안내 메시지 |

---

## 📄 서비스 기획서

- **서비스명:** 오늘 뭐 먹지? (WhatEat)
- **타겟:** 점심 메뉴 고민하는 직장인 / 대학생
- **핵심 기능:** 기분·음식종류·인원수·예산 입력 → AI 메뉴 추천
- **페이지 구성:** Hero / AI 추천 / 서비스 소개 / FAQ
