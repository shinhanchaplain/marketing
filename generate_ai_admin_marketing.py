import json
from hook_engine import HookEngine
from detail_page_generator import DetailPageGenerator
from landing_page_generator import LandingPageGenerator
import subprocess

# 1. 김진호 박사님의 『AI 행정학 마스터』 정본 팩트 잠금 (Fact Locking)
book_facts = {
    "product_name": "AI 행정학 마스터 (바이브 코딩으로 완성하는 초자동화 워크플로우)",
    "price": "17,460원",
    "specs": [
        "자연어로 끝내는 바이브 코딩(Vibe Coding)",
        "공무원·교직원 맞춤 15년 실무 행정 초자동화",
        "180쪽 올컬러 실전 워크플로우 가이드 (210*297mm)"
    ],
    "weight": "180쪽 (부크크/교보/알라딘 유통)",
    "included": "실전 프롬프트 템플릿 & 실무 자동화 예제 코드 포함",
    "target_persona": "매일 쏟아지는 엑셀과 공문 서류 작업에 지쳐 퇴근이 늦어지는 공무원·교직원·행정 실무자"
}

comp_pain_points = [
    "어려운 파이썬 코딩 문법만 가르쳐주다 포기하게 만드는 기존 IT 서적",
    "실제 공문서나 행정 보고서 양식과 동떨어진 이론 중심 내용",
    "공공기관 보안 및 행정 환경을 고려하지 않은 비현실적인 예제"
]

hook_engine = HookEngine()
detail_gen = DetailPageGenerator()
landing_gen = LandingPageGenerator()

locked_facts = hook_engine.lock_facts(book_facts)

# 2. 강력한 5대 후킹 카피 생성
book_hooks = [
    {
        "type": "질문형 (Question)",
        "headline": "매일 쏟아지는 엑셀과 서류 작업, 언제까지 손으로 하시겠습니까?",
        "subhead": "파이썬 문법 한 줄 몰라도 괜찮습니다. 일상의 자연어로 행정 업무를 초자동화하세요.",
        "angle": "행정 실무자의 무의식적인 텍스트 노가다 피로감을 정면으로 환기"
    },
    {
        "type": "반직관형 (Counter-intuitive)",
        "headline": "코딩 공부하지 마세요. 행정 업무는 '바이브 코딩'으로 끝납니다.",
        "subhead": "복잡한 언어 대신 일상의 말로 시스템을 움직이는 2026 차세대 행정 워크플로우.",
        "angle": "IT 공부에 대한 두려움을 없애고 즉각적인 해결책 제시"
    },
    {
        "type": "숫자·증거형 (Data / Fact)",
        "headline": "15년 대학 행정 노하우 · 180쪽 실전 가이드 · 17,460원",
        "subhead": "공학과 행정을 모두 전공한 김진호 박사의 현장 검증 초자동화 바이블.",
        "angle": "저자의 압도적 이력과 정직한 책 가격으로 즉각적인 신뢰 구축"
    },
    {
        "type": "상황 공감형 (Empathy)",
        "headline": "공무원·교직원·공공기관 실무자를 위한 진짜 행정 자동화.",
        "subhead": "결재선, 공문 양식, 데이터 정제까지... 행정의 언어를 가장 잘 아는 책.",
        "angle": "타깃의 직업적 특수성을 정확히 짚어내어 나를 위한 필독서임을 인지"
    },
    {
        "type": "행동 제안형 (Action)",
        "headline": "오늘부터 반복 서류 작업에서 영혼을 해방시키세요.",
        "subhead": "자연어 프롬프트 1회 입력 → 엑셀/공문 자동 생성. 지금 바로 읽어보세요.",
        "angle": "책을 구매하여 즉시 칼퇴근을 달성할 수 있는 명확한 행동 촉구"
    }
]

