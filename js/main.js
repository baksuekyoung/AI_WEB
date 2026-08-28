/* ===== 네비게이션 토글 (모바일) ===== */
function toggleMenu() {
  const menu = document.getElementById('nav-menu');
  menu.classList.toggle('open');
}

// 메뉴 링크 클릭 시 닫기
document.querySelectorAll('.nav-menu a').forEach(link => {
  link.addEventListener('click', () => {
    document.getElementById('nav-menu').classList.remove('open');
  });
});

/* ===== FAQ 토글 ===== */
function toggleFaq(item) {
  item.classList.toggle('open');
}

/* ===== AI 추천 메인 함수 ===== */
async function getRecommendation() {
  const mood     = document.getElementById('mood').value;
  const category = document.getElementById('category').value;
  const people   = document.getElementById('people').value;
  const budget   = document.getElementById('budget').value;

  const errorMsg     = document.getElementById('error-msg');
  const resultBox    = document.getElementById('result-box');
  const loading      = document.getElementById('loading');
  const resultContent = document.getElementById('result-content');
  const btn          = document.getElementById('recommend-btn');

  // ── 1) 빈 입력 검사 ──────────────────────────────
  if (!mood || !category) {
    errorMsg.textContent = '⚠️ 기분과 음식 종류는 필수로 선택해주세요!';
    errorMsg.classList.remove('hidden');
    return;
  }

  // ── 2) UI 초기화 ──────────────────────────────────
  errorMsg.classList.add('hidden');
  resultBox.classList.remove('hidden');
  loading.style.display = 'block';
  resultContent.innerHTML = '';
  btn.disabled = true;
  btn.textContent = '⏳ 추천 중...';

  try {
    // ── 3) 백엔드 API 호출 ────────────────────────────
    const response = await fetch('/api/recommend', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mood, category, people, budget })
    });

    // ── 4) API 오류 처리 ──────────────────────────────
    if (!response.ok) {
      throw new Error(`서버 오류: ${response.status}`);
    }

    const data = await response.json();

    if (data.error) {
      throw new Error(data.error);
    }

    // ── 5) 결과 화면에 표시 ───────────────────────────
    const altTags = data.alternatives
      .split(',')
      .map(a => `<span class="alt-tag">${a.trim()}</span>`)
      .join('');

    resultContent.innerHTML = `
      <div class="menu-card">
        <p class="result-label">🎯 오늘의 추천 메뉴</p>
        <p class="menu-name">${data.menu}</p>
        <p class="menu-reason">💬 ${data.reason}</p>
        <p class="alt-title">다른 선택지도 있어요</p>
        <div class="alt-list">${altTags}</div>
        <button class="retry-btn" onclick="getRecommendation()">🔄 다시 추천받기</button>
      </div>
    `;

  } catch (error) {
    // ── 6) 오류 메시지 표시 ───────────────────────────
    resultContent.innerHTML = '';
    errorMsg.textContent = '😥 잠시 후 다시 시도해주세요. (' + error.message + ')';
    errorMsg.classList.remove('hidden');
    resultBox.classList.add('hidden');

  } finally {
    // ── 7) 버튼 복구 ──────────────────────────────────
    loading.style.display = 'none';
    btn.disabled = false;
    btn.textContent = '🎲 AI 추천 받기';
  }
}
