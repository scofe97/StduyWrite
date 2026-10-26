"""로컬 실행 기반 Remote Control과 클라우드 실행 기반 Web Session의 호스트 및 통신 배치.

# 타입 스펙: type-deployment
"""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, INFO, KR, MONO

W, H = 960, 508
d = D(
    W, H,
    "REMOTE CONTROL VS WEB SESSIONS · DEPLOYMENT",
    "원격 조종과 웹 세션 실행 환경 배치",
    "로컬 개발 머신 중심 원격 조종과 클라우드 인프라 중심 웹 세션의 물리적 구동 위치 및 통신 경로",
    lead="원격 조종은 코드가 로컬에서 돌고, 웹 세션은 클라우드에서 실행되며 로컬로 가져와 이어갈 수 있습니다"
)

# 1. 존 (Zone) 경계 정의 (type-deployment 규약: 배경 직후 가장 먼저 그린다)
ZY, ZH = 100, 336
zones = [
    (24, ZY, 272, ZH, "ZONE: LOCAL"),
    (400, ZY, 208, ZH, "ZONE: REMOTE"),
    (712, ZY, 224, ZH, "ZONE: CLOUD"),
]

for zx, zy, zw, zh, zlabel in zones:
    d.box(zx, zy, zw, zh, fill=PAPER2, stroke=RULE, sw=1.0, r=8)
    d.t(zx + 16, zy + 24, zlabel, 8.5, SOFT, MONO, "start")

# 2. 통신 경로 (Network Paths: 직교 엘보우, 존 사이 간격 중심 배치)
# 경로 1: 원격 제어 (로컬 -> 모바일/브라우저, 아웃바운드 TLS) [Focal! Accent!]
d.arrow([(284, 192), (304, 192)], ACC, "acc", 1.6)
d.arrow([(412, 192), (392, 192)], MUTED, "ar", 1.4)
d.t(348, 148, "아웃바운드 TLS", 12, ACC, KR, "middle", 600)
d.t(348, 252, "인바운드 차단", 11.5, MUTED, KR, "middle")
# Anthropic API 중계점: 로컬 세션과 웹·모바일 클라이언트 사이 메시지를 서버가 중계
d.box(304, 160, 88, 64, fill=PAPER2, stroke=SOFT, sw=1.0, r=6)
d.t(348, 188, "Anthropic", 11.5, INK, MONO, "middle", 600)
d.t(348, 208, "API 중계", 11.5, MUTED, KR, "middle")

# 경로 2: 웹 세션 (브라우저 -> 클라우드 직접 구동)
d.arrow([(596, 192), (724, 192)], INFO, "info", 1.5)
d.t(660, 178, "HTTPS", 12, INFO, MONO, "middle", 600)
d.t(660, 210, "브라우저 접속", 11.5, MUTED, KR, "middle")

# 경로 3: 텔레포트 (클라우드 세션 -> 로컬 머신 회수)
d.arrow([(824, 312), (824, 372), (284, 372)], OK, "ok", 1.5)
d.t(504, 356, "claude --teleport", 12, OK, MONO, "middle", 600)
d.t(504, 388, "브랜치·대화 사본을 로컬로 가져옴", 12, INK, KR, "middle")

# 3. 인프라 노드 및 아티팩트 칩 (Infrastructure Nodes & Artifact Chips)
def draw_node(nx, ny, nw, nh, tag, title, sub, is_focal=False):
    if is_focal:
        d.tone(nx, ny, nw, nh, ACC, 6, "14", 1.4)
    else:
        d.box(nx, ny, nw, nh, fill=PAPER, stroke=RULE, sw=1.0, r=6)
    tag_w = len(tag) * 6.5 + 12
    d.box(nx + 14, ny + 12, tag_w, 18, fill=PAPER2, stroke=RULE, sw=0.8, r=2)
    d.t(nx + 14 + tag_w / 2, ny + 25, tag, 8.5, SOFT, MONO, "middle", 600)
    d.t(nx + 20 + tag_w, ny + 26, title, 13, ACC if is_focal else INK, KR, "start", 600)
    d.t(nx + 16, ny + 50, sub, 11.5, MUTED, KR, "start")

def draw_chip(cx, cy, cw, ch, label, sublabel=None, c=MUTED):
    d.box(cx, cy, cw, ch, fill=PAPER2, stroke=c, sw=0.8, r=4)
    d.t(cx + 10, cy + 18, label, 11.5, INK, MONO if "." in label or "CLI" in label or "App" in label or "UI" in label else KR, "start", 600)
    if sublabel:
        d.t(cx + cw - 10, cy + 18, sublabel, 11, c, MONO if "." in sublabel else KR, "end")

# Node 1: 로컬 개발 머신 (Zone 1)
draw_node(36, 144, 248, 272, "HOST", "로컬 머신", "도구 실행 호스트", is_focal=True)
draw_chip(46, 212, 228, 28, "Claude Code", "로컬 실행", ACC)
draw_chip(46, 248, 228, 28, "로컬 파일시스템", "Git 저장소", MUTED)
draw_chip(46, 284, 228, 28, "로컬 MCP 서버", "도구 연동", INFO)
draw_chip(46, 320, 228, 28, "터미널 세션", "프로세스 상주", MUTED)

# Node 2: 외부 제어 기기 (Zone 2)
draw_node(412, 144, 184, 168, "CLIENT", "원격 기기", "제어 인터페이스")
draw_chip(422, 212, 164, 28, "Claude 앱", "모바일", INFO)
draw_chip(422, 248, 164, 28, "claude.ai", "웹 브라우저", INFO)

# Node 3: 클라우드 인프라 (Zone 3)
draw_node(724, 144, 200, 168, "VM", "클라우드 인프라", "클라우드 가상 환경")
draw_chip(734, 212, 180, 28, "Web Session", "클라우드 러너", MUTED)
draw_chip(734, 248, 180, 28, "독립 샌드박스", "격리 환경", MUTED)

# 4. 범례
d.legend(460, [
    ("원격 조종 (로컬 실행)", ACC),
    ("웹 세션 (클라우드)", INFO),
    ("텔레포트 (로컬로 가져옴)", OK),
])

d.save("05-04.remote-vs-web.svg")