# 3. 07차시 10섹션 상세페이지 생성
detail_sections = [
    {
        "index": 1,
        "role": "01. Hook (시선 집중)",
        "customer_question": "왜 지금 이 책을 읽어야 하는가?",
        "headline": "매일 쏟아지는 엑셀과 반복 서류 작업에 영혼을 갉아먹히고 있습니까?",
        "subhead": "단순 반복 업무와 극심한 감정 노동에 지친 행정인을 위한 궁극의 업무 해방 지침서.",
        "recommended_scene": "산더미처럼 쌓인 결재 서류와 복잡한 엑셀 화면 앞에서 피로해하는 행정 실무자 클로즈업"
    },
    {
        "index": 2,
        "role": "02. Problem (문제 제기)",
        "customer_question": "이게 정말 내 문제인가?",
        "headline": "남들은 AI로 칼퇴한다는데, 왜 내 업무는 여전히 그대로일까요?",
        "subhead": "시중의 AI 서적은 파이썬 문법만 늘어놓거나, 행정 실무와는 거리가 먼 뜬구름 잡는 이야기뿐입니다.",
        "recommended_scene": "두꺼운 코딩 서적을 사두고 이해하지 못해 덮어버린 직장인의 책상 모습"
    },
    {
        "index": 3,
        "role": "03. Empathy (상황 공감)",
        "customer_question": "저자가 내 행정 실무 상황을 진짜 아는가?",
        "headline": "15년간 대학 현장에서 뼛속 깊이 행정 실무자로 구른 저자의 피땀.",
        "subhead": "홍익대 컴퓨터공학 전공의 시스템 논리와 백석대 경영·행정학 박사의 조직 이해가 하나로 결합되었습니다.",
        "recommended_scene": "김진호 저자의 프로필과 신한대학교 등 실제 교육/행정 현장에서 진행된 워크숍 강의 장면"
    },
    {
        "index": 4,
        "role": "04. Solution (해결 방식)",
        "customer_question": "이 책은 어떤 방식으로 해결하는가?",
        "headline": "코딩 공부는 필요 없습니다. 일상의 자연어로 기계를 부리는 '바이브 코딩'.",
        "subhead": "말하듯이 프롬프트를 툭 던지면 복잡한 행정 서류와 엑셀 취합이 마법처럼 자동으로 끝납니다.",
        "recommended_scene": "자연어 한 문장을 입력하자 거대한 데이터가 표와 보고서로 자동 완성되는 UI 모니터 화면"
    },
    {
        "index": 5,
        "role": "05. Benefit (핵심 혜택)",
        "customer_question": "책을 읽고 나면 내 업무가 어떻게 달라지는가?",
        "headline": "하루 4시간 걸리던 서류 취합과 데이터 정리가 10초 만에 끝납니다.",
        "subhead": "반복 노동에서 해방되어 진짜 중요한 기획과 정책, 그리고 여유로운 저녁 시간을 되찾으세요.",
        "recommended_scene": "여유롭게 커피 한 잔을 마시며 정시 퇴근하는 활기찬 공무원·교직원의 모습"
    },
    {
        "index": 6,
        "role": "06. 차별점 (기존 도서 대비)",
        "customer_question": "왜 다른 책이 아니라 'AI 행정학 마스터'인가?",
        "headline": "문법 나열 0% · 행정 공문 및 실무 예제 100%.",
        "subhead": "이론서가 아닙니다. 책을 펼쳐 옆에 두고 그대로 따라 하기만 하면 즉시 작동하는 실전 워크플로우 북입니다.",
        "recommended_scene": "복잡한 코딩 책 vs 한글로 쓰인 직관적인 실무 프롬프트 예시 비교 컷"
    },
    {
        "index": 7,
        "role": "07. Proof (신뢰 근거)",
        "customer_question": "믿고 구매할 근거가 있는가?",
        "headline": "15년 현장 행정 전문가 김진호 박사 저술 · 180쪽 올컬러 판형 · 17,460원.",
        "subhead": "신한대학교 중앙도서관 입수 및 네이버 도서, 교보문고, 알라딘 공식 유통 검증 도서.",
        "recommended_scene": "도서 실물 표지 3D 목업 컷과 도서관 소장 서지 정보 배지"
    },
    {
        "index": 8,
        "role": "08. Spec (목차 및 구성)",
        "customer_question": "책은 구체적으로 어떻게 구성되어 있는가?",
        "headline": "기초 이해 ➔ 프롬프트 엔지니어링 ➔ 행정 실전 초자동화 3단계 완성.",
        "subhead": "180쪽 분량, A4 변형 판형(210*297mm)으로 펼쳐놓고 실습하기 가장 좋은 최적의 레이아웃.",
        "recommended_scene": "핵심 챕터 목차 요약 그래픽 카드 및 내부 페이지 미리보기 인쇄 컷"
    },
    {
        "index": 9,
        "role": "09. FAQ (망설임 해소)",
        "customer_question": "정말 컴퓨터를 전혀 모르는 왕초보도 따라 할 수 있나요?",
        "headline": "컴맹이어도 가능합니다 · 교재 예제 프롬프트 100% 무료 제공 · 정가 17,460원.",
        "subhead": "키보드로 타자만 칠 수 있다면 누구나 오늘 당장 행정 자동화 워크플로우를 가동할 수 있습니다.",
        "recommended_scene": "자주 묻는 질문 3가지와 명쾌한 답변 카드"
    },
    {
        "index": 10,
        "role": "10. CTA (구매 결심)",
        "customer_question": "이제 무엇을 해야 하는가?",
        "headline": "『AI 행정학 마스터』 지금 주문하고 내일부터 칼퇴근하세요.",
        "subhead": "정가 17,460원 (부크크 · 교보문고 · 알라딘 · 네이버 도서 판매 중)",
        "recommended_scene": "선명한 책 표지 이미지와 [지금 도서 구매하러 가기] 단일 강조 버튼"
    }
]

