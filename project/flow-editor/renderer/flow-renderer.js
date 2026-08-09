"use strict";
/* flow-renderer.js — Flow DSL v0.3 렌더러 (클릭 탐색 모델).
   재생 개념 없음: 캔버스는 항상 돌아가고(ambient + 주인공 패킷 루프),
   사용자는 노드/엣지를 클릭해 구간 상세를 본다. */

/* ================= 상수 ================= */
const KIND_COLOR_RAW = { packet: "#5b9bd5", signal: "#d4a853", data: "#66bb6a", error: "#e05555" };
/* 아이콘은 기술 문서 톤에 맞춰 절제된 기하 기호를 쓴다.
   컬러 이모지는 문서 안에서 튀고 플랫폼마다 모양이 달라 피한다. */
const ROLE_ICON = { process: "▣", store: "▤", external: "◇", decision: "◈" };
const MECH_LABEL = {
  "table-lookup": "테이블 매칭", "weighted-select": "가중치 선택", "rewrite": "헤더 재작성",
  "crypt": "암복호화", "k8s-resolve": "K8s 리소스 매핑", "encap": "캡슐화", "decap": "디캡슐화",
  "filter": "필터", "queue": "큐",
};
/* 노드 창 안에 다는 메커니즘 배지 — 기호 + 짧은 이름.
   패널의 MECH_LABEL 과 같은 어휘를 쓴다 (노드와 패널의 라벨 통일) */
const MECH_BADGE = {
  "table-lookup": { icon: "≡", short: "테이블 매칭" }, "weighted-select": { icon: "%", short: "가중치 선택" },
  "rewrite": { icon: "⇄", short: "헤더 재작성" }, "crypt": { icon: "🔐", short: "암복호화" },
  "k8s-resolve": { icon: "⎈", short: "K8s 매핑" }, "encap": { icon: "⊞", short: "캡슐화" },
  "decap": { icon: "⊟", short: "디캡슐화" }, "filter": { icon: "⊘", short: "필터" },
  "queue": { icon: "▤", short: "큐" },
};
const DECO_LABEL = {
  "one-to-one": "1:1 — 양끝이 정확히 하나씩 대응",
  "one-to-many": "1:N — 한 출발점이 여러 목적지로 갈라짐",
  "optional": "선택 경로 — 조건에 따라 흐르지 않을 수 있음",
};
const NS = "http://www.w3.org/2000/svg";
const TITLE_H = 24, GROUP_TITLE_H = 22, PAD = 18, GAP_RANK = 90, GAP_NODE = 26;
const PORT_R = 4.5;
const AMBIENT_SPEED = 46;    // px/s

/* ================= 상태 ================= */
const nodesById = {}, edgesById = {};
let collapsed = new Set();
let layout = {};
let portPos = {};
let edgePaths = {};
let ambient = [];
let viewBox = { x: 0, y: 0, w: 100, h: 100 };
let contentBox = { x: 0, y: 0, w: 100, h: 100 };

const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
let motionOn = !reducedMotion;
let speed = 1.0;
let lastTs = null;

let resolvedChanges = [];         // stepIdx -> [{kind,layer,layerName,field,from,to,note}]
let nodeSnapshot = new Map();     // nodeId -> 그 노드를 떠날 때의 패킷 계층 상태
let panelNodeId = null, panelEdgeId = null;

