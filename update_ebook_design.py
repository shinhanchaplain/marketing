import subprocess

svg_code = '''<svg width="1950" height="1420" viewBox="0 0 1950 1420" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- DESKTOP 1440px FRAME -->
  <g id="Desktop_1440px">
    <rect x="0" y="0" width="1440" height="1380" rx="16" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="2"/>
    <text x="60" y="55" fill="#475569" font-family="Pretendard, Inter, sans-serif" font-size="16" font-weight="bold">[도서 상세페이지 &amp; 랜딩페이지 - Desktop 1440px (종이책 + 전자책)]</text>
    
    <!-- 01 HERO -->
    <rect x="60" y="80" width="1320" height="240" rx="12" fill="#FFFFFF" stroke="#2563EB" stroke-width="2"/>
    <rect x="90" y="105" width="280" height="26" rx="6" fill="#DBEAFE"/>
    <text x="100" y="123" fill="#1E40AF" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">01. HERO | 공무원·교직원·행정 실무자 필독서</text>
    <text x="90" y="170" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="28" font-weight="bold">매일 쏟아지는 엑셀과 서류 작업, 언제까지 손으로 하시겠습니까?</text>
    <text x="90" y="205" fill="#475569" font-family="Pretendard, sans-serif" font-size="16">『AI 행정학 마스터: 바이브 코딩으로 완성하는 초자동화 워크플로우』 | 김진호 저</text>
    
    <!-- 듀얼 오퍼 배지 -->
    <rect x="90" y="235" width="190" height="46" rx="8" fill="#2563EB"/>
    <text x="125" y="264" fill="#FFFFFF" font-family="Pretendard, sans-serif" font-size="15" font-weight="bold">📖 종이책 17,460원</text>
    <rect x="295" y="235" width="220" height="46" rx="8" fill="#0F172A"/>
    <text x="325" y="264" fill="#FFFFFF" font-family="Pretendard, sans-serif" font-size="15" font-weight="bold">💻 전자책(PDF) 13,000원</text>
    <text x="535" y="264" fill="#15803D" font-family="Pretendard, sans-serif" font-size="14" font-weight="bold">★ 실전 예제 프롬프트 100% 무료 증정</text>

    <!-- 02 PROBLEM -->
    <rect x="60" y="340" width="1320" height="160" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
    <rect x="90" y="360" width="140" height="24" rx="6" fill="#FEE2E2"/>
    <text x="100" y="377" fill="#991B1B" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">02. PROBLEM</text>
    <text x="90" y="420" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="22" font-weight="bold">코딩 공부하지 마세요. 행정 업무는 '바이브 코딩'으로 끝납니다.</text>
    <text x="90" y="453" fill="#475569" font-family="Pretendard, sans-serif" font-size="15">기존 IT 책은 파이썬만 늘어놓다 포기하게 만듭니다. 행정 실무에는 일상의 자연어로 시스템을 움직이는 실전 워크플로우가 필요합니다.</text>

    <!-- 03 BENEFIT -->
    <rect x="60" y="520" width="1320" height="170" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
    <rect x="90" y="540" width="130" height="24" rx="6" fill="#DCFCE7"/>
    <text x="100" y="557" fill="#166534" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">03. BENEFIT</text>
    <text x="90" y="600" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="22" font-weight="bold">하루 4시간 걸리던 취합 서류 업무가 단 10초 만에 끝납니다.</text>
    <text x="90" y="633" fill="#475569" font-family="Pretendard, sans-serif" font-size="15">종이책으로 원리를 정독하고, 전자책(PDF)으로 프롬프트를 듀얼 모니터에서 복사·붙여넣기(Ctrl+C, V)하여 오늘 즉시 칼퇴근하세요.</text>

    <!-- 04 PROOF -->
    <rect x="60" y="710" width="1320" height="160" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
    <rect x="90" y="730" width="130" height="24" rx="6" fill="#FEF3C7"/>
    <text x="100" y="747" fill="#92400E" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">04. PROOF</text>
    <text x="90" y="790" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="22" font-weight="bold">15년 대학교 현장 행정 전문가 김진호 박사의 검증된 노하우</text>
    <text x="90" y="823" fill="#475569" font-family="Pretendard, sans-serif" font-size="15">홍익대 컴공의 시스템 논리 + 백석대 경영·행정학 박사(Ph.D.) | 신한대학교 중앙도서관 입수 | 네이버 도서·교보·알라딘 공식 유통</text>

    <!-- 05 DUAL OFFER & CTA -->
    <rect x="60" y="890" width="1320" height="290" rx="12" fill="#EFF6FF" stroke="#2563EB" stroke-width="2"/>
    <rect x="90" y="915" width="220" height="24" rx="6" fill="#DBEAFE"/>
    <text x="100" y="932" fill="#1E40AF" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">05. DUAL OFFER (맞춤 선택)</text>
    <text x="90" y="980" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="26" font-weight="bold">나에게 맞는 형태로 선택하세요 (종이책 vs 전자책)</text>
    
    <!-- 옵션 1 종이책 -->
    <rect x="90" y="1010" width="480" height="130" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
    <text x="110" y="1040" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="18" font-weight="bold">📖 종이책 (소장 및 정독용)</text>
    <text x="110" y="1068" fill="#475569" font-family="Pretendard, sans-serif" font-size="14">180쪽 올컬러 A4 변형 실습 판형 (210*297mm)</text>
    <text x="110" y="1100" fill="#2563EB" font-family="Pretendard, sans-serif" font-size="20" font-weight="bold">17,460원 <tspan fill="#64748B" font-size="13">(정가 18,000원)</tspan></text>

    <!-- 옵션 2 전자책 -->
    <rect x="600" y="1010" width="480" height="130" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
    <text x="620" y="1040" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="18" font-weight="bold">💻 전자책 eBook (실무 즉시 복붙용)</text>
    <text x="620" y="1068" fill="#475569" font-family="Pretendard, sans-serif" font-size="14">구매 즉시 PDF 다운로드 + 프롬프트 복사집 포함</text>
    <text x="620" y="1100" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="20" font-weight="bold">13,000원 <tspan fill="#166534" font-size="13">(즉시 열람)</tspan></text>
  </g>

  <!-- MOBILE 390px FRAME -->
  <g id="Mobile_390px" transform="translate(1510, 0)">
    <rect x="0" y="0" width="390" height="1380" rx="28" fill="#FFFFFF" stroke="#0F172A" stroke-width="4"/>
    <text x="30" y="45" fill="#64748B" font-family="Pretendard, sans-serif" font-size="13" font-weight="bold">[Mobile 390px - 세로 흐름]</text>
    
    <!-- M HERO -->
    <rect x="20" y="65" width="350" height="260" rx="12" fill="#EFF6FF" stroke="#2563EB" stroke-width="1.5"/>
    <text x="35" y="95" fill="#1E40AF" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">01. HERO</text>
    <text x="35" y="130" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="20" font-weight="bold">서류 업무, 이제 AI로 칼퇴</text>
    <text x="35" y="160" fill="#475569" font-family="Pretendard, sans-serif" font-size="13">바이브 코딩으로 완성하는 초자동화</text>
    <text x="35" y="185" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="15" font-weight="bold">종이책 17,460원 | 전자책 13,000원</text>
    <rect x="35" y="205" width="320" height="42" rx="8" fill="#2563EB"/>
    <text x="125" y="232" fill="#FFFFFF" font-family="Pretendard, sans-serif" font-size="14" font-weight="bold">도서 구매하러 가기</text>
    <text x="35" y="270" fill="#166534" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">★ 프롬프트 예제집 100% 증정</text>

    <!-- M PROBLEM -->
    <rect x="20" y="345" width="350" height="150" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
    <text x="35" y="375" fill="#991B1B" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">02. PROBLEM</text>
    <text x="35" y="410" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="16" font-weight="bold">코딩 몰라도 가능합니다</text>
    <text x="35" y="440" fill="#475569" font-family="Pretendard, sans-serif" font-size="13">일상의 자연어로 통제하는 행정 자동화</text>

    <!-- M BENEFIT -->
    <rect x="20" y="515" width="350" height="160" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
    <text x="35" y="545" fill="#166534" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">03. BENEFIT</text>
    <text x="35" y="580" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="16" font-weight="bold">종이책 + 전자책 듀얼 활용</text>
    <text x="35" y="610" fill="#475569" font-family="Pretendard, sans-serif" font-size="13">책으로 정독하고 PDF로 프롬프트 복붙</text>

    <!-- M PROOF -->
    <rect x="20" y="695" width="350" height="150" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
    <text x="35" y="725" fill="#92400E" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">04. PROOF</text>
    <text x="35" y="760" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="16" font-weight="bold">15년 현장 행정가의 검증</text>
    <text x="35" y="790" fill="#475569" font-family="Pretendard, sans-serif" font-size="13">홍익대 컴공 + 행정학 박사 김진호 저</text>

    <!-- M OFFER -->
    <rect x="20" y="865" width="350" height="230" rx="12" fill="#EFF6FF" stroke="#2563EB" stroke-width="1.5"/>
    <text x="35" y="895" fill="#1E40AF" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">05. OFFER (옵션 선택)</text>
    <text x="35" y="930" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="16" font-weight="bold">종이책 17,460원 / 전자책 13,000원</text>
    <text x="35" y="960" fill="#475569" font-family="Pretendard, sans-serif" font-size="13">실전 템플릿 코드 전원 무료 제공</text>
    <rect x="35" y="990" width="320" height="46" rx="8" fill="#2563EB"/>
    <text x="135" y="1018" fill="#FFFFFF" font-family="Pretendard, sans-serif" font-size="14" font-weight="bold">원하는 옵션 주문하기</text>
  </g>
</svg>'''

with open("figma_canvas_design.svg", "w", encoding="utf-8") as f:
    f.write(svg_code)

proc = subprocess.Popen(['powershell', '-Command', 'Set-Clipboard'], stdin=subprocess.PIPE, text=True, encoding='utf-8')
proc.communicate(input=svg_code)
print("UPDATED_WITH_EBOOK_SUCCESS")
