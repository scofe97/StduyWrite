# 타입 스펙: type-deployment — 소프트웨어가 *어디서 도는가*. 호스트 CPU 와 어댑터 칩이라는 실행 위치에 계층을 얹는다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §6.1.2 Figure 6.2 의 구성 요소와 본문의 역할 분담 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, KR, MONO

W, H = 940, 536
d = D(W, H, "SECTION 6.1.2 · WHERE THE LINK LAYER RUNS",
      "링크 계층은 칩과 CPU 에 걸쳐 있습니다",
      "프로토콜 스택의 어느 층이 호스트 CPU 위 소프트웨어이고 어느 층이 어댑터 칩 위 하드웨어인지. 링크 계층만 그 경계에 걸친다.",
      "원문 Figure 6.2 의 구성 그대로입니다")

# 왼쪽 — 프로토콜 스택
SX, SW, LH = 24, 150, 42
d.t(SX, 100, "프로토콜 스택", 11, SOFT, KR, "start", 600)
for name, y, c in [("애플리케이션", 116, INFO), ("트랜스포트", 162, INFO), ("네트워크", 208, INFO),
                   ("링크", 254, INFO), ("링크", 330, OK), ("물리", 376, OK)]:
    d.tone(SX, y, SW, LH, c, 6, "14", 1.1)
    d.t(SX + SW / 2, y + 26, name, 12, c, KR, "middle", 600)

# 경계 — 이 도식의 초점
d.line(SX, 300, SX + SW, 300, ACC, 1.4)
d.chip(SX + SW / 2, 316, "소프트웨어 · 하드웨어", ACC, 11)

# 가운데 — 호스트
d.box(222, 104, 330, 320, PAPER2, RULE, 1.0)
d.t(387, 128, "호스트", 12, INK, KR, "middle", 600)

d.tone(250, 146, 140, 50, INFO, 6, "14", 1.1)
d.t(320, 176, "CPU", 12, INFO, KR, "middle", 600)
d.tone(402, 146, 122, 50, INFO, 6, "14", 1.1)
d.t(463, 176, "메모리", 12, INFO, KR, "middle", 600)

d.line(320, 196, 320, 220, RULE, 1.1)
d.line(463, 196, 463, 220, RULE, 1.1)
d.line(250, 220, 524, 220, RULE, 1.2)
d.t(524, 214, "마더보드 버스", 10, MUTED, KR, "end")
d.line(387, 220, 387, 248, RULE, 1.1)

d.box(250, 248, 274, 160, PAPER, f"{OK}55", 1.4, 7)
d.t(387, 268, "네트워크 어댑터 (NIC)", 11, OK, KR, "middle", 600)
d.tone(274, 282, 226, 48, OK, 6, "14", 1.1)
d.t(387, 310, "컨트롤러", 12, OK, KR, "middle", 600)
d.tone(274, 346, 226, 48, OK, 6, "14", 1.1)
d.t(387, 374, "물리 전송", 12, OK, KR, "middle", 600)
d.line(387, 330, 387, 346, RULE, 1.1)

# 스택 ↔ 실행 위치 대응 (직각으로만)
d.path("M 178 275 L 200 275 L 200 171 L 244 171", INFO, 1.1, m="info", dash="4 5")
d.path("M 178 376 L 208 376 L 208 306 L 244 306", OK, 1.1, m="ok", dash="4 5")

# 오른쪽 — 무엇을 어디가 맡나
CX, CW = 596, 320
for title, c, y, items in [
    ("소프트웨어가 맡는 일 · 호스트 CPU", INFO, 116,
     ["링크 계층 주소 정보를 조립합니다", "컨트롤러 하드웨어를 활성화합니다",
      "컨트롤러 인터럽트에 응답합니다", "데이터그램을 네트워크 계층으로 올립니다"]),
    ("하드웨어가 맡는 일 · 어댑터 칩", OK, 272,
     ["데이터그램을 프레임에 담습니다", "링크 접속 규칙대로 내보냅니다",
      "오류 검출 비트를 채우고 검사합니다", "프레임을 받아 데이터그램을 꺼냅니다"]),
]:
    d.box(CX, y, CW, 140, PAPER2, f"{c}44", 1.2, 7)
    d.t(CX + 16, y + 24, title, 11, c, KR, "start", 600)
    d.line(CX + 16, y + 34, CX + CW - 16, y + 34, RULE, 0.8)
    for i, it in enumerate(items):
        d.t(CX + 16, y + 56 + i * 22, "·  " + it, 11, MUTED, KR, "start")

d.line(24, 440, W - 48, 440, RULE, 0.8)
d.t(24, 462, "이더넷 기능은 마더보드 칩셋에 통합돼 있거나 값싼 전용 이더넷 칩으로 구현됩니다. "
             "어느 쪽이든 프레이밍·링크 접속·오류 검출은 그 칩 안에서 끝납니다.", 11, MUTED, KR, "start")
d.t(24, 480, "링크 계층은 이 둘의 조합입니다. 스택에서 소프트웨어가 하드웨어를 만나는 자리가 여기입니다.",
     11, MUTED, KR, "start")

d.legend(496, [("호스트 CPU 위 소프트웨어", INFO), ("어댑터 칩 위 하드웨어", OK), ("둘이 만나는 자리", ACC)])

out = pathlib.Path(__file__).resolve().parent.parent / "06-01.adapter-boundary.svg"
d.save(out)
print("→", out)
