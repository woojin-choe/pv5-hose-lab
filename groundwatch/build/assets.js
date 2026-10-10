// GroundWatch 일러스트 에셋 생성기 (v2: 야간 렌더 스타일)
// 실제 사진·로고 없이 SVG로 그려 images/*.png로 저장한다.
const sharp = require("sharp");
const path = require("path");
const React = require("react");
const { renderToStaticMarkup } = require("react-dom/server");
const Lu = require("react-icons/lu");
const OUT = path.join(__dirname, "..", "images");

const C = {
  ink: "#0E1726", navy: "#0B1F3A", amber: "#F5B400", red: "#D93025",
  sky0: "#070E1C", sky1: "#0F2142", sky2: "#2A4370", sky3: "#7C8DAE", glow: "#FFD48A",
};
const FONT = "Pretendard, Apple SD Gothic Neo, sans-serif";
const T = (x, y, s, txt, o = {}) =>
  `<text x="${x}" y="${y}" font-family="${FONT}" font-size="${s}" font-weight="${o.w || 500}" fill="${o.c || C.ink}" text-anchor="${o.a || "start"}">${txt}</text>`;
const COMMON_DEFS = `
  <filter id="b2" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2"/></filter>
  <filter id="b6" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>
  <filter id="b14" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14"/></filter>
  <filter id="b30" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="30"/></filter>
  <linearGradient id="bodyDay" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FBFCFD"/><stop offset=".55" stop-color="#E7EBF0"/><stop offset="1" stop-color="#C9D0D9"/></linearGradient>
  <linearGradient id="bodyNight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C9D2DE"/><stop offset=".35" stop-color="#8E9AAB"/><stop offset="1" stop-color="#3C4757"/></linearGradient>
  <linearGradient id="glass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3A4D6B"/><stop offset=".6" stop-color="#16233A"/><stop offset="1" stop-color="#0B1322"/></linearGradient>
  <linearGradient id="clad" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2E3540"/><stop offset="1" stop-color="#171B22"/></linearGradient>
  <radialGradient id="rim" cx=".5" cy=".45" r=".6"><stop offset="0" stop-color="#E9EDF2"/><stop offset=".6" stop-color="#9AA5B2"/><stop offset="1" stop-color="#5D6774"/></radialGradient>
  <linearGradient id="beam" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFF4D6" stop-opacity=".55"/><stop offset="1" stop-color="#FFF4D6" stop-opacity="0"/></linearGradient>
  <linearGradient id="soil" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8A7560"/><stop offset=".35" stop-color="#6D5847"/><stop offset="1" stop-color="#3F3229"/></linearGradient>
  <linearGradient id="asph" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3A3F48"/><stop offset="1" stop-color="#23272E"/></linearGradient>`;
const svg = (w, h, body, defs = "") => `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}"><defs>${COMMON_DEFS}${defs}</defs>${body}</svg>`;

// PV5 카고 측면(오른쪽 진행). 로컬 0..400 x 0..185
function pv5Side(x, y, s, o = {}) {
  const night = !!o.night;
  let g = `<g transform="translate(${x},${y}) scale(${s})">`;
  if (o.shadow !== false) g += `<ellipse cx="210" cy="183" rx="215" ry="10" fill="#000" opacity="${night ? 0.65 : 0.22}" filter="url(#b6)"/>`;
  if (night) g += `<path d="M 396 106 L 640 70 L 640 170 L 396 128 Z" fill="url(#beam)" filter="url(#b6)"/>`;
  if (o.gpr) {
    g += `<rect x="8" y="148" width="6" height="22" fill="#2B3138"/><rect x="60" y="148" width="6" height="22" fill="#2B3138"/>`;
    g += `<rect x="-14" y="166" width="98" height="11" rx="2" fill="#2B3138"/><rect x="-14" y="166" width="98" height="4" rx="2" fill="${C.amber}"/>`;
    if (o.waves) for (let k = 1; k <= 4; k++) g += `<path d="M ${-20 - k * 12} ${184 + k * 9} Q 35 ${196 + k * 22} ${90 + k * 12} ${184 + k * 9}" fill="none" stroke="${C.amber}" stroke-width="1.6" opacity="${0.8 - k * 0.17}"/>`;
  }
  g += `<path d="M 18 142 L 18 46 Q 18 21 44 20 L 318 16 Q 334 16 340 28 L 376 90 Q 380 96 390 100 Q 399 104 399 118 L 399 142 Q 399 152 389 152 L 28 152 Q 18 152 18 142 Z" fill="${night ? "url(#bodyNight)" : "url(#bodyDay)"}"/>`;
  g += `<path d="M 44 20 L 318 16 Q 334 16 340 28 L 342 31 L 44 25 Z" fill="#fff" opacity="${night ? 0.35 : 0.8}"/>`;
  g += `<path d="M 330 26 L 340 28 L 376 91 L 364 92 Z" fill="url(#glass)"/>`;
  g += `<path d="M 270 30 L 326 27 L 360 90 L 270 90 Z" fill="url(#glass)"/><path d="M 286 30 L 300 29 L 282 90 L 270 90 L 270 60 Z" fill="#fff" opacity=".08"/>`;
  g += `<line x1="182" y1="30" x2="182" y2="128" stroke="#000" stroke-opacity=".14" stroke-width="1.2"/><line x1="266" y1="26" x2="266" y2="128" stroke="#000" stroke-opacity=".14" stroke-width="1.2"/>`;
  g += `<rect x="236" y="74" width="14" height="3.5" rx="1.7" fill="#000" opacity=".25"/>`;
  g += `<path d="M 18 124 L 399 124 L 399 142 Q 399 152 389 152 L 28 152 Q 18 152 18 142 Z" fill="url(#clad)"/>`;
  g += `<rect x="18" y="36" width="4" height="80" rx="2" fill="${night ? "#FF4B4B" : "#B4232A"}"/>`;
  if (night) g += `<rect x="6" y="40" width="22" height="72" rx="10" fill="#FF3B3B" opacity=".55" filter="url(#b6)"/>`;
  g += `<rect x="378" y="58" width="4" height="36" rx="2" fill="${night ? "#FFF6DD" : "#E6EAF0"}"/>`;
  if (night) g += `<ellipse cx="392" cy="100" rx="16" ry="22" fill="#FFF6DD" opacity=".6" filter="url(#b6)"/>`;
  for (const cx of [86, 322]) {
    g += `<path d="M ${cx - 38} 152 A 38 38 0 0 1 ${cx + 38} 152 Z" fill="#0E1116"/>`;
    g += `<circle cx="${cx}" cy="152" r="30" fill="#14181E"/><circle cx="${cx}" cy="152" r="18" fill="url(#rim)"/><circle cx="${cx}" cy="152" r="5" fill="#2B3138"/>`;
  }
  if (o.roof) g += `<rect x="54" y="13" width="22" height="7" rx="3" fill="#2B3138"/><ellipse cx="65" cy="12" rx="9" ry="4" fill="#E9EDF2"/><rect x="232" y="11" width="22" height="9" rx="3" fill="#2B3138"/><circle cx="249" cy="15.5" r="3" fill="#7CC4FF"/>`;
  if (o.beacon) {
    g += `<rect x="134" y="12" width="50" height="6" rx="3" fill="${C.amber}"/>`;
    if (night) g += `<ellipse cx="159" cy="14" rx="40" ry="12" fill="${C.amber}" opacity=".5" filter="url(#b6)"/>`;
  }
  return g + `</g>`;
}
function pv5Rear(x, y, s) {
  let g = `<g transform="translate(${x},${y}) scale(${s})">`;
  g += `<ellipse cx="100" cy="188" rx="110" ry="9" fill="#000" opacity=".6" filter="url(#b6)"/>`;
  g += `<rect x="18" y="150" width="30" height="36" rx="6" fill="#111"/><rect x="152" y="150" width="30" height="36" rx="6" fill="#111"/>`;
  g += `<path d="M 14 160 L 14 40 Q 14 18 38 16 L 162 16 Q 186 18 186 40 L 186 160 Z" fill="url(#bodyNight)"/>`;
  g += `<path d="M 38 16 L 162 16 Q 186 18 186 30 L 14 30 Q 14 18 38 16 Z" fill="#fff" opacity=".25"/>`;
  g += `<rect x="40" y="36" width="120" height="42" rx="6" fill="url(#glass)"/><line x1="100" y1="34" x2="100" y2="150" stroke="#000" stroke-opacity=".25" stroke-width="1.5"/>`;
  for (const lx of [16, 177]) g += `<rect x="${lx}" y="28" width="7" height="100" rx="3" fill="#FF4B4B"/><rect x="${lx - 10}" y="30" width="27" height="96" rx="12" fill="#FF3B3B" opacity=".55" filter="url(#b6)"/>`;
  g += `<rect x="14" y="146" width="172" height="20" rx="4" fill="url(#clad)"/><rect x="40" y="168" width="120" height="8" rx="2" fill="#2B3138"/><rect x="40" y="168" width="120" height="3" rx="1" fill="${C.amber}"/>`;
  g += `<rect x="74" y="10" width="52" height="6" rx="3" fill="${C.amber}"/><ellipse cx="100" cy="12" rx="44" ry="11" fill="${C.amber}" opacity=".45" filter="url(#b6)"/>`;
  return g + `</g>`;
}
function worker(x, y, s) {
  let g = `<g transform="translate(${x},${y}) scale(${s})">`;
  g += `<ellipse cx="30" cy="158" rx="26" ry="4" fill="#000" opacity=".25" filter="url(#b2)"/>`;
  g += `<rect x="17" y="104" width="11" height="54" rx="5" fill="#2E3540"/><rect x="32" y="104" width="11" height="54" rx="5" fill="#262C35"/>`;
  g += `<path d="M 10 52 Q 30 42 50 52 L 52 108 L 8 108 Z" fill="#F08C00"/><rect x="10" y="76" width="42" height="5" fill="#E9EDF2"/><rect x="10" y="91" width="42" height="5" fill="#E9EDF2"/>`;
  g += `<rect x="2" y="54" width="10" height="42" rx="5" fill="#E07B00"/><rect x="48" y="54" width="10" height="42" rx="5" fill="#E07B00"/>`;
  g += `<circle cx="30" cy="31" r="13" fill="#E8C3A0"/><path d="M 15 28 Q 30 8 45 28 Z" fill="${C.amber}"/><rect x="13" y="26" width="34" height="4" rx="2" fill="#D49A00"/>`;
  return g + `</g>`;
}
function cartGpr(x, y, s) {
  let g = `<g transform="translate(${x},${y}) scale(${s})">`;
  g += `<ellipse cx="40" cy="74" rx="46" ry="5" fill="#000" opacity=".25" filter="url(#b2)"/>`;
  g += `<rect x="0" y="40" width="80" height="22" rx="4" fill="#2B3138"/><rect x="0" y="40" width="80" height="6" rx="3" fill="${C.amber}"/>`;
  g += `<circle cx="12" cy="66" r="8" fill="#111"/><circle cx="68" cy="66" r="8" fill="#111"/>`;
  g += `<line x1="70" y1="42" x2="110" y2="-10" stroke="#2B3138" stroke-width="5" stroke-linecap="round"/>`;
  g += `<rect x="96" y="-26" width="32" height="22" rx="3" fill="#1B2129"/><rect x="99" y="-23" width="26" height="16" rx="1" fill="#3B82C4"/>`;
  return g + `</g>`;
}

