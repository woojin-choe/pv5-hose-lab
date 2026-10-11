// PV5 GroundWatch 장비 배치도(측면·후면 기술 도면). 치수는 기아 공식 제원(카고 롱) 기준, 세부 형상은 실차 사진 참고 근사.
const sharp = require("sharp");
const path = require("path");
const OUT = path.join(__dirname, "..", "images");
const F = "Noto Sans CJK KR, sans-serif";
const INK = "#1F2A37", MID = "#6B7686", LT = "#C5CCD6", FILL = "#F3F5F8", GLS = "#DCE3EC", BLK = "#4A525E", ACC = "#C8102E", NAVY = "#0B1F3A";
const t = (x, y, s, txt, o = {}) => `<text x="${x}" y="${y}" font-family="${F}" font-size="${s}" font-weight="${o.w || 400}" fill="${o.c || INK}" text-anchor="${o.a || "start"}">${txt}</text>`;

function side() {
  const S = 0.31, OX = 150, GY = 700;               // mm → px, 지면 y
  const X = (mm) => OX + mm * S, Y = (mm) => GY - mm * S;
  const p = (pts) => pts.map(([a, b]) => `${X(a).toFixed(1)},${Y(b).toFixed(1)}`).join(" ");
  let g = "";
  // 지면
  g += `<line x1="${X(-400)}" y1="${GY}" x2="${X(5100)}" y2="${GY}" stroke="${MID}" stroke-width="1.2"/>`;
  for (let m = -400; m < 5100; m += 120) g += `<line x1="${X(m)}" y1="${GY}" x2="${X(m - 60)}" y2="${GY + 10}" stroke="${LT}" stroke-width="1"/>`;
  // 차체 외곽
  const body = [[0, 360], [0, 1820], [40, 1890], [120, 1905], [3300, 1905], [3420, 1880], [3520, 1830], [4250, 1190], [4560, 1080], [4660, 1020], [4695, 940], [4695, 380], [4650, 300], [4400, 270], [4190, 270], [4190, 300], [3500, 300], [3500, 270], [1200, 270], [1200, 300], [500, 300], [500, 270], [140, 270], [40, 300]];
  g += `<polygon points="${p(body)}" fill="${FILL}" stroke="${INK}" stroke-width="2"/>`;
  // 하단 클래딩·휠아치(각진 형태)
  const arch = (cx) => [[cx - 520, 270], [cx - 520, 560], [cx - 430, 700], [cx + 430, 700], [cx + 520, 560], [cx + 520, 270]];
  g += `<polygon points="${p([[0, 360], [0, 560], [330, 560], ...arch(850).slice(0), [1370, 560], [3325, 560], ...arch(3845), [4365, 560], [4695, 560], [4695, 380], [4650, 300], [4400, 270], [140, 270], [40, 300]])}" fill="${BLK}" opacity=".88"/>`;
  for (const cx of [850, 3845]) g += `<polygon points="${p(arch(cx))}" fill="#2A3038"/>`;
  // 바퀴
  for (const cx of [850, 3845]) {
    g += `<circle cx="${X(cx)}" cy="${Y(343)}" r="${343 * S}" fill="#20252C"/><circle cx="${X(cx)}" cy="${Y(343)}" r="${215 * S}" fill="#8B95A3"/><circle cx="${X(cx)}" cy="${Y(343)}" r="${215 * S}" fill="none" stroke="#2A3038" stroke-width="1.5"/>`;
    for (let k = 0; k < 5; k++) { const a = (k * 72 - 90) * Math.PI / 180; g += `<line x1="${X(cx)}" y1="${Y(343)}" x2="${X(cx) + Math.cos(a) * 200 * S}" y2="${Y(343) + Math.sin(a) * 200 * S}" stroke="#3A424D" stroke-width="3"/>`; }
    g += `<circle cx="${X(cx)}" cy="${Y(343)}" r="${45 * S}" fill="#2A3038"/>`;
  }
  // 글라스 밴드(윈드실드 측면 + 1열 창)·검은 루프 끝
  g += `<polygon points="${p([[3060, 1180], [3060, 1800], [3380, 1830], [3500, 1800], [4230, 1200]])}" fill="${GLS}" stroke="${INK}" stroke-width="1.5"/>`;
  g += `<polygon points="${p([[3060, 1800], [3300, 1905], [3420, 1880], [3520, 1830], [3500, 1800], [3380, 1830]])}" fill="${BLK}"/>`;
  g += `<line x1="${X(3330)}" y1="${Y(1815)}" x2="${X(3330)}" y2="${Y(1190)}" stroke="${INK}" stroke-width="2.5"/>`;
  // 도어 라인·손잡이·캐릭터 라인
  for (const dx of [2000, 3040]) g += `<line x1="${X(dx)}" y1="${Y(1840)}" x2="${X(dx)}" y2="${Y(560)}" stroke="${MID}" stroke-width="1.2"/>`;
  g += `<rect x="${X(2780)}" y="${Y(1120)}" width="${150 * S}" height="${30 * S}" rx="3" fill="${MID}"/><rect x="${X(1820)}" y="${Y(1120)}" width="${150 * S}" height="${30 * S}" rx="3" fill="${MID}"/>`;
  g += `<polyline points="${p([[60, 1180], [2600, 1180], [2800, 1080], [3060, 1080]])}" fill="none" stroke="${LT}" stroke-width="1.2"/>`;
  // 램프: 후면 세로 리어램프, 전면 ㄱ자 라이트 바
  g += `<rect x="${X(0) - 3}" y="${Y(1700)}" width="6" height="${800 * S}" rx="3" fill="${ACC}"/>`;
  g += `<polyline points="${p([[4250, 1190], [4560, 1080], [4660, 1020]])}" fill="none" stroke="#E7EBF0" stroke-width="5" stroke-linecap="round"/><polyline points="${p([[4250, 1190], [4560, 1080], [4660, 1020]])}" fill="none" stroke="${INK}" stroke-width="1" />`;
  // 미러
  g += `<polygon points="${p([[3420, 1300], [3560, 1300], [3560, 1120], [3440, 1120]])}" fill="${BLK}"/>`;
  // 카고룸(점선) 2,255mm
  g += `<rect x="${X(160)}" y="${Y(1800)}" width="${2255 * S}" height="${1520 * S}" fill="none" stroke="${NAVY}" stroke-width="1.4" stroke-dasharray="7 5"/>`;
  // ---- 장비 ----
  const E = "#E8A317";
  const eq = [];
  // 1 전방 카메라 포드
  g += `<rect x="${X(3150)}" y="${Y(1975)}" width="${200 * S}" height="${70 * S}" rx="4" fill="${NAVY}"/>`; eq.push([1, X(3250), Y(1975)]);
  // 2 경광등
  g += `<rect x="${X(2150)}" y="${Y(1990)}" width="${600 * S}" height="${50 * S}" rx="6" fill="${E}"/><rect x="${X(2130)}" y="${Y(1945)}" width="${640 * S}" height="${40 * S}" fill="${NAVY}"/>`; eq.push([2, X(2450), Y(1990)]);
  // 3 RTK-GNSS
  g += `<rect x="${X(560)}" y="${Y(1960)}" width="${30 * S}" height="${55 * S}" fill="${NAVY}"/><path d="M ${X(470)} ${Y(1960)} Q ${X(575)} ${Y(2090)} ${X(680)} ${Y(1960)} Z" fill="#E7EBF0" stroke="${NAVY}" stroke-width="1.5"/>`; eq.push([3, X(575), Y(2070)]);
  // 4 측면 카메라(미러)
  g += `<rect x="${X(3480)}" y="${Y(1350)}" width="${90 * S}" height="${50 * S}" rx="3" fill="${NAVY}"/>`; eq.push([4, X(3525), Y(1350)]);
  // 5 화물실 Edge Gateway 랙
  g += `<rect x="${X(1900)}" y="${Y(1500)}" width="${450 * S}" height="${1150 * S}" fill="#E6ECF5" stroke="${NAVY}" stroke-width="1.5"/>`;
  for (let k = 0; k < 5; k++) g += `<rect x="${X(1935)}" y="${Y(1450 - k * 200)}" width="${380 * S}" height="${130 * S}" rx="2" fill="${k ? "#B9C4D3" : NAVY}"/>`;
  eq.push([5, X(2125), Y(1500)]);
  // 6 수동 GPR·AR 보관
  g += `<rect x="${X(1050)}" y="${Y(1030)}" width="${650 * S}" height="${430 * S}" fill="#E6ECF5" stroke="${NAVY}" stroke-width="1.5"/><rect x="${X(1090)}" y="${Y(970)}" width="${300 * S}" height="${140 * S}" rx="3" fill="${E}"/><rect x="${X(1450)}" y="${Y(970)}" width="${200 * S}" height="${140 * S}" rx="3" fill="${NAVY}"/>`;
  eq.push([6, X(1375), Y(1030)]);
  // 7 후방 장비함(내시경·콘)
  g += `<rect x="${X(220)}" y="${Y(1030)}" width="${700 * S}" height="${430 * S}" fill="#E6ECF5" stroke="${NAVY}" stroke-width="1.5"/>`;
  for (let k = 0; k < 3; k++) g += `<polygon points="${p([[300 + k * 150, 650], [365 + k * 150, 970], [430 + k * 150, 650]])}" fill="#E8590C"/>`;
  eq.push([7, X(570), Y(1030)]);
  // 8 후방 하부 다채널 GPR 어레이
  g += `<rect x="${X(80)}" y="${Y(270)}" width="${40 * S}" height="${110 * S}" fill="${NAVY}"/><rect x="${X(420)}" y="${Y(270)}" width="${40 * S}" height="${110 * S}" fill="${NAVY}"/>`;
  g += `<rect x="${X(-60)}" y="${Y(160)}" width="${620 * S}" height="${70 * S}" rx="4" fill="${NAVY}"/><rect x="${X(-60)}" y="${Y(160)}" width="${620 * S}" height="${14 * S}" fill="${E}"/>`;
  for (let k = 1; k <= 3; k++) g += `<path d="M ${X(-60 - k * 80)} ${GY + 4 + k * 9} Q ${X(250)} ${GY + 12 + k * 22} ${X(560 + k * 80)} ${GY + 4 + k * 9}" fill="none" stroke="${E}" stroke-width="1.6" opacity="${1 - k * 0.25}"/>`;
  eq.push([8, X(250), Y(90)]);
  // 9 휠 인코더
  g += `<circle cx="${X(850)}" cy="${Y(343)}" r="${70 * S}" fill="${E}" stroke="${NAVY}" stroke-width="1.5"/>`; eq.push([9, X(850), Y(343)]);
  // 번호 지시선
  const lab = { 1: [1080, 70], 2: [880, 70], 3: [300, 70], 4: [1300, 300], 5: [820, 200], 6: [600, 395], 7: [235, 395], 8: [175, 790], 9: [470, 790] };
  for (const [n, px, py] of eq) {
    const [lx, ly] = lab[n];
    g += `<line x1="${px}" y1="${py}" x2="${lx}" y2="${ly}" stroke="${INK}" stroke-width="0.9"/><circle cx="${px}" cy="${py}" r="3" fill="${INK}"/>`;
    g += `<circle cx="${lx}" cy="${ly}" r="13" fill="#fff" stroke="${INK}" stroke-width="1.3"/>` + t(lx, ly + 5, 14, n, { a: "middle", w: 700 });
  }
  // 치수선
  const dimH = (x1, x2, y, label) => `<line x1="${x1}" y1="${y}" x2="${x2}" y2="${y}" stroke="${MID}" stroke-width="1"/><line x1="${x1}" y1="${y - 7}" x2="${x1}" y2="${y + 7}" stroke="${MID}"/><line x1="${x2}" y1="${y - 7}" x2="${x2}" y2="${y + 7}" stroke="${MID}"/><rect x="${(x1 + x2) / 2 - label.length * 4.6}" y="${y - 10}" width="${label.length * 9.2}" height="20" fill="#fff"/>` + t((x1 + x2) / 2, y + 5, 13, label, { a: "middle", c: MID });
  g += dimH(X(0), X(4695), GY + 72, "전장 4,695") + dimH(X(850), X(3845), GY + 44, "휠베이스 2,995") ;
  g += t(X(1287), Y(1800) + 24, 13, "카고룸 길이 2,255(점선)", { a: "middle", c: NAVY });
  const xv = X(4695) + 70;
  g += `<line x1="${xv}" y1="${GY}" x2="${xv}" y2="${Y(1905)}" stroke="${MID}"/><line x1="${xv - 7}" y1="${GY}" x2="${xv + 7}" y2="${GY}" stroke="${MID}"/><line x1="${xv - 7}" y1="${Y(1905)}" x2="${xv + 7}" y2="${Y(1905)}" stroke="${MID}"/><line x1="${X(4400)}" y1="${Y(1905)}" x2="${xv}" y2="${Y(1905)}" stroke="${LT}" stroke-dasharray="4 4"/>`;
  g += `<text x="${xv + 18}" y="${(GY + Y(1905)) / 2}" font-family="${F}" font-size="13" fill="${MID}" text-anchor="middle" transform="rotate(-90 ${xv + 18} ${(GY + Y(1905)) / 2})">전고 1,905</text>`;
  g += t(X(-380), 40, 15, "측면도", { w: 700 }) + t(X(-380), 820, 12, "단위 mm. 차량 치수는 기아 공식 제원(PV5 카고 롱), 차체 형상은 실차 사진 기준 근사, 장비 형상·위치는 제안 예시", { c: MID });
  return { W: 1800, H: 840, g };
}

