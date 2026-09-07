# 타입 스펙: type-gantt — 시간 축 위의 막대. 슬롯 하나가 곧 한 노드의 구간이고, 네 칸이 한 프레임이다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §6.3.1 Figure 6.9 — 네 노드 TDM·FDM 예 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, KR, MONO

W, H = 940, 524
d = D(W, H, "SECTION 6.3.1 · CHANNEL PARTITIONING",
      "미리 잘라 나눠 주면 부딪히지 않습니다",
      "TDM 은 시간을 잘라 슬롯을 배정하고 FDM 은 주파수를 잘라 대역을 배정한다. 충돌은 사라지지만 혼자 보낼 때도 자기 몫에 묶인다.",
      "원문 Figure 6.9 의 네 노드 예입니다")

NODE_C = [INFO, ACC, OK, MUTED]
AX, AW = 624, 292


def panel(y, h, title, lines):
    d.box(AX, y, AW, h, PAPER2, RULE, 1.0)
    d.t(AX + 16, y + 24, title, 11, INK, KR, "start", 600)
    d.line(AX + 16, y + 34, AX + AW - 16, y + 34, RULE, 0.8)
    for i, (c, s) in enumerate(lines):
        d.t(AX + 16, y + 56 + i * 20, "·", 11, c, KR, "start", 600)
        d.t(AX + 30, y + 56 + i * 20, s, 11, MUTED, KR, "start")


# TDM — 네 칸이 한 프레임, 세 프레임 반복
d.t(24, 116, "TDM — 시간을 자릅니다", 12, INK, KR, "start", 600)
SX, SW, SY, SH = 24, 48, 132, 46
for f in range(3):
    for s in range(4):
        i = f * 4 + s
        x = SX + i * SW
        d.tone(x, SY, SW - 4, SH, NODE_C[s], 4, "1E" if s == 1 else "14", 1.4 if s == 1 else 1.0)
        d.t(x + (SW - 4) / 2, SY + 29, str(s + 1), 13, NODE_C[s], MONO, "middle", 600)

d.line(SX, 188, SX + SW - 4, 188, MUTED, 1.1)
d.t(SX + (SW - 4) / 2, 204, "슬롯", 10, MUTED, KR)
d.line(SX, 218, SX + 4 * SW - 4, 218, MUTED, 1.1)
d.t(SX + (4 * SW - 4) / 2, 234, "프레임 — 네 슬롯이 한 바퀴", 10, MUTED, KR)
d.t(SX + 4 * SW + 24, 234, "이 패턴이 계속 돕니다", 10, SOFT, KR, "start")

panel(132, 112, "TDM 이 얻는 것과 잃는 것", [
    (ACC, "2 번 슬롯은 한 송수신 쌍에 고정입니다"),
    (OK, "충돌이 없고 완벽히 공정합니다"),
    (MUTED, "혼자 보내도 R/4 를 넘지 못합니다"),
])

# FDM — 대역을 자릅니다
d.t(24, 274, "FDM — 주파수를 자릅니다", 12, INK, KR, "start", 600)
FY, FH, FW = 290, 28, 480
for i in range(4):
    y = FY + i * (FH + 6)
    d.tone(24, y, FW, FH, NODE_C[i], 4, "1E" if i == 1 else "14", 1.4 if i == 1 else 1.0)
    d.t(24 + FW / 2, y + 19, f"노드 {i + 1} 전용 대역 · R/4", 11, NODE_C[i], KR, "middle", 600)
FBOT = FY + 4 * (FH + 6) - 6
d.line(520, FY, 520, FBOT, RULE, 1.2)
d.t(532, (FY + FBOT) / 2 + 4, "한 링크", 11, MUTED, KR, "start")

panel(290, 112, "FDM 이 하는 일", [
    (INFO, "R bps 하나를 R/4 짜리 넷으로 나눕니다"),
    (MUTED, "장점도 단점도 TDM 과 같습니다"),
    (MUTED, "셀룰러·WiFi·블루투스·위성에 쓰입니다"),
])

d.line(24, 440, W - 48, 440, RULE, 0.8)
d.t(24, 462, "CDMA 는 시간도 주파수도 아닌 코드를 나눠 줍니다. 3G 셀룰러의 기반 기술이었으나 4G·5G 에서는 다른 기술로 바뀌었습니다.",
     11, MUTED, KR, "start")

d.legend(484, [("추적하는 몫 — 노드 2", ACC), ("노드 1", INFO), ("노드 3", OK), ("노드 4", MUTED)])

out = pathlib.Path(__file__).resolve().parent.parent / "06-02.tdm-fdm.svg"
d.save(out)
print("→", out)
