// 마케팅 자동화 툴 10섹션 피그마 플러그인 로직
figma.showUI(__html__, { width: 440, height: 460 });

figma.ui.onmessage = async (msg) => {
  if (msg.type === 'BUILD_PAGES') {
    const data = msg.data;
    const mode = msg.mode;

    // 폰트 로드
    await figma.loadFontAsync({ family: "Inter", style: "Regular" });
    await figma.loadFontAsync({ family: "Inter", style: "Bold" });

    let offsetX = figma.viewport.center.x;
    let offsetY = figma.viewport.center.y;

    if (mode === 'both' || mode === 'desktop') {
      const desktopFrame = createResponsiveFrame(data.desktop, "Desktop 1440px - 캠페인", 1440, offsetX, offsetY);
      figma.currentPage.appendChild(desktopFrame);
      offsetX += 1560; // 모바일 프레임과의 간격
    }

    if (mode === 'both' || mode === 'mobile') {
      const mobileFrame = createResponsiveFrame(data.mobile, "Mobile 390px - 캠페인", 390, offsetX, offsetY);
      figma.currentPage.appendChild(mobileFrame);
    }

    figma.notify("✅ 마케팅 10섹션 프레임이 성공적으로 생성되었습니다!");
  }
};

function createResponsiveFrame(specData, title, width, x, y) {
  const frame = figma.createFrame();
  frame.name = title;
  frame.resize(width, 100); // 오토레이아웃으로 늘어남
  frame.x = x;
  frame.y = y;

  // 오토레이아웃 설정 (세로 정렬)
  frame.layoutMode = "VERTICAL";
  frame.primaryAxisSizingMode = "AUTO";
  frame.counterAxisSizingMode = "FIXED";
  frame.itemSpacing = 24;
  frame.paddingTop = 40;
  frame.paddingBottom = 60;
  frame.paddingLeft = width === 1440 ? 120 : 20;
  frame.paddingRight = width === 1440 ? 120 : 20;

  // 배경색 (깔끔한 슬레이트 화이트)
  frame.fills = [{ type: 'SOLID', color: { r: 0.97, g: 0.98, b: 0.99 } }];

  // 상단 타이틀 바
  const header = figma.createText();
  header.characters = `[마케팅 플랜] ${title}`;
  header.fontName = { family: "Inter", style: "Bold" };
  header.fontSize = width === 1440 ? 18 : 14;
  header.fills = [{ type: 'SOLID', color: { r: 0.4, g: 0.45, b: 0.55 } }];
  frame.appendChild(header);

  // 각 섹션 렌더링
  const sections = specData.sections || [];
  for (const sec of sections) {
    const secBox = figma.createFrame();
    secBox.name = `Section_${sec.type}`;
    secBox.layoutMode = "VERTICAL";
    secBox.primaryAxisSizingMode = "AUTO";
    secBox.counterAxisSizingMode = "AUTO";
    secBox.layoutAlign = "STRETCH";
    secBox.itemSpacing = 12;
    secBox.paddingTop = width === 1440 ? 32 : 20;
    secBox.paddingBottom = width === 1440 ? 32 : 20;
    secBox.paddingLeft = width === 1440 ? 32 : 16;
    secBox.paddingRight = width === 1440 ? 32 : 16;
    secBox.cornerRadius = 12;

    // 히어로나 오퍼 섹션은 강조 스타일 적용
    if (sec.type.includes("HERO") || sec.type.includes("OFFER")) {
      secBox.fills = [{ type: 'SOLID', color: { r: 1, g: 1, b: 1 } }];
      secBox.strokes = [{ type: 'SOLID', color: { r: 0.2, g: 0.45, b: 0.95 } }];
      secBox.strokeWeight = 2;
    } else {
      secBox.fills = [{ type: 'SOLID', color: { r: 1, g: 1, b: 1 } }];
      secBox.strokes = [{ type: 'SOLID', color: { r: 0.9, g: 0.92, b: 0.95 } }];
      secBox.strokeWeight = 1;
    }

    // 섹션 뱃지
    const badge = figma.createText();
    badge.characters = sec.type;
    badge.fontName = { family: "Inter", style: "Bold" };
    badge.fontSize = 11;
    badge.fills = [{ type: 'SOLID', color: { r: 0.15, g: 0.4, b: 0.9 } }];
    secBox.appendChild(badge);

    // 제목 텍스트
    const titleText = figma.createText();
    titleText.characters = sec.title;
    titleText.fontName = { family: "Inter", style: "Bold" };
    titleText.fontSize = width === 1440 ? (sec.type.includes("HERO") ? 32 : 22) : 18;
    titleText.fills = [{ type: 'SOLID', color: { r: 0.05, g: 0.08, b: 0.15 } }];
    secBox.appendChild(titleText);

    // 설명 텍스트
    if (sec.desc) {
      const descText = figma.createText();
      descText.characters = sec.desc;
      descText.fontName = { family: "Inter", style: "Regular" };
      descText.fontSize = width === 1440 ? 15 : 13;
      descText.fills = [{ type: 'SOLID', color: { r: 0.35, g: 0.4, b: 0.48 } }];
      secBox.appendChild(descText);
    }

    // CTA 버튼이 있는 경우 버튼 노드 생성
    if (sec.cta) {
      const btn = figma.createFrame();
      btn.name = "CTA_Button";
      btn.layoutMode = "HORIZONTAL";
      btn.primaryAxisSizingMode = "AUTO";
      btn.counterAxisSizingMode = "AUTO";
      btn.paddingLeft = 24;
      btn.paddingRight = 24;
      btn.paddingTop = 12;
      btn.paddingBottom = 12;
      btn.cornerRadius = 8;
      btn.fills = [{ type: 'SOLID', color: { r: 0.14, g: 0.39, b: 0.92 } }];

      const btnText = figma.createText();
      btnText.characters = sec.cta;
      btnText.fontName = { family: "Inter", style: "Bold" };
      btnText.fontSize = 14;
      btnText.fills = [{ type: 'SOLID', color: { r: 1, g: 1, b: 1 } }];
      btn.appendChild(btnText);

      secBox.appendChild(btn);
    }

    frame.appendChild(secBox);
  }

  return frame;
}