// 야간 도심(블루아워)
function nightCity(w, h, o = {}) {
  const hz = h * (o.horizon || 0.6);
  const id = "sk" + w + h;
  const d = `<linearGradient id="${id}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${C.sky0}"/><stop offset=".5" stop-color="${C.sky1}"/><stop offset=".85" stop-color="${C.sky2}"/><stop offset="1" stop-color="${o.dawn ? "#C99068" : C.sky3}"/></linearGradient>
  <linearGradient id="rd${id}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1A2230"/><stop offset="1" stop-color="#06090F"/></linearGradient>`;
  let g = `<rect width="${w}" height="${h}" fill="url(#${id})"/>`;
  g += `<ellipse cx="${w * 0.5}" cy="${hz}" rx="${w * 0.7}" ry="${h * 0.12}" fill="${o.dawn ? "#E2A66F" : "#4A6390"}" opacity=".35" filter="url(#b30)"/>`;
  let bx = -10, i = 0;
  while (bx < w) { const bw = 50 + ((i * 53) % 80), bh = hz * (0.22 + ((i * 37) % 45) / 100); g += `<rect x="${bx}" y="${hz - bh}" width="${bw}" height="${bh}" fill="#13233F" opacity=".9"/>`; bx += bw + 3; i++; }
  bx = -30; i = 2;
  while (bx < w) {
    const bw = 120 + ((i * 71) % 150), bh = hz * (0.38 + ((i * 29) % 42) / 100);
    g += `<rect x="${bx}" y="${hz - bh}" width="${bw}" height="${bh}" fill="#0A1528"/>`;
    for (let wy = hz - bh + 16; wy < hz - 16; wy += 20) for (let wx = bx + 10; wx < bx + bw - 12; wx += 15) {
      const r = (wx * 13 + wy * 7 + i * 31) % 37;
      if (r < 2) g += `<rect x="${wx}" y="${wy}" width="8" height="10" fill="#FFD08A" opacity="${0.45 + (r % 2) * 0.35}"/>`;
      else if (r === 3) g += `<rect x="${wx}" y="${wy}" width="8" height="10" fill="#9CC3FF" opacity=".25"/>`;
    }
    bx += bw + 28; i++;
  }
  g += `<rect y="${hz - 2}" width="${w}" height="${h * 0.04}" fill="#5D79A8" opacity=".18" filter="url(#b14)"/>`;
  g += `<rect y="${hz}" width="${w}" height="${h - hz}" fill="url(#rd${id})"/><rect y="${hz}" width="${w}" height="6" fill="#2C3647"/>`;
  for (let lx = 0; lx < w; lx += 150) g += `<rect x="${lx}" y="${hz + (h - hz) * 0.5}" width="80" height="5" rx="2" fill="#D6DCE4" opacity=".35"/>`;
  for (let lx = 120; lx < w; lx += 460) {
    g += `<rect x="${lx}" y="${hz - 230}" width="5" height="234" fill="#1F2937"/><path d="M ${lx + 2} ${hz - 230} q 10 -12 46 -8" stroke="#1F2937" stroke-width="5" fill="none"/>`;
    g += `<ellipse cx="${lx + 46}" cy="${hz - 232}" rx="60" ry="60" fill="${C.glow}" opacity=".22" filter="url(#b30)"/><rect x="${lx + 34}" y="${hz - 238}" width="24" height="5" rx="2" fill="#FFE9BD"/>`;
    g += `<path d="M ${lx + 34} ${hz - 233} L ${lx - 40} ${hz} L ${lx + 130} ${hz} L ${lx + 58} ${hz - 233} Z" fill="${C.glow}" opacity=".05"/>`;
    g += `<rect x="${lx + 36}" y="${hz + 8}" width="20" height="${(h - hz) * 0.7}" fill="${C.glow}" opacity=".14" filter="url(#b14)"/>`;
  }
  return { g, d, hz };
}
function groundSection(x, y, w, h) {
  let g = `<g transform="translate(${x},${y})"><rect width="${w}" height="${h * 0.07}" fill="url(#asph)"/><rect y="${h * 0.07}" width="${w}" height="${h * 0.1}" fill="#9C8B78"/><rect y="${h * 0.17}" width="${w}" height="${h * 0.83}" fill="url(#soil)"/>`;
  for (let i = 0; i < 90; i++) g += `<circle cx="${(i * 137) % w}" cy="${h * 0.19 + ((i * 89) % (h * 0.79))}" r="${0.8 + (i % 3) * 0.7}" fill="#2E241C" opacity=".35"/>`;
  return g + `</g>`;
}
let BS = 0;
function bscan(x, y, w, h, o = {}) {
  const id = "bs" + BS++;
  const d = `<clipPath id="c${id}"><rect width="${w}" height="${h}" rx="4"/></clipPath><filter id="${id}" x="0" y="0" width="1" height="1"><feTurbulence type="fractalNoise" baseFrequency="0.9 0.05" numOctaves="2" seed="${o.seed || 3}"/><feColorMatrix type="saturate" values="0"/><feComponentTransfer><feFuncA type="table" tableValues="0 .5"/></feComponentTransfer></filter>`;
  let g = `<g transform="translate(${x},${y})"><g clip-path="url(#c${id})"><rect width="${w}" height="${h}" fill="#575B61"/><rect width="${w}" height="${h}" filter="url(#${id})"/>`;
  for (let i = 0; i < 9; i++) {
    const yy = 14 + i * (h / 10);
    let p = `M 0 ${yy}`;
    for (let xx = 0; xx <= w; xx += 20) p += ` L ${xx} ${yy + Math.sin((xx + i * 37) / 41) * 2.2}`;
    g += `<path d="${p}" fill="none" stroke="${i % 2 ? "#E9ECEF" : "#1C1F23"}" stroke-width="${i < 2 ? 2.6 : 1.2}" opacity=".6"/>`;
  }
  const hyp = (cx, cy, a, k, col, sw) => { let p = ""; for (let t = -a; t <= a; t += 4) p += `${p ? "L" : "M"} ${cx + t} ${cy + (t * t) / k} `; return `<path d="${p}" fill="none" stroke="${col}" stroke-width="${sw}"/>`; };
  g += hyp(w * 0.22, h * 0.42, w * 0.15, w * 0.12, "#F8F9FA", 2.6) + hyp(w * 0.22, h * 0.42 + 6, w * 0.14, w * 0.12, "#16191D", 1.8);
  if (o.cavity) {
    const cx = w * 0.64, cy = h * 0.52, sc = o.cavity;
    g += hyp(cx, cy, w * 0.18 * sc, w * 0.1, "#FFFFFF", 3.4) + hyp(cx, cy + 7, w * 0.17 * sc, w * 0.1, "#0D0F12", 2.6);
    g += `<ellipse cx="${cx}" cy="${cy + 16 * sc}" rx="${w * 0.1 * sc}" ry="${h * 0.06 * sc}" fill="#000" opacity=".45" filter="url(#b2)"/>`;
  }
  if (o.box) { const b = o.box; g += `<rect x="${w * b[0]}" y="${h * b[1]}" width="${w * b[2]}" height="${h * b[3]}" rx="3" fill="${C.amber}" fill-opacity=".12" stroke="${C.amber}" stroke-width="2.5"/>`; }
  g += `</g>`;
  for (let i = 1; i <= 3; i++) g += `<line x1="0" y1="${(h / 4) * i}" x2="7" y2="${(h / 4) * i}" stroke="#fff" stroke-width="1.2"/>` + T(11, (h / 4) * i + 4, 12, `${(i * 0.5).toFixed(1)}m`, { c: "#fff" });
  return { g: g + `</g>`, d };
}

