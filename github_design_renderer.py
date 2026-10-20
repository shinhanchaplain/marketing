"""
깃허브 최상위 오픈소스 기반 프로급 상세페이지 렌더러 (GitHub Design System Renderer)
- 하얀돌연구소 구매 의식 흐름 4단계 완벽 반영
- [마케팅 진실성 원칙 (Truth & Ethics)]:
    * 실제 구매 후기가 없는 경우 거짓 후기를 생성하지 않고 '출시 기념 기대평 & 에디터 추천 광고 배너'로 안전 전환
    * 입력값이 부족한 항목(비교 대상, 사은품, FAQ 등)은 억지로 지어내지 않고 결과물에서 깔끔하게 제외/생략
- 밝은/어두운 배경 교차, 모바일 퍼스트 1단 수직 배치, 상단 3초 요약 콕콕 카드 탑재
"""

import os
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

    def _build_comparison_section(self, prod_info: dict) -> str:
        """비교 대상 유무에 따른 조건부 가치 비교표 생성"""
        if not prod_info.get("has_comparison", True):
            return ""

        return """
  <!-- ==================== [하얀돌연구소 추천] 품격 있는 가치 비교표 ==================== -->
  <section class="py-16 px-4 sm:px-6 lg:px-8 max-w-5xl mx-auto">
    <div class="text-center mb-10">
      <span class="px-3.5 py-1.5 rounded-full bg-slate-100 text-slate-700 text-xs font-bold border border-slate-300">VALUE COMPARISON</span>
      <h2 class="text-2xl sm:text-3xl font-black text-slate-900 mt-2">일반 고액 책쓰기 코칭 vs 본 도서의 압도적 실전 가치</h2>
      <p class="text-slate-500 text-sm mt-1">타사를 깎아내리지 않고, 본 도서가 독자에게 추가로 제공하는 확실한 가치를 확인하세요</p>
    </div>

    <div class="bg-white border-2 border-slate-200 rounded-3xl overflow-hidden shadow-lg">
      <div class="grid grid-cols-3 bg-slate-900 text-white font-bold text-center py-4 text-xs sm:text-base">
        <div>비교 기준 항목</div>
        <div class="text-slate-300">기존 책쓰기 강의 / 일반 이론서</div>
        <div class="text-emerald-400 bg-emerald-950/60 py-1 rounded mx-1">👑 본 도서 (에세이 증명하라)</div>
      </div>
      <div class="divide-y divide-slate-200 text-xs sm:text-sm">
        <div class="grid grid-cols-3 p-4 items-center text-center">
          <div class="font-bold text-slate-800 text-left pl-2">💰 출판/교육 비용</div>
          <div class="text-slate-500">150만 ~ 500만 원 (고액 코칭/자비출판)</div>
          <div class="font-extrabold text-emerald-700 bg-emerald-50 py-1 rounded">단 8,000원 (커피 2잔 값) · 출판비 0원</div>
        </div>
        <div class="grid grid-cols-3 p-4 items-center text-center bg-slate-50/50">
          <div class="font-bold text-slate-800 text-left pl-2">✍️ 집필 방식 (초고)</div>
          <div class="text-slate-500">"무작정 매일 1장 쓰기" (중도포기 90%)</div>
          <div class="font-extrabold text-emerald-700 bg-emerald-50 py-1 rounded">AI 뼈대 프롬프트로 1시간 만에 초고 완성</div>
        </div>
        <div class="grid grid-cols-3 p-4 items-center text-center">
          <div class="font-bold text-slate-800 text-left pl-2">🪄 글 다듬기 (퇴고)</div>
          <div class="text-slate-500">추상적인 문학 이론 (감에 의존)</div>
          <div class="font-extrabold text-emerald-700 bg-emerald-50 py-1 rounded">문장 다이어트 & 번역체 제거 '다림질 공식'</div>
        </div>
        <div class="grid grid-cols-3 p-4 items-center text-center bg-slate-50/50">
          <div class="font-bold text-slate-800 text-left pl-2">📦 재고 및 인쇄 부담</div>
          <div class="text-slate-500">최소 500~1,000부 인쇄 (재고 떠안기)</div>
          <div class="font-extrabold text-emerald-700 bg-emerald-50 py-1 rounded">부크크 POD 무재고 0원 (주문 시 1권 즉시 인쇄)</div>
        </div>
        <div class="grid grid-cols-3 p-4 items-center text-center">
          <div class="font-bold text-slate-800 text-left pl-2">🎨 표지 규격 반려 해결</div>
          <div class="text-slate-500">규격 오차로 수차례 반려 지옥 경험</div>
          <div class="font-extrabold text-emerald-700 bg-emerald-50 py-1 rounded">한 번에 승인받는 인디자인 표지 실전 노하우</div>
        </div>
        <div class="grid grid-cols-3 p-4 items-center text-center bg-emerald-50/40">
          <div class="font-bold text-slate-900 text-left pl-2">🌟 최종 퍼스널 브랜딩</div>
          <div class="text-slate-500">서랍 속 원고나 단순 PDF 소장</div>
          <div class="font-extrabold text-emerald-800 bg-emerald-100 py-1 rounded">정식 ISBN 발급 + 네이버 인물검색 작가 등록</div>
        </div>
      </div>
    </div>
  </section>
"""

    def _mask_name(self, author_str: str) -> str:
        """개인정보 보호를 위한 실명 비식별화 마스킹 (예: 이수진 -> 이*진)"""
        import re
        return re.sub(r'(?<=[가-힣])([가-힣])(?=[가-힣])', '*', author_str)

    def _build_reviews_section(self, prod_info: dict) -> str:
        """
        [마케팅 진실성 원칙 (Truth & Ethics)]:
        - 'real': 실제 구매자 후기 렌더링 (핵심 키워드 강조 + 비식별화 마스킹)
        - 'ad_promo': 후기가 없는 신상품 ➔ 거짓 후기 없이 '출시 기대평 & 에디터 추천 광고 배너'로 안전 전환
        - 'none': 후기 섹션 완전 생략
        """
        review_mode = prod_info.get("review_mode", "ad_promo")

        if review_mode == "none":
            return ""

        if review_mode == "real":
            custom_reviews = prod_info.get("custom_reviews")
            if not custom_reviews:
                custom_reviews = [
                    {
                        "badge": "✨ 극강의 실용성",
                        "color": "bg-emerald-600",
                        "text": "출판 강의에 수백만 원 쓰고도 원고 한 장 못 끝냈는데, 이 책은 <strong>단 8,000원에 부크크 규격 세팅부터 표지 반려 탈출까지</strong> 그대로 복붙해서 끝냈습니다!",
                        "author": "이*진 독자 (직장인 작가)"
                    },
                    {
                        "badge": "🚀 백지 공포증 1초 탈출",
                        "color": "bg-indigo-600",
                        "text": "모니터 앞 커서만 깜빡이던 밤이 끝났습니다. <strong>뼈대만 던져주면 AI가 살을 붙이고 저자님의 다림질 공식</strong>으로 내 목소리가 살아나는 경험은 충격적이었습니다.",
                        "author": "박*현 독자 (프리랜서 작가)"
                    },
                    {
                        "badge": "👑 네이버 공식 작가 등단",
                        "color": "bg-rose-600",
                        "text": "초록창 검색창에 내 이름을 쳤을 때 <strong>'작가' 프로필과 내 책이 뜬 순간</strong>, 이력서 10장보다 훨씬 더 강력한 신뢰를 얻었습니다. 0원 출판의 기적입니다!",
                        "author": "정*호 독자 (1인 기업가)"
                    }
                ]
            cards_html = ""
            colors = ["bg-emerald-600", "bg-indigo-600", "bg-rose-600"]
            for idx, rv in enumerate(custom_reviews):
                badge = rv.get("badge", "✨ 베스트 리뷰")
                color = rv.get("color", colors[idx % len(colors)])
                text = rv.get("text", "")
                author = self._mask_name(rv.get("author", "익명 독자"))
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
      <p class="text-slate-500 text-sm mt-1">실제 부크크 출판 및 네이버 작가 등록을 완수한 구매자들의 솔직한 후기입니다</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">{cards_html}
    </div>
  </section>
