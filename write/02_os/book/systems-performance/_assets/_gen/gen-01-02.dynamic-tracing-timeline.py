# 01-02 §4 동적 계측 — 동적 계측이 연구에서 리눅스 · DTrace · BPF 로 오기까지(원서 1.7.3).
# 타입 스펙: type-timeline — 사건이 연도 위에 놓이고 세대가 바꾼 것이 논지다. 눈금 간격은 실제 연도 간격(30 px/년).
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, OK, PAPER2, RULE, KR, MONO

W, H = 1000, 456
X0, PX, BASE = 64, 30, 240

def x(y): return X0 + (y - 1990) * PX

d = DK(W, H, "SYSTEMS PERFORMANCE · 01-02 §4 · SEC 1.7.3",
       "동적 계측이 세대마다 바꾼 것",
       "원서 1.7.3 의 연표. 동적 계측은 1990년대 연구에서 시작해 2000년 리눅스 개발, 2004년 kprobes 병합으로 이어졌지만 잘 알려지지 않고 쓰기 어려웠다. 2005년 DTrace 가 쉽고 안전한 도구로 널리 알렸고, 2013년부터 확장된 BPF 가 BCC · bpftrace 를 떠받친다.",
       "기술은 1990년대부터 있었고, 널리 알려진 것은 2005년 DTrace 이후입니다")

# 구간 띠
d.tone(x(1994), BASE + 12, x(2005) - x(1994), 20, SOFT, 4, "22", 1.0)
d.t((x(1994) + x(2005)) / 2, BASE + 27, "잘 알려지지 않음 · 쓰기 어려움", 12, MUTED, KR, "middle")
d.tone(x(2005), BASE + 12, x(2020) - x(2005), 20, OK, 4, "18", 1.0)
d.t((x(2005) + x(2020)) / 2, BASE + 27, "널리 알려짐", 12, OK, KR, "middle")

d.line(x(1990), BASE, x(2020), BASE, MUTED, 1.0)
for yr in range(1990, 2021, 5):
    d.line(x(yr), BASE - 4, x(yr), BASE + 4, MUTED, 1.0)
    d.t(x(yr), BASE + 56, str(yr), 12, SOFT, MONO, "middle")

EVENTS = [   # 연도, 위(-1)/아래(+1), 두 줄, focal
    (1994, -1, "동적 계측 연구", "Hollingsworth 94", False),
    (1999, +1, "kerninst", "Tamches 99", False),
    (2000, -1, "리눅스에서 첫 개발", "Kleen 08", False),
    (2004, +1, "kprobes", "커널 병합 시작", False),
    (2005, -1, "DTrace", "쉽고 프로덕션 안전", True),
    (2013, +1, "확장 BPF", "BCC · bpftrace", False),
]
for yr, side, l1, l2, focal in EVENTS:
    c = ACC if focal else INK
    cx = x(yr)
    if side < 0:
        d.line(cx, BASE - 8, cx, BASE - 44, RULE, 1.0)
        d.t(cx, BASE - 72, l1, 13, c, KR, "middle", 600)
        d.t(cx, BASE - 54, l2, 12, MUTED, KR, "middle")
    else:
        d.line(cx, BASE + 36, cx, BASE + 84, RULE, 1.0)
        d.t(cx, BASE + 104, l1, 13, c, KR, "middle", 600)
        d.t(cx, BASE + 122, l2, 12, MUTED, KR, "middle")
    d.o.append(f'<circle cx="{cx}" cy="{BASE}" r="{6 if focal else 4}" fill="{c}"/>')
    ylab = "1990년대" if yr == 1994 else str(yr)
    d.t(cx, BASE - 88 if side < 0 else BASE + 140, ylab, 12, SOFT, KR if yr == 1994 else MONO, "middle")

d.legend(BASE + 168, [("DTrace — 널리 알린 전환점", ACC), ("그 뒤 구간", OK), ("그 앞 구간", SOFT)])
d.save("01-02.dynamic-tracing-timeline.svg")
