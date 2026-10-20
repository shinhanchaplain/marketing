import base64
import subprocess
import os

# 세 이미지 파일 로드 및 Base64 인코딩
cover_p = "product_images/book_cover.jpg"
pain_p = "product_images/scene_pain_point.jpg"
sol_p = "product_images/scene_solution.jpg"

with open(cover_p, "rb") as f:
    cover_b64 = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode("utf-8")

with open(pain_p, "rb") as f:
    pain_b64 = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode("utf-8")

with open(sol_p, "rb") as f:
    sol_b64 = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode("utf-8")

# 이미지가 실제 내장된 SVG 코드 작성
svg_code = f'''<svg width="1950" height="1520" viewBox="0 0 1950 1520" fill="none" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <!-- DESKTOP 1440px FRAME -->
  <g id="Desktop_1440px">
    <rect x="0" y="0" width="1440" height="1480" rx="16" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="2"/>
    <text x="60" y="55" fill="#475569" font-family="Pretendard, Inter, sans-serif" font-size="16" font-weight="bold">[『AI 행정학 마스터』 고전환 비주얼 상세페이지 - Desktop 1440px]</text>
    
    <!-- 01 HERO (실제 책 표지 포함) -->
    <rect x="60" y="80" width="1320" height="320" rx="12" fill="#FFFFFF" stroke="#2563EB" stroke-width="2.5"/>
    <rect x="90" y="105" width="280" height="26" rx="6" fill="#2563EB"/>
    <text x="100" y="123" fill="#FFFFFF" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">⚡ 구매 즉시 다운로드 · 평생 소장 PDF</text>
    <text x="90" y="165" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="26" font-weight="bold">배송 기다리지 마세요. 결제 3초 후 칼퇴 시작.</text>
    <text x="90" y="195" fill="#475569" font-family="Pretendard, sans-serif" font-size="15">『AI 행정학 마스터』 | 김진호 저 | 듀얼 모니터 복붙 실습 최적화</text>
    <rect x="90" y="225" width="310" height="46" rx="8" fill="#2563EB"/>
    <text x="125" y="254" fill="#FFFFFF" font-family="Pretendard, sans-serif" font-size="16" font-weight="bold">전자책(PDF) 즉시 다운로드 (13,000원) →</text>
    <text x="90" y="295" fill="#15803D" font-family="Pretendard, sans-serif" font-size="13" font-weight="bold">★ 실전 행정 프롬프트 템플릿집 100% 무료 증정</text>
    <text x="90" y="325" fill="#64748B" font-family="Pretendard, sans-serif" font-size="12">(종이책 소장을 원하시면 17,460원에 주문 가능)</text>
    
    <!-- 실제 도서 표지 이미지 삽입 -->
    <clipPath id="clipCover">
      <rect x="1060" y="95" width="200" height="290" rx="8"/>
    </clipPath>
    <rect x="1056" y="91" width="208" height="298" rx="10" fill="#E2E8F0"/>
    <image xlink:href="{cover_b64}" x="1060" y="95" width="200" height="290" clip-path="url(#clipCover)" preserveAspectRatio="xMidYMid slice"/>

    <!-- 02 PROBLEM (AI 생성 고객 고통 야근 컷 포함) -->
    <rect x="60" y="420" width="1320" height="260" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
    <rect x="90" y="445" width="140" height="24" rx="6" fill="#FEE2E2"/>
    <text x="100" y="462" fill="#991B1B" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">02. PROBLEM</text>
    <text x="90" y="505" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="22" font-weight="bold">책 보며 일일이 타이핑하지 마세요. 오타 나면 끝입니다.</text>
    <text x="90" y="538" fill="#475569" font-family="Pretendard, sans-serif" font-size="15">기존 IT 책은 파이썬 문법만 늘어놓아 포기하게 만듭니다.</text>
    <text x="90" y="565" fill="#475569" font-family="Pretendard, sans-serif" font-size="15">행정인에게 필요한 건 모니터 옆에 띄우고 바로 복사해 쓰는 실전 프롬프트입니다.</text>
    
    <!-- AI 야근 고통 이미지 삽입 -->
    <clipPath id="clipPain">
      <rect x="980" y="435" width="310" height="230" rx="8"/>
    </clipPath>
    <image xlink:href="{pain_b64}" x="980" y="435" width="310" height="230" clip-path="url(#clipPain)" preserveAspectRatio="xMidYMid slice"/>

    <!-- 03 BENEFIT & SOLUTION (AI 생성 듀얼 모니터 해결 컷 포함) -->
    <rect x="60" y="700" width="1320" height="270" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
    <rect x="90" y="725" width="140" height="24" rx="6" fill="#DCFCE7"/>
    <text x="100" y="742" fill="#166534" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">03. SOLUTION &amp; BENEFIT</text>
    <text x="90" y="785" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="22" font-weight="bold">듀얼 모니터 분할 화면 최적화: 1초 검색, 1초 복사, 10초 칼퇴.</text>
    <text x="90" y="818" fill="#475569" font-family="Pretendard, sans-serif" font-size="15">한쪽엔 PDF 전자책, 한쪽엔 업무 창을 띄우고 프롬프트를 복붙하면,</text>
    <text x="90" y="845" fill="#475569" font-family="Pretendard, sans-serif" font-size="15">하루 4시간 걸리던 서류 취합과 데이터 정리가 즉시 초자동화됩니다.</text>
    
    <!-- AI 듀얼 모니터 해결 이미지 삽입 -->
    <clipPath id="clipSol">
      <rect x="980" y="715" width="310" height="235" rx="8"/>
    </clipPath>
    <image xlink:href="{sol_b64}" x="980" y="715" width="310" height="235" clip-path="url(#clipSol)" preserveAspectRatio="xMidYMid slice"/>

    <!-- 04 PROOF (신뢰도) -->
    <rect x="60" y="990" width="1320" height="150" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
    <rect x="90" y="1015" width="130" height="24" rx="6" fill="#FEF3C7"/>
    <text x="100" y="1032" fill="#92400E" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">04. PROOF</text>
    <text x="90" y="1070" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="22" font-weight="bold">15년 대학교 현장 행정 전문가 김진호 박사의 검증된 실전 바이블</text>
    <text x="90" y="1100" fill="#475569" font-family="Pretendard, sans-serif" font-size="15">홍익대 컴공 논리 + 행정학 박사 | 신한대학교 도서관 입수 | 네이버 도서·교보·알라딘 공식 유통</text>

    <!-- 05 SPECIAL OFFER -->
    <rect x="60" y="1160" width="1320" height="260" rx="12" fill="#EFF6FF" stroke="#2563EB" stroke-width="2"/>
    <rect x="90" y="1185" width="220" height="24" rx="6" fill="#DBEAFE"/>
    <text x="100" y="1202" fill="#1E40AF" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">05. SPECIAL OFFER</text>
    <text x="90" y="1245" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="24" font-weight="bold">『AI 행정학 마스터』 전자책 특별 패키지 (13,000원)</text>
    <text x="90" y="1280" fill="#475569" font-family="Pretendard, sans-serif" font-size="15">결제 즉시 평생 소장 PDF 다운로드 + 실무 프롬프트 예제집 100% 무료 증정</text>
    <rect x="90" y="1310" width="280" height="48" rx="8" fill="#2563EB"/>
    <text x="135" y="1340" fill="#FFFFFF" font-family="Pretendard, sans-serif" font-size="16" font-weight="bold">전자책 즉시 다운로드받기 →</text>
  </g>

  <!-- MOBILE 390px FRAME -->
  <g id="Mobile_390px" transform="translate(1510, 0)">
    <rect x="0" y="0" width="390" height="1480" rx="28" fill="#FFFFFF" stroke="#0F172A" stroke-width="4"/>
    <text x="30" y="45" fill="#64748B" font-family="Pretendard, sans-serif" font-size="13" font-weight="bold">[Mobile 390px - 이미지 포함]</text>
    
    <!-- M HERO -->
    <rect x="20" y="65" width="350" height="360" rx="12" fill="#EFF6FF" stroke="#2563EB" stroke-width="1.5"/>
    <text x="35" y="95" fill="#1E40AF" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">⚡ 결제 즉시 다운로드</text>
    <text x="35" y="125" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="18" font-weight="bold">배송 없이 오늘 바로 칼퇴</text>
    
    <!-- 모바일 책 표지 -->
    <clipPath id="clipCoverM">
      <rect x="125" y="140" width="140" height="200" rx="6"/>
    </clipPath>
    <image xlink:href="{cover_b64}" x="125" y="140" width="140" height="200" clip-path="url(#clipCoverM)" preserveAspectRatio="xMidYMid slice"/>

    <rect x="35" y="360" width="320" height="42" rx="8" fill="#2563EB"/>
    <text x="100" y="387" fill="#FFFFFF" font-family="Pretendard, sans-serif" font-size="14" font-weight="bold">전자책 다운로드 (13,000원)</text>

    <!-- M PROBLEM (야근 이미지) -->
    <rect x="20" y="445" width="350" height="320" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
    <text x="35" y="475" fill="#991B1B" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">02. PROBLEM</text>
    <text x="35" y="505" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="16" font-weight="bold">손으로 코드 치지 마세요</text>
    <clipPath id="clipPainM">
      <rect x="35" y="520" width="320" height="220" rx="8"/>
    </clipPath>
    <image xlink:href="{pain_b64}" x="35" y="520" width="320" height="220" clip-path="url(#clipPainM)" preserveAspectRatio="xMidYMid slice"/>

    <!-- M SOLUTION (해결 이미지) -->
    <rect x="20" y="785" width="350" height="330" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
    <text x="35" y="815" fill="#166534" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">03. SOLUTION</text>
    <text x="35" y="845" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="16" font-weight="bold">듀얼 모니터 복붙 1초</text>
    <clipPath id="clipSolM">
      <rect x="35" y="860" width="320" height="230" rx="8"/>
    </clipPath>
    <image xlink:href="{sol_b64}" x="35" y="860" width="320" height="230" clip-path="url(#clipSolM)" preserveAspectRatio="xMidYMid slice"/>
  </g>
</svg>'''

with open("figma_canvas_design.svg", "w", encoding="utf-8") as f:
    f.write(svg_code)

proc = subprocess.Popen(['powershell', '-Command', 'Set-Clipboard'], stdin=subprocess.PIPE, text=True, encoding='utf-8')
proc.communicate(input=svg_code)
print("EMBEDDED_IMAGES_SVG_SUCCESSFULLY_INJECTED_TO_CLIPBOARD")
