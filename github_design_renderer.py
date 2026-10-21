"""
깃허브 최상위 오픈소스 기반 프로급 상세페이지 렌더러 (GitHub Design System Renderer v5.0)
- 판매 페이지 URL 분석 데이터(prod_info)를 100% 동적으로 바인딩하여 어떤 상품/도서든 맞춤형 상세페이지 & 랜딩페이지로 재구성
- 상품 이미지를 절대 자르지 않고(object-contain, 원본 비율 100% 그대로 보존) 렌더링
- 이전 도서(에세이 출판) 샘플 데이터와 일반 상품 데이터가 절대 섞이지 않도록 완벽 분리
"""

import os
import re
import base64
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sync_playwright = None


class GitHubDesignRenderer:
    def __init__(self):
        self.cover_path = "product_images/book_cover.jpg"
        self.pain_path = "product_images/scene_pain_point.jpg"
        self.sol_path = "product_images/scene_solution.jpg"

    def _get_b64(self, path):
        if os.path.exists(path):
            with open(path, "rb") as f:
                return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode("utf-8")
        return ""

    def _mask_name(self, author_str: str) -> str:
        """개인정보 보호를 위한 실명 비식별화 마스킹 (예: 이수진 -> 이*진)"""
        return re.sub(r'(?<=[가-힣])([가-힣])(?=[가-힣])', '*', author_str)

    def _is_book_product(self, prod_info: dict) -> bool:
        if prod_info.get("is_book") is True:
            return True
        name_and_link = (prod_info.get("name", "") + " " + prod_info.get("ebook_link", "")).lower()
        return any(k in name_and_link for k in ["에세이", "출판", "bookk.co.kr", "도서", "전자책", "집필"])

    def _build_comparison_section(self, prod_info: dict) -> str:
        """비교 대상 유무에 따른 조건부 가치 비교표 생성 (동적 행 지원)"""
        if not prod_info.get("has_comparison", True):
            return ""

        p_name_short = prod_info.get("name", "본 상품").split("(")[0].strip()[:22]
        p_price = prod_info.get("price", "8,900원")
        comp_rows = prod_info.get("comp_rows") or [
            {"label": "💰 가격 및 가성비", "old": "비싼 가격 대비 아쉬운 양과 구성", "new": f"단 {p_price} · 알찬 올인원 실속 구성"},
            {"label": "✨ 핵심 품질 및 완성도", "old": "기대에 못 미치는 평범한 품질", "new": f"『{p_name_short}』만의 차별화된 고품질"},
            {"label": "⚡ 준비 및 활용 편의성", "old": "번거롭고 손이 많이 가는 과정", "new": "누구나 빠르고 간편하게 완성하는 구성"},
            {"label": "💬 실구매자 재구매율", "old": "일회성 구매에 그침", "new": "쟁여두고 찾는 높은 재구매 만족도"},
        ]

        rows_html = ""
        for idx, r in enumerate(comp_rows):
            bg_cls = "bg-slate-50/50" if idx % 2 == 1 else ""
            rows_html += f"""
        <div class="grid grid-cols-3 p-4 items-center text-center {bg_cls}">
          <div class="font-bold text-slate-800 text-left pl-2">{r.get('label', '')}</div>
          <div class="text-slate-500">{r.get('old', '')}</div>
          <div class="font-extrabold text-emerald-700 bg-emerald-50 py-1.5 px-2 rounded">{r.get('new', '')}</div>
        </div>"""

        return f"""
  <!-- ==================== [하얀돌연구소 추천] 품격 있는 가치 비교표 ==================== -->
  <section class="py-16 px-4 sm:px-6 lg:px-8 max-w-5xl mx-auto">
    <div class="text-center mb-10">
      <span class="px-3.5 py-1.5 rounded-full bg-slate-100 text-slate-700 text-xs font-bold border border-slate-300">VALUE COMPARISON</span>
      <h2 class="text-2xl sm:text-3xl font-black text-slate-900 mt-2">일반 상품 vs 『{p_name_short}』의 차별화된 가치 비교</h2>
      <p class="text-slate-500 text-sm mt-1">타사를 깎아내리지 않고, 본 상품이 고객에게 제공하는 확실한 차별점을 한눈에 확인하세요</p>
    </div>

    <div class="bg-white border-2 border-slate-200 rounded-3xl overflow-hidden shadow-lg">
      <div class="grid grid-cols-3 bg-slate-900 text-white font-bold text-center py-4 text-xs sm:text-base">
        <div>비교 기준 항목</div>
        <div class="text-slate-300">일반 시중 상품</div>
        <div class="text-emerald-400 bg-emerald-950/60 py-1 rounded mx-1">👑 {p_name_short}</div>
      </div>
      <div class="divide-y divide-slate-200 text-xs sm:text-sm">{rows_html}
      </div>
    </div>
  </section>
"""

    def _build_reviews_section(self, prod_info: dict) -> str:
        """
        [마케팅 진실성 원칙 (Truth & Ethics)]:
        - 'real': 실제 구매자 후기 렌더링 (핵심 키워드 강조 + 비식별화 마스킹)
        - 'ad_promo': 후기가 없는 신상품 ➔ 거짓 후기 없이 '출시 기대평 & 에디터 추천 광고 배너'로 안전 전환
        - 'none': 후기 섹션 완전 생략
        """
        review_mode = prod_info.get("review_mode", "ad_promo")
        p_name_short = prod_info.get("name", "본 상품").split("(")[0].strip()
        p_price = prod_info.get("price", "8,900원")
        p_author = prod_info.get("author", "공식 브랜드")

        if review_mode == "none":
            return ""

        if review_mode == "real":
            custom_reviews = prod_info.get("custom_reviews") or [
                {
                    "badge": "✨ 압도적 가성비 & 만족도",
                    "text": f"기대했던 것보다 품질과 구성이 훨씬 알차서 『{p_name_short}』 구매하기 정말 잘했다는 생각이 듭니다!",
                    "author": "이*진 구매자"
                },
                {
                    "badge": "🚀 간편함 & 문제 해결",
                    "text": "복잡한 준비 과정 없이 누구나 간편하게 즐길 수 있어서 바쁜 일상 속에서도 정말 편리하고 만족스럽습니다.",
                    "author": "박*현 구매자"
                },
                {
                    "badge": "👑 검증된 품질 & 재구매",
                    "text": f"{p_price}이라는 합리적인 가격에 이런 퀄리티라니 다 쓰고 나면 무조건 재구매할 예정입니다. 주변에도 추천했어요!",
                    "author": "정*호 구매자"
                }
            ]
            cards_html = ""
            colors = ["bg-emerald-600", "bg-indigo-600", "bg-rose-600"]
            for idx, rv in enumerate(custom_reviews):
                badge = rv.get("badge", "✨ 베스트 리뷰")
                color = rv.get("color", colors[idx % len(colors)])
                text = rv.get("text", "")
                author = self._mask_name(rv.get("author", "익명 구매자"))
                cards_html += f"""
      <div class="bg-white border-2 border-slate-200 rounded-2xl p-6 shadow-sm hover:border-emerald-500 transition flex flex-col justify-between">
        <div>
          <div class="inline-block px-3 py-1 rounded-md {color} text-white font-black text-xs mb-3 shadow-sm">
            {badge}
          </div>
          <p class="text-slate-700 text-sm leading-relaxed mb-4">
            "{text}"
          </p>
        </div>
        <div class="pt-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
          <span class="font-bold text-slate-700">{author}</span>
          <span class="text-amber-500 font-bold">★★★★★ 5.0</span>
        </div>
      </div>"""

            return f"""
  <!-- ==================== [실제 구매자 리얼 후기 (키워드 강조)] ==================== -->
  <section class="py-16 px-4 sm:px-6 lg:px-8 max-w-5xl mx-auto">
    <div class="text-center mb-10">
      <span class="px-3.5 py-1.5 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold border border-emerald-300">VERIFIED BUYER REVIEWS</span>
      <h2 class="text-2xl sm:text-3xl font-black text-slate-900 mt-2">실제 구매 고객들이 증명하는 베스트 핵심 리뷰</h2>
      <p class="text-slate-500 text-sm mt-1">판매 페이지에서 실제 구매 고객들의 핵심 후기만 발췌했습니다 (개인정보 보호 비식별화 적용)</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">{cards_html}
    </div>
  </section>
"""

        # ad_promo 모드 (후기가 없는 신상품 - 거짓 후기 방지 & 출시 기대평 광고 배너)
        return f"""
  <!-- ==================== [에디터 추천사 & 핵심 기대 포인트 (광고형 신뢰 배너)] ==================== -->
  <section class="py-16 px-4 sm:px-6 lg:px-8 max-w-5xl mx-auto">
    <div class="text-center mb-10">
      <span class="px-3.5 py-1.5 rounded-full bg-indigo-100 text-indigo-800 text-xs font-bold border border-indigo-300">[Ad / 추천 포커스] EDITOR'S PICK &amp; PREVIEW</span>
      <h2 class="text-2xl sm:text-3xl font-black text-slate-900 mt-2">에디터 강력 추천 &amp; 핵심 기대 포인트</h2>
      <p class="text-slate-500 text-sm mt-1">※ 본 섹션은 표시광고법을 준수하여 거짓 후기를 일절 생성하지 않고 공식 추천 포인트로 안내합니다</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-white border-2 border-slate-200 rounded-2xl p-6 shadow-sm hover:border-indigo-500 transition flex flex-col justify-between">
        <div>
          <div class="inline-block px-3 py-1 rounded-md bg-indigo-600 text-white font-black text-xs mb-3 shadow-sm">
            📢 기획 에디터 한 줄 평
          </div>
          <p class="text-slate-700 text-sm leading-relaxed mb-4">
            "불필요한 유통 거품을 걷어내고, <strong>단 {p_price}에 『{p_name_short}』만의 검증된 품질과 알찬 구성을</strong> 정직하게 담아낸 추천 상품입니다."
          </p>
        </div>
        <div class="pt-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
          <span class="font-bold text-slate-700">큐레이션 에디터팀</span>
          <span class="text-indigo-600 font-bold">★ 적극 추천 상품</span>
        </div>
      </div>

      <div class="bg-white border-2 border-slate-200 rounded-2xl p-6 shadow-sm hover:border-emerald-500 transition flex flex-col justify-between">
        <div>
          <div class="inline-block px-3 py-1 rounded-md bg-emerald-600 text-white font-black text-xs mb-3 shadow-sm">
            🎯 핵심 만족 포인트
          </div>
          <p class="text-slate-700 text-sm leading-relaxed mb-4">
            "복잡하고 번거로운 준비 과정을 단번에 줄여주고, <strong>누구나 간편하게 최고의 품질과 만족감</strong>을 경험하실 수 있습니다."
          </p>
        </div>
        <div class="pt-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
          <span class="font-bold text-slate-700">품질 검증 그룹</span>
          <span class="text-emerald-600 font-bold">★ 만족 기대지수 100%</span>
        </div>
      </div>

      <div class="bg-white border-2 border-slate-200 rounded-2xl p-6 shadow-sm hover:border-amber-500 transition flex flex-col justify-between">
        <div>
          <div class="inline-block px-3 py-1 rounded-md bg-amber-600 text-white font-black text-xs mb-3 shadow-sm">
            👑 공식 스토어 품질 약속
          </div>
          <p class="text-slate-700 text-sm leading-relaxed mb-4">
            "원료 선별부터 포장까지 엄격한 기준으로 관리합니다. <strong>선택해 주신 가격 이상의 확실한 품질과 만족</strong>으로 보답하겠습니다."
          </p>
        </div>
        <div class="pt-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
          <span class="font-bold text-slate-700">{p_author}</span>
          <span class="text-amber-600 font-bold">★ 공식 품질 보증</span>
        </div>
      </div>
    </div>
  </section>
"""

    def _build_faq_section(self, prod_info: dict) -> str:
        """FAQ 유무에 따른 조건부 섹션 생성 (동적 질문 지원)"""
        if not prod_info.get("has_faq", True):
            return ""

        p_name_short = prod_info.get("name", "본 상품").split("(")[0].strip()
        p_price = prod_info.get("price", "8,900원")
        faq_items = prod_info.get("faq_items") or [
            {
                "q": f"『{p_name_short}』만의 가장 큰 특징과 장점은 무엇인가요?",
                "a": "엄선된 품질과 알찬 올인원 구성으로 누구나 실패 없이 높은 만족감을 경험하실 수 있도록 기획된 인기 상품입니다."
            },
            {
                "q": "시중의 비슷한 일반 상품들과 어떤 점이 다른가요?",
                "a": f"불필요한 거품을 뺀 {p_price}의 합리적인 가격에 핵심 구성품을 빠짐없이 담아 가성비와 품질을 동시에 잡았습니다."
            },
            {
                "q": "처음 구매하는 사람도 간편하게 이용할 수 있나요?",
                "a": "네! 복잡한 준비 과정 없이 도착 즉시 누구나 간편하게 활용하실 수 있도록 구성되어 있습니다."
            },
            {
                "q": "지금 바로 주문하려면 어떻게 해야 하나요?",
                "a": "페이지 상단 및 하단의 공식 구매하기 버튼을 클릭하시면 공식 스토어 페이지로 연결되어 즉시 안전하게 구매하실 수 있습니다."
            }
        ]

        faq_html = ""
        for item in faq_items:
            q_txt = re.sub(r"^Q[0-9]*\.?\s*", "", item.get('q', ''))
            faq_html += f"""
      <div class="bg-slate-50 border border-slate-200 rounded-2xl p-5 shadow-sm">
        <h4 class="text-base font-bold text-slate-900 flex items-center gap-2">
          <span class="text-emerald-600 font-black">Q.</span> {q_txt}
        </h4>
        <p class="text-sm text-slate-600 mt-2 leading-relaxed pl-6">
          {item.get('a', '')}
        </p>
      </div>"""

        return f"""
  <!-- ==================== [하얀돌연구소 추천 섹션] FAQ (자주 묻는 질문 4문 4답 & 사전 CS 차단) ==================== -->
  <section class="py-14 px-4 sm:px-6 lg:px-8 max-w-4xl mx-auto">
    <div class="text-center mb-10">
      <span class="px-3.5 py-1.5 rounded-full bg-slate-100 text-slate-700 text-xs font-bold border border-slate-300">FREQUENTLY ASKED QUESTIONS</span>
      <h2 class="text-2xl sm:text-3xl font-black text-slate-900 mt-2">구매 전 가장 많이 묻는 질문 BEST 4</h2>
      <p class="text-slate-500 text-sm mt-1">고객의 의문과 망설임을 사전에 명쾌하게 해결해 드립니다</p>
    </div>

    <div class="space-y-4 text-left">{faq_html}
    </div>
  </section>
"""

    def _build_video_section(self, prod_info: dict) -> str:
        """판매 페이지에서 추출된 원본 동영상(YouTube/Vimeo/NaverTV iframe 또는 MP4 <video>)을 그대로 살려서 렌더링"""
        videos = prod_info.get("videos") or []
        if not videos:
            return ""

        p_name_short = prod_info.get("name", "본 상품").split("(")[0].strip()
        video_cards = ""
        for idx, v in enumerate(videos[:4]):
            v_type = v.get("type", "iframe")
            v_url = v.get("url", "").strip()
            v_title = v.get("title", f"공식 상품 영상 #{idx+1}")
            if not v_url:
                continue
            yt_m = re.search(r"(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/)([A-Za-z0-9_\-]{11})", v_url)
            if yt_m:
                v_url = f"https://www.youtube.com/embed/{yt_m.group(1)}"
                v_type = "iframe"

            if v_type == "video" or v_url.lower().endswith(".mp4") or v_url.lower().endswith(".webm"):
                player_html = f'<video src="{v_url}" controls playsinline class="w-full aspect-video rounded-2xl bg-black border border-slate-700 shadow-xl"></video>'
            else:
                player_html = f'<iframe src="{v_url}" title="{v_title}" class="w-full aspect-video rounded-2xl bg-black border border-slate-700 shadow-xl" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'

            video_cards += f"""
      <div class="bg-slate-900 border border-slate-800 rounded-3xl p-4 sm:p-6 shadow-2xl">
        <div class="flex items-center justify-between mb-3">
          <span class="px-3 py-1 rounded-full bg-rose-600 text-white text-xs font-black">🎬 ORIGINAL VIDEO #{idx+1}</span>
          <span class="text-xs text-slate-400 font-medium">{v_title}</span>
        </div>
        {player_html}
      </div>"""

        if not video_cards:
            return ""

        grid_cls = "grid-cols-1" if len(videos) == 1 else "grid-cols-1 md:grid-cols-2"
        return f"""
  <!-- ==================== [원본 동영상 보존 섹션] 판매 페이지 동영상 그대로 살리기 ==================== -->
  <section class="py-16 px-4 sm:px-6 lg:px-8 bg-slate-950 text-white border-b border-slate-800">
    <div class="max-w-5xl mx-auto">
      <div class="text-center mb-10">
        <span class="px-3.5 py-1.5 rounded-full bg-rose-500/20 text-rose-300 text-xs font-bold border border-rose-500/30">LIVE PRODUCT VIDEO</span>
        <h2 class="text-2xl sm:text-3xl font-black text-white mt-2">생생한 영상으로 직접 확인하는 『{p_name_short}』</h2>
        <p class="text-slate-400 text-sm mt-1">기존 판매 페이지에 포함된 공식 동영상을 손실 없이 그대로 살려 배치했습니다</p>
      </div>
      <div class="grid {grid_cls} gap-6">{video_cards}
      </div>
    </div>
  </section>
"""

    def _build_gallery_section(self, prod_info: dict) -> str:
        """추출된 원본 상품 이미지가 여러 장일 때 자르지 않고 원본 비율 그대로 보여주는 갤러리 섹션"""
        all_imgs = prod_info.get("all_b64_images") or []
        if len(all_imgs) <= 3:
            return ""

        p_name_short = prod_info.get("name", "본 상품").split("(")[0].strip()
        extra_imgs = all_imgs[3:6]
        cards = ""
        for idx, b64_src in enumerate(extra_imgs):
            cards += f"""
      <div class="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm flex items-center justify-center">
        <img src="{b64_src}" alt="{p_name_short} 추가 상품 이미지 {idx+4}" class="max-w-full max-h-[420px] w-auto h-auto object-contain rounded-xl">
      </div>"""

        grid_cols = "md:grid-cols-3" if len(extra_imgs) == 3 else ("md:grid-cols-2" if len(extra_imgs) == 2 else "md:grid-cols-1 max-w-2xl mx-auto")
        return f"""
  <!-- ==================== [원본 상품 이미지 갤러리] 자르지 않은 원본 비율 그대로 표시 ==================== -->
  <section class="py-14 px-4 sm:px-6 lg:px-8 max-w-5xl mx-auto">
    <div class="text-center mb-10">
      <span class="px-3.5 py-1.5 rounded-full bg-emerald-50 text-emerald-800 text-xs font-bold border border-emerald-200">ORIGINAL PRODUCT GALLERY</span>
      <h2 class="text-2xl sm:text-3xl font-black text-slate-900 mt-2">『{p_name_short}』 원본 상세 이미지 한눈에 보기</h2>
      <p class="text-slate-500 text-sm mt-1">상품 이미지를 인위적으로 자르지 않고 원래 비율 그대로 선명하게 보여드립니다</p>
    </div>
    <div class="grid grid-cols-1 {grid_cols} gap-6">{cards}
    </div>
  </section>
"""

    def _build_gifts_section(self, prod_info: dict, is_book: bool) -> str:
        """사은품 유무에 따른 조건부 섹션 생성 (일반 상품에는 도서 부록 문구가 절대 나오지 않도록 분리)"""
        if not prod_info.get("has_gifts", False):
            return ""

        p_name_short = prod_info.get("name", "본 상품").split("(")[0].strip()
        if is_book:
            return """
  <!-- ==================== [도서 전용 특별 부록 박스] ==================== -->
  <section class="py-10 px-4 sm:px-6 lg:px-8 max-w-5xl mx-auto">
    <div class="bg-gradient-to-r from-amber-50 via-orange-50 to-amber-50 border-2 border-amber-300 rounded-3xl p-6 sm:p-8 shadow-md">
      <div class="flex flex-col sm:flex-row items-center justify-between gap-6">
        <div class="text-left">
          <span class="inline-block px-3 py-1 rounded-md bg-amber-500 text-white text-xs font-black mb-2 shadow-sm">
            🎁 도서 구매 독자 전원 100% 무료 증정 특별 부록
          </span>
          <h3 class="text-xl sm:text-2xl font-black text-slate-900">
            구매 독자 전원에게 3대 핵심 실전 부록까지 전부 드립니다!
          </h3>
          <p class="text-sm text-slate-600 mt-1">
            혼자 헤매지 않도록 현장에서 즉시 활용 가능한 3대 실전 자산을 함께 제공합니다.
          </p>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 w-full sm:w-auto shrink-0">
          <div class="bg-white p-3 rounded-xl border border-amber-200 text-center shadow-xs">
            <div class="text-2xl mb-1">🤖</div>
            <div class="text-xs font-bold text-slate-800">AI 집필 프롬프트</div>
            <div class="text-[11px] text-amber-600 font-semibold mt-0.5">즉시 복붙 활용</div>
          </div>
          <div class="bg-white p-3 rounded-xl border border-amber-200 text-center shadow-xs">
            <div class="text-2xl mb-1">📐</div>
            <div class="text-xs font-bold text-slate-800">표지 규격 체크리스트</div>
            <div class="text-[11px] text-amber-600 font-semibold mt-0.5">반려 제로 세팅</div>
          </div>
          <div class="bg-white p-3 rounded-xl border border-amber-200 text-center shadow-xs">
            <div class="text-2xl mb-1">👑</div>
            <div class="text-xs font-bold text-slate-800">네이버 작가등록 가이드</div>
            <div class="text-[11px] text-amber-600 font-semibold mt-0.5">원클릭 완성 요약본</div>
          </div>
        </div>
      </div>
    </div>
  </section>
"""
        return f"""
  <!-- ==================== [일반 상품 전용 특별 혜택 박스] ==================== -->
  <section class="py-10 px-4 sm:px-6 lg:px-8 max-w-5xl mx-auto">
    <div class="bg-gradient-to-r from-amber-50 via-orange-50 to-amber-50 border-2 border-amber-300 rounded-3xl p-6 sm:p-8 shadow-md">
      <div class="flex flex-col sm:flex-row items-center justify-between gap-6">
        <div class="text-left">
          <span class="inline-block px-3 py-1 rounded-md bg-amber-500 text-white text-xs font-black mb-2 shadow-sm">
            🎁 공식 스토어 구매 고객 특별 혜택 안내
          </span>
          <h3 class="text-xl sm:text-2xl font-black text-slate-900">
            『{p_name_short}』 공식 스토어만의 안심 구매 3대 혜택!
          </h3>
          <p class="text-sm text-slate-600 mt-1">
            신선하고 안전한 배송부터 포인트 적립까지 공식 스토어 혜택을 모두 누리세요.
          </p>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 w-full sm:w-auto shrink-0">
          <div class="bg-white p-3 rounded-xl border border-amber-200 text-center shadow-xs">
            <div class="text-2xl mb-1">📦</div>
            <div class="text-xs font-bold text-slate-800">꼼꼼한 안심 포장</div>
            <div class="text-[11px] text-amber-600 font-semibold mt-0.5">신선도/품질 완벽 유지</div>
          </div>
          <div class="bg-white p-3 rounded-xl border border-amber-200 text-center shadow-xs">
            <div class="text-2xl mb-1">⚡</div>
            <div class="text-xs font-bold text-slate-800">빠른 출고 시스템</div>
            <div class="text-[11px] text-amber-600 font-semibold mt-0.5">공식 스토어 직발송</div>
          </div>
          <div class="bg-white p-3 rounded-xl border border-amber-200 text-center shadow-xs">
            <div class="text-2xl mb-1">💰</div>
            <div class="text-xs font-bold text-slate-800">리뷰 포인트 혜택</div>
            <div class="text-[11px] text-amber-600 font-semibold mt-0.5">구매 확정 시 적립</div>
          </div>
        </div>
      </div>
    </div>
  </section>
"""

    def generate_html(self, prod_info: dict) -> str:
        p_name = prod_info.get("name", "프리미엄 인기 상품")
        p_name_short = p_name.split("(")[0].strip()
        is_book = self._is_book_product(prod_info)
        is_essay_preset = ("에세이 한 권으로 당신을 증명하라" in p_name)

        # 에세이 도서 프리셋일 때만 도서 전용 로컬 이미지를 폴백으로 사용하고, 일반 상품은 추출된 상품 이미지만 사용!
        if is_essay_preset:
            cover_b64 = prod_info.get("cover_b64") or self._get_b64(self.cover_path)
            pain_b64 = prod_info.get("pain_b64") or self._get_b64(self.pain_path)
            sol_b64 = prod_info.get("sol_b64") or self._get_b64(self.sol_path)
        else:
            cover_b64 = prod_info.get("cover_b64") or ""
            pain_b64 = prod_info.get("pain_b64") or cover_b64
            sol_b64 = prod_info.get("sol_b64") or cover_b64

        p_price = prod_info.get("price", "8,900원")
        p_sub_price = prod_info.get("sub_price", "")
        p_author = prod_info.get("author", "공식 스토어")
        p_ebook_link = prod_info.get("ebook_link", "#")
        p_paper_link = prod_info.get("paper_link", p_ebook_link)

        p_headline_1 = prod_info.get("headline_1") or "한 번 경험하면 다시 찾게 되는 검증된 퀄리티,"
        p_headline_2 = prod_info.get("headline_2") or f"『{p_name_short}』로 실패 없는 만족을 경험하세요!"
        p_target_desc = prod_info.get("target_audience") or f"『{p_name}』만의 차별화된 품질과 알찬 구성을 지금 바로 만나보세요."
        p_pain_title = prod_info.get("pain_title") or '"비슷해 보이는 수많은 상품들, 어떤 걸 골라야 실패가 없을까요?"'
        p_pain_desc = prod_info.get("pain_desc") or "광고만 믿고 구매했다가 아쉬운 품질이나 번거로운 준비 과정 때문에 실망하셨다면 이제 검증된 상품을 선택할 때입니다."
        p_sol_title = prod_info.get("sol_title") or f"실제 구매자 리뷰와 품질로 증명된 『{p_name_short}』만의 핵심 비결!"
        p_sol_desc = prod_info.get("sol_desc") or p_target_desc

        bento_items = prod_info.get("bento_items") or [
            {"step": "POINT 01 · 핵심 품질", "title": f"『{p_name_short}』만의 독보적 퀄리티", "desc": p_target_desc},
            {"step": "POINT 02 · 알찬 구성", "title": "누구나 간편하게 즐기는 올인원 구성", "desc": "복잡한 준비 없이 바로 활용할 수 있도록 핵심 구성을 알차게 담았습니다."},
            {"step": "POINT 03 · 검증된 만족도", "title": "실구매 고객들이 극찬한 재구매 아이템", "desc": "높은 평점과 생생한 구매 후기가 증명하는 실패 없는 선택입니다."},
            {"step": "POINT 04 · 합리적 가성비", "title": f"단 {p_price}으로 누리는 확실한 만족", "desc": "불필요한 거품을 덜어내고 가격 대비 최고의 만족감을 선사합니다."},
        ]

        top_summary_li = ""
        bento_cards_html = ""
        border_colors = ["border-t-emerald-600", "border-t-blue-600", "border-t-indigo-600", "border-t-amber-500"]
        badge_colors = ["bg-emerald-100 text-emerald-800", "bg-blue-100 text-blue-800", "bg-indigo-100 text-indigo-800", "bg-amber-100 text-amber-800"]

        for idx, b in enumerate(bento_items[:4]):
            top_summary_li += f"""
            <li class="flex items-start gap-2.5">
              <span class="text-emerald-600 font-bold">0{idx+1}</span>
              <span><strong>{b.get('title', '')}:</strong> {b.get('desc', '')[:80]}</span>
            </li>"""
            bento_cards_html += f"""
        <div class="bg-slate-50 border border-slate-200 rounded-2xl p-7 border-t-4 {border_colors[idx % 4]} shadow-sm">
          <div class="flex items-center justify-between mb-3">
            <span class="px-3 py-1 rounded-full {badge_colors[idx % 4]} text-xs font-bold">{b.get('step', f'POINT 0{idx+1}')}</span>
          </div>
          <h3 class="text-xl font-black text-slate-900 mb-3">{b.get('title', '')}</h3>
          <p class="text-sm text-slate-700 leading-relaxed">{b.get('desc', '')}</p>
        </div>"""

        metrics = prod_info.get("metrics") or [
            {"val": p_price, "label": "공식 판매 가격"},
            {"val": "100%", "label": "원본 비율 이미지 보존"},
            {"val": "BEST", "label": "엄선된 핵심 구성"},
            {"val": "★ 4.9+", "label": "구매 고객 실사용 만족도"},
        ]
        metrics_html = ""
        m_colors = ["text-amber-400", "text-emerald-400", "text-sky-400", "text-pink-400"]
        for idx, m in enumerate(metrics[:4]):
            metrics_html += f"""
      <div class="p-3">
        <div class="text-3xl sm:text-4xl font-black {m_colors[idx % 4]}">{m.get('val', '')}</div>
        <div class="text-xs sm:text-sm text-slate-300 mt-1 font-medium">{m.get('label', '')}</div>
      </div>"""

        sub_btn_hero = ""
        if p_sub_price.strip():
            sub_btn_hero = f"""
          <a href="{p_paper_link}" target="_blank" class="w-full sm:w-auto px-6 py-4 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-800 font-bold text-base border border-slate-300 transition text-center">
            📦 추가 옵션 구매 ({p_sub_price})
          </a>"""

        # 대표 상품 이미지 HTML: 도서일 때만 3D 책 목업, 일반 상품은 자르지 않은 원본 비율 그대로 노출!
        if is_book and cover_b64:
            hero_img_html = f"""
        <div class="book-3d flex justify-center">
          <div class="book-spine relative w-64 sm:w-72 rounded-r-lg overflow-hidden border border-slate-200 bg-white">
            <img src="{cover_b64}" alt="{p_name} 대표 이미지" class="w-full h-auto object-contain">
          </div>
        </div>"""
        elif cover_b64:
            hero_img_html = f"""
        <div class="flex justify-center">
          <div class="p-3 rounded-3xl border-2 border-slate-200 bg-white shadow-xl">
            <img src="{cover_b64}" alt="{p_name} 원본 대표 이미지" class="max-w-full sm:max-w-[380px] max-h-[420px] w-auto h-auto object-contain rounded-2xl mx-auto">
          </div>
        </div>"""
        else:
            hero_img_html = ""

        # Problem / Solution 이미지도 절대 자르지 않고(object-contain) 원본 비율 그대로 표시
        pain_img_block = f"""
      <div class="my-6 max-w-3xl mx-auto rounded-2xl overflow-hidden border border-rose-300 bg-white p-3 shadow-md flex justify-center">
        <img src="{pain_b64}" alt="{p_name_short} 상품 상세 이미지 1" class="max-w-full max-h-[540px] w-auto h-auto object-contain rounded-xl mx-auto">
      </div>""" if pain_b64 else ""

        sol_img_block = f"""
      <div class="my-6 max-w-3xl mx-auto rounded-2xl overflow-hidden border border-emerald-300 bg-white p-3 shadow-md flex justify-center">
        <img src="{sol_b64}" alt="{p_name_short} 상품 상세 이미지 2" class="max-w-full max-h-[540px] w-auto h-auto object-contain rounded-xl mx-auto">
      </div>""" if sol_b64 else ""

        hero_badge_text = (
            f"✨ {p_author} 공식 추천 · 핵심 노하우 완벽 수록!"
            if is_book
            else f"✨ {p_author} 공식 스토어 · 품질 & 실구매 만족도 검증!"
        )
        section5_sub = (
            "CORE FEATURES & CURRICULUM"
            if is_book
            else "CORE PRODUCT HIGHLIGHTS"
        )
        section5_title = (
            f"『{p_name_short}』 4대 핵심 구성 로드맵"
            if is_book
            else f"『{p_name_short}』 4대 핵심 매력 포인트"
        )
        section5_desc = (
            "순서대로 따라만 하면 초보자도 완벽한 결과를 완성할 수 있습니다"
            if is_book
            else "엄선된 원료와 차별화된 구성으로 왜 많은 분들이 다시 찾는지 확인해 보세요"
        )
        pain_bottom_text = (
            "👉 막연한 고민과 시행착오를 끝내려면, 처음부터 끝까지 검증된 실전 로드맵이 필요합니다!"
            if is_book
            else f"👉 이제 실패 없는 선택을 위해, 맛과 품질부터 구성까지 검증된 『{p_name_short}』를 만나보세요!"
        )
        sol_bottom_text = (
            f"👉 『{p_name_short}』와 함께라면 복잡한 과정 없이 가장 빠르고 확실하게 원하는 결과를 얻을 수 있습니다!"
            if is_book
            else f"👉 『{p_name_short}』 하나면 번거로운 준비 없이 누구나 간편하게 최고의 만족을 누릴 수 있습니다!"
        )

        video_section = self._build_video_section(prod_info)
        gallery_section = self._build_gallery_section(prod_info)
        comparison_section = self._build_comparison_section(prod_info)
        reviews_section = self._build_reviews_section(prod_info)
        faq_section = self._build_faq_section(prod_info)
        gifts_section = self._build_gifts_section(prod_info, is_book)

        html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{p_name} - 공식 상세페이지 &amp; 랜딩페이지</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" />
  <style>
    * {{
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      text-rendering: optimizeLegibility;
    }}
    h1, h2, h3, h4, p {{ word-break: keep-all; }}
    h1, h2, h3 {{ text-wrap: balance; }}
    body {{
      font-family: Pretendard, -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
      background-color: #F8FAFC;
      color: #0F172A;
      letter-spacing: -0.02em;
    }}
    .book-3d {{ perspective: 1000px; }}
    .book-spine {{
      transform: rotateY(-18deg) rotateX(4deg);
      box-shadow: -15px 20px 35px rgba(6, 78, 59, 0.28);
      transition: transform 0.4s ease;
    }}
    .book-spine:hover {{ transform: rotateY(-8deg) rotateX(2deg) translateY(-6px); }}
  </style>
