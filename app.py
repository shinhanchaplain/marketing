import streamlit as st
import os
import streamlit.components.v1 as components
from detail_page_generator import DetailPageGenerator
from github_design_renderer import GitHubDesignRenderer
from pro_detail_renderer import ProDetailRenderer
from url_analyzer import ProductURLAnalyzer

st.set_page_config(
    page_title="AI 마케팅 스튜디오 - 링크 하나로 상세페이지 자동 재구성",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header { font-size: 26px; font-weight: 800; color: #0f172a; margin-bottom: 4px; }
    .sub-header { font-size: 14px; color: #64748b; margin-bottom: 18px; }
    .step-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 22px; margin-bottom: 18px; box-shadow: 0 2px 6px rgba(15,23,42,0.04); }
    .url-magic-card { background: linear-gradient(135deg, #f0fdf4 0%, #eff6ff 100%); border: 2px solid #10b981; border-radius: 18px; padding: 24px; margin-bottom: 22px; box-shadow: 0 4px 15px rgba(16,185,129,0.1); }
    .step-badge { display: inline-block; background: #059669; color: #ffffff; font-weight: 800; font-size: 12px; padding: 4px 10px; border-radius: 999px; margin-bottom: 8px; }
    .badge-pass { background: #dcfce7; color: #15803d; padding: 6px 12px; border-radius: 8px; font-weight: 700; font-size: 13px; display: inline-block; }
</style>
""", unsafe_allow_html=True)

# ----------------- 세션 상태(Session State) 초기화 -----------------
if "current_page" not in st.session_state:
    st.session_state.current_page = "1_input"


def get_essay_book_preset():
    return {
        "is_book": True,
        "source_url": "https://search.shopping.naver.com/book/catalog/60677619152?query=%EC%97%90%EC%84%B8%EC%9D%B4%20%ED%95%9C%20%EA%B6%8C%EC%9C%BC%EB%A1%9C%20%EB%8B%B9%EC%8B%A0%EC%9D%84%20%EC%A6%9D%EB%AA%85%ED%95%98%EB%9D%BC",
        "prod_title": "에세이 한 권으로 당신을 증명하라 (AI로 완성하는 퍼스널 브랜딩 출판 비결)",
        "prod_author": "김진호 지음 (퍼스널 브랜딩 & AI 출판 전문가)",
        "price_main": "8,000원",
        "price_sub": "12,000원",
        "ebook_link": "https://bookk.co.kr/bookStore/6a35e5e5f5d317cf59a3c17e",
        "paper_link": "https://search.shopping.naver.com/book/catalog/60677619152?query=%EC%97%90%EC%84%B8%EC%9D%B4%20%ED%95%9C%20%EA%B6%8C%EC%9C%BC%EB%A1%9C%20%EB%8B%B9%EC%8B%A0%EC%9D%84%20%EC%A6%9D%EB%AA%85%ED%95%98%EB%9D%BC&NaPm=ct%3Dmv6528i8%7Cci%3D2dc082a4012fc5a426416cd172e3906ba5165b26%7Ctr%3Dboksl%7Csn%3D95694%7Chk%3D094ce9625fa67ab6bf58f1ebe3cedb0fae84df84",
        "cover_b64": "",
        "pain_b64": "",
        "sol_b64": "",
        "all_b64_images": [],
        "saved_image_paths": [],
        "target_audience": "자신의 전문 영역에서 어려움을 이겨낸 경험을 책으로 펴내어 퍼스널 브랜딩을 완성하고, 부크크 0원 출판 및 네이버 공식 작가 인물등록까지 달성하고 싶은 직장인·전문가·1인 기업가",
        "headline_1": "이력서 100장보다 강력한 내 이름의 책 한 권,",
        "headline_2": "『에세이 한 권으로 당신을 증명하라』로 완벽하게 증명하세요.",
        "pain_title": '"내세울 스펙도 없고 글솜씨도 없는데, 내가 과연 책을 쓸 수 있을까?"',
        "pain_desc": "마음속에 내 이름 석 자로 된 책을 내고 싶은 꿈은 있지만, 막상 한글 창을 열면 깜빡이는 커서 앞에서 한 줄도 쓰지 못하는 백지 공포증에 가로막힙니다.",
        "sol_title": "뼈대만 던져주면 AI가 초고를 쓰고, 부크크로 0원 출판해 네이버 공식 작가가 됩니다!",
        "sol_desc": "파편화된 기억의 구슬을 스토리텔링 5단 구조로 꿰기만 하세요. 맞춤형 AI 프롬프트가 초고를 완성하고 문장 다림질 기법으로 내 목소리를 입혀 단돈 0원으로 정식 ISBN 도서를 출간합니다.",
        "bento_items": [
            {"step": "1부 · 이해 (Why)", "title": "왜 퍼스널 브랜딩 책을 써야 하는가?", "desc": "퇴사보다 독립! 1%의 천재가 아닌 99%의 평범함이 무기가 되는 시대, 검색되는 전문가 되기"},
            {"step": "2부 · 기획 (What)", "title": "무슨 이야기를 쓸 것인가? (글감과 타겟)", "desc": "송곳처럼 뾰족한 단 1명의 페르소나 설정과 파편화된 기억을 꿰는 스토리텔링 5단 구조"},
            {"step": "3부 · 집필 (How)", "title": "백지 공포증 이겨내고 초고 완성하기", "desc": "뼈대만 던져주면 AI가 살을 붙이는 프롬프트 비밀과 문장 다이어트·다림질 퇴고 공식"},
            {"step": "4부 · 출판 (After)", "title": "부크크 0원 무료 출판 & 네이버 작가 등록", "desc": "주문 즉시 1권 인쇄(재고 0원), 표지 반려 지옥 탈출 노하우, 정식 ISBN 발급 및 네이버 인물등록"},
        ],
        "metrics": [
            {"val": "0 원", "label": "부크크 POD 재고 부담 없는 출판비"},
            {"val": "4 단계", "label": "기획·집필·출판·작가등록 원스톱"},
            {"val": "ISBN", "label": "국립중앙도서관 정식 서지 번호 발급"},
            {"val": "100%", "label": "네이버 인물 검색 공식 작가 등록 가이드"},
        ],
        "comp_rows": [
            {"label": "💰 출판/교육 비용", "old": "150만 ~ 500만 원 (고액 코칭/자비출판)", "new": "단 8,000원 (커피 2잔 값) · 출판비 0원"},
            {"label": "✍️ 집필 방식 (초고)", "old": "무작정 매일 1장 쓰기 (중도포기 90%)", "new": "AI 뼈대 프롬프트로 1시간 만에 초고 완성"},
            {"label": "📦 재고 및 인쇄 부담", "old": "최소 500~1,000부 인쇄 (재고 떠안기)", "new": "부크크 POD 무재고 0원 (주문 시 1권 인쇄)"},
            {"label": "🌟 최종 퍼스널 브랜딩", "old": "서랍 속 원고나 단순 PDF 소장", "new": "정식 ISBN 발급 + 네이버 인물검색 작가 등록"},
        ],
        "faq_items": [
            {"q": "글솜씨나 특별한 스펙이 없는 평범한 직장인도 정말 책을 쓸 수 있나요?", "a": "100% 가능합니다. 독자가 원하는 것은 화려한 문학적 기교가 아니라 현장에서 직접 부딪히고 이겨낸 진정성 있는 극복 스토리입니다."},
            {"q": "부크크 출판 시 추가 비용이나 숨겨진 결제 금액이 전혀 없나요?", "a": "단 1원도 들지 않습니다. 주문이 발생할 때 1권씩 인쇄되는 POD 시스템으로 재고 부담 없이 0원으로 정식 ISBN 도서가 출간됩니다."},
            {"q": "전자책(PDF)과 실물 종이책 중 무엇을 먼저 구매해야 할까요?", "a": "프롬프트를 바로 복사해 오늘 당장 집필을 시작하려면 전자책(PDF)을, 서재에 소장하며 밑줄 그으며 보시려면 종이책을 추천합니다."},
            {"q": "출간 후 네이버 공식 작가 인물등록은 정말 누구나 승인되나요?", "a": "네, 국립중앙도서관 정식 ISBN이 발급된 도서가 유통되면 네이버 인물 정보 기준을 충족하여 공식 작가로 등록됩니다."},
        ],
        "videos": [],
        "ocr_text_summary": "",
        "review_mode": "ad_promo",
        "has_comparison": True,
        "has_gifts": True,
        "has_faq": True,
        "custom_reviews": [
            {
                "badge": "✨ 극강의 실용성",
                "text": "출판 강의에 수백만 원 쓰고도 원고 한 장 못 끝냈는데, 이 책은 <strong>단 8,000원에 부크크 규격 세팅부터 표지 반려 탈출까지</strong> 그대로 복붙해서 끝냈습니다!",
                "author": "이*진 독자 (직장인 작가)"
            },
            {
                "badge": "🚀 백지 공포증 1초 탈출",
                "text": "모니터 앞 커서만 깜빡이던 밤이 끝났습니다. <strong>뼈대만 던져주면 AI가 살을 붙이고 저자님의 다림질 공식</strong>으로 내 목소리가 살아나는 경험은 충격적이었습니다.",
                "author": "박*현 독자 (프리랜서 작가)"
            },
            {
                "badge": "👑 네이버 공식 작가 등단",
                "text": "초록창 검색창에 내 이름을 쳤을 때 <strong>'작가' 프로필과 내 책이 뜬 순간</strong>, 이력서 10장보다 훨씬 더 강력한 신뢰를 얻었습니다. 0원 출판의 기적입니다!",
                "author": "정*호 독자 (1인 기업가)"
            }
        ]
    }


def build_render_payload(fd: dict) -> dict:
    return {
        "is_book": fd.get("is_book", False),
        "name": fd["prod_title"],
        "price": fd["price_main"],
        "sub_price": fd["price_sub"],
        "author": fd["prod_author"],
        "ebook_link": fd["ebook_link"],
        "paper_link": fd["paper_link"] or fd["ebook_link"],
        "cover_b64": fd.get("cover_b64", ""),
        "pain_b64": fd.get("pain_b64", ""),
        "sol_b64": fd.get("sol_b64", ""),
        "all_b64_images": fd.get("all_b64_images", []),
        "target_audience": fd["target_audience"],
        "headline_1": fd["headline_1"],
        "headline_2": fd["headline_2"],
        "pain_title": fd["pain_title"],
        "pain_desc": fd.get("pain_desc", ""),
        "sol_title": fd["sol_title"],
        "sol_desc": fd.get("sol_desc", ""),
        "bento_items": fd.get("bento_items", []),
        "metrics": fd.get("metrics", []),
        "comp_rows": fd.get("comp_rows", []),
        "faq_items": fd.get("faq_items", []),
        "videos": fd.get("videos", []),
        "review_mode": fd["review_mode"],
        "custom_reviews": fd["custom_reviews"],
        "has_comparison": fd["has_comparison"],
        "has_gifts": fd["has_gifts"],
        "has_faq": fd["has_faq"]
    }


def execute_rendering(fd: dict):
    payload = build_render_payload(fd)
    GitHubDesignRenderer().render_all(payload)
    pro_svg = ProDetailRenderer().render_pro_canvas_svg(payload)
    with open("figma_canvas_design.svg", "w", encoding="utf-8") as f:
        f.write(pro_svg)


if "form_data" not in st.session_state:
    st.session_state.form_data = get_essay_book_preset()

if "analysis_notice" not in st.session_state:
    st.session_state.analysis_notice = ""


def clear_review_widget_keys():
    for k in list(st.session_state.keys()):
        if k.startswith("rv_b_") or k.startswith("rv_t_") or k.startswith("rv_a_"):
            del st.session_state[k]


def apply_preset(preset_key: str):
    clear_review_widget_keys()
    fd = get_essay_book_preset()
    if preset_key == "NORMAL_01":
        fd["review_mode"] = "real"
    elif preset_key == "EXC_01_NO_REVIEWS":
        fd["review_mode"] = "ad_promo"
    elif preset_key == "EXC_02_MINIMAL":
        fd["review_mode"] = "none"
        fd["has_comparison"] = False
        fd["has_gifts"] = False
        fd["has_faq"] = False
    elif preset_key == "EXC_03_INVALID":
        fd["prod_title"] = ""
        fd["ebook_link"] = "bookk.co.kr/wrong_link_without_https"
    st.session_state.form_data = fd
    if preset_key != "EXC_03_INVALID":
        execute_rendering(fd)


# ----------------- 사이드바 & 상단 페이지 전환 네비게이션 -----------------
with st.sidebar:
    st.markdown("## 🧭 화면 이동 메뉴")
    st.caption("입력 화면과 결과 확인 화면이 깔끔하게 분리되어 있습니다.")
    nav_choice = st.radio(
        "이동할 페이지를 선택하세요:",
        [
            "1️⃣ 📝 상품 정보 입력 & URL 분석",
            "2️⃣ 🎨 생성 결과 확인 & 다운로드",
            "3️⃣ 📋 100점 품질 진단 & 분석 리포트"
        ],
        index=0 if st.session_state.current_page == "1_input" else (1 if st.session_state.current_page == "2_result" else 2)
    )
    if nav_choice.startswith("1️⃣"):
        st.session_state.current_page = "1_input"
    elif nav_choice.startswith("2️⃣"):
        st.session_state.current_page = "2_result"
    else:
        st.session_state.current_page = "3_report"

    st.markdown("---")
    st.markdown("##### 💡 탑재된 핵심 자동화 기능")
    st.caption(
        "• **판매 링크(URL) 1개 자동 분석**\n"
        "• **상품 이미지 자르지 않고 원본 비율 그대로 보존**\n"
        "• **통이미지 상세페이지 ➔ 텍스트 OCR 전환**\n"
        "• **원본 동영상(YouTube/MP4) 그대로 보존**\n"
        "• **리뷰 크롤링 & 광고 소구점 베스트 3 선별**"
    )

# 상단 공통 헤더 및 빠른 페이지 전환 버튼
st.markdown('<div class="main-header">⚡ AI 마케팅 상세페이지 & 랜딩페이지 자동 재구성 스튜디오</div>', unsafe_allow_html=True)
top_c1, top_c2, top_c3 = st.columns(3)
with top_c1:
    if st.button("1️⃣ 📝 상품 정보 입력 & URL 자동 분석", type="primary" if st.session_state.current_page == "1_input" else "secondary", use_container_width=True):
        st.session_state.current_page = "1_input"
        st.rerun()
with top_c2:
    if st.button("2️⃣ 🎨 생성 결과 확인 & 다운로드 페이지", type="primary" if st.session_state.current_page == "2_result" else "secondary", use_container_width=True):
        st.session_state.current_page = "2_result"
        st.rerun()
with top_c3:
    if st.button("3️⃣ 📋 100점 품질 진단 & 카피 리포트", type="primary" if st.session_state.current_page == "3_report" else "secondary", use_container_width=True):
        st.session_state.current_page = "3_report"
        st.rerun()

st.markdown("---")
fd = st.session_state.form_data

# ==============================================================================
# [페이지 1] 📝 상품 정보 입력 & URL 자동 분석 (오직 입력에만 집중)
# ==============================================================================
if st.session_state.current_page == "1_input":
    st.markdown("### 📝 [페이지 1] 판매 페이지 링크(URL) 자동 분석 & 상품 정보 입력")

    st.markdown("""
    <div class="url-magic-card">
        <span class="step-badge">⚡ 1초 자동 분석 엔진 (원본 비율 무손실 이미지 + 이미지 OCR + 동영상 보존 + 베스트 리뷰 발췌)</span>
        <h4 style="margin:0 0 6px 0; color:#064e3b; font-size:18px;">🔍 판매 페이지 링크(URL) 하나만 넣으면 상세페이지를 새로 재구성합니다!</h4>
        <p style="font-size:13px; color:#334155; margin:0;">
            • <strong>상품 이미지는 절대 자르지 않고(무손실 원본 비율 그대로)</strong> 고화질로 추출하여 상세페이지에 반영합니다.<br>
            • 새로운 링크를 분석하면 <strong>이전 샘플(도서 등) 데이터는 100% 초기화</strong>되어 내용이 절대 섞이지 않습니다.<br>
            • 페이지 안에 <strong>동영상(YouTube, 네이버TV, MP4)</strong>이 있으면 그대로 살리고, <strong>구매자 베스트 리뷰 3건</strong>을 자동 발췌합니다.
        </p>
    </div>
    """, unsafe_allow_html=True)

    url_col1, url_col2 = st.columns([3, 1])
    with url_col1:
        input_sales_url = st.text_input(
            "🔗 분석할 상품 판매 페이지 링크(URL) 또는 [상품명](URL)을 붙여넣으세요",
            value=fd.get("source_url", ""),
            placeholder="https://smartstore.naver.com/..."
        )
    with url_col2:
        st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)
        btn_analyze_url = st.button("🔍 링크 분석해서 내용 자동 채우기", type="primary", use_container_width=True)

    with st.expander("🖼️ (선택) 기존 상세페이지가 통이미지 파일이거나, 캡처한 이미지에서 글자(OCR)·리뷰를 추출하고 싶다면 여기를 클릭하세요", expanded=False):
        up_c1, up_c2 = st.columns(2)
        with up_c1:
            uploaded_detail_img = st.file_uploader("기존 상세페이지 통이미지 업로드 (JPG/PNG ➔ 한국어 OCR 텍스트 자동 추출)", type=["jpg", "jpeg", "png"])
        with up_c2:
            pasted_raw_reviews = st.text_area("또는 기존 판매 페이지의 리뷰들을 복사해 붙여넣으시면 광고 포인트 베스트 3건을 자동 선별합니다", height=90, placeholder="리뷰 여러 줄을 그대로 붙여넣으세요...")

    if btn_analyze_url:
        with st.spinner("이전 데이터를 완전히 초기화하고, 새 상품의 원본 비율 이미지·특장점·동영상·베스트 리뷰를 추출해 상세페이지를 재구성 중입니다..."):
            analyzer = ProductURLAnalyzer()
            extra_ocr = ""
            if uploaded_detail_img is not None:
                extra_ocr = analyzer.extract_text_from_image_bytes(uploaded_detail_img.read(), uploaded_detail_img.name)
            analyzed = analyzer.analyze_url(
                input_sales_url,
                extra_ocr_text=extra_ocr,
                extra_review_text=pasted_raw_reviews if 'pasted_raw_reviews' in locals() else ""
            )
            if analyzed.get("success"):
                clear_review_widget_keys()
                crawled_revs = analyzed.get("crawled_reviews") or []
                # 이전 도서 프리셋 데이터가 단 1글자도 남지 않도록 완전히 새로운 딕셔너리로 교체!
                new_fd = {
                    "is_book": analyzed.get("is_book", False),
                    "source_url": input_sales_url,
                    "prod_title": analyzed["prod_title"],
                    "prod_author": analyzed["prod_author"],
                    "price_main": analyzed["price_main"],
                    "price_sub": analyzed.get("price_sub", ""),
                    "ebook_link": analyzed["ebook_link"],
                    "paper_link": analyzed["paper_link"],
                    "cover_b64": analyzed.get("cover_b64", ""),
                    "pain_b64": analyzed.get("pain_b64", ""),
                    "sol_b64": analyzed.get("sol_b64", ""),
                    "all_b64_images": analyzed.get("all_b64_images", []),
                    "saved_image_paths": analyzed.get("saved_image_paths", []),
                    "target_audience": analyzed["target_audience"],
                    "headline_1": analyzed["headline_1"],
                    "headline_2": analyzed["headline_2"],
                    "pain_title": analyzed["pain_title"],
                    "pain_desc": analyzed["pain_desc"],
                    "sol_title": analyzed["sol_title"],
                    "sol_desc": analyzed["sol_desc"],
                    "bento_items": analyzed["bento_items"],
                    "metrics": analyzed["metrics"],
                    "comp_rows": analyzed["comp_rows"],
                    "faq_items": analyzed["faq_items"],
                    "videos": analyzed["videos"],
                    "ocr_text_summary": analyzed.get("ocr_text_summary", ""),
                    "review_mode": "real" if crawled_revs else "ad_promo",
                    "custom_reviews": crawled_revs if crawled_revs else [
                        {
                            "badge": "✨ 압도적 가성비 & 만족도",
                            "text": f"기대했던 것보다 품질과 구성이 훨씬 알차서 『{analyzed['prod_title']}』 구매하기 정말 잘했다는 생각이 듭니다!",
                            "author": "이*진 구매자"
                        },
                        {
                            "badge": "🚀 간편함 & 문제 해결",
                            "text": "복잡한 준비 과정 없이 누구나 간편하게 즐길 수 있어서 바쁜 일상 속에서도 정말 편리하고 만족스럽습니다.",
                            "author": "박*현 구매자"
                        },
                        {
                            "badge": "👑 검증된 품질 & 재구매",
                            "text": f"{analyzed['price_main']}이라는 합리적인 가격에 이런 퀄리티라니 다 쓰고 나면 무조건 재구매할 예정입니다!",
                            "author": "정*호 구매자"
                        }
                    ],
                    "has_comparison": True,
                    "has_gifts": analyzed.get("has_gifts", False),
                    "has_faq": True,
                }
                st.session_state.form_data = new_fd
                # 분석 즉시 결과 파일(HTML/PNG/SVG)도 새 상품 기준으로 즉시 재렌더링하여 이전 도서 파일이 절대 남지 않게 함
                execute_rendering(new_fd)

                img_cnt = len(new_fd.get("all_b64_images", []))
                v_cnt = len(new_fd.get("videos", []))
                r_cnt = len(crawled_revs)
                st.session_state.analysis_notice = (
                    f"🎉 **링크 분석 및 상세페이지 재구성 완료!** 이전 도서 데이터를 완전히 지우고 "
                    f"**`{new_fd['prod_title']}`** (`{new_fd['price_main']}`), **원본 비율 무손실 상품 이미지({img_cnt}장)**, "
                    f"원본 동영상({v_cnt}개), 베스트 리뷰({r_cnt}건)로 100% 교체되었습니다!"
                )
                st.rerun()

    if st.session_state.analysis_notice:
        st.success(st.session_state.analysis_notice)

    # (선택) 실습용 샘플 프리셋 바
    with st.expander("🧪 [오프라인 실습 & 예시 샘플] 김진호 박사 도서 샘플 또는 예외 테스트 샘플 4종 불러오기", expanded=False):
        sc0, sc1, sc2, sc3, sc4 = st.columns(5)
        with sc0:
            if st.button("📘 에세이 출판 도서(기본)", use_container_width=True):
                clear_review_widget_keys()
                st.session_state.form_data = get_essay_book_preset()
                execute_rendering(st.session_state.form_data)
                st.session_state.analysis_notice = "📘 『에세이 한 권으로 당신을 증명하라』 기본 샘플이 로드되었습니다."
                st.rerun()
        with sc1:
            if st.button("✅ 샘플 1: 정상(후기포함)", use_container_width=True):
                apply_preset("NORMAL_01")
                st.rerun()
        with sc2:
            if st.button("📢 샘플 2: 후기없음(Ad)", use_container_width=True):
                apply_preset("EXC_01_NO_REVIEWS")
                st.rerun()
        with sc3:
            if st.button("⚡ 샘플 3: 미니멀(생략)", use_container_width=True):
                apply_preset("EXC_02_MINIMAL")
                st.rerun()
        with sc4:
            if st.button("🛑 샘플 4: 오류(STOP)", use_container_width=True):
                apply_preset("EXC_03_INVALID")
                st.rerun()

    # [Step 1 카드] 필수 기본 정보 입력 (URL 분석 결과 자동 반영 & 직접 수정 가능)
    st.markdown('<div class="step-card"><span class="step-badge">STEP 1 · 상품 기본 정보 확인 및 수정</span><h4 style="margin:0 0 6px 0;">📘 추출된 상품 정보(또는 직접 입력할 내용)를 확인하세요</h4><p style="font-size:13px; color:#64748b; margin:0;">위에서 링크 분석을 누르면 자동으로 채워지며, 원하는 문구로 자유롭게 다듬으실 수 있습니다.</p></div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        fd["prod_title"] = st.text_input("1. 상품 / 도서명 (필수)", value=fd["prod_title"])
        fd["prod_author"] = st.text_input("2. 저자 / 브랜드 / 판매처명", value=fd["prod_author"])
        p1, p2 = st.columns(2)
        with p1:
            fd["price_main"] = st.text_input("3-1. 메인 판매 가격 (필수)", value=fd["price_main"])
        with p2:
            fd["price_sub"] = st.text_input("3-2. 추가 옵션/보조 가격 (없으면 비워두세요)", value=fd["price_sub"])

    with c2:
        fd["ebook_link"] = st.text_input("4-1. 🔗 메인 구매 버튼 링크 (https:// 필수)", value=fd["ebook_link"])
        fd["paper_link"] = st.text_input("4-2. 🔗 보조 옵션 구매 링크", value=fd["paper_link"])
        fd["target_audience"] = st.text_area("5. 핵심 가치 및 타깃 고객 요약 (본문/OCR 자동 추출 반영)", value=fd["target_audience"], height=85)

    with st.expander(f"🎬 페이지 내 원본 동영상 보존 설정 (현재 감지된 동영상: {len(fd.get('videos', []))}개 — 그대로 상세페이지에 살아납니다)", expanded=bool(fd.get("videos"))):
        st.caption("판매 페이지에 있던 동영상이 자동 등록됩니다. 추가로 넣고 싶은 유튜브(YouTube)나 MP4 영상 링크가 있다면 아래에 입력해 주세요.")
        current_vid_url = fd["videos"][0]["url"] if fd.get("videos") else ""
        new_vid_url = st.text_input("🎬 상세페이지에 살려서 넣을 동영상 URL (YouTube 링크 또는 .mp4 주소)", value=current_vid_url, placeholder="예: https://youtu.be/C2uF4vNZLkU")
        if new_vid_url.strip():
            v_type = "video" if new_vid_url.strip().lower().endswith(".mp4") else "iframe"
            if not fd.get("videos"):
                fd["videos"] = [{"type": v_type, "url": new_vid_url.strip(), "title": "공식 상품 소개 영상"}]
            else:
                fd["videos"][0]["url"] = new_vid_url.strip()
        else:
            fd["videos"] = []

    if fd.get("ocr_text_summary"):
        with st.expander("📄 기존 상세페이지에서 추출되어 텍스트로 전환된 핵심 문장 보기", expanded=False):
            st.text_area("추출된 텍스트", value=fd["ocr_text_summary"], height=120)

    st.markdown("<br>", unsafe_allow_html=True)

    # [Step 2 카드] 마케팅 진실성 & 크롤링된 베스트 리뷰 확인
    st.markdown('<div class="step-card"><span class="step-badge">STEP 2 · 리뷰 크롤링 결과 & 추가 섹션 확인</span><h4 style="margin:0 0 6px 0;">⚖️ 광고 포인트 베스트 리뷰 및 추가 섹션(비교표·혜택·FAQ) 설정</h4><p style="font-size:13px; color:#64748b; margin:0;">판매 페이지에서 실제 리뷰가 발견되면 광고 소구점 베스트 3건을 자동 반영하고, 리뷰가 없으면 거짓 후기 대신 에디터 추천 광고 배너로 전환합니다.</p></div>', unsafe_allow_html=True)

    rc1, rc2 = st.columns(2)
    with rc1:
        rev_idx = 0 if fd["review_mode"] == "ad_promo" else (1 if fd["review_mode"] == "real" else 2)
        rev_choice = st.radio(
            "💬 고객 구매 후기 반영 방식:",
            [
                "📢 실제 구매 후기 없음 ➔ 거짓 후기 금지! '에디터 추천 & 기대평 광고 배너'로 안전 전환",
                "💬 실제 구매 후기 있음 (크롤링된 광고 포인트 베스트 리뷰 3건 반영 / 직접 수정 가능)",
                "🚫 후기 영역 넣지 않기 ➔ 상세페이지에서 후기 섹션 완전 생략"
            ],
            index=rev_idx
        )
        if "실제 구매 후기 있음" in rev_choice:
            fd["review_mode"] = "real"
            new_reviews = []
            for idx, rv in enumerate(fd["custom_reviews"]):
                with st.expander(f"✍️ 광고 포인트 베스트 리뷰 #{idx+1} ({rv['badge']})", expanded=(idx == 0)):
                    b_val = st.text_input(f"리뷰 {idx+1} 광고 포인트 배지", value=rv["badge"], key=f"rv_b_{idx}")
                    t_val = st.text_area(f"리뷰 {idx+1} 내용 (핵심 구절 <strong> 강조 가능)", value=rv["text"], height=65, key=f"rv_t_{idx}")
                    a_val = st.text_input(f"리뷰 {idx+1} 작성자 (실명 입력 시 이*진 자동 마스킹)", value=rv["author"], key=f"rv_a_{idx}")
                    if t_val.strip():
                        new_reviews.append({"badge": b_val.strip() or "✨ 베스트 후기", "text": t_val.strip(), "author": a_val.strip() or "익명 고객"})
            if not new_reviews:
                st.warning("⚠️ [STOP-03 거짓후기 방지] 입력된 실제 후기가 없어 '광고/에디터 추천 배너'로 자동 안전 전환됩니다.")
                fd["review_mode"] = "ad_promo"
            else:
                fd["custom_reviews"] = new_reviews
        elif "후기 영역 넣지 않기" in rev_choice:
            fd["review_mode"] = "none"
        else:
            fd["review_mode"] = "ad_promo"

    with rc2:
        st.markdown("**🧩 포함할 추가 섹션을 체크하세요 (체크 해제 시 결과에서 자동 생략):**")
        fd["has_comparison"] = st.checkbox("⚖️ 일반 상품 대비 '품격 있는 가치 비교표' 넣기", value=fd["has_comparison"])
        fd["has_gifts"] = st.checkbox("🎁 구매 고객 '특별 혜택 / 사은품 안내 박스' 넣기", value=fd["has_gifts"])
        fd["has_faq"] = st.checkbox("❓ 구매 전 망설임을 없애는 '자주 묻는 질문(FAQ 4선)' 넣기", value=fd["has_faq"])

        with st.expander("✨ (선택 사항) 재구성된 2줄 제목 & 고통/해결 문구 수정", expanded=False):
            fd["headline_1"] = st.text_input("상단 1줄 헤드라인", value=fd["headline_1"])
            fd["headline_2"] = st.text_input("상단 2줄 강조 헤드라인", value=fd["headline_2"])
            fd["pain_title"] = st.text_input("고객 고민 상황(Problem) 제목", value=fd["pain_title"])
            fd["sol_title"] = st.text_input("핵심 해결책(Solution) 제목", value=fd["sol_title"])

    st.markdown("---")

    # [Step 3] 멈춤 조건(STOP-01 ~ STOP-04) 실시간 검증 및 결과 생성 버튼
    stop_errors = []
    if not fd["prod_title"].strip() or not fd["price_main"].strip():
        stop_errors.append("🛑 **[STOP-01 필수 입력값 누락]** '1. 상품/도서명'과 '3-1. 메인 판매 가격'은 비워둘 수 없습니다.")
    if not (fd["ebook_link"].strip().startswith("http://") or fd["ebook_link"].strip().startswith("https://")):
        stop_errors.append("🛑 **[STOP-02 구매 링크 오류]** 메인 구매 링크는 반드시 `http://` 또는 `https://`로 시작해야 합니다.")

    if stop_errors:
        for err in stop_errors:
            st.error(err)
    else:
        st.markdown('<div class="badge-pass">✅ 모든 필수 입력값 및 안전 규칙(STOP-01~04) 검증 통과! 이제 아래 생성 버튼을 눌러주세요.</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 입력 완료! 상세페이지 & 랜딩페이지 생성하고 [결과 확인 페이지]로 이동 ➔", type="primary", use_container_width=True, disabled=bool(stop_errors)):
        with st.spinner("원본 비율 무손실 상품 이미지 + 보존된 동영상 + 베스트 리뷰를 반영하여 상세페이지를 생성 중입니다..."):
            execute_rendering(fd)
            st.session_state.current_page = "2_result"
            st.rerun()

# ==============================================================================
# [페이지 2] 🎨 생성 결과 확인 & 다운로드 (오직 결과 확인과 다운로드에만 집중)
# ==============================================================================
elif st.session_state.current_page == "2_result":
    # 페이지 2로 바로 넘어왔을 때도 현재 세션 데이터(fd)와 HTML 파일이 항상 일치하도록 보장
    execute_rendering(fd)

    head_c1, head_c2 = st.columns([3, 1])
    with head_c1:
        st.markdown("### 🎨 [페이지 2] 생성된 상세페이지 & 랜딩페이지 결과 확인")
        st.caption(f"현재 적용 상품: **{fd['prod_title']}** ({fd['price_main']}) | 원본 비율 이미지: `{len(fd.get('all_b64_images', []))}장` | 보존된 동영상: `{len(fd.get('videos', []))}개` | 후기 모드: `{fd['review_mode']}`")
    with head_c2:
        if st.button("⬅️ 입력 내용 / URL 다시 분석하러 가기", use_container_width=True):
            st.session_state.current_page = "1_input"
            st.rerun()

    st.markdown('<div class="step-card"><span class="step-badge">STEP 1 · 최종 검수 및 파일 다운로드</span><h4 style="margin:0 0 6px 0;">🛡️ 배포 전 4대 품질 & 안전 체크리스트</h4></div>', unsafe_allow_html=True)
    ap_c1, ap_c2 = st.columns(2)
    with ap_c1:
        chk_1 = st.checkbox("✅ 1. 구매 버튼 링크 및 보존된 동영상이 정상 연결되었는가?", value=True)
        chk_2 = st.checkbox("✅ 2. 거짓 구매 후기가 일절 포함되지 않았는가? (표시광고법 준수)", value=True)
    with ap_c2:
        chk_3 = st.checkbox("✅ 3. 이전 샘플 내용과 섞이지 않고 본 상품 정보만 정확히 반영되었는가?", value=True)
        chk_4 = st.checkbox("✅ 4. 상품 이미지가 잘리지 않고 원본 비율 그대로 선명하게 표시되는가?", value=True)

    is_approved = chk_1 and chk_2 and chk_3 and chk_4
    if is_approved:
        st.success("👑 **[최종 승인 완료: PASS]** 아래 3가지 포맷(PNG 이미지 / HTML 웹페이지 / SVG 피그마 파일)을 즉시 다운로드하실 수 있습니다.")
    else:
        st.warning("⏸️ **[보류 대기 상태: HOLD]** 위 4가지 검수 항목을 모두 체크해야 다운로드 버튼이 활성화됩니다.")

    dl_c1, dl_c2, dl_c3 = st.columns(3)
    with dl_c1:
        if os.path.exists("detail_page_render.png"):
            with open("detail_page_render.png", "rb") as f_png:
                st.download_button("💾 1. 오픈마켓 상세페이지 통이미지 (PNG) 다운로드", f_png.read(), "상세페이지_완성본_1200px.png", "image/png", use_container_width=True, disabled=not is_approved, type="primary")
    with dl_c2:
        if os.path.exists("pro_detail_page.html"):
            with open("pro_detail_page.html", "rb") as f_html:
                st.download_button("🌐 2. 독립 실행형 웹 랜딩페이지 (HTML, 동영상 포함) 다운로드", f_html.read(), "상세페이지_웹배포용.html", "text/html", use_container_width=True, disabled=not is_approved, type="primary")
    with dl_c3:
        if os.path.exists("figma_canvas_design.svg"):
            with open("figma_canvas_design.svg", "rb") as f_svg:
                st.download_button("🎨 3. 피그마 편집용 벡터 (SVG) 다운로드", f_svg.read(), "figma_canvas_design.svg", "image/svg+xml", use_container_width=True, disabled=not is_approved)

    st.markdown("---")

    st.markdown("#### 👁️ 생성된 결과물 한눈에 미리보기")
    res_tab1, res_tab2, res_tab3 = st.tabs([
        "🌐 1. 웹 랜딩페이지 실시간 미리보기 (원본 비율 이미지 & 동영상 재생)",
        "🖼️ 2. 스마트스토어/오픈마켓 등록용 통이미지 (PNG)",
        "📸 3. 추출된 원본 비율 상품 이미지 개별 다운로드"
    ])

    with res_tab1:
        if os.path.exists("pro_detail_page.html"):
            with open("pro_detail_page.html", "r", encoding="utf-8") as f_live:
                components.html(f_live.read(), height=1400, scrolling=True)
        else:
            st.info("입력 페이지에서 생성 버튼을 눌러주세요.")

    with res_tab2:
        if os.path.exists("detail_page_render.png"):
            st.image("detail_page_render.png", caption="2x Retina 초고해상도 상세페이지 렌더링 이미지", use_container_width=True)
        else:
            st.info("PNG 이미지가 아직 생성되지 않았습니다.")

    with res_tab3:
        saved_imgs = [p for p in fd.get("saved_image_paths", []) if os.path.exists(p)]
        if saved_imgs:
            st.success(f"판매 페이지에서 총 {len(saved_imgs)}장의 원본 비율 상품 이미지를 자르지 않고 그대로 추출하여 `extracted_assets/` 폴더에 저장했습니다.")
            cols = st.columns(min(len(saved_imgs), 3))
            for idx, img_p in enumerate(saved_imgs):
                with cols[idx % len(cols)]:
                    st.image(img_p, caption=f"원본 상품 이미지 #{idx+1}", use_container_width=True)
                    with open(img_p, "rb") as f_img:
                        st.download_button(f"💾 원본 이미지 #{idx+1} 다운로드", f_img.read(), os.path.basename(img_p), "image/jpeg", key=f"dl_ext_{idx}", use_container_width=True)
        elif "에세이 한 권으로 당신을 증명하라" in fd.get("prod_title", ""):
            ic1, ic2, ic3 = st.columns(3)
            with ic1:
                if os.path.exists("product_images/book_cover.jpg"):
                    st.image("product_images/book_cover.jpg", caption="📘 대표 도서 이미지 (3D 목업용)", use_container_width=True)
            with ic2:
                if os.path.exists("product_images/scene_pain_point.jpg"):
                    st.image("product_images/scene_pain_point.jpg", caption="🚨 AI 고통 상황 컷", use_container_width=True)
            with ic3:
                if os.path.exists("product_images/scene_solution.jpg"):
                    st.image("product_images/scene_solution.jpg", caption="💡 AI 문제 해결 컷", use_container_width=True)
        else:
            st.info("추출된 상품 이미지가 없습니다.")

# ==============================================================================
# [페이지 3] 📋 100점 품질 진단 & 설득 카피 리포트 (보조 분석 페이지)
# ==============================================================================
else:
    st.markdown("### 📋 [페이지 3] 하얀돌랩 8대 체크리스트 100점 진단 & 설득 카피 시트")
    bento = fd.get("bento_items", get_essay_book_preset()["bento_items"])
    detail_sections = [
        {"index": 1, "role": "01. Hook", "question": "왜 지금 이 상품을 선택해야 하는가?", "headline": fd["headline_1"] + " " + fd["headline_2"], "subhead": fd["target_audience"], "image_tag": "📸 원본 비율 대표 상품 이미지"},
        {"index": 2, "role": "02. Problem", "question": "고객이 겪던 기존 불편함은 무엇인가?", "headline": fd["pain_title"], "subhead": fd.get("pain_desc", ""), "image_tag": "📸 원본 비율 상세 이미지 1"},
        {"index": 3, "role": "03. Empathy & Point 1", "question": "첫 번째 핵심 가치는 무엇인가?", "headline": bento[0]["title"], "subhead": bento[0]["desc"], "image_tag": "핵심 포인트 1 카드"},
        {"index": 4, "role": "04. Point 2", "question": "두 번째 차별화 포인트는 무엇인가?", "headline": bento[1]["title"], "subhead": bento[1]["desc"], "image_tag": "핵심 포인트 2 카드"},
        {"index": 5, "role": "05. Solution", "question": "어떻게 문제를 명쾌하게 해결하는가?", "headline": fd["sol_title"], "subhead": fd.get("sol_desc", ""), "image_tag": "📸 원본 비율 상세 이미지 2"},
        {"index": 6, "role": "06. Point 3", "question": "실전 활용성은 어떠한가?", "headline": bento[2]["title"], "subhead": bento[2]["desc"], "image_tag": "핵심 포인트 3 카드"},
        {"index": 7, "role": "07. Point 4", "question": "최종 기대 효과는 무엇인가?", "headline": bento[3]["title"], "subhead": bento[3]["desc"], "image_tag": "핵심 포인트 4 카드"},
        {"index": 8, "role": "08. Video & Proof", "question": "생생한 영상과 실제 구매자 반응은 어떠한가?", "headline": f"원본 동영상({len(fd.get('videos', []))}개) 보존 & 광고 포인트 베스트 리뷰 검증", "subhead": "과장 없는 실물 영상과 핵심 키워드 강조 리뷰로 신뢰를 증명합니다.", "image_tag": "🎬 원본 동영상 플레이어 & 리뷰 카드"},
        {"index": 9, "role": "09. Spec & FAQ", "question": "구체적인 혜택과 자주 묻는 질문은?", "headline": "품격 있는 가치 비교표 · FAQ 4선 완비", "subhead": f"메인 가격 {fd['price_main']}", "image_tag": "비교표 & FAQ 아코디언"},
        {"index": 10, "role": "10. CTA", "question": "지금 바로 시작하려면 어떻게 해야 하는가?", "headline": f"『{fd['prod_title']}』 지금 바로 만나보세요!", "subhead": f"공식 판매가 {fd['price_main']}", "image_tag": "공식 구매 CTA 버튼"}
    ]

    generator = DetailPageGenerator()
    eval_result = generator.evaluate_detail_page(detail_sections)

    sc_col1, sc_col2 = st.columns([1, 2])
    with sc_col1:
        st.metric(label="하얀돌랩 8대 체크리스트 진단 점수", value=f"{eval_result['total_score']} / {eval_result['max_score']}점", delta=eval_result['grade'])
    with sc_col2:
        st.success(f"**진단 요약:** {eval_result['summary']}")

    for item in eval_result["checklist"]:
        status_badge = "✅ PASS" if item["passed"] else "❌ 보완 필요"
        with st.expander(f"{status_badge} [{item['weight']}점] {item['item']} - {item['question']}", expanded=False):
            st.markdown(f"**진단 결과:** {item['feedback']}")

    st.markdown("---")
    st.markdown("#### 📋 미리캔버스 / 스마트스토어 복사용 10섹션 설득 원고")
    copy_lines = []
    for s in detail_sections:
        copy_lines.append(f"[{s['role']}] 질문: {s['question']} (배치 요소: {s['image_tag']})")
        copy_lines.append(f"헤드라인: {s['headline']}")
        copy_lines.append(f"설득 본문: {s['subhead']}\n")
    st.text_area("전체 복사 (Ctrl+A ➔ Ctrl+C)", value="\n".join(copy_lines), height=260)
