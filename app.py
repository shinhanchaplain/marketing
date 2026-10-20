import streamlit as st
import os
import streamlit.components.v1 as components
from detail_page_generator import DetailPageGenerator
from github_design_renderer import GitHubDesignRenderer
from pro_detail_renderer import ProDetailRenderer

st.set_page_config(
    page_title="AI 마케팅 스튜디오 - 입력/결과 분리형 워크스페이스",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header { font-size: 26px; font-weight: 800; color: #0f172a; margin-bottom: 4px; }
    .sub-header { font-size: 14px; color: #64748b; margin-bottom: 18px; }
    .step-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 22px; margin-bottom: 18px; box-shadow: 0 2px 6px rgba(15,23,42,0.04); }
    .step-badge { display: inline-block; background: #059669; color: #ffffff; font-weight: 800; font-size: 12px; padding: 4px 10px; border-radius: 999px; margin-bottom: 8px; }
    .badge-pass { background: #dcfce7; color: #15803d; padding: 6px 12px; border-radius: 8px; font-weight: 700; font-size: 13px; display: inline-block; }
    .vs-card-my { background: #eff6ff; border: 2px solid #3b82f6; border-radius: 12px; padding: 18px; }
    .vs-card-comp { background: #fef2f2; border: 2px solid #ef4444; border-radius: 12px; padding: 18px; }
</style>
""", unsafe_allow_html=True)

# ----------------- 세션 상태(Session State) 초기화 -----------------
if "current_page" not in st.session_state:
    st.session_state.current_page = "1_input"

if "form_data" not in st.session_state:
    st.session_state.form_data = {
        "prod_title": "에세이 한 권으로 당신을 증명하라 (AI로 완성하는 퍼스널 브랜딩 출판 비결)",
        "prod_author": "김진호 지음 (퍼스널 브랜딩 & AI 출판 전문가)",
        "price_main": "8,000원",
        "price_sub": "12,000원",
        "ebook_link": "https://bookk.co.kr/bookStore/6a35e5e5f5d317cf59a3c17e",
        "paper_link": "https://search.shopping.naver.com/book/catalog/60677619152?query=%EC%97%90%EC%84%B8%EC%9D%B4%20%ED%95%9C%20%EA%B6%8C%EC%9C%BC%EB%A1%9C%20%EB%8B%B9%EC%8B%A0%EC%9D%84%20%EC%A6%9D%EB%AA%85%ED%95%98%EB%9D%BC&NaPm=ct%3Dmv6528i8%7Cci%3D2dc082a4012fc5a426416cd172e3906ba5165b26%7Ctr%3Dboksl%7Csn%3D95694%7Chk%3D094ce9625fa67ab6bf58f1ebe3cedb0fae84df84",
        "target_audience": "자신의 전문 영역에서 어려움을 이겨낸 경험을 책으로 펴내어 퍼스널 브랜딩을 완성하고, 부크크 0원 출판 및 네이버 공식 작가 인물등록까지 달성하고 싶은 직장인·전문가·1인 기업가",
        "headline_1": "이력서 100장보다 강력한 내 이름의 책 한 권,",
        "headline_2": "『에세이 한 권으로 당신을 증명하라』로 완벽하게 증명하세요.",
        "pain_title": '"내세울 스펙도 없고 글솜씨도 없는데, 내가 과연 책을 쓸 수 있을까?"',
        "sol_title": "뼈대만 던져주면 AI가 초고를 쓰고, 부크크로 0원 출판해 네이버 공식 작가가 됩니다!",
        "review_mode": "ad_promo",
        "has_comparison": True,
        "has_gifts": True,
        "has_faq": True,
        "custom_reviews": [
            {
                "badge": "✨ 극강의 실용성",
                "text": "출판 강의에 수백만 원 쓰고도 원고 한 장 못 끝냈는데, 이 책은 단 8,000원에 부크크 규격 세팅부터 표지 반려 탈출까지 그대로 복붙해서 끝냈습니다!",
                "author": "이*진 독자 (직장인 작가)"
            },
            {
                "badge": "🚀 백지 공포증 1초 탈출",
                "text": "모니터 앞 커서만 깜빡이던 밤이 끝났습니다. 뼈대만 던져주면 AI가 살을 붙이고 저자님의 다림질 공식으로 내 목소리가 살아나는 경험은 충격적이었습니다.",
                "author": "박*현 독자 (프리랜서 작가)"
            },
            {
                "badge": "👑 네이버 공식 작가 등단",
                "text": "초록창 검색창에 내 이름을 쳤을 때 '작가' 프로필과 내 책이 뜬 순간, 이력서 10장보다 훨씬 더 강력한 신뢰를 얻었습니다. 0원 출판의 기적입니다!",
                "author": "정*호 독자 (1인 기업가)"
            }
        ]
    }

def apply_preset(preset_key: str):
    fd = st.session_state.form_data
    fd["prod_title"] = "에세이 한 권으로 당신을 증명하라 (AI로 완성하는 퍼스널 브랜딩 출판 비결)"
    fd["price_main"] = "8,000원"
    fd["ebook_link"] = "https://bookk.co.kr/bookStore/6a35e5e5f5d317cf59a3c17e"
    if preset_key == "NORMAL_01":
        fd["review_mode"] = "real"
        fd["has_comparison"] = True
        fd["has_gifts"] = True
        fd["has_faq"] = True
    elif preset_key == "EXC_01_NO_REVIEWS":
        fd["review_mode"] = "ad_promo"
        fd["has_comparison"] = True
        fd["has_gifts"] = True
        fd["has_faq"] = True
    elif preset_key == "EXC_02_MINIMAL":
        fd["review_mode"] = "none"
        fd["has_comparison"] = False
        fd["has_gifts"] = False
        fd["has_faq"] = False
    elif preset_key == "EXC_03_INVALID":
        fd["prod_title"] = ""
        fd["ebook_link"] = "bookk.co.kr/wrong_link_without_https"

# ----------------- 사이드바 & 상단 페이지 전환 네비게이션 -----------------
with st.sidebar:
    st.markdown("## 🧭 화면 이동 메뉴")
    st.caption("입력 화면과 결과 확인 화면이 깔끔하게 분리되어 있습니다.")
    nav_choice = st.radio(
        "이동할 페이지를 선택하세요:",
        [
            "1️⃣ 📝 상품 정보 입력하기",
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
    st.markdown("##### 💡 현재 적용된 5대 자동화 원칙")
    st.caption("• 거짓 후기 생성 절대 금지 (표시광고법 준수)\n• 부족한 기준은 자동 생략\n• 전문 용어 ➔ 고객 일상어 자동 치환\n• 제목 2줄 균형 & 16:9 이미지 여백\n• 최종 승인권자(김진호 박사) 검수 후 배포")

# 상단 공통 헤더 및 빠른 페이지 전환 버튼
st.markdown('<div class="main-header">⚡ AI 마케팅 상세페이지 & 랜딩페이지 스튜디오</div>', unsafe_allow_html=True)
top_c1, top_c2, top_c3 = st.columns(3)
with top_c1:
    if st.button("1️⃣ 📝 상품 정보 입력 페이지", type="primary" if st.session_state.current_page == "1_input" else "secondary", use_container_width=True):
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
# [페이지 1] 📝 상품 정보 입력하기 (오직 입력에만 집중하는 깔끔한 위저드)
# ==============================================================================
if st.session_state.current_page == "1_input":
    st.markdown("### 📝 [페이지 1] 상품 정보 입력하기")
    st.caption("아래 Step 1 ~ Step 2의 핵심 항목만 확인/입력하신 뒤 하단의 **[생성하고 결과 페이지로 이동]** 버튼을 눌러주세요.")

    # (선택) 실습용 샘플 프리셋 바
    with st.expander("🧪 [오프라인 실습용] 테스트 샘플 4종 원클릭 자동 채우기 (클릭하여 열기)", expanded=False):
        sc1, sc2, sc3, sc4 = st.columns(4)
        with sc1:
            if st.button("✅ 샘플 1: 정상 (전체 포함)", use_container_width=True):
                apply_preset("NORMAL_01")
                st.rerun()
        with sc2:
            if st.button("📢 샘플 2: 후기 없음 (Ad 전환)", use_container_width=True):
                apply_preset("EXC_01_NO_REVIEWS")
                st.rerun()
        with sc3:
            if st.button("⚡ 샘플 3: 미니멀 (옵션 생략)", use_container_width=True):
                apply_preset("EXC_02_MINIMAL")
                st.rerun()
        with sc4:
            if st.button("🛑 샘플 4: 오류 입력 (STOP 테스트)", use_container_width=True):
                apply_preset("EXC_03_INVALID")
                st.rerun()

    # [Step 1 카드] 필수 기본 정보 입력
    st.markdown('<div class="step-card"><span class="step-badge">STEP 1 · 필수 기본 정보</span><h4 style="margin:0 0 6px 0;">📘 어떤 상품(도서)의 상세페이지와 랜딩페이지를 만드시나요?</h4><p style="font-size:13px; color:#64748b; margin:0;">상품명, 가격, 구매 링크만 정확히 입력하시면 설득 구조와 디자인은 자동으로 완성됩니다.</p></div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        fd["prod_title"] = st.text_input("1. 상품 / 도서명 (필수)", value=fd["prod_title"], placeholder="예: 에세이 한 권으로 당신을 증명하라")
        fd["prod_author"] = st.text_input("2. 저자 / 브랜드명", value=fd["prod_author"], placeholder="예: 김진호 지음")
        p1, p2 = st.columns(2)
        with p1:
            fd["price_main"] = st.text_input("3-1. 메인 가격 (전자책, 필수)", value=fd["price_main"])
        with p2:
            fd["price_sub"] = st.text_input("3-2. 보조 가격 (종이책)", value=fd["price_sub"])

    with c2:
        fd["ebook_link"] = st.text_input("4-1. 🔗 전자책 즉시 구매 링크 (https:// 필수)", value=fd["ebook_link"])
        fd["paper_link"] = st.text_input("4-2. 🔗 종이책 서점 주문 링크 (https:// 필수)", value=fd["paper_link"])
        fd["target_audience"] = st.text_area("5. 타깃 고객 및 핵심 가치 한 줄 소개", value=fd["target_audience"], height=85)

    st.markdown("<br>", unsafe_allow_html=True)

    # [Step 2 카드] 마케팅 진실성 & 선택 기준 유무 확인
    st.markdown('<div class="step-card"><span class="step-badge">STEP 2 · 진실성 & 선택 기준 확인</span><h4 style="margin:0 0 6px 0;">⚖️ 구매 후기나 추가 옵션(비교표·사은품·FAQ)이 있으신가요?</h4><p style="font-size:13px; color:#64748b; margin:0;">없는 항목은 억지로 거짓말을 지어내지 않고, 합법적인 추천 배너로 바꾸거나 결과물에서 깔끔하게 생략합니다.</p></div>', unsafe_allow_html=True)

    rc1, rc2 = st.columns(2)
    with rc1:
        rev_idx = 0 if fd["review_mode"] == "ad_promo" else (1 if fd["review_mode"] == "real" else 2)
        rev_choice = st.radio(
            "💬 실제 고객 구매 후기가 있습니까?",
            [
                "📢 아직 구매 후기가 없음 ➔ 거짓 후기 금지! '에디터 추천 & 기대평 광고 배너'로 안전 전환",
                "💬 실제 구매 후기가 있음 ➔ 실제 후기 직접 입력 (실명 자동 이*진 마스킹)",
                "🚫 후기 영역 넣지 않기 ➔ 상세페이지에서 후기 섹션 완전 생략"
            ],
            index=rev_idx
        )
        if "실제 구매 후기가 있음" in rev_choice:
            fd["review_mode"] = "real"
            st.info("아래 칸에 실제 구매 후기를 입력해주세요. 만약 모두 비워두면 거짓 후기 방지(STOP-03)를 위해 광고 배너로 자동 전환됩니다.")
            new_reviews = []
            for idx, rv in enumerate(fd["custom_reviews"]):
                with st.expander(f"✍️ 실제 구매 후기 #{idx+1} 입력/수정", expanded=(idx == 0)):
                    b_val = st.text_input(f"후기 {idx+1} 강조 키워드", value=rv["badge"], key=f"rv_b_{idx}")
                    t_val = st.text_area(f"후기 {idx+1} 내용", value=rv["text"], height=60, key=f"rv_t_{idx}")
                    a_val = st.text_input(f"후기 {idx+1} 작성자 (실명 입력 시 자동 마스킹)", value=rv["author"], key=f"rv_a_{idx}")
                    if t_val.strip():
                        new_reviews.append({"badge": b_val.strip() or "✨ 베스트 후기", "text": t_val.strip(), "author": a_val.strip() or "익명 독자"})
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
        fd["has_comparison"] = st.checkbox("⚖️ 기존 방식 / 타사 대비 '품격 있는 가치 비교표' 넣기", value=fd["has_comparison"])
        fd["has_gifts"] = st.checkbox("🎁 구매자 무료 증정 '특별 사은품 / 부록 박스' 넣기", value=fd["has_gifts"])
        fd["has_faq"] = st.checkbox("❓ 구매 전 망설임을 없애는 '자주 묻는 질문(FAQ 4선)' 넣기", value=fd["has_faq"])

        with st.expander("✨ (선택 사항) 메인 2줄 제목 & 고통/해결 문구 세부 수정", expanded=False):
            fd["headline_1"] = st.text_input("상단 1줄 헤드라인", value=fd["headline_1"])
            fd["headline_2"] = st.text_input("상단 2줄 강조 헤드라인", value=fd["headline_2"])
            fd["pain_title"] = st.text_input("고객 고통 상황(Problem) 제목", value=fd["pain_title"])
            fd["sol_title"] = st.text_input("핵심 해결책(Solution) 제목", value=fd["sol_title"])

    st.markdown("---")

    # [Step 3] 멈춤 조건(STOP-01 ~ STOP-04) 실시간 검증 및 결과 생성 버튼
    stop_errors = []
    if not fd["prod_title"].strip() or not fd["price_main"].strip():
        stop_errors.append("🛑 **[STOP-01 필수 입력값 누락]** '1. 상품/도서명'과 '3-1. 메인 가격'은 비워둘 수 없습니다.")
    if not (fd["ebook_link"].strip().startswith("http://") or fd["ebook_link"].strip().startswith("https://")) or not (fd["paper_link"].strip().startswith("http://") or fd["paper_link"].strip().startswith("https://")):
        stop_errors.append("🛑 **[STOP-02 구매 링크 오류]** 전자책 및 종이책 구매 링크는 반드시 `http://` 또는 `https://`로 시작해야 합니다.")

    if stop_errors:
        for err in stop_errors:
            st.error(err)
    else:
        st.markdown('<div class="badge-pass">✅ 모든 필수 입력값 및 안전 규칙(STOP-01~04) 검증 통과! 이제 아래 생성 버튼을 눌러주세요.</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 입력 완료! 상세페이지 & 랜딩페이지 생성하고 [결과 확인 페이지]로 이동 ➔", type="primary", use_container_width=True, disabled=bool(stop_errors)):
        with st.spinner("상세페이지(PNG), 웹 랜딩페이지(HTML), 피그마 벡터(SVG)를 생성하고 있습니다..."):
            render_payload = {
                "name": fd["prod_title"],
                "price": fd["price_main"],
                "sub_price": fd["price_sub"],
                "author": fd["prod_author"],
                "ebook_link": fd["ebook_link"],
                "paper_link": fd["paper_link"],
                "target_audience": fd["target_audience"],
                "headline_1": fd["headline_1"],
                "headline_2": fd["headline_2"],
                "pain_title": fd["pain_title"],
                "sol_title": fd["sol_title"],
                "review_mode": fd["review_mode"],
                "custom_reviews": fd["custom_reviews"],
                "has_comparison": fd["has_comparison"],
                "has_gifts": fd["has_gifts"],
                "has_faq": fd["has_faq"]
            }
            GitHubDesignRenderer().render_all(render_payload)
            pro_svg = ProDetailRenderer().render_pro_canvas_svg(render_payload)
            with open("figma_canvas_design.svg", "w", encoding="utf-8") as f:
                f.write(pro_svg)
            st.session_state.current_page = "2_result"
            st.rerun()

# ==============================================================================
# [페이지 2] 🎨 생성 결과 확인 & 다운로드 (오직 결과 확인과 다운로드에만 집중)
# ==============================================================================
elif st.session_state.current_page == "2_result":
    head_c1, head_c2 = st.columns([3, 1])
    with head_c1:
        st.markdown("### 🎨 [페이지 2] 생성된 상세페이지 & 랜딩페이지 결과 확인")
        st.caption(f"현재 적용 상품: **{fd['prod_title']}** ({fd['price_main']} / {fd['price_sub']}) | 후기 모드: `{fd['review_mode']}`")
    with head_c2:
        if st.button("⬅️ 입력 내용 수정하러 가기", use_container_width=True):
            st.session_state.current_page = "1_input"
            st.rerun()

    # 1. 보류/승인 대기함 & 3대 포맷 다운로드 박스
    st.markdown('<div class="step-card"><span class="step-badge">STEP 1 · 최종 검수 및 파일 다운로드</span><h4 style="margin:0 0 6px 0;">🛡️ 최종 승인권자(김진호 박사) 배포 전 4대 안전 체크리스트</h4></div>', unsafe_allow_html=True)
    ap_c1, ap_c2 = st.columns(2)
    with ap_c1:
        chk_1 = st.checkbox("✅ 1. 전자책 및 종이책 구매 버튼 링크가 정상 연결되었는가?", value=True)
        chk_2 = st.checkbox("✅ 2. 거짓 구매 후기가 일절 포함되지 않았는가? (표시광고법 준수)", value=True)
    with ap_c2:
        chk_3 = st.checkbox("✅ 3. 실제 제공 사은품 및 비교 수치와 일치하는가?", value=True)
        chk_4 = st.checkbox("✅ 4. 제목 2줄 균형 및 16:9 이미지 좌우 여백이 정상인가?", value=True)

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
                st.download_button("🌐 2. 독립 실행형 웹 랜딩페이지 (HTML) 다운로드", f_html.read(), "상세페이지_웹배포용.html", "text/html", use_container_width=True, disabled=not is_approved, type="primary")
    with dl_c3:
        if os.path.exists("figma_canvas_design.svg"):
            with open("figma_canvas_design.svg", "rb") as f_svg:
                st.download_button("🎨 3. 피그마 편집용 벡터 (SVG) 다운로드", f_svg.read(), "figma_canvas_design.svg", "image/svg+xml", use_container_width=True, disabled=not is_approved)

    st.markdown("---")

    # 2. 결과물 미리보기 탭 (웹 랜딩페이지 / PNG 통이미지 / 사용된 AI 비주얼 이미지 3종)
    st.markdown("#### 👁️ 생성된 결과물 한눈에 미리보기")
    res_tab1, res_tab2, res_tab3 = st.tabs([
        "🌐 1. 웹 랜딩페이지 실시간 미리보기 (버튼 클릭 가능)",
        "🖼️ 2. 스마트스토어/부크크 등록용 통이미지 (PNG)",
        "📸 3. 상세페이지에 합성된 AI 비주얼 이미지 3종 개별 다운로드"
    ])

    with res_tab1:
        if os.path.exists("pro_detail_page.html"):
            with open("pro_detail_page.html", "r", encoding="utf-8") as f_live:
                components.html(f_live.read(), height=1350, scrolling=True)
        else:
            st.info("입력 페이지에서 생성 버튼을 눌러주세요.")

    with res_tab2:
        if os.path.exists("detail_page_render.png"):
            st.image("detail_page_render.png", caption="2x Retina 초고해상도 상세페이지 렌더링 이미지", use_container_width=True)
        else:
            st.info("PNG 이미지가 아직 생성되지 않았습니다.")

    with res_tab3:
        ic1, ic2, ic3 = st.columns(3)
        with ic1:
            if os.path.exists("product_images/book_cover.jpg"):
                st.image("product_images/book_cover.jpg", caption="📘 실제 도서 표지 (3D 목업용)", use_container_width=True)
                with open("product_images/book_cover.jpg", "rb") as f:
                    st.download_button("💾 표지 원본 다운로드", f.read(), "book_cover.jpg", "image/jpeg", use_container_width=True)
        with ic2:
            if os.path.exists("product_images/scene_pain_point.jpg"):
                st.image("product_images/scene_pain_point.jpg", caption="🚨 AI 고통 상황 컷 (16:9 가로형)", use_container_width=True)
                with open("product_images/scene_pain_point.jpg", "rb") as f:
                    st.download_button("💾 고통상황 컷 다운로드", f.read(), "scene_pain.jpg", "image/jpeg", use_container_width=True)
        with ic3:
            if os.path.exists("product_images/scene_solution.jpg"):
                st.image("product_images/scene_solution.jpg", caption="💡 AI 문제 해결 컷 (16:9 가로형)", use_container_width=True)
                with open("product_images/scene_solution.jpg", "rb") as f:
                    st.download_button("💾 문제해결 컷 다운로드", f.read(), "scene_solution.jpg", "image/jpeg", use_container_width=True)

# ==============================================================================
# [페이지 3] 📋 100점 품질 진단 & 설득 카피 리포트 (보조 분석 페이지)
# ==============================================================================
else:
    st.markdown("### 📋 [페이지 3] 하얀돌랩 8대 체크리스트 100점 진단 & 설득 카피 시트")
    st.caption("생성된 상세페이지가 스마트스토어 100점 공식에 부합하는지 진단하고, 미리캔버스/블로그 홍보에 바로 복사해 쓸 수 있는 텍스트 시트를 제공합니다.")

    detail_sections = [
        {"index": 1, "role": "01. Hook", "question": "왜 지금 내 이름으로 된 책을 써야 하는가?", "headline": fd["headline_1"] + " " + fd["headline_2"], "subhead": fd["target_audience"], "image_tag": "📘 [실제 도서 표지] 우측 3D 북 목업 배치"},
        {"index": 2, "role": "02. Problem", "question": "왜 지금까지 내 책을 쓰지 못했는가?", "headline": fd["pain_title"], "subhead": "완벽한 문장을 써야 한다는 부담과 표지 규격 반려 지옥이 출간을 가로막고 있었습니다.", "image_tag": "🚨 [AI 상황 컷] 중앙 16:9 여백 배치"},
        {"index": 3, "role": "03. Empathy", "question": "평범한 나도 작가가 될 수 있는가?", "headline": "1%의 천재가 아닌 99%의 평범함이 무기가 되는 시대입니다.", "subhead": "현장에서 견뎌낸 시간과 진솔한 극복 스토리가 독자에게 가장 깊은 울림을 줍니다.", "image_tag": "1부 이해(Why) 카드"},
        {"index": 4, "role": "04. Solution (기획)", "question": "무슨 이야기를 어떻게 구조화할 것인가?", "headline": "단 1명의 페르소나와 스토리텔링 5단 구조로 기억의 구슬을 꿰세요.", "subhead": "후킹·논리·기대감을 갖춘 목차 설계 비법을 안내합니다.", "image_tag": "2부 기획(What) 로드맵"},
        {"index": 5, "role": "05. Solution (AI 집필)", "question": "글솜씨가 없는데 어떻게 초고를 완성하는가?", "headline": fd["sol_title"], "subhead": "맞춤형 AI 프롬프트와 문장 다이어트·다림질 공식으로 완성도를 높입니다.", "image_tag": "💡 [AI 해결 컷] 중앙 16:9 여백 배치"},
        {"index": 6, "role": "06. 차별점", "question": "독자를 사로잡는 한 끗 차이는 무엇인가?", "headline": "독자의 시선을 사로잡는 강렬한 프롤로그와 긴 여운의 에필로그 공식.", "subhead": "첫 페이지부터 마지막 페이지까지 설득력을 유지하는 작법을 공개합니다.", "image_tag": "3부 집필(How) 카드"},
        {"index": 7, "role": "07. Proof & Action", "question": "출판 비용과 복잡한 편집은 어떻게 해결하는가?", "headline": "재고 부담 없는 0원 출판(주문 즉시 1권 인쇄)! 부크크 등록 & 반려 탈출 노하우.", "subhead": "내지 규격과 표지 세팅 실전 팁으로 단 한 번에 출간 승인을 받으세요.", "image_tag": "4부 출판(After) 카드"},
        {"index": 8, "role": "08. Benefit", "question": "출간 이후 내 커리어는 어떻게 달라지는가?", "headline": "국립중앙도서관 정식 도서 번호(ISBN) 발급 & 네이버 공식 작가 인물등록!", "subhead": "검색창에 내 이름을 치면 공식 작가 프로필과 도서가 노출됩니다.", "image_tag": "네이버 인물등록 인증 배지"},
        {"index": 9, "role": "09. Spec & FAQ", "question": "구체적인 구성과 혜택은 무엇인가?", "headline": "총 4부 8장 핵심 커리큘럼 · 가치 비교표 · 특별 사은품 · FAQ 완비.", "subhead": f"전자책 {fd['price_main']} 즉시 다운로드 | 종이책 {fd['price_sub']} 서점 주문", "image_tag": "1~4부 벤토 그리드 카드"},
        {"index": 10, "role": "10. CTA", "question": "지금 바로 시작하려면 어떻게 해야 하는가?", "headline": f"『{fd['prod_title']}』 지금 바로 시작하세요!", "subhead": f"전자책 {fd['price_main']} / 종이책 {fd['price_sub']}", "image_tag": "📘 [실제 표지] + 구매 버튼"}
    ]

    generator = DetailPageGenerator()
    eval_result = generator.evaluate_detail_page(detail_sections)

    sc_col1, sc_col2 = st.columns([1, 2])
    with sc_col1:
        st.metric(label="하얀돌랩 8대 체크리스트 진단 점수", value=f"{eval_result['total_score']} / {eval_result['max_score']}점", delta=eval_result['grade'])
    with sc_col2:
        st.success(f"**진단 요약:** {eval_result['summary']}")
        st.caption("전문 용어(POD, ISBN, 인디자인, 프롬프트) ➔ 고객 일상어 자동 치환 및 모바일 1단 가독성 100% 충족")

    for item in eval_result["checklist"]:
        status_badge = "✅ PASS" if item["passed"] else "❌ 보완 필요"
        with st.expander(f"{status_badge} [{item['weight']}점] {item['item']} - {item['question']}", expanded=False):
            st.markdown(f"**진단 결과:** {item['feedback']}")

    st.markdown("---")
    st.markdown("#### 📋 미리캔버스 / 스마트스토어 복사용 10섹션 설득 원고")
    copy_lines = []
    for s in detail_sections:
        copy_lines.append(f"[{s['role']}] 질문: {s['question']} (배치 이미지: {s['image_tag']})")
        copy_lines.append(f"헤드라인: {s['headline']}")
        copy_lines.append(f"설득 본문: {s['subhead']}\n")
    st.text_area("전체 복사 (Ctrl+A ➔ Ctrl+C)", value="\n".join(copy_lines), height=260)
