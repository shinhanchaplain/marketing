"""
판매 페이지 URL 원클릭 자동 분석 + 이미지 OCR 텍스트 변환 + 원본 동영상(Video) 보존 + 베스트 리뷰 크롤링/선별 엔진 (URL Analyzer v3.0)
1. 판매 페이지 링크(URL) 입력 시 메타데이터(OpenGraph, JSON-LD), 본문 텍스트, 가격, 대표 이미지를 자동 추출
2. 상세페이지 내용이 통이미지(<img>)로 되어 있을 경우, 상세 이미지들을 수집하고 무료 한국어 OCR 엔진으로 이미지 속 텍스트를 추출·정리하여 새 상세페이지 구조(4단계 심리 여정)로 재구성
3. 판매 페이지에 동영상(YouTube, Naver TV, Vimeo iframe 또는 MP4 <video>)이 포함되어 있으면 이를 그대로 추출하여 새 상세페이지/랜딩페이지에 원본 동영상을 살려서 임베드
4. 판매 페이지의 고객 리뷰를 크롤링하여 광고 소구점(실용성/가성비, 문제해결/쉬움, 품질/신뢰도) 점수가 가장 높은 베스트 리뷰 3건을 선별 및 볼드 강조하여 상세페이지에 자동 반영 (리뷰가 0건이면 거짓 후기 없이 광고 배너 모드로 안전 전환)
"""
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
        # 광고 포인트(Selling Point) 카테고리별 핵심 키워드 사전
        self.ad_point_categories = [
            {
                "badge": "✨ 압도적 가성비 & 실용성",
                "keywords": ["가성비", "실용", "도움", "유용", "알차", "가격", "돈값", "아깝지", "바로", "최고", "만족", "추천", "혜자"]
            },
            {
                "badge": "🚀 빠른 문제 해결 & 쉬움",
                "keywords": ["쉽게", "해결", "초보", "이해", "빠르게", "덕분에", "정리", "친절", "깔끔", "고민", "시간", "단축", "그대로"]
            },
            {
                "badge": "👑 검증된 품질 & 신뢰도",
                "keywords": ["품질", "퀄리티", "믿고", "기대 이상", "정성", "확실", "전문", "재구매", "선물", "감동", "튼튼", "완벽"]
            }
        ]

    def _normalize_url(self, src: str, base_url: str) -> str:
        if not src:
            return ""
        src = src.strip()
        if src.startswith("//"):
            return "https:" + src
        if src.startswith("http://") or src.startswith("https://"):
            return src
        return urllib.parse.urljoin(base_url, src)

    def _mask_name(self, author_str: str) -> str:
        author_str = (author_str or "구매 고객").strip()
        return re.sub(r'(?<=[가-힣])([가-힣])(?=[가-힣])', '*', author_str)

    def _fetch_image_as_b64(self, img_url: str) -> str:
        if not img_url:
            return ""
        try:
            if img_url.startswith("//"):
                img_url = "https:" + img_url
            resp = requests.get(img_url, headers=self.headers, timeout=6)
            if resp.status_code == 200 and len(resp.content) > 500:
                mime = resp.headers.get("Content-Type", "image/jpeg")
                b64 = base64.b64encode(resp.content).decode("utf-8")
                return f"data:{mime};base64,{b64}"
        except Exception:
            pass
        return ""

    def extract_text_from_image_url(self, img_url: str) -> str:
        """상세페이지 통이미지 URL에서 한국어/영문 텍스트를 무료 OCR로 추출"""
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
        """업로드된 상세페이지/리뷰 캡처 이미지(bytes)에서 한국어 텍스트를 무료 OCR로 추출"""
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
        """판매 페이지 내 포함된 동영상(YouTube, Vimeo, Naver TV, <video>, .mp4)을 모두 찾아내어 보존"""
        videos = []
        seen_urls = set()

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

    def _extract_and_score_reviews(self, soup: BeautifulSoup, raw_html: str, extra_review_text: str = "") -> list:
        """
        판매 페이지에서 실제 구매자 리뷰를 크롤링하고,
        '광고할 만한 소구점(가성비/실용성, 문제해결/쉬움, 품질/신뢰도)' 점수가 가장 높은 베스트 리뷰 3건을 선별
        """
        raw_reviews = []

        # 1) JSON-LD 구조화 데이터 내 review 배열 추출
        if soup:
            for script in soup.find_all("script", type="application/ld+json"):
                try:
                    data = json.loads(script.string or "{}")
                    items = data if isinstance(data, list) else [data]
                    for item in items:
                        if not isinstance(item, dict):
                            continue
                        rev_list = item.get("review") or item.get("reviews") or []
                        if isinstance(rev_list, dict):
                            rev_list = [rev_list]
                        for r in rev_list:
                            if not isinstance(r, dict):
                                continue
                            body = (r.get("reviewBody") or r.get("description") or r.get("name") or "").strip()
                            author_obj = r.get("author")
                            author = "실제 구매자"
                            if isinstance(author_obj, dict):
                                author = author_obj.get("name", "실제 구매자")
                            elif isinstance(author_obj, str):
                                author = author_obj
                            if len(body) >= 12:
                                raw_reviews.append({"text": body, "author": author})
                except Exception:
                    pass

            # 2) HTML DOM 내 리뷰 관련 클래스/아이디 영역 탐색
            review_selectors = [
                '[class*="review"]', '[id*="review"]',
                '[class*="comment"]', '[class*="reply"]',
                '[class*="epilogue"]', '[class*="after"]'
            ]
            seen_texts = set(r["text"] for r in raw_reviews)
            for sel in review_selectors:
                for el in soup.select(sel)[:35]:
                    txt = re.sub(r"\s+", " ", el.get_text(separator=" ").strip())
                    # 너무 짧거나 단순 메뉴명 제외
                    if 18 <= len(txt) <= 220 and txt not in seen_texts:
                        if not any(bad in txt for bad in ["리뷰 작성", "로그인 후", "권한이 없습니다", "작성일", "신고하기", "배송문의"]):
                            seen_texts.add(txt)
                            raw_reviews.append({"text": txt, "author": "인증 구매 고객"})

        # 3) 사용자가 추가로 붙여넣거나 OCR로 추출한 리뷰 텍스트 병합
        if extra_review_text.strip():
            for line in extra_review_text.splitlines():
                cl = re.sub(r"\s+", " ", line).strip()
                if len(cl) >= 12:
                    raw_reviews.insert(0, {"text": cl, "author": "실제 구매 고객"})

        if not raw_reviews:
            return []

        # 4) 광고 포인트(Selling Point) 스코어링 및 베스트 3건 선별
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

            # 광고 소구점 점수 계산 (키워드 매칭 수 * 10 + 적절한 길이 가산점)
            length_bonus = 5 if 25 <= len(text) <= 140 else 1
            score = (max_cat_hits * 10) + length_bonus

            # 매칭된 광고 키워드가 있으면 해당 키워드 주변 구절을 볼드(<strong>) 강조
            highlighted_text = text
            for kw in matched_kw[:2]:
                highlighted_text = highlighted_text.replace(kw, f"<strong>{kw}</strong>", 1)

            scored_reviews.append({
                "score": score,
                "badge": best_cat_badge,
                "text": highlighted_text,
                "author": self._mask_name(rv.get("author", f"구매고객 #{idx+1}"))
            })

        # 점수순 정렬 후 상위 3개 반환
        scored_reviews.sort(key=lambda x: x["score"], reverse=True)
        selected = []
        used_badges = set()
        for item in scored_reviews:
            if len(selected) >= 3:
                break
            # 배지가 겹치면 다른 카테고리 배지 부여
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

    def _extract_detail_images_and_ocr(self, soup: BeautifulSoup, base_url: str) -> tuple:
        """상세페이지 통이미지 URL 수집 및 상위 상세 이미지 한국어 OCR 텍스트 자동 추출"""
        detail_img_urls = []
        img_alt_texts = []
        skip_keywords = ["logo", "icon", "btn", "button", "banner_top", "avatar", "sprite", "blank", "1x1", "pixel"]

        for img in soup.find_all("img"):
            src = img.get("data-src") or img.get("data-original") or img.get("data-lazy-src") or img.get("src") or ""
            src = self._normalize_url(src, base_url)
            if not src or src.startswith("data:"):
                continue
            if any(k in src.lower() for k in skip_keywords):
                continue

            alt = (img.get("alt") or img.get("title") or "").strip()
            if len(alt) >= 6:
                img_alt_texts.append(alt)

            if src not in detail_img_urls:
                detail_img_urls.append(src)

        ocr_extracted_lines = []
        for img_u in detail_img_urls[:2]:
            ocr_txt = self.extract_text_from_image_url(img_u)
            if ocr_txt:
                for line in ocr_txt.splitlines():
                    clean_l = re.sub(r"\s+", " ", line).strip()
                    if len(clean_l) >= 6:
                        ocr_extracted_lines.append(clean_l)

        return detail_img_urls[:6], img_alt_texts, ocr_extracted_lines

    def analyze_url(self, url: str, extra_ocr_text: str = "", extra_review_text: str = "") -> dict:
        url = url.strip()
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
        query_hint = ""
        if "query" in qs and qs["query"]:
            query_hint = urllib.parse.unquote(qs["query"][0]).strip()

        raw_text_lines = []
        og_title = ""
        og_desc = ""
        og_image = ""
        found_price = ""
        found_author = ""
        ocr_lines = []
        soup = None
        raw_html = ""

        if url:
            try:
                resp = requests.get(url, headers=self.headers, timeout=8)
                resp.encoding = resp.apparent_encoding or "utf-8"
                raw_html = resp.text
                soup = BeautifulSoup(raw_html, "html.parser")

                # 1) 동영상(Video) 자동 감지 및 보존
                result["videos"] = self._extract_videos_from_soup(soup, raw_html, url)

                # 2) OpenGraph 메타 태그 추출
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

                # 3) JSON-LD 구조화 데이터 추출
                for script in soup.find_all("script", type="application/ld+json"):
                    try:
                        data = json.loads(script.string or "{}")
                        items = data if isinstance(data, list) else [data]
                        for item in items:
                            if not isinstance(item, dict):
                                continue
                            if not og_title and item.get("name"):
                                og_title = str(item["name"]).strip()
                            if not og_desc and item.get("description"):
                                og_desc = str(item["description"]).strip()
                            if not og_image and item.get("image"):
                                img_val = item["image"]
                                og_image = img_val[0] if isinstance(img_val, list) else str(img_val)
                            offers = item.get("offers")
                            if isinstance(offers, dict) and offers.get("price"):
                                p_num = str(offers["price"]).replace(",", "")
                                if p_num.isdigit():
                                    found_price = f"{int(p_num):,}원"
                            author_obj = item.get("author") or item.get("brand")
                            if isinstance(author_obj, dict) and author_obj.get("name"):
                                found_author = str(author_obj["name"]).strip()
                            elif isinstance(author_obj, str):
                                found_author = author_obj.strip()
                    except Exception:
                        pass

                # 4) 판매 페이지 리뷰 크롤링 & 광고 소구점 베스트 리뷰 선별
                crawled_revs = self._extract_and_score_reviews(soup, raw_html, extra_review_text)
                if crawled_revs:
                    result["crawled_reviews"] = crawled_revs
                    result["review_mode"] = "real"

                # 5) 상세 이미지 수집 & 이미지 내 텍스트(alt + OCR) 추출
                detail_imgs, alt_texts, auto_ocr_lines = self._extract_detail_images_and_ocr(soup, url)
                result["detail_images"] = detail_imgs
                ocr_lines.extend(alt_texts)
                ocr_lines.extend(auto_ocr_lines)

                # 6) HTML 본문 텍스트 추출
                for tag in soup(["script", "style", "noscript", "header", "footer", "nav"]):
                    tag.decompose()
                body_text = soup.get_text(separator="\n")
                for line in body_text.splitlines():
                    clean_l = re.sub(r"\s+", " ", line).strip()
                    if len(clean_l) >= 8:
                        raw_text_lines.append(clean_l)
                    if not found_price:
                        m_p = re.search(r"([1-9][0-9]{0,2}(?:,[0-9]{3})+)\s*원", clean_l)
                        if m_p:
                            found_price = m_p.group(1) + "원"
            except Exception:
                pass

        # URL 없이 리뷰 텍스트만 추가로 들어온 경우 처리
        if not result["crawled_reviews"] and extra_review_text.strip():
            crawled_revs = self._extract_and_score_reviews(None, "", extra_review_text)
            if crawled_revs:
                result["crawled_reviews"] = crawled_revs
                result["review_mode"] = "real"

        # 사용자가 추가로 업로드한 이미지 OCR 텍스트 병합
        if extra_ocr_text.strip():
            for line in extra_ocr_text.splitlines():
                cl = line.strip()
                if len(cl) >= 5:
                    ocr_lines.insert(0, cl)

        all_extracted_lines = ocr_lines + raw_text_lines
        if ocr_lines:
            result["ocr_text_summary"] = "\n".join(ocr_lines[:15])

        bad_titles = ["에러", "오류", "접근", "보안", "캡차", "Captcha", "Access Denied", "네이버 쇼핑", "부크크"]
        if (not og_title or any(b in og_title for b in bad_titles)) and query_hint:
            og_title = query_hint
        if not og_title and ocr_lines:
            og_title = ocr_lines[0][:40]
        if not og_title:
            og_title = query_hint or "스마트 비즈니스 솔루션"

        clean_title = re.split(r"\s*[\-\|\:]\s*(?:부크크|네이버|교보문고|예스24|알라딘|쿠팡|스마트스토어|Bookk)", og_title)[0].strip()
        if not clean_title:
            clean_title = og_title

        result["prod_title"] = clean_title
        result["prod_author"] = found_author or "공식 브랜드 / 전문 제작팀"
        result["price_main"] = found_price or "15,000원"
        result["price_sub"] = ""

        target_cover_url = og_image or (result["detail_images"][0] if result["detail_images"] else "")
        if target_cover_url:
            b64_img = self._fetch_image_as_b64(target_cover_url)
            if b64_img:
                result["cover_b64"] = b64_img

        summary_desc = og_desc if (og_desc and len(og_desc) > 15) else (
            " / ".join(all_extracted_lines[:3])[:220]
            if all_extracted_lines
            else f"『{clean_title}』의 핵심 가치와 특장점을 한눈에 확인하고 즉시 시작할 수 있는 공식 상세페이지입니다."
        )
        result["target_audience"] = summary_desc

        result["headline_1"] = "복잡한 고민과 시행착오를 단번에 끝내는 선택,"
        result["headline_2"] = f"『{clean_title}』로 확실한 변화를 경험하세요!"
        result["pain_title"] = '"기존 방식의 한계와 막막함, 아직도 혼자 고민하고 계신가요?"'
        result["pain_desc"] = (
            "기존 이미지 상세페이지 속에 흩어져 있던 복잡한 상품 정보를 고객이 3초 만에 이해할 수 있도록 텍스트로 전환·정리했습니다. "
            "불필요한 거품을 빼고 가장 확실한 문제 해결책을 제시합니다."
        )
        result["sol_title"] = f"검증된 핵심 솔루션! 『{clean_title}』가 명쾌한 해답을 드립니다."
        result["sol_desc"] = summary_desc

        candidate_points = [
            l for l in all_extracted_lines
            if 10 <= len(l) <= 100 and not any(skip in l for skip in ["로그인", "장바구니", "배송", "쿠키", "개인정보", "고객센터", "Copyright"])
        ]
        if len(candidate_points) >= 4:
            bento = [
                {"step": "POINT 01 · 핵심 특장점", "title": candidate_points[0][:36], "desc": candidate_points[0]},
                {"step": "POINT 02 · 차별화 가치", "title": candidate_points[1][:36], "desc": candidate_points[1]},
                {"step": "POINT 03 · 실전 활용성", "title": candidate_points[2][:36], "desc": candidate_points[2]},
                {"step": "POINT 04 · 기대 효과", "title": candidate_points[3][:36], "desc": candidate_points[3]},
            ]
        else:
            bento = [
                {"step": "POINT 01 · 핵심 가치 (Why)", "title": f"왜 『{clean_title}』를 선택해야 하는가?", "desc": summary_desc[:100]},
                {"step": "POINT 02 · 차별화된 설계 (What)", "title": "타 상품과 비교불가한 핵심 경쟁력", "desc": "불필요한 거품을 걷어내고 고객에게 꼭 필요한 핵심 기능과 혜택만 집중 설계"},
                {"step": "POINT 03 · 간편한 활용 (How)", "title": "초보자도 즉시 체감하는 쉬운 사용성", "desc": "어려운 전문 용어 없이 누구나 바로 적용하고 결과를 얻을 수 있는 직관적 구성"},
                {"step": "POINT 04 · 확실한 만족 (After)", "title": "구매 후 검증된 결과와 사후 지원", "desc": "단회성 구매로 끝나지 않고 실질적인 문제 해결과 만족을 보장하는 솔루션"},
            ]
        result["bento_items"] = bento

        result["metrics"] = [
            {"val": result["price_main"], "label": "거품 없는 합리적 가격"},
            {"val": "4대 핵심", "label": "이미지 OCR/본문 분석 요약"},
            {"val": f"{len(result['videos'])}개 영상" if result["videos"] else "검증 완료", "label": "원본 영상 & 리뷰 검증"},
            {"val": "100%", "label": "고객 눈높이 맞춤 재구성"},
        ]

        result["comp_rows"] = [
            {"label": "💰 가격 및 경제성", "old": "비싼 비용 대비 낮은 체감 효과", "new": f"단 {result['price_main']}으로 핵심 가치 100% 확보"},
            {"label": "📖 정보 전달력", "old": "글씨가 작고 흐릿한 통이미지 나열", "new": "모바일에서도 선명한 텍스트 전환 + 핵심 4단계 요약"},
            {"label": "🎬 영상 & 리뷰 검증", "old": "단조로운 설명과 찾기 힘든 후기", "new": "원본 동영상 그대로 보존 + 광고 포인트 베스트 리뷰 발췌"},
            {"label": "🎯 구매 후 만족도", "old": "복잡한 사용법으로 중도 포기", "new": "누구나 즉시 활용 가능한 눈높이 가이드"},
        ]

        result["faq_items"] = [
            {"q": f"『{clean_title}』의 가장 큰 장점은 무엇인가요?", "a": summary_desc},
            {"q": "기존 상세페이지의 이미지 내용과 영상, 리뷰가 모두 반영되었나요?", "a": "네! 통이미지 속 텍스트를 추출해 읽기 쉽게 정리하고, 원본 동영상과 광고 포인트 베스트 리뷰를 그대로 살려 배치했습니다."},
            {"q": "모바일과 PC에서 모두 선명하게 보이나요?", "a": "네, 통이미지의 흐릿한 글씨 대신 웹 표준 타이포그래피로 재구성하여 어떤 화면에서도 깨짐 없이 선명하게 읽힙니다."},
            {"q": "지금 바로 구매하려면 어떻게 하나요?", "a": "상단 또는 하단의 구매하기 버튼을 클릭하시면 공식 판매 페이지로 즉시 이동합니다."},
        ]

        result["success"] = True
        return result
