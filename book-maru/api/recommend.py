import json
import os
from http.server import BaseHTTPRequestHandler

from google import genai
from google.genai import types

# 안정적인 Gemini 2.5 Flash 모델 지정
MODEL_NAME = "gemini-2.5-flash"


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(content_length) if content_length else b"{}"
            payload = json.loads(raw_body or b"{}")

            age_group = (payload.get("ageGroup") or "").strip()
            interest = (payload.get("interest") or "").strip()
            mood = (payload.get("mood") or "").strip()

            if not age_group or not interest or not mood:
                self._send_json(
                    400,
                    {"error": "필수값을 입력하세요. 나이대, 관심 분야, 기분을 모두 입력해주세요."},
                )
                return

            api_key = os.environ.get("GEMINI_API_KEY")
            if not api_key:
                self._send_json(500, {"error": "서버에 API 키가 설정되어 있지 않습니다."})
                return

            client = genai.Client(api_key=api_key)

            prompt = f"""당신은 동네 작은도서관의 다정한 AI 사서입니다.
아래 방문자 정보를 참고해서 책 3권을 추천해주세요.

- 나이대: {age_group}
- 관심 분야: {interest}
- 오늘의 기분: {mood}

반드시 아래 JSON 형식으로만 답하세요. 다른 설명은 절대 추가하지 마세요.
{{
  "books": [
    {{"title": "책 제목", "author": "저자", "reason": "이 책을 추천하는 이유 (2문장 이내, 한국어)"}},
    {{"title": "책 제목", "author": "저자", "reason": "이 책을 추천하는 이유 (2문장 이내, 한국어)"}},
    {{"title": "책 제목", "author": "저자", "reason": "이 책을 추천하는 이유 (2문장 이내, 한국어)"}}
  ]
}}"""

            # 자동 함수 호출 옵션을 끄고 순수 텍스트/JSON 생성 모드로 실행
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    tools=[],  # AFC 경고 및 오류 방지
                ),
            )

            raw_text = (response.text or "").strip()
            
            # JSON 마크다운 태그 제거 처리
            if raw_text.startswith("```"):
                lines = raw_text.splitlines()
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].startswith("```"):
                    lines = lines[:-1]
                raw_text = "\n".join(lines).strip()

            result = json.loads(raw_text)
            self._send_json(200, result)

        except json.JSONDecodeError:
            self._send_json(502, {"error": "AI 응답을 해석하지 못했습니다. 잠시 후 다시 시도해주세요."})
        except Exception as e:
            self._send_json(500, {"error": f"서버 오류: {str(e)}"})

    def _send_json(self, status_code, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)