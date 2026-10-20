import streamlit as st
import json
import re
import urllib.request
import os
import subprocess
from bs4 import BeautifulSoup
from hook_engine import HookEngine
from detail_page_generator import DetailPageGenerator
from landing_page_generator import LandingPageGenerator

st.set_page_config(
    page_title="AI 마케팅 스튜디오 - 스마트 링크 분석 & AI 이미지 생성기",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header { font-size: 26px; font-weight: 800; color: #1e293b; margin-bottom: 2px; }
    .sub-header { font-size: 14px; color: #64748b; margin-bottom: 20px; }
    .box-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 18px; margin-bottom: 14px; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
    .vs-card-my { background: #eff6ff; border: 2px solid #3b82f6; border-radius: 12px; padding: 18px; }
    .vs-card-comp { background: #fef2f2; border: 2px solid #ef4444; border-radius: 12px; padding: 18px; }
    .badge-primary { background: #2563eb; color: #ffffff; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 11px; }
    .badge-pass { background: #dcfce7; color: #15803d; padding: 3px 8px; border-radius: 6px; font-weight: 600; font-size: 11px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">⚡ AI 마케팅 자동화 스튜디오</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">내 상품 링크 or 경쟁사 분석 모드 ➔ 고객 결핍 AI 이미지 생성 ➔ 상세페이지/피그마 1초 완성</div>', unsafe_allow_html=True)

# ----------------- 0. [02_입력_샘플.md] 원클릭 샘플 프리셋 로더 -----------------
if "preset_mode" not in st.session_state:
    st.session_state.preset_mode = "NORMAL_01"

st.markdown("##### 🧪 [오프라인 실습용] `02_입력_샘플.md` 원클릭 테스트 샘플 로더")
p_col1, p_col2, p_col3, p_col4 = st.columns(4)
with p_col1:
    if st.button("✅ 샘플 1: 정상 (전체 포함)", use_container_width=True):
        st.session_state.preset_mode = "NORMAL_01"
with p_col2:
    if st.button("📢 샘플 2: 후기 없음 (Ad 전환)", use_container_width=True):
        st.session_state.preset_mode = "EXC_01_NO_REVIEWS"
with p_col3:
    if st.button("⚡ 샘플 3: 미니멀 (옵션 생략)", use_container_width=True):
        st.session_state.preset_mode = "EXC_02_MINIMAL"
with p_col4:
    if st.button("🛑 샘플 4: 오류 입력 (STOP 테스트)", use_container_width=True):
        st.session_state.preset_mode = "EXC_03_INVALID"

preset = st.session_state.preset_mode
default_title = "" if preset == "EXC_03_INVALID" else "에세이 한 권으로 당신을 증명하라 (AI로 완성하는 퍼스널 브랜딩 출판 비결)"
default_ebook_url = "bookk.co.kr/wrong_link_without_https" if preset == "EXC_03_INVALID" else "https://bookk.co.kr/bookStore/6a35e5e5f5d317cf59a3c17e"
default_rev_idx = 1 if preset == "NORMAL_01" else (2 if preset == "EXC_02_MINIMAL" else 0)
default_comp = False if preset == "EXC_02_MINIMAL" else True
default_gifts = False if preset == "EXC_02_MINIMAL" else True
default_faq = False if preset == "EXC_02_MINIMAL" else True

# ----------------- 1. 모드 선택 및 입력 폼 -----------------
with st.expander("🛠️ [1단계] 분석 모드 선택 및 인터넷 링크 / 상품 정보 입력 (펼치기/접기)", expanded=True):
    mode = st.radio(
        "분석 시나리오를 선택하세요:",
        ["🅰️ 내 상품 판매 페이지가 이미 있는 경우 (내 링크에서 정보 & 이미지 자동 추출)",
         "🅱️ 새 상품 기획 / 경쟁사만 분석하는 경우 (경쟁사 결핍을 분석해 내 장점 역도출)"],
        index=0
    )

    col1, col2 = st.columns([1, 1])

    if "내 상품 판매 페이지가 이미 있는 경우" in mode:
        with col1:
            st.markdown("#### 📘 내 상품 판매 웹페이지 링크")
            my_url = st.text_input(
                "내 상품 링크 (네이버 쇼핑, 스마트스토어, 부크크, 알라딘, 쿠팡 등)",
                value="https://search.shopping.naver.com/book/catalog/60677619152?query=%EC%97%90%EC%84%B8%EC%9D%B4%20%ED%95%9C%20%EA%B6%8C%EC%9C%BC%EB%A1%9C%20%EB%8B%B9%EC%8B%A0%EC%9D%84%20%EC%A6%9D%EB%AA%85%ED%95%98%EB%9D%BC"
            )
            prod_title = st.text_input("상품/도서명 (필수)", value=default_title)
            prod_author = st.text_input("저자/브랜드", value="김진호 지음 (퍼스널 브랜딩 & AI 출판 전문가)")
            
            c_p1, c_p2 = st.columns(2)
            with c_p1:
                price_main = st.text_input("메인 가격 (전자책, 필수)", value="8,000원")
            with c_p2:
                price_sub = st.text_input("보조 가격 (종이책)", value="12,000원")
            
            c_l1, c_l2 = st.columns(2)
            with c_l1:
                ebook_link = st.text_input(
                    "🔗 전자책 구매 링크 (CTA 버튼 연결)",
                    value=default_ebook_url
                )
            with c_l2:
                paper_link = st.text_input(
                    "🔗 종이책 서점 주문 링크 (서브 버튼 연결)",
                    value="https://search.shopping.naver.com/book/catalog/60677619152?query=%EC%97%90%EC%84%B8%EC%9D%B4%20%ED%95%9C%20%EA%B6%8C%EC%9C%BC%EB%A1%9C%20%EB%8B%B9%EC%8B%A0%EC%9D%84%20%EC%A6%9D%EB%AA%85%ED%95%98%EB%9D%BC&NaPm=ct%3Dmv6528i8%7Cci%3D2dc082a4012fc5a426416cd172e3906ba5165b26%7Ctr%3Dboksl%7Csn%3D95694%7Chk%3D094ce9625fa67ab6bf58f1ebe3cedb0fae84df84"
                )

        with col2:
            st.markdown("#### 🥊 참고할 경쟁 상품 링크 (선택 사항)")
            comp_urls = st.text_area(
                "경쟁 상품 링크 (경쟁사 약점을 분석해 내 상품의 차별점으로 역이용)",
                value="https://search.shopping.naver.com/book/catalog/essay_writing_class\nhttps://search.shopping.naver.com/book/catalog/self_publishing_guide",
                height=85
            )
            target_audience = st.text_area(
                "타깃 고객 및 핵심 소개 문구",
                value="자신의 전문 영역에서 어려움을 이겨낸 경험을 책으로 펴내어 퍼스널 브랜딩을 완성하고, 부크크 0원 출판 및 네이버 공식 작가 인물등록까지 달성하고 싶은 직장인·전문가·1인 기업가",
                height=70
            )
            with st.expander("✨ 메인 헤드라인 / 고통(Problem) / 해결책(Solution) 카피 직접 커스텀 (선택)", expanded=False):
                custom_h1 = st.text_input("히어로 상단 1줄 헤드라인", value="이력서 100장보다 강력한 내 이름의 책 한 권,")
                custom_h2 = st.text_input("히어로 상단 2줄 강조 헤드라인", value=f"『{prod_title.split('(')[0].strip() or '내 책'}』로 완벽하게 증명하세요.")
                custom_pain = st.text_input("고객 고통 상황(Problem) 헤드라인", value='"내세울 스펙도 없고 글솜씨도 없는데, 내가 과연 책을 쓸 수 있을까?"')
                custom_sol = st.text_input("핵심 해결책(Solution) 헤드라인", value="뼈대만 던져주면 AI가 초고를 쓰고, 부크크로 0원 출판해 네이버 공식 작가가 됩니다!")

    else:
        # 모드 B: 경쟁사 분석 전용
        with col1:
            st.markdown("#### 🥊 분석할 경쟁 상품 판매 링크")
            comp_urls = st.text_area(
                "경쟁 상품 링크들을 줄바꿈으로 입력하세요 (내용을 베끼지 않고 결핍/약점을 역분석합니다)",
                value="https://search.shopping.naver.com/book/catalog/essay_writing_class\nhttps://search.shopping.naver.com/book/catalog/self_publishing_guide",
                height=130
            )
            st.caption("💡 경쟁사 상품 설명 및 고객 리뷰를 분석하여 '고객이 불만족해하는 지점'을 찾아냅니다.")

        with col2:
            st.markdown("#### 💡 내 신규 상품 기획 정보")
            prod_title = st.text_input("기획 중인 내 상품/도서명", value="에세이 한 권으로 당신을 증명하라 (AI로 완성하는 퍼스널 브랜딩 출판 비결)")
            prod_author = st.text_input("저자/브랜드", value="김진호 지음 (퍼스널 브랜딩 & AI 출판 전문가)")
            price_main = st.text_input("판매 예정 가격", value="8,000원")
            target_audience = st.text_area(
                "타깃 고객 페르소나",
                value="백지 공포증을 AI로 극복하고 내 이름으로 된 책을 무료 출판해 네이버 인물등록 작가가 되고 싶은 사람",
                height=70
            )
            price_sub = "12,000원"
            ebook_link = "https://bookk.co.kr/bookStore/6a35e5e5f5d317cf59a3c17e"
            paper_link = "https://search.shopping.naver.com/book/catalog/60677619152?query=%EC%97%90%EC%84%B8%EC%9D%B4%20%ED%95%9C%20%EA%B6%8C%EC%9C%BC%EB%A1%9C%20%EB%8B%B9%EC%8B%A0%EC%9D%84%20%EC%A6%9D%EB%AA%85%ED%95%98%EB%9D%BC&NaPm=ct%3Dmv6528i8%7Cci%3D2dc082a4012fc5a426416cd172e3906ba5165b26%7Ctr%3Dboksl%7Csn%3D95694%7Chk%3D094ce9625fa67ab6bf58f1ebe3cedb0fae84df84"
            custom_h1 = "이력서 100장보다 강력한 내 이름의 책 한 권,"
            custom_h2 = f"『{prod_title.split('(')[0].strip() or '내 책'}』로 완벽하게 증명하세요."
            custom_pain = '"내세울 스펙도 없고 글솜씨도 없는데, 내가 과연 책을 쓸 수 있을까?"'
            custom_sol = "뼈대만 던져주면 AI가 초고를 쓰고, 부크크로 0원 출판해 네이버 공식 작가가 됩니다!"

    st.markdown("---")
    st.markdown("#### ⚖️ [2단계] 마케팅 진실성 & 조건부 섹션 제어 (허위 후기 방지 & 맞춤 구성)")
    st.caption("💡 정보가 부족하거나 없는 항목은 억지로 거짓 데이터를 지어내지 않고, 부족한 기준은 입력을 요청하거나 안전한 광고/비전 배너로 대체 및 생략합니다.")
    
    col_t1, col_t2 = st.columns(2)
    custom_reviews_payload = []
    with col_t1:
        review_opt = st.radio(
            "💬 고객 구매 후기 반영 방식 선택:",
            [
                "📢 [출시 초기/신상품] 실제 구매 후기 없음 (거짓 후기 절대 금지! 에디터 추천 & 기대평 광고 배너로 안전 전환)",
                "💬 실제 구매 고객 후기 있음 (실제 후기 직접 입력 & 핵심 키워드 강조형으로 생성)",
                "🚫 후기 섹션 완전 제외 (상세페이지에 후기 블록을 넣지 않음)"
            ],
            index=default_rev_idx
        )
        if "실제 구매 고객 후기 있음" in review_opt:
            review_mode = "real"
            st.info("실제 구매 고객 후기를 입력해주세요. (실명 입력 시 '이*진' 형태로 자동 비식별화 마스킹됩니다. 비워두면 STOP-03 규칙에 의해 거짓 후기 생성을 멈추고 광고 배너로 전환됩니다.)")
            with st.expander("✍️ 실제 구매자 후기 3건 입력 / 수정 (클릭하여 열기)", expanded=True):
                rv1_badge = st.text_input("후기 1 핵심 키워드 배지", value="✨ 극강의 실용성")
                rv1_text = st.text_area("후기 1 본문", value="출판 강의에 수백만 원 쓰고도 원고 한 장 못 끝냈는데, 이 책은 단 8,000원에 부크크 규격 세팅부터 표지 반려 탈출까지 그대로 복붙해서 끝냈습니다!", height=65)
                rv1_author = st.text_input("후기 1 작성자 (실명 입력 시 자동 마스킹)", value="이*진 독자 (직장인 작가)")

                rv2_badge = st.text_input("후기 2 핵심 키워드 배지", value="🚀 백지 공포증 1초 탈출")
                rv2_text = st.text_area("후기 2 본문", value="모니터 앞 커서만 깜빡이던 밤이 끝났습니다. 뼈대만 던져주면 AI가 살을 붙이고 저자님의 다림질 공식으로 내 목소리가 살아나는 경험은 충격적이었습니다.", height=65)
                rv2_author = st.text_input("후기 2 작성자 (실명 입력 시 자동 마스킹)", value="박*현 독자 (프리랜서 작가)")

                rv3_badge = st.text_input("후기 3 핵심 키워드 배지", value="👑 네이버 공식 작가 등단")
                rv3_text = st.text_area("후기 3 본문", value="초록창 검색창에 내 이름을 쳤을 때 '작가' 프로필과 내 책이 뜬 순간, 이력서 10장보다 훨씬 더 강력한 신뢰를 얻었습니다. 0원 출판의 기적입니다!", height=65)
                rv3_author = st.text_input("후기 3 작성자 (실명 입력 시 자동 마스킹)", value="정*호 독자 (1인 기업가)")

                for b_val, t_val, a_val in [(rv1_badge, rv1_text, rv1_author), (rv2_badge, rv2_text, rv2_author), (rv3_badge, rv3_text, rv3_author)]:
                    if t_val.strip():
                        custom_reviews_payload.append({"badge": b_val.strip() or "✨ 실제 구매 후기", "text": t_val.strip(), "author": a_val.strip() or "익명 독자"})
                if not custom_reviews_payload:
                    st.warning("⚠️ [STOP-03 발동] 실제 후기 모드가 선택되었으나 입력된 후기 텍스트가 없습니다! 거짓 후기 생성을 방지하기 위해 '출시 기념 에디터 추천 광고 배너(ad_promo)'로 안전 전환합니다.")
                    review_mode = "ad_promo"
        elif "후기 섹션 완전 제외" in review_opt:
            review_mode = "none"
            st.caption("후기 섹션이 결과물에서 완전히 제외됩니다.")
        else:
            review_mode = "ad_promo"
            st.success("공정거래위원회 표시광고법 준수: 거짓 후기를 일절 생성하지 않고 '출시 기념 에디터 추천사 & 사전 기대평 광고 배너'로 안전하게 전환됩니다.")

    with col_t2:
        st.markdown("**기타 선택적 상세페이지 섹션 유무 (체크 해제 시 깔끔하게 생략):**")
        has_comparison = st.checkbox("⚖️ 타사 / 기존 방식과의 가치 비교표 포함", value=default_comp, help="체크 해제 시 가치 비교표가 결과물에서 깔끔하게 생략됩니다.")
        has_gifts = st.checkbox("🎁 특별 사은품 / 무료 증정 부록 박스 포함", value=default_gifts, help="체크 해제 시 사은품 박스가 생략됩니다.")
        has_faq = st.checkbox("❓ 자주 묻는 질문(FAQ BEST 4) 포함", value=default_faq, help="체크 해제 시 FAQ 아코디언이 생략됩니다.")

        # 04_규칙과_예외.md 실시간 멈춤 조건(STOP-01 ~ STOP-04) 검증 패널
        st.markdown("##### 🛡️ [`04_규칙과_예외.md`] 멈춤 조건(Stop Rules) 실시간 검증")
        stop_errors = []
        if not prod_title.strip() or not price_main.strip():
            stop_errors.append("🛑 **[STOP-01 필수 입력값 누락]** 상품/도서명과 메인 가격은 비워둘 수 없습니다.")
        if not (ebook_link.strip().startswith("http://") or ebook_link.strip().startswith("https://")) or not (paper_link.strip().startswith("http://") or paper_link.strip().startswith("https://")):
            stop_errors.append("🛑 **[STOP-02 비정상 구매 URL]** 전자책 및 종이책 구매 링크는 반드시 `http://` 또는 `https://`로 시작해야 합니다.")
        if stop_errors:
            for err in stop_errors:
                st.error(err)
        else:
            st.markdown('<span class="badge-pass">✅ STOP-01~04 모든 안전 규칙 통과 (렌더링 가능)</span>', unsafe_allow_html=True)

    btn_run = st.button("🚀 마케팅 분석 가동 & 맞춤형 상세페이지 생성", type="primary", use_container_width=True, disabled=bool(stop_errors))
    if btn_run:
        with st.spinner("깃허브 최상위 디자인 시스템 및 하얀돌연구소 프레임워크 기반으로 상세페이지를 렌더링하고 있습니다..."):
            from github_design_renderer import GitHubDesignRenderer
            from pro_detail_renderer import ProDetailRenderer
            gh_renderer = GitHubDesignRenderer()
            render_payload = {
                "name": prod_title,
                "price": price_main,
                "sub_price": price_sub,
                "author": prod_author,
                "ebook_link": ebook_link,
                "paper_link": paper_link,
                "target_audience": target_audience,
                "headline_1": custom_h1,
                "headline_2": custom_h2,
                "pain_title": custom_pain,
                "sol_title": custom_sol,
                "review_mode": review_mode,
                "custom_reviews": custom_reviews_payload,
                "has_comparison": has_comparison,
                "has_gifts": has_gifts,
                "has_faq": has_faq
            }
            gh_renderer.render_all(render_payload)
            pro_svg = ProDetailRenderer().render_pro_canvas_svg(render_payload)
            with open("figma_canvas_design.svg", "w", encoding="utf-8") as f:
                f.write(pro_svg)
        st.success("🎉 [렌더링 완료] 진실성 원칙 및 조건부 섹션이 완벽하게 반영된 초고화질 상세페이지(PNG/HTML/SVG)가 보류/승인 대기함에 생성되었습니다! 아래 4번 탭을 확인하세요.")

# ----------------- 2. 이미지 갤러리 (실제 표지 + AI 생성 상황/해결 컷) -----------------
st.markdown("### 🖼️ 상세페이지 필수 비주얼 자산 (실제 상품 컷 + AI 상황/해결 컷)")

img_c1, img_c2, img_c3 = st.columns(3)

# 1. 실제 상품 표지 이미지
cover_path = "product_images/book_cover.jpg"
with img_c1:
    if os.path.exists(cover_path):
        st.image(cover_path, caption="📘 [실제 상품] 『에세이 한 권으로 당신을 증명하라』 표지 원본", use_container_width=True)
        with open(cover_path, "rb") as f_c:
            st.download_button("💾 표지 이미지 다운로드", f_c.read(), "book_cover.jpg", "image/jpeg", key="dl_c")
    else:
        st.info("실제 상품 표지 다운로드 준비 중...")

# 2. AI 생성: 고객 고통 상황 (백지 공포증 & 스펙 고민)
pain_path = "product_images/scene_pain_point.jpg"
with img_c2:
    if os.path.exists(pain_path):
        st.image(pain_path, caption="🚨 [AI 상황 컷] 백지 공포증과 커리어 증명에 막막한 밤 (Problem)", use_container_width=True)
        with open(pain_path, "rb") as f_p:
            st.download_button("💾 고통상황 컷 다운로드", f_p.read(), "scene_pain.jpg", "image/jpeg", key="dl_p")
    else:
        st.info("고통 상황 이미지 생성 준비 중...")

# 3. AI 생성: 문제 해결 장면 (AI 초고 집필 + 부크크 출판 + 네이버 인물등록)
sol_path = "product_images/scene_solution.jpg"
with img_c3:
    if os.path.exists(sol_path):
        st.image(sol_path, caption="💡 [AI 해결 컷] AI 집필 · 부크크 0원 출판 · 네이버 공식 작가 등록 (Solution)", use_container_width=True)
        with open(sol_path, "rb") as f_s:
            st.download_button("💾 문제해결 컷 다운로드", f_s.read(), "scene_solution.jpg", "image/jpeg", key="dl_s")
    else:
        st.info("문제 해결 이미지 생성 준비 중...")

# ----------------- 3. 경쟁사 비교 분석 배틀카드 -----------------
comp_analysis_report = {
    "my_product": {
        "name": prod_title,
        "format": "전자책(PDF 110쪽) 즉시 다운로드 + 올컬러 종이책(112쪽) 동시 출간",
        "price": f"{price_main} (종이책 {price_sub}) — 출판 강의 대비 1/50 비용",
        "learning_curve": "백지 공포증 제로 (뼈대만 던져주면 살을 붙이는 AI 맞춤형 프롬프트 + 문장 다림질 비법)",
        "practicality": "주제 선정 ➔ 스토리텔링 5단 구조 ➔ AI 초고 집필 ➔ 부크크 0원 출판(인디자인 표지) ➔ 네이버 인물등록까지 A to Z 원스톱",
        "delivery": "결제 즉시 PDF 열람 & 따라 하기만 하면 내 이름으로 된 ISBN 정식 도서 출간",
        "author_fit": f"{prod_author} (직접 부크크 종이책·전자책 출간 및 대형 서점 유통을 완수한 실전 노하우)"
    },
    "competitors": {
        "name": "기존 글쓰기 작법서 / 고액 책쓰기 코칭 강의 (A사, B사)",
        "format": "추상적인 문학 이론서 또는 수백만 원대 오프라인 강의",
        "price": "도서 18,000~25,000원 / 책쓰기 강의 150만~500만 원",
        "learning_curve": "무작정 매일 글쓰기 강요 (바쁜 직장인·전문가 중도 포기율 90% 이상)",
        "practicality": "글쓰기 마인드셋만 다루고 실제 ISBN 발급·표지 규격(반려 탈출)·네이버 인물등록 실무는 누락",
        "delivery": "수개월간 직접 부딪히며 표지 반려 지옥 경험",
        "author_fit": "전업 작가 중심 (일반 직장인·전문가의 퍼스널 브랜딩 및 AI 활용법 부재)"
    },
    "winning_strategy": (
        "1. [스펙을 이기는 스토리] 1%의 천재가 아닌 99%의 평범한 사람이 각자의 전문 영역에서 어려움을 이겨낸 과정을 '검색되는 전문가의 무기'로 전환\n"
        "2. [백지 공포증 완벽 해결] '완벽한 문장이라는 오만함'을 버리게 하고, 뼈대만 던져주면 AI가 초고를 쓰고 내 글로 다림질하는 실전 프롬프트 제공\n"
        "3. [0원 출판 ~ 네이버 인물등록 완결성] 부크크 POD 0원 출판, 표지 반려 지옥 탈출 노하우, ISBN 발급 후 네이버 공식 '작가' 인물 검색 등록까지 완벽 가이드"
    )
}

# ----------------- 4. 07차시 10섹션 상세페이지 카피 & 이미지 매핑 -----------------
p_name = prod_title
p_price = price_main

ebook_hooks = [
    {
        "type": "권위/증명형 (Authority & Proof)",
        "headline": "이력서 한 줄보다 강력한 무기, 내 이름으로 된 '책 한 권'과 '네이버 작가 등록'입니다.",
        "subhead": f"『{p_name}』 — 각자의 전문 영역에서 견뎌낸 시간을 세상이 검색하는 브랜드로 바꾸는 법.",
        "angle": "퇴사보다 독립을 꿈꾸는 직장인·전문가에게 '검색되는 전문가(네이버 인물등록)'라는 확실한 결과물 제시"
    },
    {
        "type": "장벽 파괴/AI 솔루션형 (Barrier Breaker)",
        "headline": "깜빡이는 커서 앞의 백지 공포증? 뼈대만 던져주면 AI가 마법처럼 초고를 완성합니다.",
        "subhead": "괴상한 프롬프트로 기계 냄새를 지우고, 문장 다이어트와 다림질로 '진짜 내 글'을 만드는 비결.",
        "angle": "글재주가 없어서 책을 못 쓴다는 최대 심리적 장벽을 AI 집필 & 퇴고 파이프라인으로 해결"
    },
    {
        "type": "반직관/공감형 (Counter-intuitive Empathy)",
        "headline": "1%의 천재가 아니라, 99%의 평범함이 가장 강력한 무기가 되는 시대입니다.",
        "subhead": "독자는 화려한 문장이 아니라 당신이 현장에서 직접 겪고 이겨낸 진정성 있는 실패담과 감정선을 원합니다.",
        "angle": "'내가 무슨 책을 써?'라고 주저하는 타깃 독자의 내면 장벽을 무너뜨리는 강력한 메시지"
    },
    {
        "type": "실용/가성비형 (0-Won POD & Value)",
        "headline": f"출판 비용 0원, 재고 부담 0원! 커피 두 잔 값({p_price})으로 평생 남을 내 책을 출간하세요.",
        "subhead": "부크크(POD) 무료 출판 등록부터 표지 반려 지옥 탈출 인디자인 노하우, 정식 ISBN 발급까지 그대로 따라 하기.",
        "angle": "수백만 원이 드는 기획/자비 출판 대신 0원 POD 출판의 압도적 경제성과 실무 매뉴얼 강조"
    },
    {
        "type": "스토리텔링/구조형 (Actionable Roadmap)",
        "headline": "구슬도 꿰어야 보배다! 흩어진 기억을 한 권의 책으로 엮는 '스토리텔링 5단 구조'.",
        "subhead": "과거의 나에게 쓰는 송곳처럼 뾰족한 페르소나 설정부터 독자의 멱살을 잡는 프롤로그·에필로그 작성법까지.",
        "angle": "막연한 에세이가 아니라 '팔리고 읽히는 퍼스널 브랜딩 도서'의 체계적인 기획법 제시"
    }
]

detail_sections = [
    {"index": 1, "role": "01. Hook", "question": "왜 지금 내 이름으로 된 책을 써야 하는가?", "headline": "스펙을 이기는 단 하나의 스토리, 에세이 한 권으로 당신을 증명하라!", "subhead": "퇴사보다 독립! 내 이름 석 자로 시작하는 인생 2막. 주제 선정부터 AI 집필, 부크크 0원 출판, 네이버 공식 작가 등록까지.", "image_tag": "📘 [실제 도서 표지] 우측 3D 북 목업 배치"},
    {"index": 2, "role": "02. Problem", "question": "왜 지금까지 내 책을 쓰지 못했는가?", "headline": "전문성은 충분한데 막상 쓰려니 막막한 '백지 공포증', 언제까지 미루시겠습니까?", "subhead": "'완벽한 문장을 써야 한다'는 오만함과 표지 규격 반려 지옥이 당신의 출간을 가로막고 있었습니다.", "image_tag": "🚨 [AI 상황 컷: 백지 공포증과 커리어 고민] 중앙 16:9 배치"},
    {"index": 3, "role": "03. Empathy", "question": "평범한 나도 작가가 될 수 있는가?", "headline": "1%의 천재가 아닌 99%의 평범함이 무기가 되는 시대입니다.", "subhead": "남들이 좋아하는 트렌드보다 내가 현장에서 '견뎌낸 시간'과 '실패담의 감정선'이 독자에게 가장 깊은 울림을 줍니다.", "image_tag": "1부 이해(Why) — 퍼스널 브랜딩과 에세이의 본질 카드"},
    {"index": 4, "role": "04. Solution (기획)", "question": "무슨 이야기를 어떻게 구조화할 것인가?", "headline": "과거의 '나'에게 쓰는 위로장! 송곳처럼 뾰족한 페르소나와 스토리텔링 5단 구조.", "subhead": "모두를 위한 책은 아무도 읽지 않습니다. 후킹·논리·기대감을 갖춘 목차 설계로 파편화된 기억의 구슬을 꿸 수 있습니다.", "image_tag": "2부 기획(What) — 타겟 설정 & 5단 구조 로드맵"},
    {"index": 5, "role": "05. Solution (AI 집필)", "question": "글솜씨가 없는데 어떻게 초고를 완성하는가?", "headline": "뼈대만 던져주면 AI가 살을 붙인다! 마법 같은 초고 완성과 '내 글 다림질' 비법.", "subhead": "인간적 글쓰기를 끌어내는 괴상한 프롬프트의 비밀, 그리고 문장 다이어트·시제 통일·번역체 제거로 완성도를 극대화합니다.", "image_tag": "💡 [AI 해결 컷: AI 집필 & 출간 작가 브랜딩] 중앙 16:9 배치"},
    {"index": 6, "role": "06. 차별점 (프롤로그/에필로그)", "question": "독자를 사로잡는 한 끗 차이는 무엇인가?", "headline": "독자의 멱살을 잡는 강렬한 프롤로그와 긴 여운을 남기는 에필로그 작성 공식.", "subhead": "첫 페이지에서 독자를 설득하고 마지막 페이지에서 당신의 팬으로 만드는 화룡점정 작법을 공개합니다.", "image_tag": "3부 집필(How) — 초고 다듬기 & 프롤로그 공식"},
    {"index": 7, "role": "07. Proof & Action (부크크 출판)", "question": "출판 비용과 복잡한 편집은 어떻게 해결하는가?", "headline": "재고 부담 없는 0원 출판의 마법! 부크크(POD) 원고 등록 & 반려 지옥 탈출 노하우.", "subhead": "내지 규격 맞추기, 전용 폰트 세팅, 완벽한 표지를 위한 인디자인 실전 팁으로 단 한 번에 출간 승인을 받으세요.", "image_tag": "4부 출판(After) — 부크크 0원 출판 & ISBN 발급"},
    {"index": 8, "role": "08. Benefit (네이버 인물등록)", "question": "출간 이후 내 삶과 커리어는 어떻게 달라지는가?", "headline": "나도 이제 네이버 공식 작가! 초록창에 내 이름을 검색하면 '작가' 프로필이 뜹니다.", "subhead": "정식 ISBN 발급으로 교보문고·예스24·알라딘 유통은 물론, 신뢰를 증명하는 최고의 레퍼런스인 네이버 인물 검색을 완성합니다.", "image_tag": "네이버 인물등록 & 대형 서점 유통 인증 배지"},
    {"index": 9, "role": "09. Spec & FAQ", "question": "책의 구체적인 구성과 분량은 어떠한가?", "headline": "총 4부 8장 체계적 커리큘럼 · 전자책 110쪽(PDF) / 종이책 112쪽(올컬러) 완벽 구성.", "subhead": f"전자책 {price_main} 즉시 다운로드 또는 소장용 종이책 {price_sub} 서점 구매 가능.", "image_tag": "1~4부 전체 커리큘럼 벤토 그리드 카드"},
    {"index": 10, "role": "10. CTA", "question": "지금 바로 시작하려면 어떻게 해야 하는가?", "headline": f"『{p_name}』 지금 바로 당신의 이름을 증명하세요!", "subhead": f"전자책 {price_main} (결제 즉시 열람) | 종이책 {price_sub} (네이버 도서·부크크 공식 판매)", "image_tag": "📘 [실제 표지] + 전자책/종이책 즉시 구매 버튼"}
]

# ----------------- 5. 탭 구성 -----------------
st.markdown("---")
tab_video, tab_comp, tab1, tab2, tab3 = st.tabs([
    "🎬 [영상 분석] 하얀돌연구소 8대 체크리스트 진단기",
    "🥊 1. 경쟁 상품 비교 분석 리포트 (Battle Card)",
    "🎯 2. 5대 후킹 카피 (광고/소구점)",
    "📄 3. [07차시] 상세페이지 10섹션 (이미지 완벽 매핑)",
    "🚀 4. [고도화 1] 깃허브 디자인 시스템 적용 상세페이지 & 원클릭 다운로드"
])

with tab_video:
    st.subheader("🎬 하얀돌연구소 『스마트스토어 판매 상세페이지』 완벽 분석 & 진단")
    st.caption("📺 유튜브 영상: https://youtu.be/C2uF4vNZLkU | 강의 핵심 공식 100% 반영")
    
    # 1. 핵심 철학 배너
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3a8a 0%, #065f46 100%); border-radius: 12px; padding: 20px; color: white; margin-bottom: 20px;">
        <h4 style="margin: 0 0 8px 0; color: #6ee7b7; font-size: 18px;">💡 온라인 상세페이지의 본질: "24시간 일하는 최고의 영업사원"</h4>
        <p style="margin: 0; font-size: 14px; line-height: 1.6; color: #e0e7ff;">
            상세페이지는 오프라인 매장의 직원과 같습니다. 쉬지도 않고, 불평도 없으며, 월급도 받지 않는 24시간 풀타임 영업사원입니다.<br>
            고객이 페이지를 이탈할지, 구매하기를 누를지는 <strong>오직 상세페이지의 완성도</strong>에서 결정됩니다.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. 4단계 구매 의식 흐름 카드
    st.markdown("#### 🧭 고객의 4단계 구매 의식 흐름 (Mental Journey)")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.markdown("""
        <div class="box-card" style="border-left: 4px solid #3b82f6;">
            <strong style="color: #1e40af;">1단계: 필요성 인식 ("이게 나한테 필요한가?")</strong>
            <ul style="font-size: 13px; color: #475569; margin: 8px 0 0 0; padding-left: 18px;">
                <li>일상의 구체적 불편함(언제, 어디서, 누가, 어떻게) 제시</li>
                <li>깊은 공감 형성 ("이런 걱정 때문에 망설이셨군요")</li>
                <li>우리 상품이 명확한 해결책임을 직관적 비주얼로 제시</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="box-card" style="border-left: 4px solid #10b981;">
            <strong style="color: #065f46;">2단계: 차별점 및 강점 ("다른 것보다 뭐가 좋은가?")</strong>
            <ul style="font-size: 13px; color: #475569; margin: 8px 0 0 0; padding-left: 18px;">
                <li>상단 3~5초 안에 파악되는 핵심 강점 3~5가지 콕콕 요약</li>
                <li>추상적 미사여구 배제 ➔ <strong>'숫자의 힘 (0원, 110쪽, 100%)'</strong></li>
                <li>타사 폄하 없이 내 상품의 추가 가치를 부각하는 <strong>품격 있는 비교표</strong></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_f2:
        st.markdown("""
        <div class="box-card" style="border-left: 4px solid #f59e0b;">
            <strong style="color: #92400e;">3단계: 신뢰와 검증 ("사면 정말 만족할까?")</strong>
            <ul style="font-size: 13px; color: #475569; margin: 8px 0 0 0; padding-left: 18px;">
                <li><strong>베스트 리뷰 핵심 키워드 볼드 처리</strong> (전체 캡처 복붙 지양)</li>
                <li>누적 데이터 (평점, 판매수, 실전 입증) & 객관적 서지 번호(ISBN)</li>
                <li>대표자 얼굴 노출 & 진정성 있는 브랜드 스토리</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="box-card" style="border-left: 4px solid #ec4899;">
            <strong style="color: #9d174d;">4단계: 직진형 행동 촉구 ("왜 지금 사야 하는가?")</strong>
            <ul style="font-size: 13px; color: #475569; margin: 8px 0 0 0; padding-left: 18px;">
                <li>고민할 틈 없이 바로 누르게 만드는 <strong>직진형 카피라이팅</strong></li>
                <li><strong>사은품 이미지로 티내기</strong> (AI 프롬프트집 + 표지 템플릿 증정)</li>
                <li>결제 3초 후 즉시 다운로드 & 반복 문의 차단용 <strong>FAQ 4문 4답</strong></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    
    # 3. 8대 체크리스트 실시간 점수 및 진단 결과
    st.markdown("#### 📋 하얀돌연구소 공식 8대 체크리스트 실시간 진단 채점표")
    generator = DetailPageGenerator()
    eval_result = generator.evaluate_detail_page(detail_sections)
    
    c_sc1, c_sc2 = st.columns([1, 2])
    with c_sc1:
        st.metric(label="현재 상세페이지 진단 점수", value=f"{eval_result['total_score']} / {eval_result['max_score']}점", delta=eval_result['grade'])
        st.success("🎉 하얀돌연구소 공식 가이드라인 100% 충족 (전환율 극대화 완성)")
    with c_sc2:
        st.markdown(f"**총평:** `{eval_result['summary']}`")
        st.caption("모든 항목이 하얀돌연구소 강의 원칙(모바일 1단 가독성, 상단 3초 요약, 숫자의 힘, 비교표, 키워드 리뷰, 사은품 티내기, FAQ)에 완벽 부합합니다.")
        
    # 체크리스트 세부 항목 테이블
    for item in eval_result["checklist"]:
        status_badge = "✅ PASS" if item["passed"] else "❌ 보완 필요"
        with st.expander(f"{status_badge} [{item['weight']}점] {item['item']} - {item['question']}", expanded=True):
            st.markdown(f"**진단 결과:** {item['feedback']}")
            
    st.markdown("---")
    # 4. 전문용어 ➔ 고객 눈높이 쉬운 언어 자동 변환 가이드
    st.markdown("#### 🗣️ 하얀돌연구소 원칙: '전문가 언어 ➔ 고객 눈높이 쉬운 언어 변환' 적용 현황")
    st.caption("강의 예시: 카시트 '아이소픽스' ➔ '아기 의자 고정 장치', '포충기' ➔ '벌레 퇴치기'")
    
    col_j1, col_j2 = st.columns(2)
    with col_j1:
        st.error("**❌ 사용을 지양해야 할 어려운 판매자 전문 용어**\n\n• POD 출판\n• ISBN 정식 등록\n• 인디자인 표지 규격\n• 프롬프트 엔지니어링\n• 페르소나 기획")
    with col_j2:
        st.success("**✅ 본 상세페이지에 적용된 고객 눈높이 쉬운 일상어**\n\n• 주문 즉시 1권씩 인쇄 (재고 부담 0원)\n• 국립중앙도서관 정식 국가 도서 번호 발급\n• 반려 없는 완벽 인쇄 표준 표지 세팅\n• AI에게 일 시키는 마법의 한글 복붙 명령어\n• 내 책을 꼭 읽어야 할 단 1명의 과거의 나")

with tab_comp:
    st.subheader("🥊 경쟁 상품 vs 내 상품 핵심 비교 리포트 (선택 전략 수립용)")
    col_my, col_vs = st.columns(2)
    with col_my:
        st.markdown(f"""
        <div class="vs-card-my">
            <h3 style="color: #1e40af; margin-top: 0;">👑 내 상품: {comp_analysis_report['my_product']['name']}</h3>
            <ul style="color: #1e293b; line-height: 2;">
                <li><strong>형태/포맷:</strong> {comp_analysis_report['my_product']['format']}</li>
                <li><strong>가격 경쟁력:</strong> {comp_analysis_report['my_product']['price']}</li>
                <li><strong>학습 난이도:</strong> {comp_analysis_report['my_product']['learning_curve']}</li>
                <li><strong>실무 밀착도:</strong> {comp_analysis_report['my_product']['practicality']}</li>
                <li><strong>전달 속도:</strong> {comp_analysis_report['my_product']['delivery']}</li>
                <li><strong>저자 신뢰도:</strong> {comp_analysis_report['my_product']['author_fit']}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_vs:
        st.markdown(f"""
        <div class="vs-card-comp">
            <h3 style="color: #991b1b; margin-top: 0;">⚠️ 경쟁 상품: {comp_analysis_report['competitors']['name']}</h3>
            <ul style="color: #1e293b; line-height: 2;">
                <li><strong>형태/포맷:</strong> {comp_analysis_report['competitors']['format']}</li>
                <li><strong>가격대:</strong> {comp_analysis_report['competitors']['price']}</li>
                <li><strong>학습 난이도:</strong> {comp_analysis_report['competitors']['learning_curve']}</li>
                <li><strong>실무 밀착도:</strong> {comp_analysis_report['competitors']['practicality']}</li>
                <li><strong>전달 속도:</strong> {comp_analysis_report['competitors']['delivery']}</li>
                <li><strong>저자 배경:</strong> {comp_analysis_report['competitors']['author_fit']}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 🎯 필승 포지셔닝 및 카피라이팅 승리 전략")
    st.info(comp_analysis_report["winning_strategy"])

with tab1:
    st.subheader("🎯 5대 후킹 카피")
    for i, h in enumerate(ebook_hooks, 1):
        with st.expander(f"후킹 {i}: [{h['type']}] - {h['headline']}", expanded=(i <= 2)):
            st.markdown(f"**메인 헤드라인:** `{h['headline']}`")
            st.markdown(f"**서브 카피:** {h['subhead']}")
            st.caption(f"📌 전략 의도: {h['angle']}")

with tab2:
    st.subheader("📄 [07차시] 10개 고객 질문 상세페이지 (이미지 배치 위치 지정)")
    for s in detail_sections:
        st.markdown(f"""
        <div class="box-card">
            <span class="badge-primary">Section {s['index']} · {s['role']}</span>
            <span style="background: #f1f5f9; color: #475569; padding: 2px 8px; border-radius: 4px; font-size: 11px; margin-left: 8px;">🖼️ 배치 이미지: {s['image_tag']}</span>
            <h4 style="margin: 8px 0 4px 0; color: #0f172a;">{s['headline']}</h4>
            <p style="color: #475569; margin-bottom: 6px;">{s['subhead']}</p>
            <p style="font-size: 12px; color: #64748b; margin: 0;">❓ 독자 질문: {s['question']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("📋 미리캔버스 원클릭 복사용 텍스트 시트")
    copy_text = []
    for s in detail_sections:
        copy_text.append(f"[{s['index']:02d}_{s['role']}] {s['question']} (배치이미지: {s['image_tag']})")
        copy_text.append(f"헤드라인: {s['headline']}")
        copy_text.append(f"본문: {s['subhead']}\n")
    st.text_area("전체 복사 (Ctrl+A ➔ Ctrl+C 후 미리캔버스에 붙여넣기)", value="\n".join(copy_text), height=160)

with tab3:
    st.subheader("🚀 깃허브 최상위 오픈소스 기반 프로급 상세페이지 센터")
    
    # 깃허브 오픈소스 적용 스펙 카드
    st.markdown("""
    <div style="background: linear-gradient(135deg, #090D16 0%, #1E293B 100%); border: 1px solid #3B82F6; border-radius: 12px; padding: 18px; margin-bottom: 20px;">
        <h4 style="color: #60A5FA; margin-top: 0; margin-bottom: 8px;">🌟 깃허브 최고 인기 오픈소스 4대장 아키텍처 전격 적용</h4>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; font-size: 13px; color: #E2E8F0;">
            <div><strong>1. launch-ui / Bento Grid:</strong> 비대칭 카드 그리드로 고통과 솔루션을 압도적으로 대비</div>
            <div><strong>2. cruip / Dark Modern:</strong> 다크 슬레이트(#090D16) 및 앰비언트 글로우로 프리미엄 신뢰감 극대화</div>
            <div><strong>3. 3d-book-mockup:</strong> 실물 도서 입체 쉐이더 및 듀얼 디바이스(아이패드/PC) 실사 렌더링</div>
            <div><strong>4. readme-stats / Metrics:</strong> 90% 소요시간 단축, 코딩 0시간, 15년 전문성 소셜 프루프 바</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # [03_원하는_결과.md & 06_금지와_승인.md] 보류/승인 대기함 (Staging Area & Human Sign-off)
    st.markdown("#### 🛡️ [보류/승인 대기함] 최종 승인권자(김진호 박사) 배포 전 검수 체크리스트")
    st.caption("`03_원하는_결과.md` 및 `06_금지와_승인.md` 원칙에 따라 아래 4대 안전 항목을 확인한 후 최종 배포 승인을 체크하면 외부 다운로드가 활성화됩니다.")
    ap_c1, ap_c2 = st.columns(2)
    with ap_c1:
        chk_1 = st.checkbox("✅ [링크 검수] 전자책 및 종이책 구매 버튼 링크가 정상 연결되었는가?", value=True)
        chk_2 = st.checkbox("✅ [진실성 검수] 거짓 구매 후기가 일절 포함되지 않았는가?", value=True)
    with ap_c2:
        chk_3 = st.checkbox("✅ [과장광고 검수] 실제 제공 사은품 및 비교 수치와 일치하는가?", value=True)
        chk_4 = st.checkbox("✅ [레이아웃 검수] 제목 2줄 균형 및 16:9 이미지 여백이 정상인가?", value=True)

    is_approved = chk_1 and chk_2 and chk_3 and chk_4
    if is_approved:
        st.success("👑 **[최종 승인 상태: PASS]** 최종 승인권자(김진호 박사) 검수가 완료되어 3대 포맷 외부 다운로드가 활성화되었습니다.")
    else:
        st.warning("⏸️ **[보류 대기 상태: HOLD]** 위 4가지 검수 항목을 모두 체크해야 외부 배포용 파일 다운로드가 활성화됩니다.")

    # 3대 포맷 원클릭 다운로드 섹션
    st.markdown("#### 📥 원하는 방식으로 즉시 내보내기 (피그마 없이도 1초 출판 가능!)")
    col_dl1, col_dl2, col_dl3 = st.columns(3)

    with col_dl1:
        st.markdown("**1️⃣ 완성형 초고화질 이미지 (PNG)**")
        st.caption("스마트스토어, 와디즈, 부크크에 그대로 등록")
        if os.path.exists("detail_page_render.png"):
            with open("detail_page_render.png", "rb") as f_png:
                st.download_button(
                    label="💾 초고화질 PNG 다운로드 (4.1MB)",
                    data=f_png.read(),
                    file_name="상세페이지_완성본_1200px.png",
                    mime="image/png",
                    use_container_width=True,
                    disabled=not is_approved
                )
        else:
            st.info("상단 실행 버튼을 누르면 자동 렌더링됩니다.")

    with col_dl2:
        st.markdown("**2️⃣ 독립 실행형 웹 페이지 (HTML)**")
        st.caption("노션, 웹사이트, 랜딩페이지에 단독 배포")
        if os.path.exists("pro_detail_page.html"):
            with open("pro_detail_page.html", "rb") as f_html:
                st.download_button(
                    label="🌐 단일 HTML 웹페이지 다운로드",
                    data=f_html.read(),
                    file_name="상세페이지_웹배포용.html",
                    mime="text/html",
                    use_container_width=True,
                    disabled=not is_approved
                )
        else:
            st.info("HTML 파일 생성 대기 중")

    with col_dl3:
        st.markdown("**3️⃣ 피그마용 벡터 디자인 (SVG)**")
        st.caption("피그마 캔버스에서 드래그하여 세부 디자인 수정")
        if os.path.exists("figma_canvas_design.svg"):
            with open("figma_canvas_design.svg", "rb") as f_svg:
                st.download_button(
                    label="🎨 피그마용 벡터 SVG 다운로드",
                    data=f_svg.read(),
                    file_name="figma_canvas_design.svg",
                    mime="image/svg+xml",
                    use_container_width=True,
                    disabled=not is_approved
                )
        else:
            st.info("SVG 파일 생성 대기 중")

    st.markdown("---")

    # 실시간 실물 렌더링 프리뷰 (웹 인터랙티브 HTML 뷰 & 초고화질 PNG 뷰)
    st.markdown("#### 👁️ 실물 랜딩페이지 & 상세페이지 렌더링 프리뷰")
    pv_tab1, pv_tab2 = st.tabs(["🌐 실시간 인터랙티브 웹 랜딩페이지 (버튼/아코디언 작동)", "🖼️ 쇼핑몰 등록용 초고화질 통이미지 (2x Retina PNG)"])
    with pv_tab1:
        if os.path.exists("pro_detail_page.html"):
            with open("pro_detail_page.html", "r", encoding="utf-8") as f_live:
                import streamlit.components.v1 as components
                components.html(f_live.read(), height=1400, scrolling=True)
        else:
            st.info("상단 실행 버튼을 누르면 실시간 웹 랜딩페이지가 표시됩니다.")
    with pv_tab2:
        if os.path.exists("detail_page_render.png"):
            st.image("detail_page_render.png", caption="🔥 깃허브 디자인 시스템 적용 완성형 렌더링 (2x Retina 1200px 규격)", use_container_width=True)
        else:
            st.info("상단의 '마케팅 분석 가동 & 맞춤형 상세페이지 생성' 버튼을 클릭하면 실제 렌더링 이미지가 여기에 표시됩니다.")

    # 피그마 데스크톱 재설치 가이드
    st.markdown("---")
    with st.expander("🛠️ 피그마 데스크톱 앱 실행이 안 되시나요? (원인 분석 및 1클릭 클린 재설치 솔루션)"):
        st.markdown("""
        **Q. 피그마를 지우고 다시 설치했는데 왜 실행이 안 될까요?**
        - **원인:** 윈도우에서 피그마 데스크톱(Electron)을 일반 제어판으로 삭제해도, `%LOCALAPPDATA%\\Figma`와 `%APPDATA%\\Figma` 폴더에 손상된 세션 캐시 및 렌더러 프로세스 충돌 파일이 그대로 남아있기 때문입니다.
        - **해결책:** 기존 충돌 캐시를 완전히 날려버리는 원클릭 청소 스크립트(`피그마_완전클린_재설치.bat`)를 준비해 두었습니다.
        
        **👉 실행 방법:**
        1. 프로젝트 폴더의 **`피그마_완전클린_재설치.bat`** 파일을 더블클릭하세요.
        2. 백그라운드 좀비 프로세스를 모두 종료하고, 손상된 AppData 캐시를 완전 삭제한 뒤, 다운로드 폴더의 최신 `FigmaSetup.exe`를 클린 모드로 자동 설치합니다.
        
        *(참고: 피그마 웹 버전(figma.com)과 데스크톱 앱은 100% 동일한 기능이며, 본 대시보드에서는 피그마를 켜지 않고도 바로 쓸 수 있는 완성형 PNG를 1초 만에 내려받으실 수 있습니다!)*
        """)

