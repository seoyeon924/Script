// ═══════════════════════════════════════════════
// AVENGERS CHARACTER NETWORK — Tableau Viz Extension
// Dual-mode: Tableau Extension + Standalone
// ═══════════════════════════════════════════════

// ── Tableau Detection ──
const IS_TABLEAU = (typeof tableau !== 'undefined' && tableau.extensions);

// ── Settings Multipliers ──
const settings = {
  lineWidth: 1,
  lineOpacity: 1,
  nodeSize: 1,
  labelSize: 1,
  bgBrightness: 0.7
};

// ── Data (populated from Tableau or fallback) ──
let nodes = [];
let links = [];
let faceImages = { ...FACE_IMAGES };
let facePositions = { ...FACE_POSITIONS };
let groupColors = { ...GROUP_COLORS };
const groupOrder = GROUP_ORDER;
let nodeMap = {};
let maxStrength = 10;   // 데이터별 strength 최대값 (굵기 정규화용 — 다른 데이터에서도 굵기 차이 일정)
const imageLoaded = {};

// ── Color helper: lighten a hex color for stroke ──
function lightenColor(hex, amount) {
  if (amount === undefined) amount = 0.3;
  hex = hex.replace('#', '');
  if (hex.length === 3) hex = hex[0]+hex[0]+hex[1]+hex[1]+hex[2]+hex[2];
  const r = parseInt(hex.slice(0,2), 16);
  const g = parseInt(hex.slice(2,4), 16);
  const b = parseInt(hex.slice(4,6), 16);
  const nr = Math.min(255, Math.round(r + (255 - r) * amount));
  const ng = Math.min(255, Math.round(g + (255 - g) * amount));
  const nb = Math.min(255, Math.round(b + (255 - b) * amount));
  return '#' + nr.toString(16).padStart(2,'0') + ng.toString(16).padStart(2,'0') + nb.toString(16).padStart(2,'0');
}

// Auto-generate group colors for unknown groups
const AUTO_PALETTE = [
  '#3a7bd5','#c96a1e','#1d8a4e','#1a8fa0','#7e3db8',
  '#4a4e5a','#b82a2a','#5a5a5a','#d4a017','#2e8b57',
  '#8b4513','#6a5acd','#cd5c5c','#20b2aa','#daa520'
];
let _autoPaletteIdx = 0;

function ensureGroupColor(group) {
  if (!groupColors[group]) {
    const base = AUTO_PALETTE[_autoPaletteIdx % AUTO_PALETTE.length];
    _autoPaletteIdx++;
    groupColors[group] = { fill: base, stroke: lightenColor(base) };
  }
}

// ── Parse Tableau flat rows → nodes[] + links[] ──
function parseNetworkData(rows) {
  const nodeSet = {};
  const linkList = [];
  const dynamicImages = {};

  rows.forEach(row => {
    const src = row.Source;
    const tgt = row.Target;
    if (!src || !tgt) return; // Skip rows without Source/Target

    const rawStrength = +row.Strength;
    const strength = isNaN(rawStrength) || rawStrength <= 0 ? 5 : rawStrength;
    const type = row.Type || 'ally';

    // Validate time format (mm:ss or m:ss)
    function safeTime(t) {
      if (!t || typeof t !== 'string') return '0:00';
      if (/^\d{1,3}:\d{2}$/.test(t.trim())) return t.trim();
      return '0:00';
    }

    if (!nodeSet[src]) {
      nodeSet[src] = {
        id: src,
        name: row.Source_Name || src.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase()),
        group: row.Source_Group || 'Default',
        importance: Math.max(1, +row.Source_Importance || 1),
        time: safeTime(row.Source_Time)
      };
    }
    if (!nodeSet[tgt]) {
      nodeSet[tgt] = {
        id: tgt,
        name: row.Target_Name || tgt.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase()),
        group: row.Target_Group || 'Default',
        importance: Math.max(1, +row.Target_Importance || 1),
        time: safeTime(row.Target_Time)
      };
    }

    // Optional: image URLs from data (http URL은 그대로, images/.. 상대경로는 프로젝트 루트 기준 해석)
    { const u = resolveImageUrl(row.Source_Image); if (u) dynamicImages[src] = u; }
    { const u = resolveImageUrl(row.Target_Image); if (u) dynamicImages[tgt] = u; }

    linkList.push({ source: src, target: tgt, strength, type });
  });

  return {
    nodes: Object.values(nodeSet),
    links: linkList,
    images: dynamicImages
  };
}

// ── Normalize Tableau field name → expected column name ──
function normalizeFieldName(name) {
  // Strip aggregation wrappers: SUM(...), 합계(...), AGG(...), ATTR(...), etc.
  let n = name.replace(/^[A-Za-z가-힣]+\((.+)\)$/, '$1');
  // Replace spaces with underscores
  n = n.replace(/ /g, '_');
  return n;
}

// ── Clean Tableau cell value (handle nulls and empty) ──
function cleanValue(v) {
  if (v === null || v === undefined) return '';
  if (typeof v === 'string') {
    const lc = v.toLowerCase().trim();
    if (lc === 'null' || lc === '%null%' || lc === '' || lc === 'undefined') return '';
  }
  return v;
}

// ── Load data from Tableau worksheet ──
async function loadDataFromTableau() {
  try {
    const worksheetContent = tableau.extensions.worksheetContent;
    const worksheet = worksheetContent.worksheet;

    const dataReader = await worksheet.getSummaryDataReaderAsync();
    const rows = [];

    // Read all pages (not just page 0)
    for (let p = 0; p < dataReader.pageCount; p++) {
      const page = await dataReader.getPageAsync(p);
      const columns = page.columns;

      if (p === 0) {
        console.log('Tableau columns:', columns.map(c => c.fieldName));
        console.log('Normalized:', columns.map(c => normalizeFieldName(c.fieldName)));
      }

      for (let r = 0; r < page.data.length; r++) {
        const row = {};
        columns.forEach((col, i) => {
          const normalized = normalizeFieldName(col.fieldName);
          row[normalized] = cleanValue(page.data[r][i].formattedValue);
        });
        rows.push(row);
      }
    }

    await dataReader.releaseAsync();
    if (rows.length > 0) {
      console.log('First row keys:', Object.keys(rows[0]));
      console.log('First row values:', rows[0]);
    }
    return rows;
  } catch (e) {
    console.warn('Tableau data load failed:', e);
    return null;
  }
}

// ═══════════════════════════════════════════════
// STATE
// ═══════════════════════════════════════════════
let W = window.innerWidth;
let H = window.innerHeight;
let selectedId = "thanos";
let positions = {};
let isTransitioning = false;
let isInitialState = true;
let _firstSelection = true;
let activeFilter = "all";
let activeGroupFilter = "all";
let _snapPositions = false;
let _bounceSize = false;
let _staggerLines = false;
let _animateConnectedLines = false;
let hoveredId = null;
let _spinRotationRad = 0;
let _prevSelectedForSnap = null;

// ── Derived data (recomputed on data change) ──
let circleOrder = [];

function rebuildDerivedData() {
  nodeMap = {};
  nodes.forEach(n => nodeMap[n.id] = n);
  // Ensure all groups have colors
  nodes.forEach(n => ensureGroupColor(n.group));
  // Add unknown groups to groupOrder dynamically
  const knownGroups = new Set(groupOrder);
  nodes.forEach(n => {
    if (!knownGroups.has(n.group)) {
      groupOrder.push(n.group);
      knownGroups.add(n.group);
    }
  });
  circleOrder = [...nodes].sort((a, b) => {
    const ga = groupOrder.indexOf(a.group);
    const gb = groupOrder.indexOf(b.group);
    if (ga !== gb) return ga - gb;
    return b.importance - a.importance;
  });
}