async function save(name, w, h, body, defs = "", density = 144) {
  const file = path.join(OUT, name + ".png");
  await sharp(Buffer.from(svg(w, h, body, defs)), { density }).png().toFile(file);
  return file;
}
async function icon(name, Comp, color, size = 256) {
  const el = React.createElement(Comp, { size, color, strokeWidth: 1.6 });
  await sharp(Buffer.from(renderToStaticMarkup(el))).resize(size, size).png().toFile(path.join(OUT, "ico_" + name + ".png"));
}

const jobs = {};
jobs.cover = async () => {
  const W = 1920, H = 1080;
  const { g, d, hz } = nightCity(W, H, { horizon: 0.52 });
  let b = g;
  const top = hz + 150;
  b += `<rect y="${top}" width="${W}" height="${H - top}" fill="#07090D"/><rect y="${top}" width="${W}" height="2" fill="#3A4350"/><rect y="${top + 2}" width="${W}" height="${H - top}" fill="url(#soil)" opacity=".25"/>`;
  b += `<rect x="0" y="${top + 92}" width="${W}" height="28" fill="#1A1F27"/><rect x="0" y="${top + 92}" width="${W}" height="2" fill="#2E3540"/>`;
  const cx = 1360, cy = top + 70;
  b += `<ellipse cx="${cx}" cy="${cy}" rx="190" ry="58" fill="${C.amber}" opacity=".12" filter="url(#b30)"/>`;
  [[70, 22, 0.35], [120, 38, 0.55], [178, 56, 0.9]].forEach(([rx, ry, op], k) => (b += `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="none" stroke="${C.amber}" stroke-width="${1.2 + k * 0.6}" stroke-dasharray="${k === 2 ? "0" : "6 7"}" opacity="${op}"/>`));
  b += `<ellipse cx="${cx}" cy="${cy}" rx="150" ry="44" fill="#000" opacity=".65" filter="url(#b6)"/>`;
  for (let k = 0; k < 7; k++) b += `<path d="M ${cx - 70 + k * 22} ${top + 120} q 4 8 0 11 q -4 -3 0 -11 z" fill="#6CB4FF" opacity=".55"/>`;
  const dd = d + `<linearGradient id="shadeL" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#050A14" stop-opacity=".92"/><stop offset=".45" stop-color="#050A14" stop-opacity=".7"/><stop offset=".75" stop-color="#050A14" stop-opacity="0"/></linearGradient>`;
  b += `<rect width="${W}" height="${H}" fill="url(#shadeL)"/>`;
  return save("cover", W, H, b, dd);
};
jobs.mechanism = async () => {
  const W = 1600, H = 820;
  let b = `<rect width="${W}" height="${H}" fill="#EEF2F7"/>` + groundSection(0, 110, W, 710);
  b += `<path d="M 560 170 L 1040 170 L 860 640 Z" fill="#5E4A3A" opacity=".85"/><path d="M 560 170 L 1040 170 L 860 640 Z" fill="none" stroke="#1E150F" stroke-width="2.5" stroke-dasharray="10 8"/>`;
  b += T(800, 410, 30, "쐐기형 토체", { w: 700, c: "#fff", a: "middle" });
  b += `<rect x="0" y="232" width="${W}" height="38" fill="#4B525C"/><rect x="0" y="232" width="${W}" height="3" fill="#6B737E"/>`;
  for (let k = 0; k < 8; k++) b += `<path d="M ${640 + k * 30} 274 q 6 12 0 17 q -6 -5 0 -17 z" fill="#6CB4FF"/>`;
  b += T(40, 259, 24, "노후 하수관 누수", { w: 700, c: "#fff" });
  b += `<path d="M 0 520 Q 400 500 800 560 T ${W} 600" fill="none" stroke="#6CB4FF" stroke-width="4" stroke-dasharray="12 9"/>`;
  b += `<path d="M 1380 470 L 1380 580" stroke="#6CB4FF" stroke-width="5"/><path d="M 1366 576 L 1380 600 L 1394 576 Z" fill="#6CB4FF"/>` + T(1140, 455, 24, "지하수위 저하", { w: 700, c: "#D9ECFF" });
  b += `<rect x="0" y="690" width="${W}" height="96" rx="48" fill="#111418" opacity=".9"/>` + T(40, 748, 24, "하부 터널 굴착", { w: 700, c: "#fff" });
  b += `<rect x="0" y="104" width="${W}" height="12" fill="#2B3038"/>`;
  return save("mechanism", W, H, b);
};
const stage = (W, H) => `<rect width="${W}" height="${H}" fill="#EEF2F7"/><rect y="${H * 0.76}" width="${W}" height="${H * 0.24}" fill="#D9DFE7"/><rect y="${H * 0.76}" width="${W}" height="2" fill="#C5CDD8"/>`;
jobs.methodVehicle = async () => {
  const W = 800, H = 480;
  let b = stage(W, H) + `<g transform="translate(150,170)"><ellipse cx="260" cy="200" rx="270" ry="10" fill="#000" opacity=".2" filter="url(#b6)"/><rect x="0" y="30" width="440" height="160" rx="14" fill="url(#bodyDay)"/><path d="M 440 50 L 520 110 Q 528 118 528 130 L 528 180 Q 528 190 518 190 L 440 190 Z" fill="url(#bodyDay)"/><path d="M 450 62 L 512 110 L 450 110 Z" fill="url(#glass)"/><rect x="0" y="160" width="528" height="30" rx="6" fill="url(#clad)"/><circle cx="110" cy="192" r="32" fill="#14181E"/><circle cx="110" cy="192" r="18" fill="url(#rim)"/><circle cx="430" cy="192" r="32" fill="#14181E"/><circle cx="430" cy="192" r="18" fill="url(#rim)"/><rect x="-70" y="186" width="130" height="12" rx="2" fill="#2B3138"/><rect x="-70" y="186" width="130" height="4" fill="${C.amber}"/></g>`;
  return save("method_vehicle", W, H, b);
};
jobs.methodCart = async () => save("method_cart", 800, 480, stage(800, 480) + worker(440, 210, 1.05) + cartGpr(260, 304, 1.25));
jobs.methodScope = async () => {
  let b = `<rect width="800" height="480" fill="#EEF2F7"/>` + groundSection(0, 250, 800, 230);
  b += `<rect x="372" y="200" width="56" height="70" rx="4" fill="#2B3138"/><rect x="390" y="250" width="20" height="150" fill="#1B2129"/><ellipse cx="400" cy="420" rx="120" ry="40" fill="#0A0B0D" opacity=".75" filter="url(#b2)"/><circle cx="400" cy="408" r="8" fill="#6CB4FF"/><path d="M 400 408 L 480 380 L 480 440 Z" fill="#A9D3FF" opacity=".35"/>`;
  return save("method_scope", 800, 480, b);
};
jobs.gapTimeline = async () => {
  const W = 1700, H = 420;
  let b = `<rect width="${W}" height="${H}" fill="#fff"/><rect x="440" y="200" width="1000" height="56" rx="6" fill="${C.amber}" opacity=".16"/><line x1="80" y1="228" x2="1620" y2="228" stroke="#C5CDD8" stroke-width="4"/>`;
  ["5월", "6월", "7월", "8월"].forEach((m, i) => { const x = 160 + i * 460; b += `<line x1="${x}" y1="214" x2="${x}" y2="242" stroke="#8A94A3" stroke-width="3"/>` + T(x, 290, 28, m, { a: "middle", c: "#5B6573", w: 600 }); });
  b += `<circle cx="200" cy="228" r="18" fill="#2F9E44"/><circle cx="1540" cy="228" r="18" fill="${C.red}"/>`;
  b += T(200, 92, 34, "5.7~5.16  GPR 탐사", { a: "middle", w: 800, c: "#1F7A35" }) + T(200, 138, 28, "공동 미발견", { a: "middle", c: "#1F7A35", w: 600 });
  b += T(1540, 92, 34, "8.29  도로 함몰", { a: "middle", w: 800, c: C.red }) + T(1540, 138, 28, "주행 차량 빠짐", { a: "middle", c: C.red, w: 600 });
  b += T(940, 370, 32, "이 사이의 지하 변화는 기록되지 않았습니다", { a: "middle", w: 700, c: "#7A5A00" });
  return save("gap_timeline", W, H, b);
};
jobs.overviewPv5 = async () => {
  const { g, d } = nightCity(900, 620, { horizon: 0.64 });
  return save("overview_pv5", 900, 620, g + pv5Side(150, 250, 1.45, { night: true, gpr: true, roof: true, beacon: true, waves: true }), d);
};
jobs.dawnPatrol = async () => {
  const W = 1920, H = 1080;
  const { g, d, hz } = nightCity(W, H, { horizon: 0.58, dawn: true });
  let b = g + pv5Side(900, hz - 30, 2.25, { night: true, gpr: true, roof: true, beacon: true });
  const dd = d + `<linearGradient id="shadeL2" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#050A14" stop-opacity=".94"/><stop offset=".45" stop-color="#050A14" stop-opacity=".8"/><stop offset=".62" stop-color="#050A14" stop-opacity="0"/></linearGradient>`;
  b += `<rect width="${W}" height="${H}" fill="url(#shadeL2)"/>`;
  return save("dawn_patrol", W, H, b, dd);
};
jobs.dawnPlain = async () => {
  const W = 1920, H = 1080;
  const { g, d, hz } = nightCity(W, H, { horizon: 0.58, dawn: true });
  return save("dawn_plain", W, H, g + pv5Side(620, hz - 30, 2.25, { night: true, gpr: true, roof: true, beacon: true }), d);
};
jobs.cutaway = async () => {
  const W = 1700, H = 760;
  let b = `<rect width="${W}" height="${H}" fill="#fff"/><rect y="690" width="${W}" height="70" fill="#EEF2F7"/>` + pv5Side(170, 70, 3.4, { gpr: true, roof: true, beacon: true, waves: true });
  const X = (lx) => 170 + lx * 3.4, Y = (ly) => 70 + ly * 3.4;
  const zone = (x1, x2, col) => `<rect x="${X(x1)}" y="${Y(36)}" width="${(x2 - x1) * 3.4}" height="${86 * 3.4}" rx="8" fill="${col}" fill-opacity=".1" stroke="${col}" stroke-width="2.5" stroke-dasharray="9 6"/>`;
  b += zone(184, 256, "#1C64B5") + zone(100, 180, "#0B1F3A") + zone(24, 96, "#B4232A");
  b += `<rect x="${X(196)}" y="${Y(70)}" width="${46 * 3.4}" height="${52 * 3.4}" rx="8" fill="#232A33"/>`;
  for (let k = 0; k < 4; k++) b += `<rect x="${X(200)}" y="${Y(74 + k * 11.5)}" width="${38 * 3.4}" height="${8 * 3.4}" rx="3" fill="${k === 0 ? "#2F6FB3" : "#3A434F"}"/><circle cx="${X(234)}" cy="${Y(78 + k * 11.5)}" r="5" fill="${k === 3 ? C.amber : "#5AD27A"}"/>`;
  b += `<rect x="${X(108)}" y="${Y(92)}" width="${36 * 3.4}" height="${28 * 3.4}" rx="6" fill="#2B3138"/><rect x="${X(108)}" y="${Y(92)}" width="${36 * 3.4}" height="12" rx="6" fill="${C.amber}"/>`;
  b += `<rect x="${X(148)}" y="${Y(98)}" width="${26 * 3.4}" height="${22 * 3.4}" rx="6" fill="#1B2A44"/><rect x="${X(152)}" y="${Y(104)}" width="${18 * 3.4}" height="10" rx="5" fill="#7CC4FF"/>`;
  b += `<path d="M ${X(32)} ${Y(122)} L ${X(40)} ${Y(96)} L ${X(48)} ${Y(122)} Z" fill="#E8590C"/><path d="M ${X(52)} ${Y(122)} L ${X(60)} ${Y(96)} L ${X(68)} ${Y(122)} Z" fill="#E8590C"/><rect x="${X(74)}" y="${Y(100)}" width="${18 * 3.4}" height="${22 * 3.4}" rx="5" fill="#3A434F"/>`;
  return save("cutaway", W, H, b);
};
jobs.map4d = async () => {
  const W = 1700, H = 900;
  let b = `<rect width="${W}" height="${H}" rx="16" fill="#0D1828"/>` + T(32, 46, 24, "GroundWatch Cloud", { w: 700, c: "#fff" }) + T(268, 46, 20, "4D 도로 지하 변화지도", { c: "#9AA8BC" }) + T(W - 32, 46, 18, "예시 화면", { a: "end", c: "#7D8BA0" });
  const mx = 20, my = 76, mw = 1080, mh = 804;
  b += `<rect x="${mx}" y="${my}" width="${mw}" height="${mh}" rx="10" fill="#E7ECF2"/>`;
  for (let i = 0; i < 14; i++) for (let j = 0; j < 10; j++) b += `<rect x="${mx + 14 + i * 76}" y="${my + 14 + j * 78}" width="62" height="64" rx="5" fill="#F7F9FB"/>`;
  b += `<path d="M ${mx} ${my + 610} C 300 640, 600 560, ${mx + mw} 620 L ${mx + mw} 700 C 600 640, 300 720, ${mx} 690 Z" fill="#BFDDF7"/>`;
  const seg = (x1, y1, x2, y2, col, dash) => `<line x1="${mx + x1}" y1="${my + y1}" x2="${mx + x2}" y2="${my + y2}" stroke="${col}" stroke-width="11" stroke-linecap="round" ${dash ? 'stroke-dasharray="2 16"' : ""}/>`;
  b += seg(7, 85, 1070, 85, "#B5BDC8") + seg(7, 241, 1070, 241, "#3BA55C") + seg(7, 397, 1070, 397, "#3BA55C") + seg(83, 0, 83, 600, "#3BA55C") + seg(311, 0, 311, 600, "#3BA55C") + seg(539, 0, 539, 600, "#B5BDC8") + seg(767, 0, 767, 600, "#3BA55C");
  b += seg(311, 241, 539, 241, C.amber) + seg(539, 397, 767, 397, "#F08C00") + seg(767, 241, 767, 397, C.red) + seg(83, 397, 311, 397, "#3BA55C", true) + seg(995, 0, 995, 600, "#B5BDC8", true);
  b += `<circle cx="${mx + 767}" cy="${my + 320}" r="34" fill="${C.red}" opacity=".18"/><circle cx="${mx + 767}" cy="${my + 320}" r="10" fill="${C.red}" stroke="#fff" stroke-width="3"/>`;
  b += `<rect x="${mx + 16}" y="${my + mh - 66}" width="1010" height="50" rx="10" fill="#fff"/>`;
  [["#B5BDC8", "미조사"], ["#3BA55C", "변화 없음"], [C.amber, "새 이상 신호"], ["#F08C00", "확대 의심"], [C.red, "정밀 재탐사"]].forEach(([c, t], i) => (b += `<rect x="${mx + 36 + i * 190}" y="${my + mh - 48}" width="30" height="12" rx="6" fill="${c}"/>` + T(mx + 76 + i * 190, my + mh - 36, 19, t, { c: "#2B3138", w: 600 })));
  const px = 1120, py = 76;
  b += `<rect x="${px}" y="${py}" width="560" height="804" rx="10" fill="#132238"/>` + T(px + 24, py + 42, 22, "구간 상세", { w: 700, c: "#fff" }) + T(px + 536, py + 42, 18, "R-0427", { a: "end", c: "#9AA8BC" });
  const bs = bscan(px + 24, py + 70, 512, 210, { cavity: 0.8, seed: 7, box: [0.45, 0.28, 0.42, 0.62] });
  b += bs.g + T(px + 24, py + 318, 17, "회차별 이상 반사 면적", { c: "#9AA8BC" });
  [[0, 40, "#3BA55C"], [1, 44, "#3BA55C"], [2, 62, C.amber], [3, 86, "#F08C00"], [4, 106, C.red]].forEach(([i, v, col]) => (b += `<rect x="${px + 40 + i * 100}" y="${py + 450 - v}" width="56" height="${v}" rx="4" fill="${col}"/>` + T(px + 68 + i * 100, py + 476, 15, `${i + 1}회`, { a: "middle", c: "#7D8BA0" })));
  [["마지막 조사", "최근 회차"], ["반복 조사", "5회"], ["추정 깊이", "0.9–1.3 m"], ["AI 위험점수 · 신뢰도", "높음 · 84%"], ["위치 오차", "±[실증 필요]"], ["전문가 검토", "대기"]].forEach(([k, v], i) => (b += `<line x1="${px + 24}" y1="${py + 512 + i * 46}" x2="${px + 536}" y2="${py + 512 + i * 46}" stroke="#22344F"/>` + T(px + 24, py + 543 + i * 46, 18, k, { c: "#9AA8BC" }) + T(px + 536, py + 543 + i * 46, 18, v, { a: "end", w: 700, c: i === 3 ? C.amber : "#fff" })));
  return save("map4d", W, H, b, bs.d);
};
jobs.aiCompare = async () => {
  const W = 1700, H = 600;
  const a = bscan(0, 56, 800, 520, { cavity: 0.55, seed: 4 });
  const c = bscan(900, 56, 800, 520, { cavity: 0.9, seed: 4, box: [0.46, 0.3, 0.38, 0.52] });
  let b = `<rect width="${W}" height="${H}" fill="#fff"/>` + a.g + c.g + T(0, 36, 26, "이전 탐사 회차", { w: 700, c: "#5B6573" }) + T(900, 36, 26, "현재 탐사 회차", { w: 700, c: C.navy });
  b += `<line x1="812" y1="316" x2="878" y2="316" stroke="${C.navy}" stroke-width="3"/><path d="M 872 306 L 890 316 L 872 326 Z" fill="${C.navy}"/>`;
  b += `<rect x="${900 + 368}" y="${56 + 156 - 36}" width="190" height="30" rx="4" fill="${C.amber}"/>` + T(900 + 380, 56 + 156 - 15, 18, "새로 커진 신호", { w: 700 });
  return save("ai_compare", W, H, b, a.d + c.d);
};
jobs.surfaceCrack = async () => {
  const W = 700, H = 420;
  let b = `<rect width="${W}" height="${H}" fill="#353A42"/>`;
  for (let i = 0; i < 380; i++) b += `<circle cx="${(i * 97) % W}" cy="${(i * 53) % H}" r="${0.8 + (i % 3) * 0.6}" fill="#4B525C" opacity=".7"/>`;
  b += `<circle cx="420" cy="230" r="88" fill="#4A5059"/><circle cx="420" cy="230" r="88" fill="none" stroke="#24282E" stroke-width="9"/><circle cx="420" cy="230" r="60" fill="none" stroke="#24282E" stroke-width="3"/>`;
  b += `<path d="M 330 210 l -40 -20 l -30 12 l -40 -28 M 290 190 l -10 40 l -36 24" stroke="#14171B" stroke-width="3.5" fill="none"/><path d="M 340 300 q 40 30 120 14" stroke="#4E8FD9" stroke-width="9" fill="none" opacity=".35"/>`;
  b += `<rect x="190" y="150" width="160" height="110" rx="3" fill="none" stroke="${C.amber}" stroke-width="3"/><rect x="190" y="122" width="146" height="26" rx="3" fill="${C.amber}"/>` + T(200, 141, 16, "균열 신규 0.86", { w: 700 });
  b += `<rect x="322" y="132" width="196" height="196" rx="3" fill="none" stroke="#7CC4FF" stroke-width="3" stroke-dasharray="9 6"/><rect x="420" y="332" width="164" height="26" rx="3" fill="#7CC4FF"/>` + T(430, 351, 16, "맨홀 주변 단차", { w: 700 });
  return save("surface_crack", W, H, b);
};
function iviScreen(mode) {
  const W = 1600, H = 620;
  let b = `<rect width="${W}" height="${H}" rx="26" fill="#05080D"/><rect x="16" y="16" width="${W - 32}" height="${H - 32}" rx="16" fill="#0C1524"/>` + T(46, 64, 24, "GroundWatch Patrol", { w: 700, c: "#fff" }) + T(W - 46, 64, 20, "04:42   배터리 86%", { a: "end", c: "#8A97AB" });
  b += `<rect x="38" y="92" width="900" height="500" rx="12" fill="#16243A"/>`;
  for (let i = 1; i < 9; i++) b += `<line x1="${38 + i * 100}" y1="92" x2="${38 + i * 100}" y2="592" stroke="#1D2E48" stroke-width="2"/>`;
  for (let j = 1; j < 5; j++) b += `<line x1="38" y1="${92 + j * 100}" x2="938" y2="${92 + j * 100}" stroke="#1D2E48" stroke-width="2"/>`;
  b += `<path d="M 120 540 L 120 392 L 420 392 L 420 192 L 820 192 L 820 292" fill="none" stroke="#4E9BEA" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/><path d="M 120 540 L 120 392 L 300 392" fill="none" stroke="#3BA55C" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>`;
  [[420, 300], [640, 192], [820, 292]].forEach(([x, y], i) => (b += `<circle cx="${x}" cy="${y}" r="18" fill="${i === 2 ? C.red : C.amber}" stroke="#0C1524" stroke-width="4"/>` + T(x, y + 6, 16, `${i + 1}`, { a: "middle", w: 800, c: i === 2 ? "#fff" : C.ink })));
  b += `<circle cx="300" cy="392" r="12" fill="#fff"/>`;
  const px = 960;
  const row = (y, k, v, col) => `<rect x="${px}" y="${y}" width="602" height="68" rx="10" fill="#132238"/>` + T(px + 22, y + 42, 19, k, { c: "#8A97AB" }) + T(px + 580, y + 43, 24, v, { a: "end", w: 700, c: col || "#fff" });
  if (mode === "pre") {
    b += row(92, "오늘의 기본 순찰거리", "38.4 km") + row(170, "재확인 포인트", "3곳", C.amber) + row(248, "예상 소요시간", "3시간 10분") + row(326, "GPR · Edge Gateway", "연결됨", "#5AD27A") + row(404, "AR 글래스 · 저장공간", "92% · 71%", "#5AD27A");
    b += `<rect x="${px}" y="500" width="602" height="92" rx="14" fill="${C.amber}"/>` + T(px + 301, 558, 30, "순찰 시작", { a: "middle", w: 800 });
  } else if (mode === "drive") {
    b += row(92, "스캔 상태", "수집 중", "#5AD27A") + row(170, "데이터 품질", "양호", "#5AD27A") + row(248, "GNSS · IMU", "RTK 고정", "#5AD27A");
    b += `<rect x="${px}" y="330" width="602" height="262" rx="14" fill="#132238"/>` + T(px + 28, 384, 20, "다음 재확인 지점까지", { c: "#8A97AB" }) + T(px + 28, 500, 96, "420 m", { w: 800, c: C.amber });
  } else {
    b += `<rect x="${px}" y="92" width="602" height="112" rx="12" fill="#3A1216"/>` + T(px + 24, 132, 19, "위험등급", { c: "#FFB3B3" }) + T(px + 24, 182, 36, "정밀 재탐사 필요", { w: 800, c: "#fff" });
    b += row(214, "이전 회차 대비", "신규 확대") + row(290, "변화량 [예시]", "+17%", C.amber) + row(366, "추정 깊이 [예시]", "0.9–1.3 m");
    b += `<rect x="${px}" y="446" width="296" height="146" rx="14" fill="#132238"/>` + T(px + 148, 504, 19, "안전 정차 위치", { a: "middle", c: "#8A97AB" }) + T(px + 148, 552, 26, "우측 40 m", { a: "middle", w: 800, c: "#fff" });
    b += `<rect x="${px + 306}" y="446" width="296" height="146" rx="14" fill="${C.amber}"/>` + T(px + 454, 512, 25, "현장 점검 시작", { a: "middle", w: 800 }) + T(px + 454, 552, 18, "AR 글래스 연결", { a: "middle", c: "#4A3700" });
  }
  return { W, H, b };
}
jobs.iviPre = async () => { const s = iviScreen("pre"); return save("ivi_pre", s.W, s.H, s.b); };
jobs.iviDrive = async () => { const s = iviScreen("drive"); return save("ivi_drive", s.W, s.H, s.b); };
jobs.iviStop = async () => { const s = iviScreen("stop"); return save("ivi_stop", s.W, s.H, s.b); };
jobs.dashboard = async () => {
  const W = 1700, H = 760;
  const d = `<linearGradient id="ws" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0E1C33"/><stop offset="1" stop-color="#3A5582"/></linearGradient><linearGradient id="dash" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1D232D"/><stop offset="1" stop-color="#0B0E13"/></linearGradient>`;
  let b = `<rect width="${W}" height="${H}" fill="url(#ws)"/>`;
  for (let i = 0; i < 12; i++) b += `<circle cx="${100 + i * 140}" cy="${240 + (i % 3) * 20}" r="${10 + (i % 4) * 6}" fill="#FFD08A" opacity=".18" filter="url(#b6)"/>`;
  b += `<path d="M 0 330 Q 850 250 ${W} 330 L ${W} ${H} L 0 ${H} Z" fill="url(#dash)"/><path d="M 0 330 Q 850 250 ${W} 330" stroke="#3A4250" stroke-width="3" fill="none"/>`;
  b += `<circle cx="340" cy="650" r="200" fill="none" stroke="#262D38" stroke-width="36"/><circle cx="340" cy="650" r="58" fill="#262D38"/>`;
  return save("dashboard", W, H, b, d);
};
function arPov(mode) {
  const W = 1700, H = 900;
  const d = `<linearGradient id="arr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1D2532"/><stop offset="1" stop-color="#0C1017"/></linearGradient>`;
  let b = `<rect width="${W}" height="${H}" fill="#0A1222"/>`;
  for (let i = 0; i < 10; i++) b += `<rect x="${i * 190 - 30}" y="${110 + (i % 3) * 30}" width="150" height="${250 - (i % 3) * 30}" fill="#08101E"/>`;
  b += `<ellipse cx="850" cy="360" rx="900" ry="40" fill="#4A6390" opacity=".25" filter="url(#b30)"/><path d="M 0 360 L ${W} 360 L ${W} ${H} L 0 ${H} Z" fill="url(#arr)"/>`;
  b += `<path d="M 1000 360 L 1090 360 L ${W + 500} ${H} L ${W + 300} ${H} Z" fill="#6F7783"/><path d="M 848 380 L 852 380 L 870 ${H} L 830 ${H} Z" fill="#E9EDF2" opacity=".55"/><path d="M 984 360 L 1000 360 L ${W + 260} ${H} L ${W + 210} ${H} Z" fill="#E9EDF2" opacity=".55"/>`;
  b += `<ellipse cx="850" cy="880" rx="760" ry="300" fill="#FFE2A8" opacity=".09" filter="url(#b30)"/>`;
  b += `<ellipse cx="620" cy="600" rx="128" ry="44" fill="#363C45"/><ellipse cx="620" cy="600" rx="128" ry="44" fill="none" stroke="#15181C" stroke-width="9"/><ellipse cx="620" cy="600" rx="84" ry="27" fill="none" stroke="#15181C" stroke-width="3"/>`;
  const G = "#5AD27A";
  const bracket = (x, y, w, h, label) => { const L = 26; return `<path d="M ${x} ${y + L} V ${y} H ${x + L} M ${x + w - L} ${y} H ${x + w} V ${y + L} M ${x + w} ${y + h - L} V ${y + h} H ${x + w - L} M ${x + L} ${y + h} H ${x} V ${y + h - L}" stroke="${G}" stroke-width="4" fill="none"/><rect x="${x}" y="${y - 38}" width="${label.length * 19 + 28}" height="30" rx="4" fill="${G}"/>` + T(x + 12, y - 16, 18, label, { w: 700, c: "#06120A" }); };
  if (mode === "calib") {
    b += bracket(470, 540, 300, 120, "맨홀 중심") + bracket(1180, 520, 260, 200, "경계석") + bracket(800, 420, 120, 200, "차선 모서리");
    b += `<circle cx="620" cy="600" r="7" fill="${G}"/><polyline points="620,600 860,520 1310,620" fill="none" stroke="${G}" stroke-width="2.5" stroke-dasharray="8 6"/>`;
  } else {
    b += `<path d="M 520 520 L 1060 520 L 1180 800 L 400 800 Z" fill="${C.amber}" fill-opacity=".14" stroke="${C.amber}" stroke-width="4"/>`;
    for (let k = 1; k < 5; k++) b += `<line x1="${520 - k * 24}" y1="${520 + k * 56}" x2="${1060 + k * 24}" y2="${520 + k * 56}" stroke="${C.amber}" stroke-width="1.5" opacity=".5"/>`;
    for (let k = 0; k < 4; k++) b += `<path d="M ${560 + k * 140} 560 L ${520 + k * 160} 760" stroke="#7CC4FF" stroke-width="4" stroke-dasharray="12 9"/><path d="M ${510 + k * 160} 752 L ${531 + k * 160} 752 L ${518 + k * 160} 784 Z" fill="#7CC4FF"/>`;
    b += `<circle cx="560" cy="560" r="12" fill="${G}"/><rect x="1068" y="770" width="24" height="24" rx="3" fill="${C.red}"/>` + cartGpr(700, 760, 1.6);
  }
  const hud = (x, y, w, h) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="14" fill="#07101E" opacity=".78"/><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="14" fill="none" stroke="#7CC4FF" stroke-opacity=".5" stroke-width="1.5"/>`;
  if (mode === "calib") b += hud(40, 40, 460, 170) + T(68, 92, 26, "위치 보정", { w: 700, c: "#fff" }) + T(68, 136, 21, "기준점 3개 + RTK 결합", { c: "#A9D3FF" }) + T(68, 178, 22, "위치 오차 ±[실증 필요]", { w: 700, c: G });
  else b += hud(40, 40, 460, 210) + T(68, 92, 26, "재탐사 3 / 4회", { w: 700, c: "#fff" }) + T(68, 134, 21, "추정 깊이 0.9–1.3 m", { c: "#A9D3FF" }) + T(68, 172, 21, "이전 대비 +17%", { c: C.amber }) + T(68, 210, 21, "AI 신뢰도 84%", { c: "#A9D3FF" });
  b += hud(W - 500, 40, 460, 64) + T(W - 474, 82, 21, mode === "calib" ? "정차 확인됨 · 작업 모드" : "음성 “이상 위치 표시”", { c: "#fff" });
  b += `<rect x="220" y="${H - 66}" width="${W - 440}" height="42" rx="8" fill="#3A1216" opacity=".92"/>` + T(W / 2, H - 38, 19, "GPR 기반 추정 위치입니다. 굴착 전 정밀조사와 관계기관 승인이 필요합니다.", { a: "middle", c: "#FFC9C9", w: 600 });
  return { W, H, b, d };
}
jobs.arCalib = async () => { const s = arPov("calib"); return save("ar_calib", s.W, s.H, s.b, s.d); };
jobs.arScan = async () => { const s = arPov("scan"); return save("ar_scan", s.W, s.H, s.b, s.d); };
jobs.crossCheck = async () => {
  const W = 1600, H = 720;
  let b = `<rect width="${W}" height="${H}" fill="#fff"/><rect x="0" y="40" width="${W}" height="640" rx="12" fill="url(#asph)"/>`;
  for (let k = 0; k < 9; k++) b += `<rect x="0" y="${70 + k * 66}" width="${W}" height="40" fill="${C.amber}" opacity=".13"/>`;
  b += `<line x1="0" y1="360" x2="${W}" y2="360" stroke="#E9EDF2" stroke-width="5" stroke-dasharray="40 30" opacity=".5"/><ellipse cx="1060" cy="370" rx="80" ry="50" fill="#000" opacity=".45" filter="url(#b6)"/>`;
  b += `<rect x="880" y="210" width="360" height="320" rx="6" fill="none" stroke="${C.red}" stroke-width="4"/>`;
  for (let k = 0; k < 6; k++) b += `<line x1="${915 + k * 58}" y1="226" x2="${915 + k * 58}" y2="514" stroke="#7CC4FF" stroke-width="5"/>`;
  for (let k = 0; k < 4; k++) b += `<line x1="896" y1="${260 + k * 74}" x2="1224" y2="${260 + k * 74}" stroke="#5AD27A" stroke-width="5" stroke-dasharray="14 8"/>`;
  b += `<path d="M 60 600 L 400 600" stroke="#fff" stroke-width="3"/><path d="M 392 590 L 412 600 L 392 610 Z" fill="#fff"/>` + T(60, 640, 22, "차량 진행 방향", { c: "#fff", w: 600 });
  return save("cross_check", W, H, b);
};
jobs.patrolNet = async () => {
  const W = 1600, H = 900;
  let b = `<rect width="${W}" height="${H}" fill="#F3F6F9"/><path d="M 0 520 C 300 460, 600 600, 900 520 S 1400 470, ${W} 540 L ${W} 620 C 1300 560, 1000 640, 700 600 S 200 560, 0 610 Z" fill="#CFE5F8"/>`;
  for (let i = 0; i < 22; i++) for (let j = 0; j < 12; j++) if (!(j > 6 && j < 9)) b += `<rect x="${20 + i * 72}" y="${20 + j * 74}" width="58" height="58" rx="6" fill="#E3E8EE"/>`;
  const route = (pts, col, w, dash) => `<polyline points="${pts}" fill="none" stroke="${col}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round" ${dash ? `stroke-dasharray="${dash}"` : ""}/>`;
  b += route("85,85 517,85 517,377 85,377 85,85", "#3BA55C", 9) + route("1093,85 1525,85 1525,377 1093,377", "#4E8FD9", 9) + route("589,229 1021,229 1021,377", "#F08C00", 11) + route("733,157 877,157 877,301 733,301 733,157", C.red, 13) + route("157,701 1381,701 1381,845", "#7048E8", 9, "16 12");
  b += `<circle cx="805" cy="229" r="22" fill="${C.navy}"/>` + T(805, 236, 18, "역", { a: "middle", w: 800, c: "#fff" });
  return save("patrol_net", W, H, b);
};
jobs.fleet = async () => {
  const W = 1600, H = 880;
  let b = `<rect width="${W}" height="${H}" rx="14" fill="#0D1828"/>`;
  [[30, "A 권역", "#4E8FD9"], [550, "B 권역", "#3BA55C"], [1070, "C 권역", "#F08C00"]].forEach(([x, t, col]) => {
    b += `<rect x="${x}" y="30" width="500" height="430" rx="12" fill="#132238"/>` + T(x + 24, 76, 26, t, { w: 700, c: col });
    for (let k = 0; k < 5; k++) b += `<line x1="${x + 30}" y1="${120 + k * 60}" x2="${x + 470}" y2="${120 + k * 60}" stroke="#1D2E48" stroke-width="3"/>`;
    b += `<polyline points="${x + 60},420 ${x + 60},180 ${x + 300},180 ${x + 300},300 ${x + 440},300" fill="none" stroke="${col}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>` + pv5Side(x + 150, 250, 0.42, { night: true, beacon: true, shadow: false });
  });
  b += `<rect x="30" y="490" width="1540" height="360" rx="12" fill="#132238"/>` + T(60, 542, 24, "차량별 현황 [예시]", { w: 700, c: "#fff" });
  ["차량", "권역", "순찰거리", "재확인", "배터리"].forEach((h, i) => (b += T(60 + i * 300, 600, 20, h, { c: "#7D8BA0", w: 600 })));
  [["PV5-01", "A", "24.1 km", "2곳", "71%"], ["PV5-02", "B", "18.6 km", "1곳", "83%"], ["PV5-03", "C", "31.0 km", "4곳", "58%"]].forEach((r, j) => { b += `<line x1="60" y1="${622 + j * 66}" x2="1540" y2="${622 + j * 66}" stroke="#22344F"/>`; r.forEach((v, i) => (b += T(60 + i * 300, 664 + j * 66, 24, v, { c: i === 3 ? C.amber : "#fff", w: 600 }))); });
  return save("fleet", W, H, b);
};
jobs.layers = async () => {
  const W = 1600, H = 880;
  let b = `<rect width="${W}" height="${H}" fill="#fff"/>`;
  [["보수 이력", "#C5CDD8"], ["강우", "#A9D3FF"], ["지하수", "#6CB4FF"], ["지하철 구조물", "#5B6573"], ["굴착공사", "#F08C00"], ["하수관", "#8A94A3"], ["GPR 변화 신호", C.amber]].forEach(([t, col], i) => {
    const y = 80 + i * 100;
    b += `<path d="M 260 ${y + 46} L 680 ${y} L 1280 ${y} L 860 ${y + 46} Z" fill="${col}" opacity=".92"/><path d="M 260 ${y + 46} L 860 ${y + 46} L 860 ${y + 56} L 260 ${y + 56} Z" fill="#000" opacity=".1"/>`;
    b += `<line x1="1290" y1="${y + 24}" x2="1340" y2="${y + 24}" stroke="#C5CDD8" stroke-width="2"/>` + T(1352, y + 34, 28, t, { w: 700, c: "#2B3138" });
  });
  return save("layers", W, H, b);
};
jobs.twin = async () => {
  const W = 1700, H = 900;
  let b = `<rect width="${W}" height="${H}" fill="#0A1222"/><ellipse cx="850" cy="500" rx="700" ry="300" fill="#1C3560" opacity=".35" filter="url(#b30)"/>`;
  const slab = (y, top, side, h) => `<path d="M 350 ${y} L 850 ${y - 200} L 1350 ${y} L 850 ${y + 200} Z" fill="${top}"/><path d="M 350 ${y} L 850 ${y + 200} L 850 ${y + 200 + h} L 350 ${y + h} Z" fill="${side}"/><path d="M 850 ${y + 200} L 1350 ${y} L 1350 ${y + h} L 850 ${y + 200 + h} Z" fill="${side}" opacity=".75"/>`;
  b += slab(570, "#4A3A2E", "#2A2018", 140) + `<line x1="430" y1="600" x2="1260" y2="600" stroke="#8A94A3" stroke-width="10" opacity=".6"/>`;
  b += `<ellipse cx="900" cy="618" rx="110" ry="40" fill="${C.amber}" opacity=".3" filter="url(#b14)"/><ellipse cx="900" cy="618" rx="56" ry="20" fill="${C.amber}" opacity=".85"/>` + slab(330, "#2B3442", "#1A212C", 34);
  for (let i = 0; i < 6; i++) { const x = 560 + i * 90, hh = 120 + ((i * 23) % 80); b += `<rect x="${x}" y="${300 - (i % 2) * 30 - hh}" width="56" height="${hh}" fill="#16294A" stroke="#4E8FD9" stroke-opacity=".6" stroke-width="2"/>`; }
  b += `<line x1="900" y1="380" x2="900" y2="590" stroke="${C.amber}" stroke-width="2.5" stroke-dasharray="6 6"/>`;
  return save("twin", W, H, b);
};
jobs.closing = async () => {
  const W = 1920, H = 1080;
  const d = `<linearGradient id="s2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#081329"/><stop offset=".55" stop-color="#22406E"/><stop offset=".84" stop-color="#C98E64"/><stop offset="1" stop-color="#EBC596"/></linearGradient><linearGradient id="r2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2A3446"/><stop offset="1" stop-color="#0D121B"/></linearGradient>`;
  let b = `<rect width="${W}" height="${H}" fill="url(#s2)"/><ellipse cx="960" cy="640" rx="700" ry="90" fill="#F3C48D" opacity=".45" filter="url(#b30)"/>`;
  let bx = 0, i = 0;
  while (bx < W) { const bw = 70 + ((i * 53) % 100), bh = 110 + ((i * 37) % 190); b += `<rect x="${bx}" y="${640 - bh}" width="${bw + 1}" height="${bh}" fill="${i % 2 ? "#18284A" : "#1B2D52"}"/>`; bx += bw; i++; }
  b += `<rect y="640" width="${W}" height="${H - 640}" fill="url(#r2)"/><path d="M 920 640 L 1000 640 L 1560 ${H} L 360 ${H} Z" fill="#2C3648" opacity=".9"/>`;
  for (let k = 0; k < 7; k++) { const t = k / 7, y = 650 + t * t * 420; b += `<rect x="${957 - t * 12}" y="${y}" width="${6 + t * 24}" height="${10 + t * 48}" fill="#E9EDF2" opacity=".55"/>`; }
  b += pv5Rear(820, 690, 1.4);
  return save("closing", W, H, b, d);
};
jobs.freqDepth = async () => {
  const W = 1400, H = 700;
  let b = `<rect width="${W}" height="${H}" fill="#fff"/>` + groundSection(0, 60, W, 640);
  [["저주파", 0.85, "#6CB4FF", "깊게 · 해상도 낮음"], ["중주파", 0.55, C.amber, "균형"], ["고주파", 0.3, C.red, "얕게 · 해상도 높음"]].forEach(([t, dd, col, desc], i) => {
    const x = 220 + i * 460;
    b += `<path d="M ${x - 110} 60 L ${x + 110} 60 L ${x + 50 + dd * 80} ${60 + dd * 620} L ${x - 50 - dd * 80} ${60 + dd * 620} Z" fill="${col}" opacity=".3"/>`;
    b += `<rect x="${x - 110}" y="8" width="220" height="44" rx="6" fill="${col}"/>` + T(x, 39, 24, t, { a: "middle", w: 800, c: i === 1 ? C.ink : "#fff" }) + T(x, 108, 22, desc, { a: "middle", w: 700, c: "#fff" });
  });
  const y2 = 60 + 0.32 * 640;
  b += `<line x1="0" y1="${y2}" x2="${W}" y2="${y2}" stroke="#fff" stroke-width="2.5" stroke-dasharray="12 8"/>` + T(W - 20, y2 + 34, 22, "주 대상 약 2 m 내외", { a: "end", w: 700, c: "#fff" });
  return save("freq_depth", W, H, b);
};
jobs.icons = async () => {
  const list = { cloud: Lu.LuCloud, server: Lu.LuServer, glasses: Lu.LuGlasses, radar: Lu.LuRadar, map: Lu.LuMap, cpu: Lu.LuCpu, route: Lu.LuRoute, layers: Lu.LuLayers, shield: Lu.LuShieldCheck, mic: Lu.LuMic, camera: Lu.LuCamera, scan: Lu.LuScanLine, users: Lu.LuUsers, db: Lu.LuDatabase, brain: Lu.LuBrainCircuit, monitor: Lu.LuMonitorSmartphone, wifi: Lu.LuWifi, check: Lu.LuCircleCheck, alert: Lu.LuTriangleAlert, moon: Lu.LuMoon, drive: Lu.LuHardDrive, car: Lu.LuCar, eye: Lu.LuEye };
  for (const [k, comp] of Object.entries(list)) { await icon(k, comp, "#0B1F3A"); await icon(k + "_w", comp, "#FFFFFF"); await icon(k + "_a", comp, "#F5B400"); }
};

(async () => {
  const only = process.argv.slice(2);
  for (const [k, fn] of Object.entries(jobs)) if (!only.length || only.includes(k)) await fn();
  console.log("assets done");
})();