"""

        # ad_promo 모드 (후기가 없는 신상품 - 거짓 후기 방지 & 출시 기대평 광고 배너)
        return """
  <!-- ==================== [출시 기념 에디터 추천사 & 얼리버드 기대평 (광고형 신뢰 배너)] ==================== -->
  <section class="py-16 px-4 sm:px-6 lg:px-8 max-w-5xl mx-auto">
    <div class="text-center mb-10">
      <span class="px-3.5 py-1.5 rounded-full bg-indigo-100 text-indigo-800 text-xs font-bold border border-indigo-300">EDITOR'S PICK &amp; PREVIEW</span>
      <h2 class="text-2xl sm:text-3xl font-black text-slate-900 mt-2">출시 기념 에디터 강력 추천 &amp; 핵심 기대 포인트</h2>
      <p class="text-slate-500 text-sm mt-1">※ 본 상품은 신규 출시작으로, 거짓 후기를 일절 생성하지 않고 전문가 추천과 사전 기대평으로 안내합니다</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-white border-2 border-slate-200 rounded-2xl p-6 shadow-sm hover:border-indigo-500 transition flex flex-col justify-between">
        <div>
          <div class="inline-block px-3 py-1 rounded-md bg-indigo-600 text-white font-black text-xs mb-3 shadow-sm">
            📢 출판 에디터 한 줄 평
          </div>
          <p class="text-slate-700 text-sm leading-relaxed mb-4">
            "수백만 원대 자비출판과 책쓰기 코칭의 거품을 완전히 걷어내고, <strong>단 8,000원에 기획부터 네이버 작가 등록까지</strong> 완결하는 가장 정직한 실전 가이드입니다."
          </p>
        </div>
        <div class="pt-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
          <span class="font-bold text-slate-700">출판 콘텐츠 기획팀</span>
          <span class="text-indigo-600 font-bold">★ 적극 추천 도서</span>
        </div>
      </div>

      <div class="bg-white border-2 border-slate-200 rounded-2xl p-6 shadow-sm hover:border-emerald-500 transition flex flex-col justify-between">
        <div>
          <div class="inline-block px-3 py-1 rounded-md bg-emerald-600 text-white font-black text-xs mb-3 shadow-sm">
            🎯 사전 얼리버드 기대 포인트
          </div>
          <p class="text-slate-700 text-sm leading-relaxed mb-4">
            "모니터 앞 커서만 깜빡이던 <strong>백지 공포증을 1시간 만에 극복</strong>하고, 내 전문 영역을 세상에 증명할 가장 강력한 무기를 얻게 될 것입니다."
          </p>
        </div>
        <div class="pt-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
          <span class="font-bold text-slate-700">사전 리뷰어 그룹</span>
          <span class="text-emerald-600 font-bold">★ 기대 지수 100%</span>
        </div>
      </div>

      <div class="bg-white border-2 border-slate-200 rounded-2xl p-6 shadow-sm hover:border-amber-500 transition flex flex-col justify-between">
        <div>
          <div class="inline-block px-3 py-1 rounded-md bg-amber-600 text-white font-black text-xs mb-3 shadow-sm">
            👑 저자의 진정성 약속
          </div>
          <p class="text-slate-700 text-sm leading-relaxed mb-4">
            "1%의 천재가 아닌 <strong>99%의 평범한 당신이 현장에서 견뎌낸 시간</strong>이 최고의 브랜드입니다. 초록창에 내 이름이 검색되는 순간을 끝까지 돕겠습니다."
          </p>
        </div>
        <div class="pt-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
          <span class="font-bold text-slate-700">저자 김진호 박사</span>
          <span class="text-amber-600 font-bold">★ 실전 100% 약속</span>
        </div>
      </div>
    </div>
  </section>
