# 타입 스펙: type-architecture — 설치 선언(§1)에서 업그레이드 규칙·데이터패스 유지(§2·§3)를 거쳐 노드 단위 CNI 이전·지표 관측(§4·§5)으로 이어지는 Cilium 운영 수명주기 개요.
# 값 근거: 16-01 본문 §1~§5, 원문 ch16.txt 줄 40-393, docs.cilium.io/en/v1.20/ (Cilium 1.20.5)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 560

def fam(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO

d = D(W, H, "ARCHITECTURE · 16-01 OVERVIEW",
      "설치 선언에서 업그레이드·이전·관측까지 Cilium 운영 흐름",
      "16-01 개요도. 왼쪽 Zone 1(§1)은 CLI 와 로컬 Helm 의 값 유실·권한 과다 문제를 Helm 과 GitOps 단일 원천 선언으로 풀되 같은 클러스터 교착에 대비함을 보인다. "
      "가운데 Zone 2(§2·§3)는 한 마이너씩 최신 패치에서 출발해 preflight 와 -f 값 파일로 업그레이드하고, 에이전트 재시작 중 eBPF 데이터패스는 유지되지만 백엔드 교체 틈에 맵이 낡음을 보인다. "
      "오른쪽 Zone 3(§4·§5)은 이중 오버레이(10.245.0.0/16·8473)로 CNI 를 노드 단위 이전하고 9962·9963·9964·9965 포트의 Prometheus 지표로 상태를 확인함을 보인다.",
      lead="칩은 절 번호, 구역 사이 화살표는 읽는 순서, §4 는 다른 CNI 에서 오는 별도 갈래입니다.")

def zone(x, y, w, h, label, lw):
    d.box(x, y, w, h, "rgba(245,245,243,0.02)", "rgba(245,245,243,0.12)", 0.8, r=8)
    d.box(x + 12, y + 4, lw, 12, PAPER, PAPER, 0, r=2)
    d.t(x + 12 + lw / 2, y + 13, label, 8, SOFT, MONO, "middle", 600)

def node(x, y, w, h, title, sub, c, sec, focal=False):
    if focal:
        d.tone(x, y, w, h, c, r=6, op="18", sw=1.4)
    else:
        d.tone(x, y, w, h, c, r=6, op="12", sw=1.0)
    d.chip(x + w - 20, y + 14, sec, c, 10, pad=5)
    d.t(x + (w - 28) / 2 + 4, y + 32, title, 12 if len(title) > 10 else 13, c if focal else INK, fam(title), "middle", 600)
    sub_size = 11 if fam(sub) == MONO else 12
    d.t(x + w / 2, y + 54, sub, sub_size, MUTED, fam(sub), "middle")

# 3개 구역
zone(20, 104, 208, 380, "INSTALL · §1", 92)
zone(268, 104, 392, 380, "UPGRADE · §2 §3", 116)
zone(700, 104, 200, 380, "MIGRATE & OBSERVE · §4 §5", 172)

# 구역 간 직각 연결선 (먼저 그려 노드 뒤에 깐다)
d.path("M 216 308 H 240 Q 248 308 248 300 V 190 Q 248 182 256 182 H 278", OK, 1.4, "ok")
d.path("M 444 308 H 456 Q 464 308 464 300 V 190 Q 464 182 472 182 H 482", OK, 1.4, "ok")
d.path("M 648 432 H 708", OK, 1.4, "ok")

# 구역 1 내부 연결선
d.arrow([(56, 220), (56, 265)], ACC, "acc", 1.4)
d.t(66, 247, "선언형으로", 12, MUTED, KR, "start", 600)
d.arrow([(56, 348), (56, 393)], INFO, "info", 1.2, "4 3")
d.t(66, 375, "같은 클러스터면", 12, MUTED, KR, "start", 600)

# 구역 2a 내부 연결선
d.arrow([(304, 220), (304, 265)], OK, "ok", 1.4)
d.t(314, 247, "이미지 사전 풀", 12, MUTED, KR, "start", 600)
d.arrow([(304, 348), (304, 393)], INFO, "info", 1.2, "4 3")
d.t(314, 375, "값은 파일로", 12, MUTED, KR, "start", 600)

# 구역 2b 내부 연결선
d.arrow([(508, 220), (508, 265)], INFO, "info", 1.4)
d.t(518, 247, "Pod 교체 겹치면", 12, MUTED, KR, "start", 600)
d.arrow([(508, 348), (508, 393)], OK, "ok", 1.4)
d.t(518, 375, "에이전트 복구 뒤", 12, MUTED, KR, "start", 600)

# 구역 3 내부 연결선
d.arrow([(732, 220), (732, 265)], OK, "ok", 1.4)
d.t(742, 247, "대역·포트 분리", 12, MUTED, KR, "start", 600)
d.arrow([(732, 348), (732, 393)], OK, "ok", 1.4)
d.t(742, 375, "상태를 지표로", 12, MUTED, KR, "start", 600)

# 구역 1 노드 (§1)
node(32, 144, 184, 76, "CLI · 로컬 Helm", "값 유실 · 권한 과다", INFO, "§1")
node(32, 268, 184, 80, "Helm + GitOps", "Git 단일 원천 선언", ACC, "§1", focal=True)
node(32, 396, 184, 72, "동일 클러스터 교착", "임시 클러스터 · 복구 잡", INFO, "§1")

# 구역 2a 노드 (§2)
node(280, 144, 164, 76, "연속 마이너 규칙", "한 마이너 · 최신 패치", OK, "§2")
node(280, 268, 164, 80, "preflight · 값 파일", "READY 일치 · -f 적용", OK, "§2")
node(280, 396, 164, 72, "--reuse-values 금지", "이상 시 helm rollback", INFO, "§2")

# 구역 2b 노드 (§3)
node(484, 144, 164, 76, "eBPF 데이터패스", "Pod·서비스·L3 유지", OK, "§3")
node(484, 268, 164, 80, "에이전트 재시작 틈", "맵 낡음 · 백엔드 불일치", INFO, "§3")
node(484, 396, 164, 72, "기동 완료 · 백오프", "서비스 맵 재동기화", OK, "§3")

# 구역 3 노드 (§4·§5)
node(712, 144, 176, 76, "CNI 혼재 섬 분리", "Pod 샌드박스 수명", INFO, "§4")
node(712, 268, 176, 80, "이중 오버레이 이전", "10.245.0.0/16 · 8473", OK, "§4")
node(712, 396, 176, 72, "지표 · 대시보드", "9962·9963·9964·9965", OK, "§5")

d.legend(504, [("문제 · 주의", INFO), ("대응 · 유지", OK), ("이 장의 한 줄", ACC)])
d.save("16-01.chapter-overview.svg")