// 이미지 경로 해석: http(s)·절대·data URI는 그대로, 상대경로(images/..)는
// 확장 폴더(tableau-extension/) 기준 한 단계 위(프로젝트 루트)로 해석 → localhost:8080/images/..
function resolveImageUrl(u) {
  if (!u || typeof u !== 'string') return null;
  u = u.trim();
  if (!u) return null;
  if (/^(https?:\/\/|\/|data:)/i.test(u)) return u;        // 절대 URL은 그대로
  try { return new URL('../' + u.replace(/^\.\//, ''), location.href).href; }
  catch (_) { return '../' + u.replace(/^\.\//, ''); }
}

// Apply dynamic images and colors from parsed data
function applyDynamicData(parsed) {
  // 이미지는 데이터의 이미지 URL(Source_Image/Target_Image)이 있을 때만 표시.
  // 없으면 내장 기본 사진을 쓰지 않고 비움 → 다른 데이터에서 어벤져스 사진이 뜨는 것 방지.
  faceImages = (parsed.images && Object.keys(parsed.images).length > 0) ? parsed.images : {};
}

// ═══════════════════════════════════════════════
// HELPERS
// ═══════════════════════════════════════════════
function getConnections(nodeId) {
  const conns = [];
  links.forEach(l => {
    if (l.source === nodeId && nodeMap[l.target]) {
      conns.push({ node: nodeMap[l.target], strength: l.strength || 5, type: l.type || 'ally' });
    } else if (l.target === nodeId && nodeMap[l.source]) {
      conns.push({ node: nodeMap[l.source], strength: l.strength || 5, type: l.type || 'ally' });
    }
  });
  return conns;
}

function nodeRadius(d, isSelected) {
  const m = settings.nodeSize;
  if (isSelected) return Math.min(W, H) * 0.038 * m;
  return Math.min(W, H) * 0.013 * m;
}

// ═══════════════════════════════════════════════
// LAYOUT CALCULATION
// ═══════════════════════════════════════════════
function getFilteredNodeIds(filterType, groupFilter) {
  let ids;
  if (filterType === "all") {
    ids = new Set(nodes.map(n => n.id));
  } else {
    ids = new Set();
    links.forEach(l => {
      if (l.type === filterType) { ids.add(l.source); ids.add(l.target); }
    });
  }
  if (groupFilter && groupFilter !== "all") {
    const groupIds = new Set(nodes.filter(n => n.group === groupFilter).map(n => n.id));
    ids = new Set([...ids].filter(id => groupIds.has(id)));
  }
  return ids;
}

function calculateLayout(selId) {
  const pos = {};
  const padding = Math.min(W, H) * 0.16;
  const conns = getConnections(selId);
  const connIds = new Set(conns.map(c => c.node.id));
  const connMap = {};
  conns.forEach(c => { connMap[c.node.id] = c; });

  const filteredIds = getFilteredNodeIds(activeFilter, activeGroupFilter);
  filteredIds.add(selId);

  const visibleOrder = circleOrder.filter(n => filteredIds.has(n.id));
  const N = visibleOrder.length;

  const portrait = H > W * 1.2;
  let R, cx, cy;
  if (portrait) {
    R = (W / 2) - padding;
    cx = W / 2;
    cy = H * 0.38;
  } else {
    R = (H / 2) - padding;
    cy = H / 2;
    cx = W * 0.2 + R;
    cx = Math.max(cx, padding + R);
    cx = Math.min(cx, W - padding - R);
  }
  pos._center = { x: cx, y: cy };
  pos._R = R;
  pos._portrait = portrait;
  pos._visibleIds = filteredIds;

  const selIdx = visibleOrder.findIndex(n => n.id === selId);
  const slotAngle = N > 0 ? (2 * Math.PI) / N : 0;

  visibleOrder.forEach((n, i) => {
    const isConn = connIds.has(n.id);
    const relIdx = ((i - selIdx) + N) % N;
    const angle = Math.PI + relIdx * slotAngle;

    pos[n.id] = {
      x: cx + Math.cos(angle) * R,
      y: cy + Math.sin(angle) * R,
      connected: isConn,
      strength: isConn ? connMap[n.id].strength : 0,
      type: isConn ? connMap[n.id].type : null,
      selected: n.id === selId
    };
  });

  circleOrder.forEach(n => {
    if (!filteredIds.has(n.id)) {
      pos[n.id] = {
        x: cx, y: cy,
        connected: false, strength: 0, type: null,
        hidden: true
      };
    }
  });

  return pos;
}

// ═══════════════════════════════════════════════
// SVG SETUP
// ═══════════════════════════════════════════════
const svg = d3.select("#viz").attr("width", W).attr("height", H);
const defs = svg.append("defs");

// Background
const bgGrad = defs.append("radialGradient").attr("id","bg-grad")
  .attr("cx","50%").attr("cy","48%").attr("r","60%");
bgGrad.append("stop").attr("offset","0%").attr("stop-color","#000000");
bgGrad.append("stop").attr("offset","100%").attr("stop-color","#000000");
svg.append("rect").attr("width",W).attr("height",H).attr("fill","url(#bg-grad)").attr("opacity", 0.4);

// Glow filters
const glowSmall = defs.append("filter").attr("id","glow-sm").attr("x","-80%").attr("y","-80%").attr("width","260%").attr("height","260%");
glowSmall.append("feGaussianBlur").attr("stdDeviation","3").attr("result","b");
glowSmall.append("feMerge").selectAll("feMergeNode").data(["b","SourceGraphic"]).enter().append("feMergeNode").attr("in",d=>d);

const glowBig = defs.append("filter").attr("id","glow-lg").attr("x","-100%").attr("y","-100%").attr("width","300%").attr("height","300%");
glowBig.append("feGaussianBlur").attr("stdDeviation","8").attr("result","b");
glowBig.append("feMerge").selectAll("feMergeNode").data(["b","SourceGraphic"]).enter().append("feMergeNode").attr("in",d=>d);

// Conflict glow filter
const glowConflict = defs.append("filter").attr("id","glow-conflict").attr("x","-50%").attr("y","-50%").attr("width","200%").attr("height","200%");
glowConflict.append("feGaussianBlur").attr("in","SourceGraphic").attr("stdDeviation","4").attr("result","blur");
glowConflict.append("feFlood").attr("flood-color","#950606").attr("flood-opacity","0.6").attr("result","color");
glowConflict.append("feComposite").attr("in","color").attr("in2","blur").attr("operator","in").attr("result","glow");
const glowConflictMerge = glowConflict.append("feMerge");
glowConflictMerge.append("feMergeNode").attr("in","glow");
glowConflictMerge.append("feMergeNode").attr("in","SourceGraphic");

// Line glow filters per relationship type
function makeLineGlow(id, color, stdDev, opacity) {
  const f = defs.append("filter").attr("id", id)
    .attr("x","-60%").attr("y","-60%").attr("width","220%").attr("height","220%");
  f.append("feGaussianBlur").attr("in","SourceGraphic").attr("stdDeviation", stdDev).attr("result","blur1");
  f.append("feFlood").attr("flood-color", color).attr("flood-opacity", opacity).attr("result","color1");
  f.append("feComposite").attr("in","color1").attr("in2","blur1").attr("operator","in").attr("result","glow1");
  f.append("feGaussianBlur").attr("in","SourceGraphic").attr("stdDeviation", stdDev * 0.4).attr("result","blur2");
  const mg = f.append("feMerge");
  mg.append("feMergeNode").attr("in","glow1");
  mg.append("feMergeNode").attr("in","blur2");
  mg.append("feMergeNode").attr("in","SourceGraphic");
}
makeLineGlow("glow-line-ally", "#00c8ff", 7, 0.55);
makeLineGlow("glow-line-enemy", "#ff2020", 8, 0.6);
makeLineGlow("glow-line-romantic", "#c040ff", 7, 0.55);
makeLineGlow("glow-line-family", "#c0c8d0", 6, 0.5);

// Node gradients — built dynamically
function buildNodeGradients() {
  // Remove old gradients
  defs.selectAll("radialGradient[id^='grad-']").remove();
  Object.entries(groupColors).forEach(([group, colors]) => {
    const grad = defs.append("radialGradient").attr("id", `grad-${group.replace(/\s/g,'')}`)
      .attr("cx","35%").attr("cy","35%").attr("r","65%");
    grad.append("stop").attr("offset","0%").attr("stop-color", colors.stroke);
    grad.append("stop").attr("offset","100%").attr("stop-color", colors.fill);
  });
}
buildNodeGradients();

// SVG cloud shapes at bottom
const cloudGroup = svg.append("g").attr("class","clouds").style("opacity", 0.5);
function addCloud(cx, cy, rx, ry, opacity) {
  cloudGroup.append("ellipse").attr("cx",cx).attr("cy",cy).attr("rx",rx).attr("ry",ry)
    .attr("fill","#000000").attr("filter","url(#glow-lg)").style("opacity", opacity);
}
function rebuildClouds() {
  cloudGroup.selectAll("*").remove();
  if (IS_TABLEAU) return; // Skip blur-heavy clouds in Tableau for performance
  addCloud(W*0.15, H*0.92, W*0.25, 60, 0.6);
  addCloud(W*0.5, H*0.95, W*0.35, 80, 0.5);
  addCloud(W*0.8, H*0.9, W*0.2, 50, 0.55);
  addCloud(W*0.35, H*0.88, W*0.15, 40, 0.4);
  addCloud(W*0.7, H*0.96, W*0.3, 70, 0.45);
}
rebuildClouds();

const mainGroup = svg.append("g");
const linkGroup = mainGroup.append("g").attr("class","links");
const nodeGroup = mainGroup.append("g").attr("class","nodes");
const labelGroup = mainGroup.append("g").attr("class","labels");

// ═══════════════════════════════════════════════
// CURVED LINE GENERATOR
// ═══════════════════════════════════════════════
function makeCurve(sx, sy, tx, ty) {
  const dx = tx - sx, dy = ty - sy;
  const dist = Math.sqrt(dx*dx + dy*dy);
  if (dist < 1) return `M${sx},${sy}L${tx},${ty}`;

  const nx = -dy / dist, ny = dx / dist;
  const curvature = dist * 0.18;
  const mx = (sx + tx) / 2 + nx * curvature;
  const my = (sy + ty) / 2 + ny * curvature;

  return `M${sx},${sy} Q${mx},${my} ${tx},${ty}`;
}

// ═══════════════════════════════════════════════
// TEXT ROTATION HELPER
// ═══════════════════════════════════════════════
function getTextAttrs(nx, ny, cx, cy, radius) {
  const dx = nx - cx, dy = ny - cy;
  const angle = Math.atan2(dy, dx);
  const deg = angle * 180 / Math.PI;
  const offset = radius + 10;
  const tx = nx + Math.cos(angle) * offset;
  const ty = ny + Math.sin(angle) * offset;

  let rot, anchor;
  if (deg > -90 && deg < 90) {
    rot = deg; anchor = "start";
  } else {
    rot = deg + 180; anchor = "end";
  }
  return { x: tx, y: ty, rotation: rot, anchor };
}

// ═══════════════════════════════════════════════
// PROXIMITY HOVER SYSTEM
// ═══════════════════════════════════════════════
function highlightNode(id, pageX, pageY) {
  if (id === selectedId) return;
  const d = nodeMap[id];
  if (!d) return;
  hoveredId = id;

  const tt = document.getElementById("tooltip");
  const gc = groupColors[d.group] || { stroke: '#888' };
  tt.innerHTML = `<div class="tt-name">${d.name}</div>
    <div class="tt-group" style="color:${gc.stroke}">${d.group}</div>
    <div class="tt-time">Screen time: ${d.time}</div>`;
  tt.classList.add("visible");
  if (pageX != null) {
    tt.style.left = (pageX + 16) + "px";
    tt.style.top = (pageY - 8) + "px";
  }

  const nodeEl = nodeGroup.selectAll("g.node").filter(n => n.id === id);
  nodeEl.select(".body").transition("hover").duration(60)
    .attr("stroke", "#ffffff").attr("stroke-width", 2)
    .attr("filter", "url(#glow-lg)");
  nodeEl.transition("hover").duration(60)
    .style("opacity", 1);

  labelGroup.selectAll("text.label").filter(l => l.id === id)
    .transition("hover").duration(80)
    .attr("fill", "#ffffff")
    .attr("font-weight", "700")
    .attr("letter-spacing", "4px")
    .style("opacity", 1)
    .style("text-shadow", "0 0 12px rgba(255,255,255,.35), 0 0 25px rgba(255,255,255,.15), 0 0 6px rgba(255,255,255,.4)");
}

function unhighlightNode(id) {
  if (!id) return;
  const d = nodeMap[id];
  if (!d || id === selectedId) return;
  hoveredId = null;

  document.getElementById("tooltip").classList.remove("visible");

  const conns = getConnections(selectedId);
  const isConn = conns.some(c => c.node.id === id);
  const allSmall = isInitialState;

  const nodeEl = nodeGroup.selectAll("g.node").filter(n => n.id === id);
  nodeEl.select(".body").transition("hover").duration(150)
    .attr("stroke", allSmall ? "rgba(255,255,255,0.3)" : (isConn ? "rgba(255,255,255,0.5)" : "rgba(255,255,255,0.2)"))
    .attr("stroke-width", allSmall ? 1.5 : 0.8)
    .attr("filter", "url(#glow-sm)");
  nodeEl.transition("hover").duration(150)
    .style("opacity", allSmall ? 0.9 : (isConn ? 0.95 : 0.4));

  labelGroup.selectAll("text.label").filter(l => l.id === id)
    .transition("hover").duration(150)
    .attr("fill", allSmall ? "#ffffff" : (isConn ? "#ffffff" : "#999"))
    .attr("font-weight", allSmall ? (d.importance >= 6 ? "600" : "400") : (isConn ? (d.importance >= 6 ? "700" : "600") : "400"))
    .attr("letter-spacing", allSmall ? "2px" : (isConn ? "2.5px" : "2px"))
    .style("opacity", allSmall ? 1 : (isConn ? 1 : 0.55))
    .style("text-shadow", allSmall
      ? "0 0 12px rgba(0,0,0,1), 0 0 30px rgba(0,0,0,.9), 0 0 50px rgba(0,0,0,.7)"
      : (isConn
        ? "0 0 20px rgba(255,255,255,.15), 0 0 40px rgba(0,0,0,.9)"
        : "0 0 16px rgba(0,0,0,.95)"));
}

// ═══════════════════════════════════════════════
// RENDER / UPDATE
// ═══════════════════════════════════════════════
function render(selId, animate) {
  if (!selId || !nodeMap[selId]) return;
  positions = calculateLayout(selId);
  const selPos = positions[selId];
  const selNode = nodeMap[selId];
  const conns = getConnections(selId);
  const connIds = new Set(conns.map(c => c.node.id));
  const dur = animate ? (IS_TABLEAU ? 180 : 350) : 0;
  const ease = d3.easeExpOut;
  const shouldSnap = _snapPositions;

  document.getElementById("click-hint").style.opacity = "0";

  // ── All relationship links ──
  const visibleIds = positions._visibleIds || new Set(nodes.map(n => n.id));
  const allLinkData = links.map(l => ({
    id: `${l.source}-${l.target}`,
    sourceId: l.source,
    targetId: l.target,
    strength: l.strength,
    type: l.type,
    visible: visibleIds.has(l.source) && visibleIds.has(l.target) &&
             (activeFilter === "all" || l.type === activeFilter)
  }));

  // 데이터별 strength 최대값으로 정규화 → 다른 데이터(스타워즈 등)에서도 굵기 차이가 일정
  maxStrength = d3.max(allLinkData, d => +d.strength) || 10;
  if (maxStrength < 1) maxStrength = 1;

  const linkSel = linkGroup.selectAll("path.link").data(allLinkData, d => d.id);
  linkSel.exit().transition().duration(dur/2).attr("stroke-opacity", 0).remove();

  const linkEnter = linkSel.enter().append("path").attr("class","link")
    .attr("fill","none")
    .attr("stroke-linecap","round")
    .attr("stroke-opacity", 0);

  const linkMerge = linkEnter.merge(linkSel);

  function linkWidth(d) {
    if (!d.visible) return 0;
    const m = settings.lineWidth;
    const s = isNaN(d.strength) ? 5 : d.strength;
    const ns = s / maxStrength;   // 0~1 정규화 (데이터 무관 일정한 굵기)
    if (isInitialState) return (0.02 + Math.pow(ns, 3.5) * 5) * m;
    const isSel = d.sourceId === selId || d.targetId === selId;
    if (isSel) return (0.5 + Math.pow(ns, 2) * 2) * m;
    // Background lines: subtle but visible
    return (0.15 + Math.pow(ns, 2) * 0.6) * m;
  }
  function linkOpacity(d) {
    if (!d.visible) return 0;
    const m = settings.lineOpacity;
    const s = isNaN(d.strength) ? 5 : d.strength;
    const ns = s / maxStrength;
    if (isInitialState) return Math.min(1, (0.06 + ns * 0.6) * m);
    const isSel = d.sourceId === selId || d.targetId === selId;
    if (isSel) return Math.min(1, (0.6 + Math.pow(ns, 2) * 0.4) * m);
    // Background lines: subtle but visible
    return Math.min(1, (0.04 + Math.pow(ns, 2) * 0.1) * m);
  }
  function linkFilter() { return null; }

  if (shouldSnap) {
    linkMerge.interrupt("link-style").interrupt("link-dash").interrupt("line-grow")
      .attr("d", d => {
        const sp = positions[d.sourceId];
        const tp = positions[d.targetId];
        return makeCurve(sp.x, sp.y, tp.x, tp.y);
      })
      .attr("stroke", "#ffffff")
      .attr("stroke-width", linkWidth)
      .attr("stroke-opacity", linkOpacity)
      .attr("stroke-dasharray", null)
      .attr("filter", linkFilter);
  } else {
    linkMerge.each(function(d) {
      const el = d3.select(this);
      const isSel = d.sourceId === selId || d.targetId === selId;
      const sp = positions[d.sourceId];
      const tp = positions[d.targetId];
      const path = makeCurve(sp.x, sp.y, tp.x, tp.y);

      if (isSel && _animateConnectedLines) {
        el.interrupt("link-style")
          .attr("d", path)
          .attr("stroke", "#ffffff")
          .attr("stroke-width", linkWidth(d))
          .attr("stroke-opacity", 0)
          .attr("filter", null);
      } else {
        el.transition("link-style").duration(120).ease(ease)
          .attr("d", path)
          .attr("stroke", "#ffffff")
          .attr("stroke-width", linkWidth(d))
          .attr("stroke-opacity", linkOpacity(d))
          .attr("filter", null);
      }
    });
  }

  // Line draw animation
  if (animate && _staggerLines) {
    let lineIdx = 0;
    linkMerge.each(function(d) {
      if (!d.visible) { d3.select(this).attr("stroke-opacity", 0); return; }
      const isSelected = d.sourceId === selId || d.targetId === selId;
      const str = isNaN(d.strength) ? 5 : d.strength;
      const targetOpacity = isSelected ? 0.7 + Math.pow(str / 10, 2) * 0.3 : 0.04 + Math.pow(str / 10, 2) * 0.1;
      const length = 1200;
      d3.select(this).interrupt("link-style").interrupt("link-dash")
        .attr("stroke-opacity", 0)
        .attr("stroke-dasharray", length)
        .attr("stroke-dashoffset", length)
        .transition("link-dash").delay(lineIdx * 3).duration(60).ease(d3.easeLinear)
        .attr("stroke-opacity", targetOpacity)
        .attr("stroke-dashoffset", 0)
        .on("end", function() { d3.select(this).attr("stroke-dasharray", null); });
      lineIdx++;
    });
    _staggerLines = false;
  } else if (animate) {
    linkEnter.each(function() {
      const length = 1200;
      d3.select(this)
        .attr("stroke-dasharray", length)
        .attr("stroke-dashoffset", length)
        .transition("link-dash").delay(0).duration(60).ease(d3.easeLinear)
        .attr("stroke-dashoffset", 0)
        .on("end", function() { d3.select(this).attr("stroke-dasharray", null); });
    });
  }

  // ── Connected lines grow-from-selected animation ──
  if (_animateConnectedLines) {
    _animateConnectedLines = false;
    const connLineItems = [];
    linkMerge.each(function(d) {
      if (!d.visible) return;
      const isConnToSel = d.sourceId === selId || d.targetId === selId;
      if (!isConnToSel) return;
      connLineItems.push({ el: this, d: d });
    });
    const L = Math.max(W, H) * 1.5;
    connLineItems.forEach((item, idx) => {
      const el = d3.select(item.el);
      const fromStart = item.d.sourceId === selId;
      const startOffset = fromStart ? L : -L;

      el.attr("stroke-dasharray", L)
        .attr("stroke-dashoffset", startOffset)
        .attr("stroke-opacity", 0)
        .attr("stroke-width", linkWidth(item.d))
        .attr("filter", null)
        .transition("line-grow")
        .delay(60 + idx * 20)
        .duration(350)
        .ease(d3.easeCubicOut)
        .attr("stroke-dashoffset", 0)
        .attr("stroke-opacity", linkOpacity(item.d))
        .on("end", function() {
          d3.select(this).attr("stroke-dasharray", null);
        });
    });
  }

  // ── Nodes ──
  const nodeSel = nodeGroup.selectAll("g.node").data(nodes, d => d.id);

  const nodeEnter = nodeSel.enter().append("g").attr("class","node")
    .attr("transform", d => `translate(${positions[d.id]?.x || W/2},${positions[d.id]?.y || H/2})`)
    .style("cursor","pointer")
    .style("opacity", 0);

  nodeEnter.append("circle").attr("class","body")
    .attr("stroke-width", 1.5);

  nodeEnter.each(function(d) {
    const imgUrl = faceImages[d.id];
    if (!imgUrl) return;

    const r = nodeRadius(d, false);
    const fo = d3.select(this).append("foreignObject")
      .attr("class","face")
      .attr("x", -r).attr("y", -r)
      .attr("width", r * 2).attr("height", r * 2)
      .style("pointer-events","none")
      .style("overflow","hidden")
      .style("border-radius","50%");

    const div = fo.append("xhtml:div")
      .style("width","100%").style("height","100%")
      .style("border-radius","50%")
      .style("overflow","hidden");

    div.append("xhtml:img")
      .attr("src", imgUrl)
      .style("width","100%").style("height","100%")
      .style("object-fit","cover")
      .style("object-position", facePositions[d.id] || "center")
      .style("display","block")
      .attr("crossorigin", "anonymous")
      .on("load", function() { imageLoaded[d.id] = true; })
      .on("error", function() {
        console.warn('Image load failed:', d.id, imgUrl);
        imageLoaded[d.id] = false;
        d3.select(this.parentNode.parentNode).style("display","none");
      });
  });

  // Handle exit for dynamic data
  nodeSel.exit().transition().duration(dur/2).style("opacity", 0).remove();

  const nodeMerge = nodeEnter.merge(nodeSel);

  const allSmall = isInitialState;
  if (_snapPositions) {
    nodeMerge.interrupt()
      .attr("transform", d => `translate(${positions[d.id].x},${positions[d.id].y})`)
      .style("opacity", d => {
        if (positions[d.id].hidden) return 0;
        if (d.id === selId) return 1;
        if (connIds.has(d.id)) return 0.95;
        return 0.4;
      });
    _snapPositions = false;
  } else {
    nodeMerge.transition().duration(dur).ease(ease)
      .attr("transform", d => `translate(${positions[d.id].x},${positions[d.id].y})`)
      .style("opacity", d => {
        if (positions[d.id].hidden) return 0;
        if (allSmall) return 0.9;
        if (d.id === selId) return 1;
        if (connIds.has(d.id)) return 0.95;
        return 0.4;
      });
  }

  // ── Size ──
  if (_bounceSize) _bounceSize = false;
  const sizeDur = shouldSnap ? 0 : dur;
  const growSelected = shouldSnap && !allSmall && _firstSelection;
  const growDur = 400;
  const growEase = d3.easeBackOut.overshoot(1.2);

  if (shouldSnap && !growSelected) {
    nodeMerge.select(".body")
      .attr("r", d => nodeRadius(d, !allSmall && d.id === selId))
      .attr("fill", d => `url(#grad-${d.group.replace(/\s/g,'')})`)
      .attr("stroke", d => {
        if (allSmall) return "rgba(255,255,255,0.3)";
        if (d.id === selId) return "#ffffff";
        return connIds.has(d.id) ? "rgba(255,255,255,0.5)" : "rgba(255,255,255,0.2)";
      })
      .attr("stroke-width", d => (!allSmall && d.id === selId) ? 2 : 0.8);
    const _faceChanged = new Set([selId]);
    if (_prevSelectedForSnap) _faceChanged.add(_prevSelectedForSnap);
    nodeMerge.filter(d => _faceChanged.has(d.id)).select(".face").each(function(d) {
      const r = nodeRadius(d, !allSmall && d.id === selId) - 2;
      this.setAttribute("x", -r);
      this.setAttribute("y", -r);
      this.setAttribute("width", r * 2);
      this.setAttribute("height", r * 2);
    });
    _prevSelectedForSnap = null;
  } else {
    nodeMerge.select(".body")
      .transition().duration(growSelected ? 0 : sizeDur).ease(ease)
      .attr("r", d => {
        if (growSelected && d.id === selId) return nodeRadius(d, false);
        return nodeRadius(d, !allSmall && d.id === selId);
      })
      .attr("fill", d => `url(#grad-${d.group.replace(/\s/g,'')})`)
      .attr("stroke", d => {
        if (allSmall) return "rgba(255,255,255,0.3)";
        if (d.id === selId) return "#ffffff";
        return connIds.has(d.id) ? "rgba(255,255,255,0.5)" : "rgba(255,255,255,0.2)";
      })
      .attr("stroke-width", d => (!allSmall && d.id === selId) ? 2 : 0.8);
    nodeMerge.select(".face")
      .transition().duration(growSelected ? 0 : sizeDur).ease(ease)
      .attr("x", d => { const r = nodeRadius(d, growSelected ? false : (!allSmall && d.id === selId)) - 2; return -r; })
      .attr("y", d => { const r = nodeRadius(d, growSelected ? false : (!allSmall && d.id === selId)) - 2; return -r; })
      .attr("width", d => { const r = nodeRadius(d, growSelected ? false : (!allSmall && d.id === selId)) - 2; return r * 2; })
      .attr("height", d => { const r = nodeRadius(d, growSelected ? false : (!allSmall && d.id === selId)) - 2; return r * 2; });
  }

  // Grow animation: selected node expands only on first selection
  if (growSelected) {
    _firstSelection = false;
    const selNodes = nodeMerge.filter(d => d.id === selId);
    selNodes.select(".body")
      .transition().delay(30).duration(growDur).ease(growEase)
      .attr("r", nodeRadius(selNode, true))
      .attr("stroke", "#ffffff").attr("stroke-width", 2);
    const bigR = nodeRadius(selNode, true) - 2;
    selNodes.select(".face")
      .transition().delay(30).duration(growDur).ease(growEase)
      .attr("x", -bigR).attr("y", -bigR)
      .attr("width", bigR * 2).attr("height", bigR * 2);
  }

  nodeMerge.select(".body")
    .attr("filter", d => {
      if (d.id === selId) return "url(#glow-lg)";
      if (IS_TABLEAU) return null; // Skip glow on all other nodes in Tableau for performance
      if (connIds.has(d.id)) return "url(#glow-sm)";
      return null;
    });

  // ── Labels ──
  const center = positions._center || selPos;
  const labelData = nodes.filter(n => (allSmall || n.id !== selId) && visibleIds.has(n.id));
  const lblSel = labelGroup.selectAll("text.label").data(labelData, d => d.id);

  lblSel.exit().transition().duration(dur/2).style("opacity",0).remove();

  const lblEnter = lblSel.enter().append("text").attr("class","label")
    .style("pointer-events","none")
    .style("opacity", 0);

  const lblMerge = lblEnter.merge(lblSel);

  if (shouldSnap) {
    lblMerge.interrupt()
      .each(function(d) {
        const p = positions[d.id];
        const r = nodeRadius(d, false);
        const ta = getTextAttrs(p.x, p.y, center.x, center.y, r);
        d3.select(this).attr("transform", `translate(${ta.x},${ta.y}) rotate(${ta.rotation})`);
      })
      .text(d => d.name.toUpperCase())
      .attr("text-anchor", d => {
        const p = positions[d.id];
        return getTextAttrs(p.x, p.y, center.x, center.y, nodeRadius(d,false)).anchor;
      })
      .attr("dominant-baseline","central")
      .attr("fill", d => allSmall ? "#ffffff" : (connIds.has(d.id) ? "#ffffff" : "#999"))
      .attr("font-size", d => {
        const m = settings.labelSize;
        if (allSmall) {
          if (d.importance >= 7) return (10 * m) + "px";
          if (d.importance >= 4) return (8.5 * m) + "px";
          return (7.5 * m) + "px";
        }
        if (!connIds.has(d.id)) return (7.5 * m) + "px";
        if (d.importance >= 7) return (11 * m) + "px";
        if (d.importance >= 4) return (9.5 * m) + "px";
        return (8.5 * m) + "px";
      })
      .attr("font-weight", d => {
        if (allSmall) return d.importance >= 6 ? "600" : "400";
        if (!connIds.has(d.id)) return "400";
        return d.importance >= 6 ? "700" : "600";
      })
      .attr("letter-spacing", d => {
        if (allSmall) return "2px";
        if (connIds.has(d.id)) return "2.5px";
        return "2px";
      })
      .style("opacity", d => {
        if (allSmall) return 1;
        if (connIds.has(d.id)) return 1;
        return 0.55;
      })
      .style("text-shadow", d => allSmall
        ? "0 0 12px rgba(0,0,0,1), 0 0 30px rgba(0,0,0,.9), 0 0 50px rgba(0,0,0,.7)"
        : (connIds.has(d.id)
          ? "0 0 20px rgba(255,255,255,.15), 0 0 40px rgba(0,0,0,.9)"
          : "0 0 16px rgba(0,0,0,.95)"));
  } else {
    lblMerge.transition().duration(IS_TABLEAU ? 0 : dur).ease(ease)
      .attrTween("transform", function(d) {
        const prev = d3.select(this).attr("transform") || `translate(${W/2},${H/2}) rotate(0)`;
        const p = positions[d.id];
        const r = nodeRadius(d, false);
        const ta = getTextAttrs(p.x, p.y, center.x, center.y, r);
        const target = `translate(${ta.x},${ta.y}) rotate(${ta.rotation})`;
        return d3.interpolateString(prev, target);
      })
      .text(d => d.name.toUpperCase())
      .attr("text-anchor", d => {
        const p = positions[d.id];
        return getTextAttrs(p.x, p.y, center.x, center.y, nodeRadius(d,false)).anchor;
      })
      .attr("dominant-baseline","central")
      .attr("fill", d => allSmall ? "#ffffff" : (connIds.has(d.id) ? "#ffffff" : "#999"))
      .attr("font-size", d => {
        const m = settings.labelSize;
        if (allSmall) {
          if (d.importance >= 7) return (10 * m) + "px";
          if (d.importance >= 4) return (8.5 * m) + "px";
          return (7.5 * m) + "px";
        }
        if (!connIds.has(d.id)) return (7.5 * m) + "px";
        if (d.importance >= 7) return (11 * m) + "px";
        if (d.importance >= 4) return (9.5 * m) + "px";
        return (8.5 * m) + "px";
      })
      .attr("font-weight", d => {
        if (allSmall) return d.importance >= 6 ? "600" : "400";
        if (!connIds.has(d.id)) return "400";
        return d.importance >= 6 ? "700" : "600";
      })
      .attr("letter-spacing", d => {
        if (allSmall) return "2px";
        if (connIds.has(d.id)) return "2.5px";
        return "2px";
      })
      .style("opacity", d => {
        if (allSmall) return 1;
        if (connIds.has(d.id)) return 1;
        return 0.55;
      })
      .style("text-shadow", d => allSmall
        ? "0 0 12px rgba(0,0,0,1), 0 0 30px rgba(0,0,0,.9), 0 0 50px rgba(0,0,0,.7)"
        : (connIds.has(d.id)
          ? "0 0 20px rgba(255,255,255,.15), 0 0 40px rgba(0,0,0,.9)"
          : "0 0 16px rgba(0,0,0,.95)"));
  }

  // ── Selected info text ──
  const info = document.getElementById("selected-info");
  if (allSmall) {
    info.classList.add("hidden");
  } else {
    const selR = nodeRadius(selNode, true);
    if (positions._portrait) {
      const ctr = positions._center;
      info.style.top = (ctr.y - positions._R - 24) + "px";
      info.style.left = ctr.x + "px";
      info.style.transform = "translate(-50%, -100%)";
    } else {
      info.style.top = (selPos.y - selR * 0.3) + "px";
      info.style.left = (selPos.x + selR + 16) + "px";
      info.style.transform = "translate(0, -50%)";
    }
    info.classList.remove("hidden");
  }

  // ── Connection panel ──
  try {
    if (allSmall) {
      document.getElementById("connection-panel").style.opacity = "0";
    }
    let panelConns = [...conns];
    if (activeFilter !== "all") {
      panelConns = panelConns.filter(c => c.type === activeFilter);
    }
    if (activeGroupFilter !== "all") {
      panelConns = panelConns.filter(c => nodeMap[c.node?.id]?.group === activeGroupFilter);
    }
    function timeToSec(t) {
      if (!t || typeof t !== 'string' || !t.includes(':')) return 0;
      const [m, s] = t.split(":").map(Number);
      return (isNaN(m) ? 0 : m) * 60 + (isNaN(s) ? 0 : s);
    }
    panelConns.sort((a, b) => timeToSec(b.node?.time) - timeToSec(a.node?.time));

    document.getElementById("sel-name").textContent = selNode.name;
    document.getElementById("sel-meta").textContent = panelConns.length + " connections";
    document.getElementById("bottom-number").textContent = panelConns.length;

    document.getElementById("panel-count").textContent = panelConns.length;
    const connListEl = document.getElementById("conn-list");
    const typeLabel = { ally: "Alliance", enemy: "Conflict", romantic: "Romance", family: "Family" };
    requestAnimationFrame(() => {
      connListEl.innerHTML = panelConns.map(c => {
        const pct = (timeToSec(c.node?.time) / timeToSec("29:00")) * 100;
        return `<div class="conn-row">
          <div class="conn-top">
            <span class="conn-name">${c.node?.name || '—'}</span>
            <span class="conn-type">${typeLabel[c.type] || c.type || '—'} · ${c.node?.time || '0:00'}</span>
          </div>
          <div class="conn-bar-bg"><div class="conn-bar" style="width:${Math.max(0, pct || 0)}%"></div></div>
        </div>`;
      }).join("");
    });
  } catch (panelErr) {
    console.warn('Connection panel render error:', panelErr);
  }

  // ── Disable individual pointer events — SVG-level click handles everything ──
  nodeMerge
    .on("mouseenter", null).on("mousemove", null).on("mouseleave", null)
    .on("click", null)
    .style("pointer-events", "none");

  lblMerge
    .style("pointer-events", "none");
}

// ═══════════════════════════════════════════════
// SPIN ANIMATION
// ═══════════════════════════════════════════════
function spinTo(targetId) {
  if (!targetId || !nodeMap[targetId] || !nodeMap[selectedId]) {
    console.warn('spinTo guard: missing node', targetId, !!nodeMap[targetId], !!nodeMap[selectedId]);
    return;
  }
  const visible = circleOrder.filter(n => getFilteredNodeIds(activeFilter, activeGroupFilter).has(n.id));
  if (visible.length <= 1 || isTransitioning || targetId === selectedId) {
    console.warn('spinTo guard: visible=', visible.length, 'transitioning=', isTransitioning, 'same=', targetId === selectedId);
    return;
  }
  isTransitioning = true;
  isInitialState = false;
  document.body.classList.add('spinning');

  const N = visible.length;
  const center = positions._center;
  const R = positions._R;
  const slotAngle = (2 * Math.PI) / N;

  const curIdx = visible.findIndex(n => n.id === selectedId);
  const targetIdx = visible.findIndex(n => n.id === targetId);
  if (curIdx < 0 || targetIdx < 0) { isTransitioning = false; return; }

  const fwd = ((targetIdx - curIdx) + N) % N;
  const bwd = ((curIdx - targetIdx) + N) % N;
  let steps, dir;
  if (fwd <= bwd) { steps = fwd; dir = 1; }
  else { steps = bwd; dir = -1; }

  const totalAngleRad = -dir * (steps * slotAngle);
  const totalAngleDeg = totalAngleRad * 180 / Math.PI;

  const anchorX = positions[selectedId].x;
  const anchorY = positions[selectedId].y;

  document.getElementById("connection-panel").style.opacity = "0";

  // Shrink selected node instantly
  const smallR = Math.min(W, H) * 0.013 * settings.nodeSize;
  nodeGroup.selectAll("g.node").filter(d => d.id === selectedId).each(function() {
    d3.select(this).select(".body").attr("r", smallR);
    d3.select(this).select(".face")
      .attr("x", -(smallR - 2)).attr("y", -(smallR - 2))
      .attr("width", (smallR - 2) * 2).attr("height", (smallR - 2) * 2);
  });

  // Create spotlight
  const bigR = Math.min(W, H) * 0.038 * settings.nodeSize;
  const spotGroup = svg.append("g").attr("class", "spotlight")
    .attr("transform", `translate(${anchorX},${anchorY})`);

  spotGroup.append("circle")
    .attr("r", bigR + 6).attr("fill", "none")
    .attr("stroke", "#fff").attr("stroke-width", 1.5).attr("stroke-opacity", 0.3);

  const curGroup = nodeMap[selectedId].group.replace(/\s/g, '');
  spotGroup.append("circle").attr("class", "spot-body")
    .attr("r", bigR).attr("fill", `url(#grad-${curGroup})`)
    .attr("stroke", "#ffffff").attr("stroke-width", 2).attr("filter", "url(#glow-lg)");

  const spotFo = spotGroup.append("foreignObject")
    .attr("x", -(bigR - 2)).attr("y", -(bigR - 2))
    .attr("width", (bigR - 2) * 2).attr("height", (bigR - 2) * 2)
    .style("pointer-events", "none").style("overflow", "hidden").style("border-radius", "50%");
  const spotDiv = spotFo.append("xhtml:div")
    .style("width", "100%").style("height", "100%")
    .style("border-radius", "50%").style("overflow", "hidden");
  const spotImg = spotDiv.append("xhtml:img")
    .style("width", "100%").style("height", "100%")
    .style("object-fit", "cover")
    .style("object-position", facePositions[selectedId] || "center")
    .style("display", "block");
  if (faceImages[selectedId]) spotImg.attr("src", faceImages[selectedId]);

  const flashCircle = spotGroup.append("circle")
    .attr("r", bigR).attr("fill", "#ffffff").attr("opacity", 0);

  // Capture original angles
  const origAngles = {};
  visible.forEach(n => {
    origAngles[n.id] = Math.atan2(
      positions[n.id].y - center.y,
      positions[n.id].x - center.x
    );
  });

  const spinDur = Math.min(1200, 300 + steps * 40);
  let startTime = null;
  let lastFaceId = selectedId;

  function easeOutQuint(t) {
    return 1 - Math.pow(1 - t, 5);
  }

  function angleDist(a, b) {
    let d = a - b;
    while (d > Math.PI) d -= 2 * Math.PI;
    while (d < -Math.PI) d += 2 * Math.PI;
    return Math.abs(d);
  }

  function tick(now) {
    if (!startTime) startTime = now;
    const t = Math.min((now - startTime) / spinDur, 1);
    const eased = easeOutQuint(t);
    const currentDeg = totalAngleDeg * eased;
    const currentRad = currentDeg * Math.PI / 180;
    _spinRotationRad = currentRad;

    mainGroup.attr("transform", `rotate(${currentDeg},${center.x},${center.y})`);

    let closestId = lastFaceId;
    let closestDist = Infinity;
    visible.forEach(n => {
      const curAngle = origAngles[n.id] + currentRad;
      const dist = angleDist(curAngle, Math.PI);
      if (dist < closestDist) {
        closestDist = dist;
        closestId = n.id;
      }
    });

    if (closestId !== lastFaceId) {
      lastFaceId = closestId;
      if (faceImages[closestId]) {
        spotImg.attr("src", faceImages[closestId]);
        spotImg.style("object-position", facePositions[closestId] || "center");
      }
      const grp = nodeMap[closestId].group.replace(/\s/g, '');
      spotGroup.select(".spot-body").attr("fill", `url(#grad-${grp})`);

      document.getElementById("sel-name").textContent = nodeMap[closestId].name;
      document.getElementById("sel-meta").textContent = nodeMap[closestId].group;
    }

    if (t < 1) {
      requestAnimationFrame(tick);
    } else {
      mainGroup.attr("transform", null);
      _spinRotationRad = 0;
      document.body.classList.remove('spinning');

      _prevSelectedForSnap = selectedId;
      selectedId = targetId;
      _snapPositions = true;
      _bounceSize = false;
      _staggerLines = false;
      _animateConnectedLines = true;

      document.getElementById("connection-panel").style.opacity = "";
      render(selectedId, false);

      spotGroup.transition().duration(100).style("opacity", 0).remove();

      setTimeout(() => { isTransitioning = false; }, 120);
    }
  }

  requestAnimationFrame(tick);
}

// ═══════════════════════════════════════════════
// NAVIGATION
// ═══════════════════════════════════════════════
function spinToNext(dir) {
  const visible = circleOrder.filter(n => getFilteredNodeIds(activeFilter, activeGroupFilter).has(n.id));
  if (visible.length <= 1 || isTransitioning) return;
  const N = visible.length;
  const curIdx = visible.findIndex(n => n.id === selectedId);
  const nextIdx = (curIdx + dir + N) % N;
  spinTo(visible[nextIdx].id);
}

document.addEventListener("keydown", e => {
  if (isTransitioning) return;
  if (e.key === "ArrowRight" || e.key === "ArrowDown") {
    e.preventDefault();
    spinToNext(1);
  }
  if (e.key === "ArrowLeft" || e.key === "ArrowUp") {
    e.preventDefault();
    spinToNext(-1);
  }
});

let scrollAccum = 0;
const scrollThreshold = 50;
document.addEventListener("wheel", e => {
  if (isTransitioning) return;
  e.preventDefault();
  scrollAccum += e.deltaY;
  if (Math.abs(scrollAccum) < scrollThreshold) return;
  const dir = scrollAccum > 0 ? 1 : -1;
  scrollAccum = 0;
  spinToNext(dir);
}, { passive: false });

// ═══════════════════════════════════════════════
// SVG PROXIMITY HOVER
// ═══════════════════════════════════════════════
svg.on("mousemove.hover", function(event) {
  const [mx, my] = d3.pointer(event);
  let closestId = null;
  let closestDist = Infinity;
  const threshold = Math.min(W, H) * 0.055;
  const ctr = positions._center;

  const spinning = _spinRotationRad !== 0 && ctr;
  const cosR = spinning ? Math.cos(_spinRotationRad) : 1;
  const sinR = spinning ? Math.sin(_spinRotationRad) : 0;

  nodes.forEach(n => {
    if (n.id === selectedId) return;
    const p = positions[n.id];
    if (!p || p.hidden) return;
    if (positions._visibleIds && !positions._visibleIds.has(n.id)) return;

    let vx = p.x, vy = p.y;
    if (spinning) {
      const dx = p.x - ctr.x, dy = p.y - ctr.y;
      vx = ctr.x + dx * cosR - dy * sinR;
      vy = ctr.y + dx * sinR + dy * cosR;
    }

    let dist = Math.hypot(mx - vx, my - vy);

    if (ctr) {
      const r = nodeRadius(n, false);
      const ta = getTextAttrs(vx, vy, ctr.x, ctr.y, r);
      dist = Math.min(dist, Math.hypot(mx - ta.x, my - ta.y));
      dist = Math.min(dist, Math.hypot(mx - (vx + ta.x) / 2, my - (vy + ta.y) / 2));
    }

    if (dist < closestDist) {
      closestDist = dist;
      closestId = n.id;
    }
  });

  if (closestDist > threshold) closestId = null;

  if (closestId !== hoveredId) {
    if (hoveredId) unhighlightNode(hoveredId);
    if (closestId) highlightNode(closestId, event.pageX, event.pageY);
  } else if (hoveredId) {
    const tt = document.getElementById("tooltip");
    tt.style.left = (event.pageX + 16) + "px";
    tt.style.top = (event.pageY - 8) + "px";
  }

  // Cursor feedback — works even in Tableau where individual element cursors may fail
  const clickTarget = findClickTarget(mx, my);
  svg.style("cursor", clickTarget ? "pointer" : "default");
}).on("mouseleave.hover", function() {
  if (hoveredId) unhighlightNode(hoveredId);
  svg.style("cursor", "default");
});

// ── Find closest node to click point (same logic as hover, larger threshold) ──
function findClickTarget(mx, my) {
  const threshold = Math.min(W, H) * 0.13;
  const ctr = positions._center;
  let closestId = null, closestDist = Infinity;

  nodes.forEach(n => {
    const p = positions[n.id];
    if (!p || p.hidden) return;
    if (positions._visibleIds && !positions._visibleIds.has(n.id)) return;

    let dist = Math.hypot(mx - p.x, my - p.y);
    if (ctr) {
      const r = nodeRadius(n, false);
      const ta = getTextAttrs(p.x, p.y, ctr.x, ctr.y, r);
      dist = Math.min(dist, Math.hypot(mx - ta.x, my - ta.y));
      dist = Math.min(dist, Math.hypot(mx - (p.x + ta.x) / 2, my - (p.y + ta.y) / 2));
    }
    if (dist < closestDist) { closestDist = dist; closestId = n.id; }
  });

  return closestDist <= threshold ? closestId : null;
}

svg.on("click", function(event) {
  event.stopPropagation();
  if (isTransitioning) return;
  const [mx, my] = d3.pointer(event);
  const targetId = findClickTarget(mx, my);
  if (!targetId) return;

  if (targetId === selectedId) {
    if (!isInitialState) {
      isInitialState = true;
      render(selectedId, true);
    }
    return;
  }
  if (hoveredId) unhighlightNode(hoveredId);
  document.getElementById("tooltip").classList.remove("visible");
  spinTo(targetId);
});

// ═══════════════════════════════════════════════
// FILTER HANDLERS (standalone mode only)
// ═══════════════════════════════════════════════
function initFilters() {
  document.querySelectorAll(".rel-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      if (isTransitioning) return;
      const type = btn.dataset.type;
      if (type === activeFilter) return;

      document.querySelectorAll(".rel-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      activeFilter = type;

      const filteredIds = getFilteredNodeIds(activeFilter, activeGroupFilter);
      if (!filteredIds.has(selectedId)) {
        const first = circleOrder.find(n => filteredIds.has(n.id));
        if (first) selectedId = first.id;
      }

      isTransitioning = true;
      render(selectedId, true);
      setTimeout(() => { isTransitioning = false; }, 150);
    });
  });

  document.querySelectorAll(".group-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      if (isTransitioning) return;
      const group = btn.dataset.group;
      if (group === activeGroupFilter) return;

      document.querySelectorAll(".group-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      activeGroupFilter = group;

      const filteredIds = getFilteredNodeIds(activeFilter, activeGroupFilter);
      if (!filteredIds.has(selectedId)) {
        const first = circleOrder.find(n => filteredIds.has(n.id));
        if (first) selectedId = first.id;
      }

      isTransitioning = true;
      render(selectedId, true);
      setTimeout(() => { isTransitioning = false; }, 150);
    });
  });
}

// ═══════════════════════════════════════════════
// RESIZE
// ═══════════════════════════════════════════════
window.addEventListener("resize", () => {
  W = window.innerWidth; H = window.innerHeight;
  svg.attr("width", W).attr("height", H);
  svg.select("rect").attr("width", W).attr("height", H);
  rebuildClouds();
  render(selectedId, false);
});

// ═══════════════════════════════════════════════
// TABLEAU DATA CHANGE HANDLER
// ═══════════════════════════════════════════════
let _dataChangeTimer = 0;
function onTableauDataChanged() {
  clearTimeout(_dataChangeTimer);
  _dataChangeTimer = setTimeout(_handleDataChange, 100);
}

async function _handleDataChange() {
  // Reset transition state — data change interrupts any ongoing animation
  isTransitioning = false;
  document.body.classList.remove('spinning');
  mainGroup.attr("transform", null);
  svg.selectAll(".spotlight").remove();

  const rows = await loadDataFromTableau();

  if (!rows || rows.length === 0) {
    // Data removed or encodings cleared — show empty state
    showEmptyState(true);
    linkGroup.selectAll("*").remove();
    nodeGroup.selectAll("*").remove();
    labelGroup.selectAll("*").remove();
    nodes = [];
    links = [];
    return;
  }

  showEmptyState(false);
  const parsed = parseNetworkData(rows);
  nodes = parsed.nodes;
  links = parsed.links;
  applyDynamicData(parsed);
  rebuildDerivedData();
  buildNodeGradients();

  if (!nodeMap[selectedId]) {
    selectedId = nodes.length > 0 ? nodes[0].id : null;
  }

  linkGroup.selectAll("*").remove();
  nodeGroup.selectAll("*").remove();
  labelGroup.selectAll("*").remove();

  isInitialState = true;
  _firstSelection = true;
  if (selectedId) render(selectedId, true);
}

// ═══════════════════════════════════════════════
// LIGHTWEIGHT SETTINGS UPDATE (no layout recalc)
// ═══════════════════════════════════════════════
function applySettingsLive() {
  const selId = selectedId;
  const conns = getConnections(selId);
  const connIds = new Set(conns.map(c => c.node.id));
  const allSmall = isInitialState;
  const visibleIds = positions._visibleIds || new Set(nodes.map(n => n.id));

  // Update links — only stroke-width and stroke-opacity
  linkGroup.selectAll("path.link").each(function(d) {
    if (!d.visible) return;
    const m_w = settings.lineWidth;
    const m_o = settings.lineOpacity;
    const str = isNaN(d.strength) ? 5 : d.strength;
    let w, o;
    if (allSmall) {
      w = (0.02 + Math.pow(str / 10, 3.5) * 5) * m_w;
      o = Math.min(1, (0.06 + str * 0.06) * m_o);
    } else {
      const isSel = d.sourceId === selId || d.targetId === selId;
      if (isSel) {
        w = (0.5 + Math.pow(str / 10, 2) * 2) * m_w;
        o = Math.min(1, (0.6 + Math.pow(str / 10, 2) * 0.4) * m_o);
      } else {
        // Background lines: subtle but visible
        w = (0.15 + Math.pow(str / 10, 2) * 0.6) * m_w;
        o = Math.min(1, (0.04 + Math.pow(str / 10, 2) * 0.1) * m_o);
      }
    }
    this.setAttribute("stroke-width", w);
    this.setAttribute("stroke-opacity", o);
  });

  // Update nodes — radius only
  nodeGroup.selectAll("g.node").each(function(d) {
    const isSel = !allSmall && d.id === selId;
    const r = nodeRadius(d, isSel);
    const el = d3.select(this);
    el.select(".body").attr("r", r);
    const faceR = r - 2;
    const face = el.select(".face").node();
    if (face) {
      face.setAttribute("x", -faceR);
      face.setAttribute("y", -faceR);
      face.setAttribute("width", faceR * 2);
      face.setAttribute("height", faceR * 2);
    }
  });

  // Update labels — font-size only
  const m_l = settings.labelSize;
  labelGroup.selectAll("text.label").each(function(d) {
    let size;
    if (allSmall) {
      size = d.importance >= 7 ? 10 : d.importance >= 4 ? 8.5 : 7.5;
    } else if (!connIds.has(d.id)) {
      size = 7.5;
    } else {
      size = d.importance >= 7 ? 11 : d.importance >= 4 ? 9.5 : 8.5;
    }
    this.setAttribute("font-size", (size * m_l) + "px");
  });
}

// ═══════════════════════════════════════════════
// SETTINGS PANEL
// ═══════════════════════════════════════════════
function initSettings() {
  const btn = document.getElementById('settings-btn');
  const panel = document.getElementById('settings-panel');
  const closeBtn = document.getElementById('settings-close');
  const resetBtn = document.getElementById('settings-reset');

  btn.addEventListener('click', () => {
    panel.classList.toggle('settings-hidden');
  });
  closeBtn.addEventListener('click', () => {
    panel.classList.add('settings-hidden');
  });

  // Throttle: only run applySettingsLive once per frame
  let _settingsRaf = 0;
  function scheduleSettingsUpdate() {
    if (_settingsRaf) return;
    _settingsRaf = requestAnimationFrame(() => {
      _settingsRaf = 0;
      applySettingsLive();
    });
  }

  function bindSlider(sliderId, valId, key, formatter) {
    const slider = document.getElementById(sliderId);
    const valEl = document.getElementById(valId);
    slider.addEventListener('input', () => {
      const v = parseFloat(slider.value);
      settings[key] = v;
      valEl.textContent = formatter(v);
      scheduleSettingsUpdate();
    });
  }

  bindSlider('set-line-width', 'val-line-width', 'lineWidth', v => v.toFixed(1) + 'x');
  bindSlider('set-line-opacity', 'val-line-opacity', 'lineOpacity', v => v.toFixed(1) + 'x');
  bindSlider('set-node-size', 'val-node-size', 'nodeSize', v => v.toFixed(1) + 'x');
  bindSlider('set-label-size', 'val-label-size', 'labelSize', v => v.toFixed(1) + 'x');

  // Background brightness — direct DOM, no render needed
  const bgSlider = document.getElementById('set-bg-brightness');
  const bgVal = document.getElementById('val-bg-brightness');
  bgSlider.addEventListener('input', () => {
    const v = parseFloat(bgSlider.value);
    settings.bgBrightness = v;
    bgVal.textContent = Math.round(v * 100) + '%';
    const bgEl = document.getElementById('bg-image');
    if (bgEl) bgEl.style.filter = `brightness(${v}) saturate(0.6)`;
  });

  resetBtn.addEventListener('click', () => {
    settings.lineWidth = 1;
    settings.lineOpacity = 1;
    settings.nodeSize = 1;
    settings.labelSize = 1;
    settings.bgBrightness = 0.7;

    document.getElementById('set-line-width').value = 1;
    document.getElementById('set-line-opacity').value = 1;
    document.getElementById('set-node-size').value = 1;
    document.getElementById('set-label-size').value = 1;
    document.getElementById('set-bg-brightness').value = 0.7;

    document.getElementById('val-line-width').textContent = '1.0x';
    document.getElementById('val-line-opacity').textContent = '1.0x';
    document.getElementById('val-node-size').textContent = '1.0x';
    document.getElementById('val-label-size').textContent = '1.0x';
    document.getElementById('val-bg-brightness').textContent = '70%';

    const bgEl = document.getElementById('bg-image');
    if (bgEl) bgEl.style.filter = 'brightness(0.7) saturate(0.6)';

    applySettingsLive();
  });
}

// ═══════════════════════════════════════════════
// EMPTY STATE (Tableau: no data assigned)
// ═══════════════════════════════════════════════
function showEmptyState(show) {
  const el = document.getElementById('empty-state');
  if (!el) return;
  if (show) {
    el.classList.remove('hidden');
    document.getElementById('selected-info').classList.add('hidden');
    document.getElementById('connection-panel').style.opacity = '0';
    document.getElementById('click-hint').style.display = 'none';
    document.getElementById('bottom-label').style.display = 'none';
    document.getElementById('bottom-number').style.display = 'none';
  } else {
    el.classList.add('hidden');
    document.getElementById('click-hint').style.display = '';
    document.getElementById('bottom-label').style.display = '';
    document.getElementById('bottom-number').style.display = '';
  }
}

// ═══════════════════════════════════════════════
// INITIALIZATION
// ═══════════════════════════════════════════════
async function init() {
  if (IS_TABLEAU) {
    document.body.classList.add('tableau-mode');
    try {
      await tableau.extensions.initializeAsync();
      console.log('Tableau Extensions API initialized');

      const rows = await loadDataFromTableau();
      if (rows && rows.length > 0) {
        const parsed = parseNetworkData(rows);
        nodes = parsed.nodes;
        links = parsed.links;
        console.log(`Parsed: ${nodes.length} nodes, ${links.length} links, ${Object.keys(parsed.images).length} images`);
        if (links.length > 0) console.log('First link:', JSON.stringify(links[0]));
        applyDynamicData(parsed);
        selectedId = nodes[0].id;
        showEmptyState(false);
      } else {
        // No data assigned — show placeholder
        showEmptyState(true);
      }

      // Listen for data changes (filters, encodings, etc.)
      const worksheet = tableau.extensions.worksheetContent.worksheet;
      worksheet.addEventListener(
        tableau.TableauEventType.SummaryDataChanged,
        onTableauDataChanged
      );
    } catch (e) {
      console.warn('Tableau init failed:', e);
      showEmptyState(true);
    }
  } else {
    // Standalone mode — use fallback data for demo
    nodes = FALLBACK_NODES;
    links = FALLBACK_LINKS;
    initFilters();
  }

  initSettings();

  if (nodes.length > 0) {
    rebuildDerivedData();
    render(selectedId, true);
  }
}

init();