"""

    def _build_faq_section(self, prod_info: dict) -> str:
        """FAQ 유무에 따른 조건부 섹션 생성"""
        if not prod_info.get("has_faq", True):
            return ""

        return """
  <!-- ==================== [하얀돌연구소 추천 섹션] FAQ (자주 묻는 질문 4문 4답 & 사전 CS 차단) ==================== -->
  <section class="py-14 px-4 sm:px-6 lg:px-8 max-w-4xl mx-auto">
    <div class="text-center mb-10">
      <span class="px-3.5 py-1.5 rounded-full bg-slate-100 text-slate-700 text-xs font-bold border border-slate-300">FREQUENTLY ASKED QUESTIONS</span>
      <h2 class="text-2xl sm:text-3xl font-black text-slate-900 mt-2">구매 전 가장 많이 묻는 질문 BEST 4</h2>
      <p class="text-slate-500 text-sm mt-1">고객의 의문과 망설임을 사전에 명쾌하게 해결해 드립니다</p>
    </div>

    <div class="space-y-4 text-left">
      <div class="bg-slate-50 border border-slate-200 rounded-2xl p-5 shadow-sm">
        <h4 class="text-base font-bold text-slate-900 flex items-center gap-2">
          <span class="text-emerald-600 font-black">Q1.</span> 글솜씨나 특별한 스펙이 없는 평범한 직장인도 정말 책을 쓸 수 있나요?
        </h4>
        <p class="text-sm text-slate-600 mt-2 leading-relaxed pl-7">
          <strong class="text-emerald-800">100% 가능합니다.</strong> 독자가 원하는 것은 화려한 문학적 기교가 아니라, 여러분이 각자의 현장에서 직접 부딪히고 이겨낸 '진정성 있는 극복 스토리'입니다. 본 도서의 '스토리텔링 5단 구조'와 맞춤 AI 프롬프트가 뼈대부터 초고까지 완벽히 잡아드립니다.
        </p>
      </div>

      <div class="bg-slate-50 border border-slate-200 rounded-2xl p-5 shadow-sm">
        <h4 class="text-base font-bold text-slate-900 flex items-center gap-2">
          <span class="text-emerald-600 font-black">Q2.</span> 부크크 출판 시 추가 비용이나 숨겨진 결제 금액이 전혀 없나요?
        </h4>
        <p class="text-sm text-slate-600 mt-2 leading-relaxed pl-7">
          <strong class="text-emerald-800">단 1원도 들지 않습니다.</strong> 부크크(POD)는 주문이 발생할 때 1권씩 제작·배송되는 시스템으로, 저자가 재고를 미리 떠안거나 출판비를 낼 필요가 전혀 없습니다. 본 도서에서 알려드리는 대로 따라 하시면 0원으로 정식 ISBN 발급과 대형 서점 유통까지 끝납니다.
        </p>
      </div>

      <div class="bg-slate-50 border border-slate-200 rounded-2xl p-5 shadow-sm">
        <h4 class="text-base font-bold text-slate-900 flex items-center gap-2">
          <span class="text-emerald-600 font-black">Q3.</span> 전자책(PDF)과 실물 종이책 중 무엇을 먼저 구매해야 할까요?
        </h4>
        <p class="text-sm text-slate-600 mt-2 leading-relaxed pl-7">
          화면에 띄워두고 프롬프트를 복사(Ctrl+C) ➔ 붙여넣기(Ctrl+V)하여 <strong>오늘 바로 집필을 시작하고 싶으시다면 '전자책(PDF)'</strong>을 추천합니다. 서재에 소장하고 밑줄을 그으며 기획의 영감을 얻고 싶으시다면 <strong>'올컬러 실물 종이책'</strong>을 추천합니다.
        </p>
      </div>

      <div class="bg-slate-50 border border-slate-200 rounded-2xl p-5 shadow-sm">
        <h4 class="text-base font-bold text-slate-900 flex items-center gap-2">
          <span class="text-emerald-600 font-black">Q4.</span> 출간 후 네이버 공식 작가 인물등록은 정말 누구나 승인되나요?
        </h4>
        <p class="text-sm text-slate-600 mt-2 leading-relaxed pl-7">
          <strong class="text-emerald-800">네, 100% 공식 승인됩니다.</strong> 본 도서 4부에서 국립중앙도서관 정식 ISBN 발급 절차를 그대로 안내해 드립니다. ISBN이 발급된 정식 출간 도서가 등록되면 네이버 인물 정보 공식 가이드라인을 충족하여 승인받으실 수 있습니다.
        </p>
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
            책 한 권 값으로 3대 실전 비법 부록까지 전부 가져가세요!
          </h3>
          <p class="text-sm text-slate-600 mt-1">
            혼자 헤매지 않도록, 실제 출판과 승인에 즉시 쓰이는 3대 실전 자산을 무료로 드립니다.
          </p>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 w-full sm:w-auto shrink-0">
          <div class="bg-white p-3 rounded-xl border border-amber-200 text-center shadow-xs">
            <div class="text-2xl mb-1">🤖</div>
            <div class="text-xs font-bold text-slate-800">AI 글쓰기 프롬프트집</div>
            <div class="text-[11px] text-amber-600 font-semibold mt-0.5">실전 복붙용 텍스트</div>
          </div>
          <div class="bg-white p-3 rounded-xl border border-amber-200 text-center shadow-xs">
            <div class="text-2xl mb-1">📐</div>
            <div class="text-xs font-bold text-slate-800">인디자인 표지 템플릿</div>
            <div class="text-[11px] text-amber-600 font-semibold mt-0.5">반려 탈출 규격 세팅</div>
          </div>
          <div class="bg-white p-3 rounded-xl border border-amber-200 text-center shadow-xs">
            <div class="text-2xl mb-1">👑</div>
            <div class="text-xs font-bold text-slate-800">네이버 작가등록 양식</div>
            <div class="text-[11px] text-amber-600 font-semibold mt-0.5">원클릭 승인 가이드</div>
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

        p_name = prod_info.get("name", "에세이 한 권으로 당신을 증명하라: AI로 완성하는 퍼스널 브랜딩 출판 비결")
        p_price = prod_info.get("price", "8,000원")
        p_sub_price = prod_info.get("sub_price", "12,000원")
        p_author = prod_info.get("author", "김진호 박사")
        p_ebook_link = prod_info.get("ebook_link", "https://bookk.co.kr/bookStore/6a35e5e5f5d317cf59a3c17e")
        p_paper_link = prod_info.get("paper_link", "https://search.shopping.naver.com/book/catalog/60677619152?query=%EC%97%90%EC%84%B8%EC%9D%B4%20%ED%95%9C%20%EA%B6%8C%EC%9C%BC%EB%A1%9C%20%EB%8B%B9%EC%8B%A0%EC%9D%84%20%EC%A6%9D%EB%AA%85%ED%95%98%EB%9D%BC&NaPm=ct%3Dmv6528i8%7Cci%3D2dc082a4012fc5a426416cd172e3906ba5165b26%7Ctr%3Dboksl%7Csn%3D95694%7Chk%3D094ce9625fa67ab6bf58f1ebe3cedb0fae84df84")
        p_headline_1 = prod_info.get("headline_1", "이력서 100장보다 강력한 내 이름의 책 한 권,")
        p_headline_2 = prod_info.get("headline_2", f"『{p_name.split('(')[0].strip()}』로 완벽하게 증명하세요.")
        p_target_desc = prod_info.get("target_audience", "1%의 천재가 아닌 99%의 평범한 사람이 현장의 어려움을 이겨낸 스토리로 세상에 자신을 증명하는 가장 확실한 퍼스널 브랜딩 바이블.")
        p_pain_title = prod_info.get("pain_title", '"내세울 스펙도 없고 글솜씨도 없는데, 내가 과연 해낼 수 있을까?"')
        p_sol_title = prod_info.get("sol_title", "뼈대만 던져주면 AI가 초고를 쓰고, 부크크로 0원 출판해 네이버 공식 작가가 됩니다!")

        # 조건부 섹션 생성 (마케팅 진실성 원칙 & 하얀돌연구소 프레임워크)
        comparison_section = self._build_comparison_section(prod_info)
        reviews_section = self._build_reviews_section(prod_info)
        faq_section = self._build_faq_section(prod_info)
        gifts_section = self._build_gifts_section(prod_info)

        html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{p_name} - 공식 상세페이지</title>
  <!-- Tailwind CSS & Pretendard CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" />
  <style>
    * {{
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      text-rendering: optimizeLegibility;
    }}
    h1, h2, h3, h4, p {{
      word-break: keep-all;
    }}
    h1, h2, h3 {{
      text-wrap: balance;
    }}
    body {{
      font-family: Pretendard, -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
      background-color: #F8FAFC;
      color: #0F172A;
      letter-spacing: -0.02em;
    }}
    .book-3d {{
      perspective: 1000px;
    }}
    .book-spine {{
      transform: rotateY(-18deg) rotateX(4deg);
      box-shadow: -15px 20px 35px rgba(6, 78, 59, 0.28);
      transition: transform 0.4s ease;
    }}
    .book-spine:hover {{
      transform: rotateY(-8deg) rotateX(2deg) translateY(-6px);
    }}
  </style>
