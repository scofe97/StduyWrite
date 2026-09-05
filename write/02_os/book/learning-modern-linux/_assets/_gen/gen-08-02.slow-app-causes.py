# 08-02 §1 — 관측된 증상 하나를 자원 범주로 나누고, 범주마다 여는 창을 붙인다.
# 원문("Observability Strategy"): "let's say an application is slow. Let's further assume there are
#       multiple possible reasons for this (not enough memory, too few CPU cycles, network I/O
#       insufficient, etc.)."
# 원문("Monitoring"): "The two types of activities you'll carry out most often in the context of
#       monitoring are as follows: Tracking one or more metrics (over time) · Alerting on a condition"
# 주의: 원문이 이름 붙인 원인은 셋(메모리 · CPU 사이클 · 네트워크 I/O)이고 나머지는 "etc." 로 열어 두었다.
#       디스크 I/O 는 그 열린 자리에 들어가지만 뼈대로 그리지 않았다. 880 폭에서 네 번째 뼈대의
#       한글 라벨이 캔버스 왼쪽 밖으로 나가고, 원문이 이름 붙인 것은 셋뿐이기 때문이다.
#       가지 끝의 도구 이름은 각 도구의 man page 로 확인한 관측 경로이고 원문의 문장이 아니다.
#       accent 를 메모리에 건 것은 저자가 그 가설을 먼저 시험하기 때문이고("Does the performance improve
#       after you provided more RAM to the app?"), 확정된 근본 원인이라는 뜻이 아니다.
# 타입 스펙: type-fishbone — 관측된 결과 하나의 원인을 범주로 묶는다. 60도 뼈대와 가지 눈금은 이 타입의
#           문법이라 직교 연결 규칙에서 면제된다. 축약: 범주당 하위 원인은 둘로 제한했고,
#           하위 원인은 한 줄로 적고 관측 도구를 괄호에 넣었다. 두 줄로 나누면 아래쪽 뼈대에서
#           범주 태그 상자를 덮는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 592
CY, HEAD = 316, 700
d = D(W, H, "LEARNING MODERN LINUX · 08-02 §1",
      "느리다는 증상 하나가 세 범주로 갈린다",
      "저자가 든 느린 앱의 원인 후보를 자원 범주로 묶고, 범주마다 이 장에서 여는 창을 가지 끝에 붙인 것. "
      "범주가 정해져야 §2 부터의 명령이 순서를 갖는다.",
      "저자가 먼저 시험하는 가설은 메모리입니다")

d.line(40, CY, HEAD - 6, CY, INK, 1.4)
d.o.append(f'<path d="M {HEAD - 14} {CY} L {HEAD - 4} {CY}" fill="none" stroke="{INK}" '
           f'stroke-width="1.4" marker-end="url(#acc)"/>')
EW, EH = 156, 84
d.o.append(f'<rect x="{HEAD}" y="{CY - EH / 2}" width="{EW}" height="{EH}" rx="6" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(HEAD + EW / 2, CY - 12, "앱이 느리다", 15, ACC, KR, "middle", 600)
d.t(HEAD + EW / 2, CY + 10, "관측된 증상", 11.5, ACC, KR)
d.t(HEAD + EW / 2, CY + 30, "원인이 아니다", 11.5, MUTED, KR)

BONES = [
    ("메모리", ACC, True, ["스왑으로 밀린다 (vmstat)", "남은 메모리가 적다 (free)"]),
    ("CPU", INFO, False, ["실행 대기가 길다 (vmstat r)", "부하 평균이 오른다 (uptime)"]),
    ("네트워크 I/O", INFO, False, ["누가 쥐고 있나 (lsof)", "소켓 큐가 쌓인다 (ss)"]),
]
for k, (name, col, focal, subs) in enumerate(BONES, start=1):
    above = (k % 2 == 1)
    sgn = -1 if above else 1
    ax = HEAD - 112 - k * 112
    fx, fy = ax - 68, CY + sgn * 119
    d.line(ax, CY, fx, fy, col, 1.6 if focal else 1.1)
    TW, TH = 152, 32
    if focal:
        d.tone(fx - TW / 2, fy - TH / 2, TW, TH, ACC, 4, "12", 1.4)
    else:
        d.box(fx - TW / 2, fy - TH / 2, TW, TH, PAPER2, col, 1.1, 4)
    d.t(fx, fy + 5, name, 12.5, col, KR, "middle", 600)
    for j, m in enumerate((2, 4)):
        tx, ty = ax - 11.2 * m, CY + sgn * 19.6 * m
        d.line(tx, ty, tx - 22, ty, SOFT, 1.0)
        d.t(tx - 28, ty - 4 if above else ty + 12, subs[j], 11, MUTED, KR, "end")

d.t(24, 486, "모니터링에서 가장 자주 하는 일은 둘이라고 저자가 적습니다. 하나 이상의 메트릭을 시간에 걸쳐 "
             "추적하는 것과, 조건에 알림을 거는 것입니다.", 12, MUTED, KR, "start")
d.t(24, 510, "범주를 먼저 세워야 그 둘이 무엇을 대상으로 하는지가 정해집니다.", 12, SOFT, KR, "start")

d.legend(534, [("증상과 먼저 시험할 가설", ACC), ("원문이 이름 붙인 원인", INFO),
               ("하위 원인", MUTED), ("관측 경로", SOFT)])
d.save("08-02.slow-app-causes.svg")
print("ok 08-02.slow-app-causes")
