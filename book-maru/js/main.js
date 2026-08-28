// ===========================================
// 책마루 AI 사서 — 공통 스크립트
// ===========================================

// 모바일 메뉴 토글 (모든 페이지 공통)
const menuToggle = document.getElementById("menuToggle");
const navLinks = document.getElementById("navLinks");
if (menuToggle && navLinks) {
  menuToggle.addEventListener("click", () => {
    navLinks.classList.toggle("open");
  });
}

// ---------- AI 책 추천 기능 (recommend.html 전용) ----------
const form = document.getElementById("recommendForm");

if (form) {
  const submitBtn = document.getElementById("submitBtn");
  const formMsg = document.getElementById("formMsg");
  const resultCard = document.getElementById("resultCard");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const ageGroup = document.getElementById("ageGroup").value.trim();
    const interest = document.getElementById("interest").value.trim();
    const mood = document.getElementById("mood").value.trim();

    // 1) 빈 입력값 처리
    if (!ageGroup || !interest || !mood) {
      formMsg.textContent = "필수값을 입력하세요. 나이대, 관심 분야, 기분을 모두 선택/입력해주세요.";
      formMsg.classList.add("error");
      return;
    }

    formMsg.textContent = "";
    formMsg.classList.remove("error");

    // 2) 로딩 표시
    submitBtn.disabled = true;
    submitBtn.textContent = "AI 사서가 책을 고르는 중...";
    resultCard.innerHTML = `<p class="placeholder"><span class="spinner"></span>잠시만 기다려주세요. AI 사서가 책장을 살펴보고 있어요.</p>`;

    // 3) 타임아웃 처리 (12초)
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 12000);

    try {
      const res = await fetch("/api/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ageGroup, interest, mood }),
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!res.ok) {
        throw new Error("API_ERROR");
      }

      const data = await res.json();
      renderBooks(data.books);
    } catch (err) {
      if (err.name === "AbortError") {
        resultCard.innerHTML = `<p class="placeholder">응답이 지연되고 있어요. 잠시 후 다시 시도해주세요.</p>`;
      } else {
        resultCard.innerHTML = `<p class="placeholder">잠시 후 다시 시도해주세요. 문제가 계속되면 도서관 데스크로 문의해주세요.</p>`;
      }
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = "책 추천받기";
    }
  });
}

function renderBooks(books) {
  const resultCard = document.getElementById("resultCard");
  if (!books || !books.length) {
    resultCard.innerHTML = `<p class="placeholder">추천 결과를 불러오지 못했어요. 잠시 후 다시 시도해주세요.</p>`;
    return;
  }

  resultCard.innerHTML = books
    .map(
      (b) => `
      <div class="book-item">
        <h4>${escapeHtml(b.title)}${b.author ? " · " + escapeHtml(b.author) : ""}</h4>
        <p>${escapeHtml(b.reason)}</p>
      </div>
    `
    )
    .join("");
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str ?? "";
  return div.innerHTML;
}