# 4. SVG 피그마 벡터 캔버스 디자인 코드 생성
svg_code = f'''<svg width="1900" height="1350" viewBox="0 0 1900 1350" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- DESKTOP 1440px FRAME -->
  <g id="Desktop_1440px">
    <rect x="0" y="0" width="1440" height="1300" rx="16" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="2"/>
    <text x="60" y="55" fill="#475569" font-family="Pretendard, Inter, sans-serif" font-size="16" font-weight="bold">[도서 상세페이지 & 랜딩페이지 - Desktop 1440px]</text>
    
    <!-- 01 HERO -->
    <rect x="60" y="80" width="1320" height="230" rx="12" fill="#FFFFFF" stroke="#2563EB" stroke-width="2"/>
    <rect x="90" y="105" width="220" height="26" rx="6" fill="#DBEAFE"/>
    <text x="100" y="123" fill="#1E40AF" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">01. HERO | 공무원·교직원 행정 해방서</text>
    <text x="90" y="170" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="28" font-weight="bold">매일 쏟아지는 엑셀과 서류 작업, 언제까지 손으로 하시겠습니까?</text>
    <text x="90" y="205" fill="#475569" font-family="Pretendard, sans-serif" font-size="16">『AI 행정학 마스터: 바이브 코딩으로 완성하는 초자동화 워크플로우』 | 김진호 저 | 17,460원</text>
    <rect x="90" y="235" width="230" height="46" rx="8" fill="#2563EB"/>
    <text x="135" y="264" fill="#FFFFFF" font-family="Pretendard, sans-serif" font-size="15" font-weight="bold">지금 도서 구매하기 →</text>
    <text x="340" y="264" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="18" font-weight="bold">17,460원 (무료배송)</text>

    <!-- 02 PROBLEM -->
    <rect x="60" y="325" width="1320" height="160" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
    <rect x="90" y="345" width="140" height="24" rx="6" fill="#FEE2E2"/>
    <text x="100" y="362" fill="#991B1B" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">02. PROBLEM</text>
    <text x="90" y="405" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="22" font-weight="bold">코딩 공부는 필요 없습니다. 문제는 복잡한 문법이 아닙니다.</text>
    <text x="90" y="438" fill="#475569" font-family="Pretendard, sans-serif" font-size="15">기존 IT 책은 파이썬만 늘어놓다 포기하게 만듭니다. 행정 실무에는 실무에 맞는 자연어 통제법이 필요합니다.</text>

    <!-- 03 BENEFIT -->
    <rect x="60" y="500" width="1320" height="160" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
    <rect x="90" y="520" width="130" height="24" rx="6" fill="#DCFCE7"/>
    <text x="100" y="537" fill="#166534" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">03. BENEFIT</text>
    <text x="90" y="580" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="22" font-weight="bold">하루 4시간 걸리던 취합 업무가 단 10초 만에 끝납니다.</text>
    <text x="90" y="613" fill="#475569" font-family="Pretendard, sans-serif" font-size="15">공학과 행정을 아우른 15년 현장 행정가 김진호 박사의 실전 프롬프트와 자동화 워크플로우 전격 공개.</text>

    <!-- 04 PROOF -->
    <rect x="60" y="675" width="1320" height="160" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
    <rect x="90" y="695" width="130" height="24" rx="6" fill="#FEF3C7"/>
    <text x="100" y="712" fill="#92400E" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">04. PROOF</text>
    <text x="90" y="755" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="22" font-weight="bold">검증된 현장 전문성과 투명한 팩트</text>
    <text x="90" y="788" fill="#475569" font-family="Pretendard, sans-serif" font-size="15">홍익대 컴공 논리 + 백석대 경영·행정학 박사 | 180쪽 올컬러 실습 판형 | 네이버 도서·교보·알라딘 공식 유통</text>

    <!-- 05 OFFER & CTA -->
    <rect x="60" y="850" width="1320" height="250" rx="12" fill="#EFF6FF" stroke="#2563EB" stroke-width="2"/>
    <rect x="90" y="875" width="140" height="24" rx="6" fill="#DBEAFE"/>
    <text x="100" y="892" fill="#1E40AF" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">05. OFFER &amp; CTA</text>
    <text x="90" y="940" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="26" font-weight="bold">『AI 행정학 마스터』 지금 주문하고 내일부터 칼퇴근하세요.</text>
    <text x="90" y="975" fill="#475569" font-family="Pretendard, sans-serif" font-size="15">단 한 권으로 끝내는 2026 초자동화 행정 혁명 | 17,460원</text>
    <rect x="90" y="1005" width="240" height="50" rx="8" fill="#2563EB"/>
    <text x="140" y="1037" fill="#FFFFFF" font-family="Pretendard, sans-serif" font-size="16" font-weight="bold">온라인 서점 바로가기 →</text>
  </g>

  <!-- MOBILE 390px FRAME -->
  <g id="Mobile_390px" transform="translate(1480, 0)">
    <rect x="0" y="0" width="390" height="1300" rx="28" fill="#FFFFFF" stroke="#0F172A" stroke-width="4"/>
    <text x="30" y="45" fill="#64748B" font-family="Pretendard, sans-serif" font-size="13" font-weight="bold">[Mobile 390px - 세로 흐름]</text>
    
    <!-- M HERO -->
    <rect x="20" y="65" width="350" height="230" rx="12" fill="#EFF6FF" stroke="#2563EB" stroke-width="1.5"/>
    <text x="35" y="95" fill="#1E40AF" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">01. HERO</text>
    <text x="35" y="130" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="20" font-weight="bold">서류 업무, 이제 AI로 칼퇴</text>
    <text x="35" y="160" fill="#475569" font-family="Pretendard, sans-serif" font-size="13">바이브 코딩으로 완성하는 초자동화</text>
    <text x="35" y="185" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="15" font-weight="bold">17,460원 | 저자 김진호</text>
    <rect x="35" y="205" width="320" height="42" rx="8" fill="#2563EB"/>
    <text x="125" y="232" fill="#FFFFFF" font-family="Pretendard, sans-serif" font-size="14" font-weight="bold">도서 구매하러 가기</text>

    <!-- M PROBLEM -->
    <rect x="20" y="310" width="350" height="150" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
    <text x="35" y="340" fill="#991B1B" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">02. PROBLEM</text>
    <text x="35" y="375" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="16" font-weight="bold">코딩 몰라도 가능합니다</text>
    <text x="35" y="405" fill="#475569" font-family="Pretendard, sans-serif" font-size="13">자연어로 기계를 부리는 바이브 코딩</text>

    <!-- M BENEFIT -->
    <rect x="20" y="475" width="350" height="150" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
    <text x="35" y="505" fill="#166534" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">03. BENEFIT</text>
    <text x="35" y="540" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="16" font-weight="bold">4시간 업무를 10초 만에</text>
    <text x="35" y="570" fill="#475569" font-family="Pretendard, sans-serif" font-size="13">15년 현장 행정가의 실전 프롬프트</text>

    <!-- M PROOF -->
    <rect x="20" y="640" width="350" height="150" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
    <text x="35" y="670" fill="#92400E" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">04. PROOF</text>
    <text x="35" y="705" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="16" font-weight="bold">공학 + 행정학 박사의 검증</text>
    <text x="35" y="735" fill="#475569" font-family="Pretendard, sans-serif" font-size="13">180쪽 올컬러 | 교보/알라딘/네이버</text>

    <!-- M OFFER -->
    <rect x="20" y="805" width="350" height="220" rx="12" fill="#EFF6FF" stroke="#2563EB" stroke-width="1.5"/>
    <text x="35" y="835" fill="#1E40AF" font-family="Pretendard, sans-serif" font-size="12" font-weight="bold">05. OFFER</text>
    <text x="35" y="870" fill="#0F172A" font-family="Pretendard, sans-serif" font-size="19" font-weight="bold">정가: 17,460원</text>
    <text x="35" y="900" fill="#475569" font-family="Pretendard, sans-serif" font-size="13">실전 템플릿 코드 전원 무료 증정</text>
    <rect x="35" y="930" width="320" height="46" rx="8" fill="#2563EB"/>
    <text x="120" y="958" fill="#FFFFFF" font-family="Pretendard, sans-serif" font-size="14" font-weight="bold">지금 도서 구매하기</text>
  </g>
</svg>'''

# 5. 파일 저장 및 윈도우 클립보드에 즉시 주입
with open("figma_canvas_design.svg", "w", encoding="utf-8") as f:
    f.write(svg_code)

proc = subprocess.Popen(['powershell', '-Command', 'Set-Clipboard'], stdin=subprocess.PIPE, text=True, encoding='utf-8')
proc.communicate(input=svg_code)

print("AI_ADMIN_MASTER_GENERATED_AND_CLIPBOARD_UPDATED")
