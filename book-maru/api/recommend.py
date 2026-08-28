import json
import os
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler

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

            prompt = f"""당신은 동네 작은도서관의 다정한 AI 사서입니다.
아래 방문자 정보를 참고해서 책 3권을 추천해주세요.

- 나이대: {age_group}
- 관심 분야: {interest}
- 오늘의 기분: {mood}

반드시 아래 JSON 형식으로만 답하세요. 다른 설명이나 마크다운 태그는 절대로 추가하지 마세요.
{{
  "books": [
    {{"title": "책 제목", "author": "저자", "reason": "이 책을 추천하는 이유 (2문장 이내, 한국어)"}},
    {{"title": "책 제목", "author": "저자", "reason": "이 책을 추천하는 이유 (2문장 이내, 한국어)"}},
    {{"title": "책 제목", "author": "저자", "reason": "이 책을 추천하는 이유 (2문장 이내, 한국어)"}}
  ]
}}"""

            # Gemini REST API 직접 호출
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={api_key}"
            
            req_data = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }],
                "generationConfig": {
                    "responseMimeType": "application/json"
                }
            }
            
            headers = {"Content-Type": "application/json"}
            req = urllib.request.Request(
                url, 
                data=json.dumps(req_data).encode("utf-8"), 
                headers=headers, 
                method="POST"
            )

            with urllib.request.urlopen(req) as response:
                res_body = response.read().decode("utf-8")
                res_json = json.loads(res_body)

            # Gemini 응답 데이터 추출
            raw_text = res_json["candidates"][0]["content"]["parts"][0]["text"].strip()

            # 마크다운 렌더링 문구 제거
            if raw_text.startswith("```"):
                lines = raw_text.splitlines()
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].startswith("```"):
                    lines = lines[:-1]
                raw_text = "\n".join(lines).strip()

            result = json.loads(raw_text)
            self._send_json(200, result)

        except urllib.error.HTTPError as e:
            err_msg = e.read().decode("utf-8")
            self._send_json(500, {"error": f"Gemini API 오류: {err_msg}"})
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