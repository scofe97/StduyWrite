# 타입 스펙: type-dp-security-matrix — 어느 요구가 무엇으로 깨지고 어디서 답하는가를 격자로.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §8.1 (책 558~560쪽) —
#   네 성질의 이름과 정의, 각 성질을 다루는 절 번호, 침입자의 두 능력은 원문 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, WARN, BAD, KR, MONO

W, H = 1000, 656
d = D(W, H, "SECTION 8.1 · WHAT IS NETWORK SECURITY",
      "안전하다는 말은 네 가지 요구입니다",
      "하나를 만족시키는 장치가 나머지 셋을 주지 않는다. 그래서 이 장은 절을 나눠 하나씩 맡는다.",
      "네 성질과 담당 절은 원문 §8.1 이 직접 적은 것입니다")

COLS = [(216, 236, "무엇을 요구하나"), (452, 260, "깨지면 벌어지는 일"), (712, 152, "다루는 절")]
ROWS = [
    ("기밀성", "보낸 이와 받기로 한 이만 내용을 이해", "도청자가 가로챈 것을 읽습니다", "§8.2", ACC),
    ("메시지 무결성", "오가는 중에 내용이 바뀌지 않음", "바뀐 것을 모르고 받습니다", "§8.3", INFO),
    ("종단 인증", "상대가 정말 그 사람인지 확인", "다른 개체를 상대로 말합니다", "§8.4", INFO),
    ("운영 보안", "조직의 망 자체를 지킴", "웜·정보 유출·구성 탐색·DoS", "§8.9", INFO),
]
LX, LW = 24, 184
Y0, RH, STRIDE = 176, 56, 64

d.t(LX, 152, "요구", 11, SOFT, KR, "start", 600)
for x, w, name in COLS:
    d.t(x + w / 2, 152, name, 11, SOFT, KR, "middle", 600)
for i, (name, need, broken, sec, c) in enumerate(ROWS):
    y = Y0 + i * STRIDE
    d.tone(LX, y, LW, RH, c, 6, "18" if c is ACC else "12", 1.4 if c is ACC else 1.2)
    d.t(LX + LW / 2, y + RH / 2 + 4, name, 12, c, KR, "middle", 600)
    d.box(COLS[0][0], y, COLS[0][1], RH, PAPER2, RULE, 0.9)
    d.t(COLS[0][0] + COLS[0][1] / 2, y + RH / 2 + 4, need, 11, INK, KR)
    d.tone(COLS[1][0], y, COLS[1][1], RH, BAD, 6, "14", 1.1)
    d.t(COLS[1][0] + COLS[1][1] / 2, y + RH / 2 + 4, broken, 11, BAD, KR)
    d.box(COLS[2][0], y, COLS[2][1], RH, PAPER2, RULE, 0.9)
    d.t(COLS[2][0] + COLS[2][1] / 2, y + RH / 2 + 4, sec, 12, MUTED, MONO)

PY = Y0 + len(ROWS) * STRIDE + 12
d.box(24, PY, 952, 108, PAPER2, RULE, 1.0)
d.t(44, PY + 28, "침입자에게 허용된 능력은 둘뿐입니다", 12, INK, KR, "start", 600)
d.line(44, PY + 40, 956, PY + 40, RULE, 0.8)
CAP = [(44, "엿듣기", "채널의 제어·데이터 메시지를 훔쳐 기록합니다"),
       (516, "변조 · 삽입 · 삭제", "메시지나 그 내용을 바꾸거나 넣거나 지웁니다")]
for x, name, desc in CAP:
    d.t(x, PY + 66, name, 12, WARN, KR, "start", 600)
    d.t(x, PY + 88, desc, 11, MUTED, KR, "start")
d.t(24, PY + 132, "능력은 둘인데 그것으로 훔쳐보기·사칭·세션 탈취·서비스 거부가 모두 나옵니다.",
    11, MUTED, KR, "start")

d.legend(PY + 152, [("이 편이 다루는 요구", ACC), ("뒤 편이 다루는 요구", INFO),
                    ("깨졌을 때", BAD), ("침입자의 능력", WARN)])
out = pathlib.Path(__file__).resolve().parent.parent / "08-01.security-properties.svg"
d.save(out); print("→", out.name)