const svg = document.getElementById("canvas");
const $ = (id) => document.getElementById(id);
const esc = (s) => String(s ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

/* ================= 데이터 준비 ================= */
function init() {
  if (!FLOW) { $("hint").textContent = "FLOW 데이터가 주입되지 않았습니다. tools/build.go 로 생성하세요."; return; }
  for (const n of FLOW.nodes) {
    nodesById[n.id] = n;
    if (n.type !== "group" && !n.ports) {
      n.ports = { in: [{ id: "_in", kind: "data" }], out: [{ id: "_out", kind: "data" }] };
    }
    if (n.type === "group" && n.collapsed) collapsed.add(n.id);
  }
  for (const e of FLOW.edges) edgesById[e.id] = e;

  $("title").textContent = FLOW.meta.title;
  $("subtitle").textContent = FLOW.meta.subtitle || "";
  document.title = FLOW.meta.title + " — Flow Editor";
  buildLegend();
  precomputeTrace();

  relayout(true);
  bindControls();
  requestAnimationFrame(tick);
}

function iconOf(n) {
  return n.icon || (n.type === "group" ? "" : (ROLE_ICON[n.role || "process"] || "⚙️"));
}

function buildLegend() {
  const leg = $("legend");
  const shapes = { packet: rectShape, signal: triShape, data: circShape, error: diamShape };
  for (const k of ["packet", "signal", "data", "error"]) {
    const span = document.createElement("span");
    const s = document.createElementNS(NS, "svg");
    s.setAttribute("width", 12); s.setAttribute("height", 12);
    s.appendChild(shapes[k](6, 6, 4.5, KIND_COLOR_RAW[k]));
    span.appendChild(s);
    span.appendChild(document.createTextNode(k));
    leg.appendChild(span);
  }
}

/* trace 사전 계산 — 스텝별 변형(이전값 포함)과 각 노드 시점의 패킷 상태를 함께 구한다.
   패킷 필드를 손으로 적지 않고 layerOps 를 순서대로 적용해 자동으로 얻는다. */
function precomputeTrace() {
  resolvedChanges = [];
  nodeSnapshot = new Map();
  if (!FLOW.trace) return;
  const steps = FLOW.trace.steps;
  const sim = (FLOW.trace.entity.layers || []).map(l => ({ id: l.id, name: l.name, fields: { ...(l.fields || {}) }, locked: !!l.locked }));
  steps.forEach((s) => {
    const changes = [];
    for (const op of s.layerOps || []) {
      if (op.op === "set") {
        const layer = sim.find(l => l.id === op.layer);
        if (!layer) continue;
        changes.push({ kind: "set", layer: op.layer, layerName: layer.name, field: op.field, from: layer.fields[op.field], to: op.value });
        layer.fields[op.field] = op.value;
      } else if (op.op === "push") {
        sim.unshift({ id: op.layer.id, name: op.layer.name, fields: { ...(op.layer.fields || {}) }, locked: false });
        changes.push({ kind: "push", layer: op.layer.id, layerName: op.layer.name });
      } else if (op.op === "pop") {
        const idx = sim.findIndex(l => l.id === op.layer);
        if (idx >= 0) { changes.push({ kind: "pop", layer: op.layer, layerName: sim[idx].name }); sim.splice(idx, 1); }
      } else if (op.op === "lock" || op.op === "unlock") {
        const layer = sim.find(l => l.id === op.layer);
        if (layer) { layer.locked = op.op === "lock"; changes.push({ kind: op.op, layer: op.layer, layerName: layer.name, note: op.note }); }
      }
    }
    resolvedChanges.push(changes);
    // 이 스텝을 마친 시점의 패킷 상태를 노드에 박제한다 (바뀐 필드 표시 포함)
    const changedFields = new Set(changes.filter(c => c.kind === "set").map(c => `${c.layer}.${c.field}`));
    const changedLayers = new Set(changes.filter(c => c.kind !== "set").map(c => c.layer));
    nodeSnapshot.set(s.at, {
      layers: sim.map(l => ({ id: l.id, name: l.name, fields: { ...l.fields }, locked: l.locked })),
      changedFields, changedLayers,
      dropped: changes.filter(c => c.kind === "pop").map(c => c.layerName),
    });
  });
}

/* ================= 가시성 계산 ================= */
function ancestorChain(id) {
  const chain = [];
  let cur = nodesById[id];
  while (cur) { chain.push(cur.id); cur = cur.parentId ? nodesById[cur.parentId] : null; }
  return chain;
}
function visibleOf(id) {
  const chain = ancestorChain(id);
  for (let i = chain.length - 1; i >= 1; i--) {
    if (collapsed.has(chain[i])) return chain[i];
  }
  return id;
}
function childAtLevel(containerId, nodeId) {
  let cur = nodesById[nodeId];
  while (cur) {
    const p = cur.parentId || null;
    if (p === containerId) return cur.id;
    cur = p ? nodesById[p] : null;
  }
  return null;
}
function directChildren(containerId) {
  return FLOW.nodes.filter(n => (n.parentId || null) === containerId);
}

/* ================= 크기·레이아웃 ================= */
/* 폭 근사. 모노스페이스(계층 필드)는 라틴 글자가 0.6em 로 더 넓어 따로 잰다 */
function textWidth(s, size, mono) {
  let w = 0;
  const latin = mono ? 0.605 : 0.55;
  for (const ch of s || "") w += /[ᄀ-퟿　-ヿ]/.test(ch) ? size : size * latin;
  return w;
}
/* 완전한 문장과 패킷 계층이 들어가므로 노드 폭을 정해두고 줄바꿈한다 */
const NODE_W = 268, INFO_FONT = 10, INFO_LH = 13;
const LAYER_LH = 12, LAYER_NAME_W = 62;
function wrapText(s, fontSize, maxW, mono) {
  const words = String(s || "").split(/\s+/).filter(Boolean);
  const lines = [];
  let cur = "";
  for (const w of words) {
    const cand = cur ? cur + " " + w : w;
    if (textWidth(cand, fontSize, mono) <= maxW || !cur) cur = cand;
    else { lines.push(cur); cur = w; }
  }
  if (cur) lines.push(cur);
  return lines;
}
function nodeBody(n) {
  /* 창 3단: info 설명 → 메커니즘 배지 → 패킷 계층 스택.
     렌더와 크기 계산이 어긋나지 않도록 한 곳에서 만든다 */
  const inner = NODE_W - 18;
  const infoLines = (n.info || []).flatMap(line => wrapText(line, INFO_FONT, inner));
  const badges = (n.mechanisms || []).map(m => MECH_BADGE[m.type]).filter(Boolean);

  /* 이 노드를 지난 뒤의 패킷 상태 — layerOps 로 자동 계산된 스냅샷.
     계층마다 필드를 나열하고, 이 노드에서 바뀐 필드만 강조한다 */
  const snap = nodeSnapshot.get(n.id);
  const layerRows = [];
  if (snap) {
    for (const l of snap.layers) {
      const fieldText = l.locked
        ? "암호화되어 볼 수 없음"
        : Object.entries(l.fields).map(([k, v]) => `${k}=${v}`).join("  ");
      // 계층 이름 칸(LAYER_NAME_W)만큼 밀려 시작하므로 그만큼 빼고 줄바꿈한다 (모노스페이스 기준)
      const wrapped = wrapText(fieldText, 9, inner - LAYER_NAME_W, true);
      wrapped.forEach((text, i) => layerRows.push({
        name: i === 0 ? l.name : "",
        text,
        locked: l.locked,
        changed: !l.locked && Object.keys(l.fields).some(k => snap.changedFields.has(`${l.id}.${k}`)),
        layerChanged: snap.changedLayers.has(l.id),
      }));
    }
    for (const name of snap.dropped) {
      layerRows.push({ name: "", text: `${name} 헤더는 여기서 벗겨졌습니다`, dropped: true });
    }
  }
  return { infoLines, badges, layerRows };
}
function leafSize(n) {
  if (n.type === "group") {  // 접힌 그룹
    const label = n.label + "  ▸";
    const w = Math.max(textWidth(label, 12) + 40 + (iconOf(n) ? 18 : 0), 150);
    return { w: Math.ceil(w), h: 52 };
  }
  const { infoLines, badges, layerRows } = nodeBody(n);
  let h = TITLE_H + 6;
  if (n.sublabel) h += 14;
  if (infoLines.length) h += infoLines.length * INFO_LH + 3;
  if (badges.length) h += 17;
  if (layerRows.length) h += 6 + layerRows.length * LAYER_LH + 4;
  h += 8;
  return { w: NODE_W, h: Math.max(h, 46) };
}
function countDescendants(gid) {
  let c = 0;
  for (const n of FLOW.nodes) {
    if (n.id === gid) continue;
    if (ancestorChain(n.id).includes(gid)) c++;
  }
  return c;
}

function layoutContainer(containerId) {
  const kids = directChildren(containerId);
  const sizes = {}, inner = {};
  for (const k of kids) {
    if (k.type === "group" && !collapsed.has(k.id)) {
      const sub = layoutContainer(k.id);
      sizes[k.id] = { w: sub.w, h: sub.h };
      inner[k.id] = sub;
    } else {
      sizes[k.id] = leafSize(k);
    }
  }
  const kidIds = kids.map(k => k.id);
  const succ = {}; kidIds.forEach(id => succ[id] = new Set());
  const hasPred = new Set();
  for (const e of FLOW.edges) {
    const s = childAtLevel(containerId, e.source);
    const t = childAtLevel(containerId, e.target);
    if (s && t && s !== t) { succ[s].add(t); hasPred.add(t); }
  }
  const rank = {};
  function setRank(id, r, seen) {
    if (seen.has(id)) return;
    seen.add(id);
    if (rank[id] === undefined || r > rank[id]) {
      rank[id] = r;
      for (const nx of succ[id]) setRank(nx, r + 1, seen);
    }
    seen.delete(id);
  }
  for (const id of kidIds) if (!hasPred.has(id)) setRank(id, 0, new Set());
  for (const id of kidIds) if (rank[id] === undefined) rank[id] = 0;

  const isTB = (FLOW.meta.direction || "LR") === "TB";
  const byRank = {};
  for (const id of kidIds) (byRank[rank[id]] = byRank[rank[id]] || []).push(id);
  const rankKeys = Object.keys(byRank).map(Number).sort((a, b) => a - b);

  const children = {};
  let main = 0, crossMax = 0;
  for (const r of rankKeys) {
    const ids = byRank[r];
    let cross = 0, mainSize = 0;
    for (const id of ids) {
      const sz = sizes[id];
      const mw = isTB ? sz.h : sz.w, cw = isTB ? sz.w : sz.h;
      children[id] = { main, cross, w: sz.w, h: sz.h };
      cross += cw + GAP_NODE;
      mainSize = Math.max(mainSize, mw);
    }
    cross -= GAP_NODE;
    for (const id of ids) children[id]._rankCross = cross;
    crossMax = Math.max(crossMax, cross);
    main += mainSize + GAP_RANK;
  }
  main -= GAP_RANK;

  const titleH = containerId ? GROUP_TITLE_H : 0;
  for (const id of Object.keys(children)) {
    const c = children[id];
    const centered = c.cross + (crossMax - c._rankCross) / 2;
    const x = isTB ? centered : c.main;
    const y = isTB ? c.main : centered;
    children[id] = { x: x + PAD, y: y + PAD + titleH, w: c.w, h: c.h, inner: inner[id] };
  }
  const w = (isTB ? crossMax : main) + PAD * 2;
  const h = (isTB ? main : crossMax) + PAD * 2 + titleH;
  return { w: Math.max(w, 140), h: Math.max(h, 60), children };
}

function computeLayout() {
  layout = {};
  const root = layoutContainer(null);
  (function absolutize(frame, ox, oy) {
    for (const [id, c] of Object.entries(frame.children)) {
      layout[id] = { x: ox + c.x, y: oy + c.y, w: c.w, h: c.h };
      if (c.inner) absolutize(c.inner, ox + c.x, oy + c.y);
    }
  })(root, 0, 0);
  contentBox = { x: -20, y: -20, w: root.w + 40, h: root.h + 40 };
}

/* ================= 포트 위치 ================= */
function computePorts() {
  portPos = {};
  const isTB = (FLOW.meta.direction || "LR") === "TB";
  for (const n of FLOW.nodes) {
    if (visibleOf(n.id) !== n.id) continue;
    if (n.type === "group") continue;
    const rect = layout[n.id]; if (!rect) continue;
    placeDeclaredPorts(n, rect, isTB);
  }
  for (const n of FLOW.nodes) {
    if (n.type !== "group") continue;
    if (visibleOf(n.id) !== n.id) continue;
    const rect = layout[n.id]; if (!rect) continue;
    if (!collapsed.has(n.id)) continue;
    placeBoundaryPorts(n, rect, isTB);
  }
}
function placeDeclaredPorts(n, rect, isTB) {
  for (const side of ["in", "out"]) {
    const list = (n.ports?.[side] || []);
    list.forEach((p, i) => {
      const frac = (i + 1) / (list.length + 1);
      let x, y;
      if (!isTB) { x = side === "in" ? rect.x : rect.x + rect.w; y = rect.y + rect.h * frac; }
      else       { y = side === "in" ? rect.y : rect.y + rect.h; x = rect.x + rect.w * frac; }
      portPos[`${n.id}/${p.id}`] = { x, y, kind: p.kind };
    });
  }
}
function placeBoundaryPorts(g, rect, isTB) {
  const ins = [], outs = [];
  for (const e of FLOW.edges) {
    const vs = visibleOf(e.source), vt = visibleOf(e.target);
    if (vs === g.id && vt !== g.id) outs.push(e);
    if (vt === g.id && vs !== g.id) ins.push(e);
  }
  ins.forEach((e, i) => {
    const frac = (i + 1) / (ins.length + 1);
    portPos[`boundary/${e.id}/in`] = !isTB
      ? { x: rect.x, y: rect.y + rect.h * frac, kind: e.kind }
      : { x: rect.x + rect.w * frac, y: rect.y, kind: e.kind };
  });
  outs.forEach((e, i) => {
    const frac = (i + 1) / (outs.length + 1);
    portPos[`boundary/${e.id}/out`] = !isTB
      ? { x: rect.x + rect.w, y: rect.y + rect.h * frac, kind: e.kind }
      : { x: rect.x + rect.w * frac, y: rect.y + rect.h, kind: e.kind };
  });
}
function endpointPos(e, side) {
  const nodeId = e[side], v = visibleOf(nodeId);
  const dirKey = side === "source" ? "out" : "in";
  if (v !== nodeId || (nodesById[v].type === "group" && collapsed.has(v))) {
    return portPos[`boundary/${e.id}/${dirKey}`];
  }
  const n = nodesById[nodeId];
  const portId = e[side + "Port"];
  if (portId && portPos[`${nodeId}/${portId}`]) return portPos[`${nodeId}/${portId}`];
  const list = (n.ports?.[dirKey] || []);
  const match = list.find(p => p.kind === e.kind) || list[0];
  return match ? portPos[`${nodeId}/${match.id}`] : centerOf(layout[nodeId]);
}
function centerOf(r) { return r ? { x: r.x + r.w / 2, y: r.y + r.h / 2 } : { x: 0, y: 0 }; }

/* ================= SVG 렌더 ================= */
function el(tag, attrs, parent) {
  const e = document.createElementNS(NS, tag);
  for (const [k, v] of Object.entries(attrs || {})) e.setAttribute(k, v);
  if (parent) parent.appendChild(e);
  return e;
}
function rectShape(cx, cy, r, color) { return el("rect", { x: cx - r, y: cy - r, width: r * 2, height: r * 2, fill: color, class: "port" }); }
function triShape(cx, cy, r, color) { return el("path", { d: `M ${cx} ${cy - r} L ${cx + r} ${cy + r} L ${cx - r} ${cy + r} Z`, fill: color, class: "port" }); }
function circShape(cx, cy, r, color) { return el("circle", { cx, cy, r, fill: color, class: "port" }); }
function diamShape(cx, cy, r, color) { return el("path", { d: `M ${cx} ${cy - r} L ${cx + r} ${cy} L ${cx} ${cy + r} L ${cx - r} ${cy} Z`, fill: color, class: "port" }); }
const SHAPE_FN = { packet: rectShape, signal: triShape, data: circShape, error: diamShape };

let gEdges, gNodes, gEdgeHits, gParticles;

function render() {
  svg.innerHTML = "";
  const gRoot = el("g", { id: "g-root" }, svg);
  gEdges = el("g", {}, gRoot);
  gNodes = el("g", {}, gRoot);
  gEdgeHits = el("g", {}, gRoot);   // 히트 영역은 노드/그룹 위 — 그룹 박스가 엣지 클릭을 가로채지 않게
  gParticles = el("g", {}, gRoot);

  renderContainers(null);
  renderEdges();
  renderAmbientInit();
  applyViewBox();
  markPanelTarget();
}

function renderContainers(containerId) {
  for (const n of directChildren(containerId)) {
    if (n.type === "group") renderGroup(n);
    else renderLeaf(n);
  }
}
function renderGroup(g) {
  const rect = layout[g.id]; if (!rect) return;
  const isCol = collapsed.has(g.id);
  const grp = el("g", { class: "group" + (isCol ? " collapsed" : ""), "data-id": g.id }, gNodes);
  const box = el("rect", { x: rect.x, y: rect.y, width: rect.w, height: rect.h, rx: 8, class: "group-box" }, grp);
  const th = el("rect", { x: rect.x, y: rect.y, width: rect.w, height: GROUP_TITLE_H, rx: 8, class: "group-title-bg" }, grp);
  const tl = el("text", { x: rect.x + 10, y: rect.y + 15, class: "group-label" }, grp);
  const gi = iconOf(g);
  tl.textContent = `${isCol ? "▸" : "▾"} ${gi ? gi + " " : ""}${g.label}`;
  if (isCol) {
    const sub = el("text", { x: rect.x + 10, y: rect.y + 34, class: "node-sublabel" }, grp);
    sub.textContent = `${countDescendants(g.id)}개 노드 (클릭해 펼치기)`;
  }
  const toggle = (ev) => { ev.stopPropagation(); collapsed.has(g.id) ? collapsed.delete(g.id) : collapsed.add(g.id); relayout(false); };
  th.addEventListener("click", toggle);
  tl.addEventListener("click", toggle);
  box.addEventListener("click", (ev) => { ev.stopPropagation(); openNodePanel(g.id); });
  th.setAttribute("role", "button");
  th.setAttribute("aria-label", `${g.label} ${isCol ? "펼치기" : "접기"}`);

  if (!isCol) renderContainers(g.id);
  else renderBoundaryPorts(g);
}
function renderBoundaryPorts(g) {
  for (const [key, p] of Object.entries(portPos)) {
    if (!key.startsWith("boundary/")) continue;
    const eid = key.split("/")[1];
    const e = edgesById[eid];
    if (visibleOf(e.source) !== g.id && visibleOf(e.target) !== g.id) continue;
    const kind = p.kind || "data";
    gNodes.appendChild(SHAPE_FN[kind](p.x, p.y, PORT_R, KIND_COLOR_RAW[kind]));
  }
}
function renderLeaf(n) {
  const rect = layout[n.id]; if (!rect) return;
  const role = n.role || "process";
  const grp = el("g", { class: `node role-${role}`, "data-id": n.id }, gNodes);
  grp.addEventListener("click", (ev) => { ev.stopPropagation(); openNodePanel(n.id); });

  el("rect", { x: rect.x, y: rect.y, width: rect.w, height: rect.h, rx: 6, class: "node-box" }, grp);
  el("rect", { x: rect.x, y: rect.y, width: rect.w, height: TITLE_H, rx: 6, class: "node-title-bg" }, grp);
  const ic = iconOf(n);
  let lx = rect.x + 9;
  if (ic) {
    const it = el("text", { x: lx, y: rect.y + 16, "font-size": "11" }, grp);
    it.textContent = ic;
    lx += 18;
  }
  const lbl = el("text", { x: lx, y: rect.y + 16, class: "node-label" }, grp);
  lbl.textContent = (role === "decision" ? "◇ " : "") + n.label;

  if (role === "store") {
    el("line", { x1: rect.x, y1: rect.y + TITLE_H + 2, x2: rect.x + rect.w, y2: rect.y + TITLE_H + 2, class: "store-line" }, grp);
    el("line", { x1: rect.x, y1: rect.y + rect.h - 3, x2: rect.x + rect.w, y2: rect.y + rect.h - 3, class: "store-line" }, grp);
  }
  const { infoLines, badges, layerRows } = nodeBody(n);
  let cy = rect.y + TITLE_H + 12;
  if (n.sublabel) {
    const sub = el("text", { x: rect.x + 9, y: cy, class: "node-sublabel" }, grp);
    sub.textContent = n.sublabel;
    cy += 14;
  }
  // 1단 — 설명 문장
  for (const line of infoLines) {
    const it = el("text", { x: rect.x + 9, y: cy, class: "node-info" }, grp);
    it.textContent = line;
    cy += INFO_LH;
  }
  if (infoLines.length) cy += 3;
  // 2단 — 메커니즘 배지
  if (badges.length) {
    let bx = rect.x + 9;
    for (const b of badges) {
      const label = `${b.icon} ${b.short}`;
      const bw = textWidth(label, 9) + 12;
      el("rect", { x: bx, y: cy - 9, width: bw, height: 13, rx: 6.5, class: "mech-badge-bg" }, grp);
      const bt = el("text", { x: bx + 6, y: cy, class: "mech-badge-text" }, grp);
      bt.textContent = label;
      bx += bw + 4;
    }
    cy += 17;
  }
  // 3단 — 이 노드를 지난 뒤의 패킷 계층 상태 (layerOps 로 자동 계산)
  if (layerRows.length) {
    cy += 2;
    el("line", { x1: rect.x + 9, y1: cy, x2: rect.x + rect.w - 9, y2: cy, class: "node-divider" }, grp);
    cy += 11;
    for (const row of layerRows) {
      if (row.name) {
        const nm = el("text", { x: rect.x + 9, y: cy, class: "layer-name" + (row.layerChanged ? " chg" : "") }, grp);
        nm.textContent = row.name;
      }
      const cls = row.dropped ? "layer-dropped" : ("layer-fields" + (row.changed ? " chg" : "") + (row.locked ? " locked" : ""));
      const ft = el("text", { x: rect.x + 9 + LAYER_NAME_W, y: cy, class: cls }, grp);
      ft.textContent = row.text;
      cy += LAYER_LH;
    }
    cy += 4;
  }
  for (const side of ["in", "out"]) {
    for (const p of (n.ports?.[side] || [])) {
      const pos = portPos[`${n.id}/${p.id}`];
      if (pos) grp.appendChild(SHAPE_FN[p.kind](pos.x, pos.y, PORT_R, KIND_COLOR_RAW[p.kind]));
    }
  }
}

function renderEdges() {
  edgePaths = {};
  const isTB = (FLOW.meta.direction || "LR") === "TB";
  for (const e of FLOW.edges) {
    const vs = visibleOf(e.source), vt = visibleOf(e.target);
    if (vs === vt) { edgePaths[e.id] = { hidden: true }; continue; }
    const a = endpointPos(e, "source"), b = endpointPos(e, "target");
    if (!a || !b) { edgePaths[e.id] = { hidden: true }; continue; }
    const off = Math.max(42, (isTB ? Math.abs(b.y - a.y) : Math.abs(b.x - a.x)) / 2);
    const d = !isTB
      ? `M ${a.x} ${a.y} C ${a.x + off} ${a.y}, ${b.x - off} ${b.y}, ${b.x} ${b.y}`
      : `M ${a.x} ${a.y} C ${a.x} ${a.y + off}, ${b.x} ${b.y - off}, ${b.x} ${b.y}`;
    const color = KIND_COLOR_RAW[e.kind];
    const path = el("path", { d, class: "edge-path", stroke: color, "data-edge": e.id }, gEdges);
    const len = path.getTotalLength();
    // 넓은 투명 히트 영역 — 엣지 클릭용 (노드 위 레이어)
    const hit = el("path", { d, class: "edge-hit", "data-edge": e.id }, gEdgeHits);
    hit.addEventListener("click", (ev) => { ev.stopPropagation(); openEdgePanel(e.id); });
    edgePaths[e.id] = { el: path, len, hidden: false };
    drawDecoration(e, path, len, color);
  }
}
function drawDecoration(e, path, len, color) {
  if (!e.decoration) return;
  const tangentAt = (l) => {
    const p1 = path.getPointAtLength(Math.max(0, l - 2)), p2 = path.getPointAtLength(Math.min(len, l + 2));
    const dx = p2.x - p1.x, dy = p2.y - p1.y, m = Math.hypot(dx, dy) || 1;
    return { x: dx / m, y: dy / m };
  };
  const perp = (t) => ({ x: -t.y, y: t.x });
  if (e.decoration === "one-to-one") {
    for (const l of [10, len - 10]) {
      const p = path.getPointAtLength(l), t = tangentAt(l), pp = perp(t);
      el("line", { x1: p.x - pp.x * 5, y1: p.y - pp.y * 5, x2: p.x + pp.x * 5, y2: p.y + pp.y * 5,
                   class: "edge-deco", stroke: color }, gEdges);
    }
  } else if (e.decoration === "one-to-many") {
    const l = len - 4, base = len - 14;
    const p = path.getPointAtLength(l), b = path.getPointAtLength(base), t = tangentAt(base), pp = perp(t);
    for (const s of [-1, 0, 1]) {
      el("line", { x1: b.x, y1: b.y, x2: p.x + pp.x * 6 * s, y2: p.y + pp.y * 6 * s,
                   class: "edge-deco", stroke: color }, gEdges);
    }
  } else if (e.decoration === "optional") {
    const p = path.getPointAtLength(12);
    el("circle", { cx: p.x, cy: p.y, r: 4, fill: "none", class: "edge-deco", stroke: color }, gEdges);
  }
}

/* ================= 상시 입자 ================= */
function renderAmbientInit() {
  ambient = [];
  for (const [eid, ep] of Object.entries(edgePaths)) {
    if (ep.hidden) continue;
    const rate = FLOW.stream?.rates?.[eid] || 1;
    const count = Math.max(1, Math.round(ep.len / 150 * Math.min(rate, 3)));
    for (let i = 0; i < count; i++) ambient.push({ eid, off: (ep.len / count) * i });
  }
  drawAmbient(true);
}
function drawAmbient(rebuild) {
  if (rebuild) gParticles.innerHTML = "";
  if (!motionOn) { gParticles.innerHTML = ""; return; }
  ambient.forEach((p, i) => {
    const ep = edgePaths[p.eid]; if (!ep || ep.hidden) return;
    const pos = ep.el.getPointAtLength(p.off % ep.len);
    const kind = edgesById[p.eid].kind;
    let node = gParticles.childNodes[i];
    if (rebuild || !node) {
      node = SHAPE_FN[kind](0, 0, 2.6, KIND_COLOR_RAW[kind]);
      node.classList.add("particle");
      gParticles.appendChild(node);
    }
    node.setAttribute("transform", `translate(${pos.x} ${pos.y})`);
  });
}

/* trace 스텝이 탄 엣지를 찾는다 — 엣지 패널이 "이 구간을 지나는 흐름"을 뽑을 때 쓴다 */
function stepEdgeOf(idx) {
  if (!FLOW.trace || idx <= 0) return null;
  const s = FLOW.trace.steps[idx];
  if (s.via && edgesById[s.via]) return edgesById[s.via];
  const prev = FLOW.trace.steps[idx - 1].at;
  return FLOW.edges.find(e => e.source === prev && e.target === s.at) || null;
}

/* ================= 상세 패널 ================= */
function markPanelTarget() {
  document.querySelectorAll(".node.panel-open").forEach(g => g.classList.remove("panel-open"));
  document.querySelectorAll(".edge-path.panel-open").forEach(g => g.classList.remove("panel-open"));
  if (panelNodeId) {
    const g = document.querySelector(`.node[data-id="${panelNodeId}"]`);
    if (g) g.classList.add("panel-open");
  }
  if (panelEdgeId && edgePaths[panelEdgeId] && !edgePaths[panelEdgeId].hidden) {
    edgePaths[panelEdgeId].el.classList.add("panel-open");
  }
}
function closePanel() {
  panelNodeId = null; panelEdgeId = null;
  $("detail-panel").classList.remove("open");
  markPanelTarget();
}
function nodeSteps(nodeId) {
  if (!FLOW.trace) return [];
  return FLOW.trace.steps.map((s, i) => ({ ...s, _idx: i })).filter(s => s.at === nodeId);
}
function jumpButton(id, label) {
  return `<button class="jump" data-jump="${esc(id)}">${esc(label)}</button>`;
}
function bindJumps() {
  document.querySelectorAll("#panel-body .jump").forEach(b => {
    b.addEventListener("click", () => {
      const id = b.getAttribute("data-jump");
      if (nodesById[id]) openNodePanel(id);
      else if (edgesById[id]) openEdgePanel(id);
    });
  });
}
function openNodePanel(nodeId) {
  const n = nodesById[nodeId]; if (!n) return;
  panelNodeId = nodeId; panelEdgeId = null;
  const ic = iconOf(n);
  $("panel-title").textContent = `${ic ? ic + " " : ""}${n.label}`;
  let html = `<div class="meta-line">${esc(n.type)}${n.role ? " · " + esc(n.role) : ""}${n.sublabel ? " · " + esc(n.sublabel) : ""}</div>`;

  // 개요
  if (n.detail) html += `<p class="detail-text">${esc(n.detail)}</p>`;
  if (n.type === "group") {
    html += `<div class="meta-line">내부 노드 ${countDescendants(n.id)}개 · ${collapsed.has(n.id) ? "접힘 (제목 클릭으로 펼침)" : "펼침"}</div>`;
  }
  // 여기서 일어나는 일
  const steps = nodeSteps(nodeId);
  if (steps.length) {
    html += `<div class="sec-head">여기서 일어나는 일</div>`;
    for (const s of steps) {
      html += `<div class="step-block">${esc(s.narration)}</div>`;
    }
  }
  // 패킷 변형
  const allChanges = steps.flatMap(s => resolvedChanges[s._idx] || []);
  if (allChanges.length) {
    html += `<div class="sec-head">패킷 변형</div>`;
    for (const c of allChanges) {
      if (c.kind === "set") {
        html += `<div class="mech-rewrite">${esc(c.layerName)}.${esc(c.field)}: <span class="from">${esc(c.from)}</span> <span class="arrow">→</span> <span class="to">${esc(c.to)}</span></div>`;
      } else if (c.kind === "pop") {
        html += `<div class="mech-rewrite"><span class="from">[${esc(c.layerName)}]</span> 계층 벗겨짐</div>`;
      } else if (c.kind === "push") {
        html += `<div class="mech-rewrite"><span class="to">[${esc(c.layerName)}]</span> 계층 씌워짐</div>`;
      } else if (c.kind === "lock") {
        html += `<div class="mech-rewrite">🔒 [${esc(c.layerName)}] 암호화${c.note ? " — " + esc(c.note) : ""}</div>`;
      } else if (c.kind === "unlock") {
        html += `<div class="mech-rewrite">🔓 [${esc(c.layerName)}] 복호화</div>`;
      }
    }
  }
  // 내부 동작
  if ((n.mechanisms || []).length) {
    html += `<div class="sec-head">내부 동작</div>`;
    const sel = new Set(steps.flatMap(s => s.mechanismEvent?.select || []));
    for (const m of n.mechanisms) html += renderMechanism(m, sel);
  }
  // 연결
  const ins = FLOW.edges.filter(e => e.target === nodeId);
  const outs = FLOW.edges.filter(e => e.source === nodeId);
  if (ins.length || outs.length) {
    html += `<div class="sec-head">연결</div>`;
    for (const e of ins) {
      const from = nodesById[e.source];
      html += `<div class="conn-row">⬅ ${jumpButton(e.source, (iconOf(from) ? iconOf(from) + " " : "") + from.label)}
        <span class="conn-kind" style="color:${KIND_COLOR_RAW[e.kind]}">${esc(e.kind)}</span>
        ${e.label ? `<span class="conn-label">${esc(e.label)}</span>` : ""}
        ${e.ratio ? `<span class="conn-ratio">비율 ${esc(e.ratio)}</span>` : ""}
        ${jumpButton(e.id, "엣지")}</div>`;
    }
    for (const e of outs) {
      const to = nodesById[e.target];
      html += `<div class="conn-row">➡ ${jumpButton(e.target, (iconOf(to) ? iconOf(to) + " " : "") + to.label)}
        <span class="conn-kind" style="color:${KIND_COLOR_RAW[e.kind]}">${esc(e.kind)}</span>
        ${e.label ? `<span class="conn-label">${esc(e.label)}</span>` : ""}
        ${e.ratio ? `<span class="conn-ratio">비율 ${esc(e.ratio)}</span>` : ""}
        ${jumpButton(e.id, "엣지")}</div>`;
    }
  }
  if (!n.detail && !steps.length && !(n.mechanisms || []).length && !ins.length && !outs.length) {
    html += `<div class="meta-line">상세 정보 없음</div>`;
  }
  $("panel-body").innerHTML = html;
  bindJumps();
  $("detail-panel").classList.add("open");
  markPanelTarget();
}
function openEdgePanel(edgeId) {
  const e = edgesById[edgeId]; if (!e) return;
  panelEdgeId = edgeId; panelNodeId = null;
  const from = nodesById[e.source], to = nodesById[e.target];
  $("panel-title").textContent = `${from.label} → ${to.label}`;
  let html = `<div class="meta-line">엣지 · <span style="color:${KIND_COLOR_RAW[e.kind]}">${esc(e.kind)}</span>${e.ratio ? " · 비율 " + esc(e.ratio) : ""}</div>`;
  if (e.label) html += `<p class="detail-text">${esc(e.label)}</p>`;
  if (e.decoration) html += `<div class="meta-line">${esc(DECO_LABEL[e.decoration] || e.decoration)}</div>`;
  html += `<div class="sec-head">양끝</div>`;
  html += `<div class="conn-row">출발 ${jumpButton(e.source, (iconOf(from) ? iconOf(from) + " " : "") + from.label)}</div>`;
  html += `<div class="conn-row">도착 ${jumpButton(e.target, (iconOf(to) ? iconOf(to) + " " : "") + to.label)}</div>`;
  // 이 엣지를 타는 스텝
  if (FLOW.trace) {
    const rides = FLOW.trace.steps.map((s, i) => ({ s, i })).filter(({ i }) => {
      const edge = stepEdgeOf(i);
      return edge && edge.id === edgeId;
    });
    if (rides.length) {
      html += `<div class="sec-head">이 구간을 지나는 흐름</div>`;
      for (const { s } of rides) {
        html += `<div class="step-block">${esc(s.narration)}</div>`;
      }
    }
  }
  $("panel-body").innerHTML = html;
  bindJumps();
  $("detail-panel").classList.add("open");
  markPanelTarget();
}
function renderMechanism(m, sel) {
  const title = esc(m.title || MECH_LABEL[m.type] || m.type);
  let body = "";
  if (m.type === "table-lookup") {
    body = `<table class="mech-table">`;
    if (m.columns) body += `<tr>${m.columns.map(c => `<th>${esc(c)}</th>`).join("")}</tr>`;
    for (const r of m.rows || []) {
      body += `<tr class="${sel.has(r.id) ? "sel" : ""}">${(r.cells || []).map(c => `<td>${esc(c)}</td>`).join("")}</tr>`;
      if (r.note) body += `<tr class="${sel.has(r.id) ? "sel" : ""}"><td colspan="${(r.cells || []).length}" class="mech-note">${esc(r.note)}</td></tr>`;
    }
    body += `</table>`;
  } else if (m.type === "weighted-select") {
    const total = (m.candidates || []).reduce((s, c) => s + c.weight, 0) || 1;
    body = (m.candidates || []).map(c => {
      const pct = Math.round(c.weight / total * 100);
      const isSel = sel.has(c.id);
      return `<div class="mech-cand ${isSel ? "sel" : ""}">
        <span>${esc(c.label)}</span>
        <span class="bar-wrap"><span class="bar" style="width:${pct}%"></span></span>
        <span class="pct">${pct}%</span>${isSel ? `<span class="check">✓ 선택</span>` : ""}</div>`;
    }).join("");
  } else if (m.type === "rewrite") {
    body = (m.changes || []).map(c =>
      `<div class="mech-rewrite">${esc(c.layer)}.${esc(c.field)}: <span class="from">${esc(c.from)}</span> <span class="arrow">→</span> <span class="to">${esc(c.to)}</span></div>`
    ).join("");
  } else if (m.type === "crypt") {
    body = `<div class="mech-crypt">
      <span class="mode">${m.mode === "decrypt" ? "🔓 복호화" : "🔒 암호화"}</span>
      ${m.cipher ? `<span>암호군: ${esc(m.cipher)}</span>` : ""}
      ${m.layers?.length ? `<span>대상 계층: ${m.layers.map(esc).join(", ")}</span>` : ""}
      ${m.note ? `<span class="mech-note">${esc(m.note)}</span>` : ""}</div>`;
  } else if (m.type === "k8s-resolve") {
    body = `<div class="mech-describe">` + (m.lines || []).map(l => {
      const pad = "  ".repeat(l.indent || 0);
      return `<span class="line ${l.id && sel.has(l.id) ? "sel" : ""}">${pad}${esc(l.text)}</span>`;
    }).join("\n") + `</div>`;
  } else {
    const dump = Object.entries(m).filter(([k]) => k !== "type" && k !== "title")
      .map(([k, v]) => `${k}: ${typeof v === "object" ? JSON.stringify(v) : v}`).join("\n");
    body = `<div class="mech-kv">${esc(dump) || "(데이터 없음)"}</div>`;
  }
  return `<div class="mech-section">
    <div class="mech-head">${title}<span class="mech-type-tag">${esc(m.type)}</span></div>
    <div class="mech-body">${body}</div></div>`;
}

/* ================= 애니메이션 루프 ================= */
function tick(ts) {
  if (lastTs === null) lastTs = ts;
  const dt = Math.max(0, Math.min(64, ts - lastTs)); lastTs = ts;  // 음수 dt 방어

  if (motionOn) {
    for (const p of ambient) {
      const ep = edgePaths[p.eid];
      if (ep && !ep.hidden) p.off = (p.off + AMBIENT_SPEED * dt / 1000) % ep.len;
    }
    drawAmbient(false);
  }
  requestAnimationFrame(tick);
}

/* ================= 레이아웃 갱신 ================= */
function relayout(fitView) {
  computeLayout();
  computePorts();
  render();
  if (fitView) fitViewBox();
}

/* ================= viewBox 팬/줌 ================= */
/* 전체가 화면에 들어가도 글씨가 안 읽히면 소용없다.
   최소 가독 배율(1.0×)을 바닥으로 두고, 그보다 더 줄여야 하는 경우엔
   왼쪽 위(흐름 시작점)를 기준으로 맞춘다 — 나머지는 팬으로 본다. */
const MIN_READABLE_SCALE = 1.0;
function fitViewBox() {
  const wrap = document.getElementById("canvas-wrap");
  const cw = wrap.clientWidth, ch = Math.max(1, wrap.clientHeight);
  const ar = cw / ch;
  let { x, y, w, h } = contentBox;
  if (w / h < ar) { const nw = h * ar; x -= (nw - w) / 2; w = nw; }
  else { const nh = w / ar; y -= (nh - h) / 2; h = nh; }
  if (cw / w < MIN_READABLE_SCALE) {
    const nw = cw / MIN_READABLE_SCALE, nh = nw / ar;
    x = contentBox.x; y = contentBox.y + (contentBox.h - nh) / 2;
    w = nw; h = nh;
  }
  viewBox = { x, y, w, h };
  applyViewBox();
}
function applyViewBox() {
  svg.setAttribute("viewBox", `${viewBox.x} ${viewBox.y} ${viewBox.w} ${viewBox.h}`);
}
function bindPanZoom() {
  /* 클릭과 팬 구분: 누른 자리에서 5px 이상 움직여야 팬 시작.
     pointerdown 즉시 캡처하면 click 이 svg 로 리타게팅되어 노드 클릭이 죽는다 (v0.2 버그) */
  let pending = null, panning = false;
  svg.addEventListener("pointerdown", (ev) => {
    if (ev.target.closest?.("button")) return;
    pending = { x: ev.clientX, y: ev.clientY, id: ev.pointerId };
  });
  svg.addEventListener("pointermove", (ev) => {
    if (!pending) return;
    if (!panning) {
      if (Math.hypot(ev.clientX - pending.x, ev.clientY - pending.y) < 5) return;
      panning = true;
      svg.classList.add("panning");
      svg.setPointerCapture(pending.id);
    }
    const sc = viewBox.w / svg.clientWidth;
    viewBox.x -= (ev.clientX - pending.x) * sc;
    viewBox.y -= (ev.clientY - pending.y) * sc;
    pending.x = ev.clientX; pending.y = ev.clientY;
    applyViewBox();
  });
  const end = () => { pending = null; panning = false; svg.classList.remove("panning"); };
  svg.addEventListener("pointerup", end);
  svg.addEventListener("pointercancel", end);
  svg.addEventListener("wheel", (ev) => {
    ev.preventDefault();
    const factor = ev.deltaY > 0 ? 1.1 : 1 / 1.1;
    const rect = svg.getBoundingClientRect();
    const mx = viewBox.x + (ev.clientX - rect.left) / rect.width * viewBox.w;
    const my = viewBox.y + (ev.clientY - rect.top) / rect.height * viewBox.h;
    viewBox = {
      x: mx - (mx - viewBox.x) * factor,
      y: my - (my - viewBox.y) * factor,
      w: viewBox.w * factor, h: viewBox.h * factor,
    };
    applyViewBox();
  }, { passive: false });
  svg.addEventListener("dblclick", fitViewBox);
  // 빈 캔버스 클릭 → 패널 닫기
  svg.addEventListener("click", (ev) => {
    if (ev.target === svg || ev.target.id === "g-root") closePanel();
  });
}

/* ================= 컨트롤 ================= */
function setSpeed(s) {
  speed = Math.min(4, Math.max(0.25, s));
  $("speed-label").textContent = speed.toFixed(2).replace(/0$/, "") + "×";
}
function setMotion(on) {
  motionOn = on;
  const b = $("btn-motion");
  b.setAttribute("aria-pressed", String(on));
  b.setAttribute("aria-label", "애니메이션 " + (on ? "켜짐" : "꺼짐"));
  drawAmbient(true);
}
function bindControls() {
  $("btn-faster").addEventListener("click", () => setSpeed(speed * 1.25));
  $("btn-slower").addEventListener("click", () => setSpeed(speed / 1.25));
  $("btn-motion").addEventListener("click", () => setMotion(!motionOn));
  $("btn-panel-close").addEventListener("click", closePanel);
  if (reducedMotion) setMotion(false);

  document.addEventListener("keydown", (ev) => {
    if (ev.target.closest?.("input, textarea")) return;
    if (ev.key === "+" || ev.key === "=") $("btn-faster").click();
    else if (ev.key === "-") $("btn-slower").click();
    else if (ev.key === "0") fitViewBox();
    else if (ev.key === "Escape") closePanel();
  });
  bindPanZoom();
  addEventListener("resize", fitViewBox);
}

init();
