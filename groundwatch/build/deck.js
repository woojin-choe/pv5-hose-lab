// PV5 GroundWatch 공모전 제안서 27장 생성기 (v2)
// 디자인 원칙: 노랑은 '변화 신호'에만, 강조는 야간 순찰 장면 한 곳에, 카드·번호·가운뎃점 남발 금지
const pptxgen = require("pptxgenjs");
const sharp = require("sharp");
const path = require("path");
const fs = require("fs");
const { applyTheme } = require(process.env.PPTX_SKILL + "/scripts/apply_theme.js");

const IMG = path.join(__dirname, "..", "images");
const OUT = path.join(__dirname, "..", "PV5_GroundWatch.pptx");
const FONT = "Noto Sans CJK KR";
const HF = "Noto Serif CJK KR";
const K = { night: "0A1628", navy: "0B1F3A", amber: "F5B400", red: "D93025", ink: "101828", steel: "5B6573", mute: "8A94A3", fog: "F2F4F7", line: "DCE1E8", white: "FFFFFF", green: "2F9E44", blue: "1C64B5" };
const THEME = {
  name: "GroundWatch", headFontFace: HF, bodyFontFace: FONT,
  colors: { dk1: K.ink, lt1: K.white, dk2: K.navy, lt2: K.fog, accent1: K.navy, accent2: K.amber, accent3: K.red, accent4: K.green, accent5: K.blue, accent6: K.steel, hlink: K.blue, folHlink: "7048E8" },
};
const BASIS = "작성 기준일 2026.10.10";
const M = 0.6, CW = 13.333 - 2 * M;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.title = "PV5 GroundWatch";
pres.author = "";
pres.theme = { headFontFace: HF, bodyFontFace: FONT };
// 굵은 글씨는 SemiBold 서체로, 큰 글씨는 한 단계 줄여 보고서 톤으로 맞춘다
const tsize = (n) => (n >= 40 ? Math.round(n * 0.72) : n >= 24 ? Math.round(n * 0.8) : n >= 15 ? n - 1 : n);
function tone(o) {
  if (!o) return o;
  const r = { ...o };
  if (r.fontSize) r.fontSize = tsize(r.fontSize);
  return r;
}
const _addSlide = pres.addSlide.bind(pres);
pres.addSlide = (...a) => {
  const sl = _addSlide(...a);
  const _t = sl.addText.bind(sl);
  sl.addText = (t, o) => _t(Array.isArray(t) ? t.map((r) => ({ ...r, options: tone(r.options) })) : t, o && o.placeholder ? o : tone(o));
  return sl;
};

pres.defineSlideMaster({
  title: "GW_CONTENT",
  background: { color: K.white },
  objects: [
    { line: { x: M, y: 1.0, w: CW, h: 0, line: { color: "C9D0DA", width: 0.75 } } },
    { line: { x: M, y: 7.12, w: CW, h: 0, line: { color: "DCE1E8", width: 0.5 } } },
    { text: { text: "PV5 GroundWatch  |  반복 관측 기반 도심 지하공동 변화 감지 순찰체계", options: { x: M, y: 7.15, w: 9, h: 0.25, fontFace: FONT, fontSize: 8.5, color: K.mute, margin: 0, valign: "middle" } } },
    { placeholder: { options: { name: "title", type: "title", x: M, y: 0.42, w: CW, h: 0.52, fontFace: HF, fontSize: 21, bold: true, color: K.navy, align: "left", valign: "middle", margin: 0 }, text: "" } },
  ],
  slideNumber: { x: 12.25, y: 7.15, w: 0.5, h: 0.25, fontFace: FONT, fontSize: 9, color: K.mute, align: "right" },
});
pres.defineSlideMaster({ title: "GW_FULL", background: { color: "000000" }, objects: [] });

// ---------- 헬퍼 ----------
const DIM = {};
const FIG = { n: 0 };
const EXT = {};
async function loadDims() { for (const f of fs.readdirSync(IMG)) if (/\.(png|jpg)$/.test(f)) { const m = await sharp(path.join(IMG, f)).metadata(); DIM[f.slice(0, -4)] = m.width / m.height; EXT[f.slice(0, -4)] = f.slice(-3); } }
function img(s, name, x, y, w, h, o = {}) {
  const r = DIM[name]; let W = w, H = h;
  if (!o.stretch) { if (w / h > r) W = h * r; else H = w / r; }
  const X = o.align === "left" ? x : o.align === "right" ? x + w - W : x + (w - W) / 2;
  const Y = o.valign === "top" ? y : o.valign === "bottom" ? y + h - H : y + (h - H) / 2;
  s.addImage({ path: path.join(IMG, name + "." + EXT[name]), x: X, y: Y, w: W, h: H, objectName: name });
  if (o.cap) { FIG.n += 1; s.addText([{ text: `그림 ${FIG.n}. `, options: { bold: true, color: K.ink } }, { text: o.cap, options: { color: K.steel } }], { x: X, y: Y + H + 0.04, w: Math.max(W, 3), h: 0.24, fontSize: 9.5, margin: 0, valign: "top", isTextBox: true, objectName: "caption" }); }
  return { x: X, y: Y, w: W, h: H };
}
const ico = (s, name, x, y, sz) => s.addImage({ path: path.join(IMG, "ico_" + name + ".png"), x, y, w: sz, h: sz, objectName: "icon_" + name });
const SECT = { "문제": ["Ⅰ", "문제 정의", "1"], "운영 모델": ["Ⅱ", "운영 모델", "2"], "확장": ["Ⅲ", "확장 방향", "3"], "부록": ["부록", "", "A"] };
const SEQ = {};
function slideC(desc, tag, tagColor, section) {
  const s = pres.addSlide({ masterName: "GW_CONTENT", sectionTitle: section });
  const [rn, nm, pre] = SECT[section];
  SEQ[section] = (SEQ[section] || 0) + 1;
  const label = tag.replace(/^#\d+\s*/, "").replace(/^(확장|부록)\s*\d+\s*/, "");
  const crumb = (nm ? `${rn}. ${nm}` : rn) + `   ›   ${pre}.${SEQ[section]}  ${label}`;
  s.addText(crumb, { x: M, y: 0.16, w: CW, h: 0.26, fontSize: 10, color: K.steel, margin: 0, valign: "middle", isTextBox: true, objectName: "crumb" });
  s.addText(desc, { placeholder: "title" });
  return s;
}
function lead(s, text, o = {}) {
  s.addText([{ text: "□ ", options: { color: K.navy, bold: true } }, { text, options: { color: K.ink } }], { x: o.x || M, y: o.y || 1.12, w: o.w || CW, h: o.h || 0.5, fontSize: o.fs || 15, margin: 0, valign: "top", isTextBox: true, objectName: "lead" });
}
function src(s, text, dark) { s.addText(text.replace(/^출처:\s*/, "자료: ").replace(/^참고:\s*/, "자료: "), { x: M, y: 6.86, w: CW, h: 0.24, fontSize: 9, color: dark ? "8C9BB0" : K.mute, margin: 0, valign: "middle", isTextBox: true, objectName: "source" }); }
function bubble(s, text, x, y, w, h, o = {}) {
  s.addText([{ text: "시사점  ", options: { bold: true, color: K.navy } }, { text: text.replace(/\n/g, " "), options: { color: K.ink } }], { shape: pres.ShapeType.rect, x, y, w, h, fill: { color: "EEF2F7" }, line: { color: "C9D0DA", width: 0.75 }, fontSize: Math.min(o.fs || 14, 14), align: "left", valign: "middle", margin: 8, isTextBox: true, objectName: "keyMessage" });
}
function arrowLine(s, x1, y1, x2, y2, color = K.navy, w = 1.75) {
  const flipH = x2 < x1, flipV = y2 < y1;
  s.addShape(pres.ShapeType.line, { x: Math.min(x1, x2), y: Math.min(y1, y2), w: Math.max(Math.abs(x2 - x1), 0.001), h: Math.max(Math.abs(y2 - y1), 0.001), flipH, flipV, line: { color, width: w, endArrowType: "triangle" }, objectName: "arrow" });
}
function rule(s, x, y, w, color = K.line) { s.addShape(pres.ShapeType.line, { x, y, w, h: 0, line: { color, width: 1 }, objectName: "rule" }); }
function panel(s, x, y, w, h, fill = K.fog) { s.addShape(pres.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.06, fill: { color: fill }, line: { color: fill }, objectName: "panel" }); }
function block(s, x, y, w, title, body, o = {}) {
  s.addText("○ " + title, { x, y, w, h: 0.38, fontSize: o.tfs || 16, bold: true, color: o.tc || K.ink, margin: 0, valign: "top", isTextBox: true });
  if (body) s.addText(body, { x, y: y + 0.42, w, h: o.h || 0.9, fontSize: o.fs || 14, color: o.bc || K.steel, margin: 0, valign: "top", paraSpaceAfter: 3, isTextBox: true });
}
function num(s, n, x, y, d = 0.42, fill = K.navy, color = K.white) {
  s.addText(String(n), { shape: pres.ShapeType.ellipse, x, y, w: d, h: d, fill: { color: fill }, line: { color: fill }, fontSize: 14, bold: true, color, align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: "step" });
}
function stat(s, x, y, w, value, label, o = {}) {
  s.addText(value, { x, y, w, h: 0.62, fontSize: o.vfs || 32, bold: true, color: o.vc || K.navy, margin: 0, valign: "bottom", isTextBox: true });
  s.addText(label, { x, y: y + 0.66, w, h: 0.5, fontSize: 13, color: o.lc || K.steel, margin: 0, valign: "top", isTextBox: true });
}
const L = (arr, o = {}) => arr.map((t, i) => ({ text: t, options: { breakLine: i < arr.length - 1, ...o, ...(o.bullet ? { bullet: { code: "2013", indent: 14 } } : {}) } }));

