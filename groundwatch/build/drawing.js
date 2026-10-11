// PV5 GroundWatch 장비 배치도: 공학 도면(선화) 스타일. 차량 치수 = 기아 공식 제원(PV5 카고 롱), 형상은 실차 사진 기준 근사.
const sharp = require("sharp");
const path = require("path");
const OUT = path.join(__dirname, "..", "images");
const F = "Noto Sans CJK KR, sans-serif";
const K = "#1B1F24", G = "#7A828C", L = "#B8BEC6", P = "#9AA3AE", ACC = "#C9861A", BLUE = "#2C5A8C";
const T = (x, y, s, t, o = {}) => `<text x="${x}" y="${y}" font-family="${F}" font-size="${s}" font-weight="${o.w || 400}" fill="${o.c || K}" text-anchor="${o.a || "start"}">${t}</text>`;
const DEFS = `<defs>
  <pattern id="hatch" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="7" stroke="#B8C2CE" stroke-width="1"/></pattern>
  <pattern id="hatch2" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(-45)"><line x1="0" y1="0" x2="0" y2="5" stroke="#C9CED6" stroke-width="0.8"/></pattern>
</defs>`;

function side() {
  const S = 0.3, OX = 120, GY = 640;
  const X = (m) => OX + m * S, Y = (m) => GY - m * S;
  const pts = (a) => a.map(([x, y]) => `${X(x).toFixed(1)},${Y(y).toFixed(1)}`).join(" ");
  const line = (a, o = {}) => `<polyline points="${pts(a)}" fill="${o.fill || "none"}" stroke="${o.c || K}" stroke-width="${o.w || 1}" ${o.dash ? `stroke-dasharray="${o.dash}"` : ""} stroke-linejoin="round" stroke-linecap="round"/>`;
  let g = "";
  // 지면
  g += `<line x1="${X(-450)}" y1="${GY}" x2="${X(5150)}" y2="${GY}" stroke="${K}" stroke-width="1.2"/>`;
  // 차체 외곽(실루엣)
  const body = [[30, 330], [0, 420], [0, 1800], [40, 1880], [140, 1905], [3260, 1905], [3380, 1890], [3470, 1840], [4230, 1205], [4520, 1110], [4640, 1060], [4690, 980], [4695, 420], [4660, 330], [4380, 300],
    [4370, 300], [4360, 560], [4300, 690], [3390, 690], [3330, 560], [3320, 300], [1375, 300], [1365, 560], [1305, 690], [395, 690], [335, 560], [325, 300], [30, 330]];
  g += `<polygon points="${pts(body)}" fill="#FFFFFF" stroke="${K}" stroke-width="2.2" stroke-linejoin="round"/>`;
  // 하단 클래딩 경계
  g += line([[0, 560], [335, 560]], { w: 1.2 }) + line([[1365, 560], [3330, 560]], { w: 1.2 }) + line([[4360, 560], [4695, 560]], { w: 1.2 });
  g += `<polygon points="${pts([[1365, 560], [3330, 560], [3320, 300], [1375, 300]])}" fill="url(#hatch2)"/><polygon points="${pts([[0, 560], [335, 560], [325, 300], [30, 330], [0, 420]])}" fill="url(#hatch2)"/><polygon points="${pts([[4360, 560], [4695, 560], [4695, 420], [4660, 330], [4380, 300], [4370, 300]])}" fill="url(#hatch2)"/>`;
  // 글라스(1열 창 + 윈드실드 측면) 해칭
  const glass = [[3060, 1190], [3060, 1790], [3380, 1820], [3460, 1790], [4200, 1215]];
  g += `<polygon points="${pts(glass)}" fill="url(#hatch)" stroke="${K}" stroke-width="1.3"/>`;
  g += line([[3330, 1810], [3330, 1195]], { w: 2.2 });
  // 루프 끝 블랙 패널 경계
  g += line([[3060, 1790], [3060, 1905]], { w: 1 });
  // 도어 분할선, 손잡이, 캐릭터 라인
  g += line([[2010, 1860], [2010, 560]], { w: 1 }) + line([[3040, 1860], [3040, 560]], { w: 1 });
  g += `<rect x="${X(1840)}" y="${Y(1130)}" width="${140 * S}" height="${28 * S}" rx="2" fill="none" stroke="${K}"/><rect x="${X(2830)}" y="${Y(1130)}" width="${140 * S}" height="${28 * S}" rx="2" fill="none" stroke="${K}"/>`;
  g += line([[60, 1190], [2700, 1190], [2860, 1100], [3060, 1100]], { c: L });
  // 램프
  g += `<rect x="${X(0) - 3}" y="${Y(1700)}" width="6" height="${820 * S}" rx="3" fill="none" stroke="${K}" stroke-width="1.2"/>`;
  g += line([[4230, 1205], [4520, 1110], [4640, 1060]], { w: 3.2 });
  // 미러
  g += `<polygon points="${pts([[3430, 1310], [3560, 1310], [3560, 1130], [3450, 1130]])}" fill="#fff" stroke="${K}" stroke-width="1.3"/>`;
  // 바퀴
  for (const cx of [850, 3845]) {
    const cx_ = X(cx), cy = Y(343);
    g += `<circle cx="${cx_}" cy="${cy}" r="${343 * S}" fill="#F1F2F4" stroke="${K}" stroke-width="2"/><circle cx="${cx_}" cy="${cy}" r="${300 * S}" fill="none" stroke="${L}"/>`;
    g += `<circle cx="${cx_}" cy="${cy}" r="${215 * S}" fill="#fff" stroke="${K}" stroke-width="1.3"/>`;
    for (let k = 0; k < 5; k++) { const a = (k * 72 - 90) * Math.PI / 180, b = a + 0.32; g += `<polygon points="${cx_ + Math.cos(a) * 55 * S},${cy + Math.sin(a) * 55 * S} ${cx_ + Math.cos(a) * 205 * S},${cy + Math.sin(a) * 205 * S} ${cx_ + Math.cos(b) * 205 * S},${cy + Math.sin(b) * 205 * S}" fill="none" stroke="${K}" stroke-width="1"/>`; }
    g += `<circle cx="${cx_}" cy="${cy}" r="${45 * S}" fill="#fff" stroke="${K}"/>`;
  }
  // ---- 내부(팬텀선) ----
  g += `<rect x="${X(160)}" y="${Y(1820)}" width="${2255 * S}" height="${(1820 - 419) * S}" fill="none" stroke="${P}" stroke-width="1" stroke-dasharray="8 5"/>`;
  g += line([[160, 419], [2415, 419]], { c: P, dash: "8 5" });
  // 5 Edge Gateway 랙(격벽 쪽)
  const rx = 2120, rw = 280;
  g += `<rect x="${X(rx)}" y="${Y(1560)}" width="${rw * S}" height="${(1560 - 419) * S}" fill="#F4F6F9" stroke="${BLUE}" stroke-width="1.3"/>`;
  for (let k = 0; k < 7; k++) g += `<line x1="${X(rx)}" y1="${Y(1480 - k * 150)}" x2="${X(rx + rw)}" y2="${Y(1480 - k * 150)}" stroke="${BLUE}" stroke-width=".8"/><circle cx="${X(rx + rw - 40)}" cy="${Y(1520 - k * 150)}" r="2" fill="${BLUE}"/>`;
  // 6 수동 GPR 카트(바퀴·핸들 실루엣)
  const cx0 = 1450;
  g += `<rect x="${X(cx0)}" y="${Y(560)}" width="${520 * S}" height="${100 * S}" rx="4" fill="#F4F6F9" stroke="${BLUE}" stroke-width="1.3"/>`;
  g += `<circle cx="${X(cx0 + 70)}" cy="${Y(470)}" r="${50 * S}" fill="#fff" stroke="${BLUE}" stroke-width="1.3"/><circle cx="${X(cx0 + 450)}" cy="${Y(470)}" r="${50 * S}" fill="#fff" stroke="${BLUE}" stroke-width="1.3"/>`;
  g += line([[cx0 + 480, 560], [cx0 + 620, 1050]], { c: BLUE, w: 2 }) + `<rect x="${X(cx0 + 560)}" y="${Y(1130)}" width="${160 * S}" height="${100 * S}" rx="3" fill="#F4F6F9" stroke="${BLUE}" stroke-width="1.3"/>`;
  // AR 글래스 케이스(선반)
  g += `<rect x="${X(1450)}" y="${Y(1500)}" width="${520 * S}" height="${200 * S}" rx="4" fill="#F4F6F9" stroke="${BLUE}" stroke-width="1.3"/>` + line([[1450, 1290], [1970, 1290]], { c: BLUE });
  // 7 후방 장비 수납장(휠하우스 위)
  g += `<rect x="${X(200)}" y="${Y(1300)}" width="${1050 * S}" height="${(1300 - 760) * S}" fill="#F4F6F9" stroke="${BLUE}" stroke-width="1.3"/>` + line([[725, 1300], [725, 760]], { c: BLUE }) + line([[200, 1030], [1250, 1030]], { c: BLUE });
  // ---- 외부 장비 ----
  // 1 전방 카메라 포드
  g += `<rect x="${X(3150)}" y="${Y(1975)}" width="${190 * S}" height="${70 * S}" rx="6" fill="#fff" stroke="${K}" stroke-width="1.5"/><circle cx="${X(3245)}" cy="${Y(1940)}" r="${18 * S}" fill="none" stroke="${K}"/>`;
  // 2 경광등
  g += `<rect x="${X(2130)}" y="${Y(1945)}" width="${640 * S}" height="${40 * S}" fill="#fff" stroke="${K}" stroke-width="1.5"/><rect x="${X(2160)}" y="${Y(1995)}" width="${580 * S}" height="${50 * S}" rx="8" fill="#F6E3BE" stroke="${ACC}" stroke-width="1.5"/>`;
  // 3 RTK-GNSS
  g += `<rect x="${X(560)}" y="${Y(1960)}" width="${30 * S}" height="${55 * S}" fill="#fff" stroke="${K}"/><path d="M ${X(470)} ${Y(1960)} Q ${X(575)} ${Y(2090)} ${X(680)} ${Y(1960)} Z" fill="#fff" stroke="${K}" stroke-width="1.5"/>`;
  // 4 측면 카메라
  g += `<rect x="${X(3480)}" y="${Y(1360)}" width="${90 * S}" height="${50 * S}" rx="3" fill="#fff" stroke="${K}" stroke-width="1.3"/>`;
  // 8 후방 하부 GPR 어레이
  for (const bx of [80, 520]) g += `<rect x="${X(bx)}" y="${Y(300)}" width="${30 * S}" height="${140 * S}" fill="#fff" stroke="${K}"/>`;
  g += `<rect x="${X(-40)}" y="${Y(160)}" width="${640 * S}" height="${80 * S}" rx="5" fill="#F4F6F9" stroke="${K}" stroke-width="1.5"/>`;
  for (let k = 0; k < 8; k++) g += `<line x1="${X(0 + k * 75)}" y1="${Y(150)}" x2="${X(0 + k * 75)}" y2="${Y(90)}" stroke="${L}"/>`;
  // 9 휠 인코더
  g += `<circle cx="${X(850)}" cy="${Y(343)}" r="${75 * S}" fill="#fff" stroke="${K}" stroke-width="1.5"/><circle cx="${X(850)}" cy="${Y(343)}" r="${30 * S}" fill="none" stroke="${K}"/>`;
  // 지시선·번호
  const call = [[1, 3245, 1975, 1080, 40], [2, 2450, 1995, 830, 40], [3, 575, 2060, 300, 40], [4, 3525, 1360, 1300, 300], [5, 2260, 1560, 820, 120], [6, 1700, 560, 620, 520], [7, 700, 1300, 260, 150], [8, 280, 120, 175, 735], [9, 850, 343, 420, 735]];
  for (const [n, mx, my, lx, ly] of call) {
    g += `<line x1="${X(mx)}" y1="${Y(my)}" x2="${lx}" y2="${ly}" stroke="${K}" stroke-width=".8"/><circle cx="${X(mx)}" cy="${Y(my)}" r="2.5" fill="${K}"/>`;
    g += `<circle cx="${lx}" cy="${ly}" r="12" fill="#fff" stroke="${K}" stroke-width="1.2"/>` + T(lx, ly + 4.5, 13, n, { a: "middle", w: 700 });
  }
  // 치수
  const dim = (x1, x2, y, label) => { const m = (x1 + x2) / 2; return `<line x1="${x1}" y1="${y}" x2="${x2}" y2="${y}" stroke="${G}"/><path d="M ${x1} ${y} l 9 -3.5 l 0 7 Z M ${x2} ${y} l -9 -3.5 l 0 7 Z" fill="${G}"/><line x1="${x1}" y1="${y - 10}" x2="${x1}" y2="${y + 10}" stroke="${G}" stroke-width=".8"/><line x1="${x2}" y1="${y - 10}" x2="${x2}" y2="${y + 10}" stroke="${G}" stroke-width=".8"/><rect x="${m - label.length * 4.4}" y="${y - 10}" width="${label.length * 8.8}" height="20" fill="#fff"/>` + T(m, y + 4.5, 12.5, label, { a: "middle", c: G }); };
  g += dim(X(850), X(3845), GY + 45, "휠베이스 2,995") + dim(X(0), X(4695), GY + 78, "전장 4,695") + dim(X(160), X(2415), Y(1820) - 18, "카고룸 2,255");
  const xv = X(4695) + 60;
  g += `<line x1="${xv}" y1="${GY}" x2="${xv}" y2="${Y(1905)}" stroke="${G}"/><path d="M ${xv} ${GY} l -3.5 -9 l 7 0 Z M ${xv} ${Y(1905)} l -3.5 9 l 7 0 Z" fill="${G}"/><line x1="${X(4300)}" y1="${Y(1905)}" x2="${xv + 10}" y2="${Y(1905)}" stroke="${L}" stroke-dasharray="3 4"/>`;
  g += `<text x="${xv + 16}" y="${(GY + Y(1905)) / 2}" font-family="${F}" font-size="12.5" fill="${G}" text-anchor="middle" transform="rotate(-90 ${xv + 16} ${(GY + Y(1905)) / 2})">전고 1,905</text>`;
  // 범례
  g += `<line x1="${X(3300)}" y1="${GY + 125}" x2="${X(3420)}" y2="${GY + 125}" stroke="${P}" stroke-dasharray="8 5"/>` + T(X(3440), GY + 129, 12, "카고룸 내부(팬텀선)", { c: G });
  g += `<rect x="${X(3980)}" y="${GY + 118}" width="16" height="14" fill="#F4F6F9" stroke="${BLUE}"/>` + T(X(3980) + 24, GY + 129, 12, "탑재 장비", { c: G });
  g += T(X(-400), GY + 129, 12, "단위 mm  |  차량 치수: 기아 공식 제원(PV5 카고 롱)  |  장비 형상·위치: 제안 예시", { c: G });
  return { W: 1720, H: 790, g };
}

