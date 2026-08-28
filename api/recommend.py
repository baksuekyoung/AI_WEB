import os
import json
from http.server import BaseHTTPRequestHandler
from openai import OpenAI


class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        try:
            # ── 1) 요청 바디 읽기 ──────────────────────────
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body)

            mood     = data.get('mood', '')
            category = data.get('category', '')
            people   = data.get('people', '혼밥')
            budget   = data.get('budget', '상관없음')

            # ── 2) 필수값 검사 ─────────────────────────────
            if not mood or not category:
                self._send_json(400, {'error': '기분과 음식 종류를 선택해주세요.'})
                return

            # ── 3) OpenAI 클라이언트 생성 ──────────────────
            api_key = os.environ.get('OPENAI_API_KEY')
            if not api_key:
                self._send_json(500, {'error': 'API 키가 설정되지 않았습니다.'})
                return

            client = OpenAI(api_key=api_key)

            # ── 4) 프롬프트 작성 ───────────────────────────
            prompt = f"""
사용자 상황:
- 오늘 기분: {mood}
- 선호 음식 종류: {category}
- 인원수: {people}
- 예산: {budget}

위 상황에 딱 맞는 점심 메뉴 1개를 추천해주세요.
반드시 아래 JSON 형식으로만 답하세요. 다른 말은 하지 마세요:
{{
  "menu": "추천 메뉴 이름 (예: 김치찌개)",
  "reason": "추천 이유를 한 문장으로 (예: 피곤할 때는 얼큰한 국물이 최고예요!)",
  "alternatives": "대안 메뉴1, 대안 메뉴2"
}}
"""

            # ── 5) OpenAI API 호출 ─────────────────────────
            response = client.chat.completions.create(
                model='gpt-4o-mini',
                messages=[
                    {
                        'role': 'system',
                        'content': (
                            '당신은 점심 메뉴 추천 전문가입니다. '
                            '항상 JSON 형식으로만 답하세요.'
                        )
                    },
                    {'role': 'user', 'content': prompt}
                ],
                max_tokens=300,
                temperature=0.8
            )

            # ── 6) 응답 파싱 ───────────────────────────────
            result_text = response.choices[0].message.content.strip()

            # 코드블록 제거 (```json ... ``` 형태 대응)
            if result_text.startswith('```'):
                result_text = result_text.split('```')[1]
                if result_text.startswith('json'):
                    result_text = result_text[4:]

            result = json.loads(result_text)
            self._send_json(200, result)

        except json.JSONDecodeError:
            self._send_json(500, {'error': 'AI 응답을 파싱하지 못했습니다. 다시 시도해주세요.'})
        except Exception as e:
            self._send_json(500, {'error': str(e)})

    def do_OPTIONS(self):
        # CORS preflight 대응
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()

    def _send_json(self, status_code, data):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status_code)
        self._set_cors_headers()
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _set_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
