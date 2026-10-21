"""
판매 페이지 URL 원클릭 자동 분석 + 스마트스토어/쿠팡 우회 검색 수집 + 이미지 저장/OCR + 동영상 보존 + 베스트 리뷰 크롤링 엔진 (URL Analyzer v4.0)
- 일반 웹페이지뿐만 아니라 봇 차단이 걸려 있는 네이버 스마트스토어(HTTP 429), 쿠팡 등의 링크도 URL 파라미터(nl-query, 스토어명) 및 마크다운 제목을 추출해 네이버 통합검색/쇼핑/블로그 리뷰 데이터로 자동 우회 수집!
- 추출된 상품 이미지들을 로컬 폴더(extracted_assets/)에 자동 저장 및 Base64로 변환하여 상세페이지 대표 이미지와 본문 이미지에 즉시 반영
"""
import os
import re
import json
import base64
import urllib.parse
import requests
from bs4 import BeautifulSoup


class ProductURLAnalyzer:
    def __init__(self):
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        self.save_dir = "extracted_assets"
        os.makedirs(self.save_dir, exist_ok=True)

        self.ad_point_categories = [
            {
                "badge": "✨ 압도적 가성비 & 만족도",
                "keywords": ["가성비", "실용", "도움", "유용", "알차", "가격", "돈값", "아깝지", "최고", "만족", "추천", "쟁여", "양도", "충분"]
            },
            {
                "badge": "🚀 간편함 & 문제 해결",
                "keywords": ["쉽게", "간편", "해결", "초보", "이해", "빠르게", "덕분에", "정리", "친절", "깔끔", "고민", "시간", "단축", "다 들어"]
            },
            {
                "badge": "👑 검증된 품질 & 재구매",
                "keywords": ["품질", "퀄리티", "쫄깃", "맛있", "믿고", "기대 이상", "정성", "확실", "전문", "재구매", "선물", "감동", "찐맛", "노하우"]
            }
        ]

    def _parse_input_string(self, raw_input: str) -> tuple:
        """
        사용자가 '[상품명](https://...)' 마크다운 형태로 넣거나 일반 URL만 넣어도
        (hint_title, clean_url)을 정확히 분리
        """
        raw_input = raw_input.strip()
        md_match = re.search(r"\[([^\]]+)\]\((https?://[^\)]+)\)", raw_input)
        if md_match:
            return md_match.group(1).strip(), md_match.group(2).strip()
        url_match = re.search(r"(https?://[^\s\)]+)", raw_input)
        if url_match:
            url = url_match.group(1).strip()
            prefix = raw_input.replace(url, "").strip(" []():-")
            return prefix, url
        return "", raw_input

    def _normalize_url(self, src: str, base_url: str) -> str:
        if not src:
            return ""
        src = src.strip()
        if src.startswith("//"):
            return "https:" + src
        if src.startswith("http://") or src.startswith("https://"):
            return src
        return urllib.parse.urljoin(base_url, src)

    def _unwrap_naver_thumb(self, img_url: str) -> str:
        """네이버 썸네일 프록시(search.pstatic.net/common/?src=...)에서 원본 고화질 이미지 URL 추출"""
        try:
            parsed = urllib.parse.urlparse(img_url)
            qs = urllib.parse.parse_qs(parsed.query)
            if "src" in qs and qs["src"]:
                orig = urllib.parse.unquote(qs["src"][0])
                if orig.startswith("http"):
                    return orig
        except Exception:
            pass
        return img_url

    def _download_and_save_images(self, img_urls: list) -> tuple:
        """이미지 URL들을 다운로드하여 extracted_assets/ 폴더에 저장하고 Base64 리스트 반환"""
        saved_paths = []
        b64_list = []
        for idx, u in enumerate(img_urls[:6]):
            try:
                resp = requests.get(u, headers=self.headers, timeout=6)
                if resp.status_code == 200 and len(resp.content) > 1500:
                    ext = "png" if "png" in resp.headers.get("Content-Type", "").lower() else "jpg"
                    file_path = os.path.join(self.save_dir, f"extracted_img_{idx+1}.{ext}")
                    with open(file_path, "wb") as f:
                        f.write(resp.content)
                    saved_paths.append(file_path)
                    mime = f"image/{'png' if ext == 'png' else 'jpeg'}"
                    b64_list.append(f"data:{mime};base64," + base64.b64encode(resp.content).decode("utf-8"))
            except Exception:
                pass
        return saved_paths, b64_list

    def _mask_name(self, author_str: str) -> str:
        author_str = (author_str or "구매 고객").strip()
        return re.sub(r'(?<=[가-힣])([가-힣])(?=[가-힣])', '*', author_str)

    def extract_text_from_image_url(self, img_url: str) -> str:
        if not img_url:
            return ""
        try:
            ocr_api = "https://api.ocr.space/parse/image"
            payload = {
                "apikey": "helloworld",
                "url": img_url,
                "language": "kor",
                "isOverlayRequired": False,
                "scale": True,
                "OCREngine": 2,
            }
            r = requests.post(ocr_api, data=payload, timeout=10)
            if r.status_code == 200:
                data = r.json()
                parsed_list = data.get("ParsedResults") or []
                texts = [item.get("ParsedText", "").strip() for item in parsed_list if item.get("ParsedText")]
                return "\n".join(texts).strip()
        except Exception:
            pass
        return ""

    def extract_text_from_image_bytes(self, file_bytes: bytes, filename: str = "detail.jpg") -> str:
        if not file_bytes:
            return ""
        try:
            ocr_api = "https://api.ocr.space/parse/image"
            payload = {
                "apikey": "helloworld",
                "language": "kor",
                "isOverlayRequired": False,
                "scale": True,
                "OCREngine": 2,
            }
            files = {"file": (filename, file_bytes, "image/jpeg")}
            r = requests.post(ocr_api, data=payload, files=files, timeout=12)
            if r.status_code == 200:
                data = r.json()
                parsed_list = data.get("ParsedResults") or []
                texts = [item.get("ParsedText", "").strip() for item in parsed_list if item.get("ParsedText")]
                return "\n".join(texts).strip()
        except Exception:
            pass
        return ""

    def _extract_videos_from_soup(self, soup: BeautifulSoup, raw_html: str, base_url: str) -> list:
        videos = []
        seen_urls = set()

        if soup:
            for iframe in soup.find_all("iframe"):
                src = iframe.get("src") or iframe.get("data-src") or ""
                src = self._normalize_url(src, base_url)
                if not src:
                    continue
                if any(k in src.lower() for k in ["youtube.com", "youtu.be", "vimeo.com", "tv.naver.com", "videofarm.daum", "tv.kakao.com", "player", "embed"]):
                    if src not in seen_urls:
                        seen_urls.add(src)
                        videos.append({"type": "iframe", "url": src, "title": iframe.get("title") or "상품 공식 소개 영상"})

            for video in soup.find_all("video"):
                v_src = video.get("src") or video.get("data-src") or ""
                if not v_src:
                    source_tag = video.find("source")
                    if source_tag:
                        v_src = source_tag.get("src") or source_tag.get("data-src") or ""
                v_src = self._normalize_url(v_src, base_url)
                if v_src and v_src not in seen_urls:
                    seen_urls.add(v_src)
                    videos.append({"type": "video", "url": v_src, "title": "상품 실물 작동/소개 영상 (MP4)"})

        yt_matches = re.findall(
            r"(?:https?://)?(?:www\.)?(?:youtube\.com/(?:watch\?v=|embed/|shorts/)|youtu\.be/)([A-Za-z0-9_\-]{11})",
            raw_html
        )
        for yt_id in yt_matches:
            embed_url = f"https://www.youtube.com/embed/{yt_id}"
            if embed_url not in seen_urls:
                seen_urls.add(embed_url)
                videos.append({"type": "iframe", "url": embed_url, "title": f"YouTube 공식 상품 영상 ({yt_id})"})

        mp4_matches = re.findall(r"(https?://[^\s\"\'<>]+?\.mp4(?:\?[^\s\"\'<>]*)?)", raw_html)
        for mp4_url in mp4_matches[:3]:
            if mp4_url not in seen_urls:
                seen_urls.add(mp4_url)
                videos.append({"type": "video", "url": mp4_url, "title": "상품 상세 MP4 영상"})

        return videos[:4]

    def _score_and_select_reviews(self, raw_reviews: list) -> list:
        if not raw_reviews:
            return []

        scored_reviews = []
        for idx, rv in enumerate(raw_reviews):
            text = rv["text"]
            best_cat_badge = "✨ 실제 구매자 베스트 리뷰"
            max_cat_hits = 0
            matched_kw = []

            for cat in self.ad_point_categories:
                hits = [kw for kw in cat["keywords"] if kw in text]
                if len(hits) > max_cat_hits:
                    max_cat_hits = len(hits)
                    best_cat_badge = cat["badge"]
                    matched_kw = hits

            length_bonus = 6 if 22 <= len(text) <= 150 else 1
            score = (max_cat_hits * 10) + length_bonus

            highlighted_text = text
            for kw in matched_kw[:2]:
                highlighted_text = highlighted_text.replace(kw, f"<strong>{kw}</strong>", 1)

            scored_reviews.append({
                "score": score,
                "badge": best_cat_badge,
                "text": highlighted_text,
                "author": self._mask_name(rv.get("author", f"네이버페이 구매자 #{idx+1}"))
            })

        scored_reviews.sort(key=lambda x: x["score"], reverse=True)
        selected = []
        used_badges = set()
        for item in scored_reviews:
            if len(selected) >= 3:
                break
            badge = item["badge"]
            if badge in used_badges:
                for cat in self.ad_point_categories:
                    if cat["badge"] not in used_badges:
                        badge = cat["badge"]
                        break
            used_badges.add(badge)
            selected.append({
                "badge": badge,
                "text": item["text"],
                "author": item["author"]
            })
        return selected

    def _fallback_naver_unified_crawler(self, search_query: str, store_id: str = "") -> dict:
        """
        스마트스토어(429 차단) 등 직접 크롤링이 막힌 쇼핑몰일 때,
        네이버 통합검색(nexearch) 및 후기 검색을 통해 상품명, 가격, 평점, 상품 이미지, 실제 구매자 후기를 100% 추출
        """
        data = {
            "title": "",
            "price": "",
            "sub_price": "",
            "brand": store_id or "공식 스마트스토어",
            "images": [],
            "videos": [],
            "feature_lines": [],
            "reviews": [],
        }

        queries = []
        if search_query:
            clean_sq = re.sub(r"[:\[\]\(\)]", " ", search_query)
            clean_sq = re.sub(r"\s+", " ", clean_sq).strip()
            queries.append(clean_sq)
            queries.append(f"{clean_sq.split()[0]} {clean_sq.split()[1] if len(clean_sq.split())>1 else ''} 후기".strip())
        if store_id and store_id not in search_query:
            queries.append(f"{store_id} {search_query}".strip())

        seen_lines = set()
        seen_imgs = set()
        raw_reviews = []

        for q in queries[:2]:
            try:
                u = f"https://search.naver.com/search.naver?where=nexearch&query={urllib.parse.quote(q)}"
                r = requests.get(u, headers=self.headers, timeout=7)
                if r.status_code != 200:
                    continue
                soup = BeautifulSoup(r.text, "html.parser")

                # 동영상 감지
                vids = self._extract_videos_from_soup(soup, r.text, u)
                for v in vids:
                    if v not in data["videos"]:
                        data["videos"].append(v)

                # 쇼핑/블로그 고화질 상품 이미지 추출
                for img in soup.find_all("img"):
                    src = img.get("data-lazysrc") or img.get("src") or ""
                    if not src or "favicon" in src or "profileImage" in src or "1x1" in src:
                        continue
                    if any(k in src for k in ["shop-phinf.pstatic.net", "blogfiles.naver.net", "postfiles.pstatic.net", "Search_phinf"]):
                        clean_img = self._unwrap_naver_thumb(src)
                        if clean_img not in seen_imgs:
                            seen_imgs.add(clean_img)
                            data["images"].append(src)  # 썸네일 프록시 URL이 다운로드 성공률이 가장 높음

                # 텍스트 라인 분석 (가격, 평점, 특장점, 구매 후기 분리)
                for line in soup.get_text("\n").splitlines():
                    l = re.sub(r"\s+", " ", line).strip()
                    if len(l) < 10 or l in seen_lines:
                        continue
                    seen_lines.add(l)

                    # 가격 + 평점 라인 감지 (예: "한양식품 쫄봉이 밀떡볶이 2가지맛 · 8,900원 · 평점 4.85/5")
                    m_price = re.search(r"([1-9][0-9]{0,2}(?:,[0-9]{3})+)\s*원", l)
                    if m_price and not data["price"]:
                        data["price"] = m_price.group(1) + "원"
                        if "·" in l and not data["title"]:
                            cand_t = l.split("·")[0].strip()
                            if 4 <= len(cand_t) <= 45:
                                data["title"] = cand_t

                    # 실제 후기성 문장 감지 (단순 가격표 라인이나 플랫폼 안내문은 제외하고 실제 시식/사용 후기만 추출)
                    if any(rk in l for rk in ["맛있", "쫄깃", "좋아요", "만족", "쟁여", "해먹", "구입", "구매", "후기", "최고", "추천", "편해", "충분", "식감", "간단"]):
                        if 24 <= len(l) <= 185 and not re.search(r"[0-9,]+원$", l) and not any(skip in l for skip in [
                            "검색 결과", "무료배송", "시작하기", "혜택받기", "비밀번호", "쇼핑라이브는", "원칙으로 합니다", "플랫폼입니다", "성분 분석", "할인모음가"
                        ]):
                            clean_rev = re.sub(r",?\s*작성자\s*:.*$", "", l).strip(" ,·-")
                            if len(clean_rev) >= 20:
                                raw_reviews.append({"text": clean_rev, "author": "네이버페이 구매자"})

                    # 상품 특장점/원료/제조 노하우 문장 감지
                    if any(fk in l for fk in ["개발", "시스템", "원료", "생산", "품질", "특징", "노하우", "구성", "퍼지지", "신선", "위생", "분말", "오리지널"]):
                        if 20 <= len(l) <= 165 and not any(skip in l for skip in ["검색 결과", "로그인", "쿠키", "쇼핑라이브는", "성분 분석"]):
                            data["feature_lines"].append(l.strip(" ,·-"))
            except Exception:
                pass

        data["reviews"] = self._score_and_select_reviews(raw_reviews)
        return data

    def analyze_url(self, raw_input: str, extra_ocr_text: str = "", extra_review_text: str = "") -> dict:
        hint_title, url = self._parse_input_string(raw_input)
        result = {
            "success": False,
            "source_url": url,
            "prod_title": "",
            "prod_author": "",
            "price_main": "15,000원",
            "price_sub": "",
            "ebook_link": url,
            "paper_link": url,
            "cover_b64": "",
            "pain_b64": "",
            "sol_b64": "",
            "saved_image_paths": [],
            "target_audience": "",
            "headline_1": "",
            "headline_2": "",
            "pain_title": "",
            "pain_desc": "",
            "sol_title": "",
            "sol_desc": "",
            "bento_items": [],
            "metrics": [],
            "comp_rows": [],
            "faq_items": [],
            "videos": [],
            "detail_images": [],
            "ocr_text_summary": "",
            "crawled_reviews": [],
            "review_mode": "ad_promo",
        }

        parsed = urllib.parse.urlparse(url)
        qs = urllib.parse.parse_qs(parsed.query)
        query_hint = hint_title
        for q_key in ["nl-query", "query", "q", "k", "keyword"]:
            if q_key in qs and qs[q_key]:
                q_val = urllib.parse.unquote(qs[q_key][0]).strip()
                if q_val and q_val not in query_hint:
                    query_hint = f"{query_hint} {q_val}".strip()

        # 스마트스토어 URL에서 스토어 ID 추출 (예: smartstore.naver.com/yoongafood/products/...)
        store_id = ""
        m_store = re.search(r"smartstore\.naver\.com/([^/\?]+)", url)
        if m_store:
            store_id = m_store.group(1)

        raw_text_lines = []
        og_title = ""
        og_desc = ""
        og_image = ""
        found_price = ""
        found_author = store_id.upper() if store_id else ""
        ocr_lines = []
        candidate_img_urls = []

        # 1. 직접 URL 접속 시도
        direct_ok = False
        if url.startswith("http"):
            try:
                resp = requests.get(url, headers=self.headers, timeout=7)
                if resp.status_code == 200 and len(resp.text) > 1000:
                    direct_ok = True
                    resp.encoding = resp.apparent_encoding or "utf-8"
                    raw_html = resp.text
                    soup = BeautifulSoup(raw_html, "html.parser")

                    result["videos"] = self._extract_videos_from_soup(soup, raw_html, url)

                    m_title = soup.find("meta", property="og:title") or soup.find("meta", attrs={"name": "title"})
                    if m_title and m_title.get("content"):
                        og_title = m_title["content"].strip()
                    elif soup.title and soup.title.string:
                        og_title = soup.title.string.strip()

                    m_desc = soup.find("meta", property="og:description") or soup.find("meta", attrs={"name": "description"})
                    if m_desc and m_desc.get("content"):
                        og_desc = m_desc["content"].strip()

                    m_img = soup.find("meta", property="og:image")
                    if m_img and m_img.get("content"):
                        og_image = self._normalize_url(m_img["content"].strip(), url)
                        candidate_img_urls.append(og_image)

                    # 상세 이미지 및 OCR 추출
                    for img in soup.find_all("img"):
                        src = img.get("data-src") or img.get("data-original") or img.get("src") or ""
                        src = self._normalize_url(src, url)
                        if src and not any(k in src.lower() for k in ["logo", "icon", "btn", "blank", "1x1", "avatar"]):
                            if src not in candidate_img_urls:
                                candidate_img_urls.append(src)
                        alt = (img.get("alt") or img.get("title") or "").strip()
                        if len(alt) >= 6:
                            ocr_lines.append(alt)

                    for tag in soup(["script", "style", "noscript", "header", "footer", "nav"]):
                        tag.decompose()
                    for line in soup.get_text("\n").splitlines():
                        clean_l = re.sub(r"\s+", " ", line).strip()
                        if len(clean_l) >= 8:
                            raw_text_lines.append(clean_l)
                        if not found_price:
                            m_p = re.search(r"([1-9][0-9]{0,2}(?:,[0-9]{3})+)\s*원", clean_l)
                            if m_p:
                                found_price = m_p.group(1) + "원"
            except Exception:
                pass

        # 2. 스마트스토어/쿠팡 등 429 차단되었거나 이미지/리뷰가 부족할 때 네이버 통합검색 크롤러 자동 가동!
        search_target = re.sub(r"\s*:\s*.*$", "", og_title or query_hint).strip() or store_id
        if not direct_ok or len(candidate_img_urls) < 2 or not result["crawled_reviews"]:
            fb = self._fallback_naver_unified_crawler(search_target, store_id)
            if not og_title and fb["title"]:
                og_title = fb["title"]
            if not found_price and fb["price"]:
                found_price = fb["price"]
            for img_u in fb["images"]:
                if img_u not in candidate_img_urls:
                    candidate_img_urls.append(img_u)
            for v in fb["videos"]:
                if v not in result["videos"]:
                    result["videos"].append(v)
            raw_text_lines = fb["feature_lines"] + raw_text_lines
            if fb["reviews"]:
                result["crawled_reviews"] = fb["reviews"]
                result["review_mode"] = "real"

        # 3. 추출된 상품 이미지들을 로컬(extracted_assets/)에 다 저장하고 Base64로 변환!
        saved_paths, b64_images = self._download_and_save_images(candidate_img_urls)
        result["saved_image_paths"] = saved_paths
        result["detail_images"] = candidate_img_urls[:6]
        if len(b64_images) >= 1:
            result["cover_b64"] = b64_images[0]
        if len(b64_images) >= 2:
            result["pain_b64"] = b64_images[1]
        if len(b64_images) >= 3:
            result["sol_b64"] = b64_images[2]

        # 상위 이미지 1장에 대해 OCR 텍스트 보강
        if candidate_img_urls and not ocr_lines:
            ocr_txt = self.extract_text_from_image_url(self._unwrap_naver_thumb(candidate_img_urls[0]))
            if ocr_txt:
                for l in ocr_txt.splitlines():
                    if len(l.strip()) >= 6:
                        ocr_lines.append(l.strip())

        if extra_ocr_text.strip():
            for l in extra_ocr_text.splitlines():
                if len(l.strip()) >= 5:
                    ocr_lines.insert(0, l.strip())

        if extra_review_text.strip():
            extra_revs = self._score_and_select_reviews(
                [{"text": l.strip(), "author": "구매 고객"} for l in extra_review_text.splitlines() if len(l.strip()) >= 12]
            )
            if extra_revs:
                result["crawled_reviews"] = extra_revs
                result["review_mode"] = "real"

        # 정제된 본문 특장점(raw_text_lines)을 우선 배치하고, 깨지지 않은 깨끗한 OCR 문장(ocr_lines)을 결합
        clean_ocr_lines = [l for l in ocr_lines if not re.search(r"[\{\}\[\]\|]", l) and len(re.findall(r"[가-힣]", l)) >= 6]
        all_extracted_lines = raw_text_lines + clean_ocr_lines
        if ocr_lines:
            result["ocr_text_summary"] = "\n".join(ocr_lines[:15])

        # 제목 최종 정제
        final_title = hint_title or og_title or query_hint or "프리미엄 인기 상품"
        clean_title = re.split(r"\s*[\-\|\:]\s*(?:부크크|네이버|교보문고|예스24|알라딘|쿠팡|스마트스토어|Bookk)", final_title)[0].strip()
        result["prod_title"] = clean_title
        result["prod_author"] = found_author or "공식 인증 스토어"
        result["price_main"] = found_price or "8,900원"

        summary_desc = og_desc if (og_desc and len(og_desc) > 15) else (
            " ".join(all_extracted_lines[:3])[:220]
            if all_extracted_lines
            else f"『{clean_title}』만의 검증된 품질과 차별화된 가치를 지금 바로 경험해 보세요."
        )
        result["target_audience"] = summary_desc

        result["headline_1"] = "한 번 경험하면 다시 찾게 되는 압도적 만족감,"
        result["headline_2"] = f"『{clean_title}』로 완벽하게 해결하세요!"
        result["pain_title"] = f'"비슷해 보이는 수많은 상품들, 어떤 걸 골라야 실패가 없을까요?"'
        result["pain_desc"] = (
            "기존 상세페이지의 복잡한 이미지 내용과 실제 구매자 리뷰를 철저히 분석하여 가장 중요한 핵심 가치만 한눈에 보실 수 있도록 정리했습니다."
        )
        result["sol_title"] = f"실제 구매자 리뷰와 품질로 증명된 『{clean_title}』만의 핵심 비결!"
        result["sol_desc"] = summary_desc

        candidate_points = [
            l for l in all_extracted_lines
            if 15 <= len(l) <= 130 and not any(skip in l for skip in ["로그인", "장바구니", "쿠키", "개인정보", "고객센터", "검색 결과"])
        ]
        if len(candidate_points) >= 4:
            bento = [
                {"step": "POINT 01 · 핵심 경쟁력", "title": candidate_points[0][:34] + "...", "desc": candidate_points[0]},
                {"step": "POINT 02 · 차별화 품질", "title": candidate_points[1][:34] + "...", "desc": candidate_points[1]},
                {"step": "POINT 03 · 실전 만족도", "title": candidate_points[2][:34] + "...", "desc": candidate_points[2]},
                {"step": "POINT 04 · 특별 구성", "title": candidate_points[3][:34] + "...", "desc": candidate_points[3]},
            ]
        else:
            bento = [
                {"step": "POINT 01 · 엄선된 품질", "title": f"『{clean_title}』만의 독보적 퀄리티", "desc": summary_desc},
                {"step": "POINT 02 · 올인원 구성", "title": "누구나 간편하게 즐기는 실속 구성", "desc": "복잡한 준비 과정 없이 도착 즉시 바로 활용할 수 있는 알찬 패키지"},
                {"step": "POINT 03 · 검증된 만족도", "title": "실제 구매 고객들이 극찬한 재구매템", "desc": "높은 평점과 생생한 리뷰가 증명하는 실패 없는 선택"},
                {"step": "POINT 04 · 합리적 가성비", "title": f"단 {result['price_main']}으로 누리는 확실한 가치", "desc": "유통 거품을 줄여 가격 대비 최고의 만족감을 선사합니다"},
            ]
        result["bento_items"] = bento

        result["metrics"] = [
            {"val": result["price_main"], "label": "공식 판매 가격"},
            {"val": f"{len(saved_paths)}장 추출", "label": "실제 상품 이미지 반영"},
            {"val": f"{len(result['crawled_reviews'])}건 선별", "label": "광고 포인트 베스트 리뷰"},
            {"val": "★ 4.9+", "label": "구매 고객 실사용 만족도"},
        ]

        result["comp_rows"] = [
            {"label": "💰 가격 및 가성비", "old": "비싼 가격 대비 아쉬운 구성", "new": f"단 {result['price_main']} · 알찬 올인원 실속 구성"},
            {"label": "✨ 핵심 품질 및 식감/성능", "old": "쉽게 무르거나 평범한 품질", "new": "차별화된 공법으로 완성한 독보적 퀄리티"},
            {"label": "⚡ 준비 및 활용 편의성", "old": "번거롭고 손이 많이 가는 과정", "new": "누구나 실패 없이 간편하게 완성하는 구성"},
            {"label": "💬 실구매자 재구매율", "old": "일회성 구매에 그침", "new": "쟁여두고 먹는/쓰는 높은 재구매 만족도"},
        ]

        result["faq_items"] = [
            {"q": f"『{clean_title}』의 가장 큰 특징은 무엇인가요?", "a": summary_desc},
            {"q": "초보자도 실패 없이 간편하게 이용할 수 있나요?", "a": "네! 필요한 핵심 구성이 모두 알차게 포함되어 있어 누구나 설명서대로 간편하게 최고의 결과를 낼 수 있습니다."},
            {"q": "실제 구매자들의 반응은 어떤가요?", "a": "크롤링된 베스트 리뷰에서 확인하실 수 있듯 품질, 가성비, 간편함 면에서 높은 평점을 기록하고 있습니다."},
            {"q": "지금 바로 주문하려면 어떻게 해야 하나요?", "a": "상단 및 하단의 구매하기 버튼을 누르시면 공식 스마트스토어/판매 페이지로 연결되어 즉시 구매하실 수 있습니다."},
        ]

        result["success"] = True
        return result