function rear() {
  const S = 0.29, OX = 120, GY = 640;
  const X = (mm) => OX + (mm + 948) * S, Y = (mm) => GY - mm * S;     // 중심 0
  const p = (pts) => pts.map(([a, b]) => `${X(a).toFixed(1)},${Y(b).toFixed(1)}`).join(" ");
  let g = `<line x1="${X(-1300)}" y1="${GY}" x2="${X(1300)}" y2="${GY}" stroke="${MID}" stroke-width="1.2"/>`;
  for (const cx of [-760, 760]) g += `<rect x="${X(cx - 110)}" y="${Y(690)}" width="${220 * S}" height="${690 * S}" rx="10" fill="#20252C"/>`;
  g += `<polygon points="${p([[-948, 330], [-948, 1780], [-890, 1880], [-780, 1905], [780, 1905], [890, 1880], [948, 1780], [948, 330]])}" fill="${FILL}" stroke="${INK}" stroke-width="2"/>`;
  g += `<polygon points="${p([[-948, 330], [948, 330], [948, 560], [-948, 560]])}" fill="${BLK}" opacity=".88"/>`;
  g += `<line x1="${X(0)}" y1="${Y(1840)}" x2="${X(0)}" y2="${Y(560)}" stroke="${MID}" stroke-width="1.3"/>`;
  g += `<rect x="${X(-700)}" y="${Y(1250)}" width="${560 * S}" height="${260 * S}" rx="8" fill="none" stroke="${LT}" stroke-width="1.2"/>`;
  for (const lx of [-930, 905]) g += `<rect x="${X(lx)}" y="${Y(1700)}" width="${25 * S + 2}" height="${850 * S}" rx="3" fill="${ACC}"/>`;
  const E = "#E8A317";
  g += `<rect x="${X(-300)}" y="${Y(1990)}" width="${600 * S}" height="${50 * S}" rx="6" fill="${E}"/><rect x="${X(-320)}" y="${Y(1945)}" width="${640 * S}" height="${40 * S}" fill="${NAVY}"/>`;
  g += `<rect x="${X(560)}" y="${Y(1960)}" width="${30 * S}" height="${55 * S}" fill="${NAVY}"/><path d="M ${X(470)} ${Y(1960)} Q ${X(575)} ${Y(2090)} ${X(680)} ${Y(1960)} Z" fill="#E7EBF0" stroke="${NAVY}" stroke-width="1.5"/>`;
  g += `<rect x="${X(-700)}" y="${Y(1950)}" width="${180 * S}" height="${60 * S}" rx="4" fill="${NAVY}"/>`;
  g += `<rect x="${X(-160)}" y="${Y(900)}" width="${320 * S}" height="${70 * S}" rx="3" fill="#FFF3C4" stroke="${E}" stroke-width="1.5"/>` + t(X(0), Y(900) + 15, 11, "저속 탐사 차량", { a: "middle", c: "#6B4E00", w: 700 });
  for (const bx of [-700, 0, 660]) g += `<rect x="${X(bx)}" y="${Y(330)}" width="${40 * S}" height="${170 * S}" fill="${NAVY}"/>`;
  g += `<rect x="${X(-900)}" y="${Y(160)}" width="${1800 * S}" height="${70 * S}" rx="4" fill="${NAVY}"/><rect x="${X(-900)}" y="${Y(160)}" width="${1800 * S}" height="${14 * S}" fill="${E}"/>`;
  for (let k = 0; k < 16; k++) g += `<rect x="${X(-870 + k * 110)}" y="${Y(130)}" width="${80 * S}" height="${40 * S}" fill="#3A4A66"/>`;
  // 스캔 폭
  g += `<polygon points="${X(-900)},${GY} ${X(900)},${GY} ${X(1050)},${GY + 60} ${X(-1050)},${GY + 60}" fill="${E}" opacity=".18"/><line x1="${X(-1050)}" y1="${GY + 60}" x2="${X(1050)}" y2="${GY + 60}" stroke="${E}" stroke-width="1.5"/>`;
  g += t(X(0), GY + 90, 13, "GPR 다채널 스캔 폭(차로 방향 연속 탐사)", { a: "middle", c: "#8A5A00" });
  const yv = GY + 130;
  g += `<line x1="${X(-948)}" y1="${yv}" x2="${X(948)}" y2="${yv}" stroke="${MID}"/><line x1="${X(-948)}" y1="${yv - 7}" x2="${X(-948)}" y2="${yv + 7}" stroke="${MID}"/><line x1="${X(948)}" y1="${yv - 7}" x2="${X(948)}" y2="${yv + 7}" stroke="${MID}"/><rect x="${X(0) - 50}" y="${yv - 10}" width="100" height="20" fill="#fff"/>` + t(X(0), yv + 5, 13, "전폭 1,895", { a: "middle", c: MID });
  g += t(X(-1300), 40, 15, "후면도", { w: 700 });
  return { W: 820, H: 820, g };
}

(async () => {
  for (const [name, d] of [["draw_side", side()], ["draw_rear", rear()]]) {
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${d.W}" height="${d.H}" viewBox="0 0 ${d.W} ${d.H}"><rect width="${d.W}" height="${d.H}" fill="#fff"/>${d.g}</svg>`;
    await sharp(Buffer.from(svg), { density: 216 }).png().toFile(path.join(OUT, name + ".png"));
  }
  console.log("drawings done");
})();
