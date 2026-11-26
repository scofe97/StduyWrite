# 타입 스펙: type-architecture
# 클러스터에서 웹 서비스 주소 찾기 — 인바운드·아웃바운드 계층 지도
import importlib.util
import pathlib
import sys

sys.path.insert(0, ".")
try:
    from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER, PAPER2, KR, MONO
except ModuleNotFoundError:
    _p = pathlib.Path.home() / "claude/.claude/skills/writing-method/assets/scripts/dd-primitives.py"
    _s = importlib.util.spec_from_file_location("dd", _p)
    _m = importlib.util.module_from_spec(_s)
    _s.loader.exec_module(_m)
    D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER, PAPER2, KR, MONO = (
        _m.D, _m.INK, _m.MUTED, _m.SOFT, _m.RULE, _m.ACC, _m.OK, _m.WARN, _m.INFO, _m.PAPER, _m.PAPER2, _m.KR, _m.MONO
    )

W, H = 920, 580

d = D(
    W, H,
    "KUBERNETES · OPENSHIFT · SERVICE ADDRESS",
    "주소가 정해지는 층 지도 — 인바운드와 아웃바운드",
    "브라우저 요청(1~5)과 앱의 미들웨어 호출(6~8)이 거치는 선언·노출·접속 계층",
    lead="브라우저 요청(1~5)과 앱의 미들웨어 호출(6~8)이 거치는 선언·노출·접속 계층",
)

# 1. Zones (OUTSIDE CLUSTER / INSIDE CLUSTER) — y=96..464 (h=368)
d.o.append(f'<rect x="14" y="96" width="276" height="368" rx="8" fill="rgba(245,245,243,0.02)" stroke="rgba(245,245,243,0.12)" stroke-width="0.8"/>')
d.o.append(f'<rect x="26" y="100" width="116" height="12" rx="2" fill="{PAPER}"/>')
d.t(84, 109, "OUTSIDE CLUSTER", 8, SOFT, MONO, "middle")

d.o.append(f'<rect x="368" y="96" width="538" height="368" rx="8" fill="rgba(245,245,243,0.02)" stroke="rgba(245,245,243,0.12)" stroke-width="0.8"/>')
d.o.append(f'<rect x="380" y="100" width="108" height="12" rx="2" fill="{PAPER}"/>')
d.t(434, 109, "INSIDE CLUSTER", 8, SOFT, MONO, "middle")

def node(x, y, w, h, title, val, cmd, col=INFO, focal=False, val_kr=False, cmd_kr=False):
    sw = 1.4 if focal else 1.1
    op = "18" if focal else "12"
    d.tone(x, y, w, h, col, r=6, op=op, sw=sw)
    cx = x + w / 2
    d.t(cx, y + 24, title, 13, INK, KR, "middle", 600)
    d.t(cx, y + 44, val, 12 if val_kr else 11, col, KR if val_kr else MONO, "middle", 500)
    d.t(cx, y + 64, cmd, 12 if cmd_kr else 11, MUTED, KR if cmd_kr else MONO, "middle")

# Zone 1 Nodes (x=24, w=256, cx=152)
Z1X, Z1W, Z1CX = 24, 256, 152
node(Z1X, 128, Z1W, 76, "브라우저", "portal.apps.<cluster>.example.com", "curl -v --resolve", INFO)
node(Z1X, 252, Z1W, 76, "DNS · hosts", "VIP -> 10.0.0.46", "nslookup · dig", INFO)
node(Z1X, 376, Z1W, 76, "외부 미들웨어 (VM)", "10.0.0.144:3306", "클러스터 밖 직접 IP", WARN, cmd_kr=True)

# Zone 2 Col A Nodes (x=384, w=208, cx=488)
CAX, CAW, CACX = 384, 208, 488
node(CAX, 128, CAW, 76, "Router (L7 프록시)", "VIP 10.0.0.46:443", "get svc -A", INFO)
node(CAX, 252, CAW, 76, "Ingress · 자동 Route", "auth-ingress-7sgb6", "get ingress · route", ACC, focal=True)
node(CAX, 376, CAW, 76, "Service", "ClusterIP · NodePort", "get svc -A", OK)

# Zone 2 Col B Nodes (x=672, w=216, cx=780)
CBX, CBW, CBCX = 672, 216, 780
node(CBX, 128, CBW, 76, "ConfigMap · Secret", "APP_MINIO_URL · *_JDBC_URL", "get cm -o jsonpath", OK)
node(CBX, 252, CBW, 76, "Pod (myapp)", "컨테이너 env · 포트", "get deploy -o yaml", OK, val_kr=True)
node(CBX, 376, CBW, 76, "내부 대상 (minio)", "minio.my-ns.svc", "클러스터 DNS 전용", OK, cmd_kr=True)

# 2. Inbound Arrows (1~5)
# 1. Browser -> DNS
d.arrow([(Z1CX, 204), (Z1CX, 252)], INFO, "info")
d.t(Z1CX + 12, 232, "1. 이름 해석", 12, INFO, KR, "start", 600)

# 2. Browser -> Router
d.arrow([(Z1X + Z1W, 166), (CAX, 166)], INFO, "info")
d.t(332, 152, "2. VIP 접속", 12, INFO, KR, "middle", 600)

# 3. Router -> Ingress/Route
d.arrow([(CACX, 204), (CACX, 252)], ACC, "acc")
d.t(CACX + 12, 232, "3. 호스트·경로", 12, ACC, KR, "start", 600)

# 4. Ingress/Route -> Service
d.arrow([(CACX, 328), (CACX, 376)], INFO, "info")
d.t(CACX + 12, 356, "4. 백엔드 연결", 12, INFO, KR, "start", 600)

# 5. Service -> Pod
d.arrow([(CAX + CAW, 414), (632, 414), (632, 300), (CBX, 300)], INFO, "info")
d.t(632, 286, "5. 파드 전달", 12, INFO, KR, "middle", 600)

# 3. Outbound Arrows (6~8)
# 6. ConfigMap -> Pod (dashed)
d.arrow([(CBCX, 204), (CBCX, 252)], OK, "ok", dash="4 3")
d.t(CBCX + 12, 232, "6. 설정 주입", 12, OK, KR, "start", 600)

# 7. Pod -> 내부 대상
d.arrow([(CBCX, 328), (CBCX, 376)], OK, "ok")
d.t(CBCX + 12, 356, "7. 내부 DNS", 12, OK, KR, "start", 600)

# 8. Pod -> 외부 VM (bottom channel below zones y=464)
d.arrow([(CBX + CBW, 290), (898, 290), (898, 496), (Z1CX, 496), (Z1CX, 452)], WARN, "warn")
d.t(520, 484, "8. 외부 DB 직접 IP (10.0.0.144:3306)", 12, WARN, KR, "middle", 600)

# 4. Legend
LEG_Y = 524
d.legend(LEG_Y, [
    ("인바운드 경로", INFO),
    ("진입 매핑(초점)", ACC),
    ("클러스터 내부 해석", OK),
    ("외부 미들웨어", WARN),
])

d.save("2026-11-26_클러스터에서 웹 서비스 주소 찾기 — Ingress·Route·Service·DNS 추적.address-layers.svg")
