"""
프로급 고전환 상세페이지 렌더러 (Pro Detail Page Renderer - Figma SVG)
대상 도서: 《에세이 한 권으로 당신을 증명하라: AI로 완성하는 퍼스널 브랜딩 출판 비결》 (김진호 지음)
사양:
1. 밝은/어두운 교차 배경 (Hero 화이트 -> Stats 다크 -> Problem 웜로즈 -> Solution 에메랄드 -> Curriculum 화이트 -> Offer 다크)
2. 16:9 가로형 이미지(840x470) 중앙 배치 + 양옆 200px 여유 여백
3. 이미지 위(헤드라인/설명) - 가운데 이미지 - 이미지 아래(핵심 요약 상자) 버티컬 스택
4. Desktop 1440px + Mobile 390px 듀얼 프레임 나란히 생성
5. 전자책(8,000원) 및 종이책(12,000원) 실제 판매 링크 연결
"""

import base64
import os

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

    def render_pro_canvas_svg(self, prod_info: dict) -> str:
        cover_b64 = self._get_b64(self.cover_path)
        pain_b64 = self._get_b64(self.pain_path)
        sol_b64 = self._get_b64(self.sol_path)

        p_name = prod_info.get("name", "에세이 한 권으로 당신을 증명하라")
        p_price = prod_info.get("price", "8,000원")
        p_sub_price = prod_info.get("sub_price", "12,000원")
        p_author = prod_info.get("author", "김진호 박사")
        p_ebook_link = prod_info.get("ebook_link", "https://bookk.co.kr/bookStore/6a35e5e5f5d317cf59a3c17e")
        p_paper_link = prod_info.get("paper_link", "https://search.shopping.naver.com/book/catalog/60677619152?query=%EC%97%90%EC%84%B8%EC%9D%B4%20%ED%95%9C%20%EA%B6%8C%EC%9C%BC%EB%A1%9C%20%EB%8B%B9%EC%8B%A0%EC%9D%84%20%EC%A6%9D%EB%AA%85%ED%95%98%EB%9D%BC&NaPm=ct%3Dmv6528i8%7Cci%3D2dc082a4012fc5a426416cd172e3906ba5165b26%7Ctr%3Dboksl%7Csn%3D95694%7Chk%3D094ce9625fa67ab6bf58f1ebe3cedb0fae84df84")

        svg = f'''<svg width="2000" height="4100" viewBox="0 0 2000 4100" fill="none" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
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

  <!-- ========================================================================= -->
  <!-- 🖥️ 1. 데스크톱 프레임 (Desktop 1440px) : x=0, y=0                         -->
  <!-- ========================================================================= -->
  <g id="Desktop_1440px">
    <rect x="0" y="0" width="1440" height="4100" fill="#F8FAFC"/>

    <!-- [섹션 1: 밝은 배경] HERO 섹션 (y=0 ~ y=540) -->
    <rect x="0" y="0" width="1440" height="540" fill="#FFFFFF"/>
    <g id="D_Hero" transform="translate(100, 60)">
      <!-- 뱃지 -->
      <rect x="0" y="0" width="440" height="36" rx="18" fill="#ECFDF5" stroke="#059669" stroke-width="1.5"/>
      <text x="18" y="23" fill="#065F46" font-family="Pretendard, sans-serif" font-size="13" font-weight="bold">✨ 주제 선정 ➔ AI 초고 집필 ➔ 부크크 0원 출판 ➔ 네이버 작가 등록</text>

      <!-- 타이틀 (깔끔한 2줄 블록) -->
      <text x="0" y="95" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="40" font-weight="900" letter-spacing="-1">이력서 100장보다 강력한 내 이름의 책 한 권,</text>
      <text x="0" y="150" fill="#047857" font-family="Pretendard, sans-serif" font-size="40" font-weight="900" letter-spacing="-1">AI로 쉽게 쓰고 네이버 공식 작가가 되세요.</text>
      
      <text x="0" y="200" fill="#475569" font-family="Pretendard, sans-serif" font-size="17" font-weight="500">
        99%의 평범한 사람이 각자의 전문 영역에서 어려움을 이겨낸 과정을 에세이로 출간하는 가장 확실한 로드맵
      </text>

      <!-- CTA 버튼 -->
      <a xlink:href="{p_ebook_link}" target="_blank">
        <rect x="0" y="245" width="370" height="60" rx="12" fill="#047857" filter="url(#softShadow)"/>
        <text x="45" y="282" fill="#FFFFFF" font-family="Pretendard, sans-serif" font-size="18" font-weight="bold">전자책(PDF) 즉시 구매 ({p_price}) →</text>
      </a>
      <text x="390" y="282" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="15" font-weight="bold">★ AI 초고 프롬프트 &amp; 표지 반려 탈출 비법 수록</text>

      <!-- 3D 도서 목업 -->
      <g id="D_3D_Book" transform="translate(860, -10)">
        <ellipse cx="180" cy="380" rx="180" ry="24" fill="#000000" opacity="0.25"/>
        <path d="M 30 20 L 60 0 L 60 360 L 30 380 Z" fill="#064E3B" stroke="#022C22"/>
        <rect x="60" y="0" width="260" height="360" rx="4" fill="#064E3B" stroke="#CBD5E1" stroke-width="2"/>
        <clipPath id="dBookCoverClip">
          <rect x="60" y="0" width="260" height="360" rx="4"/>
        </clipPath>
        <image xlink:href="{cover_b64}" x="60" y="0" width="260" height="360" clip-path="url(#dBookCoverClip)" preserveAspectRatio="xMidYMid slice"/>
        <path d="M 62 0 L 100 0 L 75 360 L 62 360 Z" fill="#FFFFFF" opacity="0.18"/>
      </g>
    </g>

    <!-- [섹션 2: 어두운 배경 교차] 소셜 프루프 다크 스트립 (y=540 ~ y=690) -->
    <rect x="0" y="540" width="1440" height="150" fill="#0F172A"/>
    <g id="D_Stats" transform="translate(100, 560)">
      <g transform="translate(60, 25)">
        <text x="0" y="32" fill="#FBBF24" font-family="Pretendard, sans-serif" font-size="34" font-weight="900">0 원</text>
        <text x="0" y="58" fill="#CBD5E1" font-family="Pretendard, sans-serif" font-size="14">부크크 재고 부담 없는 출판비</text>
      </g>
      <line x1="330" y1="15" x2="330" y2="85" stroke="#334155"/>
      <g transform="translate(400, 25)">
        <text x="0" y="32" fill="#34D399" font-family="Pretendard, sans-serif" font-size="34" font-weight="900">4 단계</text>
        <text x="0" y="58" fill="#CBD5E1" font-family="Pretendard, sans-serif" font-size="14">기획·AI집필·출판·작가등록</text>
      </g>
      <line x1="680" y1="15" x2="680" y2="85" stroke="#334155"/>
      <g transform="translate(750, 25)">
        <text x="0" y="32" fill="#38BDF8" font-family="Pretendard, sans-serif" font-size="34" font-weight="900">ISBN</text>
        <text x="0" y="58" fill="#CBD5E1" font-family="Pretendard, sans-serif" font-size="14">정식 국제표준도서번호 발급</text>
      </g>
      <line x1="1000" y1="15" x2="1000" y2="85" stroke="#334155"/>
      <g transform="translate(1040, 25)">
        <text x="0" y="32" fill="#F472B6" font-family="Pretendard, sans-serif" font-size="34" font-weight="900">100%</text>
        <text x="0" y="58" fill="#CBD5E1" font-family="Pretendard, sans-serif" font-size="14">네이버 공식 작가 등록 가이드</text>
      </g>
    </g>

    <!-- [섹션 3: 밝은 웜톤 교차] PROBLEM 섹션 (y=740 ~ y=1510) -->
    <!-- 버티컬 스택 + 양옆 200px 여백 16:9 와이드 이미지(840x472) -->
    <g id="D_Problem" transform="translate(100, 740)">
      <rect x="0" y="0" width="1240" height="770" rx="24" fill="#FFF1F2" stroke="#FECDD3" stroke-width="2" filter="url(#softShadow)"/>
      
      <!-- 상단 텍스트 -->
      <g transform="translate(200, 35)">
        <rect x="0" y="0" width="210" height="28" rx="6" fill="#FEE2E2"/>
        <text x="14" y="19" fill="#E11D48" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">🚨 REAL PAIN POINT (백지 공포증)</text>
        <text x="0" y="65" fill="#1E293B" font-family="Pretendard, sans-serif" font-size="28" font-weight="900">"내세울 스펙도 없고 글솜씨도 없는데, 내가 책을 쓸 수 있을까?"</text>
        <text x="0" y="98" fill="#475569" font-family="Pretendard, sans-serif" font-size="15">
          내 이름의 책을 내고 싶지만 하얀 커서 앞에서 한 줄도 못 쓰는 백지 공포증과 수백만 원 출판비 앞에서 포기하셨나요?
        </text>
      </g>

      <!-- 중앙 이미지: 양옆 200px 여백, 840x472 (16:9 와이드 가로형) -->
      <g transform="translate(200, 160)" filter="url(#imgShadow)">
        <clipPath id="dPainClip">
          <rect x="0" y="0" width="840" height="472" rx="16"/>
        </clipPath>
        <rect x="0" y="0" width="840" height="472" rx="16" fill="#E2E8F0"/>
        <image xlink:href="{pain_b64}" x="0" y="0" width="840" height="472" clip-path="url(#dPainClip)" preserveAspectRatio="xMidYMid slice"/>
        <rect x="0" y="0" width="840" height="472" rx="16" fill="none" stroke="#FDA4AF" stroke-width="1.5"/>
      </g>

      <!-- 하단 결론 상자 -->
      <g transform="translate(200, 660)">
        <rect x="0" y="0" width="840" height="65" rx="12" fill="#FFE4E6" stroke="#FECDD3" stroke-width="1"/>
        <text x="24" y="40" fill="#9F1239" font-family="Pretendard, sans-serif" font-size="16" font-weight="bold">
          👉 독자는 1% 천재의 완벽한 문장이 아니라, 99% 평범한 당신이 어려움을 이겨낸 '진짜 이야기'를 원합니다!
        </text>
      </g>
    </g>

    <!-- [섹션 4: 밝은 에메랄드 교차] SOLUTION 섹션 (y=1550 ~ y=2320) -->
    <!-- 버티컬 스택 + 양옆 200px 여백 16:9 와이드 이미지(840x472) -->
    <g id="D_Solution" transform="translate(100, 1550)">
      <rect x="0" y="0" width="1240" height="770" rx="24" fill="#ECFDF5" stroke="#A7F3D0" stroke-width="2" filter="url(#softShadow)"/>
      
      <!-- 상단 텍스트 -->
      <g transform="translate(200, 35)">
        <rect x="0" y="0" width="250" height="28" rx="6" fill="#D1FAE5"/>
        <text x="14" y="19" fill="#047857" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">💡 SMART SOLUTION (AI 집필 &amp; 0원 출판)</text>
        <text x="0" y="65" fill="#1E293B" font-family="Pretendard, sans-serif" font-size="28" font-weight="900">뼈대만 던져주면 AI가 초고를 쓰고, 부크크로 0원 출판합니다!</text>
        <text x="0" y="98" fill="#475569" font-family="Pretendard, sans-serif" font-size="15">
          스토리텔링 5단 구조로 목차를 잡고, AI 프롬프트와 '문장 다림질'로 초고를 완성해 부크크 정식 도서로 출간하세요.
        </text>
      </g>

      <!-- 중앙 이미지: 양옆 200px 여백, 840x472 (16:9 와이드 가로형) -->
      <g transform="translate(200, 160)" filter="url(#imgShadow)">
        <clipPath id="dSolClip">
          <rect x="0" y="0" width="840" height="472" rx="16"/>
        </clipPath>
        <rect x="0" y="0" width="840" height="472" rx="16" fill="#E2E8F0"/>
        <image xlink:href="{sol_b64}" x="0" y="0" width="840" height="472" clip-path="url(#dSolClip)" preserveAspectRatio="xMidYMid slice"/>
        <rect x="0" y="0" width="840" height="472" rx="16" fill="none" stroke="#6EE7B7" stroke-width="1.5"/>
      </g>

      <!-- 하단 결론 상자 -->
      <g transform="translate(200, 660)">
        <rect x="0" y="0" width="840" height="65" rx="12" fill="#D1FAE5" stroke="#A7F3D0" stroke-width="1"/>
        <text x="24" y="40" fill="#065F46" font-family="Pretendard, sans-serif" font-size="16" font-weight="bold">
          👉 정식 ISBN 발급부터 '네이버 인물 검색 공식 작가' 등록까지, 평생 검색되는 전문가 브랜드를 완성합니다!
        </text>
      </g>
    </g>

    <!-- [섹션 5: 화이트 배경 교차] 1부~4부 핵심 커리큘럼 로드맵 (y=2360 ~ y=2920) -->
    <rect x="0" y="2360" width="1440" height="560" fill="#FFFFFF"/>
    <g id="D_Curriculum" transform="translate(100, 2410)">
      <text x="620" y="30" text-anchor="middle" fill="#047857" font-family="Pretendard, sans-serif" font-size="13" font-weight="bold">4-STEP AUTHOR CURRICULUM</text>
      <text x="620" y="70" text-anchor="middle" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="32" font-weight="900">주제 선정부터 네이버 작가 등록까지 4부 구성 로드맵</text>

      <!-- 1부~4부 4개 카드 -->
      <g transform="translate(0, 110)">
        <rect x="0" y="0" width="290" height="320" rx="16" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1.5"/>
        <rect x="20" y="20" width="90" height="24" rx="12" fill="#D1FAE5"/>
        <text x="32" y="36" fill="#065F46" font-family="Pretendard, sans-serif" font-size="11" font-weight="bold">1부 · 이해(Why)</text>
        <text x="20" y="75" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="18" font-weight="900">왜 에세이를 써야 하는가</text>
        <text x="20" y="115" fill="#475569" font-family="Pretendard, sans-serif" font-size="13">• 내 이름 석 자로 시작하는 독립</text>
        <text x="20" y="145" fill="#475569" font-family="Pretendard, sans-serif" font-size="13">• 스펙을 이기는 99% 평범함의 무기</text>
        <text x="20" y="175" fill="#475569" font-family="Pretendard, sans-serif" font-size="13">• 일기와 에세이의 결정적 차이</text>
        <text x="20" y="205" fill="#475569" font-family="Pretendard, sans-serif" font-size="13">• 완벽한 문장이라는 오만함 버리기</text>
        <text x="20" y="235" fill="#475569" font-family="Pretendard, sans-serif" font-size="13">• 실패담과 감정선을 녹여내는 법</text>
      </g>

      <g transform="translate(316, 110)">
        <rect x="0" y="0" width="290" height="320" rx="16" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1.5"/>
        <rect x="20" y="20" width="95" height="24" rx="12" fill="#DBEAFE"/>
        <text x="32" y="36" fill="#1E40AF" font-family="Pretendard, sans-serif" font-size="11" font-weight="bold">2부 · 기획(What)</text>
        <text x="20" y="75" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="18" font-weight="900">글감 발굴과 목차 구조화</text>
        <text x="20" y="115" fill="#475569" font-family="Pretendard, sans-serif" font-size="13">• 송곳처럼 뾰족한 1명의 페르소나</text>
        <text x="20" y="145" fill="#475569" font-family="Pretendard, sans-serif" font-size="13">• 과거의 나에게 쓰는 위로장</text>
        <text x="20" y="175" fill="#475569" font-family="Pretendard, sans-serif" font-size="13">• 내가 견뎌낸 시간의 브랜드 가치</text>
        <text x="20" y="205" fill="#475569" font-family="Pretendard, sans-serif" font-size="13">• 매력적인 목차 3요소(후킹·논리)</text>
        <text x="20" y="235" fill="#475569" font-family="Pretendard, sans-serif" font-size="13">• [실전] 스토리텔링 5단 구조</text>
      </g>

      <g transform="translate(632, 110)">
        <rect x="0" y="0" width="290" height="320" rx="16" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1.5"/>
        <rect x="20" y="20" width="95" height="24" rx="12" fill="#E0E7FF"/>
        <text x="32" y="36" fill="#3730A3" font-family="Pretendard, sans-serif" font-size="11" font-weight="bold">3부 · 집필(How)</text>
        <text x="20" y="75" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="18" font-weight="900">AI 초고 집필 &amp; 다림질</text>
        <text x="20" y="115" fill="#475569" font-family="Pretendard, sans-serif" font-size="13">• 뼈대만 주면 살 붙이는 AI 프롬프트</text>
        <text x="20" y="145" fill="#475569" font-family="Pretendard, sans-serif" font-size="13">• 인간적 글쓰기 괴상한 프롬프트</text>
        <text x="20" y="175" fill="#475569" font-family="Pretendard, sans-serif" font-size="13">• AI 초고를 내 글로 다림질하기</text>
        <text x="20" y="205" fill="#475569" font-family="Pretendard, sans-serif" font-size="13">• 문장 다이어트 &amp; 번역체 버리기</text>
        <text x="20" y="235" fill="#475569" font-family="Pretendard, sans-serif" font-size="13">• 독자 멱살 잡는 프롤로그·에필로그</text>
      </g>

      <g transform="translate(948, 110)">
        <rect x="0" y="0" width="290" height="320" rx="16" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1.5"/>
        <rect x="20" y="20" width="110" height="24" rx="12" fill="#FEF3C7"/>
        <text x="30" y="36" fill="#92400E" font-family="Pretendard, sans-serif" font-size="11" font-weight="bold">4부 · 출판(After)</text>
        <text x="20" y="75" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="18" font-weight="900">부크크 출판 &amp; 작가 등록</text>
        <text x="20" y="115" fill="#475569" font-family="Pretendard, sans-serif" font-size="13">• 재고 부담 없는 0원 POD 출판</text>
        <text x="20" y="145" fill="#475569" font-family="Pretendard, sans-serif" font-size="13">• 내지 규격 맞추기 &amp; 전용 폰트 세팅</text>
        <text x="20" y="175" fill="#475569" font-family="Pretendard, sans-serif" font-size="13">• 반려 지옥 탈출 인디자인 표지 비법</text>
        <text x="20" y="205" fill="#475569" font-family="Pretendard, sans-serif" font-size="13">• 정식 ISBN 발급 &amp; 초기 마케팅</text>
        <text x="20" y="235" fill="#047857" font-family="Pretendard, sans-serif" font-size="13" font-weight="bold">★ 네이버 인물 검색 공식 작가 등록!</text>
      </g>
    </g>

    <!-- [섹션 6: 어두운 배경 교차] OFFER & PRICING 섹션 (y=2920 ~ y=4100) -->
    <rect x="0" y="2920" width="1440" height="1180" fill="#090D16"/>
    <g id="D_Offer" transform="translate(100, 3000)">
      <rect x="0" y="0" width="1240" height="460" rx="24" fill="#111827" stroke="#10B981" stroke-width="2" filter="url(#darkCardShadow)"/>
      
      <text x="620" y="65" text-anchor="middle" fill="#FFFFFF" font-family="Pretendard, sans-serif" font-size="32" font-weight="900">
        오늘 읽고, 이번 달에 내 이름이 찍힌 첫 책을 출간하세요
      </text>
      <text x="620" y="100" text-anchor="middle" fill="#94A3B8" font-family="Pretendard, sans-serif" font-size="16">
        커피 두 잔 값으로 평생 검색되는 '네이버 공식 등록 작가'가 되는 가장 확실한 지름길
      </text>

      <!-- 전자책 메인 카드 -->
      <g transform="translate(140, 140)">
        <rect x="0" y="0" width="440" height="260" rx="16" fill="#1E293B" stroke="#10B981" stroke-width="2"/>
        <rect x="24" y="20" width="160" height="24" rx="4" fill="#059669"/>
        <text x="34" y="37" fill="#FFFFFF" font-family="Pretendard, sans-serif" font-size="11" font-weight="bold">BEST CHOICE · 즉시 다운로드</text>
        <text x="24" y="80" fill="#FFFFFF" font-family="Pretendard, sans-serif" font-size="22" font-weight="bold">💻 전자책(PDF) 에디션</text>
        <text x="24" y="120" fill="#FBBF24" font-family="Pretendard, sans-serif" font-size="32" font-weight="900">{p_price}</text>
        <text x="24" y="156" fill="#CBD5E1" font-family="Pretendard, sans-serif" font-size="13">✓ 110쪽 PDF 즉시 열람 (ISBN 9791112221186)</text>
        <text x="24" y="180" fill="#CBD5E1" font-family="Pretendard, sans-serif" font-size="13">✓ AI 집필 프롬프트 &amp; 부크크 출판·네이버 작가등록</text>
        <a xlink:href="{p_ebook_link}" target="_blank">
          <rect x="24" y="200" width="392" height="42" rx="8" fill="#059669"/>
          <text x="135" y="227" fill="#FFFFFF" font-family="Pretendard, sans-serif" font-size="15" font-weight="bold">전자책 즉시 구매하기 ({p_price}) →</text>
        </a>
      </g>

      <!-- 종이책 서브 카드 -->
      <g transform="translate(660, 140)">
        <rect x="0" y="0" width="440" height="260" rx="16" fill="#0F172A" stroke="#334155" stroke-width="1.5"/>
        <text x="24" y="45" fill="#94A3B8" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">실물 소장용 옵션</text>
        <text x="24" y="80" fill="#FFFFFF" font-family="Pretendard, sans-serif" font-size="22" font-weight="bold">📖 올컬러 실물 종이책</text>
        <text x="24" y="120" fill="#F1F5F9" font-family="Pretendard, sans-serif" font-size="32" font-weight="900">{p_sub_price}</text>
        <text x="24" y="156" fill="#94A3B8" font-family="Pretendard, sans-serif" font-size="13">✓ 112쪽 올컬러 A5 판형 (ISBN 9791112222077)</text>
        <text x="24" y="180" fill="#94A3B8" font-family="Pretendard, sans-serif" font-size="13">✓ 네이버 도서 / 부크크 / 교보문고 / 알라딘 유통</text>
        <a xlink:href="{p_paper_link}" target="_blank">
          <rect x="24" y="200" width="392" height="42" rx="8" fill="#334155"/>
          <text x="145" y="227" fill="#CBD5E1" font-family="Pretendard, sans-serif" font-size="15" font-weight="bold">종이책 서점 주문하기 ({p_sub_price})</text>
        </a>
      </g>
    </g>
  </g>

  <!-- ========================================================================= -->
  <!-- 📱 2. 모바일 프레임 (Mobile 390px) : x=1540, y=0                          -->
  <!-- ========================================================================= -->
  <g id="Mobile_390px" transform="translate(1540, 0)">
    <rect x="0" y="0" width="390" height="4100" fill="#F8FAFC"/>

    <!-- M1. [밝은 배경] HERO -->
    <rect x="0" y="0" width="390" height="540" fill="#FFFFFF"/>
    <g id="M_Hero" transform="translate(20, 30)">
      <rect x="0" y="0" width="310" height="28" rx="14" fill="#ECFDF5" stroke="#059669"/>
      <text x="12" y="18" fill="#065F46" font-family="Pretendard, sans-serif" font-size="10" font-weight="bold">✨ AI 에세이 집필 ➔ 부크크 0원 출판 ➔ 네이버 작가</text>

      <text x="0" y="60" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="23" font-weight="900">에세이 한 권으로 당신을 증명하라</text>
      <text x="0" y="92" fill="#047857" font-family="Pretendard, sans-serif" font-size="22" font-weight="900">AI로 쓰고 네이버 공식 작가 데뷔!</text>
      
      <text x="0" y="122" fill="#475569" font-family="Pretendard, sans-serif" font-size="12">
        김진호 박사의 퍼스널 브랜딩 0원 출판 실전 비결
      </text>

      <!-- 3D 도서 목업 -->
      <g transform="translate(75, 145)">
        <ellipse cx="100" cy="270" rx="90" ry="16" fill="#000000" opacity="0.2"/>
        <rect x="20" y="0" width="160" height="250" rx="4" fill="#064E3B" stroke="#CBD5E1" stroke-width="1.5"/>
        <clipPath id="mBookCoverClip">
          <rect x="20" y="0" width="160" height="250" rx="4"/>
        </clipPath>
        <image xlink:href="{cover_b64}" x="20" y="0" width="160" height="250" clip-path="url(#mBookCoverClip)" preserveAspectRatio="xMidYMid slice"/>
      </g>

      <!-- CTA 버튼 -->
      <a xlink:href="{p_ebook_link}" target="_blank">
        <rect x="0" y="445" width="350" height="52" rx="12" fill="#047857"/>
        <text x="45" y="477" fill="#FFFFFF" font-family="Pretendard, sans-serif" font-size="16" font-weight="bold">전자책 즉시 구매하기 ({p_price}) →</text>
      </a>
    </g>

    <!-- M2. [어두운 배경 교차] 소셜 프루프 -->
    <rect x="0" y="540" width="390" height="170" fill="#0F172A"/>
    <g id="M_Stats" transform="translate(20, 555)">
      <g transform="translate(20, 20)">
        <text x="0" y="24" fill="#FBBF24" font-family="Pretendard, sans-serif" font-size="22" font-weight="900">0 원</text>
        <text x="0" y="44" fill="#CBD5E1" font-family="Pretendard, sans-serif" font-size="11">부크크 무료 출판</text>
      </g>
      <g transform="translate(190, 20)">
        <text x="0" y="24" fill="#34D399" font-family="Pretendard, sans-serif" font-size="22" font-weight="900">4 단계</text>
        <text x="0" y="44" fill="#CBD5E1" font-family="Pretendard, sans-serif" font-size="11">기획·집필·출판·등록</text>
      </g>
      <g transform="translate(20, 85)">
        <text x="0" y="24" fill="#38BDF8" font-family="Pretendard, sans-serif" font-size="22" font-weight="900">ISBN</text>
        <text x="0" y="44" fill="#CBD5E1" font-family="Pretendard, sans-serif" font-size="11">정식 도서 번호 발급</text>
      </g>
      <g transform="translate(190, 85)">
        <text x="0" y="24" fill="#F472B6" font-family="Pretendard, sans-serif" font-size="22" font-weight="900">100%</text>
        <text x="0" y="44" fill="#CBD5E1" font-family="Pretendard, sans-serif" font-size="11">네이버 인물등록 비법</text>
      </g>
    </g>

    <!-- M3. [모바일 PROBLEM - 균형 있는 여백] -->
    <g id="M_Problem" transform="translate(20, 740)">
      <rect x="0" y="0" width="350" height="490" rx="16" fill="#FFF1F2" stroke="#FECDD3" stroke-width="1.5"/>
      
      <rect x="15" y="18" width="130" height="22" rx="4" fill="#FEE2E2"/>
      <text x="24" y="33" fill="#E11D48" font-family="Pretendard, sans-serif" font-size="10" font-weight="bold">🚨 REAL PAIN POINT</text>
      
      <text x="15" y="65" fill="#1E293B" font-family="Pretendard, sans-serif" font-size="17" font-weight="900">백지 공포증에 막히셨나요?</text>
      <text x="15" y="88" fill="#475569" font-family="Pretendard, sans-serif" font-size="12">
        스펙과 글재주가 없어 첫 문장조차 못 쓰던 날들
      </text>

      <!-- 모바일 이미지: 310x180 와이드 가로형 중앙 배치 -->
      <g transform="translate(20, 110)">
        <clipPath id="mPainClip">
          <rect x="0" y="0" width="310" height="190" rx="10"/>
        </clipPath>
        <image xlink:href="{pain_b64}" x="0" y="0" width="310" height="190" clip-path="url(#mPainClip)" preserveAspectRatio="xMidYMid slice"/>
        <rect x="0" y="0" width="310" height="190" rx="10" fill="none" stroke="#FDA4AF" stroke-width="1"/>
      </g>

      <!-- 하단 결론 -->
      <g transform="translate(20, 315)">
        <rect x="0" y="0" width="310" height="50" rx="8" fill="#FFE4E6"/>
        <text x="10" y="30" fill="#9F1239" font-family="Pretendard, sans-serif" font-size="11" font-weight="bold">👉 독자는 화려한 문장보다 당신의 진정성을 원합니다.</text>
      </g>
    </g>

    <!-- M4. [모바일 SOLUTION - 균형 있는 여백] -->
    <g id="M_Solution" transform="translate(20, 1260)">
      <rect x="0" y="0" width="350" height="490" rx="16" fill="#ECFDF5" stroke="#A7F3D0" stroke-width="1.5"/>
      
      <rect x="15" y="18" width="140" height="22" rx="4" fill="#D1FAE5"/>
      <text x="24" y="33" fill="#047857" font-family="Pretendard, sans-serif" font-size="10" font-weight="bold">💡 SMART SOLUTION</text>
      
      <text x="15" y="65" fill="#1E293B" font-family="Pretendard, sans-serif" font-size="17" font-weight="900">AI 집필 + 부크크 0원 출판</text>
      <text x="15" y="88" fill="#475569" font-family="Pretendard, sans-serif" font-size="12">
        뼈대만 잡으면 AI가 초고를 쓰고 네이버 작가가 됩니다!
      </text>

      <!-- 모바일 이미지: 310x180 와이드 가로형 중앙 배치 -->
      <g transform="translate(20, 110)">
        <clipPath id="mSolClip">
          <rect x="0" y="0" width="310" height="190" rx="10"/>
        </clipPath>
        <image xlink:href="{sol_b64}" x="0" y="0" width="310" height="190" clip-path="url(#mSolClip)" preserveAspectRatio="xMidYMid slice"/>
        <rect x="0" y="0" width="310" height="190" rx="10" fill="none" stroke="#6EE7B7" stroke-width="1"/>
      </g>

      <!-- 하단 결론 -->
      <g transform="translate(20, 315)">
        <rect x="0" y="0" width="310" height="50" rx="8" fill="#D1FAE5"/>
        <text x="10" y="30" fill="#065F46" font-family="Pretendard, sans-serif" font-size="11" font-weight="bold">👉 ISBN 발급 후 네이버 인물 검색에 작가로 등단하세요!</text>
      </g>
    </g>

    <!-- M5. [어두운 배경 교차] 모바일 OFFER & PRICING -->
    <rect x="0" y="1780" width="390" height="2320" fill="#090D16"/>
    <g id="M_Offer" transform="translate(20, 1810)">
      <rect x="0" y="0" width="350" height="250" rx="16" fill="#1E293B" stroke="#10B981" stroke-width="2"/>
      <rect x="15" y="15" width="130" height="22" rx="4" fill="#059669"/>
      <text x="22" y="30" fill="#FFFFFF" font-family="Pretendard, sans-serif" font-size="10" font-weight="bold">BEST CHOICE · 즉시 열람</text>
      <text x="15" y="68" fill="#FFFFFF" font-family="Pretendard, sans-serif" font-size="18" font-weight="bold">💻 전자책(PDF) 에디션</text>
      <text x="15" y="105" fill="#FBBF24" font-family="Pretendard, sans-serif" font-size="28" font-weight="900">{p_price}</text>
      <text x="15" y="132" fill="#E2E8F0" font-family="Pretendard, sans-serif" font-size="12">✓ 110쪽 PDF 즉시 다운로드 &amp; 평생 소장</text>
      <text x="15" y="152" fill="#E2E8F0" font-family="Pretendard, sans-serif" font-size="12">✓ 부크크 0원 출판 &amp; 네이버 작가 등록 가이드</text>
      <a xlink:href="{p_ebook_link}" target="_blank">
        <rect x="15" y="180" width="320" height="46" rx="8" fill="#059669"/>
        <text x="85" y="209" fill="#FFFFFF" font-family="Pretendard, sans-serif" font-size="14" font-weight="bold">전자책 즉시 구매하기 ({p_price}) →</text>
      </a>
    </g>
  </g>
</svg>'''
        return svg

if __name__ == "__main__":
    renderer = ProDetailRenderer()
    svg = renderer.render_pro_canvas_svg({
        "name": "에세이 한 권으로 당신을 증명하라: AI로 완성하는 퍼스널 브랜딩 출판 비결",
        "price": "8,000원",
        "sub_price": "12,000원",
        "author": "김진호 박사",
        "ebook_link": "https://bookk.co.kr/bookStore/6a35e5e5f5d317cf59a3c17e",
        "paper_link": "https://search.shopping.naver.com/book/catalog/60677619152?query=%EC%97%90%EC%84%B8%EC%9D%B4%20%ED%95%9C%20%EA%B6%8C%EC%9C%BC%EB%A1%9C%20%EB%8B%B9%EC%8B%A0%EC%9D%84%20%EC%A6%9D%EB%AA%85%ED%95%98%EB%9D%BC&NaPm=ct%3Dmv6528i8%7Cci%3D2dc082a4012fc5a426416cd172e3906ba5165b26%7Ctr%3Dboksl%7Csn%3D95694%7Chk%3D094ce9625fa67ab6bf58f1ebe3cedb0fae84df84"
    })
    with open("figma_canvas_design.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("PRO_DESIGN_SVG_GENERATED_SUCCESSFULLY")
