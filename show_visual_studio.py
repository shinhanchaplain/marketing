import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QScrollArea, QFrame, QTabWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPalette

class MarketingVisualStudio(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("⚡ 마케팅 자동화 완성 시안 뷰어 (NOVA DESK FOLD ONE)")
        self.setGeometry(100, 100, 1300, 850)
        self.setStyleSheet("background-color: #f1f5f9;")
        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)

        # 상단 타이틀
        title = QLabel("🎨 마케팅 툴 자동 완성 결과 (07차시 상세페이지 & 08차시 캠페인 랜딩페이지)")
        title.setFont(QFont("Malgun Gothic", 16, QFont.Bold))
        title.setStyleSheet("color: #0f172a; padding: 10px 0;")
        main_layout.addWidget(title)

        # 탭 구성
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabBar::tab { font-size: 14px; font-weight: bold; padding: 10px 20px; }
            QTabBar::tab:selected { background: #2563eb; color: white; border-radius: 6px; }
        """)

        tabs.addTab(self.create_desktop_tab(), "🖥️ 08차시 데스크톱 랜딩페이지 (1440px)")
        tabs.addTab(self.create_mobile_tab(), "📱 08차시 모바일 랜딩페이지 (390px)")
        tabs.addTab(self.create_detail_tab(), "📄 07차시 10개 고객 질문 상세페이지")

        main_layout.addWidget(tabs)
        self.setCentralWidget(main_widget)

    def create_section_card(self, badge, title, desc, cta=None, is_highlight=False):
        frame = QFrame()
        bg = "#ffffff" if not is_highlight else "#eff6ff"
        border = "#3b82f6" if is_highlight else "#cbd5e1"
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {bg};
                border: 2px solid {border};
                border-radius: 12px;
                padding: 16px;
                margin-bottom: 12px;
            }}
        """)
        layout = QVBoxLayout(frame)

        badge_lbl = QLabel(badge)
        badge_lbl.setFont(QFont("Malgun Gothic", 10, QFont.Bold))
        badge_lbl.setStyleSheet("color: #2563eb; background: #dbeafe; padding: 2px 8px; border-radius: 4px;")
        layout.addWidget(badge_lbl)

        title_lbl = QLabel(title)
        title_lbl.setFont(QFont("Malgun Gothic", 15, QFont.Bold))
        title_lbl.setStyleSheet("color: #0f172a; margin-top: 6px;")
        layout.addWidget(title_lbl)

        desc_lbl = QLabel(desc)
        desc_lbl.setFont(QFont("Malgun Gothic", 11))
        desc_lbl.setStyleSheet("color: #475569; margin-top: 4px;")
        desc_lbl.setWordWrap(True)
        layout.addWidget(desc_lbl)

        if cta:
            btn = QPushButton(cta)
            btn.setFont(QFont("Malgun Gothic", 11, QFont.Bold))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2563eb;
                    color: white;
                    padding: 8px 16px;
                    border-radius: 6px;
                    border: none;
                }
            """)
            layout.addWidget(btn, alignment=Qt.AlignLeft)

        return frame

    def create_desktop_tab(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(50, 20, 50, 20)

        layout.addWidget(self.create_section_card(
            "01. HERO (첫 약속)", "어디서 일하든, 내 작업을 10초 만에.",
            "6단계 각도 조절 · 620g 휴대용 알루미늄 스탠드 (정가 39,000원)",
            "FOLD ONE 자세히 보기", is_highlight=True
        ))
        layout.addWidget(self.create_section_card(
            "02. PROBLEM (결핍 자극)", "책상은 바뀌는데, 화면 각도는 그대로인가요?",
            "장소가 바뀔 때마다 겪는 시선 높이 불안정과 작업 리듬 파괴를 해결합니다."
        ))
        layout.addWidget(self.create_section_card(
            "03. BENEFIT (고객 변화)", "620g과 전용 파우치 한 묶음으로 가볍게.",
            "가방에 쏙 들어가는 간결한 부피로 다음 작업 장소까지 가볍게 이동합니다."
        ))
        layout.addWidget(self.create_section_card(
            "04. PROOF (숫자 팩트)", "확인된 세 가지 숫자로 선택하세요.",
            "6단계 각도 조절 · 620g 경량 알루미늄 · 39,000원 정직한 가격"
        ))
        layout.addWidget(self.create_section_card(
            "05. OFFER (최종 제안)", "지금 시작하는 패키지: NOVA DESK FOLD ONE",
            "본품 + 전용 보관 파우치 포함 (39,000원)",
            "바로 신청하기", is_highlight=True
        ))

        scroll.setWidget(content)
        return scroll

    def create_mobile_tab(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setAlignment(Qt.AlignHCenter)

        # 모바일 폭 390px 시뮬레이션 컨테이너
        phone = QFrame()
        phone.setFixedWidth(420)
        phone.setStyleSheet("background-color: #ffffff; border: 3px solid #0f172a; border-radius: 24px; padding: 16px;")
        p_layout = QVBoxLayout(phone)

        p_layout.addWidget(self.create_section_card(
            "모바일 01. HERO", "내 작업을 10초 만에.",
            "6단계 각도 조절 · 620g", "자세히 보기", is_highlight=True
        ))
        p_layout.addWidget(self.create_section_card(
            "모바일 02. PROBLEM", "장소마다 달라지는 각도",
            "매번 흐트러지는 작업 환경을 정돈"
        ))
        p_layout.addWidget(self.create_section_card(
            "모바일 03. BENEFIT", "한 묶음으로 가볍게",
            "전용 파우치 포함 구성"
        ))
        p_layout.addWidget(self.create_section_card(
            "모바일 04. PROOF", "숫자로 보는 팩트",
            "6단계 / 620g / 39,000원"
        ))
        p_layout.addWidget(self.create_section_card(
            "모바일 05. OFFER", "패키지 39,000원",
            "본품 + 파우치", "바로 신청하기", is_highlight=True
        ))

        layout.addWidget(phone)
        scroll.setWidget(content)
        return scroll

    def create_detail_tab(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        layout = QVBoxLayout(content)

        questions = [
            ("01. Hook", "왜 지금 멈춰야 하는가?", "화면 각도, 매번 그대로인가요?", "6단계로 내 작업 각도를 10초 만에 맞춥니다."),
            ("02. Problem", "내 문제인가?", "책상은 바뀌는데, 화면 각도는 그대로인가요?", "장소가 달라지면 각도도 다시 선택해야 합니다."),
            ("03. Empathy", "내 상황을 아는가?", "집에서도, 공유오피스에서도, 늦은 작업에서도.", "작업 장소가 바뀌면 시선 높이와 작업 리듬도 무너집니다."),
            ("04. Solution", "무엇이 달라지는가?", "NOVA DESK는 6단계 각도로 화면 위치를 바꿉니다.", "눈높이에 맞춘 각도 선택으로 화면을 정면에서 편안하게 마주합니다."),
            ("05. Benefit", "어떤 결과를 얻는가?", "620g, 전용 파우치까지 한 번에.", "이동 전 준비를 한 묶음으로 챙겨 어디서든 일정한 리듬 유지."),
            ("06. 차별점", "왜 이 방식이어야 하는가?", "6단계 조절 · 620g · 파우치 포함", "차이는 추상적인 미사여구가 아닌 명확한 숫자로 확인하세요."),
            ("07. Proof", "믿을 근거가 있는가?", "6단계 조절 · 620g 경량 · 39,000원", "NOVA DESK의 객관적 팩트를 숫자로 증명합니다."),
            ("08. Spec", "어떻게 사용하는가?", "펼치기 → 각도 선택 → 노트북 거치", "사용 후에는 반으로 접어 전용 파우치에 3초 만에 보관."),
            ("09. FAQ", "무엇이 아직 망설여지는가?", "무게 620g · 파우치 포함 · 정가 39,000원", "망설여지는 핵심 정보 세 가지를 한 화면에서 확인."),
            ("10. CTA", "이제 무엇을 할 것인가?", "NOVA DESK · 39,000원", "오늘부터 내 작업 환경 정돈하기")
        ]

        for num, q, h, sub in questions:
            layout.addWidget(self.create_section_card(
                f"{num} - 질문: {q}", h, sub
            ))

        scroll.setWidget(content)
        return scroll

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MarketingVisualStudio()
    window.show()
    sys.exit(app.exec_())
