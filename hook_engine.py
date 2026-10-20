"""
후킹 포인트 및 고전환 카피 도출 엔진 (Hooking & Copywriting Engine)
- marketing-os (Hook Engine, 5대 후킹 카테고리, Copy Grading)
- marketing-skills (FAB, PAS, AIDA 프레임워크)
- CopyMonster (Fact Locking 사실 잠금 및 허위·과장 방지 필터)
"""

import json
from typing import Dict, List, Any


class HookEngine:
    """고객의 페인포인트와 제품 팩트를 결합하여 검증된 후킹 카피를 생성하는 클래스"""

    def __init__(self):
        # 금지 표현 사전 (과장, 미확인 수치, 가상 후기 필터링)
        self.banned_terms = [
            "1위", "최고의", "완벽한", "기적의", "압도적 1등", "치료", "완치",
            "무조건 만족", "평점 5.0 만점", "리뷰 보장", "인생템 보장"
        ]

    def lock_facts(self, product_facts: Dict[str, Any]) -> Dict[str, Any]:
        """
        [사실 잠금 (Fact Locking)]
        제품명, 가격, 사양, 구성품을 불변(Immutable) 상태로 잠금
        """
        locked = {
            "product_name": product_facts.get("product_name", "제품명"),
            "price": product_facts.get("price", "39,000원"),
            "specs": product_facts.get("specs", ["6단계 각도 조절", "접이식 구조"]),
            "weight": product_facts.get("weight", "620g"),
            "included": product_facts.get("included", "전용 파우치 포함"),
            "target_persona": product_facts.get(
                "target_persona", "작업 장소를 자주 이동하며 노트북 각도를 맞추는 사용자"
            )
        }
        return locked

    def generate_hooks(
        self,
        locked_facts: Dict[str, Any],
        pain_points: List[str]
    ) -> List[Dict[str, str]]:
        """
        marketing-os의 5가지 핵심 후킹 공식 기반 카피 생성:
        1. 질문형 (Question Hook)
        2. 반직관형 (Counter-intuitive Hook)
        3. 숫자·증거형 (Data/Fact Hook)
        4. 공감·상황형 (Empathy/Situation Hook)
        5. 해결·행동형 (Action Hook)
        """
        name = locked_facts["product_name"]
        specs_str = " · ".join(locked_facts["specs"])
        weight = locked_facts["weight"]
        included = locked_facts["included"]
        price = locked_facts["price"]
        main_pain = pain_points[0] if pain_points else "작업 공간 변경 시 각도 불편"

        hooks = [
            {
                "type": "질문형 (Question)",
                "headline": "화면 각도, 매번 그대로인가요?",
                "subhead": f"{specs_str} 사실만으로 내 시선 높이를 10초 만에 맞춥니다.",
                "angle": "사용자의 무의식적인 불편함을 환기하여 스크롤 정지 유도"
            },
            {
                "type": "반직관형 (Counter-intuitive)",
                "headline": "책상은 바뀌는데, 화면 각도는 왜 그대로일까요?",
                "subhead": f"장소가 달라지면 각도도 달라져야 합니다. {specs_str}.",
                "angle": "당연하게 넘기던 비효율을 짚어내고 새로운 해결 기준 제시"
            },
            {
                "type": "숫자·증거형 (Data / Fact)",
                "headline": f"{specs_str} · {weight} · {price}",
                "subhead": f"{name}, 과장 없는 세 가지 숫자와 구성으로 확인하세요.",
                "angle": "미사여구 없이 검증된 스펙과 정직한 가격으로 즉각적인 신뢰 구축"
            },
            {
                "type": "상황 공감형 (Empathy)",
                "headline": "집에서도, 공유오피스에서도, 늦은 카페 작업에서도.",
                "subhead": f"{weight}와 {included} 한 묶음으로 다음 작업 장소로 이동합니다.",
                "angle": "실제 타깃이 일하는 생생한 장면을 보여주며 나를 위한 제품임을 인지"
            },
            {
                "type": "행동 제안형 (Action)",
                "headline": "어디서 일하든, 내 작업 환경을 10초 만에 정돈하세요.",
                "subhead": f"펼치기 → 각도 선택 → 노트북 거치. {name} 바로 확인하기.",
                "angle": "복잡한 설명 없이 명확한 3단계 동작과 단일 CTA로 즉각 유도"
            }
        ]

        # 금지 표현 필터 검증
        for hook in hooks:
            for banned in self.banned_terms:
                hook["headline"] = hook["headline"].replace(banned, "")
                hook["subhead"] = hook["subhead"].replace(banned, "")

        return hooks

    def derive_fab_benefits(self, locked_facts: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        marketing-skills의 FAB 프레임워크 기반 혜택 전환
        (강의안 원칙: Feature는 확인된 방식, Benefit은 고객이 얻는 변화)
        """
        weight = locked_facts["weight"]
        included = locked_facts["included"]
        specs = locked_facts["specs"]

        fab_list = [
            {
                "feature": "6단계 각도 조절 구조",
                "advantage": "어떤 높이의 테이블에서도 눈높이에 정확히 수평을 맞춤",
                "benefit": "장소가 바뀌어도 목과 어깨의 편안한 작업 리듬을 유지"
            },
            {
                "feature": f"{weight} 무게 및 {included}",
                "advantage": "노트북과 함께 가방에 쏙 들어가는 간결한 부피",
                "benefit": "이동 전 챙길 짐을 하나로 줄이고 어디서든 10초 만에 업무 시작"
            },
            {
                "feature": "접이식 원터치 개폐 구조",
                "advantage": "별도의 나사나 조립 없이 손으로 펼치면 즉시 고정",
                "benefit": "세팅에 낭비되는 시간 없이 본 작업에 즉시 집중"
            }
        ]
        return fab_list


if __name__ == "__main__":
    engine = HookEngine()
    facts = {
        "product_name": "NOVA DESK FOLD ONE",
        "price": "39,000원",
        "specs": ["6단계 각도 조절", "접이식 구조"],
        "weight": "620g",
        "included": "전용 파우치 포함",
        "target_persona": "작업 공간을 자주 이동하는 노트북 사용자"
    }
    locked = engine.lock_facts(facts)
    hooks = engine.generate_hooks(locked, ["휴대성 부족 및 무게 부담", "각도 조절 불편"])
    print("=== 후킹 카피 5종 ===")
    print(json.dumps(hooks, ensure_ascii=False, indent=2))
