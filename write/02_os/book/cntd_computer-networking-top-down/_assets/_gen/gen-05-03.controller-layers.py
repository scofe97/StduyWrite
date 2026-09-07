# 타입 스펙: type-layers — 컨트롤러 내부를 아래에서 위로 쌓는다. 원문이 일부러 상향식으로 설명하는 순서 그대로.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §5.5.1 Figure 5.15 (컨트롤러의 세 층)
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, KR, MONO

W, H = 1000, 668
d = D(W, H, "SECTION 5.5.1 · SDN CONTROLLER",
      "컨트롤러는 세 층입니다",
      "SDN 컨트롤러의 내부 구조. 아래로는 장비와 이야기하고, 가운데에 망 전체 상태를 두고, 위로는 제어 앱에 읽기와 쓰기를 열어 준다.",
      "원문이 일부러 아래에서 위로 설명하는 순서를 그대로 따랐습니다")

BX, BW = 170, 660
LAYERS = [
    ("제어 앱", "라우팅 · 접근 제어 · 부하 분산", ACC, 130, 62),
    ("북향 인터페이스", "앱이 상태와 흐름 표를 읽고 씁니다 · 상태 변화 알림 구독", ACC, 208, 56),
    ("망 전체 상태 관리", "호스트 · 링크 · 스위치 상태와 흐름 표 사본, 그리고 계수기 값", INK, 282, 76),
    ("남향 인터페이스", "컨트롤러와 장비 사이의 프로토콜 · 대개 OpenFlow", INFO, 376, 56),
    ("제어되는 장비", "스위치 · 호스트 — 이벤트를 올려보내고 표를 받아 적용", INFO, 450, 62),
]
for name, sub, c, y, h in LAYERS:
    focal = "인터페이스" in name
    d.tone(BX, y, BW, h, c, 8, "10" if focal else "07", 1.5 if focal else 1.1)
    d.t(BX + BW / 2, y + (26 if h > 60 else 24), name, 12, c, KR, "middle", 600)
    d.t(BX + BW / 2, y + (46 if h > 60 else 42), sub, 11, MUTED, KR)

d.t(BX - 14, 250, "위로 열린 API", 11, ACC, KR, "end")
d.t(BX - 14, 410, "아래로 난 프로토콜", 11, INFO, KR, "end")
d.t(BX + BW + 14, 320, "여기가 컨트롤러의", 11, SOFT, KR, "start")
d.t(BX + BW + 14, 338, "본체입니다", 11, SOFT, KR, "start")

# 캡션을 범례 위에 둔다 — 범례선(y)보다 아래로 내려가면 스와치와 겹친다
d.t(30, 546, "논리적으로는 하나지만 실제로는 여러 서버에 흩어져 구현됩니다. 그러면 사건의 순서·일관성·합의 같은", 11, MUTED, KR, "start")
d.t(30, 566, "분산 시스템의 문제가 그대로 따라옵니다. ONOS 와 Orion 이 공들인 자리가 바로 여기입니다.", 11, MUTED, KR, "start")

d.legend(592, [("제어 앱 쪽", ACC), ("장비 쪽", INFO), ("상태", INK)])
d.t(960, 644, "KUROSE-ROSS 9E FIG 5.15", 8, SOFT, MONO, "end")

out = pathlib.Path(__file__).resolve().parent.parent / "05-03.controller-layers.svg"
d.save(out)
print("→", out)
