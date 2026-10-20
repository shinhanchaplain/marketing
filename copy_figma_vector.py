import subprocess

svg_content = '''<svg width="1900" height="1200" viewBox="0 0 1900 1200" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- DESKTOP 1440px FRAME -->
  <g id="Desktop_1440px">
    <rect x="0" y="0" width="1440" height="1150" rx="16" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="2"/>
    <text x="60" y="60" fill="#64748B" font-family="Inter, sans-serif" font-size="16" font-weight="bold">[08차시 캠페인 랜딩페이지 - Desktop 1440px]</text>
    
    <!-- 01 HERO -->
    <rect x="60" y="90" width="1320" height="220" rx="12" fill="#FFFFFF" stroke="#3B82F6" stroke-width="2"/>
    <rect x="90" y="115" width="120" height="26" rx="6" fill="#DBEAFE"/>
    <text x="100" y="133" fill="#1E40AF" font-family="Inter, sans-serif" font-size="12" font-weight="bold">01. HERO (첫 약속)</text>
    <text x="90" y="180" fill="#0F172A" font-family="Inter, sans-serif" font-size="32" font-weight="bold">어디서 일하든, 내 작업을 10초 만에.</text>
    <text x="90" y="215" fill="#475569" font-family="Inter, sans-serif" font-size="16">6단계 각도 조절 · 620g 휴대용 알루미늄 스탠드 | NOVA DESK FOLD ONE</text>
    <rect x="90" y="240" width="220" height="46" rx="8" fill="#2563EB"/>
    <text x="130" y="269" fill="#FFFFFF" font-family="Inter, sans-serif" font-size="15" font-weight="bold">FOLD ONE 자세히 보기 →</text>
    <text x="330" y="269" fill="#0F172A" font-family="Inter, sans-serif" font-size="18" font-weight="bold">39,000원</text>

    <!-- 02 PROBLEM -->
    <rect x="60" y="330" width="1320" height="150" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
    <rect x="90" y="350" width="140" height="24" rx="6" fill="#FEE2E2"/>
    <text x="100" y="367" fill="#991B1B" font-family="Inter, sans-serif" font-size="12" font-weight="bold">02. PROBLEM (결핍 자극)</text>
    <text x="90" y="410" fill="#0F172A" font-family="Inter, sans-serif" font-size="22" font-weight="bold">책상은 바뀌는데, 화면 각도는 그대로인가요?</text>
    <text x="90" y="440" fill="#475569" font-family="Inter, sans-serif" font-size="15">장소가 바뀔 때마다 겪는 시선 높이 불안정과 흐트러지는 작업 리듬을 방치하지 마세요.</text>

    <!-- 03 BENEFIT -->
    <rect x="60" y="500" width="1320" height="150" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
    <rect x="90" y="520" width="130" height="24" rx="6" fill="#DCFCE7"/>
    <text x="100" y="537" fill="#166534" font-family="Inter, sans-serif" font-size="12" font-weight="bold">03. BENEFIT (고객 변화)</text>
    <text x="90" y="580" fill="#0F172A" font-family="Inter, sans-serif" font-size="22" font-weight="bold">620g과 전용 파우치 한 묶음으로 가볍게.</text>
    <text x="90" y="610" fill="#475569" font-family="Inter, sans-serif" font-size="15">이동 전 준비를 하나로 줄여 카페, 공유오피스 어디서든 10초 만에 업무를 시작합니다.</text>

    <!-- 04 PROOF -->
    <rect x="60" y="670" width="1320" height="150" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
    <rect x="90" y="690" width="130" height="24" rx="6" fill="#FEF3C7"/>
    <text x="100" y="707" fill="#92400E" font-family="Inter, sans-serif" font-size="12" font-weight="bold">04. PROOF (숫자 팩트)</text>
    <text x="90" y="750" fill="#0F172A" font-family="Inter, sans-serif" font-size="22" font-weight="bold">확인된 숫자로 선택하세요.</text>
    <text x="90" y="780" fill="#475569" font-family="Inter, sans-serif" font-size="15">6단계 각도 조절 · 620g 경량 구조 · 39,000원 정직한 가격</text>

    <!-- 05 OFFER & CTA -->
    <rect x="60" y="840" width="1320" height="240" rx="12" fill="#EFF6FF" stroke="#3B82F6" stroke-width="2"/>
    <rect x="90" y="865" width="140" height="24" rx="6" fill="#DBEAFE"/>
    <text x="100" y="882" fill="#1E40AF" font-family="Inter, sans-serif" font-size="12" font-weight="bold">05. OFFER (최종 제안)</text>
    <text x="90" y="930" fill="#0F172A" font-family="Inter, sans-serif" font-size="26" font-weight="bold">지금 시작하는 패키지: FOLD ONE (39,000원)</text>
    <text x="90" y="965" fill="#475569" font-family="Inter, sans-serif" font-size="15">본품 + 전용 보관 파우치 포함 구성으로 오늘부터 내 작업 환경을 정돈하세요.</text>
    <rect x="90" y="995" width="240" height="50" rx="8" fill="#2563EB"/>
    <text x="140" y="1027" fill="#FFFFFF" font-family="Inter, sans-serif" font-size="16" font-weight="bold">내 작업 환경 정돈하기 →</text>
  </g>

  <!-- MOBILE 390px FRAME -->
  <g id="Mobile_390px" transform="translate(1480, 0)">
    <rect x="0" y="0" width="390" height="1150" rx="28" fill="#FFFFFF" stroke="#0F172A" stroke-width="4"/>
    <text x="30" y="50" fill="#64748B" font-family="Inter, sans-serif" font-size="13" font-weight="bold">[Mobile 390px - 세로 흐름]</text>
    
    <!-- M HERO -->
    <rect x="20" y="70" width="350" height="220" rx="12" fill="#EFF6FF" stroke="#3B82F6" stroke-width="1.5"/>
    <text x="35" y="105" fill="#1E40AF" font-family="Inter, sans-serif" font-size="12" font-weight="bold">01. HERO (첫 약속)</text>
    <text x="35" y="145" fill="#0F172A" font-family="Inter, sans-serif" font-size="22" font-weight="bold">내 작업을 10초 만에.</text>
    <text x="35" y="175" fill="#475569" font-family="Inter, sans-serif" font-size="13">6단계 각도 조절 · 620g 스탠드</text>
    <rect x="35" y="210" width="320" height="44" rx="8" fill="#2563EB"/>
    <text x="120" y="238" fill="#FFFFFF" font-family="Inter, sans-serif" font-size="14" font-weight="bold">FOLD ONE 자세히 보기</text>

    <!-- M PROBLEM -->
    <rect x="20" y="310" width="350" height="150" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
    <text x="35" y="345" fill="#991B1B" font-family="Inter, sans-serif" font-size="12" font-weight="bold">02. PROBLEM</text>
    <text x="35" y="380" fill="#0F172A" font-family="Inter, sans-serif" font-size="17" font-weight="bold">장소마다 달라지는 각도</text>
    <text x="35" y="415" fill="#475569" font-family="Inter, sans-serif" font-size="13">매번 흐트러지는 작업 환경</text>

    <!-- M BENEFIT -->
    <rect x="20" y="480" width="350" height="150" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
    <text x="35" y="515" fill="#166534" font-family="Inter, sans-serif" font-size="12" font-weight="bold">03. BENEFIT</text>
    <text x="35" y="550" fill="#0F172A" font-family="Inter, sans-serif" font-size="17" font-weight="bold">한 묶음으로 가볍게</text>
    <text x="35" y="585" fill="#475569" font-family="Inter, sans-serif" font-size="13">전용 파우치로 즉시 이동</text>

    <!-- M PROOF -->
    <rect x="20" y="650" width="350" height="150" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
    <text x="35" y="685" fill="#92400E" font-family="Inter, sans-serif" font-size="12" font-weight="bold">04. PROOF</text>
    <text x="35" y="720" fill="#0F172A" font-family="Inter, sans-serif" font-size="17" font-weight="bold">숫자로 보는 팩트</text>
    <text x="35" y="755" fill="#475569" font-family="Inter, sans-serif" font-size="13">6단계 / 620g / 39,000원</text>

    <!-- M OFFER -->
    <rect x="20" y="820" width="350" height="220" rx="12" fill="#EFF6FF" stroke="#3B82F6" stroke-width="1.5"/>
    <text x="35" y="855" fill="#1E40AF" font-family="Inter, sans-serif" font-size="12" font-weight="bold">05. OFFER</text>
    <text x="35" y="890" fill="#0F172A" font-family="Inter, sans-serif" font-size="20" font-weight="bold">패키지: 39,000원</text>
    <text x="35" y="920" fill="#475569" font-family="Inter, sans-serif" font-size="13">본품 + 전용 파우치 포함</text>
    <rect x="35" y="955" width="320" height="46" rx="8" fill="#2563EB"/>
    <text x="120" y="984" fill="#FFFFFF" font-family="Inter, sans-serif" font-size="14" font-weight="bold">내 환경 정돈하기</text>
  </g>
</svg>'''

# 윈도우 클립보드에 SVG 코드 복사
cmd = f'powershell -Command "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; Set-Clipboard -Value @\'\\n{svg_content}\\n\'@"'
subprocess.run(cmd, shell=True)
print("SUCCESS_CLIPBOARD_COPIED")
