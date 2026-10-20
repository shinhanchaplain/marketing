import subprocess

svg_code = '''<svg width="1950" height="1420" viewBox="0 0 1950 1420" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- DESKTOP 1440px FRAME -->
  <g id="Desktop_1440px">
    <rect x="0" y="0" width="1440" height="1380" rx="16" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="2"/>
    <text x="60" y="55" fill="#475569" font-family="Pretendard, Inter, sans-serif" font-size="16" font-weight="bold">[『AI 행정학 마스터』 전자책(eBook) 고전환 랜딩페이지 - Desktop 1440px]</text>
    
    <!-- 01 HERO (전자책 즉시 다운로드 집중) -->
    <rect x="60" y="80" width="1320" height="240" rx="12" fill="#FFFFFF" stroke="#2563EB" stroke-width="2.5"/>
    <rect x="90" y="105" width="260" height="26" rx="6" fill="#2563EB"/>
    <text x="100" y="123" fill="#FFFFFF" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">⚡ 구매 즉시 다운로드 · 평생 소장 PDF</text>
    <text x="90" y="170" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="28" font-weight="bold">배송 기다리지 마세요. 결제 3초 후 다운로드받아 오늘 바로 칼퇴합니다.</text>
    <text x="90" y="205" fill="#475569" font-family="Pretendard, sans-serif" font-size="16">듀얼 모니터에 띄우고 프롬프트 복붙(Ctrl+C, V)으로 끝내는 2026 초자동화 행정 워크플로우</text>
    
    <!-- 전자책 메인 CTA 버튼 -->
    <rect x="90" y="235" width="280" height="48" rx="8" fill="#2563EB"/>
    <text x="125" y="265" fill="#FFFFFF" font-family="Pretendard, sans-serif" font-size="16" font-weight="bold">전자책(PDF) 즉시 다운로드 (13,000원) →</text>
    <text x="390" y="265" fill="#15803D" font-family="Pretendard, sans-serif" font-size="14" font-weight="bold">★ 프롬프트 템플릿집 무료 증정</text>
    <text x="660" y="265" fill="#64748B" font-family="Pretendard, sans-serif" font-size="13">(종이책 소장을 원하시면 17,460원에 주문 가능)</text>

    <!-- 02 PROBLEM (코딩 공부의 비효율) -->
    <rect x="60" y="340" width="1320" height="160" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
    <rect x="90" y="360" width="140" height="24" rx="6" fill="#FEE2E2"/>
    <text x="100" y="377" fill="#991B1B" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">02. PROBLEM</text>
    <text x="90" y="420" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="22" font-weight="bold">책 보며 일일이 타이핑하지 마세요. 오타 나면 끝입니다.</text>
    <text x="90" y="453" fill="#475569" font-family="Pretendard, sans-serif" font-size="15">기존 IT 책은 파이썬 문법만 늘어놓아 포기하게 만듭니다. 행정인에게 필요한 건 모니터 옆에 띄우고 바로 복사해 쓰는 실전 프롬프트입니다.</text>

    <!-- 03 BENEFIT (전자책 실무 최적화) -->
    <rect x="60" y="520" width="1320" height="170" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
    <rect x="90" y="540" width="130" height="24" rx="6" fill="#DCFCE7"/>
    <text x="100" y="557" fill="#166534" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">03. BENEFIT</text>
    <text x="90" y="600" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="22" font-weight="bold">듀얼 모니터 분할 화면 최적화: 1초 검색, 1초 복사, 10초 칼퇴.</text>
    <text x="90" y="633" fill="#475569" font-family="Pretendard, sans-serif" font-size="15">한쪽엔 PDF 전자책, 한쪽엔 업무 창을 띄우고 프롬프트를 복사(Ctrl+C)해 붙여넣으면(Ctrl+V) 하루 4시간 걸리던 서류 취합이 즉시 끝납니다.</text>

    <!-- 04 PROOF (저자 신뢰도) -->
    <rect x="60" y="710" width="1320" height="160" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
    <rect x="90" y="730" width="130" height="24" rx="6" fill="#FEF3C7"/>
    <text x="100" y="747" fill="#92400E" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">04. PROOF</text>
    <text x="90" y="790" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="22" font-weight="bold">15년 대학교 현장 행정 전문가 김진호 박사의 검증된 실전 바이블</text>
    <text x="90" y="823" fill="#475569" font-family="Pretendard, sans-serif" font-size="15">홍익대 컴공의 시스템 논리 + 백석대 행정학 박사(Ph.D.) | 신한대학교 도서관 입수 | 네이버 도서·교보·알라딘 공식 유통 원본 완벽 수록</text>

    <!-- 05 OFFER (전자책 집중 오퍼) -->
    <rect x="60" y="890" width="1320" height="280" rx="12" fill="#EFF6FF" stroke="#2563EB" stroke-width="2"/>
    <rect x="90" y="915" width="220" height="24" rx="6" fill="#DBEAFE"/>
    <text x="100" y="932" fill="#1E40AF" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">05. SPECIAL OFFER</text>
    <text x="90" y="975" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="26" font-weight="bold">『AI 행정학 마스터』 전자책(PDF) 특별 패키지 (13,000원)</text>
    <text x="90" y="1010" fill="#475569" font-family="Pretendard, sans-serif" font-size="15">결제 즉시 평생 소장 PDF 다운로드 + 실무 프롬프트 예제집 100% 전원 증정</text>
    <rect x="90" y="1035" width="280" height="50" rx="8" fill="#2563EB"/>
    <text x="135" y="1066" fill="#FFFFFF" font-family="Pretendard, sans-serif" font-size="16" font-weight="bold">전자책 즉시 다운로드받기 →</text>
    <text x="390" y="1066" fill="#64748B" font-family="Pretendard, sans-serif" font-size="14">(실물 종이책 소장 희망 시: 17,460원 선택 주문 가능)</text>
  </g>

  <!-- MOBILE 390px FRAME -->
  <g id="Mobile_390px" transform="translate(1510, 0)">
    <rect x="0" y="0" width="390" height="1380" rx="28" fill="#FFFFFF" stroke="#0F172A" stroke-width="4"/>
    <text x="30" y="45" fill="#64748B" font-family="Pretendard, sans-serif" font-size="13" font-weight="bold">[Mobile 390px - 전자책 집중 전환]</text>
    
    <!-- M HERO -->
    <rect x="20" y="65" width="350" height="260" rx="12" fill="#EFF6FF" stroke="#2563EB" stroke-width="1.5"/>
    <text x="35" y="95" fill="#1E40AF" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">⚡ 결제 즉시 다운로드</text>
    <text x="35" y="130" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="20" font-weight="bold">배송 없이 오늘 바로 칼퇴</text>
    <text x="35" y="160" fill="#475569" font-family="Pretendard, sans-serif" font-size="13">화면에 띄우고 프롬프트 복붙 1초</text>
    <text x="35" y="185" fill="#2563EB" font-family="Pretendard, sans-serif" font-size="16" font-weight="bold">전자책(PDF) 특별가: 13,000원</text>
    <rect x="35" y="205" width="320" height="42" rx="8" fill="#2563EB"/>
    <text x="110" y="232" fill="#FFFFFF" font-family="Pretendard, sans-serif" font-size="14" font-weight="bold">전자책 즉시 다운로드</text>
    <text x="35" y="270" fill="#166534" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">★ 프롬프트 예제 템플릿 무료 증정</text>

    <!-- M PROBLEM -->
    <rect x="20" y="345" width="350" height="150" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
    <text x="35" y="375" fill="#991B1B" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">02. PROBLEM</text>
    <text x="35" y="410" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="16" font-weight="bold">손으로 코드 치지 마세요</text>
    <text x="35" y="440" fill="#475569" font-family="Pretendard, sans-serif" font-size="13">Ctrl+C, Ctrl+V 복사로 즉시 실행</text>

    <!-- M BENEFIT -->
    <rect x="20" y="515" width="350" height="160" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
    <text x="35" y="545" fill="#166534" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">03. BENEFIT</text>
    <text x="35" y="580" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="16" font-weight="bold">1초 검색 · 10초 서류 완성</text>
    <text x="35" y="610" fill="#475569" font-family="Pretendard, sans-serif" font-size="13">PC·태블릿·스마트폰 평생 무제한 열람</text>

    <!-- M PROOF -->
    <rect x="20" y="695" width="350" height="150" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
    <text x="35" y="725" fill="#92400E" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">04. PROOF</text>
    <text x="35" y="760" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="16" font-weight="bold">15년 현장 행정 전문가</text>
    <text x="35" y="790" fill="#475569" font-family="Pretendard, sans-serif" font-size="13">홍익대 컴공 + 행정학 박사 김진호 저</text>

    <!-- M OFFER -->
    <rect x="20" y="865" width="350" height="230" rx="12" fill="#EFF6FF" stroke="#2563EB" stroke-width="1.5"/>
    <text x="35" y="895" fill="#1E40AF" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">05. OFFER</text>
    <text x="35" y="930" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="18" font-weight="bold">전자책 풀패키지: 13,000원</text>
    <text x="35" y="960" fill="#475569" font-family="Pretendard, sans-serif" font-size="13">구매 즉시 PDF 발송 + 템플릿 포함</text>
    <rect x="35" y="990" width="320" height="46" rx="8" fill="#2563EB"/>
    <text x="120" y="1018" fill="#FFFFFF" font-family="Pretendard, sans-serif" font-size="14" font-weight="bold">전자책 다운로드받기</text>
  </g>
</svg>'''

with open("figma_canvas_design.svg", "w", encoding="utf-8") as f:
    f.write(svg_code)

proc = subprocess.Popen(['powershell', '-Command', 'Set-Clipboard'], stdin=subprocess.PIPE, text=True, encoding='utf-8')
proc.communicate(input=svg_code)
print("EBOOK_FOCUSED_CLIPBOARD_UPDATED")
