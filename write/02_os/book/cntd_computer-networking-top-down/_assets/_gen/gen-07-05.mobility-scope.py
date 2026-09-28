# 타입 스펙: type-nested — 포함·범위로 드러나는 계층. 이동의 범위가 넓어질수록 필요한 장치가 늘어난다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §7.5.1 Figure 7.43 —
#   시나리오 (a)(b)(c) 의 구분과 각각에 필요한 것은 원문 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, KR, MONO

W, H = 940, 588
d = D(W, H, "SECTION 7.5.1 · DEGREES OF MOBILITY",
      "얼마나 멀리 움직이면서 끊기지 않을 수 있는가",
      "이동성은 하나가 아니라 세 층이다. 층마다 필요한 장치가 다르고, 이 책은 가운데 층에 집중한다.",
      "세 시나리오 구분은 원문 Figure 7.43 의 것입니다")

LEVELS = [
    (24, 116, 512, 316, "(c) 여러 사업자 망 사이", "사업자들이 핸드오버를 서로 맞춰야 함", MUTED),
    (60, 168, 440, 228, "(b) 한 사업자 망 안의 접속망 사이", "그 사업자가 혼자 핸드오버 지휘", ACC),
    (96, 220, 368, 132, "(a) 하나의 접속망 안", "붙었다 떼었다만 반복", INFO),
]
for x, y, w, h, name, sub, c in LEVELS:
    d.tone(x, y, w, h, c, 8, "10", 1.3)
    d.t(x + 16, y + 24, name, 12, c, KR, "start", 600)
    d.t(x + 16, y + 44, sub, 11, MUTED, KR, "start")
d.t(112, 288, "교실에서 끄고 식당에서 켜는 정도", 11, INFO, KR, "start")
d.t(112, 308, "지금까지 배운 것만으로 충분", 11, INFO, KR, "start")
d.t(76, 366, "IP 데이터그램 송수신·TCP 연결 유지한 채 이동 필요", 11, ACC, KR, "start")
d.t(40, 412, "이 책은 (b) 에 집중 — (c) 는 복잡·사업자 영역 확대로 희소",
    11, MUTED, KR, "start")

PX, PW = 572, 332
d.box(PX, 116, PW, 316, PAPER2, RULE, 1.0)
d.t(PX + 20, 142, "(b) 를 풀려면 답할 것이 셋", 12, INK, KR, "start", 600)
d.line(PX + 20, 154, PX + PW - 20, 154, RULE, 0.8)
QS = [
    ("링크 계층만인가", ["링크 계층만 — 서브넷 안에서만 이동 (WiFi)", "망 계층까지 — 사업자 망 전체 이동 (5G)"]),
    ("누가 왜 시작하나", ["신호 저하 또는 부하 분산이 계기", "판단 알고리즘은 표준 밖 사업자 재량"]),
    ("어떻게 하나", ["기기 상태 이전", "전달 경로 재설정"]),
]
qy = 178
for title, lines in QS:
    d.t(PX + 20, qy, title, 11, ACC, KR, "start", 600)
    for j, ln in enumerate(lines):
        d.t(PX + 20, qy + 20 + j * 18, ln, 11, MUTED, KR, "start")
    qy += 20 + len(lines) * 18 + 16

NY = 452
d.box(24, NY, 880, 62, PAPER2, RULE, 1.0)
d.t(44, NY + 24, "핸드오버 판단에 쓰는 측정값", 12, INK, KR, "start", 600)
d.t(44, NY + 46,
    "5G — 4비트 채널 품질 지시자, WiFi — AP 별 수신 신호 세기 지시자 보고",
    11, MUTED, KR, "start")

d.legend(528, [("장치가 필요 없는 범위", INFO), ("이 장이 다루는 범위", ACC), ("사업자 간 협력이 필요한 범위", MUTED)])

out = pathlib.Path(__file__).resolve().parent.parent / "07-05.mobility-scope.svg"
d.save(out)
print("→", out)