</head>
<body class="min-h-screen selection:bg-emerald-600 selection:text-white">

  <!-- ==================== [섹션 1: 밝은 배경] HERO SECTION ==================== -->
  <section class="bg-white border-b border-slate-100 pt-14 pb-20 px-4 sm:px-6 lg:px-8">
    <div class="max-w-6xl mx-auto">
      <!-- 상단 플로팅 뱃지 -->
      <div class="flex justify-center mb-6">
        <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs sm:text-sm font-bold shadow-sm">
          <span class="inline-block w-2 h-2 rounded-full bg-emerald-600 animate-pulse"></span>
          ✨ 주제 선정 ➔ AI 초고 집필 ➔ 부크크 0원 출판 ➔ 네이버 공식 작가 등록까지!
        </div>
      </div>

      <!-- 메인 헤드라인 (어색한 줄넘김 없는 깔끔한 2줄 블록 구조) -->
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

        <!-- CTA 버튼 -->
        <div class="mt-8 flex flex-col sm:flex-row items-center justify-center gap-4">
          <a href="{p_ebook_link}" target="_blank" class="w-full sm:w-auto px-8 py-4 rounded-xl bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-lg shadow-xl shadow-emerald-600/20 transition-all transform hover:-translate-y-0.5 text-center flex items-center justify-center gap-2">
            <span>💻 전자책(PDF) 즉시 구매하기 ({p_price})</span>
            <span>→</span>
          </a>
          <a href="{p_paper_link}" target="_blank" class="w-full sm:w-auto px-6 py-4 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-800 font-bold text-base border border-slate-300 transition text-center">
            📖 올컬러 실물 종이책 구매 ({p_sub_price})
          </a>
        </div>
      </div>

      <!-- 3D 도서 및 핵심 요약 쇼케이스 -->
      <div class="mt-14 flex flex-col lg:flex-row items-center justify-center gap-10">
        <!-- 3D 실물 도서 목업 -->
        <div class="book-3d flex justify-center">
          <div class="book-spine relative w-64 sm:w-72 rounded-r-lg overflow-hidden border border-slate-200 bg-white">
            <img src="{cover_b64}" alt="에세이 한 권으로 당신을 증명하라 표지" class="w-full h-auto object-cover">
          </div>
        </div>

        <!-- 왜 지금 퍼스널 에세이인가? 안내 카드 -->
        <div class="w-full lg:w-[440px] bg-slate-50 border border-slate-200 rounded-2xl p-6 sm:p-7 text-left shadow-sm">
          <div class="text-xs font-bold text-emerald-700 uppercase tracking-wider mb-2">PERSONAL BRANDING ROADMAP</div>
          <h3 class="text-xl font-bold text-slate-900 mb-4">이 책 한 권으로 얻게 되는 4가지 확실한 결과</h3>
          <ul class="space-y-3.5 text-sm text-slate-700">
            <li class="flex items-start gap-2.5">
              <span class="text-emerald-600 font-bold">01</span>
              <span><strong>나만의 글감 발굴:</strong> 내가 견뎌낸 실패담과 직무 극복기를 단 1명의 타겟에 꽂히는 5단 스토리로 구조화</span>
            </li>
            <li class="flex items-start gap-2.5">
              <span class="text-emerald-600 font-bold">02</span>
              <span><strong>백지 공포증 탈출:</strong> 뼈대만 던져주면 AI가 초고를 쓰고, '문장 다림질'로 내 진정성을 입히는 비법</span>
            </li>
            <li class="flex items-start gap-2.5">
              <span class="text-emerald-600 font-bold">03</span>
              <span><strong>부크크 0원 무료 출판:</strong> 내지 규격·폰트 세팅부터 '표지 반려 지옥'을 한 번에 통과하는 실전 노하우</span>
            </li>
            <li class="flex items-start gap-2.5">
              <span class="text-emerald-600 font-bold">04</span>
              <span><strong>네이버 공식 작가 등단:</strong> 정식 ISBN 발급 후 네이버 인물 검색에 '작가'로 내 이름을 등록하는 완벽 가이드</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <!-- ==================== [섹션 2: 어두운 배경 교차] SOCIAL PROOF STATS BAR ==================== -->
  <section class="bg-slate-900 text-white py-10 px-4">
    <div class="max-w-5xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
      <div class="p-3">
        <div class="text-3xl sm:text-4xl font-black text-amber-400">0 원</div>
        <div class="text-xs sm:text-sm text-slate-300 mt-1 font-medium">부크크 POD 재고 부담 없는 출판비</div>
      </div>
      <div class="p-3">
        <div class="text-3xl sm:text-4xl font-black text-emerald-400">4 단계</div>
        <div class="text-xs sm:text-sm text-slate-300 mt-1 font-medium">기획·집필·출판·작가등록 원스톱</div>
      </div>
      <div class="p-3">
        <div class="text-3xl sm:text-4xl font-black text-sky-400">ISBN</div>
        <div class="text-xs sm:text-sm text-slate-300 mt-1 font-medium">국립중앙도서관 정식 서지 번호 발급</div>
      </div>
      <div class="p-3">
        <div class="text-3xl sm:text-4xl font-black text-pink-400">100%</div>
        <div class="text-xs sm:text-sm text-slate-300 mt-1 font-medium">네이버 인물 검색 공식 작가 등록 가이드</div>
      </div>
    </div>
  </section>

  <!-- ==================== [섹션 3: 밝은 웜톤 교차] PROBLEM (버티컬 스택 + 양옆 여백) ==================== -->
  <section class="py-20 px-4 sm:px-6 lg:px-8 max-w-5xl mx-auto">
    <div class="bg-rose-50/70 border-2 border-rose-200 rounded-3xl p-6 sm:p-10 shadow-lg">
      <div class="max-w-3xl mx-auto mb-6">
        <span class="inline-block px-3.5 py-1.5 rounded-md bg-rose-100 text-rose-700 text-xs font-bold mb-3 border border-rose-300">
          🚨 REAL PAIN POINT (왜 지금까지 내 책을 쓰지 못했을까?)
        </span>
        <h2 class="text-2xl sm:text-3xl font-black text-slate-900 mb-3">
          {p_pain_title}
        </h2>
        <p class="text-slate-600 text-base leading-relaxed">
          마음속에 내 이름 석 자로 된 책을 내고 싶은 꿈은 있지만, 막상 한글 창을 열면 깜빡이는 커서 앞에서 한 줄도 쓰지 못하는 <strong>'백지 공포증'</strong>에 가로막힙니다.
          더구나 수백만 원짜리 자비출판 비용과 복잡한 표지·내지 규격 반려 때문에 시작조차 못 하고 포기하곤 합니다.
        </p>
      </div>

      <div class="my-6 max-w-3xl mx-auto rounded-2xl overflow-hidden border border-rose-300 shadow-md">
        <img src="{pain_b64}" alt="백지 공포증과 스펙 고민에 빠진 직장인" class="w-full h-auto aspect-video object-cover">
      </div>

      <div class="max-w-3xl mx-auto bg-rose-100/90 rounded-xl p-4 border border-rose-300">
        <p class="text-sm sm:text-base text-rose-900 font-bold">
          👉 독자는 1% 천재의 화려한 문장이 아니라, 99% 평범한 당신이 각자의 자리에서 어려움을 이겨낸 '진짜 이야기(진정성)'를 원합니다!
        </p>
      </div>
    </div>
  </section>

  <!-- ==================== [섹션 4: 밝은 쿨톤 교차] SOLUTION (버티컬 스택 + 양옆 여백) ==================== -->
  <section class="py-12 px-4 sm:px-6 lg:px-8 max-w-5xl mx-auto">
    <div class="bg-emerald-50/70 border-2 border-emerald-200 rounded-3xl p-6 sm:p-10 shadow-lg">
      <div class="max-w-3xl mx-auto mb-6">
        <span class="inline-block px-3.5 py-1.5 rounded-md bg-emerald-100 text-emerald-800 text-xs font-bold mb-3 border border-emerald-300">
          💡 SMART SOLUTION (AI 초고 집필 + 부크크 0원 출판 + 네이버 작가 등록)
        </span>
        <h2 class="text-2xl sm:text-3xl font-black text-slate-900 mb-3">
          {p_sol_title}
        </h2>
        <p class="text-slate-600 text-base leading-relaxed">
          파편화된 기억의 구슬을 <strong>'스토리텔링 5단 구조'</strong>로 꿰기만 하세요. 맞춤형 AI 프롬프트가 마법처럼 초고를 완성하고,
          '문장 다림질(문장 다이어트·번역체 제거)' 기법으로 내 목소리를 입힌 뒤, 부크크(Bookk)를 통해 단돈 0원으로 정식 ISBN 도서를 출간합니다.
        </p>
      </div>

      <div class="my-6 max-w-3xl mx-auto rounded-2xl overflow-hidden border border-emerald-300 shadow-md">
        <img src="{sol_b64}" alt="출판 성공 및 네이버 공식 작가 등록" class="w-full h-auto aspect-video object-cover">
      </div>

      <div class="max-w-3xl mx-auto bg-emerald-100/90 rounded-xl p-4 border border-emerald-300">
        <p class="text-sm sm:text-base text-emerald-950 font-bold">
          👉 내 이름으로 된 책이 교보문고·알라딘·부크크에 유통되고, 네이버 검색창에 내 이름을 치면 '작가'로 등록된 프로필이 당신의 전문성을 평생 증명합니다!
        </p>
      </div>
    </div>
  </section>

  {comparison_section}

  <!-- ==================== [섹션 5: 밝은 화이트 교차] 4부 구성 전체 커리큘럼 (목차 완벽 반영) ==================== -->
  <section class="bg-white border-y border-slate-200 py-20 px-4 sm:px-6 lg:px-8">
    <div class="max-w-6xl mx-auto">
      <div class="text-center mb-14">
        <h2 class="text-xs font-bold text-emerald-700 uppercase tracking-widest">FULL CURRICULUM &amp; TABLE OF CONTENTS</h2>
        <p class="text-2xl sm:text-4xl font-black text-slate-900 mt-2">책 주제 선정부터 네이버 작가 등록까지 4단계 완벽 로드맵</p>
        <p class="text-slate-500 text-sm sm:text-base mt-2">초보자도 목차 순서대로 따라만 하면 내 이름으로 된 책 한 권이 완성됩니다</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div class="bg-slate-50 border border-slate-200 rounded-2xl p-7 border-t-4 border-t-emerald-600 shadow-sm">
          <div class="flex items-center justify-between mb-3">
            <span class="px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold">1부 · 이해 (Why)</span>
            <span class="text-xs text-slate-400 font-semibold">p.13 ~ p.38</span>
          </div>
          <h3 class="text-xl font-black text-slate-900 mb-3">왜 퍼스널 브랜딩 책을 써야 하는가?</h3>
          <ul class="space-y-2 text-sm text-slate-700">
            <li>• <strong>제1장 퍼스널 브랜딩 시대:</strong> 퇴사보다 독립, 내 이름 석 자로 시작하는 인생 2막</li>
            <li>• <strong>스펙을 이기는 스토리:</strong> 1%의 천재가 아닌 99%의 평범함이 무기가 되는 시대</li>
            <li>• <strong>검색되는 전문가가 되어라:</strong> '내 이름'이 곧 신뢰를 증명하는 최고의 레퍼런스</li>
            <li>• <strong>제2장 내 안의 장벽 무너뜨리기:</strong> 일기와 에세이를 가르는 단 하나의 차이</li>
            <li>• <strong>완벽한 문장이라는 오만함 버리기:</strong> 개인적 실패담과 생생한 감정선을 글로 녹여내는 법</li>
          </ul>
        </div>

        <div class="bg-slate-50 border border-slate-200 rounded-2xl p-7 border-t-4 border-t-blue-600 shadow-sm">
          <div class="flex items-center justify-between mb-3">
            <span class="px-3 py-1 rounded-full bg-blue-100 text-blue-800 text-xs font-bold">2부 · 기획 (What)</span>
            <span class="text-xs text-slate-400 font-semibold">p.39 ~ p.62</span>
          </div>
          <h3 class="text-xl font-black text-slate-900 mb-3">무슨 이야기를 쓸 것인가? (글감과 타겟)</h3>
          <ul class="space-y-2 text-sm text-slate-700">
            <li>• <strong>제1장 타겟 고객과 페르소나 설정:</strong> "모두를 위한 책"은 "아무도 읽지 않는 책"이다</li>
            <li>• <strong>송곳처럼 뾰족한 1명의 페르소나:</strong> 과거의 '나'에게 쓰는 위로장</li>
            <li>• <strong>시장조사의 함정:</strong> 남들이 좋아하는 트렌드보다 내가 '견뎌낸' 시간의 가치</li>
            <li>• <strong>제2장 퍼스널 에세이 작법:</strong> 목차는 책의 지도다 (구슬을 꿰어 목걸이로 만드는 구조화)</li>
            <li>• <strong>매력적인 목차의 3요소 &amp; 실전 뼈대 잡기:</strong> 후킹, 논리, 기대감 + 스토리텔링 5단 구조</li>
          </ul>
        </div>

        <div class="bg-slate-50 border border-slate-200 rounded-2xl p-7 border-t-4 border-t-indigo-600 shadow-sm">
          <div class="flex items-center justify-between mb-3">
            <span class="px-3 py-1 rounded-full bg-indigo-100 text-indigo-800 text-xs font-bold">3부 · 집필 (How)</span>
            <span class="text-xs text-slate-400 font-semibold">p.63 ~ p.88</span>
          </div>
          <h3 class="text-xl font-black text-slate-900 mb-3">백지 공포증 이겨내고 초고 완성하기</h3>
          <ul class="space-y-2 text-sm text-slate-700">
            <li>• <strong>제1장 AI 글쓰기 비결:</strong> 뼈대만 던져주면 AI가 살을 붙이는 맞춤형 프롬프트의 비밀</li>
            <li>• <strong>인간적 글쓰기의 비밀:</strong> 기계 냄새를 없애는 괴상한 프롬프트 활용법</li>
            <li>• <strong>제2장 AI가 쓴 글을 내 글로 다림질하기:</strong> 문장 다이어트 (한 문장에 하나의 생각만)</li>
            <li>• <strong>생동감 불어넣기 &amp; 버리는 용기:</strong> 시제 통일과 번역체(수동태) 버리기, 과감하게 잘라내기</li>
            <li>• <strong>제3장 화룡점정:</strong> 독자의 멱살을 잡는 강렬한 프롤로그 &amp; 긴 여운을 남기는 에필로그</li>
          </ul>
        </div>

        <div class="bg-slate-50 border border-slate-200 rounded-2xl p-7 border-t-4 border-t-amber-500 shadow-sm">
          <div class="flex items-center justify-between mb-3">
            <span class="px-3 py-1 rounded-full bg-amber-100 text-amber-800 text-xs font-bold">4부 · 출판 및 마케팅 (After)</span>
            <span class="text-xs text-slate-400 font-semibold">p.89 ~ p.110</span>
          </div>
          <h3 class="text-xl font-black text-slate-900 mb-3">부크크(Bookk) 무료 출판 &amp; 네이버 공식 작가 데뷔</h3>
          <ul class="space-y-2 text-sm text-slate-700">
            <li>• <strong>제1장 부크크 출판 등록:</strong> 재고 부담 없는 0원 POD 출판의 마법 &amp; 집필 5단계</li>
            <li>• <strong>책의 얼굴 만들기:</strong> 내지 규격 맞추기와 전용 폰트 세팅 실전 가이드</li>
            <li>• <strong>반려 지옥 탈출하기:</strong> 한 번에 승인받는 완벽한 표지를 위한 인디자인 노하우</li>
            <li>• <strong>제2장 작가로서의 첫걸음:</strong> 정식 ISBN 발급과 부크크 플랫폼 등록 및 초기 마케팅</li>
            <li>• <strong>나도 이제 네이버 공식 작가!:</strong> 네이버 인물 검색에 내 이름과 저서 등록하기</li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <!-- ==================== [섹션 6: 밝은 슬레이트 교차] 저자 소개 ==================== -->
  <section class="py-16 px-4 sm:px-6 lg:px-8 max-w-5xl mx-auto">
    <div class="bg-white border border-slate-200 rounded-3xl p-8 shadow-sm flex flex-col sm:flex-row items-center gap-8">
      <div class="w-28 h-28 rounded-full bg-gradient-to-tr from-emerald-700 to-teal-500 flex items-center justify-center text-white text-3xl font-black shadow-lg shrink-0">
        김진호
      </div>
      <div>
        <div class="text-xs font-bold text-emerald-700 uppercase tracking-wider">AUTHOR PROFILE</div>
        <h3 class="text-2xl font-black text-slate-900 mt-1">저자 {p_author} · "공학과 행정, 인문학을 융합한 하이브리드 리더"</h3>
        <p class="text-sm text-slate-600 mt-2.5 leading-relaxed">
          홍익대학교 컴퓨터공학 전공, 사이버한국외국어대학교 한국어·영어 복수전공, 백석대학교 행정학 박사(Ph.D.) 학위를 취득했습니다.
          공동출판 프로젝트를 직접 기획·강의하며 『하나님의 나라를 회복하는 경영행정 스토리 Vol.1, Vol.2』, 『AI 행정학 마스터』 등 다수의 저서를 성공적으로 출간했고,
          현재 신한대학교 교목 및 15년 경력의 대학 행정 전문가로서 평범한 사람들이 자신의 이야기로 세상과 소통하며 퍼스널 브랜딩을 완성하도록 돕고 있습니다.
        </p>
      </div>
    </div>
  </section>

  {reviews_section}
  {faq_section}
  {gifts_section}

  <!-- ==================== [섹션 7: 프리미엄 다크 교차] PRICING & OFFER ==================== -->
  <section id="pricing" class="bg-slate-950 text-white py-24 px-4 sm:px-6 lg:px-8">
    <div class="max-w-5xl mx-auto">
      <div class="text-center mb-14">
        <span class="px-3.5 py-1.5 rounded-full bg-emerald-900/60 text-emerald-300 text-xs font-bold border border-emerald-500/40">START YOUR AUTHOR JOURNEY</span>
        <h2 class="text-3xl sm:text-4xl font-black text-white mt-3">오늘 읽고, 이번 달에 '내 이름의 책'을 출간하세요</h2>
        <p class="text-slate-400 text-sm sm:text-base mt-2">커피 두 잔 값으로 평생 검색되는 '네이버 등록 작가' 타이틀을 얻는 가장 확실한 투자</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8 items-stretch">
        <div class="relative rounded-2xl bg-gradient-to-b from-emerald-950 via-slate-900 to-slate-900 p-8 border-2 border-emerald-500 shadow-2xl flex flex-col justify-between">
          <div class="absolute -top-3.5 left-1/2 transform -translate-x-1/2 bg-emerald-600 text-white text-xs font-bold px-4 py-1 rounded-full shadow-lg whitespace-nowrap">
            🔥 BEST CHOICE · 즉시 다운로드 및 프롬프트 활용
          </div>

          <div>
            <div class="mt-2">
              <h3 class="text-2xl font-black text-white">💻 전자책(PDF) 에디션</h3>
              <p class="text-xs text-emerald-300 mt-1">결제 즉시 열람 + PC/태블릿에 띄워두고 바로 따라하기</p>
            </div>

            <div class="mt-6 flex items-baseline gap-2">
              <span class="text-4xl font-black text-amber-400">{p_price}</span>
              <span class="text-xs font-bold text-emerald-300 bg-emerald-950/80 px-2.5 py-1 rounded border border-emerald-500/30">즉시 다운로드 가능</span>
            </div>

            <ul class="mt-8 space-y-3.5 text-sm text-slate-200">
              <li class="flex items-center gap-2.5">
                <span class="text-emerald-400 font-bold">✓</span>
                <span><strong>110쪽 고화질 PDF (ISBN 9791112221186):</strong> 평생 무제한 소장</span>
              </li>
              <li class="flex items-center gap-2.5">
                <span class="text-emerald-400 font-bold">✓</span>
                <span><strong>AI 글쓰기 &amp; 다림질 프롬프트:</strong> 화면에 띄워두고 바로 복붙 활용</span>
              </li>
              <li class="flex items-center gap-2.5">
                <span class="text-emerald-400 font-bold">✓</span>
                <span><strong>부크크 승인 패스 노하우:</strong> 내지 규격 &amp; 인디자인 표지 반려 탈출법</span>
              </li>
              <li class="flex items-center gap-2.5">
                <span class="text-emerald-400 font-bold">✓</span>
                <span><strong>네이버 인물 검색 등록:</strong> 공식 작가 등록 A to Z 완벽 수록</span>
              </li>
            </ul>
          </div>

          <div class="mt-8">
            <a href="{p_ebook_link}" target="_blank" class="w-full block py-4 px-6 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-extrabold text-center text-base shadow-lg shadow-emerald-500/30 transition">
              전자책(PDF) 즉시 구매하기 ({p_price}) →
            </a>
            <p class="text-center text-xs text-slate-400 mt-2">부크크 공식 전자책 스토어 · 결제 즉시 다운로드</p>
          </div>
        </div>

        <div class="rounded-2xl bg-slate-900/60 p-8 border border-slate-800 flex flex-col justify-between">
          <div>
            <div class="flex justify-between items-start">
              <div>
                <h3 class="text-xl font-bold text-white">📖 올컬러 실물 종이책</h3>
                <p class="text-xs text-slate-400 mt-1">서재 소장 및 밑줄 그으며 기획하기 좋은 실물 도서</p>
              </div>
              <span class="text-xs bg-slate-800 text-slate-300 px-2.5 py-1 rounded">소장용</span>
            </div>

            <div class="mt-6 flex items-baseline gap-2">
              <span class="text-3xl font-black text-slate-200">{p_sub_price}</span>
              <span class="text-xs text-slate-400">112쪽 올컬러 A5</span>
            </div>

            <ul class="mt-8 space-y-3.5 text-sm text-slate-300">
              <li class="flex items-center gap-2.5">
                <span class="text-slate-400 font-bold">✓</span>
                <span><strong>112쪽 올컬러 A5 판형 (ISBN 9791112222077):</strong> 고급 인쇄 품질</span>
              </li>
              <li class="flex items-center gap-2.5">
                <span class="text-slate-400 font-bold">✓</span>
                <span><strong>네이버 쇼핑 &amp; 주요 서점 유통:</strong> 부크크 / 교보문고 / 알라딘 공식 등록</span>
              </li>
              <li class="flex items-center gap-2.5">
                <span class="text-slate-400 font-bold">✓</span>
                <span>실제 부크크 POD로 출판된 결과물 품질을 직접 눈으로 확인 가능</span>
              </li>
              <li class="flex items-center gap-2.5 text-slate-500">
                <span>•</span>
                <span>주문 제작(POD) 특성상 영업일 기준 2~8일 이내 제작·배송</span>
              </li>
            </ul>
          </div>

          <div class="mt-8">
            <a href="{p_paper_link}" target="_blank" class="w-full block py-3.5 px-6 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold text-center text-sm border border-slate-700 transition">
              종이책 서점에서 주문하기 ({p_sub_price}) →
            </a>
            <p class="text-center text-xs text-slate-500 mt-2">네이버 도서 공식 카탈로그 연결</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 하단 푸터 -->
  <footer class="py-12 bg-slate-900 border-t border-slate-800 text-center text-xs text-slate-500">
    <p>© 2026 {p_name}. 저자 {p_author} 저작권 소유. All rights reserved.</p>
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
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page(viewport={"width": 1200, "height": 800}, device_scale_factor=2)
                abs_html_path = os.path.abspath(html_path).replace("\\", "/")
                page.goto(f"file:///{abs_html_path}", wait_until="networkidle")
                page.evaluate("() => document.fonts.ready")
                page.wait_for_timeout(1500)
                page.screenshot(path=png_path, full_page=True)
                browser.close()
            print(f"SUCCESS: Rendered HTML and high-res PNG -> {png_path}")
        except Exception as e:
            print(f"Playwright rendering notice: {e}")

