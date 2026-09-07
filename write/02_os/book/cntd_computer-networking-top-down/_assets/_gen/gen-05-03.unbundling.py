# 타입 스펙: type-architecture — 한 상자였던 것이 세 조각으로 갈라지고, 조각마다 공급자가 달라진다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §5.5 도입 (SDN 의 네 가지 특징과 unbundling)
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, KR, MONO

W, H = 1000, 620
d = D(W, H, "SECTION 5.5 · UNBUNDLING",
      "한 상자가 세 조각으로 갈라집니다",
      "SDN 이전의 라우터는 데이터 평면과 제어 평면 소프트웨어가 한 상자 안에 수직 통합돼 한 공급자가 팔았다. SDN 은 그것을 스위치·컨트롤러·제어 앱 셋으로 나눈다.",
      "메인프레임이 PC 로 갈라졌던 일과 같은 모양이라고 원문은 적습니다")

d.t(230, 116, "SDN 이전", 12, INK, KR, "middle", 600)
d.t(690, 116, "SDN 이후", 12, ACC, KR, "middle", 600)

# 왼쪽 — 수직 통합된 한 상자
d.box(90, 140, 280, 250, PAPER2, RULE, 1.2, 10)
for i, (name, sub) in enumerate([("제어 평면 소프트웨어", "라우팅 프로토콜 구현"),
                                 ("운영체제", "공급자 고유"),
                                 ("전달 하드웨어", "빠르지만 바꿀 수 없음")]):
    d.box(110, 164 + i * 76, 240, 62, PAPER, f"{MUTED}66", 1.0, 6)
    d.t(230, 188 + i * 76, name, 11, INK, KR)
    d.t(230, 208 + i * 76, sub, 11, MUTED, KR)
d.t(230, 412, "공급자 하나가 통째로 팝니다", 11, MUTED, KR)

d.path("M 396 264 L 448 264", ACC, 2.0, m="acc")

# 오른쪽 — 갈라진 셋
RIGHT = [("제어 앱", "라우팅 · 접근 제어 · 부하 분산", ACC),
         ("SDN 컨트롤러", "망 상태를 갖고 API 를 엽니다", ACC),
         ("패킷 스위치", "일치와 동작만 빠르게 실행", INFO)]
for i, (name, sub, c) in enumerate(RIGHT):
    y = 140 + i * 86
    d.tone(500, y, 380, 68, c, 8, "10", 1.4)
    d.t(690, y + 28, name, 12, c, KR, "middle", 600)
    d.t(690, y + 48, sub, 11, MUTED, KR)
    if i < 2:
        d.path(f"M 690 {y + 68} L 690 {y + 82}", MUTED, 1.2, m="ar")
d.t(690, 412, "조각마다 다른 곳에서 올 수 있습니다", 11, ACC, KR)

d.t(30, 456, "원문이 꼽는 SDN 의 네 가지 특징입니다.", 11, INK, KR, "start", 600)
for i, txt in enumerate(["흐름 기반 전달 — 목적지 IP 하나가 아니라 여러 헤더 필드로 일치를 겁니다",
                         "데이터 평면과 제어 평면의 분리 — 스위치는 표를 실행하고 서버가 표를 정합니다",
                         "제어 기능이 스위치 밖에 — 원격 서버에서 도는 소프트웨어입니다",
                         "프로그래밍 가능한 제어 평면 — 제어 앱이 API 로 데이터 평면을 지정합니다"]):
    d.t(30, 480 + i * 20, f"· {txt}", 11, MUTED, KR, "start")

d.legend(568, [("제어 평면", ACC), ("데이터 평면", INFO), ("한 공급자의 상자", MUTED)])

out = pathlib.Path(__file__).resolve().parent.parent / "05-03.unbundling.svg"
d.save(out)
print("→", out)
