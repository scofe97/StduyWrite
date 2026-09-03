# 01-01 §1 하류 지연의 원인 후보와 호출자가 구분할 수 없다는 사실.
# 본문: 저자는 Preference 가 Customer 를 부르는데 응답이 느려지는 상황을 두고 원인 후보 여섯을 나열한다.
#       핵심은 호출자가 이 여섯을 구분할 수 없다는 것이고, 그래서 원인별 대응이 아니라 증상에 대한
#       일반적 방어책이 필요해진다. 여섯은 저자의 목록 그대로이고 세 묶음은 노트가 성격으로 나눈 것이다.
# 타입 스펙: type-fishbone — 관찰된 결과 하나, 범주별 원인, 범주에 달린 하위 원인. 척추는 가로선,
#           뼈대는 60도 대각(이 타입의 문법이라 직각 엘보 예외), 결과 상자는 accent.
#           축약: 스펙은 뼈대 하나를 확정된 근본 원인으로 accent 하라고 하지만, 이 절의 논지가 바로
#           "어느 뼈대인지 확정할 수 없다"는 것이라 뼈대는 모두 중립으로 두고 결과 상자만 accent 한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 640
d = D(W, H, "ISTIO IN ACTION · 01-01 §1",
      "여섯 갈래가 호출자에게는 한 증상이다",
      "저자가 든 원인 후보 여섯을 성격별로 묶었다. 호출자는 이 중 어느 것인지 가릴 수 없고, "
      "그것이 이 장의 설계를 바꾼다. 확정된 뼈대가 없다는 것이 이 그림의 요점이다.",
      "구분할 수 없으므로 원인별 대응이 아니라 증상에 대한 방어책이 필요해집니다")

CY, HEAD = 320, 684
d.path(f"M 96 {CY} L {HEAD - 8} {CY}", INK, 1.2, m="ar")

bones = [
    ("하류 서비스", ["과부하로 느려짐", "서비스에 버그"], -1),
    ("네트워크 경로", ["방화벽이 지연시킴", "혼잡으로 느려짐"], 1),
    ("하드웨어", ["장비 장애로 우회 중", "NIC 장애"], -1),
]
for k, (cat, subs, side) in enumerate(bones):
    ax = HEAD - 140 - (k + 1) * 120
    fx, fy = ax - 72, CY + side * 168
    d.line(ax, CY, fx, fy, MUTED, 1.1)
    tw = len(cat) * 12 + 24
    bx, by = fx - tw / 2, fy - (26 if side < 0 else 0)
    d.box(bx, by, tw, 26, PAPER2, RULE, 1.0, 4)
    d.t(fx, by + 18, cat, 12, INK, KR, "middle", 600)
    for j, sc in enumerate(subs):
        t = 0.34 + j * 0.30
        tx, ty = ax + (fx - ax) * t, CY + (fy - CY) * t
        d.line(tx, ty, tx + 32, ty, SOFT, 1.0)
        d.t(tx + 40, ty + 4, sc, 11, MUTED, KR, "start")

d.o.append(f'<rect x="{HEAD}" y="{CY - 46}" width="292" height="92" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(HEAD + 146, CY - 16, "Customer 응답이", 13, ACC, KR, "middle", 600)
d.t(HEAD + 146, CY + 6, "심하게 느려졌다", 13, ACC, KR, "middle", 600)
d.t(HEAD + 146, CY + 30, "Preference 가 관찰한 것", 11, MUTED, KR, "middle")

d.t(32, 552, "저자가 못 박는 문장 — 클라우드에서는 인프라가 일시적이며 때때로 사용 불가능하다는 가정 위에서 짓는다", 11, SOFT, KR, "start")
d.t(32, 576, "Preference 입장에서는 이것이 Customer 의 장애인지조차 판별되지 않는다", 11, MUTED, KR, "start")
d.legend(596, [("관찰된 결과", ACC), ("확정할 수 없는 원인 갈래", MUTED)])
d.save("01-01.unknowable-cause.svg")
