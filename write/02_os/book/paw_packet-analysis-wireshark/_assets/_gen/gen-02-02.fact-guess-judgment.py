# 02-02 §6 — tshark 한 줄의 글자가 사실 · 추측 · 판단 가운데 어디서 왔는가.
# 타입 스펙: type-swimlane — 레인은 글자를 만든 주체 셋(프레임 바이트 · 관습 표 · 여러 프레임 대조)이고,
#           각 조각은 그것을 만든 주체의 레인에만 놓는다.
#           축약: 가로축이 절차의 순서가 아니라 원래 줄 안의 위치다. 그래서 화살표가 없고, 맨 위에 원래 줄을
#           통째로 두어 레인마다 같은 x 에 조각을 떨어뜨린다(같은 객체를 여러 번 그려 보이는 관례).
#           자기 레인이 아닌 조각은 빈 점선 칸으로 남겨 정렬을 유지한다. focal 은 대괄호 판단 조각 하나.
#           줄은 문서용 주소(RFC 5737)로 만든 캡처를 tshark 4.6.8 로 읽은 실제 출력이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 464
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 02-02 §6",
      "한 줄 안의 사실 · 추측 · 판단",
      "tshark 가 보여 준 한 줄을 조각으로 나눠, 프레임 바이트에서 읽은 사실, 포트 표로 짐작한 추측, 앞 프레임과 대조한 판단 가운데 어디서 왔는지 레인마다 갈라 놓은 그림.",
      "대괄호에는 표시가 붙지만 Protocol 열의 추측에는 아무 표시가 없습니다")

CW = 7.2                                   # 12px mono 한 글자 폭 추정
TX0, GAP, CH = 200, 8, 28                  # 조각 시작 x · 조각 사이 · 칩 높이
TOKENS = [  # (글자, 갈래) — 갈래 None 은 레인에 떨어뜨리지 않는 기호
    ("198.51.100.20", "fact"), ("→", None), ("192.0.2.10", "fact"), ("HTTP", "guess"),
    ("92", "fact"), ("[TCP Previous segment not captured]", "judge"), ("HTTP/1.1 200 OK", "fact"),
]
LANES = [  # (갈래, 이름, 서브라벨, 색)
    ("fact",  "사실", "프레임 바이트에서 읽음", INFO),
    ("guess", "추측", "포트 표 · OUI 로 짐작", WARN),
    ("judge", "판단", "앞 프레임과 대조",       ACC),
]

def w4(n): return int(-(-n // 4) * 4)      # 4 의 배수로 올림
pos, x = [], TX0
for txt, kind in TOKENS:
    w = 16 if kind is None else w4(len(txt) * CW + 16)
    pos.append((x, w)); x += w + GAP

# 원래 한 줄
LINE_Y = 116
d.t(24, LINE_Y + 19, "원래 한 줄", 13, INK, KR, "start", 600)
for (txt, kind), (x, w) in zip(TOKENS, pos):
    if kind is None:
        d.t(x + w / 2, LINE_Y + 19, txt, 12, MUTED, MONO)
        continue
    d.box(x, LINE_Y, w, CH, PAPER2, RULE, 1.0, 4)
    d.t(x + w / 2, LINE_Y + 19, txt, 12, INK, MONO)
d.line(24, 160, W - 24, 160, RULE, 0.8)

# 레인 셋 — stride 76, 레인 안 칩은 위에서 16
Y0, RS, LH = 172, 76, 64
for i, (kind, name, sub, c) in enumerate(LANES):
    y = Y0 + i * RS
    if i:
        d.line(24, y - 6, W - 24, y - 6, RULE, 0.6)
    d.t(24, y + 26, name, 14, c, KR, "start", 600)
    d.t(24, y + 46, sub, 13, MUTED, KR, "start")
    cy = y + 16
    for (txt, k), (x, w) in zip(TOKENS, pos):
        if k is None:
            continue
        if k != kind:
            d.o.append(f'<rect x="{x}" y="{cy}" width="{w}" height="{CH}" rx="4" fill="none" '
                       f'stroke="{SOFT}" stroke-opacity="0.45" stroke-width="0.8" stroke-dasharray="3,3"/>')
            continue
        if kind == "judge":
            d.o.append(f'<rect x="{x}" y="{cy}" width="{w}" height="{CH}" rx="4" '
                       f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        else:
            d.tone(x, cy, w, CH, c, 4)
        d.t(x + w / 2, cy + 19, txt, 12, c, MONO)

d.legend(Y0 + len(LANES) * RS + 12,
         [("프레임 바이트에서 읽은 사실", INFO), ("관습으로 붙인 추측", WARN), ("여러 프레임을 대조한 판단", ACC)])
d.save("02-02.fact-guess-judgment.svg")
