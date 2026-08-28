# 책마루 AI 사서

## 소개
동네 작은도서관 "책마루"를 소개하고, 방문자가 나이대·관심 분야·오늘의 기분을 입력하면
AI 사서가 책 3권을 이유와 함께 추천해주는 웹 서비스입니다.
마을돌봄사업과 연계된 돌봄 프로그램 소개 페이지도 함께 제공합니다.

## 페이지 구성
- `index.html` — 도서관 소개 (운영시간·위치·이용 대상)
- `recommend.html` — AI 책 추천 (입력 폼 + 결과 표시)
- `care.html` — 마을돌봄 프로그램 소개 및 문의(FAQ 포함)

## 기술 스택
- 프론트엔드: HTML / CSS / JavaScript (프레임워크 미사용)
- 백엔드: Vercel Serverless Functions (Python)
- AI: Anthropic Claude API (`claude-sonnet-4-6`)

## 배포 URL
(Vercel 배포 완료 후 이 줄에 실제 주소를 적어주세요. 예: https://book-maru.vercel.app)

## 실행 방법 (로컬)
1. `npm install -g vercel`
2. 프로젝트 폴더에서 `vercel dev` 실행
3. 터미널에 나오는 주소(예: http://localhost:3000)로 접속

## 환경 변수 설정
- 이름: `ANTHROPIC_API_KEY`
- 값: Anthropic API 키
- 설정 위치: Vercel 프로젝트 → Settings → Environment Variables
- 환경 변수를 추가/변경한 후에는 반드시 **Redeploy**해야 적용됩니다.
- API 키는 절대 코드나 스크린샷에 노출하지 않습니다.

## AI 기능 입력/출력/실패 처리
- 입력: 나이대(선택), 관심 분야(텍스트), 오늘의 기분(선택)
- 출력: 추천 도서 3권 (제목, 저자, 추천 이유)
- 실패 처리
  - 빈 입력값 → "필수값을 입력하세요" 안내
  - API 오류(4xx/5xx) → "잠시 후 다시 시도해주세요" 안내
  - 응답 지연(12초 초과) → "응답이 지연되고 있어요" 안내
