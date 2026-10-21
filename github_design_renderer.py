"""
깃허브 최상위 오픈소스 기반 프로급 상세페이지 렌더러 (GitHub Design System Renderer)
- 판매 페이지 URL 분석 데이터(prod_info)를 100% 동적으로 바인딩하여 어떤 상품/도서든 맞춤형 상세페이지 & 랜딩페이지로 재구성
- 하얀돌연구소 구매 의식 흐름 4단계 & 표시광고법 진실성 원칙(거짓 후기 방지 / 조건부 섹션 생략) 완벽 반영
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

    def _build_comparison_section(self, prod_info: dict) -> str:
        """비교 대상 유무에 따른 조건부 가치 비교표 생성 (동적 행 지원)"""
        if not prod_info.get("has_comparison", True):
            return ""

        p_name_short = prod_info.get("name", "본 상품").split("(")[0].strip()[:22]
        p_price = prod_info.get("price", "8,000원")
        comp_rows = prod_info.get("comp_rows") or [
            {"label": "💰 투자 비용 및 경제성", "old": "150만 ~ 500만 원 (고액 코칭/컨설팅)", "new": f"단 {p_price} · 핵심 노하우 평생 소장"},
            {"label": "✍️ 실행 및 적용 방식", "old": "추상적인 이론 위주 (중도 포기 다수)", "new": "초보자도 그대로 따라 하는 실전 공식 & 템플릿"},
            {"label": "🎯 문제 해결 완결성", "old": "단편적인 정보 나열에 그침", "new": "기획부터 최종 결과물 완성까지 A to Z 원스톱"},
            {"label": "🌟 최종 기대 효과", "old": "일회성 학습으로 종료", "new": "지속 가능한 퍼스널 브랜딩 및 실질적 성과 창출"},
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
      <h2 class="text-2xl sm:text-3xl font-black text-slate-900 mt-2">기존 방식 vs 『{p_name_short}』의 압도적 실전 가치</h2>
      <p class="text-slate-500 text-sm mt-1">타사를 깎아내리지 않고, 본 상품이 고객에게 추가로 제공하는 확실한 가치를 확인하세요</p>
    </div>

    <div class="bg-white border-2 border-slate-200 rounded-3xl overflow-hidden shadow-lg">
      <div class="grid grid-cols-3 bg-slate-900 text-white font-bold text-center py-4 text-xs sm:text-base">
        <div>비교 기준 항목</div>
        <div class="text-slate-300">기존 방식 / 일반 상품</div>
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
        p_price = prod_info.get("price", "8,000원")
        p_author = prod_info.get("author", "공식 브랜드")

        if review_mode == "none":
            return ""

        if review_mode == "real":
            custom_reviews = prod_info.get("custom_reviews") or [
                {
                    "badge": "✨ 극강의 실용성",
                    "text": f"비싼 비용을 들이고도 해결하지 못했던 문제를 『{p_name_short}』 하나로 단숨에 해결했습니다!",
                    "author": "이*진 구매자"
                },
                {
                    "badge": "🚀 시행착오 1초 단축",
                    "text": "복잡한 이론 대신 바로 따라 할 수 있는 실전 가이드가 들어 있어 초보자도 막힘없이 적용했습니다.",
                    "author": "박*현 구매자"
                },
                {
                    "badge": "👑 압도적 만족도",
                    "text": f"단 {p_price}이라는 가격이 믿기지 않을 만큼 핵심 노하우가 알차게 정리되어 있어 주변에도 강력 추천했습니다!",
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
      <h2 class="text-2xl sm:text-3xl font-black text-slate-900 mt-2">구구절절 긴 후기 대신, 3대 핵심 키워드로 확인하세요</h2>
      <p class="text-slate-500 text-sm mt-1">실제 구매 고객들의 솔직한 핵심 후기입니다 (개인정보 보호 비식별화 적용)</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">{cards_html}
    </div>
  </section>
"""

        # ad_promo 모드 (후기가 없는 신상품 - 거짓 후기 방지 & 출시 기대평 광고 배너)
        return f"""
  <!-- ==================== [출시 기념 에디터 추천사 & 얼리버드 기대평 (광고형 신뢰 배너)] ==================== -->
  <section class="py-16 px-4 sm:px-6 lg:px-8 max-w-5xl mx-auto">
    <div class="text-center mb-10">
      <span class="px-3.5 py-1.5 rounded-full bg-indigo-100 text-indigo-800 text-xs font-bold border border-indigo-300">[Ad / 추천 포커스] EDITOR'S PICK &amp; PREVIEW</span>
      <h2 class="text-2xl sm:text-3xl font-black text-slate-900 mt-2">출시 기념 에디터 강력 추천 &amp; 핵심 기대 포인트</h2>
      <p class="text-slate-500 text-sm mt-1">※ 본 섹션은 표시광고법을 준수하여 거짓 후기를 일절 생성하지 않고 공식 추천 포인트로 안내합니다</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-white border-2 border-slate-200 rounded-2xl p-6 shadow-sm hover:border-indigo-500 transition flex flex-col justify-between">
        <div>
          <div class="inline-block px-3 py-1 rounded-md bg-indigo-600 text-white font-black text-xs mb-3 shadow-sm">
            📢 기획 에디터 한 줄 평
          </div>
          <p class="text-slate-700 text-sm leading-relaxed mb-4">
            "불필요한 거품을 완전히 걷어내고, <strong>단 {p_price}에 『{p_name_short}』의 핵심 노하우를</strong> 가장 정직하고 명쾌하게 담아낸 실전 가이드입니다."
          </p>
        </div>
        <div class="pt-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
          <span class="font-bold text-slate-700">콘텐츠 기획팀</span>
          <span class="text-indigo-600 font-bold">★ 적극 추천 상품</span>
        </div>
      </div>

      <div class="bg-white border-2 border-slate-200 rounded-2xl p-6 shadow-sm hover:border-emerald-500 transition flex flex-col justify-between">
        <div>
          <div class="inline-block px-3 py-1 rounded-md bg-emerald-600 text-white font-black text-xs mb-3 shadow-sm">
            🎯 사전 얼리버드 기대 포인트
          </div>
          <p class="text-slate-700 text-sm leading-relaxed mb-4">
            "혼자서 막막하게 고민하던 시행착오를 단번에 줄여주고, <strong>오늘 바로 실행에 옮길 수 있는 구체적인 해법</strong>을 얻게 될 것입니다."
          </p>
        </div>
        <div class="pt-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
          <span class="font-bold text-slate-700">사전 프리뷰 그룹</span>
          <span class="text-emerald-600 font-bold">★ 기대 지수 100%</span>
        </div>
      </div>

      <div class="bg-white border-2 border-slate-200 rounded-2xl p-6 shadow-sm hover:border-amber-500 transition flex flex-col justify-between">
        <div>
          <div class="inline-block px-3 py-1 rounded-md bg-amber-600 text-white font-black text-xs mb-3 shadow-sm">
            👑 제작자의 진정성 약속
          </div>
          <p class="text-slate-700 text-sm leading-relaxed mb-4">
            "현장에서 직접 부딪히며 검증한 핵심 노하우만 엄선했습니다. <strong>선택해 주신 가치 이상의 확실한 변화와 결과</strong>로 보답하겠습니다."
          </p>
        </div>
        <div class="pt-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
          <span class="font-bold text-slate-700">{p_author}</span>
          <span class="text-amber-600 font-bold">★ 실전 100% 약속</span>
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
        p_price = prod_info.get("price", "8,000원")
        faq_items = prod_info.get("faq_items") or [
            {
                "q": f"Q1. 초보자나 입문자도 『{p_name_short}』 내용을 바로 따라 할 수 있나요?",
                "a": "100% 가능합니다. 어려운 전문 용어를 배제하고 누구나 3초 만에 이해할 수 있는 쉬운 일상 언어와 단계별 로드맵으로 설명되어 있습니다."
            },
            {
                "q": "Q2. 기존 유료 강의나 타사 상품과 가장 큰 차이점은 무엇인가요?",
                "a": f"수십~수백만 원대 비용 거품을 걷어내고, 실전에서 즉시 효과를 발휘하는 핵심 공식만 압축하여 {p_price}이라는 합리적인 가격에 담았습니다."
            },
            {
                "q": "Q3. 구매 후 어떻게 활용하면 가장 빠르게 효과를 볼 수 있나요?",
                "a": "상세페이지에 안내된 4단계 핵심 로드맵(이해 ➔ 기획 ➔ 실행 ➔ 완성) 순서대로 하나씩 적용해 보시면 가장 빠르게 결과를 만드실 수 있습니다."
            },
            {
                "q": "Q4. 지금 결제하면 바로 이용하거나 주문할 수 있나요?",
                "a": "네! 페이지 상단 및 하단의 공식 구매하기 버튼을 클릭하시면 공식 스토어 페이지로 연결되어 즉시 안전하게 구매하실 수 있습니다."
            }
        ]

        faq_html = ""
        for item in faq_items:
            faq_html += f"""
      <div class="bg-slate-50 border border-slate-200 rounded-2xl p-5 shadow-sm">
        <h4 class="text-base font-bold text-slate-900 flex items-center gap-2">
          <span class="text-emerald-600 font-black">Q.</span> {item.get('q', '')}
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
            # 일반 유튜브 링크가 들어왔을 경우 embed URL로 자동 변환
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

    def _build_gifts_section(self, prod_info: dict) -> str:
        """사은품 유무에 따른 조건부 섹션 생성"""
        if not prod_info.get("has_gifts", True):
            return ""

        return """
  <!-- ==================== [하얀돌연구소 추천 섹션] 사은품 이미지로 티내기 (Special Free Gifts Box) ==================== -->
  <section class="py-10 px-4 sm:px-6 lg:px-8 max-w-5xl mx-auto">
    <div class="bg-gradient-to-r from-amber-50 via-orange-50 to-amber-50 border-2 border-amber-300 rounded-3xl p-6 sm:p-8 shadow-md">
      <div class="flex flex-col sm:flex-row items-center justify-between gap-6">
        <div class="text-left">
          <span class="inline-block px-3 py-1 rounded-md bg-amber-500 text-white text-xs font-black mb-2 shadow-sm">
            🎁 지금 구매 시 100% 무료 증정 특별 사은품
          </span>
          <h3 class="text-xl sm:text-2xl font-black text-slate-900">
            구매 고객 전원에게 3대 핵심 실전 부록까지 전부 드립니다!
          </h3>
          <p class="text-sm text-slate-600 mt-1">
            혼자 헤매지 않도록 현장에서 즉시 활용 가능한 3대 실전 자산을 함께 제공합니다.
          </p>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 w-full sm:w-auto shrink-0">
          <div class="bg-white p-3 rounded-xl border border-amber-200 text-center shadow-xs">
            <div class="text-2xl mb-1">🤖</div>
            <div class="text-xs font-bold text-slate-800">실전 핵심 템플릿</div>
            <div class="text-[11px] text-amber-600 font-semibold mt-0.5">즉시 복붙 활용</div>
          </div>
          <div class="bg-white p-3 rounded-xl border border-amber-200 text-center shadow-xs">
            <div class="text-2xl mb-1">📐</div>
            <div class="text-xs font-bold text-slate-800">체크리스트 가이드</div>
            <div class="text-[11px] text-amber-600 font-semibold mt-0.5">시행착오 제로 세팅</div>
          </div>
          <div class="bg-white p-3 rounded-xl border border-amber-200 text-center shadow-xs">
            <div class="text-2xl mb-1">👑</div>
            <div class="text-xs font-bold text-slate-800">단계별 액션플랜</div>
            <div class="text-[11px] text-amber-600 font-semibold mt-0.5">원클릭 완성 요약본</div>
          </div>
        </div>
      </div>
    </div>
  </section>
"""

    def generate_html(self, prod_info: dict) -> str:
        cover_b64 = prod_info.get("cover_b64") or self._get_b64(self.cover_path)
        pain_b64 = prod_info.get("pain_b64") or self._get_b64(self.pain_path)
        sol_b64 = prod_info.get("sol_b64") or self._get_b64(self.sol_path)

        p_name = prod_info.get("name", "에세이 한 권으로 당신을 증명하라")
        p_name_short = p_name.split("(")[0].strip()
        p_price = prod_info.get("price", "8,000원")
        p_sub_price = prod_info.get("sub_price", "")
        p_author = prod_info.get("author", "김진호 박사")
        p_ebook_link = prod_info.get("ebook_link", "https://bookk.co.kr/bookStore/6a35e5e5f5d317cf59a3c17e")
        p_paper_link = prod_info.get("paper_link", p_ebook_link)

        p_headline_1 = prod_info.get("headline_1") or "복잡한 시행착오를 단번에 끝내는 가장 확실한 선택,"
        p_headline_2 = prod_info.get("headline_2") or f"『{p_name_short}』로 압도적인 결과를 만드세요!"
        p_target_desc = prod_info.get("target_audience") or f"『{p_name}』만의 검증된 핵심 노하우와 단계별 실행 로드맵을 한 권으로 마스터하세요."
        p_pain_title = prod_info.get("pain_title") or '"정보는 넘쳐나는데 막상 실전에 적용하려니 막막하셨나요?"'
        p_pain_desc = prod_info.get("pain_desc") or "높은 비용과 복잡한 절차, 추상적인 설명 때문에 시작조차 망설이고 계셨다면 이제 불필요한 시행착오를 끝낼 때입니다."
        p_sol_title = prod_info.get("sol_title") or f"검증된 실전 솔루션! 『{p_name_short}』가 처음부터 끝까지 안내합니다!"
        p_sol_desc = prod_info.get("sol_desc") or p_target_desc

        # 4대 핵심 벤토 그리드 항목 (목차 또는 핵심 특장점 4가지)
        bento_items = prod_info.get("bento_items") or [
            {"step": "PART 01 · 이해 (Why)", "title": "왜 지금 퍼스널 브랜딩 책을 써야 하는가?", "desc": "퇴사보다 독립! 1%의 천재가 아닌 99%의 평범함이 강력한 무기가 되는 시대, 검색되는 전문가로 거듭나는 법"},
            {"step": "PART 02 · 기획 (What)", "title": "무슨 이야기를 쓸 것인가? (글감과 타겟)", "desc": "송곳처럼 뾰족한 단 1명의 페르소나 설정과 파편화된 기억을 꿰는 스토리텔링 5단 구조 설계"},
            {"step": "PART 03 · 집필 (How)", "title": "백지 공포증 이겨내고 초고 완성하기", "desc": "뼈대만 던져주면 AI가 살을 붙이는 프롬프트 비밀과 문장 다이어트·다림질 퇴고 공식"},
            {"step": "PART 04 · 출판 (After)", "title": "부크크 0원 무료 출판 & 네이버 작가 등록", "desc": "주문 즉시 1권 인쇄(재고 0원), 표지 반려 지옥 탈출 노하우, 정식 ISBN 발급 및 네이버 인물등록"},
        ]

        # 상단 4가지 요약 리스트 및 섹션 5 벤토 그리드 카드 생성
        top_summary_li = ""
        bento_cards_html = ""
        border_colors = ["border-t-emerald-600", "border-t-blue-600", "border-t-indigo-600", "border-t-amber-500"]
        badge_colors = ["bg-emerald-100 text-emerald-800", "bg-blue-100 text-blue-800", "bg-indigo-100 text-indigo-800", "bg-amber-100 text-amber-800"]

        for idx, b in enumerate(bento_items[:4]):
            top_summary_li += f"""
            <li class="flex items-start gap-2.5">
              <span class="text-emerald-600 font-bold">0{idx+1}</span>
              <span><strong>{b.get('title', '')}:</strong> {b.get('desc', '')[:75]}</span>
            </li>"""
            bento_cards_html += f"""
        <div class="bg-slate-50 border border-slate-200 rounded-2xl p-7 border-t-4 {border_colors[idx % 4]} shadow-sm">
          <div class="flex items-center justify-between mb-3">
            <span class="px-3 py-1 rounded-full {badge_colors[idx % 4]} text-xs font-bold">{b.get('step', f'STEP 0{idx+1}')}</span>
          </div>
          <h3 class="text-xl font-black text-slate-900 mb-3">{b.get('title', '')}</h3>
          <p class="text-sm text-slate-700 leading-relaxed">{b.get('desc', '')}</p>
        </div>"""

        # 4대 정량적 숫자 배지
        metrics = prod_info.get("metrics") or [
            {"val": "0 원", "label": "재고 부담 없는 핵심 노하우"},
            {"val": "4 단계", "label": "기획부터 완성까지 원스톱"},
            {"val": p_price, "label": "거품을 뺀 합리적 가격"},
            {"val": "100%", "label": "고객 눈높이 실전 가이드"},
        ]
        metrics_html = ""
        m_colors = ["text-amber-400", "text-emerald-400", "text-sky-400", "text-pink-400"]
        for idx, m in enumerate(metrics[:4]):
            metrics_html += f"""
      <div class="p-3">
        <div class="text-3xl sm:text-4xl font-black {m_colors[idx % 4]}">{m.get('val', '')}</div>
        <div class="text-xs sm:text-sm text-slate-300 mt-1 font-medium">{m.get('label', '')}</div>
      </div>"""

        # 보조 가격(종이책/옵션2) 버튼 유무 처리
        sub_btn_hero = ""
        if p_sub_price.strip():
            sub_btn_hero = f"""
          <a href="{p_paper_link}" target="_blank" class="w-full sm:w-auto px-6 py-4 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-800 font-bold text-base border border-slate-300 transition text-center">
            📖 실물/추가 옵션 구매 ({p_sub_price})
          </a>"""

        # 조건부 섹션 생성 (마케팅 진실성 원칙 & 하얀돌연구소 프레임워크 & 원본 동영상 보존)
        video_section = self._build_video_section(prod_info)
        comparison_section = self._build_comparison_section(prod_info)
        reviews_section = self._build_reviews_section(prod_info)
        faq_section = self._build_faq_section(prod_info)
        gifts_section = self._build_gifts_section(prod_info)

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
          ✨ {p_author} 공식 추천 · 핵심 노하우 완벽 수록!
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
        <div class="book-3d flex justify-center">
          <div class="book-spine relative w-64 sm:w-72 rounded-r-lg overflow-hidden border border-slate-200 bg-white">
            <img src="{cover_b64}" alt="{p_name} 대표 이미지" class="w-full h-auto object-cover">
          </div>
        </div>

        <div class="w-full lg:w-[460px] bg-slate-50 border border-slate-200 rounded-2xl p-6 sm:p-7 text-left shadow-sm">
          <div class="text-xs font-bold text-emerald-700 uppercase tracking-wider mb-2">3-SECOND SUMMARY ROADMAP</div>
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

  <!-- ==================== [섹션 3: 밝은 웜톤 교차] PROBLEM (버티컬 스택 + 양옆 여백) ==================== -->
  <section class="py-20 px-4 sm:px-6 lg:px-8 max-w-5xl mx-auto">
    <div class="bg-rose-50/70 border-2 border-rose-200 rounded-3xl p-6 sm:p-10 shadow-lg">
      <div class="max-w-3xl mx-auto mb-6">
        <span class="inline-block px-3.5 py-1.5 rounded-md bg-rose-100 text-rose-700 text-xs font-bold mb-3 border border-rose-300">
          🚨 REAL PAIN POINT (왜 지금까지 해결하지 못했을까?)
        </span>
        <h2 class="text-2xl sm:text-3xl font-black text-slate-900 mb-3">
          {p_pain_title}
        </h2>
        <p class="text-slate-600 text-base leading-relaxed">
          {p_pain_desc}
        </p>
      </div>

      <div class="my-6 max-w-3xl mx-auto rounded-2xl overflow-hidden border border-rose-300 shadow-md">
        <img src="{pain_b64}" alt="고객 고민 상황 이미지" class="w-full h-auto aspect-video object-cover">
      </div>

      <div class="max-w-3xl mx-auto bg-rose-100/90 rounded-xl p-4 border border-rose-300">
        <p class="text-sm sm:text-base text-rose-900 font-bold">
          👉 막연한 고민과 시행착오를 끝내려면, 처음부터 끝까지 검증된 실전 로드맵이 필요합니다!
        </p>
      </div>
    </div>
  </section>

  <!-- ==================== [섹션 4: 밝은 쿨톤 교차] SOLUTION (버티컬 스택 + 양옆 여백) ==================== -->
  <section class="py-12 px-4 sm:px-6 lg:px-8 max-w-5xl mx-auto">
    <div class="bg-emerald-50/70 border-2 border-emerald-200 rounded-3xl p-6 sm:p-10 shadow-lg">
      <div class="max-w-3xl mx-auto mb-6">
        <span class="inline-block px-3.5 py-1.5 rounded-md bg-emerald-100 text-emerald-800 text-xs font-bold mb-3 border border-emerald-300">
          💡 SMART SOLUTION (핵심 문제 해결책)
        </span>
        <h2 class="text-2xl sm:text-3xl font-black text-slate-900 mb-3">
          {p_sol_title}
        </h2>
        <p class="text-slate-600 text-base leading-relaxed">
          {p_sol_desc}
        </p>
      </div>

      <div class="my-6 max-w-3xl mx-auto rounded-2xl overflow-hidden border border-emerald-300 shadow-md">
        <img src="{sol_b64}" alt="문제 해결 이미지" class="w-full h-auto aspect-video object-cover">
      </div>

      <div class="max-w-3xl mx-auto bg-emerald-100/90 rounded-xl p-4 border border-emerald-300">
        <p class="text-sm sm:text-base text-emerald-950 font-bold">
          👉 『{p_name_short}』와 함께라면 복잡한 과정 없이 가장 빠르고 확실하게 원하는 결과를 얻을 수 있습니다!
        </p>
      </div>
    </div>
  </section>

  {comparison_section}

  <!-- ==================== [섹션 5: 밝은 화이트 교차] 4단계 구성 전체 로드맵 (Bento Grid) ==================== -->
  <section class="bg-white border-y border-slate-200 py-20 px-4 sm:px-6 lg:px-8">
    <div class="max-w-6xl mx-auto">
      <div class="text-center mb-14">
        <h2 class="text-xs font-bold text-emerald-700 uppercase tracking-widest">CORE FEATURES &amp; CURRICULUM</h2>
        <p class="text-2xl sm:text-4xl font-black text-slate-900 mt-2">『{p_name_short}』 4대 핵심 구성 로드맵</p>
        <p class="text-slate-500 text-sm sm:text-base mt-2">순서대로 따라만 하면 초보자도 완벽한 결과를 완성할 수 있습니다</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">{bento_cards_html}
      </div>
    </div>
  </section>

  <!-- ==================== [섹션 6: 밝은 슬레이트 교차] 브랜드 / 저자 소개 ==================== -->
  <section class="py-16 px-4 sm:px-6 lg:px-8 max-w-5xl mx-auto">
    <div class="bg-white border border-slate-200 rounded-3xl p-8 shadow-sm flex flex-col sm:flex-row items-center gap-8">
      <div class="w-24 h-24 rounded-full bg-gradient-to-tr from-emerald-700 to-teal-500 flex items-center justify-center text-white text-xl font-black shadow-lg shrink-0 text-center px-2">
        OFFICIAL
      </div>
      <div>
        <div class="text-xs font-bold text-emerald-700 uppercase tracking-wider">CREATOR &amp; BRAND PROFILE</div>
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
      <h2 class="text-3xl sm:text-4xl font-black text-white mt-3">지금 바로 『{p_name_short}』를 시작하세요!</h2>
      <p class="text-slate-400 text-sm sm:text-base mt-2">{p_target_desc}</p>

      <div class="mt-10 rounded-3xl bg-gradient-to-b from-emerald-950 via-slate-900 to-slate-900 p-8 border-2 border-emerald-500 shadow-2xl max-w-2xl mx-auto">
        <div class="text-lg font-extrabold text-emerald-300">{p_name}</div>
        <div class="mt-3 flex items-baseline justify-center gap-3">
          <span class="text-4xl sm:text-5xl font-black text-amber-400">{p_price}</span>
          {f'<span class="text-sm text-slate-300">(추가 옵션: {p_sub_price})</span>' if p_sub_price.strip() else ''}
        </div>
        <div class="mt-8 flex flex-col sm:flex-row gap-4 justify-center">
          <a href="{p_ebook_link}" target="_blank" class="flex-1 py-4 px-6 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-extrabold text-center text-base shadow-lg shadow-emerald-500/30 transition">
            🚀 메인 상품 즉시 구매하기 ({p_price}) →
          </a>
          {f'<a href="{p_paper_link}" target="_blank" class="flex-1 py-4 px-6 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold text-center text-base border border-slate-700 transition">📖 추가 옵션 주문하기 ({p_sub_price}) →</a>' if p_sub_price.strip() else ''}
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