function rear() {
  const S = 0.3, CX = 420, GY = 690;
  const X = (m) => CX + m * S, Y = (m) => GY - m * S;
  const pts = (a) => a.map(([x, y]) => `${X(x).toFixed(1)},${Y(y).toFixed(1)}`).join(" ");
  let g = `<line x1="${X(-1300)}" y1="${GY}" x2="${X(1300)}" y2="${GY}" stroke="${K}" stroke-width="1.2"/>`;
  for (const cx of [-770, 770]) g += `<rect x="${X(cx - 110)}" y="${Y(690)}" width="${220 * S}" height="${690 * S}" rx="12" fill="#F1F2F4" stroke="${K}" stroke-width="1.6"/>`;
  g += `<polygon points="${pts([[-940, 330], [-948, 1760], [-900, 1870], [-790, 1905], [790, 1905], [900, 1870], [948, 1760], [940, 330]])}" fill="#fff" stroke="${K}" stroke-width="2.2" stroke-linejoin="round"/>`;
  g += `<polygon points="${pts([[-940, 330], [940, 330], [945, 560], [-945, 560]])}" fill="url(#hatch2)" stroke="${K}" stroke-width="1.2"/>`;
  g += `<line x1="${X(0)}" y1="${Y(1850)}" x2="${X(0)}" y2="${Y(560)}" stroke="${K}"/>`;
  g += `<rect x="${X(-720)}" y="${Y(1260)}" width="${560 * S}" height="${250 * S}" rx="10" fill="none" stroke="${L}" stroke-width="1.2"/>`;
  for (const lx of [-930, 905]) g += `<rect x="${X(lx)}" y="${Y(1700)}" width="${25 * S + 2}" height="${850 * S}" rx="3" fill="none" stroke="${K}" stroke-width="1.2"/>`;
  g += `<rect x="${X(-320)}" y="${Y(1945)}" width="${640 * S}" height="${40 * S}" fill="#fff" stroke="${K}" stroke-width="1.5"/><rect x="${X(-290)}" y="${Y(1995)}" width="${580 * S}" height="${50 * S}" rx="8" fill="#F6E3BE" stroke="${ACC}" stroke-width="1.5"/>`;
  g += `<rect x="${X(560)}" y="${Y(1960)}" width="${30 * S}" height="${55 * S}" fill="#fff" stroke="${K}"/><path d="M ${X(470)} ${Y(1960)} Q ${X(575)} ${Y(2090)} ${X(680)} ${Y(1960)} Z" fill="#fff" stroke="${K}" stroke-width="1.5"/>`;
  g += `<rect x="${X(-700)}" y="${Y(1950)}" width="${180 * S}" height="${60 * S}" rx="5" fill="#fff" stroke="${K}" stroke-width="1.3"/>`;
  for (const bx of [-700, -15, 670]) g += `<rect x="${X(bx)}" y="${Y(330)}" width="${30 * S}" height="${170 * S}" fill="#fff" stroke="${K}"/>`;
  g += `<rect x="${X(-900)}" y="${Y(160)}" width="${1800 * S}" height="${80 * S}" rx="5" fill="#F4F6F9" stroke="${K}" stroke-width="1.5"/>`;
  for (let k = 1; k < 16; k++) g += `<line x1="${X(-900 + k * 112.5)}" y1="${Y(150)}" x2="${X(-900 + k * 112.5)}" y2="${Y(90)}" stroke="${L}"/>`;
  // 스캔 폭(지면 아래 점선 영역)
  g += `<rect x="${X(-900)}" y="${GY}" width="${1800 * S}" height="34" fill="url(#hatch)" stroke="${P}" stroke-dasharray="6 4"/>` + T(X(0), GY + 56, 12.5, "다채널 GPR 탐사 폭 약 1.8m(16채널, 제안 예시)", { a: "middle", c: G });
  const yv = GY + 92, x1 = X(-948), x2 = X(948);
  g += `<line x1="${x1}" y1="${yv}" x2="${x2}" y2="${yv}" stroke="${G}"/><path d="M ${x1} ${yv} l 9 -3.5 l 0 7 Z M ${x2} ${yv} l -9 -3.5 l 0 7 Z" fill="${G}"/><rect x="${X(0) - 44}" y="${yv - 10}" width="88" height="20" fill="#fff"/>` + T(X(0), yv + 4.5, 12.5, "전폭 1,895", { a: "middle", c: G });
  return { W: 840, H: 820, g };
}

(async () => {
  for (const [name, d] of [["draw_side", side()], ["draw_rear", rear()]]) {
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${d.W}" height="${d.H}" viewBox="0 0 ${d.W} ${d.H}">${DEFS}<rect width="${d.W}" height="${d.H}" fill="#fff"/>${d.g}</svg>`;
    await sharp(Buffer.from(svg), { density: 216 }).png().toFile(path.join(OUT, name + ".png"));
  }
  console.log("drawings done");
})();