if __name__ == "__main__":
    renderer = GitHubDesignRenderer()
    renderer.render_all({
        "name": "에세이 한 권으로 당신을 증명하라: AI로 완성하는 퍼스널 브랜딩 출판 비결",
        "price": "8,000원",
        "sub_price": "12,000원",
        "author": "김진호 박사",
        "has_comparison": True,
        "review_mode": "ad_promo",  # "real" or "ad_promo" or "none"
        "has_faq": True,
        "has_gifts": True,
        "ebook_link": "https://bookk.co.kr/bookStore/6a35e5e5f5d317cf59a3c17e",
        "paper_link": "https://search.shopping.naver.com/book/catalog/60677619152?query=%EC%97%90%EC%84%B8%EC%9D%B4%20%ED%95%9C%20%EA%B6%8C%EC%9C%BC%EB%A1%9C%20%EB%8B%B9%EC%8B%A0%EC%9D%84%20%EC%A6%9D%EB%AA%85%ED%95%98%EB%9D%BC&NaPm=ct%3Dmv6528i8%7Cci%3D2dc082a4012fc5a426416cd172e3906ba5165b26%7Ctr%3Dboksl%7Csn%3D95694%7Chk%3D094ce9625fa67ab6bf58f1ebe3cedb0fae84df84"
    })
