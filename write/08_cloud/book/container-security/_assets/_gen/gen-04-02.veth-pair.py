# 타입 스펙: type-architecture — 두 network namespace(컨테이너 28586 · 기본 netns 1)를 zone 으로 묶고 ve1·ve2 케이블로 잇는다. 위는 최종 토폴로지, 아래는 쌍 만들기 → UP → IP 부여 → 경로 추가 네 단계(축약: 단계 줄은 별도 흐름 띠). focal 은 veth 쌍.
# 사실 출처: 노트 L47(lo 하나·DOWN), L56~L59(veth 쌍·ip link add), L71(양 끝 UP·IP 필요), L74~L77(ip addr add·라우팅 경로·호스트와 별개).
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, OK, WARN, BAD, INFO, KR, MONO, PAPER

W, H = 984, 576


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


d = D(W, H, "ARCHITECTURE · 04-02 §1",
      "veth 쌍의 양 끝을 UP 으로 올리고 IP 를 붙여야 바깥과 통신합니다",
      "컨테이너 network namespace 는 DOWN 상태의 lo 하나로 시작한다. ip link add ve1 netns 28586 type veth peer name ve2 netns 1 로 한 끝은 컨테이너, 다른 끝은 기본 namespace 에 꽂는다. "
      "양 끝을 모두 UP 으로 올리고 ip addr add 192.168.1.100/24 dev ve1 로 주소를 붙이면 라우팅 테이블에 192.168.1.0/24 경로가 생긴다.",
      lead="위는 연결이 끝난 모습, 아래는 그 모습을 만드는 순서입니다.")

# zone 두 개
ZY, ZH, ZW = 112, 220, 384
LX, RX = 36, 564
for x, name, sub in ((LX, "컨테이너 network namespace", "netns 28586"), (RX, "기본 network namespace", "netns 1")):
    d.box(x, ZY, ZW, ZH, "#ffffff08", "rgba(191,192,192,0.22)", 1.0, 8)
    d.t(x + 20, ZY + 28, name, 13, INK, KR, "start", 600)
    d.t(x + ZW - 20, ZY + 28, sub, 12, MUTED, MONO, "end")

R1, R2, NH = 160, 248, 64
# 케이블(상자보다 먼저)
cy = R1 + NH // 2
d.line(400, cy, 584, cy, ACC, 2.6)
d.t(492, cy - 12, "veth 쌍", 13, ACC, KR, "middle", 600)
d.t(492, cy + 24, "케이블 양 끝", 12, MUTED, KR, "middle")


def node(x, y, w, title, sub, c=None, tf=MONO):
    fit(title, 13, w - 16)
    fit(sub, 12, w - 16)
    if c:
        d.tone(x, y, w, NH, c, 6, "14", 1.4 if c == ACC else 1.1)
    else:
        d.box(x, y, w, NH)
    d.t(x + w / 2, y + 27, title, 13, c or INK, tf, "middle", 600)
    d.t(x + w / 2, y + 48, sub, 12, MUTED, kr(sub), "middle")


node(56, R1, 148, "lo", "루프백 · DOWN", BAD)
node(220, R1, 180, "ve1", "UP · 192.168.1.100/24", OK)
node(584, R1, 344, "ve2", "UP · 기본 namespace 쪽 끝", OK)
node(56, R2, 344, "라우팅 테이블", "192.168.1.0/24", None, KR)
node(584, R2, 344, "호스트 라우팅 테이블", "컨테이너 것과 별개", None, KR)
d.chip(492, R2 + NH // 2, "각자 따로", MUTED, 12, 8)

# 순서 띠
d.t(36, 364, "만드는 순서", 13, MUTED, KR, "start", 600)
BY, BH, BW, GAP = 380, 132, 204, 32
STEPS = [
    ("1  쌍 만들기", ["ip link add ve1", "netns 28586 type veth", "peer name ve2 netns 1"], WARN, "링크는 DOWN"),
    ("2  양 끝 UP", ["ve1  UP", "ve2  UP"], WARN, "한쪽만으론 안 됨"),
    ("3  IP 부여", ["ip addr add", "192.168.1.100/24 dev ve1"], INFO, "IP 트래픽을 보냄"),
    ("4  경로 추가", ["192.168.1.0/24"], OK, "보낼 수 있는 곳은 이 대역"),
]
for k, (title, lines, c, res) in enumerate(STEPS):
    x = 36 + k * (BW + GAP)
    if k:
        d.arrow([(x - GAP + 2, BY + BH // 2), (x - 4, BY + BH // 2)], SOFT, "soft", 1.3)
    d.box(x, BY, BW, BH)
    fit(title, 13, BW - 16)
    d.t(x + 14, BY + 26, title, 13, INK, KR, "start", 600)
    for n, ln in enumerate(lines):
        fit(ln, 12, BW - 16)
        d.t(x + BW / 2, BY + 52 + n * 18, ln, 12, INFO, MONO, "middle")
    fit(res, 12, BW - 16)
    d.t(x + BW / 2, BY + BH - 14, res, 12, c, KR, "middle", 600)

d.legend(528, [("DOWN·조건부", WARN), ("UP", OK), ("명령", INFO), ("veth 쌍", ACC), ("끊김", BAD)])
d.save(str(ASSETS / "04-02.veth-pair.svg"))
print("ok 04-02 veth-pair")
