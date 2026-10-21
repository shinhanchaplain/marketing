"""
프로급 고전환 상세페이지 렌더러 (Pro Detail Page Renderer - Figma SVG v5.0)
- 어떤 상품(스마트스토어/일반 커머스/도서)이든 prod_info를 100% 동적으로 반영하여 Desktop 1440px + Mobile 390px 듀얼 프레임 SVG 생성
- 상품 이미지를 자르지 않고(preserveAspectRatio="xMidYMid meet") 원본 비율 그대로 보존
"""

import base64
import os
import html


class ProDetailRenderer:
    def __init__(self):
        self.cover_path = "product_images/book_cover.jpg"
        self.pain_path = "product_images/scene_pain_point.jpg"
        self.sol_path = "product_images/scene_solution.jpg"

    def _get_b64(self, path):
        if os.path.exists(path):
            with open(path, "rb") as f:
                return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode("utf-8")
        return ""

    def _esc(self, text: str) -> str:
        return html.escape(str(text or ""))

    def render_pro_canvas_svg(self, prod_info: dict) -> str:
        p_name = prod_info.get("name", "프리미엄 인기 상품")
        p_name_short = p_name.split("(")[0].strip()[:26]
        is_essay_preset = ("에세이 한 권으로 당신을 증명하라" in p_name)

        if is_essay_preset:
            cover_b64 = prod_info.get("cover_b64") or self._get_b64(self.cover_path)
            pain_b64 = prod_info.get("pain_b64") or self._get_b64(self.pain_path)
            sol_b64 = prod_info.get("sol_b64") or self._get_b64(self.sol_path)
        else:
            cover_b64 = prod_info.get("cover_b64") or ""
            pain_b64 = prod_info.get("pain_b64") or cover_b64
            sol_b64 = prod_info.get("sol_b64") or cover_b64

        p_price = self._esc(prod_info.get("price", "8,900원"))
        p_sub_price = self._esc(prod_info.get("sub_price", ""))
        p_author = self._esc(prod_info.get("author", "공식 스토어"))
        p_ebook_link = self._esc(prod_info.get("ebook_link", "#"))
        p_paper_link = self._esc(prod_info.get("paper_link", p_ebook_link))

        h1 = self._esc((prod_info.get("headline_1") or "한 번 경험하면 다시 찾게 되는 검증된 퀄리티,")[:34])
        h2 = self._esc((prod_info.get("headline_2") or f"『{p_name_short}』로 완벽하게 해결하세요!")[:34])
        target_desc = self._esc((prod_info.get("target_audience") or f"『{p_name_short}』만의 검증된 품질과 알찬 구성을 만나보세요.")[:68])
        pain_title = self._esc((prod_info.get("pain_title") or '"비슷해 보이는 수많은 상품들, 어떤 걸 골라야 실패가 없을까요?"')[:42])
        pain_desc = self._esc((prod_info.get("pain_desc") or "아쉬운 품질이나 번거로운 과정 때문에 고민하셨다면 검증된 선택이 필요합니다.")[:70])
        sol_title = self._esc((prod_info.get("sol_title") or f"실제 구매자 리뷰와 품질로 증명된 『{p_name_short}』만의 비결!")[:42])
        sol_desc = self._esc((prod_info.get("sol_desc") or target_desc)[:70])

        metrics = prod_info.get("metrics") or [
            {"val": p_price, "label": "공식 판매 가격"},
            {"val": "100%", "label": "원본 비율 이미지 보존"},
            {"val": "BEST", "label": "엄선된 핵심 구성"},
            {"val": "★ 4.9+", "label": "구매 고객 실사용 만족도"},
        ]
        while len(metrics) < 4:
            metrics.append({"val": "★ 5.0", "label": "공식 품질 보증"})

        bento = prod_info.get("bento_items") or [
            {"step": "POINT 01", "title": f"『{p_name_short}』 핵심 품질", "desc": "엄선된 원료와 공정으로 완성한 독보적 퀄리티"},
            {"step": "POINT 02", "title": "누구나 간편한 올인원 구성", "desc": "복잡한 준비 과정 없이 바로 즐기는 알찬 패키지"},
            {"step": "POINT 03", "title": "실구매 고객 극찬 만족도", "desc": "높은 평점과 재구매율이 증명하는 실패 없는 선택"},
            {"step": "POINT 04", "title": f"단 {p_price} 합리적 가치", "desc": "유통 거품을 줄여 가격 대비 최고의 만족감 제공"},
        ]
        while len(bento) < 4:
            bento.append({"step": f"POINT 0{len(bento)+1}", "title": "핵심 특장점", "desc": "검증된 품질 제공"})

        svg = f'''<svg width="2000" height="3900" viewBox="0 0 2000 3900" fill="none" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <filter id="softShadow" x="-10" y="-10" width="120%" height="120%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="12" stdDeviation="20" flood-color="#0F172A" flood-opacity="0.12"/>
    </filter>
    <filter id="darkCardShadow" x="-10" y="-10" width="120%" height="120%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="16" stdDeviation="24" flood-color="#000000" flood-opacity="0.4"/>
    </filter>
    <filter id="imgShadow" x="-10" y="-10" width="120%" height="120%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="8" stdDeviation="16" flood-color="#0F172A" flood-opacity="0.15"/>
    </filter>
  </defs>

  <!-- 🖥️ 1. 데스크톱 프레임 (Desktop 1440px) -->
  <g id="Desktop_1440px">
    <rect x="0" y="0" width="1440" height="3900" fill="#F8FAFC"/>

    <!-- [섹션 1: HERO] -->
    <rect x="0" y="0" width="1440" height="540" fill="#FFFFFF"/>
    <g id="D_Hero" transform="translate(100, 60)">
      <rect x="0" y="0" width="420" height="36" rx="18" fill="#ECFDF5" stroke="#059669" stroke-width="1.5"/>
      <text x="18" y="23" fill="#065F46" font-family="Pretendard, sans-serif" font-size="13" font-weight="bold">✨ {p_author} 공식 스토어 · 검증된 핵심 품질</text>

      <text x="0" y="95" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="36" font-weight="900">{h1}</text>
      <text x="0" y="148" fill="#047857" font-family="Pretendard, sans-serif" font-size="36" font-weight="900">{h2}</text>
      <text x="0" y="198" fill="#475569" font-family="Pretendard, sans-serif" font-size="16" font-weight="500">{target_desc}</text>

      <a xlink:href="{p_ebook_link}" target="_blank">
        <rect x="0" y="245" width="380" height="60" rx="12" fill="#047857" filter="url(#softShadow)"/>
        <text x="38" y="282" fill="#FFFFFF" font-family="Pretendard, sans-serif" font-size="18" font-weight="bold">🚀 지금 바로 구매하기 ({p_price}) →</text>
      </a>

      <!-- 대표 이미지 (자르지 않고 원본 비율 그대로 meet 표시) -->
      <g id="D_Product_Hero_Img" transform="translate(830, -10)">
        <rect x="0" y="0" width="380" height="380" rx="20" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="2" filter="url(#softShadow)"/>
        <image xlink:href="{cover_b64}" x="14" y="14" width="352" height="352" preserveAspectRatio="xMidYMid meet"/>
      </g>
    </g>

    <!-- [섹션 2: STATS BAR] -->
    <rect x="0" y="540" width="1440" height="150" fill="#0F172A"/>
    <g id="D_Stats" transform="translate(100, 560)">
      <g transform="translate(60, 25)">
        <text x="0" y="32" fill="#FBBF24" font-family="Pretendard, sans-serif" font-size="32" font-weight="900">{self._esc(metrics[0].get('val',''))}</text>
        <text x="0" y="58" fill="#CBD5E1" font-family="Pretendard, sans-serif" font-size="14">{self._esc(metrics[0].get('label',''))}</text>
      </g>
      <line x1="330" y1="15" x2="330" y2="85" stroke="#334155"/>
      <g transform="translate(400, 25)">
        <text x="0" y="32" fill="#34D399" font-family="Pretendard, sans-serif" font-size="32" font-weight="900">{self._esc(metrics[1].get('val',''))}</text>
        <text x="0" y="58" fill="#CBD5E1" font-family="Pretendard, sans-serif" font-size="14">{self._esc(metrics[1].get('label',''))}</text>
      </g>
      <line x1="680" y1="15" x2="680" y2="85" stroke="#334155"/>
      <g transform="translate(750, 25)">
        <text x="0" y="32" fill="#38BDF8" font-family="Pretendard, sans-serif" font-size="32" font-weight="900">{self._esc(metrics[2].get('val',''))}</text>
        <text x="0" y="58" fill="#CBD5E1" font-family="Pretendard, sans-serif" font-size="14">{self._esc(metrics[2].get('label',''))}</text>
      </g>
      <line x1="1000" y1="15" x2="1000" y2="85" stroke="#334155"/>
      <g transform="translate(1040, 25)">
        <text x="0" y="32" fill="#F472B6" font-family="Pretendard, sans-serif" font-size="32" font-weight="900">{self._esc(metrics[3].get('val',''))}</text>
        <text x="0" y="58" fill="#CBD5E1" font-family="Pretendard, sans-serif" font-size="14">{self._esc(metrics[3].get('label',''))}</text>
      </g>
    </g>

    <!-- [섹션 3: PROBLEM (원본 이미지 비율 유지)] -->
    <g id="D_Problem" transform="translate(100, 740)">
      <rect x="0" y="0" width="1240" height="770" rx="24" fill="#FFF1F2" stroke="#FECDD3" stroke-width="2" filter="url(#softShadow)"/>
      <g transform="translate(200, 35)">
        <rect x="0" y="0" width="230" height="28" rx="6" fill="#FEE2E2"/>
        <text x="14" y="19" fill="#E11D48" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">🚨 WHY THIS MATTERS</text>
        <text x="0" y="65" fill="#1E293B" font-family="Pretendard, sans-serif" font-size="25" font-weight="900">{pain_title}</text>
        <text x="0" y="98" fill="#475569" font-family="Pretendard, sans-serif" font-size="14">{pain_desc}</text>
      </g>
      <g transform="translate(200, 160)" filter="url(#imgShadow)">
        <rect x="0" y="0" width="840" height="472" rx="16" fill="#FFFFFF" stroke="#FDA4AF" stroke-width="1.5"/>
        <image xlink:href="{pain_b64}" x="12" y="12" width="816" height="448" preserveAspectRatio="xMidYMid meet"/>
      </g>
      <g transform="translate(200, 660)">
        <rect x="0" y="0" width="840" height="65" rx="12" fill="#FFE4E6" stroke="#FECDD3" stroke-width="1"/>
        <text x="24" y="40" fill="#9F1239" font-family="Pretendard, sans-serif" font-size="15" font-weight="bold">👉 실패 없는 선택을 위해 품질과 실제 후기가 검증된 『{self._esc(p_name_short)}』를 만나보세요!</text>
      </g>
    </g>

    <!-- [섹션 4: SOLUTION (원본 이미지 비율 유지)] -->
    <g id="D_Solution" transform="translate(100, 1550)">
      <rect x="0" y="0" width="1240" height="770" rx="24" fill="#ECFDF5" stroke="#A7F3D0" stroke-width="2" filter="url(#softShadow)"/>
      <g transform="translate(200, 35)">
        <rect x="0" y="0" width="250" height="28" rx="6" fill="#D1FAE5"/>
        <text x="14" y="19" fill="#047857" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">💡 BEST CHOICE &amp; SOLUTION</text>
        <text x="0" y="65" fill="#1E293B" font-family="Pretendard, sans-serif" font-size="25" font-weight="900">{sol_title}</text>
        <text x="0" y="98" fill="#475569" font-family="Pretendard, sans-serif" font-size="14">{sol_desc}</text>
      </g>
      <g transform="translate(200, 160)" filter="url(#imgShadow)">
        <rect x="0" y="0" width="840" height="472" rx="16" fill="#FFFFFF" stroke="#6EE7B7" stroke-width="1.5"/>
        <image xlink:href="{sol_b64}" x="12" y="12" width="816" height="448" preserveAspectRatio="xMidYMid meet"/>
      </g>
      <g transform="translate(200, 660)">
        <rect x="0" y="0" width="840" height="65" rx="12" fill="#D1FAE5" stroke="#A7F3D0" stroke-width="1"/>
        <text x="24" y="40" fill="#065F46" font-family="Pretendard, sans-serif" font-size="15" font-weight="bold">👉 『{self._esc(p_name_short)}』 하나면 복잡한 과정 없이 누구나 간편하게 최고의 만족을 누립니다!</text>
      </g>
    </g>

    <!-- [섹션 5: 4대 핵심 포인트] -->
    <rect x="0" y="2360" width="1440" height="520" fill="#FFFFFF"/>
    <g id="D_Features" transform="translate(100, 2410)">
      <text x="620" y="30" text-anchor="middle" fill="#047857" font-family="Pretendard, sans-serif" font-size="13" font-weight="bold">CORE PRODUCT HIGHLIGHTS</text>
      <text x="620" y="70" text-anchor="middle" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="32" font-weight="900">『{self._esc(p_name_short)}』 4대 핵심 매력 포인트</text>

      <g transform="translate(0, 110)">
        <rect x="0" y="0" width="290" height="260" rx="16" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1.5"/>
        <text x="20" y="40" fill="#065F46" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">{self._esc(bento[0].get('step','POINT 01'))}</text>
        <text x="20" y="80" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="17" font-weight="900">{self._esc(bento[0].get('title','')[:16])}</text>
        <text x="20" y="120" fill="#475569" font-family="Pretendard, sans-serif" font-size="13">{self._esc(bento[0].get('desc','')[:22])}</text>
        <text x="20" y="145" fill="#475569" font-family="Pretendard, sans-serif" font-size="13">{self._esc(bento[0].get('desc','')[22:44])}</text>
      </g>
      <g transform="translate(316, 110)">
        <rect x="0" y="0" width="290" height="260" rx="16" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1.5"/>
        <text x="20" y="40" fill="#1E40AF" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">{self._esc(bento[1].get('step','POINT 02'))}</text>
        <text x="20" y="80" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="17" font-weight="900">{self._esc(bento[1].get('title','')[:16])}</text>
        <text x="20" y="120" fill="#475569" font-family="Pretendard, sans-serif" font-size="13">{self._esc(bento[1].get('desc','')[:22])}</text>
        <text x="20" y="145" fill="#475569" font-family="Pretendard, sans-serif" font-size="13">{self._esc(bento[1].get('desc','')[22:44])}</text>
      </g>
      <g transform="translate(632, 110)">
        <rect x="0" y="0" width="290" height="260" rx="16" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1.5"/>
        <text x="20" y="40" fill="#3730A3" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">{self._esc(bento[2].get('step','POINT 03'))}</text>
        <text x="20" y="80" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="17" font-weight="900">{self._esc(bento[2].get('title','')[:16])}</text>
        <text x="20" y="120" fill="#475569" font-family="Pretendard, sans-serif" font-size="13">{self._esc(bento[2].get('desc','')[:22])}</text>
        <text x="20" y="145" fill="#475569" font-family="Pretendard, sans-serif" font-size="13">{self._esc(bento[2].get('desc','')[22:44])}</text>
      </g>
      <g transform="translate(948, 110)">
        <rect x="0" y="0" width="290" height="260" rx="16" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1.5"/>
        <text x="20" y="40" fill="#92400E" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">{self._esc(bento[3].get('step','POINT 04'))}</text>
        <text x="20" y="80" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="17" font-weight="900">{self._esc(bento[3].get('title','')[:16])}</text>
        <text x="20" y="120" fill="#475569" font-family="Pretendard, sans-serif" font-size="13">{self._esc(bento[3].get('desc','')[:22])}</text>
        <text x="20" y="145" fill="#475569" font-family="Pretendard, sans-serif" font-size="13">{self._esc(bento[3].get('desc','')[22:44])}</text>
      </g>
    </g>

    <!-- [섹션 6: OFFER & PRICING] -->
    <rect x="0" y="2880" width="1440" height="1020" fill="#090D16"/>
    <g id="D_Offer" transform="translate(100, 2960)">
      <rect x="0" y="0" width="1240" height="420" rx="24" fill="#111827" stroke="#10B981" stroke-width="2" filter="url(#darkCardShadow)"/>
      <text x="620" y="65" text-anchor="middle" fill="#FFFFFF" font-family="Pretendard, sans-serif" font-size="32" font-weight="900">지금 바로 『{self._esc(p_name_short)}』를 시작하세요!</text>
      <text x="620" y="100" text-anchor="middle" fill="#94A3B8" font-family="Pretendard, sans-serif" font-size="16">{target_desc}</text>

      <g transform="translate(340, 135)">
        <rect x="0" y="0" width="560" height="230" rx="16" fill="#1E293B" stroke="#10B981" stroke-width="2"/>
        <text x="280" y="55" text-anchor="middle" fill="#FFFFFF" font-family="Pretendard, sans-serif" font-size="22" font-weight="bold">{self._esc(p_name_short)}</text>
        <text x="280" y="110" text-anchor="middle" fill="#FBBF24" font-family="Pretendard, sans-serif" font-size="38" font-weight="900">{p_price}</text>
        <a xlink:href="{p_ebook_link}" target="_blank">
          <rect x="40" y="145" width="480" height="52" rx="10" fill="#059669"/>
          <text x="280" y="178" text-anchor="middle" fill="#FFFFFF" font-family="Pretendard, sans-serif" font-size="17" font-weight="bold">🚀 공식 스토어에서 즉시 구매하기 ({p_price}) →</text>
        </a>
      </g>
    </g>
  </g>

  <!-- 📱 2. 모바일 프레임 (Mobile 390px) -->
  <g id="Mobile_390px" transform="translate(1540, 0)">
    <rect x="0" y="0" width="390" height="3900" fill="#F8FAFC"/>
    <rect x="0" y="0" width="390" height="540" fill="#FFFFFF"/>
    <g id="M_Hero" transform="translate(20, 30)">
      <rect x="0" y="0" width="310" height="28" rx="14" fill="#ECFDF5" stroke="#059669"/>
      <text x="12" y="18" fill="#065F46" font-family="Pretendard, sans-serif" font-size="10" font-weight="bold">✨ {p_author} 공식 스토어</text>
      <text x="0" y="60" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="20" font-weight="900">{self._esc(p_name_short[:18])}</text>
      <text x="0" y="90" fill="#047857" font-family="Pretendard, sans-serif" font-size="17" font-weight="900">검증된 품질 · 실구매 만족도</text>
      <g transform="translate(45, 120)">
        <rect x="0" y="0" width="260" height="260" rx="16" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
        <image xlink:href="{cover_b64}" x="10" y="10" width="240" height="240" preserveAspectRatio="xMidYMid meet"/>
      </g>
      <a xlink:href="{p_ebook_link}" target="_blank">
        <rect x="0" y="420" width="350" height="52" rx="12" fill="#047857"/>
        <text x="175" y="452" text-anchor="middle" fill="#FFFFFF" font-family="Pretendard, sans-serif" font-size="15" font-weight="bold">🚀 즉시 구매하기 ({p_price}) →</text>
      </a>
    </g>
  </g>
</svg>'''
        return svg
