# 타입 스펙: type-state — 주체 하나의 상태 전이·가드·재시도. 기기 한 대가 프레임 하나를 보내는 동안의 상태.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §7.3.1 CSMA/CA 네 단계 서술과 Figure 7.20 —
#   DIFS · SIFS · 이진 지수 백오프 · 재시도 시 구간 확대는 원문 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, BAD, KR, MONO

W, H = 940, 612
d = D(W, H, "SECTION 7.3.1 · CSMA/CA",
      "비어 있어도 바로 보내지 않고 세면서 기다립니다",
      "유선과 달리 무선은 보내는 중에 충돌을 못 본다. 그래서 부딪히고 나서 멈추는 대신 부딪힐 일을 줄인다.",
      "네 단계와 대기 이름은 원문 §7.3.1 의 것입니다")

BW, BH = 140, 76
TOP, BOT = 140, 286
NODES = {
    "감지": (24, TOP, "채널 감지", "보낼 프레임이 생김", INFO),
    "DIFS": (208, TOP, "DIFS 만큼 대기", "짧은 고정 시간", INFO),
    "전송": (392, TOP, "전체 프레임 전송", "중간에 멈추지 않음", ACC),
    "ACK": (576, TOP, "ACK 대기", "SIFS 뒤 응답이 옴", INFO),
    "완료": (760, TOP, "완료", "다음 프레임으로", OK),
    "백오프": (208, BOT, "백오프 값 선택", "이진 지수 백오프", MUTED),
    "카운트": (392, BOT, "카운트다운", "바쁘면 값을 얼립니다", MUTED),
}
for x, y, title, sub, c in NODES.values():
    d.tone(x, y, BW, BH, c, 8, "12", 1.2)
    d.t(x + BW / 2, y + 32, title, 12, c, KR, "middle", 600)
    d.t(x + BW / 2, y + 54, sub, 10, MUTED, KR)


def cx(k):
    return NODES[k][0] + BW / 2


def rx(k):
    return NODES[k][0] + BW


HREL = [("감지", "DIFS", "비었음"), ("전송", "ACK", ""), ("ACK", "완료", "성공"),
        ("백오프", "카운트", "")]
for a, b, lab in HREL:
    ya = NODES[a][1] + BH / 2
    d.arrow([(rx(a) + 4, ya), (NODES[b][0] - 4, ya)], MUTED, "ar", 1.3)
    if lab:
        d.t((rx(a) + NODES[b][0]) / 2, ya - 12, lab, 10, SOFT, KR)

d.arrow([(rx("DIFS") + 4, TOP + BH / 2), (NODES["전송"][0] - 4, TOP + BH / 2)], MUTED, "ar", 1.3)

d.arrow([(cx("감지"), TOP + BH + 4), (cx("감지"), BOT + BH / 2), (NODES["백오프"][0] - 4, BOT + BH / 2)],
        MUTED, "ar", 1.3)
d.t(cx("감지") + 8, BOT + BH / 2 - 12, "바빴음", 10, SOFT, KR, "start")

d.arrow([(cx("카운트"), BOT - 4), (cx("카운트"), TOP + BH + 4)], OK, "ok", 1.4)
d.t(cx("카운트") + 10, (TOP + BH + BOT) / 2 + 4, "0 이 되면", 10, OK, KR, "start")

RY = BOT + BH + 46
d.arrow([(cx("ACK"), TOP + BH + 4), (cx("ACK"), RY), (cx("백오프"), RY), (cx("백오프"), BOT + BH + 4)],
        BAD, "bad", 1.4, "5 5")
d.t((cx("ACK") + cx("백오프")) / 2, RY + 18, "ACK 이 안 오면 더 넓은 구간에서 다시 고릅니다", 11, BAD, KR, "middle", 600)

PY = RY + 44
d.box(24, PY, 880, 84, PAPER2, RULE, 1.0)
d.t(44, PY + 26, "유선의 CSMA/CD 와 갈리는 자리", 12, INK, KR, "start", 600)
for i, ln in enumerate([
    "보내면서 받을 수 없어 자기 송신에 묻힌 충돌을 못 봅니다. 그래서 한 번 시작하면 끝까지 보냅니다.",
    "충돌한 프레임을 통째로 버리므로, 부딪히고 멈추는 대신 세면서 기다려 부딪힐 일을 줄입니다.",
]):
    d.t(44, PY + 52 + i * 20, ln, 11, MUTED, KR, "start")

d.legend(PY + 104, [("정상 경로", INFO), ("전송", ACC), ("카운트다운 완료", OK), ("재시도", BAD)])

out = pathlib.Path(__file__).resolve().parent.parent / "07-02.csma-ca-states.svg"
d.save(out)
print("→", out)