async function build() {
  await loadDims();
  let s;

  // ===== 1. 표지 =====
  pres.addSection({ title: "문제" });
  s = pres.addSlide({ masterName: "GW_FULL", sectionTitle: "문제" });
  s.background = { color: K.white };
  s.addShape(pres.ShapeType.rect, { x: 6.9, y: 0, w: 6.433, h: 7.5, fill: { color: K.night }, line: { color: K.night }, objectName: "panel" });
  img(s, "f_front_n", 6.9, 1.2, 6.433, 5.1);
  s.addText("제5회 기아 PBV 아이디어 공모전  |  일반 부문 제안서", { x: M, y: 0.7, w: 6, h: 0.3, fontSize: 11, color: K.steel, margin: 0, isTextBox: true });
  s.addText("PV5 GroundWatch", { x: M, y: 1.35, w: 6.1, h: 0.8, fontFace: HF, fontSize: 38, bold: true, color: K.navy, margin: 0, isTextBox: true });
  s.addText("반복 관측 기반 도심 지하공동 변화 감지 순찰체계", { x: M, y: 2.2, w: 6.1, h: 0.45, fontFace: HF, fontSize: 18, color: K.ink, margin: 0, isTextBox: true });
  s.addShape(pres.ShapeType.line, { x: M, y: 2.95, w: 5.9, h: 0, line: { color: "C9D0DA", width: 0.75 }, objectName: "rule" });
  s.addText("도로가 무너지기까지 1~2분. 그 아래의 변화는 더 먼저 시작됐습니다.", { x: M, y: 3.15, w: 6.0, h: 0.6, fontSize: 14, color: K.ink, margin: 0, valign: "top", isTextBox: true });
  const HH = (t) => ({ text: t, options: { bold: true, color: K.steel, fill: { color: K.fog } } });
  s.addTable([[HH("구분"), HH("서울 강동구 명일동 땅꺼짐(2025.3.24)")], ["규모", "길이 22m, 폭 18m, 깊이 16m (약 1~2분 만에 확대)"], ["인명 피해", "사망 1명, 부상 1명"]], { x: M, y: 3.85, w: 5.9, colW: [1.2, 4.7], fontFace: FONT, fontSize: 11, color: K.ink, border: { type: "solid", color: K.line, pt: 0.75 }, rowH: 0.34, valign: "middle", margin: [0, 0.08, 0, 0.08], objectName: "facts" });
  s.addText("2026. 10.", { x: M, y: 6.05, w: 6, h: 0.3, fontSize: 12, color: K.steel, margin: 0, isTextBox: true });
  s.addText("자료: 국토교통부·중앙지하사고조사위원회 「서울 명일동 땅꺼짐 사고 조사결과」(2025.12.3).", { x: M, y: 6.8, w: 6.1, h: 0.45, fontSize: 8.5, color: K.mute, margin: 0, valign: "top", isTextBox: true });
  s.addNotes("이 숫자 뒤에는 집으로 돌아가지 못한 한 사람이 있습니다. 우리가 찾으려는 것은 이미 생긴 구멍이 아니라, 구멍이 되기 전의 변화입니다.\n\n[사실] 2025.3.24 18:28경 서울 강동구 명일동. 붕괴 시작 후 약 1~2분 만에 길이 22m, 폭 18m, 깊이 16m로 확대. 사망 1명, 부상 1명.\n출처: 국토교통부 정책브리핑 '땅꺼짐 사고 조사결과 발표'(2025.12.3) https://m.korea.kr/briefing/policyBriefingView.do?newsId=156732996\n최종보고서: https://www.molit.go.kr/USR/policyData/m_34681/dtl.jsp?id=4872\n\n표현 원칙: 희생자 이름, 얼굴, 구조 장면은 쓰지 않습니다. 특정 기관 책임을 단정하지 않습니다.\n이미지: PV5 실차 사진(Alexander Migl, CC BY-SA 4.0, https://commons.wikimedia.org/wiki/File:Kia_PV5_Cargo_IMG_7825.jpg).");

  // ===== 2. 제안 배경 =====
  s = slideC("붕괴는 갑자기 보였지만, 원인은 지하에서 쌓이고 있었다", "제안 배경", K.red, "문제");
  lead(s, "사고조사위원회는 하나의 원인이 아니라 지하에서 오래 쌓인 조건들이 겹쳤다고 발표했습니다.");
  img(s, "mechanism", M, 1.75, 7.3, 3.75, { align: "left", cap: "명일동 사고 조사결과의 원인 요소 개념도" });
  const causes = [["직접 원인", "심층풍화대 불연속면이 만든 쐐기형 토체가 터널 굴착 중 미끄러짐", K.red], ["간접 원인", "인근 터널공사로 지하수위 최대 26m 저하", K.steel], ["간접 원인", "노후 하수관의 장기 누수로 경계면 강도 저하", K.steel], ["간접 원인", "강관보강 그라우팅의 지보 성능 한계", K.steel]];
  causes.forEach(([k, t, c], i) => {
    const y = 1.75 + i * 0.82;
    s.addText(k, { x: 8.2, y, w: 4.5, h: 0.28, fontSize: 12, bold: true, color: c, margin: 0, isTextBox: true });
    s.addText(t, { x: 8.2, y: y + 0.28, w: 4.53, h: 0.5, fontSize: 15, color: K.ink, margin: 0, valign: "top", isTextBox: true });
  });
  rule(s, 8.2, 5.1, 4.53);
  s.addText("결과: 도로 중앙선 부근에서 시작해 약 1~2분 만에 22×18×16m로 확대", { x: 8.2, y: 5.15, w: 4.53, h: 0.6, fontSize: 15, bold: true, color: K.ink, margin: 0, valign: "top", isTextBox: true });
  [["보이지 않음", K.steel, 0.6, 1.75], ["쌓임", K.steel, 3.05, 0.85], ["갑자기 드러남", K.red, 4.6, 2.2]].forEach(([t, c, x, w], i) => {
    s.addText(t, { x, y: 5.78, w, h: 0.5, fontSize: 21, bold: true, color: c, margin: 0, valign: "middle", isTextBox: true });
    if (i < 2) arrowLine(s, x + w + 0.12, 6.03, [3.05, 4.6][i] - 0.12, 6.03, K.mute);
  });
  s.addText("사고 뒤의 복구보다, 사고 전의 변화를 관리해야 합니다.", { x: M, y: 6.38, w: 7.3, h: 0.45, fontSize: 18, bold: true, color: K.navy, margin: 0, isTextBox: true });
  panel(s, 8.2, 5.85, 4.53, 1.0, K.navy);
  s.addText(L(["우리의 목표", "한 번의 조기 발견이 한 사람의 일상을 지키도록, 도시가 같은 길을 계속 기억하게 만듭니다."]).map((r, i) => ({ text: r.text, options: { ...r.options, fontSize: i ? 12 : 14, bold: !i, color: i ? "C9D3E0" : K.amber } })), { x: 8.38, y: 5.9, w: 4.2, h: 0.9, margin: 0, valign: "middle", paraSpaceAfter: 2, isTextBox: true });
  src(s, "출처: 국토교통부 땅꺼짐 사고 조사결과(2025.12.3). 단면도는 조사 요소를 단순화한 개념도이며, GroundWatch가 이 사고를 막을 수 있었다는 뜻이 아닙니다.");
  s.addNotes("명일동 사고는 하나의 원인이 아니라 여러 조건이 겹친 결과였습니다. 직접 원인은 심층풍화대 불연속면이 만든 쐐기형 토체의 미끄러짐, 간접 원인은 터널공사로 인한 지하수위 26m 저하, 노후 하수관의 장기 누수, 강관보강 그라우팅의 지보 성능 한계입니다.\n\n주의: 이 사고는 깊은 지질구조와 터널공사가 얽힌 사고이고, GroundWatch의 차량형 GPR은 약 2m 안팎의 얕은 공동을 주로 봅니다. 그래서 이 사고를 막을 수 있었다고 말하지 않습니다. 이 사례는 단발성 점검을 반복 관측과 변화 관리로 바꿔야 하는 이유로만 씁니다.\n\n출처: https://m.korea.kr/briefing/policyBriefingView.do?newsId=156732996");

  // ===== 3. 현재 탐사 방식 =====
  s = slideC("서울시는 이미 GPR로 도로 아래를 탐사하고 있다", "현재 탐사 방식", K.navy, "문제");
  lead(s, "차량형 GPR로 넓게 선별하고 수동 GPR과 천공·내시경으로 확인합니다. GroundWatch는 이 체계를 보완합니다.");
  img(s, "ph_gpr_cart", M, 1.7, 5.4, 3.95, { stretch: true, cap: "수동(손수레형) GPR 실제 장비" });
  [["radar", "차량형 GPR", "넓은 도로를 빠르게 선별합니다. 한 번 지나가며 약 3m 폭을 탐사합니다.", "한계: 고주파 GPR 탐지 깊이 약 2m"], ["scan", "수동(손수레형) GPR", "좁은 골목과 보도처럼 차량이 들어가기 어려운 곳을 작업자가 밀며 조사합니다.", "한계: 넓은 구간에는 시간과 인력이 많이 듭니다"], ["camera", "천공과 내시경", "공동이 의심되는 지점을 뚫어 실제 빈 공간과 규모를 확인합니다.", "한계: 승인과 교통통제가 필요한 지점 단위 작업"]].forEach(([ic, t, b, lim], i) => {
    const y = 1.7 + i * 1.38;
    ico(s, ic, 6.4, y + 0.02, 0.5);
    s.addText(t, { x: 7.1, y, w: 5.63, h: 0.38, fontSize: 18, bold: true, color: K.ink, margin: 0, isTextBox: true });
    s.addText(b, { x: 7.1, y: y + 0.4, w: 5.63, h: 0.55, fontSize: 14, color: K.steel, margin: 0, valign: "top", isTextBox: true });
    s.addText(lim, { x: 7.1, y: y + 0.95, w: 5.63, h: 0.3, fontSize: 13, bold: true, color: K.red, margin: 0, isTextBox: true });
  });
  rule(s, M, 6.15, CW);
  [["33,129km", "누적 탐사 거리(2014~2025.9)"], ["7,760개", "같은 기간 발견한 공동"], ["16,423km", "2026년 탐사 계획"], ["9명 → 19명", "GPR 전담 인력"]].forEach(([v, l], i) => {
    s.addText(v, { x: M + i * 3.1, y: 6.2, w: 1.75, h: 0.45, fontSize: 22, bold: true, color: K.navy, margin: 0, valign: "middle", isTextBox: true });
    s.addText(l, { x: M + i * 3.1 + 1.75, y: 6.2, w: 1.3, h: 0.45, fontSize: 11, color: K.steel, margin: 0, valign: "middle", isTextBox: true });
  });
  src(s, "출처: 서울시 GPR 도입 자료, 서울시 지반침하 예방체계 강화 보도자료, 경향신문 2025.10.19, 세이프타임즈. 사진: The Charles Machine Works, CC BY-SA 2.0, Wikimedia Commons");
  s.addNotes("현재 서울시는 차량형 GPR, 수동형 GPR, 천공과 내시경을 조합해 운영합니다.\n- 차량형 GPR: 서울시는 2015년 국내 처음 차량탑재형 GPR을 도입했고, 한 번 지나가며 약 3m 폭을 탐사합니다. https://news.seoul.go.kr/safe/archives/41339\n- 누적 33,129km, 공동 7,760개(2014~2025.9): 경향신문 2025.10.19 https://www.khan.co.kr/article/202510191122011\n- 2026년 16,423km, GPR 인력 9명→19명: 서울시 보도자료 https://www.seoul.go.kr/news/news_report.do?nttNo=454742 (언론에 나온 18,000km 계획과 차이가 있어 공식 발표 값을 씀)\n- 고주파 GPR 탐지 깊이 약 2m: https://www.safetimes.co.kr/news/articleView.html?idxno=231486\n사진: Ground Penetrating Radar in use, The Charles Machine Works, CC BY-SA 2.0, https://commons.wikimedia.org/wiki/File:Ground_Penetrating_Radar_in_use.jpg");

  // ===== 4. 현재 방식의 공백 =====
  s = slideC("탐사와 탐사 사이, 지하의 변화는 기록되지 않는다", "현재 방식의 공백", K.red, "문제");
  lead(s, "2024년 연희동 성산로는 5월 정기 GPR 탐사에서 공동이 발견되지 않았고, 8월 29일 도로가 함몰됐습니다.");
  img(s, "gap_timeline", M, 1.75, 8.5, 2.1, { align: "left", cap: "연희동 성산로 정기 탐사와 함몰 시점" });
  img(s, "ph_crack", 9.35, 1.7, 3.38, 2.54, { stretch: true });
  s.addText("포장이 갈라지며 꺼지기 시작한 모습(해외 사례)", { x: 9.35, y: 4.27, w: 3.38, h: 0.3, fontSize: 11, color: K.steel, margin: 0, isTextBox: true });
  bubble(s, "5월엔 없었고, 8월엔 무너졌습니다.", M, 6.35, 6.0, 0.42, { fill: K.red, fs: 14 });
  [["한 시점의 결과", "회차별 결과가 보고서 단위로 끝나 시간축 비교가 어렵습니다."], ["변화 추적", "같은 지점의 신호가 새로 생겼는지, 커졌는지 이어서 보기 어렵습니다."], ["다음 조사 순서", "어느 구간을 먼저 다시 볼지 데이터로 정하기 어렵습니다."], ["같은 지점 찾기", "현장 기술자가 정확히 같은 지점을 다시 찾기 어렵습니다."]].forEach(([t, b], i) => {
    const x = M + i * 3.1;
    rule(s, x, 4.75, 2.85, K.ink);
    block(s, x, 4.88, 2.85, t, b, { h: 1.0 });
  });
  s.addText("[가설] 위 네 가지 공백은 지자체와 탐사업체 인터뷰로 검증합니다.", { x: 6.9, y: 6.4, w: 5.8, h: 0.35, fontSize: 13, color: K.steel, margin: 0, isTextBox: true });
  src(s, "출처: 뉴시스 2024.8.30(서울시 설명: 5.7~5.16 GPR 탐사차량 2대, 인력 16명 투입, 당시 빈 공간 미발견), 이투데이 2024.9. 연희동 함몰 규모는 공식 확인 전이라 쓰지 않았습니다. 사진: Famartin, CC BY-SA 4.0");
  s.addNotes("연희동 성산로 사례는 반복 관측이 왜 필요한지 보여줍니다. 서울시 설명에 따르면 이 구간은 정기점검 대상으로 2024년 5월 7일부터 16일까지 GPR 탐사차량 2대와 인력 16명을 들여 조사했지만, 당시 빈 공간이 발견되지 않았습니다. 그리고 8월 29일 함몰이 일어났습니다.\n이것이 GPR 탐사의 실패라는 뜻은 아닙니다. 지하는 변하고, 한 시점의 결과는 그 시점만 말해 준다는 뜻입니다.\n\n출처: https://www.newsis.com/view/NISX20240830_0002869815 , https://www.etoday.co.kr/news/view/2397645 , https://mediahub.seoul.go.kr/archives/2012160\n[추가 확인 필요] 연희동 함몰 규모(가로, 세로, 깊이)는 공식 자료로 확인하지 못해 쓰지 않았습니다.\n[가설] 아래 네 가지 공백은 현장 인터뷰로 검증합니다.");

  // ===== 5. 솔루션 개요 =====
  s = slideC("같은 길을 반복해서 보고, 달라진 곳만 다시 확인한다", "솔루션 개요", K.amber, "문제");
  lead(s, "순찰, 비교, 현장 재확인이 한 바퀴를 돌 때마다 같은 도로의 기록이 한 겹씩 쌓입니다.");
  img(s, "f_front", M, 1.75, 4.1, 2.85, { stretch: true });
  block(s, M, 4.75, 4.1, "1  새벽 순찰", "같은 경로를 같은 장비로 반복 주행하며 GPR과 영상을 수집합니다.", { h: 0.8 });
  arrowLine(s, 4.85, 3.17, 5.35, 3.17);
  panel(s, 5.45, 1.75, 3.5, 2.85, K.night);
  [["radar_w", "GPR, 카메라 수집"], ["map_w", "위치, 깊이, 시간 기록"], ["brain_a", "이전 회차와 비교"], ["layers_w", "4D 지하 변화지도"]].forEach(([ic, t], i) => {
    ico(s, ic, 5.7, 1.98 + i * 0.64, 0.4);
    s.addText(t, { x: 6.25, y: 1.96 + i * 0.64, w: 2.6, h: 0.44, fontSize: 15, bold: true, color: i === 2 ? K.amber : K.white, margin: 0, valign: "middle", isTextBox: true });
  });
  block(s, 5.45, 4.75, 3.5, "2  기록과 비교", "AI가 달라진 지점을 찾고 전문가가 검토합니다.", { h: 0.8 });
  arrowLine(s, 9.05, 3.17, 9.55, 3.17);
  [["server", "차량 앱과 Edge Gateway"], ["glasses", "AR 글래스"], ["scan", "수동 GPR 재탐사"]].forEach(([ic, t], i) => {
    ico(s, ic, 9.7, 1.85 + i * 0.95, 0.55);
    s.addText(t, { x: 10.4, y: 1.85 + i * 0.95, w: 2.33, h: 0.55, fontSize: 15, bold: true, color: K.ink, margin: 0, valign: "middle", isTextBox: true });
  });
  block(s, 9.7, 4.75, 3.03, "3  현장 재확인", "승인된 지점만 정차해 다시 탐사합니다.", { h: 0.8 });
  arrowLine(s, 11.2, 5.95, 11.2, 6.45, K.amber, 2);
  s.addShape(pres.ShapeType.line, { x: 2.65, y: 6.45, w: 8.55, h: 0, line: { color: K.amber, width: 2 }, objectName: "loop" });
  arrowLine(s, 2.65, 6.45, 2.65, 5.95, K.amber, 2);
  s.addText("4  확인 결과가 다음 순찰과 AI 개선으로 돌아갑니다", { x: 3.0, y: 6.5, w: 7.8, h: 0.38, fontSize: 15, bold: true, color: K.navy, align: "center", margin: 0, isTextBox: true });
  src(s, "구성은 제안안이며 장비 사양과 통신 구조는 실증 단계에서 확정합니다.");
  s.addNotes("GroundWatch는 네 단계가 반복되는 구조입니다. 새벽에 같은 경로를 순찰하고, 회차별 데이터를 위치, 깊이, 시간으로 기록해 비교하고, 전문가가 승인한 지점만 현장에서 다시 확인하고, 그 결과가 다음 순찰과 AI 개선으로 돌아갑니다.\n핵심은 한 번의 탐사가 아니라 반복 관측과 변화 관리입니다.");

  // ===== 6. 구분장 =====
  pres.addSection({ title: "운영 모델" });
  s = pres.addSlide({ masterName: "GW_FULL", sectionTitle: "운영 모델" });
  s.background = { color: K.white };
  s.addShape(pres.ShapeType.rect, { x: 7.4, y: 0, w: 5.933, h: 7.5, fill: { color: K.night }, line: { color: K.night }, objectName: "panel" });
  img(s, "f_int6", 7.4, 1.2, 5.933, 5.1);
  s.addText("Ⅱ", { x: M, y: 1.2, w: 3, h: 1.0, fontFace: HF, fontSize: 54, bold: true, color: K.navy, margin: 0, isTextBox: true });
  s.addText("지금 바로 적용 가능한 운영 모델", { x: M, y: 2.25, w: 6.4, h: 0.6, fontFace: HF, fontSize: 26, bold: true, color: K.ink, margin: 0, isTextBox: true });
  s.addShape(pres.ShapeType.line, { x: M, y: 3.05, w: 6.2, h: 0, line: { color: "C9D0DA", width: 0.75 }, objectName: "rule" });
  s.addText(["2.1  새벽 정기순찰", "2.2  PV5 이동형 탐사실", "2.3  4D 지하 변화지도", "2.4  AI 변화 감지", "2.5  재확인 포인트 생성", "2.6  GroundWatch Patrol 차량 앱", "2.7  차량·센서·AR 소프트웨어 브리지", "2.8  AR 위치 보정", "2.9  AR 수동 GPR 재탐사", "2.10  수동 GPR 교차검증", "2.11  정밀조사와 결과 저장"].map((t, i, a) => ({ text: t, options: { breakLine: i < a.length - 1 } })), { x: M, y: 3.25, w: 6.4, h: 3.4, fontSize: 12.5, color: K.steel, margin: 0, valign: "top", paraSpaceAfter: 4, isTextBox: true });
  s.addNotes("여기서부터는 지금 기술로 바로 꾸릴 수 있는 운영 모델 열한 가지를 순서대로 보여드립니다.");

  // ===== 7. #1 새벽 순찰 =====
  s = slideC("교통량이 적은 시간에 도로 아래 변화를 기록합니다", "#1 새벽 순찰", K.amber, "운영 모델");
  s.addShape(pres.ShapeType.rect, { x: M, y: 1.15, w: 4.5, h: 5.6, fill: { color: K.night }, line: { color: K.night }, objectName: "panel" });
  img(s, "f_rear_n", 5.25, 1.15, 7.48, 4.99, { stretch: true, cap: "새벽 순찰 차량 구성(루프 랙·경광등·GNSS 안테나)" });
  s.addText("보이지 않는 위험은,\n반복해서 봐야 보입니다.", { x: M + 0.1, y: 1.55, w: 4.3, h: 1.3, fontSize: 30, bold: true, color: K.white, margin: 0, valign: "top", isTextBox: true });
  [["moon_w", "차량과 보행이 가장 적은 새벽에 반복 주행"], ["car_w", "엔진 소음과 배기가스 없이 주택가 저속 운행"], ["route_w", "같은 경로, 같은 장비로 회차끼리 비교"], ["radar_w", "후방 하부 GPR 어레이로 차로를 연속 스캔"]].forEach(([ic, t], i) => {
    ico(s, ic, M + 0.1, 3.3 + i * 0.62, 0.34);
    s.addText(t, { x: M + 0.6, y: 3.27 + i * 0.62, w: 3.9, h: 0.42, fontSize: 14, color: "E2E8F0", margin: 0, valign: "middle", isTextBox: true });
  });
  bubble(s, "어제와 같은 길, 같은 장비, 같은 속도", M + 0.1, 5.95, 4.2, 0.55, { fs: 14 });
  src(s, "저속 운행 시 실제 소음과 주행거리 영향은 [실증 필요]");
  s.addNotes("새벽은 주차 차량과 보행자가 가장 적은 시간이라 같은 경로를 같은 조건으로 반복 주행하기 좋습니다. PV5는 전기차라 엔진 공회전 소음과 배기가스 없이 주택가를 저속으로 오래 달릴 수 있습니다.\n[실증 필요] 저속 장시간 운행 시 배터리 소모와 주행거리 영향, 실제 소음 수준.\n참고: https://www.kia.com/kr/vehicles/pv5-cargo/features");

  // ===== 8. #2 이동형 탐사실 =====
  s = slideC("PV5는 센서 운반차가 아니라 이동형 탐사·분석·검증 플랫폼", "#2 이동형 탐사실", K.amber, "운영 모델");
  lead(s, "장비를 차량에 고정해 회차마다 같은 측정 환경을 유지하고, 차 안에서 분석하고, 내려서 검증합니다.");
  const cw = img(s, "f_int", M, 1.6, 5.4, 3.04, { stretch: true, cap: "카고룸 탐사실 구성(뒷문 개방)" });
  const gp = img(s, "f_gpr", M + 5.55, 1.6, 2.05, 3.04, { stretch: true, cap: "후방 하부 다채널 GPR" });
  const PIN = [["1", 0.383, 0.536, "Edge Gateway·엣지 AI 랙"], ["2", 0.454, 0.49, "작업대·모니터"], ["3", 0.588, 0.747, "수동 GPR 카트(고정)"], ["4", 0.588, 0.41, "장비 수납장"], ["5", 0.658, 0.8, "라바콘·안전장비"], ["6", 0.504, 0.222, "작업 조명"]];
  PIN.forEach(([n, fx, fy]) => { const x = cw.x + fx * cw.w, y = cw.y + fy * cw.h; s.addText(n, { shape: pres.ShapeType.ellipse, x: x - 0.14, y: y - 0.14, w: 0.28, h: 0.28, fill: { color: K.navy }, line: { color: K.white, width: 1.5 }, fontSize: 10, bold: true, color: K.white, align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: "pin" }); });
  s.addText("7", { shape: pres.ShapeType.ellipse, x: gp.x + gp.w * 0.5 - 0.14, y: gp.y + gp.h * 0.62 - 0.14, w: 0.28, h: 0.28, fill: { color: K.navy }, line: { color: K.white, width: 1.5 }, fontSize: 10, bold: true, color: K.white, align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: "pin" });
  [...PIN, ["7", 0, 0, "후방 하부 다채널 GPR"], ["8", 0, 0, "루프 경광등·GNSS"]].forEach(([n, , , t2], i) => { const x = M + (i % 4) * 1.9, y = 5.0 + Math.floor(i / 4) * 0.27; s.addText([{ text: n + " ", options: { bold: true, color: K.navy } }, { text: t2, options: { color: K.ink } }], { x, y, w: 1.88, h: 0.26, fontSize: 10, margin: 0, valign: "middle", isTextBox: true }); });
  [["외부", "후방 하부 다채널 GPR, 전방·좌우·후방 카메라, RTK-GNSS, IMU, 휠 인코더, 거리 센서, 노면 조명과 경광장치", K.ink], ["화물실 전방", "Edge Gateway, 산업용 엣지 AI 컴퓨터, GPR 제어장치, 저장장치, 보안 네트워크, RTK 수신, 전원 분배", K.blue], ["화물실 측면", "지면 밀착형 수동 GPR, AR 글래스와 충전 보관함, RTK 이동국, 현장 기준 마커, 교체형 안테나", K.navy], ["화물실 후방", "관로 내시경, 작업 조명, 안전 표지판, 라바콘, 반사조끼, 개인보호장비, 세척·점검 도구", "B4232A"]].forEach(([t, b, c], i) => {
    const y = 1.65 + i * 0.8;
    s.addShape(pres.ShapeType.ellipse, { x: 8.45, y: y + 0.09, w: 0.15, h: 0.15, fill: { color: c }, line: { color: c }, objectName: "dot" });
    s.addText(t, { x: 8.72, y, w: 4.0, h: 0.32, fontSize: 14, bold: true, color: K.ink, margin: 0, isTextBox: true });
    s.addText(b, { x: 8.72, y: y + 0.3, w: 4.0, h: 0.5, fontSize: 11, color: K.steel, margin: 0, valign: "top", isTextBox: true });
  });
  rule(s, 8.45, 4.95, 4.28);
  [["2,255×1,565×1,520mm", "카고룸 길이·폭·높이(4,420L)"], ["419mm", "적재고"], ["최대 3.6kW", "실내·실외 220V V2L"]].forEach(([v, l], i) => {
    s.addText(v, { x: 8.45, y: 5.02 + i * 0.4, w: 2.35, h: 0.38, fontSize: i ? 16 : 14, bold: true, color: K.navy, margin: 0, valign: "middle", isTextBox: true });
    s.addText(l, { x: 10.8, y: 5.02 + i * 0.4, w: 1.93, h: 0.38, fontSize: 11, color: K.steel, margin: 0, valign: "middle", isTextBox: true });
  });
  s.addText([{ text: "[실증 필요] ", options: { bold: true, color: K.red } }, { text: "적재중량, 차량총중량, 전후축 하중, 전자파 간섭, 구조변경 승인 검토", options: { color: K.ink } }], { x: 8.45, y: 6.25, w: 4.28, h: 0.55, fontSize: 11, margin: 0, valign: "top", isTextBox: true });
  src(s, "출처: 기아 PV5 카고 제원과 특징, 현대차그룹 「PV5의 모든 것」. 장비 형상과 위치는 제안 예시입니다.");
  s.addNotes("PV5를 센서를 실어 나르는 차가 아니라, 탐사하고 차 안에서 분석하고 내려서 검증하는 이동형 플랫폼으로 정의합니다. 운전석의 12.9인치 PBV 전용 인포테인먼트에서 순찰 앱을 띄웁니다.\n[사실] PV5 카고 롱 카고룸 2,255×1,565×1,520mm(4,420L), 적재고 419mm, 실내·실외 V2L 220V(최대 3.6kW). https://www.kia.com/kr/vehicles/pv5-cargo/specification , https://www.hyundaimotorgroup.com/ko/story/CONT0000000000178473\n[설계 판단] PV5 하부는 배터리 팩이므로 GPR 안테나는 후방 오버행 하부에 다는 것을 기본안으로 하고, 배터리 케이스와 차체 금속의 간섭을 시험합니다.\n[실증 필요] 적재중량, 차량총중량, 전후축 하중, 전자파 간섭, 구조변경 승인.\n사진: Kia PV5 Cargo IMG 7825, Alexander Migl, CC BY-SA 4.0, https://commons.wikimedia.org/wiki/File:Kia_PV5_Cargo_IMG_7825.jpg");

  // ===== 9. #3 4D 변화지도 =====
  s = slideC("실제로 달린 도로만, 위치·깊이·시간으로 기록합니다", "#3 4D 변화지도", K.amber, "운영 모델");
  lead(s, "서울 전체의 완성된 지하지도가 아닙니다. PV5가 측정한 도로를 X·Y 위치, Z 깊이, T 시간으로 쌓은 기록입니다.");
  img(s, "map4d", M, 1.65, 8.0, 4.24, { align: "left", cap: "4D 도로 지하 변화지도 화면 구성(예시, 서울 강동구 명일동 일대)" });
  s.addText("구간마다 남기는 정보", { x: 9.15, y: 1.7, w: 3.58, h: 0.38, fontSize: 16, bold: true, color: K.ink, margin: 0, isTextBox: true });
  s.addText(L(["마지막 조사일과 반복 조사 횟수", "탐사 가능 깊이와 이상 신호 추정 깊이", "이전 회차 대비 변화량", "AI 위험점수, 신뢰도, 위치 오차", "전문가 검토와 정밀조사 결과", "보수 완료 여부"], { bullet: true }), { x: 9.15, y: 2.15, w: 3.58, h: 2.3, fontSize: 14, color: K.steel, margin: 0, paraSpaceAfter: 6, valign: "top", isTextBox: true });
  bubble(s, "지난 조사보다 이상 반사 면적이 17% 늘었습니다", 9.15, 4.65, 3.58, 0.85, { fill: K.amber, color: K.ink, fs: 14 });
  s.addText("[예시] 화면의 수치는 설명용입니다.", { x: 9.15, y: 5.6, w: 3.58, h: 0.32, fontSize: 12, color: K.mute, margin: 0, isTextBox: true });
  s.addText("지도에서 구간을 고르면 실제 위치, 지상 영상, GPR 지하 단면, 회차별 변화 그래프를 한 화면에서 봅니다. 조사하지 않은 구간과 신뢰도가 낮은 구간은 숨기지 않고 따로 표시합니다.", { x: M, y: 6.38, w: CW, h: 0.45, fontSize: 12, color: K.ink, margin: 0, valign: "top", isTextBox: true });
  src(s, "범례: 회색 미조사, 초록 변화 없음, 노랑 새 이상 신호, 주황 확대 의심, 빨강 정밀 재탐사, 점선 신뢰도 낮음");
  s.addNotes("4D 지하 변화지도는 도시 전체를 다 조사했다는 지도가 아닙니다. PV5가 실제로 주행하고 측정한 도로만 위치, 깊이, 시간으로 쌓습니다.\n색 규칙: 회색 미조사, 초록 이전과 변화 없음, 노랑 새 이상 신호, 주황 확대 의심, 빨강 정밀 재탐사, 점선 신뢰도 낮음.\n[예시] 17% 증가, 추정 깊이 0.9~1.3m, AI 신뢰도 84%는 화면 설명용 예시 값입니다.");

  // ===== 10. #4 AI 변화 감지 =====
  s = slideC("AI는 공동을 확정하지 않고, 달라진 곳의 검토 순서를 정합니다", "#4 AI 변화 감지", K.amber, "운영 모델");
  lead(s, "같은 위치의 이전 회차와 현재 회차 GPR 신호를 비교해, 새로 생기거나 커진 신호를 먼저 찾습니다.");
  img(s, "ai_compare", M, 1.7, 8.3, 2.93, { align: "left", cap: "회차 간 GPR 단면 비교(개념)" });
  img(s, "surface_crack", 9.2, 1.7, 3.53, 2.12);
  s.addText("지상 카메라도 함께 봅니다. 균열, 단차, 맨홀 주변 침하, 물 고임 [예시]", { x: 9.2, y: 3.9, w: 3.53, h: 0.7, fontSize: 12, color: K.steel, margin: 0, valign: "top", isTextBox: true });
  rule(s, M, 4.85, CW);
  s.addText("AI 결과에 함께 표시하는 것", { x: M, y: 5.0, w: 6, h: 0.36, fontSize: 15, bold: true, color: K.ink, margin: 0, isTextBox: true });
  s.addText("위험등급, 변화량, 신뢰도, 위치 오차, 권장 후속조치, 전문가 승인 여부", { x: M, y: 5.38, w: 6.3, h: 0.7, fontSize: 15, color: K.steel, margin: 0, valign: "top", isTextBox: true });
  s.addText("비교에 쓰는 데이터", { x: M, y: 6.0, w: 6, h: 0.36, fontSize: 15, bold: true, color: K.ink, margin: 0, isTextBox: true });
  s.addText("GPR 신호와 면적, 추정 깊이 변화, 굴착·재포장 흔적, 강우와 공사 이력, 기존 정밀조사 결과", { x: M, y: 6.36, w: 6.3, h: 0.55, fontSize: 13, color: K.steel, margin: 0, valign: "top", isTextBox: true });
  panel(s, 7.3, 5.0, 5.43, 1.8, "FDECEA");
  ico(s, "alert", 7.55, 5.22, 0.5);
  s.addText(L(["AI는 공동을 확정하지 않습니다", "AI 분석 결과와 전문가 검토 결과를 언제나 따로 표시합니다."]).map((r, i) => ({ text: r.text, options: { ...r.options, fontSize: i ? 14 : 19, bold: !i, color: i ? K.ink : K.red } })), { x: 8.2, y: 5.15, w: 4.35, h: 1.5, margin: 0, valign: "middle", paraSpaceAfter: 4, isTextBox: true });
  src(s, "참고: 3D GPR 딥러닝 공동 탐지 연구. 탐지율과 오탐률은 [실증 필요]");
  s.addNotes("AI의 역할은 결론이 아니라 우선순위입니다. 수많은 GPR 데이터 가운데 이전 회차와 달라진 부분을 먼저 찾아 전문가가 볼 순서를 정합니다.\n결과에는 위험등급, 변화량, 신뢰도, 위치 오차, 권장 후속조치, 전문가 승인 여부를 함께 표시하고, AI 결과와 전문가 판정을 구분합니다.\n참고 연구: https://www.researchgate.net/publication/332081634\n[실증 필요] 실제 탐지율, 오탐률, 미탐률은 천공 확인 결과로 측정합니다.");

  // ===== 11. #5 재확인 포인트 =====
  s = slideC("전문가가 승인한 지점만 다음 순찰의 재확인 업무가 됩니다", "#5 재확인 포인트", K.amber, "운영 모델");
  lead(s, "‘전날과 다음날’이 아니라 ‘이전 탐사 회차와 다음 탐사 회차’를 기준으로 관리합니다.");
  const steps5 = [["AI 후보 등록", "이전 회차 대비 새 신호와 커진 신호"], ["전문가 검토", "AI 결과와 원시 GPR 데이터를 함께 확인"], ["재확인 대기열", "위험도와 변화량 순으로 정렬"], ["다음 순찰 업무", "차량 앱 경로에 재확인 지점 자동 반영"]];
  s.addShape(pres.ShapeType.line, { x: M + 0.21, y: 2.0, w: 9.3, h: 0, line: { color: K.line, width: 2 }, objectName: "track" });
  steps5.forEach(([t, b], i) => {
    const x = M + i * 3.1;
    num(s, i + 1, x, 1.79, 0.42, i === 0 ? K.amber : K.navy, i === 0 ? K.ink : K.white);
    block(s, x, 2.4, 2.85, t, b, { h: 0.75 });
  });
  s.addText("재확인 대기열 [예시]", { x: M, y: 3.75, w: 6, h: 0.38, fontSize: 16, bold: true, color: K.ink, margin: 0, isTextBox: true });
  const H = (t) => ({ text: t, options: { bold: true, color: K.steel, fill: { color: K.fog } } });
  s.addTable([[H("지점"), H("변화"), H("AI 신뢰도"), H("전문가"), H("다음 회차 조치")], ["R-0427", "확대 의심", "높음", "승인", "지면 밀착형 GPR 재탐사"], ["R-0391", "새 이상 신호", "중간", "승인", "다음 순찰 때 재스캔"], ["R-0512", "새 이상 신호", "낮음", "보류", "데이터를 더 모은 뒤 판단"]], { x: M, y: 4.2, w: 8.2, colW: [1.2, 1.5, 1.3, 1.1, 3.1], fontSize: 14, color: K.ink, border: { type: "solid", color: K.line, pt: 0.75 }, rowH: 0.48, valign: "middle", margin: [0, 0.1, 0, 0.1], objectName: "queue" });
  bubble(s, "검토하지 않은 AI 결과는\n순찰 업무로 내려가지 않습니다", 9.25, 4.2, 3.48, 1.0, { fs: 14 });
  s.addText("집중호우 뒤에는 대기열과 별도로 긴급 조사 경로를 만듭니다.", { x: 9.25, y: 5.45, w: 3.48, h: 0.8, fontSize: 14, color: K.steel, margin: 0, valign: "top", isTextBox: true });
  src(s, "대기열 항목과 등급은 설명용 예시입니다.");
  s.addNotes("AI가 찾은 후보는 바로 현장 업무가 되지 않습니다. 전문가가 원시 GPR 데이터와 함께 검토해 승인한 지점만 재확인 대기열에 들어가고, 다음 순찰 경로에 자동으로 반영됩니다.\n[예시] 표의 지점 번호와 등급은 설명용입니다.");

  // ===== 12. #6 Patrol 앱 =====
  s = slideC("PV5의 디스플레이가 새벽 순찰의 업무 화면이 된다", "#6 Patrol 앱", K.amber, "운영 모델");
  lead(s, "PV5는 Android Automotive OS 기반 PBV 전용 인포테인먼트와 Pleos App Market을 지원합니다. GroundWatch Patrol은 이 환경의 B2B 업무용 앱을 목표로 합니다.", { h: 0.6 });
  img(s, "ivi_pre", M, 1.8, 7.3, 2.83, { align: "left" });
  s.addText("운행 전: 순찰거리, 재확인 지점, 장비 상태를 확인하고 순찰을 시작합니다", { x: M, y: 4.72, w: 7.3, h: 0.35, fontSize: 13, color: K.steel, margin: 0, isTextBox: true });
  img(s, "ivi_drive", 8.15, 1.8, 4.58, 1.78);
  s.addText("주행 중: 스캔 상태와 다음 지점 거리만", { x: 8.15, y: 3.6, w: 4.58, h: 0.3, fontSize: 12, color: K.steel, margin: 0, isTextBox: true });
  img(s, "ivi_stop", 8.15, 3.98, 4.58, 1.78);
  s.addText("정차 후: 위험등급, 변화량, 안전 정차, AR 연결", { x: 8.15, y: 5.78, w: 4.58, h: 0.3, fontSize: 12, color: K.steel, margin: 0, isTextBox: true });
  bubble(s, "주행 중에는 분석 화면을 띄우지도, 조작하게 하지도 않습니다", M, 5.35, 7.3, 0.6, { fs: 14 });
  s.addText([{ text: "배포 경로  ", options: { bold: true, color: K.ink } }, { text: "Pleos App Market 또는 기아 PBV 파트너 프로그램", options: { color: K.steel } }], { x: M, y: 6.35, w: 7.3, h: 0.4, fontSize: 13, margin: 0, valign: "top", isTextBox: true });
  s.addText("앱 배포와 차량 데이터 접근은 기아 PBV 파트너 승인과 공식 API 범위 확인이 필요합니다. 사이드로딩과 ADB 활성화는 가정하지 않습니다.", { x: 8.15, y: 6.18, w: 4.58, h: 0.7, fontSize: 12, bold: true, color: K.red, margin: 0, valign: "top", isTextBox: true });
  src(s, "출처: Kia PBV IVI·App Market(AAOS 기반, 개발 목표 고지), 기아 PBV 소프트웨어 솔루션(준비 중인 솔루션, 내용 변경 가능).");
  s.addNotes("PV5는 Android Automotive OS 기반 PBV 전용 인포테인먼트와 Pleos App Market을 지원합니다. GroundWatch Patrol은 이 환경에서 돌아가는 업무용 앱을 목표로 합니다. 완전한 독자 OS라고 표현하지 않습니다.\n활용 후보 데이터: 차량 위치, 주행·주차 상태, 배터리 잔량, 충전 상태, 운행거리, 내비게이션 목적지 전달, 업무 상태.\n기아와 추가 협의가 필요한 데이터: 조향각, 세부 차량 제어, ADAS 원시 데이터, 차량 카메라 원시 영상, 안전 관련 ECU 데이터.\n출처: https://eu-www.kia.com/uk/pbv/solutions/software/ , https://www.kia.com/kr/pbv/solution/software ('준비 중인 솔루션' 고지), PIM 제어기 https://www.hyundaimotorgroup.com/ko/news/CONT0000000000201311 (패신저 도너모델 기준, 카고 적용은 [추가 확인 필요])");

  // ===== 13. #7 SW 브리지 =====
  s = slideC("차량 앱과 엣지 게이트웨이가 AR 글래스에 작업정보를 전달한다", "#7 SW 브리지", K.amber, "운영 모델");
  lead(s, "AR 글래스는 차량 화면의 미러링이 아닙니다. 역할을 나눠 두면 차량 API가 일부 막혀도 GPR과 AR 기능은 멈추지 않습니다.", { h: 0.6 });
  const nodes = [["cloud", "GroundWatch Cloud", "4D 지도, AI, 경로, 권한"], ["monitor", "PV5 Patrol 앱", "업무와 경로 관리"], ["server", "Edge Gateway", "센서 데이터와 로컬 통신"], ["glasses", "AR 글래스", "위치 정합과 수동 탐사 안내"]];
  const links = ["보안 통신", "로컬 API", "차량 내부 보안 Wi-Fi"];
  nodes.forEach(([ic, t, d], i) => {
    const cx = M + 1.4 + i * 3.18;
    s.addShape(pres.ShapeType.ellipse, { x: cx - 0.6, y: 1.85, w: 1.2, h: 1.2, fill: { color: i === 3 ? K.navy : K.fog }, line: { color: i === 3 ? K.navy : K.fog }, objectName: "node" });
    ico(s, i === 3 ? ic + "_w" : ic, cx - 0.33, 2.12, 0.66);
    s.addText(t, { x: cx - 1.45, y: 3.15, w: 2.9, h: 0.38, fontSize: 16, bold: true, color: K.ink, align: "center", margin: 0, isTextBox: true });
    s.addText(d, { x: cx - 1.45, y: 3.53, w: 2.9, h: 0.35, fontSize: 13, color: K.steel, align: "center", margin: 0, isTextBox: true });
    if (i < 3) { s.addShape(pres.ShapeType.line, { x: cx + 0.7, y: 2.45, w: 1.78, h: 0, line: { color: K.navy, width: 1.5, beginArrowType: "triangle", endArrowType: "triangle" }, objectName: "link" }); s.addText(links[i], { x: cx + 0.7, y: 2.05, w: 1.78, h: 0.32, fontSize: 12, bold: true, color: K.navy, align: "center", margin: 0, isTextBox: true }); }
  });
  rule(s, M, 4.2, CW);
  [["글래스로 보내는 정보", "작업 ID, 재확인 좌표, 안전 정차 위치, 탐사 경로, 검색 범위, 추정 깊이, 변화량, AI 신뢰도, 위치 오차, 기준점, 재탐사 방향과 횟수"], ["글래스가 돌려보내는 정보", "기준점 인식 결과, 위치 보정 정확도, 재탐사 시작과 종료, 완료 경로, 음성 메모, 현장 사진, 이상 위치 표시, 추가 조사 요청"], ["통신 원칙", "차량 전용 Wi-Fi 또는 Wi-Fi Direct, MQTT나 WebSocket, TLS 암호화, 기기 인증과 사용자 권한, QR·일회용 코드로 최초 페어링, 오프라인 우선, Bluetooth는 보조"]].forEach(([t, b], i) => block(s, M + i * 4.15, 4.4, 3.85, t, b, { h: 1.9 }));
  src(s, "통신 구조는 제안안입니다. 통신 지연과 끊김 시 동작은 [실증 필요]");
  s.addNotes("구조는 Cloud와 PV5 Patrol 앱 사이는 보안 통신, 앱과 Edge Gateway 사이는 로컬 API, 게이트웨이와 AR 글래스 사이는 차량 내부 보안 Wi-Fi입니다.\n차량 앱은 업무와 경로, 게이트웨이는 센서 데이터와 로컬 통신, AR 글래스는 현장 위치 정합과 수동 탐사 안내를 맡습니다. 이렇게 나누면 차량 API 접근이 일부 막혀도 GPR과 AR 기능 전체가 멈추지 않습니다.\n[실증 필요] 앱, 게이트웨이, 글래스 사이 통신 지연과 네트워크 단절 시 오프라인 동작.");

  // ===== 14. #8 AR 위치 보정 =====
  s = slideC("작업자는 고정된 기준점을 인식해 지하 데이터의 위치를 맞춘다", "#8 AR 위치 보정", K.amber, "운영 모델");
  lead(s, "AR 글래스는 PV5가 안전하게 정차하고 작업자가 내린 뒤에만 켭니다. 운전자는 주행 중 착용하지 않습니다.");
  img(s, "ar_calib", M, 1.7, 8.0, 4.24, { align: "left", cap: "AR 기준점 인식과 위치 보정 화면" });
  ["정차 확인 후 앱에서 현장 정밀점검 시작", "작업 패키지가 Edge Gateway로 전송", "작업자가 글래스 착용, 보안 Wi-Fi 자동 연결", "맨홀 중심 인식", "도로 경계석과 차선 모서리 인식", "RTK 좌표와 시각 기준점 결합", "위치 오차가 기준 이내면 보정 완료"].forEach((t, i) => {
    const y = 1.7 + i * 0.6;
    num(s, i + 1, 8.85, y, 0.36, i >= 3 && i <= 5 ? K.green : K.navy);
    s.addText(t, { x: 9.35, y: y - 0.04, w: 3.4, h: 0.44, fontSize: 13, color: K.ink, margin: 0, valign: "middle", isTextBox: true });
  });
  bubble(s, "맨홀 하나로 확정하지 않고, 기준점 2~3개를 결합합니다", M, 6.1, 7.0, 0.6, { fs: 15 });
  s.addText("기준 후보: 맨홀 중심, 차선 모서리, 경계석, 고정 표지판, 건물 모서리, 현장 기준 마커, RTK-GNSS", { x: 7.85, y: 6.1, w: 4.88, h: 0.72, fontSize: 12, color: K.steel, margin: 0, valign: "middle", isTextBox: true });
  src(s, "위치 오차 기준과 야간 인식 성능은 [실증 필요]. 사진: PattayaPatrol, CC BY-SA 4.0");
  s.addNotes("AR 글래스는 차량이 안전하게 정차한 뒤 차 밖에서 작업자만 씁니다. 차량 안 멀미 보정은 핵심 기능에서 빼고, 글래스가 차 밖에서 독립적으로 위치를 추적합니다.\n위치는 맨홀 하나로 확정하지 않고 맨홀, 차선 모서리, 경계석, RTK 좌표 중 2~3개를 결합해 보정합니다.\n[실증 필요] AR 위치 정확도, 야간 기준점 인식 성능.");

  // ===== 15. #9 AR 재탐사 =====
  s = slideC("AR이 표시한 검색 범위를 따라 양손으로 수동 GPR을 조작한다", "#9 AR 재탐사", K.amber, "운영 모델");
  lead(s, "AR은 공동의 실제 모양이 아니라, AI가 지정한 재탐사 검색 범위를 도로 위에 맞춰 보여줍니다.");
  img(s, "ar_scan", M, 1.7, 8.0, 4.24, { align: "left", cap: "AR 재탐사 범위 안내 화면" });
  s.addText("화면에 보이는 것", { x: 8.85, y: 1.7, w: 3.88, h: 0.38, fontSize: 16, bold: true, color: K.ink, margin: 0, isTextBox: true });
  s.addText(L(["탐사 시작점과 종료점", "진행 방향과 반복 횟수", "추정 깊이와 이전 대비 변화량", "위치 오차와 AI 신뢰도"], { bullet: true }), { x: 8.85, y: 2.12, w: 3.88, h: 1.5, fontSize: 14, color: K.steel, margin: 0, paraSpaceAfter: 5, valign: "top", isTextBox: true });
  ico(s, "mic", 8.85, 3.85, 0.4);
  s.addText("음성으로 실행", { x: 9.35, y: 3.85, w: 3.3, h: 0.4, fontSize: 16, bold: true, color: K.ink, margin: 0, valign: "middle", isTextBox: true });
  s.addText("재탐사 시작, 이상 위치 표시, 사진 촬영, 음성 메모, 재탐사 완료, 추가 조사 요청", { x: 8.85, y: 4.32, w: 3.88, h: 0.95, fontSize: 14, color: K.steel, margin: 0, valign: "top", isTextBox: true });
  bubble(s, "두 손은 장비에, 눈은 도로에", M, 6.1, 3.6, 0.65, { fs: 15 });
  s.addText("화면 아래에는 늘 경고를 띄웁니다. “GPR 기반 추정 위치입니다. 굴착 전 정밀조사와 관계기관 승인이 필요합니다.”", { x: 4.5, y: 6.1, w: 8.23, h: 0.7, fontSize: 13, bold: true, color: K.red, margin: 0, valign: "middle", isTextBox: true });
  src(s, "수치는 설명용 예시입니다. 검색 범위는 공동의 모양이 아니라 재탐사 영역입니다. 사진: PattayaPatrol, CC BY-SA 4.0");
  s.addNotes("작업자는 AR이 도로 위에 그린 검색 범위를 따라 양손으로 수동 GPR을 밉니다. 시작점과 종료점, 진행 방향, 반복 횟수가 보이고, 사진, 메모, 이상 위치 표시는 음성으로 처리합니다.\nAR은 공동의 실제 모양을 보여주지 않습니다. 화면 아래에는 늘 '굴착 전 정밀조사와 관계기관 승인이 필요하다'는 경고를 띄웁니다.");

  // ===== 16. #10 교차검증 =====
  s = slideC("넓게 선별하고, 좁게 다른 방향으로 다시 본다", "#10 교차검증", K.amber, "운영 모델");
  lead(s, "수동 GPR이 차량형보다 늘 더 깊게 보는 것은 아닙니다. 두 장비는 역할이 다릅니다.");
  img(s, "cross_check", M, 1.7, 7.6, 3.42, { align: "left", cap: "차량형 선별과 수동형 교차검증의 탐사 범위(개념)" });
  [["차량형 다채널 GPR", "넓은 도로를 빠르게 선별합니다.", K.amber], ["지면 밀착형 수동 GPR", "좁은 범위를 다른 주파수와 방향으로 교차검증합니다.", K.red], ["내시경", "기존 맨홀이나 승인된 천공부에서 내부를 확인합니다.", K.navy]].forEach(([t, b, c], i) => {
    const y = 1.7 + i * 1.15;
    s.addShape(pres.ShapeType.ellipse, { x: 8.55, y: y + 0.1, w: 0.18, h: 0.18, fill: { color: c }, line: { color: c }, objectName: "dot" });
    block(s, 8.85, y, 3.88, t, b, { h: 0.6 });
  });
  rule(s, M, 5.4, CW);
  [["AR 글래스와 수동 GPR을 함께 씁니다"], ["측정 결과는 Edge Gateway로 바로 보냅니다"], ["차량형 결과와 같은 좌표계로 비교합니다"]].forEach(([t], i) => s.addText(t, { x: M + i * 4.15, y: 5.55, w: 3.9, h: 0.45, fontSize: 15, bold: true, color: K.ink, margin: 0, isTextBox: true }));
  bubble(s, "다른 각도로 한 번 더 본 결과만 정밀조사 요청으로 올라갑니다", M, 6.15, 7.0, 0.62, { fs: 14 });
  src(s, "참고: FHWA GPR 기술 설명(다중·스텝 주파수 안테나). 교차검증 효과는 [실증 필요]");
  s.addNotes("차량형 다채널 GPR은 넓게 선별하고, 지면 밀착형 수동 GPR은 좁은 범위를 다른 주파수와 방향으로 다시 봅니다. 수동 GPR이 늘 더 깊게 본다고 말하지 않습니다.\n참고: https://infotechnology.fhwa.dot.gov/gpr-ground-penetrating-radar-utility-general/");

  // ===== 17. #11 결과 저장 =====
  s = slideC("확인 결과는 지도와 AI로 돌아가 다음 판단을 더 정확하게 만든다", "#11 결과 저장", K.amber, "운영 모델");
  lead(s, "천공과 내시경은 관계기관 승인과 교통통제 뒤에만 합니다. 내시경만으로 차량이 공동을 바로 확정하지 않습니다.");
  const pf = ["수동 GPR 재확인", "공동 가능성 상향", "정밀조사 요청", "도로관리기관 승인", "교통통제와 천공", "내시경 확인", "복구 또는\n지속 관찰"];
  s.addShape(pres.ShapeType.line, { x: M + 0.18, y: 1.98, w: 10.9, h: 0, line: { color: K.line, width: 2 }, objectName: "track" });
  pf.forEach((t, i) => {
    const x = M + i * 1.75;
    num(s, i + 1, x, 1.8, 0.36, i < 2 ? K.amber : i < 4 ? K.navy : i < 6 ? K.steel : K.green, i < 2 ? K.ink : K.white);
    s.addText(t, { x, y: 2.28, w: 1.65, h: 0.6, fontSize: 14, bold: true, color: K.ink, margin: 0, valign: "top", isTextBox: true });
  });
  img(s, "ph_patched", M, 3.2, 4.4, 2.64, { stretch: true });
  s.addText("공동을 메우고 다시 포장한 자리(해외 사례)", { x: M, y: 5.88, w: 4.4, h: 0.28, fontSize: 11, color: K.steel, margin: 0, isTextBox: true });
  panel(s, 5.3, 3.2, 7.43, 2.64, K.night);
  s.addText("결과 저장과 학습 순환", { x: 5.6, y: 3.4, w: 6.9, h: 0.42, fontSize: 18, bold: true, color: K.amber, margin: 0, isTextBox: true });
  s.addText(L(["확인 결과와 보수 이력을 4D 지도의 해당 구간에 저장합니다", "AI 후보와 실제 확인 결과를 짝지어 검증 데이터로 쌓습니다", "오탐과 미탐 사례로 AI 성능을 점검하고 고칩니다", "보수 후 같은 구간을 다시 순찰해 재검증합니다"], { bullet: true }), { x: 5.6, y: 3.92, w: 6.9, h: 1.8, fontSize: 15, color: K.white, margin: 0, paraSpaceAfter: 6, valign: "top", isTextBox: true });
  arrowLine(s, 9.0, 5.95, 9.0, 6.4, K.amber, 2);
  s.addShape(pres.ShapeType.line, { x: 2.8, y: 6.4, w: 6.2, h: 0, line: { color: K.amber, width: 2 }, objectName: "loop" });
  arrowLine(s, 2.8, 6.4, 2.8, 5.95, K.amber, 2);
  s.addText("다음 순찰로 돌아갑니다", { x: 3.6, y: 6.45, w: 4.6, h: 0.36, fontSize: 14, bold: true, color: K.navy, align: "center", margin: 0, isTextBox: true });
  src(s, "일반적인 공동 확인 흐름을 바탕으로 한 제안안입니다. 실제 승인 절차는 관할 기관 기준을 따릅니다. 사진: Famartin, CC BY-SA 4.0");
  s.addNotes("수동 GPR 재확인으로 공동 가능성이 높아지면 관제센터가 정밀조사를 요청하고, 도로관리기관 승인과 교통통제 뒤 천공과 내시경으로 최종 확인합니다. 결과는 복구 또는 지속 관찰로 이어지고, 다시 4D 지도에 저장돼 AI 검증 데이터가 됩니다.\n승인 절차는 관할 기관 기준을 따릅니다.");

  // ===== 18. 구분장 =====
  pres.addSection({ title: "확장" });
  s = pres.addSlide({ masterName: "GW_FULL", sectionTitle: "확장" });
  s.background = { color: K.white };
  s.addShape(pres.ShapeType.rect, { x: 7.4, y: 0, w: 5.933, h: 7.5, fill: { color: K.night }, line: { color: K.night }, objectName: "panel" });
  img(s, "f_rear", 7.4, 1.2, 5.933, 5.1);
  s.addText("Ⅲ", { x: M, y: 1.2, w: 3, h: 1.0, fontFace: HF, fontSize: 54, bold: true, color: K.navy, margin: 0, isTextBox: true });
  s.addText("도시 지하 안전망으로의 확장", { x: M, y: 2.25, w: 6.4, h: 0.6, fontFace: HF, fontSize: 26, bold: true, color: K.ink, margin: 0, isTextBox: true });
  s.addShape(pres.ShapeType.line, { x: M, y: 3.05, w: 6.2, h: 0, line: { color: "C9D0DA", width: 0.75 }, objectName: "rule" });
  s.addText(["3.1  위험도별 순찰망", "3.2  여러 대의 PV5 플릿", "3.3  도시 지하 데이터 통합", "3.4  4D 도시 지하 디지털 트윈"].map((t, i, a) => ({ text: t, options: { breakLine: i < a.length - 1 } })), { x: M, y: 3.25, w: 6.4, h: 3.4, fontSize: 12.5, color: K.steel, margin: 0, valign: "top", paraSpaceAfter: 4, isTextBox: true });
  s.addNotes("여기부터는 운영 모델이 검증된 뒤의 확장 방향입니다.");

  // ===== 19. 확장1 =====
  s = slideC("위험한 곳은 더 자주, 비가 온 뒤에는 바로", "확장 1 순찰망", K.red, "확장");
  lead(s, "구간 위험도에 따라 조사 주기를 다르게 잡습니다. 아래 주기는 [예시]이며 발주기관과 협의해 정합니다.");
  img(s, "patrol_net", M, 1.7, 7.4, 4.16, { align: "left", cap: "위험도별 순찰 경로 예시(서울 강동구 명일동 일대)" });
  [["집중관리 구간", "매일 또는 주 1회", K.red], ["노후 하수관, 공사장 주변", "주 1회", "F08C00"], ["역세권 일반도로", "월 1회", "4E8FD9"], ["일반 관리구간", "분기 또는 반기", K.green], ["집중호우 이후", "긴급 조사", "7048E8"], ["AI가 변화를 감지한 구간", "다음 회차에 우선 재확인", K.amber]].forEach(([k, v, c], i) => {
    const y = 1.72 + i * 0.68;
    s.addShape(pres.ShapeType.rect, { x: 8.3, y: y + 0.12, w: 0.36, h: 0.1, fill: { color: c }, line: { color: c }, objectName: "swatch" });
    s.addText(k, { x: 8.8, y, w: 2.3, h: 0.34, fontSize: 14, bold: true, color: K.ink, margin: 0, isTextBox: true });
    s.addText(v, { x: 8.8, y: y + 0.3, w: 3.9, h: 0.32, fontSize: 13, color: K.steel, margin: 0, isTextBox: true });
  });
  bubble(s, "지하철역 주변, 노후 하수관, 굴착공사 주변, 반복 침하 구간부터 시작합니다", M, 6.1, 7.4, 0.68, { fs: 14 });
  s.addText("지도는 가상 도시 예시입니다. 서울시도 명일동 사고 이후 굴착공사장 점검을 연 1회에서 월·주 단위로 늘렸습니다.", { x: 8.3, y: 5.95, w: 4.43, h: 0.85, fontSize: 12, color: K.steel, margin: 0, valign: "top", isTextBox: true });
  src(s, "출처: 서울시 지반침하 예방체계 강화 보도자료(굴착공사장 점검 주기 강화). 조사 주기 표는 제안 예시입니다.");
  s.addNotes("위험도가 높은 구간일수록 순찰 주기를 짧게 잡습니다. 표의 주기는 예시이며 발주기관과 합의해 정합니다. 서울시도 명일동 사고 이후 굴착공사장 점검을 연 1회에서 월·주 단위로 강화했습니다.\n출처: https://www.seoul.go.kr/news/news_report.do?nttNo=454742");

  // ===== 20. 확장2 =====
  s = slideC("여러 대의 PV5가 권역을 나눠 같은 기준으로 순찰한다", "확장 2 플릿", K.red, "확장");
  lead(s, "권역을 나누고, 관제센터에서 실시간 상태를 보며, 차량별 순찰거리와 재확인 업무를 배정합니다.");
  img(s, "fleet", M, 1.7, 7.4, 4.07, { align: "left", cap: "권역 분담 플릿 관제 화면(예시)" });
  block(s, 8.3, 1.75, 4.43, "같은 사양, 같은 기준", "차량과 장비 배치가 같아야 권역이 달라도 회차 데이터를 같은 기준으로 비교할 수 있습니다.", { h: 0.9 });
  block(s, 8.3, 3.05, 4.43, "관제 연동 [추가 확인 필요]", "Pleos Fleet 차량관제 또는 기관 FMS와 배터리, 위치, 업무 상태를 잇는 방안을 검토합니다.", { h: 0.9 });
  block(s, 8.3, 4.35, 4.43, "배정 기준", "권역 위험도, 재확인 대기열, 차량 배터리, 인력 교대", { h: 0.7 });
  bubble(s, "한 대의 시제품이 아니라, 복제할 수 있는 순찰 체계", M, 6.05, 6.2, 0.68, { fs: 15 });
  src(s, "출처: 기아 PV5 카고 특징(Pleos Fleet 차량관제솔루션). 관제 화면 수치는 예시입니다.");
  s.addNotes("여러 대의 PV5가 권역을 나눠 운영하면 관제센터가 차량별 순찰거리, 재확인 업무, 배터리 상태를 한 화면에서 봅니다. 같은 사양의 차량이어야 권역이 달라도 데이터를 같은 기준으로 비교할 수 있습니다.\n[추가 확인 필요] Pleos Fleet 또는 기관 FMS와의 연동 범위. 출처: https://www.kia.com/kr/vehicles/pv5-cargo/features");

  // ===== 21. 확장3 =====
  s = slideC("GPR 변화 신호를 도시의 다른 지하 데이터와 겹쳐 본다", "확장 3 데이터 통합", K.red, "확장");
  lead(s, "하수관, 굴착공사, 지하철 구조물, 지하수, 강우, 보수 이력과 함께 볼 때 원인을 짐작하기 쉬워집니다.");
  img(s, "layers", M, 1.7, 7.4, 4.07, { align: "left", cap: "지하 안전 데이터 레이어 구성" });
  ico(s, "shield", 8.3, 1.75, 0.45);
  block(s, 8.9, 1.75, 3.83, "보안과 접근권한", "지하정보는 보안과 안전 문제가 있어 기관별 접근권한을 나누고, 계약기관이 쓰는 접근제어형 관제 서비스로 제공합니다.", { h: 1.2 });
  ico(s, "db", 8.3, 3.35, 0.45);
  block(s, 8.9, 3.35, 3.83, "데이터 표준", "지하공간 데이터 표준(OGC MUDDI 등)을 참고해 기관 간 연계 형식을 설계합니다.", { h: 0.9 });
  ico(s, "alert", 8.3, 4.65, 0.45);
  block(s, 8.9, 4.65, 3.83, "지하 데이터는 팔지 않습니다", "제3자 판매가 아니라 공공 안전 관제 목적입니다.", { h: 0.6 });
  bubble(s, "한 기관의 데이터만으로는 원인을 보기 어렵습니다", M, 6.05, 6.2, 0.68, { fs: 15 });
  src(s, "참고: OGC MUDDI(ogc.org/standards/muddi), 국토부 지하공간통합지도와 지하안전정보시스템(JIS) 연계 방향(2025.5.27 보도자료)");
  s.addNotes("GPR 변화 신호만으로는 원인을 알기 어렵습니다. 하수관, 굴착공사, 지하철 구조물, 지하수, 강우, 보수 이력과 겹쳐 볼 때 원인을 짐작하기 쉬워집니다. 국토부도 지하공간통합지도에 지하안전 정보를 연계하는 방향을 밝혔습니다.\n지하정보는 보안 문제가 있어 팔지 않고 계약기관 대상 접근제어형 서비스로 제공합니다.\n참고: https://www.ogc.org/standards/muddi/");

  // ===== 22. 확장4 =====
  s = slideC("시간이 쌓이면, 도로 아래가 변하는 모습이 보인다", "확장 4 디지털 트윈", K.red, "확장");
  lead(s, "지상 지도, 지하 시설물, 공동 의심 신호, 시간에 따른 변화를 하나의 모델에서 봅니다.");
  img(s, "twin", M, 1.7, 7.4, 3.92, { align: "left", cap: "4D 도시 지하 디지털 트윈 개념" });
  [["공사 전후 비교", "굴착공사 착공 전, 공사 중, 완료 후 같은 구간을 비교합니다."], ["재난 대응", "집중호우나 지진 뒤 우선 점검 구간을 고릅니다."], ["유지관리 계획", "변화가 잦은 구간의 관로 교체 우선순위 근거가 됩니다."], ["범위 원칙", "PV5가 측정한 도로에 한정하고, 측정하지 않은 구간은 비워 둡니다."]].forEach(([t, b], i) => block(s, 8.3, 1.75 + i * 1.03, 4.43, t, b, { h: 0.6, tfs: 16, fs: 13 }));
  bubble(s, "도시가 같은 길을 기억하면, 작은 변화도 놓치지 않을 수 있습니다", M, 5.95, 7.4, 0.7, { fs: 15 });
  src(s, "디지털 트윈은 운영 데이터가 충분히 쌓인 뒤의 장기 확장 방향입니다.");
  s.addNotes("반복 순찰 데이터가 쌓이면 지상 지도, 지하 시설물, 공동 의심 신호, 시간에 따른 변화를 하나의 모델에서 볼 수 있습니다. 공사 전후 비교, 재난 대응, 유지관리 계획에 쓸 수 있습니다. 다만 측정한 도로에 한정하고, 측정하지 않은 구간은 비워 둡니다.");

  // ===== 23. 마무리 =====
  s = pres.addSlide({ masterName: "GW_FULL", sectionTitle: "확장" });
  s.background = { color: K.white };
  s.addShape(pres.ShapeType.rect, { x: 6.9, y: 0, w: 6.433, h: 7.5, fill: { color: K.night }, line: { color: K.night }, objectName: "panel" });
  img(s, "f_front2", 6.9, 1.2, 6.433, 5.1);
  s.addText("맺음말", { x: M, y: 0.7, w: 6, h: 0.3, fontSize: 11, color: K.steel, margin: 0, isTextBox: true });
  s.addText("한 번의 조기 발견이,\n한 사람의 무사 귀가가 되도록.", { x: M, y: 1.25, w: 6.1, h: 1.3, fontFace: HF, fontSize: 26, bold: true, color: K.navy, margin: 0, valign: "top", isTextBox: true });
  s.addShape(pres.ShapeType.line, { x: M, y: 2.85, w: 5.9, h: 0, line: { color: "C9D0DA", width: 0.75 }, objectName: "rule" });
  s.addText([
    { text: "□ 단발성 점검을 반복 관측으로", options: { bold: true, color: K.ink, breakLine: true } },
    { text: "같은 도로를 같은 장비로 다시 보고, 회차 간 변화를 기록합니다.", options: { color: K.steel, breakLine: true } },
    { text: "□ AI는 순서를, 전문가는 판정을", options: { bold: true, color: K.ink, breakLine: true } },
    { text: "AI가 달라진 곳을 먼저 찾고, 확정은 전문가와 천공·내시경이 맡습니다.", options: { color: K.steel, breakLine: true } },
    { text: "□ PV5를 이동형 탐사·분석·검증 플랫폼으로", options: { bold: true, color: K.ink, breakLine: true } },
    { text: "새벽 저소음 운행, V2L 전원, 카고룸 장비 고정, 차량 앱 연동을 활용합니다.", options: { color: K.steel } },
  ], { x: M, y: 3.05, w: 6.0, h: 2.6, fontSize: 13, margin: 0, valign: "top", paraSpaceAfter: 5, isTextBox: true });
  s.addText([{ text: "PV5 GroundWatch", options: { bold: true, color: K.navy } }, { text: "", options: { color: K.steel } }], { x: M, y: 6.05, w: 6, h: 0.32, fontSize: 12, margin: 0, isTextBox: true });
  s.addText("감사합니다", { x: M, y: 6.45, w: 3, h: 0.3, fontSize: 12, color: K.steel, margin: 0, isTextBox: true });
  s.addNotes("도로가 무너진 뒤에는 누구나 구멍을 볼 수 있습니다. 우리가 찾으려는 것은 아직 보이지 않을 때 시작된 변화입니다. 한 번의 조기 발견이 한 사람의 무사 귀가가 되도록, PV5 GroundWatch를 제안합니다. 감사합니다.\n이미지: PV5 실차 사진(Alexander Migl, CC BY-SA 4.0, https://commons.wikimedia.org/wiki/File:Kia_PV5_Cargo_IMG_7829.jpg).");

  // ===== 24. 부록1 =====
  pres.addSection({ title: "부록" });
  s = slideC("GPR은 만능이 아니다. 깊이, 토질, 금속의 한계를 먼저 밝힌다", "부록 1 GPR 한계", K.navy, "부록");
  img(s, "freq_depth", M, 1.15, 6.3, 3.15, { align: "left", cap: "안테나 주파수와 탐지 깊이·해상도의 관계(개념)" });
  [["탐사 깊이", "서울시가 쓰는 고주파 GPR은 약 2m 안팎입니다. GroundWatch도 2m 안팎의 얕은 공동을 주로 봅니다."], ["주파수와 해상도", "저주파는 깊지만 흐릿하고, 고주파는 얕지만 정밀합니다(FHWA)."], ["수분과 점토", "수분과 점토가 많은 흙은 전자파를 약하게 만듭니다(FHWA)."], ["금속 간섭", "금속 관로는 강하게 반사하고 그 아래를 가립니다(FHWA)."], ["깊은 지반과 터널", "지하철 터널 같은 깊은 구조는 대상이 아닙니다. 복합탐사 같은 다른 기법의 영역입니다."]].forEach(([t, b], i) => {
    const y = 1.1 + i * 0.64;
    s.addText(t, { x: 7.2, y, w: 1.65, h: 0.58, fontSize: 14, bold: true, color: K.ink, margin: 0, valign: "top", isTextBox: true });
    s.addText(b, { x: 8.9, y, w: 3.83, h: 0.6, fontSize: 12, color: K.steel, margin: 0, valign: "top", isTextBox: true });
  });
  rule(s, M, 4.5, CW);
  s.addText("AI가 공동을 최종 확정하지 않는 이유", { x: M, y: 4.65, w: CW, h: 0.42, fontSize: 18, bold: true, color: K.red, margin: 0, isTextBox: true });
  [["신호가 비슷합니다", "관로, 매설물, 토질 변화가 공동과 비슷하게 보일 수 있어 원시 데이터 해석에 전문가 판단이 필요합니다."], ["검증 데이터가 아직 없습니다", "실제 천공으로 확인한 결과가 충분히 쌓여야 합니다. 초기 오탐률과 미탐률은 아직 검증 전입니다."], ["책임 주체가 필요합니다", "굴착과 교통통제 같은 행정 조치에는 책임 있는 판단 주체가 있어야 합니다."]].forEach(([t, b], i) => block(s, M + i * 4.15, 5.15, 3.9, t, b, { h: 1.0, tfs: 15, fs: 13 }));
  src(s, "출처: FHWA GPR 기술 설명, 서울시 설명 인용 보도(고주파 GPR 약 2m), 서울시 복합탐사(지하 5~40m) 시범 도입 보도(2025.12.30)");
  s.addNotes("GPR의 한계를 먼저 밝힙니다.\n- FHWA: 저주파는 깊고 해상도가 낮으며, 고주파는 얕고 정밀합니다. 400MHz 안테나는 최대 약 12ft. 수분과 점토가 많은 흙은 전자파를 감쇠시킵니다. 금속은 거의 모든 에너지를 반사하고 그 아래를 가립니다. https://infotechnology.fhwa.dot.gov/gpr-ground-penetrating-radar-utility-general/\n- 서울시: 고주파 GPR 탐지 깊이 약 2m, 2026년부터 지하 5~40m 복합탐사를 굴착공사장 2곳에 시범 도입. https://v.daum.net/v/20251230143011653\nGroundWatch는 지하철 구조 안전 검사가 아니라 역세권 도로와 공사 영향구간의 얕은 공동 감시입니다.\nAI는 검토 순서를, 전문가는 판정을, 천공과 내시경은 확인을 맡습니다.");

  // ===== 25. 부록2 =====
  s = slideC("새벽 도로 작업은 사람이 먼저 안전해야 한다", "부록 2 안전과 운영", K.navy, "부록");
  panel(s, M, 1.1, 4.3, 5.7, K.night);
  ico(s, "users_w", M + 0.3, 1.35, 0.55);
  s.addText("초기 운영은 2인 1조", { x: M + 1.0, y: 1.35, w: 3.2, h: 0.55, fontSize: 20, bold: true, color: K.white, margin: 0, valign: "middle", isTextBox: true });
  [["운전과 안전", "운전, 주변 교통 확인, 안전통제, 정차 위치 확보"], ["장비와 판독", "GPR 운용, AR 글래스, 수동 GPR, 현장 판독"]].forEach(([t, b], i) => block(s, M + 0.3, 2.3 + i * 1.45, 3.7, `${i + 1}명  ${t}`, b, { tc: K.amber, bc: "DCE3EC", h: 0.8, fs: 14 }));
  s.addText("안전성과 자동화 수준이 검증된 뒤 일부 구간의 1인 운용 가능성을 검토합니다.", { x: M + 0.3, y: 5.4, w: 3.7, h: 1.1, fontSize: 13, color: "9AA8BC", margin: 0, valign: "top", isTextBox: true });
  [["안전 정차", "앱이 안전 정차 위치를 안내하고, 주차 상태를 확인한 뒤에만 작업 모드를 켭니다."], ["주행 중 AR 금지", "AR 글래스는 정차 후 차 밖 작업자만 쓰고, 운전자는 착용하지 않습니다."], ["교통통제", "정차 재탐사 때 라바콘, 표지판, 경광장치, 반사조끼를 씁니다."], ["천공과 내시경", "도로관리기관 승인과 교통통제 뒤에만 진행합니다."], ["AR 위치 오차", "오차가 기준을 넘으면 검색 범위를 표시하지 않습니다. [실증 필요]"], ["개인정보", "지상 영상의 얼굴과 차량번호는 비식별화한 뒤 저장하고 공유합니다."]].forEach(([t, b], i) => {
    const x = 5.3 + (i % 2) * 3.8, y = 1.1 + Math.floor(i / 2) * 1.95;
    rule(s, x, y, 3.5, K.ink);
    block(s, x, y + 0.15, 3.5, t, b, { h: 1.1 });
  });
  src(s, "운영 원칙은 제안안입니다. 실제 운영 전 산업안전보건, 도로교통, 개인정보보호 관련 법령 검토가 필요합니다.");
  s.addNotes("새벽 도로에서 한 사람이 운전, 장비, 교통 확인, 수동 탐사를 모두 할 수 없습니다. 초기에는 2인 1조로 운영합니다. 주행 중 AR 사용 금지, 정차 확인 후 작업 모드, 천공과 내시경은 승인과 교통통제 뒤, 영상은 비식별화가 원칙입니다.");

  // ===== 26. 부록3 =====
  s = slideC("탐사 용역에서 시작해 연간 관제 계약과 패키지로 넓힌다", "부록 3 사업 모델", K.navy, "부록");
  [["1단계", "탐사 용역", ["주행 거리 기반 과금", "위험지역 집중 탐사", "공사 전후 비교 탐사", "집중호우 후 긴급 탐사", "정밀 재탐사"]], ["2단계", "연간 관제 계약", ["정기 순찰과 4D 변화지도", "AI 변화 감지와 GIS 대시보드", "정기 보고서와 우선순위", "이력 관리와 보수 후 재검증", "공공기관 연간 구독"]], ["3단계", "차량·소프트웨어 패키지", ["PV5 GroundWatch 컨버전 차량", "GPR·카메라 센서 패키지", "Patrol 앱, Edge Gateway, AR", "AI 분석 SW와 관제 대시보드", "유지보수와 교육"]]].forEach(([st, t, items], i) => {
    const x = M + i * 4.15;
    s.addText(st, { x, y: 1.1, w: 3.85, h: 0.32, fontSize: 13, bold: true, color: K.steel, margin: 0, isTextBox: true });
    s.addText(t, { x, y: 1.42, w: 3.85, h: 0.5, fontSize: 22, bold: true, color: K.navy, margin: 0, isTextBox: true });
    rule(s, x, 2.0, 3.85, K.ink);
    s.addText(L(items, { bullet: true }), { x, y: 2.15, w: 3.85, h: 2.4, fontSize: 15, color: K.ink, margin: 0, paraSpaceAfter: 7, valign: "top", isTextBox: true });
    if (i < 2) arrowLine(s, x + 3.88, 1.67, x + 4.1, 1.67, K.mute);
  });
  rule(s, M, 4.85, CW);
  s.addText("주요 고객", { x: M, y: 5.0, w: 3, h: 0.36, fontSize: 15, bold: true, color: K.ink, margin: 0, isTextBox: true });
  s.addText("서울시와 자치구 도로관리 부서, 서울교통공사와 철도 운영기관, 상하수도 관리기관, 지하안전 조사기업, 도심 굴착공사 건설사", { x: M, y: 5.38, w: CW, h: 0.6, fontSize: 15, color: K.steel, margin: 0, valign: "top", isTextBox: true });
  s.addText([{ text: "[가설] ", options: { bold: true, color: K.red } }, { text: "가격과 단가는 원가와 발주기관의 지불 의사를 확인한 뒤 설계합니다. 지하정보는 팔지 않고 접근제어형 서비스로만 제공합니다.", options: { color: K.ink } }], { x: M, y: 6.1, w: CW, h: 0.6, fontSize: 14, margin: 0, valign: "top", isTextBox: true });
  src(s, "B2G 중심, B2B 확장. 단가와 계약 형태는 실증 단계에서 확정합니다.");
  s.addNotes("1단계는 주행 거리 기반 탐사 용역, 2단계는 정기 순찰, 4D 지도, AI 변화 감지를 묶은 연간 관제 계약, 3단계는 PV5 컨버전 차량과 소프트웨어 패키지 공급입니다. 지하정보는 제3자에게 팔지 않고 계약기관이 쓰는 접근제어형 서비스로 제공합니다. 가격은 아직 정하지 않았습니다.");

  // ===== 27. 부록4 =====
  s = slideC("확인된 사실과 검증할 가설을 나눠 관리한다", "부록 4 근거와 검증", K.navy, "부록");
  s.addText("확정 데이터와 출처", { x: M, y: 1.1, w: 5.9, h: 0.38, fontSize: 16, bold: true, color: K.ink, margin: 0, isTextBox: true });
  const H2 = (t) => ({ text: t, options: { bold: true, color: K.steel, fill: { color: K.fog } } });
  s.addTable([[H2("항목"), H2("출처")], ["명일동 사고 규모와 원인", "국토부 조사결과(2025.12.3)"], ["연희동 5월 탐사 미발견", "서울시 설명(뉴시스 2024.8.30)"], ["서울시 탐사 실적과 계획", "서울시 보도자료, 경향신문"], ["고주파 GPR 약 2m", "서울시 설명 인용 보도"], ["PV5 제원과 V2L 3.6kW", "기아, 현대차그룹"], ["AAOS IVI와 App Market", "Kia PBV(개발 목표 고지)"], ["GPR 원리와 한계", "FHWA"]], { x: M, y: 1.55, w: 5.9, colW: [2.7, 3.2], fontSize: 13, color: K.ink, border: { type: "solid", color: K.line, pt: 0.75 }, rowH: 0.42, valign: "middle", margin: [0, 0.1, 0, 0.1], objectName: "facts" });
  s.addText("실증이 필요한 항목", { x: 6.9, y: 1.1, w: 5.83, h: 0.38, fontSize: 16, bold: true, color: K.red, margin: 0, isTextBox: true });
  s.addText(L(["GPR와 전기차 전자파 간섭, 배터리팩 영향", "장비 소비전력과 V2L 운용, 주행거리 영향", "적재중량, 차량총중량, 축하중, 구조변경", "AR 위치 정확도와 야간 기준점 인식", "차량 앱 배포 경로와 공식 API 범위", "앱, 게이트웨이, 글래스 통신 지연과 단절 대응", "AI 탐지율, 오탐률, 미탐률(천공 확인 기준)", "발주기관 지불 의사와 현재 방식의 공백"], { bullet: true }), { x: 6.9, y: 1.55, w: 5.83, h: 3.4, fontSize: 14, color: K.ink, margin: 0, paraSpaceAfter: 5, valign: "top", isTextBox: true });
  rule(s, M, 5.15, CW);
  [["[가설]", "사업과 운영상 가정, 인터뷰와 파일럿으로 검증"], ["[실증 필요]", "차량과 장비 시험으로 확인"], ["[추가 확인 필요]", "공식 자료 확인 전"], ["[예시]", "화면과 수치 설명용"]].forEach(([k, v], i) => {
    s.addText(k, { x: M + i * 3.1, y: 5.3, w: 2.9, h: 0.36, fontSize: 14, bold: true, color: K.navy, margin: 0, isTextBox: true });
    s.addText(v, { x: M + i * 3.1, y: 5.66, w: 2.9, h: 0.55, fontSize: 13, color: K.steel, margin: 0, valign: "top", isTextBox: true });
  });
  s.addText(BASIS + ". 링크 전체는 발표자 노트에 있습니다.", { x: M, y: 6.4, w: CW, h: 0.38, fontSize: 13, bold: true, color: K.ink, margin: 0, isTextBox: true });
  src(s, "공식 자료를 우선하고, 언론 보도는 공식 발표를 인용한 경우만 썼습니다. 값이 다르면 공식 수치를 채택했습니다(서울시 2026 탐사 16,423km).");
  s.addNotes(["출처 전체 목록(" + BASIS + ")",
    "1. 국토교통부 땅꺼짐 사고 조사결과 발표(2025.12.3) https://m.korea.kr/briefing/policyBriefingView.do?newsId=156732996",
    "2. 국토교통부 명일동 사고조사 최종보고서 https://www.molit.go.kr/USR/policyData/m_34681/dtl.jsp?id=4872",
    "3. 서울시 지반침하 예방체계 강화 https://www.seoul.go.kr/news/news_report.do?nttNo=454742",
    "4. 서울시 연희동 사고 이후 개선안 https://mediahub.seoul.go.kr/archives/2012160",
    "5. 서울시 차량탑재형 GPR 도입 https://news.seoul.go.kr/safe/archives/41339",
    "6. 서울 안전누리 GPR 탐사지도 https://safecity.seoul.go.kr/distFclt/cfMapDs/cfMapDs.page?menuId=MENU_SSNS_000176",
    "7. 뉴시스 2024.8.30 연희동 https://www.newsis.com/view/NISX20240830_0002869815",
    "8. 경향신문 2025.10.19 서울시 GPR https://www.khan.co.kr/article/202510191122011",
    "9. 세이프타임즈 GPR 2m https://www.safetimes.co.kr/news/articleView.html?idxno=231486",
    "10. 서울시 복합탐사 보도 https://v.daum.net/v/20251230143011653",
    "11. 국토부 굴착공사장 안전관리 강화방안(2025.5.27) https://www.codil.or.kr/filebank/files/202505/helpdesk/BBS_202505290920333590.pdf",
    "12. 기아 PV5 카고 특징 https://www.kia.com/kr/vehicles/pv5-cargo/features",
    "13. 기아 PV5 카고 제원 https://www.kia.com/kr/vehicles/pv5-cargo/specification",
    "14. 현대차그룹 PV5의 모든 것 https://www.hyundaimotorgroup.com/ko/story/CONT0000000000178473",
    "15. 기아 PBV 소프트웨어 https://www.kia.com/kr/pbv/solution/software",
    "16. Kia PBV IVI와 AAOS App Market https://eu-www.kia.com/uk/pbv/solutions/software/",
    "17. Hyundai Pleos Connect https://connected-mobility.hyundai.com/what-we-do/pleos",
    "18. 현대차그룹 PIM 제어기 https://www.hyundaimotorgroup.com/ko/news/CONT0000000000201311",
    "19. FHWA GPR https://infotechnology.fhwa.dot.gov/gpr-ground-penetrating-radar-utility-general/",
    "20. OGC MUDDI https://www.ogc.org/standards/muddi/"].join("\n"));

  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("wrote", OUT);
}
build().catch((e) => { console.error(e); process.exit(1); });