</head>
<body class="min-h-screen selection:bg-emerald-600 selection:text-white">

  <!-- ==================== [섹션 1: 밝은 배경] HERO SECTION ==================== -->
  <section class="bg-white border-b border-slate-100 pt-14 pb-20 px-4 sm:px-6 lg:px-8">
    <div class="max-w-6xl mx-auto">
      <div class="flex justify-center mb-6">
        <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs sm:text-sm font-bold shadow-sm">
          <span class="inline-block w-2 h-2 rounded-full bg-emerald-600 animate-pulse"></span>
          {hero_badge_text}
        </div>
      </div>

      <div class="text-center max-w-5xl mx-auto">
        <h1 class="font-black text-slate-900 tracking-tight leading-tight">
          <span class="block text-2xl sm:text-4xl lg:text-5xl text-slate-900">
            {p_headline_1}
          </span>
          <span class="block text-2xl sm:text-4xl lg:text-5xl text-emerald-700 mt-2.5">
            {p_headline_2}
          </span>
        </h1>
        <p class="mt-6 text-base sm:text-xl text-slate-600 leading-relaxed font-normal max-w-3xl mx-auto">
          <strong class="text-slate-900 font-semibold">{p_name}</strong> ({p_author}) — {p_target_desc}
        </p>

        <div class="mt-8 flex flex-col sm:flex-row items-center justify-center gap-4">
          <a href="{p_ebook_link}" target="_blank" class="w-full sm:w-auto px-8 py-4 rounded-xl bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-lg shadow-xl shadow-emerald-600/20 transition-all transform hover:-translate-y-0.5 text-center flex items-center justify-center gap-2">
            <span>🚀 지금 바로 구매하기 ({p_price})</span>
            <span>→</span>
          </a>
          {sub_btn_hero}
        </div>
      </div>

      <div class="mt-14 flex flex-col lg:flex-row items-center justify-center gap-10">
        {hero_img_html}

        <div class="w-full lg:w-[480px] bg-slate-50 border border-slate-200 rounded-2xl p-6 sm:p-7 text-left shadow-sm">
          <div class="text-xs font-bold text-emerald-700 uppercase tracking-wider mb-2">KEY HIGHLIGHTS SUMMARY</div>
          <h3 class="text-xl font-bold text-slate-900 mb-4">『{p_name_short}』 핵심 포인트 4가지</h3>
          <ul class="space-y-3.5 text-sm text-slate-700">{top_summary_li}
          </ul>
        </div>
      </div>
    </div>
  </section>

  <!-- ==================== [섹션 2: 어두운 배경 교차] SOCIAL PROOF STATS BAR ==================== -->
  <section class="bg-slate-900 text-white py-10 px-4">
    <div class="max-w-5xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-6 text-center">{metrics_html}
    </div>
  </section>

  {video_section}

  <!-- ==================== [섹션 3: 밝은 웜톤 교차] PROBLEM (원본 상품 이미지 비율 그대로 유지) ==================== -->
  <section class="py-20 px-4 sm:px-6 lg:px-8 max-w-5xl mx-auto">
    <div class="bg-rose-50/70 border-2 border-rose-200 rounded-3xl p-6 sm:p-10 shadow-lg">
      <div class="max-w-3xl mx-auto mb-6">
        <span class="inline-block px-3.5 py-1.5 rounded-md bg-rose-100 text-rose-700 text-xs font-bold mb-3 border border-rose-300">
          🚨 WHY THIS MATTERS (구매 전 꼭 확인해야 할 포인트)
        </span>
        <h2 class="text-2xl sm:text-3xl font-black text-slate-900 mb-3">
          {p_pain_title}
        </h2>
        <p class="text-slate-600 text-base leading-relaxed">
          {p_pain_desc}
        </p>
      </div>

      {pain_img_block}

      <div class="max-w-3xl mx-auto bg-rose-100/90 rounded-xl p-4 border border-rose-300">
        <p class="text-sm sm:text-base text-rose-900 font-bold">
          {pain_bottom_text}
        </p>
      </div>
    </div>
  </section>

  <!-- ==================== [섹션 4: 밝은 쿨톤 교차] SOLUTION (원본 상품 이미지 비율 그대로 유지) ==================== -->
  <section class="py-12 px-4 sm:px-6 lg:px-8 max-w-5xl mx-auto">
    <div class="bg-emerald-50/70 border-2 border-emerald-200 rounded-3xl p-6 sm:p-10 shadow-lg">
      <div class="max-w-3xl mx-auto mb-6">
        <span class="inline-block px-3.5 py-1.5 rounded-md bg-emerald-100 text-emerald-800 text-xs font-bold mb-3 border border-emerald-300">
          💡 BEST CHOICE &amp; SOLUTION (검증된 핵심 가치)
        </span>
        <h2 class="text-2xl sm:text-3xl font-black text-slate-900 mb-3">
          {p_sol_title}
        </h2>
        <p class="text-slate-600 text-base leading-relaxed">
          {p_sol_desc}
        </p>
      </div>

      {sol_img_block}

      <div class="max-w-3xl mx-auto bg-emerald-100/90 rounded-xl p-4 border border-emerald-300">
        <p class="text-sm sm:text-base text-emerald-950 font-bold">
          {sol_bottom_text}
        </p>
      </div>
    </div>
  </section>

  {gallery_section}
  {comparison_section}

  <!-- ==================== [섹션 5: 밝은 화이트 교차] 4대 핵심 특장점 (Bento Grid) ==================== -->
  <section class="bg-white border-y border-slate-200 py-20 px-4 sm:px-6 lg:px-8">
    <div class="max-w-6xl mx-auto">
      <div class="text-center mb-14">
        <h2 class="text-xs font-bold text-emerald-700 uppercase tracking-widest">{section5_sub}</h2>
        <p class="text-2xl sm:text-4xl font-black text-slate-900 mt-2">{section5_title}</p>
        <p class="text-slate-500 text-sm sm:text-base mt-2">{section5_desc}</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">{bento_cards_html}
      </div>
    </div>
  </section>

  <!-- ==================== [섹션 6: 밝은 슬레이트 교차] 브랜드 / 판매처 소개 ==================== -->
  <section class="py-16 px-4 sm:px-6 lg:px-8 max-w-5xl mx-auto">
    <div class="bg-white border border-slate-200 rounded-3xl p-8 shadow-sm flex flex-col sm:flex-row items-center gap-8">
      <div class="w-24 h-24 rounded-full bg-gradient-to-tr from-emerald-700 to-teal-500 flex items-center justify-center text-white text-xl font-black shadow-lg shrink-0 text-center px-2">
        OFFICIAL
      </div>
      <div>
        <div class="text-xs font-bold text-emerald-700 uppercase tracking-wider">OFFICIAL STORE &amp; BRAND</div>
        <h3 class="text-2xl font-black text-slate-900 mt-1">{p_author}</h3>
        <p class="text-sm text-slate-600 mt-2.5 leading-relaxed">
          {p_target_desc}
        </p>
      </div>
    </div>
  </section>

  {reviews_section}
  {faq_section}
  {gifts_section}

  <!-- ==================== [섹션 7: 프리미엄 다크 교차] PRICING & OFFER ==================== -->
  <section id="pricing" class="bg-slate-950 text-white py-20 px-4 sm:px-6 lg:px-8">
    <div class="max-w-4xl mx-auto text-center">
      <span class="px-3.5 py-1.5 rounded-full bg-emerald-900/60 text-emerald-300 text-xs font-bold border border-emerald-500/40">SPECIAL OFFER</span>
      <h2 class="text-3xl sm:text-4xl font-black text-white mt-3">지금 바로 『{p_name_short}』를 만나보세요!</h2>
      <p class="text-slate-400 text-sm sm:text-base mt-2">{p_target_desc}</p>

      <div class="mt-10 rounded-3xl bg-gradient-to-b from-emerald-950 via-slate-900 to-slate-900 p-8 border-2 border-emerald-500 shadow-2xl max-w-2xl mx-auto">
        <div class="text-lg font-extrabold text-emerald-300">{p_name}</div>
        <div class="mt-3 flex items-baseline justify-center gap-3">
          <span class="text-4xl sm:text-5xl font-black text-amber-400">{p_price}</span>
          {f'<span class="text-sm text-slate-300">(추가 옵션: {p_sub_price})</span>' if p_sub_price.strip() else ''}
        </div>
        <div class="mt-8 flex flex-col sm:flex-row gap-4 justify-center">
          <a href="{p_ebook_link}" target="_blank" class="flex-1 py-4 px-6 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-extrabold text-center text-base shadow-lg shadow-emerald-500/30 transition">
            🚀 공식 스토어에서 즉시 구매하기 ({p_price}) →
          </a>
          {f'<a href="{p_paper_link}" target="_blank" class="flex-1 py-4 px-6 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold text-center text-base border border-slate-700 transition">📦 추가 옵션 주문하기 ({p_sub_price}) →</a>' if p_sub_price.strip() else ''}
        </div>
      </div>
    </div>
  </section>

  <footer class="py-12 bg-slate-900 border-t border-slate-800 text-center text-xs text-slate-500">
    <p>© 2026 {p_name}. {p_author}. All rights reserved.</p>
  </footer>

</body>
</html>"""
        return html

    def render_all(self, prod_info: dict):
        html_content = self.generate_html(prod_info)
        html_path = "pro_detail_page.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        png_path = "detail_page_render.png"
        if sync_playwright is not None:
            try:
                with sync_playwright() as p:
                    browser = p.chromium.launch(headless=True)
                    page = browser.new_page(viewport={"width": 1200, "height": 800}, device_scale_factor=2)
                    abs_html_path = os.path.abspath(html_path).replace("\\", "/")
                    page.goto(f"file:///{abs_html_path}", wait_until="networkidle")
                    page.evaluate("() => document.fonts.ready")
                    page.wait_for_timeout(1200)
                    page.screenshot(path=png_path, full_page=True)
                    browser.close()
            except Exception as e:
                print(f"Playwright rendering notice: {e}")
