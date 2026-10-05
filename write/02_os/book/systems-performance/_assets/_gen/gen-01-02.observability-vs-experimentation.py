# 01-02 §1 — 성능 도구의 두 갈래(관측 · 실험)와 그 아래 갈래, 잎마다 1장에 나오는 실제 예.
# 타입 스펙: type-tree — 도구 분류의 부모 → 자식 관계다. 깊이 4(뿌리 + 3단), 단마다 5개 이하.
#           연결선은 꺾은 버스(부모 아래 수직 → 수평 버스 → 자식 위 수직)만 쓴다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, WARN, PAPER2, RULE, KR, MONO

W, H = 976, 520
NW, NH = 160, 48
Y = [104, 192, 280, 368]          # 단마다 y — stride 88

d = DK(W, H, "SYSTEMS PERFORMANCE · 01-02 §1 · SEC 1.7 · 1.8",
       "도구의 두 갈래 — 관측과 실험",
       "원서 1.7·1.8 의 도구 분류. 관측은 시스템을 건드리지 않고 카운터·프로파일링·트레이싱으로 보고, 실험은 합성 워크로드를 건다. 트레이싱은 다시 정적 계측·동적 계측·BPF 로 갈린다. 잎마다 1장에 나오는 예를 붙였다.",
       "프로덕션에서는 관측을 먼저, 그래도 두 손을 다 씁니다")

def node(x, y, name, sub, c=None, w=NW):
    if c: d.tone(x, y, w, NH, c, 6)
    else: d.box(x, y, w, NH, PAPER2, RULE, 1.0, 6)
    d.t(x + w / 2, y + 21, name, 13, c if c else INK, KR, "middle", 600)
    d.t(x + w / 2, y + 39, sub, 12, MUTED, KR, "middle")
    return x + w / 2

def bus(px, py, cxs, cy):
    my = py + (cy - py) / 2
    d.line(px, py, px, my, MUTED, 1.0)
    d.line(min(cxs + [px]), my, max(cxs + [px]), my, MUTED, 1.0)
    for cx in cxs: d.line(cx, my, cx, cy, MUTED, 1.0)

L3 = [24, 200, 376, 616, 792]
L4 = [200, 376, 552]
c_root = 532; c_obs = 280; c_exp = 784

# 연결선 먼저
bus(c_root, Y[0] + NH, [c_obs, c_exp], Y[1])
bus(c_obs, Y[1] + NH, [x + NW / 2 for x in L3[:3]], Y[2])
bus(c_exp, Y[1] + NH, [x + NW / 2 for x in L3[3:]], Y[2])
bus(L3[2] + NW / 2, Y[2] + NH, [x + NW / 2 for x in L4], Y[3])

node(c_root - 80, Y[0], "성능 도구", "1.7 · 1.8")
node(c_obs - 80, Y[1], "관측", "프로덕션에서 먼저", ACC)
node(c_exp - 80, Y[1], "실험", "교란 위험 · 유휴 환경", WARN)
for x, (n, s) in zip(L3, [("카운터", "vmstat · /proc"), ("프로파일링", "CPU 표집 · 플레임 그래프"),
                          ("트레이싱", "이벤트 기반 기록"), ("매크로 벤치마크", "클라이언트 시뮬레이터"),
                          ("마이크로 벤치마크", "iperf · TCP 처리량")]):
    node(x, Y[2], n, s)
for x, (n, s) in zip(L4, [("정적 계측", "tracepoint · USDT"), ("동적 계측", "kprobes · DTrace"),
                          ("BPF", "BCC · bpftrace")]):
    node(x, Y[3], n, s)

d.legend(Y[3] + NH + 40, [("관측 — 시스템을 건드리지 않음", ACC), ("실험 — 합성 워크로드를 건다", WARN)])
d.save("01-02.observability-vs-experimentation.svg")
