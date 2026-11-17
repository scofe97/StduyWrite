# 06-01 stranded resource 와 descheduler — 놀고 있는 메모리가 Pod 하나를 내보내면 다시 쓸 수 있게 된다
# 본문: Fig 6-2 의 값. Node A 는 CPU 4코어를 다 쓰고 메모리 12GB 중 4GB 가 stranded 이며 Node B 는 CPU 1코어·메모리 3GB 가 남는다.
#   descheduler 가 Node A 의 Pod 하나(cpu 1 · memory 2GB, 예시)를 축출하면 A 에 CPU 1코어가 비어 4GB 를 다시 쓸 수 있다.
# 타입 스펙: type-process — 전 · 축출 · 후로 이어지는 시간 순서에 노드별 자원 막대를 얹은 형태다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W = 960
d = D(W, 540, "KUBERNETES PATTERNS · 06-01",
      "descheduler 가 놀고 있는 자원을 다시 쓸 수 있게 만듭니다",
      "Fig 6-2 의 값입니다. Node A 는 CPU 4코어를 모두 쓰고 메모리 12GB 중 4GB 가 stranded 로 남고, Node B 는 CPU 1코어와 메모리 3GB 가 비어 있습니다. "
      "descheduler 가 Node A 의 Pod 하나(cpu 1, memory 2GB, 예시)를 축출하면 A 에 CPU 1코어가 비어 남은 메모리를 다시 쓸 수 있고, 축출된 Pod 는 스케줄러가 다시 놓습니다.",
      lead="막대의 숫자는 코어 수와 GB 이며 축출 대상 Pod 는 예시입니다")

BX0, BW_ = 0, 300          # 막대 길이
def bar(x, y, total, segs, label):
    d.t(x, y - 6, label, 12, MUTED, KR, "start")
    cx = x
    for n, kind, txt in segs:
        w = BW_ * n / total
        if kind == "free":
            d.o.append(f'<rect x="{cx:g}" y="{y}" width="{w:g}" height="26" fill="none" stroke="{MUTED}" stroke-width="1" stroke-dasharray="4 3"/>')
            col = MUTED
        else:
            c = {"pod": INFO, "evict": ACC, "strand": BAD}[kind]
            d.o.append(f'<rect x="{cx:g}" y="{y}" width="{w:g}" height="26" fill="{c}33" stroke="{c}" stroke-width="1.1"/>')
            col = c
        d.t(cx + w / 2, y + 18, txt, 12, col, MONO, "middle", 600)
        cx += w

def node(x, y, name, cpu, mem):
    d.box(x, y, 340, 148, PAPER2, RULE, 0.9, 6)
    d.t(x + 20, y + 26, name, 14, INK, MONO, "start", 600)
    bar(x + 20, y + 60, 4, cpu, "CPU 4코어")
    bar(x + 20, y + 112, 12 if name == "Node A" else 8, mem, "Memory 12GB" if name == "Node A" else "Memory 8GB")

AX, BX = 24, 596
d.t(AX, 112, "전 — 배치가 끝난 모습", 12, SOFT, KR, "start", 600)
d.t(BX, 112, "후 — Pod 하나가 나간 뒤", 12, SOFT, KR, "start", 600)
NA, NB = 128, 296
node(AX, NA, "Node A", [(2, "pod", "2"), (1, "evict", "1"), (1, "pod", "1")],
     [(4, "pod", "4"), (2, "evict", "2"), (2, "pod", "2"), (4, "strand", "stranded 4")])
node(AX, NB, "Node B", [(2, "pod", "2"), (1, "pod", "1"), (1, "free", "free")],
     [(3, "pod", "3"), (2, "pod", "2"), (3, "free", "free")])
node(BX, NA, "Node A", [(2, "pod", "2"), (1, "free", "free"), (1, "pod", "1")],
     [(4, "pod", "4"), (2, "free", "free"), (2, "pod", "2"), (4, "free", "free")])
node(BX, NB, "Node B", [(2, "pod", "2"), (1, "pod", "1"), (1, "free", "free")],
     [(3, "pod", "3"), (2, "pod", "2"), (3, "free", "free")])

# 가운데 — 축출
MX = AX + 340
d.t(MX + 116, NA + 52, "descheduler", 13, WARN, MONO, "middle", 600)
d.path(f"M {MX+8} {NA+74} L {BX-8} {NA+74}", WARN, 1.5, m="warn")
d.t(MX + 116, NA + 98, "Pod 하나 축출", 12, INK, KR)
d.tone(MX + 40, NA + 118, 152, 60, ACC, 6, "16", 1.4)
d.t(MX + 116, NA + 142, "축출된 Pod", 13, ACC, KR, "middle", 600)
d.t(MX + 116, NA + 162, "cpu 1 · memory 2GB", 11, INK, MONO)
d.t(MX + 116, NA + 204, "스케줄러가 다시 놓음", 12, MUTED, KR)

d.legend(NB + 148 + 28, [("Pod", INFO), ("축출 대상", ACC), ("stranded", BAD), ("축출 동작", WARN)])
d.save("06-01.stranded-descheduler.svg")
print("ok stranded-descheduler")
