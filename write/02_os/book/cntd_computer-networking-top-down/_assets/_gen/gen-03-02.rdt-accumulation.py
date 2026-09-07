# 03-02 §1 rdt3.0 — 단계마다 장치가 하나씩 "쌓인다"는 것이 논점.
# 옆의 rdt-evolution.svg 는 단계별 델타(그 단계에서 무엇을 더했나)를 가로로 나열하는데,
# 학습자가 물은 것은 "그래서 rdt3.0 에는 무엇이 다 들어 있나" 였다. 축이 다르므로 둘 다 둔다.
# 본문 근거: "rdt2.2 가 이미 순서 번호를 갖고 있어서 그대로 처리됩니다" — 앞 단계의 장치가
#            사라지지 않고 남는다는 것. 유일한 제거가 rdt2.2 의 NAK 이고 그것도 대체이지 삭제가 아니다.
# 타입 스펙: type-layers — 아래에서 위로 쌓이고, 각 층이 이전 층을 전제로 선다.
#            축약: 각 단계의 FSM 상태 수는 그리지 않는다. 여기서는 장치의 누적만 본다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 676
d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 03-02 §1",
      "장치는 더해질 뿐 사라지지 않습니다",
      "채널에 결함을 하나 더 허용할 때마다 장치가 하나씩 붙고, 앞 단계의 장치는 그대로 남는다. "
      "rdt3.0 이 가진 것은 타이머 하나가 아니라 넷이다.",
      "그래서 rdt3.0 을 이해하려면 앞의 넷을 다 알아야 합니다")

LX, LW = 24, 104          # 단계 이름 칸
CX, CW = 140, 250         # 채널이 하는 짓 칸
DX = 406                  # 장치 칸 시작
RH, Y0 = 88, 128

def chip_w(txt, size=11, pad=7):
    ko = any('가' <= c <= '힣' for c in txt)
    return len(txt) * (size * 1.0 if ko else size * 0.62) + pad * 2

STEPS = [
    ("rdt1.0", "아무 문제 없음", [], None, MUTED),
    ("rdt2.0", "비트를 뒤집음", ["체크섬", "ACK·NAK", "재전송"], "새로 셋", WARN),
    ("rdt2.1", "ACK·NAK 도 뒤집음", ["체크섬", "ACK·NAK", "재전송", "순서 번호"], "새로 하나", MUTED),
    ("rdt2.2", "같음", ["체크섬", "번호 담은 ACK", "재전송", "순서 번호"], "NAK 을 대체", MUTED),
    ("rdt3.0", "패킷을 잃기도 함", ["체크섬", "번호 담은 ACK", "재전송", "순서 번호", "타이머"], "새로 하나", ACC),
]

for i, (name, chan, devs, note, col) in enumerate(STEPS):
    y = Y0 + i * RH
    focal = col is ACC
    if focal:
        d.tone(LX, y, W - LX - 24, RH - 12, ACC, 6, "12", 1.4)
    else:
        d.box(LX, y, W - LX - 24, RH - 12, PAPER2, RULE, 0.9, 6)
    d.t(LX + 16, y + 30, name, 13, col if focal else INK, MONO, "start", 600)
    d.t(LX + 16, y + 52, f"{i + 1}단계", 11, SOFT, MONO, "start")
    d.line(CX - 14, y + 12, CX - 14, y + RH - 24, RULE, 0.8)
    d.t(CX, y + 30, "채널이 하는 짓", 11, SOFT, MONO, "start")
    d.t(CX, y + 52, chan, 11, INK, KR, "start")
    d.line(DX - 18, y + 12, DX - 18, y + RH - 24, RULE, 0.8)
    if not devs:
        d.t(DX, y + 44, "가진 장치가 없습니다. 되먹임조차 필요 없습니다.", 11, SOFT, KR, "start")
        continue
    x = DX
    for j, dv in enumerate(devs):
        w = chip_w(dv)
        carried = j < len(STEPS[i - 1][2]) if i else False
        c = ACC if (focal and j == len(devs) - 1) else (OK if not carried else SOFT)
        if i == 3 and dv == "번호 담은 ACK":
            c = OK
        d.chip(x + w / 2, y + 44, dv, c)
        x += w + 11
    if note:
        d.t(x + 6, y + 48, f"← {note}", 11, MUTED, KR, "start")

d.t(24, Y0 + 5 * RH + 8,
    "아래로 내려갈수록 채널을 더 의심하고, 위에서 내려온 장치는 그대로 남습니다. 유일한 제거가 rdt2.2 의 NAK 인데 그것도 삭제가 아니라 대체입니다.",
    11, MUTED, KR, "start")
d.t(24, Y0 + 5 * RH + 30,
    "그래서 rdt3.0 의 타임아웃이 만든 중복 패킷을 rdt2.1 이 넣어 둔 순서 번호가 받아 냅니다. 단계가 서로를 떠받칩니다.",
    11, SOFT, KR, "start")

d.legend(H - 44, [("rdt3.0 이 마지막으로 더한 것", ACC), ("그 단계에서 새로 붙은 것", OK), ("앞 단계에서 들고 온 것", SOFT)])
d.save("03-02.rdt-accumulation.svg")
print("ok rdt-accumulation")
