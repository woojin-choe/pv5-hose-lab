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
const FONT = "Noto Sans CJK KR, Pretendard, sans-serif";
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

// PV5 카고 측면(오른쪽 진행). 실차 비례: 평평한 루프, 짧은 앞 오버행, 검은 글라스 밴드, ㄱ자 라이트, 각진 휠아치
// 로컬 0..410 x 0..190, 바퀴 하단 y≈186
function pv5Side(x, y, s, o = {}) {
  const night = !!o.night;
  const body = night ? "url(#bodyNight)" : "url(#bodyDay)";
  let g = `<g transform="translate(${x},${y}) scale(${s})">`;
  if (o.shadow !== false) g += `<ellipse cx="212" cy="186" rx="210" ry="9" fill="#000" opacity="${night ? 0.65 : 0.22}" filter="url(#b6)"/>`;
  if (night) g += `<path d="M 404 112 L 660 80 L 660 176 L 404 136 Z" fill="url(#beam)" filter="url(#b6)"/>`;
  if (o.gpr) {
    g += `<rect x="10" y="150" width="6" height="22" fill="#2B3138"/><rect x="58" y="150" width="6" height="22" fill="#2B3138"/>`;
    g += `<rect x="-12" y="168" width="96" height="11" rx="2" fill="#2B3138"/><rect x="-12" y="168" width="96" height="4" rx="2" fill="#F5B400"/>`;
    if (o.waves) for (let k = 1; k <= 4; k++) g += `<path d="M ${-18 - k * 12} ${186 + k * 9} Q 36 ${198 + k * 22} ${90 + k * 12} ${186 + k * 9}" fill="none" stroke="#F5B400" stroke-width="1.6" opacity="${0.8 - k * 0.17}"/>`;
  }
  // 차체 실루엣
  g += `<path d="M 30 16 L 296 14 Q 312 14 320 24 L 372 82 Q 378 90 390 94 L 400 98 Q 408 102 408 114 L 408 156 Q 408 164 400 164 L 26 164 Q 16 164 16 154 L 16 30 Q 16 16 30 16 Z" fill="${body}"/>`;
  // 검은 루프 + 글라스 밴드(윈드실드, 1열 창)
  g += `<path d="M 30 16 L 296 14 Q 312 14 320 24 L 323 28 L 16 30 Q 16 16 30 16 Z" fill="#14181E"/>`;
  g += `<path d="M 262 28 L 322 27 L 371 84 L 262 84 Z" fill="url(#glass)"/>`;
  g += `<path d="M 300 28 L 314 28 L 290 84 L 276 84 Z" fill="#fff" opacity=".07"/>`;
  g += `<path d="M 322 27 L 372 83 Q 377 89 388 93 L 384 96 Q 372 92 366 85 L 316 28 Z" fill="#0B1018"/>`;
  g += `<path d="M 318 62 L 334 60 Q 338 60 338 64 L 338 72 Q 338 76 334 76 L 320 76 Z" fill="#0B1018"/>`;
  // ㄱ자 라이트 바(앞 모서리)
  g += `<path d="M 382 92 L 396 98 L 392 118" fill="none" stroke="${night ? "#FFF6DD" : "#F1F3F5"}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>`;
  if (night) g += `<ellipse cx="392" cy="106" rx="12" ry="18" fill="#FFF6DD" opacity=".55" filter="url(#b6)"/>`;
  // 앞 하단 검은 범퍼
  g += `<path d="M 404 124 L 408 124 L 408 156 Q 408 164 400 164 L 360 164 L 360 136 Q 380 132 404 124 Z" fill="#14181E"/>`;
  // 슬라이딩 도어 라인, 손잡이, 캐릭터 라인
  g += `<line x1="182" y1="32" x2="182" y2="134" stroke="#000" stroke-opacity=".16" stroke-width="1.2"/><line x1="262" y1="30" x2="262" y2="134" stroke="#000" stroke-opacity=".16" stroke-width="1.2"/>`;
  g += `<rect x="236" y="92" width="14" height="3.5" rx="1.7" fill="#000" opacity=".3"/><rect x="164" y="92" width="12" height="3.5" rx="1.7" fill="#000" opacity=".3"/>`;
  g += `<line x1="22" y1="86" x2="258" y2="86" stroke="#000" stroke-opacity=".07" stroke-width="1.2"/>`;
  // 하단 클래딩 + 각진 휠아치
  g += `<path d="M 16 134 L 360 134 L 360 164 L 26 164 Q 16 164 16 154 Z" fill="url(#clad)"/>`;
  for (const cx of [84, 316]) {
    g += `<path d="M ${cx - 46} 164 L ${cx - 46} 130 Q ${cx - 46} 112 ${cx - 28} 112 L ${cx + 28} 112 Q ${cx + 46} 112 ${cx + 46} 130 L ${cx + 46} 164 Z" fill="#1A1E25"/>`;
    g += `<circle cx="${cx}" cy="156" r="32" fill="#0F1216"/>`;
    g += `<circle cx="${cx}" cy="156" r="23" fill="${night ? "#3A424D" : "#5B636E"}"/>`;
    g += `<path d="M ${cx - 16} ${156 - 16} L ${cx + 16} ${156 + 16} M ${cx + 16} ${156 - 16} L ${cx - 16} ${156 + 16}" stroke="${night ? "#6B7480" : "#8C949E"}" stroke-width="4" stroke-linecap="round"/>`;
    g += `<circle cx="${cx}" cy="156" r="23" fill="none" stroke="#2A3038" stroke-width="2"/><circle cx="${cx}" cy="156" r="5" fill="#1A1E25"/>`;
  }
  // 세로 리어램프
  g += `<rect x="16" y="36" width="4" height="92" rx="2" fill="${night ? "#FF4B4B" : "#B4232A"}"/>`;
  if (night) g += `<rect x="4" y="40" width="22" height="84" rx="10" fill="#FF3B3B" opacity=".55" filter="url(#b6)"/>`;
  if (o.roof) g += `<rect x="52" y="8" width="22" height="7" rx="3" fill="#2B3138"/><ellipse cx="63" cy="7" rx="9" ry="4" fill="#E9EDF2"/><rect x="232" y="6" width="22" height="9" rx="3" fill="#2B3138"/><circle cx="249" cy="10.5" r="3" fill="#7CC4FF"/>`;
  if (o.beacon) {
    g += `<rect x="134" y="8" width="50" height="6" rx="3" fill="#F5B400"/>`;
    if (night) g += `<ellipse cx="159" cy="10" rx="40" ry="12" fill="#F5B400" opacity=".5" filter="url(#b6)"/>`;
  }
  return g + `</g>`;
}
// PV5 후면. 세로 리어램프, 검은 루프, 넓은 후면 유리. 로컬 0..200 x 0..190
function pv5Rear(x, y, s) {
  let g = `<g transform="translate(${x},${y}) scale(${s})">`;
  g += `<ellipse cx="100" cy="188" rx="112" ry="9" fill="#000" opacity=".6" filter="url(#b6)"/>`;
  g += `<rect x="16" y="150" width="32" height="36" rx="6" fill="#0F1216"/><rect x="152" y="150" width="32" height="36" rx="6" fill="#0F1216"/>`;
  g += `<path d="M 12 162 L 12 30 Q 12 14 28 14 L 172 14 Q 188 14 188 30 L 188 162 Z" fill="url(#bodyNight)"/>`;
  g += `<path d="M 28 14 L 172 14 Q 188 14 188 28 L 12 28 Q 12 14 28 14 Z" fill="#14181E"/>`;
  g += `<rect x="34" y="36" width="132" height="50" rx="5" fill="url(#glass)"/><line x1="100" y1="30" x2="100" y2="146" stroke="#000" stroke-opacity=".25" stroke-width="1.5"/>`;
  for (const lx of [14, 181]) g += `<rect x="${lx}" y="32" width="5" height="108" rx="2.5" fill="#FF4B4B"/><rect x="${lx - 10}" y="34" width="25" height="104" rx="11" fill="#FF3B3B" opacity=".55" filter="url(#b6)"/>`;
  g += `<path d="M 12 140 L 188 140 L 188 166 L 12 166 Z" fill="url(#clad)"/>`;
  g += `<rect x="40" y="168" width="120" height="8" rx="2" fill="#2B3138"/><rect x="40" y="168" width="120" height="3" rx="1" fill="#F5B400"/>`;
  g += `<rect x="74" y="8" width="52" height="6" rx="3" fill="#F5B400"/><ellipse cx="100" cy="10" rx="44" ry="11" fill="#F5B400" opacity=".45" filter="url(#b6)"/>`;
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
// 실사 사진 합성: 크롭 + 텍스트 가독성용 그라데이션
const PH = path.join(OUT, "photos");
require("fs").mkdirSync(path.join(OUT, "layers"), { recursive: true });
async function photo(name, src, w, h, o = {}) {
  let img = sharp(path.join(PH, src + ".jpg")).resize(w, h, { fit: "cover", position: o.pos || "centre" });
  if (o.gray) img = img.grayscale();
  if (o.tint) img = img.tint(o.tint);
  if (o.mod) img = img.modulate(o.mod);
  const layers = [];
  const g = o.grad;
  if (g) {
    let stops = "";
    if (g === "left") stops = `<linearGradient id="g" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#050A14" stop-opacity="${o.a || 0.9}"/><stop offset="${o.mid || 0.45}" stop-color="#050A14" stop-opacity="${(o.a || 0.9) * 0.75}"/><stop offset="${o.end || 0.75}" stop-color="#050A14" stop-opacity="0"/></linearGradient>`;
    if (g === "top") stops = `<linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#050A14" stop-opacity="${o.a || 0.85}"/><stop offset=".55" stop-color="#050A14" stop-opacity="${(o.a || 0.85) * 0.5}"/><stop offset="1" stop-color="#050A14" stop-opacity="${o.b || 0.25}"/></linearGradient>`;
    if (g === "flat") stops = `<linearGradient id="g"><stop offset="0" stop-color="#050A14" stop-opacity="${o.a || 0.4}"/><stop offset="1" stop-color="#050A14" stop-opacity="${o.a || 0.4}"/></linearGradient>`;
    layers.push({ input: Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}"><defs>${stops}</defs><rect width="${w}" height="${h}" fill="url(#g)"/></svg>`) });
  }
  if (o.overlay) layers.push({ input: Buffer.from(svg(w, h, o.overlay, o.defs || "")) });
  if (layers.length) img = sharp(await img.png().toBuffer()).composite(layers);
  await img.jpeg({ quality: 88 }).toFile(path.join(OUT, name + ".jpg"));
}

// ---- 실사 위 편집 ----
const AMB = "#F5B400", GRN = "#5AD27A";
const hud = (x, y, w, h) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="14" fill="#07101E" opacity=".8"/><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="14" fill="none" stroke="#7CC4FF" stroke-opacity=".55" stroke-width="1.5"/>`;
const warn = (W, H) => `<rect x="220" y="${H - 64}" width="${W - 440}" height="42" rx="8" fill="#3A1216" opacity=".92"/>` + T(W / 2, H - 36, 19, "GPR 기반 추정 위치입니다. 굴착 전 정밀조사와 관계기관 승인이 필요합니다.", { a: "middle", c: "#FFC9C9", w: 600 });
const bracket = (x, y, w, h, label, col = GRN) => { const L = 24; return `<path d="M ${x} ${y + L} V ${y} H ${x + L} M ${x + w - L} ${y} H ${x + w} V ${y + L} M ${x + w} ${y + h - L} V ${y + h} H ${x + w - L} M ${x + L} ${y + h} H ${x} V ${y + h - L}" stroke="${col}" stroke-width="4" fill="none"/><rect x="${x}" y="${y - 36}" width="${label.length * 19 + 26}" height="30" rx="4" fill="${col}"/>` + T(x + 12, y - 15, 18, label, { w: 700, c: "#06120A" }); };
jobs.photoEdits = async () => {
  // 표지: 실제 야간 도로 + 노면 아래 단면
  const W = 1920, H = 1080, top = 835;
  let ov = `<rect y="${top}" width="${W}" height="${H - top}" fill="#0B0D11"/>`;
  ov += `<rect y="${top}" width="${W}" height="20" fill="#2A2E35"/><rect y="${top + 20}" width="${W}" height="38" fill="#7D6E5E"/><rect y="${top + 58}" width="${W}" height="${H - top - 58}" fill="url(#soil)" opacity=".9"/>`;
  ov += `<rect y="${top}" width="${W}" height="2.5" fill="#D9DEE5" opacity=".85"/>`;
  for (let i = 0; i < 110; i++) ov += `<circle cx="${(i * 137) % W}" cy="${top + 64 + ((i * 53) % (H - top - 70))}" r="${1 + (i % 3) * 0.7}" fill="#241B14" opacity=".5"/>`;
  ov += `<rect y="${top + 108}" width="${W}" height="34" fill="#3B4048"/><rect y="${top + 108}" width="${W}" height="3" fill="#5C636D"/>`;
  ov += T(1880, top + 132, 18, "노후 하수관", { c: "#C9D0D9", w: 600, a: "end" });
  for (let k = 0; k < 8; k++) ov += `<path d="M ${1150 + k * 24} ${top + 146} q 5 9 0 13 q -5 -4 0 -13 z" fill="#7CC4FF" opacity=".75"/>`;
  const cx = 1330, cy = top + 185;
  ov += `<ellipse cx="${cx}" cy="${cy}" rx="260" ry="70" fill="${AMB}" opacity=".16" filter="url(#b30)"/>`;
  ov += `<path d="M ${cx - 190} ${cy} C ${cx - 170} ${cy - 62}, ${cx + 150} ${cy - 70}, ${cx + 200} ${cy - 6} C ${cx + 170} ${cy + 46}, ${cx - 140} ${cy + 52}, ${cx - 190} ${cy} Z" fill="#050608"/>`;
  [[120, 30, 0.45], [190, 46, 0.7], [255, 62, 0.95]].forEach(([rx, ry, op], k) => (ov += `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="none" stroke="${AMB}" stroke-width="${1.6 + k * 0.6}" stroke-dasharray="${k === 2 ? "0" : "8 7"}" opacity="${op}"/>`));
  ov += `<line x1="${cx}" y1="${top}" x2="${cx}" y2="${cy - 60}" stroke="${AMB}" stroke-width="2" stroke-dasharray="6 6" opacity=".8"/>`;
  ov += T(cx + 20, top + 80, 22, "커지는 빈 공간", { c: "#FFE7A3", w: 700 });
  await photo("ph_cover", "night_street_empty", W, H, { pos: "north", grad: "left", a: 0.88, mid: 0.38, end: 0.66, overlay: ov });

  // 7장: 새벽 골목 노면 위 GPR 스캔 구간
  let sw = `<path d="M 915 470 L 1072 470 L 1112 650 L 880 650 Z" fill="${AMB}" fill-opacity=".22" stroke="${AMB}" stroke-width="3"/>`;
  for (let k = 1; k < 6; k++) { const t = k / 6, y = 470 + t * 180, xl = 915 - t * 35, xr = 1072 + t * 40; sw += `<line x1="${xl}" y1="${y}" x2="${xr}" y2="${y}" stroke="${AMB}" stroke-width="1.5" opacity=".6"/>`; }
  sw += `<rect x="1130" y="430" width="230" height="40" rx="6" fill="${AMB}"/>` + T(1146, 458, 22, "GPR 스캔 구간", { w: 700, c: "#1A1300" });
  await photo("ph_dawn", "seoul_hapjeong", W, H, { pos: "centre", gray: true, tint: { r: 70, g: 105, b: 160 }, mod: { brightness: 0.62 }, grad: "left", a: 0.9, mid: 0.38, end: 0.62, overlay: sw });

  // 14·15장: 실제 야간 도로 위 AR 화면
  const AW = 1700, AH = 900;
  let c1 = bracket(360, 600, 180, 72, "배수구 덮개") + bracket(470, 690, 120, 200, "경계석") + bracket(560, 560, 70, 300, "차선 모서리");
  c1 += `<circle cx="450" cy="636" r="7" fill="${GRN}"/><polyline points="450,636 530,780 595,700" fill="none" stroke="${GRN}" stroke-width="2.5" stroke-dasharray="8 6"/>`;
  c1 += hud(40, 40, 460, 170) + T(68, 92, 26, "위치 보정", { w: 700, c: "#fff" }) + T(68, 136, 21, "기준점 3개 + RTK 결합", { c: "#A9D3FF" }) + T(68, 178, 22, "위치 오차 ±[실증 필요]", { w: 700, c: GRN });
  c1 += hud(AW - 500, 40, 460, 64) + T(AW - 474, 82, 21, "정차 확인됨 · 작업 모드", { c: "#fff" }) + warn(AW, AH);
  await photo("ar_calib", "night_street_empty", AW, AH, { pos: "centre", overlay: c1 });
  let c2 = `<path d="M 610 620 L 860 620 L 1280 860 L 600 860 Z" fill="${AMB}" fill-opacity=".2" stroke="${AMB}" stroke-width="4"/>`;
  for (let k = 1; k < 5; k++) { const t = k / 5, y = 620 + t * 240; c2 += `<line x1="${610 - t * 10}" y1="${y}" x2="${860 + t * 420}" y2="${y}" stroke="${AMB}" stroke-width="1.5" opacity=".55"/>`; }
  for (let k = 0; k < 4; k++) { const x0 = 650 + k * 60, x1 = 640 + k * 160; c2 += `<path d="M ${x0} 640 L ${x1} 830" stroke="#7CC4FF" stroke-width="4" stroke-dasharray="12 9"/><path d="M ${x1 - 11} 822 L ${x1 + 11} 822 L ${x1} 852 Z" fill="#7CC4FF"/>`; }
  c2 += `<circle cx="650" cy="640" r="11" fill="${GRN}"/><rect x="1100" y="810" width="22" height="22" rx="3" fill="#D93025"/>`;
  c2 += hud(40, 40, 460, 210) + T(68, 92, 26, "재탐사 3 / 4회", { w: 700, c: "#fff" }) + T(68, 134, 21, "추정 깊이 0.9–1.3 m", { c: "#A9D3FF" }) + T(68, 172, 21, "이전 대비 +17%", { c: AMB }) + T(68, 210, 21, "AI 신뢰도 84%", { c: "#A9D3FF" });
  c2 += hud(AW - 500, 40, 460, 64) + T(AW - 474, 82, 21, "음성 “이상 위치 표시”", { c: "#fff" }) + warn(AW, AH);
  await photo("ar_scan", "night_street_empty", AW, AH, { pos: "centre", overlay: c2 });

  // 4장·17장 실사
  await photo("ph_crack", "sinkhole_driveway", 1200, 900, { pos: "centre" });
  await photo("ph_patched", "sinkhole_patched", 1200, 900, { pos: "centre" });
};
// ---- PV5 GroundWatch 장착 예상도: 장비·빛 레이어(투명 PNG). 랩핑과 합성은 compose.py ----
const EQDEFS = `
  <linearGradient id="lens" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE6A0"/><stop offset=".45" stop-color="#F5B400"/><stop offset="1" stop-color="#B37800"/></linearGradient>
  <linearGradient id="lensOff" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F7D88A"/><stop offset=".5" stop-color="#E0A21A"/><stop offset="1" stop-color="#8F6200"/></linearGradient>
  <linearGradient id="blk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5A616B"/><stop offset=".35" stop-color="#2A2F36"/><stop offset="1" stop-color="#121418"/></linearGradient>
  <radialGradient id="domeG" cx=".38" cy=".3" r=".8"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".55" stop-color="#E3E7EC"/><stop offset="1" stop-color="#9AA3AE"/></radialGradient>
  <radialGradient id="lensG" cx=".35" cy=".35" r=".7"><stop offset="0" stop-color="#9FD3FF"/><stop offset=".5" stop-color="#1D4E80"/><stop offset="1" stop-color="#05101E"/></radialGradient>`;
const shadow = (cx, cy, rx, ry, op = 0.45) => `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="#000" opacity="${op}" filter="url(#b6)"/>`;
function beacon(x, y, w, lit) {
  return shadow(x + w / 2, y + 22, w * 0.55, 6, 0.5) +
    `<rect x="${x - 6}" y="${y + 12}" width="${w + 12}" height="10" rx="3" fill="url(#blk)"/>` +
    `<rect x="${x}" y="${y}" width="${w}" height="15" rx="7" fill="url(#${lit ? "lens" : "lensOff"})"/>` +
    `<rect x="${x + 8}" y="${y + 2}" width="${w - 16}" height="3" rx="1.5" fill="#FFF7DA" opacity=".85"/>` +
    [0.25, 0.5, 0.75].map((f) => `<line x1="${x + w * f}" y1="${y + 2}" x2="${x + w * f}" y2="${y + 14}" stroke="#7A5200" stroke-opacity=".35" stroke-width="1.5"/>`).join("");
}
function dome(cx, base, r) {
  return shadow(cx, base + 4, r * 1.25, 5, 0.5) + `<rect x="${cx - 5}" y="${base - 14}" width="10" height="14" fill="url(#blk)"/><ellipse cx="${cx}" cy="${base - 14}" rx="${r * 1.05}" ry="${r * 0.28}" fill="url(#blk)"/>` +
    `<path d="M ${cx - r} ${base - 16} Q ${cx - r} ${base - 16 - r * 1.15} ${cx} ${base - 16 - r * 1.15} Q ${cx + r} ${base - 16 - r * 1.15} ${cx + r} ${base - 16} Z" fill="url(#domeG)"/>`;
}
function camPod(x, y, w, h) {
  return shadow(x + w / 2, y + h + 2, w * 0.6, 4, 0.45) + `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${h * 0.3}" fill="url(#blk)"/><rect x="${x + 3}" y="${y + 2}" width="${w - 6}" height="2" rx="1" fill="#FFFFFF" opacity=".25"/><circle cx="${x + w / 2}" cy="${y + h / 2 + 1}" r="${h * 0.3}" fill="url(#lensG)"/>`;
}
function equipFront() {
  return camPod(566, 198, 72, 20) + beacon(1048, 184, 184, false) + dome(1560, 222, 26) + camPod(1086, 398, 38, 22) ;
}
function glowFront() {
  return `<ellipse cx="1140" cy="192" rx="190" ry="54" fill="#F5B400" opacity=".5" filter="url(#b30)"/><ellipse cx="1140" cy="192" rx="96" ry="14" fill="#FFD25A" opacity=".85" filter="url(#b6)"/>` + beacon(1048, 184, 184, true) +
    `<path d="M 618 640 L 790 492" stroke="#FFF6DD" stroke-width="10" stroke-linecap="round" filter="url(#b6)"/><path d="M 618 640 L 790 492" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>` ;
}
function equipRear() {
  let g = beacon(988, 120, 184, false) + dome(1450, 164, 24) + camPod(300, 142, 72, 20);
  for (const bx of [220, 500, 780]) g += `<rect x="${bx}" y="1060" width="12" height="32" fill="url(#blk)"/>`;
  g += shadow(505, 1140, 400, 16, 0.55);
  g += `<rect x="148" y="1086" width="716" height="40" rx="8" fill="url(#blk)"/>`;
  
  return g;
}
function glowRear() {
  let g = `<ellipse cx="1080" cy="128" rx="190" ry="54" fill="#F5B400" opacity=".5" filter="url(#b30)"/><ellipse cx="1080" cy="128" rx="96" ry="14" fill="#FFD25A" opacity=".85" filter="url(#b6)"/>` + beacon(988, 120, 184, true);
  for (const [x, y, w, h] of [[900, 345, 85, 370], [96, 330, 64, 340]]) g += `<rect x="${x - 25}" y="${y}" width="${w + 50}" height="${h}" rx="30" fill="#FF2A2A" opacity=".5" filter="url(#b30)"/><rect x="${x + w * 0.38}" y="${y + 24}" width="${w * 0.24}" height="${h - 48}" rx="5" fill="#FF6A6A"/>`;
  return g;
}
jobs.gwLayers = async () => {
  const W = 1920, H = 1278;
  for (const [n, b] of [["eq_front", equipFront()], ["eq_front_glow", glowFront()], ["eq_rear", equipRear()], ["eq_rear_glow", glowRear()]])
    await sharp(Buffer.from(svg(W, H, b, EQDEFS)), { density: 144 }).resize(W, H).png().toFile(path.join(OUT, "layers", n + ".png"));
};
jobs.photos = async () => {
  await photo("ph_road", "seoul_traffic_3", 1600, 900, { pos: "centre" });
  await photo("ph_closing", "seoul_traffic_1", 1920, 1080, { pos: "south", grad: "top", a: 0.93, b: 0.55, mod: { brightness: 0.8, saturation: 0.8 } });
  await photo("ph_pv5", "pv5_cargo_c", 1920, 1278, { pos: "centre" });
  await photo("ph_pv5_169", "pv5_cargo_c", 1600, 900, { pos: "centre" });
  await photo("ph_pv5_ov", "pv5_cargo_c", 1200, 840, { pos: "centre" });
  await photo("ph_pv5_rear", "pv5_cargo_d", 1600, 900, { pos: "centre" });
  await photo("ph_gpr_cart", "gpr_in_use", 1400, 1050, { pos: "centre" });
  await photo("ph_alley", "seoul_hapjeong", 1600, 900, { pos: "centre", gray: true, tint: { r: 70, g: 105, b: 160 }, mod: { brightness: 0.7 } });
};

// (preview removed)
jobs.mechanismOld = async () => {
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
jobs.map4dOld = async () => {
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
jobs.surfaceCrackOld = async () => {
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


jobs.crossCheckOld = async () => {
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
jobs.patrolNetOld = async () => {
  const W = 1600, H = 900;
  let b = `<rect width="${W}" height="${H}" fill="#F3F6F9"/><path d="M 0 520 C 300 460, 600 600, 900 520 S 1400 470, ${W} 540 L ${W} 620 C 1300 560, 1000 640, 700 600 S 200 560, 0 610 Z" fill="#CFE5F8"/>`;
  for (let i = 0; i < 22; i++) for (let j = 0; j < 12; j++) if (!(j > 6 && j < 9)) b += `<rect x="${20 + i * 72}" y="${20 + j * 74}" width="58" height="58" rx="6" fill="#E3E8EE"/>`;
  const route = (pts, col, w, dash) => `<polyline points="${pts}" fill="none" stroke="${col}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round" ${dash ? `stroke-dasharray="${dash}"` : ""}/>`;
  b += route("85,85 517,85 517,377 85,377 85,85", "#3BA55C", 9) + route("1093,85 1525,85 1525,377 1093,377", "#4E8FD9", 9) + route("589,229 1021,229 1021,377", "#F08C00", 11) + route("733,157 877,157 877,301 733,301 733,157", C.red, 13) + route("157,701 1381,701 1381,845", "#7048E8", 9, "16 12");
  b += `<circle cx="805" cy="229" r="22" fill="${C.navy}"/>` + T(805, 236, 18, "역", { a: "middle", w: 800, c: "#fff" });
  return save("patrol_net", W, H, b);
};
jobs.fleetOld = async () => {
  const W = 1600, H = 880;
  let b = `<rect width="${W}" height="${H}" rx="14" fill="#0D1828"/>`;
  [[30, "A 권역", "#4E8FD9"], [550, "B 권역", "#3BA55C"], [1070, "C 권역", "#F08C00"]].forEach(([x, t, col]) => {
    b += `<rect x="${x}" y="30" width="500" height="430" rx="12" fill="#132238"/>` + T(x + 24, 76, 26, t, { w: 700, c: col });
    for (let k = 0; k < 5; k++) b += `<line x1="${x + 30}" y1="${120 + k * 60}" x2="${x + 470}" y2="${120 + k * 60}" stroke="#1D2E48" stroke-width="3"/>`;
    b += `<polyline points="${x + 60},420 ${x + 60},180 ${x + 300},180 ${x + 300},300 ${x + 440},300" fill="none" stroke="${col}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>` + `<circle cx="${x + 300}" cy="240" r="26" fill="${col}" opacity=".25"/><circle cx="${x + 300}" cy="240" r="13" fill="${col}" stroke="#fff" stroke-width="4"/>`;
  });
  b += `<rect x="30" y="490" width="1540" height="360" rx="12" fill="#132238"/>` + T(60, 542, 24, "차량별 현황 [예시]", { w: 700, c: "#fff" });
  ["차량", "권역", "순찰거리", "재확인", "배터리"].forEach((h, i) => (b += T(60 + i * 300, 600, 20, h, { c: "#7D8BA0", w: 600 })));
  [["PV5-01", "A", "24.1 km", "2곳", "71%"], ["PV5-02", "B", "18.6 km", "1곳", "83%"], ["PV5-03", "C", "31.0 km", "4곳", "58%"]].forEach((r, j) => { b += `<line x1="60" y1="${622 + j * 66}" x2="1540" y2="${622 + j * 66}" stroke="#22344F"/>`; r.forEach((v, i) => (b += T(60 + i * 300, 664 + j * 66, 24, v, { c: i === 3 ? C.amber : "#fff", w: 600 }))); });
  return save("fleet", W, H, b);
};
jobs.layersOld = async () => {
  const W = 1600, H = 880;
  let b = `<rect width="${W}" height="${H}" fill="#fff"/>`;
  [["보수 이력", "#C5CDD8"], ["강우", "#A9D3FF"], ["지하수", "#6CB4FF"], ["지하철 구조물", "#5B6573"], ["굴착공사", "#F08C00"], ["하수관", "#8A94A3"], ["GPR 변화 신호", C.amber]].forEach(([t, col], i) => {
    const y = 80 + i * 100;
    b += `<path d="M 260 ${y + 46} L 680 ${y} L 1280 ${y} L 860 ${y + 46} Z" fill="${col}" opacity=".92"/><path d="M 260 ${y + 46} L 860 ${y + 46} L 860 ${y + 56} L 260 ${y + 56} Z" fill="#000" opacity=".1"/>`;
    b += `<line x1="1290" y1="${y + 24}" x2="1340" y2="${y + 24}" stroke="#C5CDD8" stroke-width="2"/>` + T(1352, y + 34, 28, t, { w: 700, c: "#2B3138" });
  });
  return save("layers", W, H, b);
};
jobs.twinOld = async () => {
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
jobs.freqDepthOld = async () => {
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


// ================= v3: 실지도·질감 기반 도판 =================
const fsx = require("fs");
let MAPB64 = {};
async function mapData(name) {
  if (!MAPB64[name]) {
    const buf = await sharp(path.join(OUT, "map", name + ".png")).modulate({ saturation: 0.12, brightness: 1.04 }).linear(0.82, 38).png().toBuffer();
    MAPB64[name] = "data:image/png;base64," + buf.toString("base64");
  }
  return MAPB64[name];
}
// 지도(2048x1280, 썸네일 1300 기준 좌표)를 상자에 cover로 배치하고 좌표 변환기를 돌려준다
function mapFit(x, y, w, h, zoom = 1, cx = 0.5, cy = 0.5) {
  const s = Math.max(w / 2048, h / 1280) * zoom, sw = 2048 * s, sh = 1280 * s;
  const ox = x + (w - sw) * cx, oy = y + (h - sh) * cy, k = s * (2048 / 1300);
  return { ox, oy, sw, sh, P: (px, py) => [ox + px * k, oy + py * k] };
}
const ROADS = {
  A: [[235, 268], [560, 268], [800, 270], [1160, 250]],
  B: [[800, 95], [797, 250], [790, 380]], B2: [[790, 380], [775, 480]], B3: [[775, 480], [755, 600], [725, 760]],
  C1: [[600, 430], [700, 420], [790, 440]], C2: [[790, 440], [950, 470], [1160, 470]],
  D: [[560, 600], [760, 600], [980, 568], [1150, 575]],
  F: [[300, 280], [290, 500], [275, 700]],
};
const poly = (m, pts, col, w, o = {}) => `<polyline points="${pts.map((p) => m.P(...p).join(",")).join(" ")}" fill="none" stroke="${col}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round" ${o.dash ? `stroke-dasharray="${o.dash}"` : ""} opacity="${o.op || 0.95}"/>`;
const halo = (m, pts, w) => poly(m, pts, "#FFFFFF", w + 5, { op: 0.9 });

const TEXDEFS = `
  <filter id="grainF" x="0" y="0" width="1" height="1"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="3" seed="7"/><feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.55 -0.12"/><feComposite in2="SourceGraphic" operator="in"/></filter>
  <filter id="mottleF" x="0" y="0" width="1" height="1"><feTurbulence type="fractalNoise" baseFrequency="0.006 0.02" numOctaves="4" seed="3"/><feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.9 -0.3"/><feComposite in2="SourceGraphic" operator="in"/></filter>
  <filter id="lightF" x="0" y="0" width="1" height="1"><feTurbulence type="fractalNoise" baseFrequency="0.012 0.04" numOctaves="3" seed="11"/><feColorMatrix type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.7 -0.35"/><feComposite in2="SourceGraphic" operator="in"/></filter>
  <filter id="aggF" x="0" y="0" width="1" height="1"><feTurbulence type="turbulence" baseFrequency="0.35" numOctaves="2" seed="5"/><feColorMatrix type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 -1.6 1.05"/><feComposite in2="SourceGraphic" operator="in"/></filter>`;
// 질감 있는 면: 바탕색 + 큰 얼룩 + 미세 입자 (+ 골재 반점)
function tex(x, y, w, h, base, o = {}) {
  const r = `x="${x}" y="${y}" width="${w}" height="${h}"`;
  let g = `<rect ${r} fill="${base}"/><rect ${r} fill="#000" filter="url(#mottleF)" opacity="${o.m ?? 0.5}"/><rect ${r} fill="#FFF" filter="url(#lightF)" opacity="${o.l ?? 0.25}"/><rect ${r} fill="#000" filter="url(#grainF)" opacity="${o.g ?? 0.6}"/>`;
  if (o.agg) g += `<rect ${r} fill="#FFF" filter="url(#aggF)" opacity="${o.agg}"/>`;
  return g;
}
const LBL = (x, y, t, o = {}) => `<rect x="${x - 6}" y="${y - (o.s || 20) - 4}" width="${t.length * (o.s || 20) * 0.95 + 12}" height="${(o.s || 20) + 12}" rx="3" fill="${o.bg || "#0E1726"}" opacity="${o.op || 0.82}"/>` + T(x, y, o.s || 20, t, { c: o.c || "#FFFFFF", w: 500 });

jobs.mechanism = async () => {
  const W = 1600, H = 820;
  let b = `<rect width="${W}" height="${H}" fill="#E9EDF2"/>`;
  b += tex(0, 92, W, 26, "#2C3036", { g: 0.7, agg: 0.25 });
  b += tex(0, 118, W, 44, "#8F7E6B", { agg: 0.2 });
  b += tex(0, 162, W, 658, "#6E5948", { m: 0.6 });
  b += `<path d="M 0 520 C 300 500 600 560 900 548 S 1400 590 ${W} 600 L ${W} 820 L 0 820 Z" fill="#3B5A7A" opacity=".18"/>`;
  b += `<path d="M 560 162 L 1040 162 L 860 640 Z" fill="#5A4636"/>` ;
  b += `<clipPath id="wedge"><path d="M 560 162 L 1040 162 L 860 640 Z"/></clipPath><g clip-path="url(#wedge)">${tex(540, 160, 520, 490, "#5E4A3A", { m: 0.7, g: 0.8 })}</g>`;
  b += `<path d="M 560 162 L 860 640 L 1040 162" fill="none" stroke="#1E150F" stroke-width="2.5" stroke-dasharray="10 6"/>`;
  for (const [x1, y1, x2, y2] of [[700, 260, 760, 330], [760, 330, 740, 420], [900, 240, 860, 330], [860, 330, 890, 400]]) b += `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="#1E150F" stroke-width="1.6" opacity=".7"/>`;
  b += `<rect x="0" y="232" width="${W}" height="40" fill="url(#pipeG)"/>`;
  for (let k = 0; k < 9; k++) b += `<path d="M ${640 + k * 30} 276 q 6 12 0 17 q -6 -5 0 -17 z" fill="#7CC4FF" opacity=".9"/>`;
  b += `<path d="M 600 290 C 700 330 820 300 940 340" fill="none" stroke="#7CC4FF" stroke-width="3" stroke-dasharray="4 8" opacity=".8"/>`;
  b += `<path d="M 0 520 Q 400 500 800 560 T ${W} 600" fill="none" stroke="#9FD0FF" stroke-width="3.5" stroke-dasharray="12 9"/>`;
  b += `<line x1="1380" y1="470" x2="1380" y2="578" stroke="#9FD0FF" stroke-width="4"/><path d="M 1368 574 L 1380 598 L 1392 574 Z" fill="#9FD0FF"/>`;
  b += `<rect x="0" y="686" width="${W}" height="104" rx="52" fill="url(#tunG)"/>`;
  b += LBL(40, 262, "노후 하수관 누수") + LBL(1150, 462, "지하수위 저하") + LBL(40, 746, "하부 터널 굴착") + LBL(740, 420, "쐐기형 토체", { s: 24 });
  b += LBL(24, 84, "포장층", { s: 18, bg: "#FFFFFF", c: "#2B3138", op: 0.9 });
  const d = `<linearGradient id="pipeG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8A929C"/><stop offset=".3" stop-color="#5A626C"/><stop offset="1" stop-color="#2E343B"/></linearGradient><linearGradient id="tunG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3A4048"/><stop offset=".5" stop-color="#15181C"/><stop offset="1" stop-color="#2A2F36"/></linearGradient>` + TEXDEFS;
  return save("mechanism", W, H, b, d);
};

jobs.map4d = async () => {
  const W = 1700, H = 900, md = await mapData("gangdong_z16");
  let b = `<rect width="${W}" height="${H}" rx="10" fill="#0D1828"/>` + T(32, 46, 22, "GroundWatch Cloud", { w: 700, c: "#fff" }) + T(250, 46, 18, "4D 도로 지하 변화지도 · 서울 강동구 명일동 일대", { c: "#9AA8BC" }) + T(W - 32, 46, 16, "예시 화면", { a: "end", c: "#7D8BA0" });
  const mx = 20, my = 70, mw = 1080, mh = 810, m = mapFit(mx, my, mw, mh, 1.25, 0.62, 0.45);
  b += `<clipPath id="mc"><rect x="${mx}" y="${my}" width="${mw}" height="${mh}" rx="6"/></clipPath><g clip-path="url(#mc)"><image href="${md}" x="${m.ox}" y="${m.oy}" width="${m.sw}" height="${m.sh}" preserveAspectRatio="none"/>`;
  const segs = [["A", "#3BA55C"], ["F", "#3BA55C"], ["B", "#3BA55C"], ["B2", C.red], ["B3", "#3BA55C"], ["C1", C.amber], ["C2", "#9AA3AE"], ["D", "#F08C00"]];
  for (const [k] of segs) b += halo(m, ROADS[k], 9);
  for (const [k, c] of segs) b += poly(m, ROADS[k], c, 9);
  const [rx, ry] = m.P(782, 430);
  b += `<circle cx="${rx}" cy="${ry}" r="30" fill="${C.red}" opacity=".18"/><circle cx="${rx}" cy="${ry}" r="9" fill="${C.red}" stroke="#fff" stroke-width="3"/>` + LBL(rx + 22, ry - 14, "R-0427", { s: 17 });
  b += `</g><rect x="${mx + 14}" y="${my + mh - 58}" width="900" height="44" rx="6" fill="#fff" opacity=".95"/>`;
  [["#9AA3AE", "미조사"], ["#3BA55C", "변화 없음"], [C.amber, "새 이상 신호"], ["#F08C00", "확대 의심"], [C.red, "정밀 재탐사"]].forEach(([c, t], i) => (b += `<rect x="${mx + 32 + i * 172}" y="${my + mh - 41}" width="28" height="9" rx="4" fill="${c}"/>` + T(mx + 68 + i * 172, my + mh - 30, 16, t, { c: "#2B3138", w: 500 })));
  b += T(mx + mw - 10, my + mh - 8, 11, "© OpenStreetMap contributors", { a: "end", c: "#5B6573" });
  const px = 1120, py = 70;
  b += `<rect x="${px}" y="${py}" width="560" height="810" rx="8" fill="#132238"/>` + T(px + 24, py + 40, 20, "구간 상세", { w: 700, c: "#fff" }) + T(px + 536, py + 40, 16, "R-0427", { a: "end", c: "#9AA8BC" });
  const bs = bscan(px + 24, py + 62, 512, 210, { cavity: 0.8, seed: 7, box: [0.45, 0.28, 0.42, 0.62] });
  b += bs.g + T(px + 24, py + 312, 15, "회차별 이상 반사 면적", { c: "#9AA8BC" });
  [[0, 40, "#3BA55C"], [1, 44, "#3BA55C"], [2, 62, C.amber], [3, 86, "#F08C00"], [4, 106, C.red]].forEach(([i, v, col]) => (b += `<rect x="${px + 40 + i * 100}" y="${py + 445 - v}" width="56" height="${v}" rx="3" fill="${col}"/>` + T(px + 68 + i * 100, py + 470, 14, `${i + 1}회`, { a: "middle", c: "#7D8BA0" })));
  [["마지막 조사", "최근 회차"], ["반복 조사", "5회"], ["추정 깊이", "0.9–1.3 m"], ["AI 위험점수 · 신뢰도", "높음 · 84%"], ["위치 오차", "±[실증 필요]"], ["전문가 검토", "대기"]].forEach(([k, v], i) => (b += `<line x1="${px + 24}" y1="${py + 508 + i * 46}" x2="${px + 536}" y2="${py + 508 + i * 46}" stroke="#22344F"/>` + T(px + 24, py + 539 + i * 46, 16, k, { c: "#9AA8BC" }) + T(px + 536, py + 539 + i * 46, 16, v, { a: "end", w: 700, c: i === 3 ? C.amber : "#fff" })));
  return save("map4d", W, H, b, bs.d);
};

jobs.surfaceCrack = async () => {
  const W = 700, H = 460, src = path.join(OUT, "photos", "sinkhole_driveway.jpg");
  const base = await sharp(src).resize(W, H, { fit: "cover" }).png().toBuffer();
  let ov = `<rect x="150" y="70" width="330" height="300" rx="2" fill="none" stroke="${C.amber}" stroke-width="3"/>` + LBL(156, 64, "균열 신규 · 0.86", { s: 16, bg: C.amber, c: "#1A1300", op: 1 });
  ov += `<rect x="290" y="190" width="150" height="110" rx="2" fill="none" stroke="#7CC4FF" stroke-width="3" stroke-dasharray="8 5"/>` + LBL(296, 322, "침하·단차 의심", { s: 16, bg: "#1C64B5", op: 1 });
  await sharp(base).composite([{ input: Buffer.from(svg(W, H, ov)) }]).png().toFile(path.join(OUT, "surface_crack.png"));
};

jobs.crossCheck = async () => {
  const W = 1600, H = 720;
  let b = `<rect width="${W}" height="${H}" fill="#fff"/>` + tex(0, 30, W, 660, "#3D4249", { m: 0.45, g: 0.75, agg: 0.35 });
  b += `<rect x="0" y="352" width="${W}" height="10" fill="#E8E2C8" opacity=".75" filter="url(#grainF)"/>`;
  for (let x = 40; x < W; x += 170) b += `<rect x="${x}" y="352" width="100" height="10" fill="#E8E2C8" opacity=".8"/>`;
  b += `<rect x="0" y="52" width="${W}" height="8" fill="#E9C34A" opacity=".75"/><rect x="0" y="66" width="${W}" height="8" fill="#E9C34A" opacity=".75"/>`;
  b += `<circle cx="300" cy="560" r="44" fill="#4A4F57" stroke="#23262B" stroke-width="7"/><circle cx="300" cy="560" r="30" fill="none" stroke="#23262B" stroke-width="2"/>`;
  b += `<path d="M 980 310 l 30 22 l -12 30 l 34 28 M 1010 332 l 40 -6" stroke="#1E2024" stroke-width="2.5" fill="none"/>`;
  b += `<ellipse cx="1060" cy="380" rx="90" ry="56" fill="#000" opacity=".25" filter="url(#b14)"/>`;
  for (let k = 0; k < 8; k++) b += `<rect x="0" y="${92 + k * 72}" width="${W}" height="54" fill="${C.amber}" opacity=".10"/>`;
  b += `<rect x="880" y="222" width="360" height="300" rx="4" fill="none" stroke="${C.red}" stroke-width="3.5"/>`;
  for (let k = 0; k < 6; k++) b += `<line x1="${915 + k * 58}" y1="236" x2="${915 + k * 58}" y2="508" stroke="#7CC4FF" stroke-width="4"/>`;
  for (let k = 0; k < 4; k++) b += `<line x1="894" y1="${264 + k * 70}" x2="1226" y2="${264 + k * 70}" stroke="#5AD27A" stroke-width="4" stroke-dasharray="14 8"/>`;
  b += LBL(70, 650, "차량 진행 방향 →", { s: 18 }) + LBL(1250, 240, "수동 GPR 재탐사 범위", { s: 18, bg: C.red, op: 0.95 });
  return save("cross_check", W, H, b, TEXDEFS);
};

jobs.patrolNet = async () => {
  const W = 1600, H = 900, md = await mapData("gangdong_z16"), m = mapFit(0, 0, W, H, 1.0, 0.5, 0.5);
  let b = `<image href="${md}" x="${m.ox}" y="${m.oy}" width="${m.sw}" height="${m.sh}" preserveAspectRatio="none"/>`;
  const R = [["A", "#3BA55C", 8], ["F", "#4E8FD9", 8], ["C1", "#F08C00", 10], ["C2", "#F08C00", 10], ["B2", C.red, 13], ["B", "#4E8FD9", 8], ["B3", "#4E8FD9", 8], ["D", "#7048E8", 8, "14 10"]];
  for (const [k, , w] of R) b += halo(m, ROADS[k], w);
  for (const [k, c, w, dash] of R) b += poly(m, ROADS[k], c, w, { dash });
  const [sx, sy] = m.P(790, 383);
  b += `<circle cx="${sx}" cy="${sy}" r="16" fill="#0B1F3A" stroke="#fff" stroke-width="3"/>` + LBL(sx + 22, sy + 6, "명일역", { s: 18 });
  b += T(W - 12, H - 10, 12, "© OpenStreetMap contributors", { a: "end", c: "#5B6573" });
  return save("patrol_net", W, H, b);
};

jobs.fleet = async () => {
  const W = 1600, H = 880, md = await mapData("gangdong_z15");
  let b = `<rect width="${W}" height="${H}" rx="10" fill="#0D1828"/>`;
  const mx = 30, my = 30, mw = 1540, mh = 440, m = mapFit(mx, my, mw, mh, 1.0, 0.5, 0.5);
  b += `<clipPath id="fc"><rect x="${mx}" y="${my}" width="${mw}" height="${mh}" rx="6"/></clipPath><g clip-path="url(#fc)"><image href="${md}" x="${m.ox}" y="${m.oy}" width="${m.sw}" height="${m.sh}" preserveAspectRatio="none"/>`;
  [[mx, "#4E8FD9", "A 권역"], [mx + mw / 3, "#3BA55C", "B 권역"], [mx + (2 * mw) / 3, "#F08C00", "C 권역"]].forEach(([x, c, t], i) => {
    b += `<rect x="${x}" y="${my}" width="${mw / 3}" height="${mh}" fill="${c}" opacity=".10"/><line x1="${x}" y1="${my}" x2="${x}" y2="${my + mh}" stroke="${c}" stroke-width="2" stroke-dasharray="8 6"/>` + LBL(x + 18, my + 34, t, { s: 18, bg: c, op: 0.95 });
    const vx = x + mw / 6 + (i - 1) * 40, vy = my + mh / 2 + (i % 2 ? -40 : 50);
    b += `<circle cx="${vx}" cy="${vy}" r="26" fill="${c}" opacity=".3"/><circle cx="${vx}" cy="${vy}" r="12" fill="${c}" stroke="#fff" stroke-width="4"/>` + LBL(vx + 20, vy + 6, `PV5-0${i + 1}`, { s: 15 });
  });
  b += `</g>` + T(mx + mw - 8, my + mh - 8, 11, "© OpenStreetMap contributors", { a: "end", c: "#5B6573" });
  b += `<rect x="30" y="500" width="1540" height="350" rx="8" fill="#132238"/>` + T(60, 548, 22, "차량별 현황 [예시]", { w: 700, c: "#fff" });
  ["차량", "권역", "순찰거리", "재확인", "배터리"].forEach((h, i) => (b += T(60 + i * 300, 602, 18, h, { c: "#7D8BA0", w: 500 })));
  [["PV5-01", "A", "24.1 km", "2곳", "71%"], ["PV5-02", "B", "18.6 km", "1곳", "83%"], ["PV5-03", "C", "31.0 km", "4곳", "58%"]].forEach((r, j) => { b += `<line x1="60" y1="${622 + j * 64}" x2="1540" y2="${622 + j * 64}" stroke="#22344F"/>`; r.forEach((v, i) => (b += T(60 + i * 300, 662 + j * 64, 22, v, { c: i === 3 ? C.amber : "#fff", w: 500 }))); });
  return save("fleet", W, H, b);
};

jobs.layers = async () => {
  const W = 1600, H = 880, md = await mapData("gangdong_z16");
  let b = `<rect width="${W}" height="${H}" fill="#fff"/>`;
  const Ls = [["보수 이력", "#C5CDD8"], ["강우", "#A9D3FF"], ["지하수", "#6CB4FF"], ["지하철 구조물", "#5B6573"], ["굴착공사", "#F08C00"], ["하수관", "#8A94A3"], ["GPR 변화 신호", null]];
  Ls.forEach(([t, col], i) => {
    const y = 70 + (6 - i) * 104;
    const pts = `260,${y + 50} 680,${y} 1280,${y} 860,${y + 50}`;
    if (col) b += `<polygon points="${pts}" fill="${col}" opacity=".85"/><polygon points="${pts}" fill="#000" filter="url(#grainF)" opacity=".15"/>`;
    else b += `<clipPath id="tl"><polygon points="${pts}"/></clipPath><g clip-path="url(#tl)"><image href="${md}" x="0" y="0" width="1000" height="625" preserveAspectRatio="none" transform="matrix(0.6 0 0.672 -0.08 260 ${y + 50})"/></g><polygon points="${pts}" fill="none" stroke="#0B1F3A" stroke-width="1.5"/>` +
      [[0.35, 0.45], [0.55, 0.3], [0.7, 0.6]].map(([u, v]) => { const px = 260 + u * 600 + v * 420, py = y + 50 - v * 50; return `<circle cx="${px}" cy="${py}" r="9" fill="${C.amber}" stroke="#fff" stroke-width="2"/>`; }).join("");
    b += `<path d="M 260 ${y + 50} L 860 ${y + 50} L 860 ${y + 58} L 260 ${y + 58} Z" fill="#000" opacity=".12"/>`;
    b += `<line x1="1290" y1="${y + 26}" x2="1336" y2="${y + 26}" stroke="#C5CDD8" stroke-width="1.5"/>` + T(1348, y + 35, 26, t, { w: 600, c: "#2B3138" });
  });
  return save("layers", W, H, b, TEXDEFS);
};

jobs.twin = async () => {
  const W = 1700, H = 900, md = await mapData("gangdong_z16");
  let b = `<rect width="${W}" height="${H}" fill="#0A1222"/><ellipse cx="850" cy="520" rx="720" ry="300" fill="#1C3560" opacity=".35" filter="url(#b30)"/>`;
  const side = (y, h, c1, c2) => `<path d="M 350 ${y} L 850 ${y + 200} L 850 ${y + 200 + h} L 350 ${y + h} Z" fill="${c1}"/><path d="M 850 ${y + 200} L 1350 ${y} L 1350 ${y + h} L 850 ${y + 200 + h} Z" fill="${c2}"/>`;
  // 지하 블록
  b += side(560, 150, "#3A2C22", "#2A2018");
  b += `<clipPath id="sl"><path d="M 350 560 L 850 760 L 850 910 L 350 710 Z"/></clipPath><g clip-path="url(#sl)">${tex(340, 540, 520, 380, "#4A382B", { m: 0.6 })}</g>`;
  b += `<path d="M 350 560 L 850 360 L 1350 560 L 850 760 Z" fill="#4A3A2E"/>`;
  b += `<line x1="430" y1="590" x2="1270" y2="590" stroke="#8A94A3" stroke-width="12" opacity=".55"/>`;
  b += `<ellipse cx="900" cy="612" rx="120" ry="42" fill="${C.amber}" opacity=".35" filter="url(#b14)"/><ellipse cx="900" cy="612" rx="56" ry="20" fill="${C.amber}" opacity=".9"/>`;
  // 지상 지도 슬래브
  b += side(330, 30, "#1E2633", "#161C26");
  b += `<clipPath id="ts"><path d="M 350 330 L 850 130 L 1350 330 L 850 530 Z"/></clipPath><g clip-path="url(#ts)"><image href="${md}" x="0" y="0" width="1000" height="1000" preserveAspectRatio="xMidYMid slice" transform="matrix(0.5 -0.2 0.5 0.2 350 330)"/><path d="M 350 330 L 850 130 L 1350 330 L 850 530 Z" fill="#0B1F3A" opacity=".18"/></g>`;
  b += `<path d="M 350 330 L 850 130 L 1350 330 L 850 530 Z" fill="none" stroke="#7CC4FF" stroke-opacity=".6" stroke-width="1.5"/>`;
  b += `<line x1="900" y1="345" x2="900" y2="600" stroke="${C.amber}" stroke-width="2.5" stroke-dasharray="6 6"/><circle cx="900" cy="345" r="8" fill="${C.amber}" stroke="#fff" stroke-width="2"/>`;
  b += LBL(1380, 330, "지상 · 도로 지도", { s: 20 }) + LBL(1380, 610, "지하 · 공동 의심 신호", { s: 20 }) + T(W - 16, H - 12, 12, "© OpenStreetMap contributors", { a: "end", c: "#7D8BA0" });
  return save("twin", W, H, b, TEXDEFS);
};

jobs.freqDepth = async () => {
  const W = 1400, H = 700;
  let b = `<rect width="${W}" height="${H}" fill="#fff"/>` + tex(0, 60, W, 22, "#2C3036", { agg: 0.25 }) + tex(0, 82, W, 40, "#8F7E6B", { agg: 0.2 }) + tex(0, 122, W, 578, "#6E5948", { m: 0.6 });
  [["저주파", 0.85, "#6CB4FF", "깊게 · 해상도 낮음"], ["중주파", 0.55, C.amber, "균형"], ["고주파", 0.3, C.red, "얕게 · 해상도 높음"]].forEach(([t, dd, col, desc], i) => {
    const x = 220 + i * 460;
    b += `<path d="M ${x - 110} 60 L ${x + 110} 60 L ${x + 50 + dd * 80} ${60 + dd * 620} L ${x - 50 - dd * 80} ${60 + dd * 620} Z" fill="${col}" opacity=".32"/><path d="M ${x - 110} 60 L ${x - 50 - dd * 80} ${60 + dd * 620} M ${x + 110} 60 L ${x + 50 + dd * 80} ${60 + dd * 620}" stroke="${col}" stroke-width="2" opacity=".8"/>`;
    b += `<rect x="${x - 110}" y="10" width="220" height="40" rx="4" fill="${col}"/>` + T(x, 38, 22, t, { a: "middle", w: 700, c: i === 1 ? C.ink : "#fff" }) + LBL(x - 95, 160, desc, { s: 18 });
  });
  const y2 = 60 + 0.32 * 640;
  b += `<line x1="0" y1="${y2}" x2="${W}" y2="${y2}" stroke="#fff" stroke-width="2.5" stroke-dasharray="12 8"/>` + LBL(W - 250, y2 + 36, "주 대상 약 2 m 내외", { s: 18 });
  return save("freq_depth", W, H, b, TEXDEFS);
};

(async () => {
  const only = process.argv.slice(2);
  for (const [k, fn] of Object.entries(jobs)) if (!k.endsWith("Old") && (!only.length || only.includes(k))) await fn();
  console.log("assets done");
})();
