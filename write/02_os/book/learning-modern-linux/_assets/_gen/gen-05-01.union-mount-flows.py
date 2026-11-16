# 05-01 §8 — 유니온 마운트의 쓰기 두 흐름. 실습 이름(a-view·a-upper·image·b-view)을 lifeline 으로 세우고
#           위에는 copy-up(실습 22), 아래에는 삭제·화이트아웃(실습 20)을 같은 lifeline 위에 그린다.
#           형제 도식 05-01.union-mount-shared 의 층 이름(보이는 / · 위층 · 이미지)과 색을 그대로 쓴다.
# 타입 스펙: type-sequence — 참여자 = 디렉터리 넷, 시간은 위→아래, 메시지 = 층 사이를 오가는 파일·조회.
#           accent 는 copy-up 화살표 하나(파일 통째 복사). 반환은 점선.
# 근거: 학습 실습(OrbStack lml-ubuntu, 2026-11-16). 원 요청서 relay-w3-union-mount-flows-20261116-2155.md 의
#       실습 20(rm a-view/etc/motd → a-upper/etc 에 c 0,0 motd, image/etc/motd 22 바이트, b-view 에 motd)과
#       실습 22(echo "one more line" >> a-view/usr/big.bin → du a-upper 4.0K → 201M, image 201M).
#       실습 머신은 btrfs 라 사본이 블록을 공유했다 → 각주 한 줄로만 밝힌다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 896
d = D(W, H, "LEARNING MODERN LINUX · 05-01 §8",
      "copy-up 과 화이트아웃 — 쓰기는 위층에만 남는다",
      "lifeline 넷은 왼쪽부터 컨테이너 A 가 보는 a-view, A 의 위층 a-upper, 공유 이미지 image, 컨테이너 B 가 "
      "보는 b-view 다. 위 흐름은 A 가 big.bin(200M) 끝에 한 줄을 덧붙이는 경우다. 위층에 big.bin 이 없어서 "
      "image 의 파일을 통째로 a-upper 로 복사(copy-up)하고 그 사본에 덧붙인다. 이후 A 는 위층 사본을 보고, "
      "B 는 image 의 원본을 그대로 본다. du 는 a-upper 4.0K 에서 201M 으로 늘고 image 는 201M 그대로다. "
      "아래 흐름은 A 가 /etc/motd 를 지우는 경우다. image 는 읽기 전용이라 지우지 못하고 a-upper/etc/motd 에 "
      "장치 번호 0,0 인 문자 장치(화이트아웃)가 생긴다. 이후 A 의 조회는 위층의 화이트아웃에서 멈춰 없음이 되고 "
      "아래 image 로 내려가지 않는다. image/etc/motd 22 바이트는 그대로이고 B 는 여전히 motd 를 본다.",
      "copy-up 은 파일을 통째로 위층에 복사하고, 삭제는 위층에 화이트아웃을 남겨 아래 원본을 가린다")

CX = {"a-view": 128, "a-upper": 336, "image": 544, "b-view": 752}   # lifeline 간격 208
LW, HY, HH = 176, 128, 52          # lane 머리 폭·위치·높이
ROW = 48                           # 메시지 행 간격


def msg(a, b, y, label, c, mk, fam=KR, dash=None, sub=None, sw=1.5):
    x1, x2 = CX[a], CX[b]
    s = 1 if x2 > x1 else -1
    d.arrow([(x1 + 6 * s, y), (x2 - 8 * s, y)], c, mk, sw, dash)
    mx = (x1 + x2) / 2
    d.t(mx, y - 10, label, 12, c, fam, "middle", 600)
    if sub:
        d.t(mx, y + 20, sub, 12, MUTED, KR)


def chip(a, y, txt, c, fill=PAPER, fam=MONO, w=None):
    w = w or len(txt) * 7.6 + 20
    d.o.append(f'<rect x="{CX[a] - w / 2}" y="{y - 12}" width="{w}" height="24" rx="4" '
               f'fill="{fill}" stroke="{c}" stroke-width="1.1"/>')
    d.t(CX[a], y + 4, txt, 12, c, fam, "middle", 600)


def rails(y0, y1):
    for x in CX.values():
        d.line(x, y0, x, y1, RULE, 1.0, "3 6")


def section(y, title, cmd):
    d.t(40, y, title, 14, INK, KR, "start", 600)
    d.t(224, y, cmd, 12, MUTED, MONO, "start")
    d.line(40, y + 12, W - 40, y + 12, RULE, 0.8)


# 컨테이너 묶음 머리
d.t(40, HY - 16, "컨테이너 A", 13, INK, KR, "start", 600)
d.t(CX["image"] - LW / 2, HY - 16, "공유 이미지 한 벌", 13, INK, KR, "start", 600)
d.t(CX["b-view"] - LW / 2, HY - 16, "컨테이너 B", 13, INK, KR, "start", 600)

# lane 머리 — 실습 이름 + 형제 도식의 층 이름
for name, sub in (("a-view", "보이는 / · merged"), ("a-upper", "위층 · upperdir"),
                  ("image", "이미지 · lowerdir"), ("b-view", "보이는 / · merged")):
    x = CX[name] - LW / 2
    if name == "image":
        d.tone(x, HY, LW, HH, ACC, 6, "1F", 1.4)
    else:
        d.box(x, HY, LW, HH, PAPER2, RULE, 1.0, 6)
    d.t(CX[name], HY + 22, name, 14, INK, MONO, "middle", 600)
    d.t(CX[name], HY + 40, sub, 12, MUTED, KR)

# ── 위: copy-up (실습 22) ─────────────────────────────
S1 = HY + HH + 40                  # 220
section(S1, "copy-up", 'echo "one more line" >> a-view/usr/big.bin')
Y1 = S1 + 56                       # 276
rails(S1 + 24, Y1 + 4 * ROW + 16)
msg("a-view", "a-upper", Y1, "1 쓰기로 열기", MUTED, "ar")
d.t(CX["a-upper"] + 16, Y1 + 4, "big.bin 없음", 12, MUTED, KR, "start")
msg("image", "a-upper", Y1 + ROW, "2 copy-up · 파일 통째 200M", ACC, "acc",
    sub="a-work 에서 만든 뒤 옮김", sw=2.2)
y3 = Y1 + 2 * ROW + 12             # 사본에 덧붙임 (self)
x = CX["a-upper"]
d.path(f"M {x + 8} {y3 - 12} L {x + 56} {y3 - 12} L {x + 56} {y3 + 12} L {x + 12} {y3 + 12}", INK, 1.4, "ar")
d.t(x + 68, y3 + 4, "3 사본 끝에 덧붙임", 12, INK, KR, "start", 600)
Y4 = Y1 + 3 * ROW + 16
msg("a-upper", "a-view", Y4, "4 이후 A 는 위층 사본", OK, "ok", dash="5 4")
msg("image", "b-view", Y4, "B 는 원본 그대로", INFO, "info", dash="5 4")
YD = Y4 + ROW                      # du 실측
chip("a-upper", YD, "du 4.0K → 201M", ACC)
chip("image", YD, "du 201M 그대로", MUTED)
d.t(40, YD + 40, "파일 단위 통째 복사 — 한 줄 덧붙임에도 200M 전부", 13, INK, KR, "start", 600)
d.t(40, YD + 60, "ext4 기준 실제 복사 · btrfs·XFS(reflink) 는 블록 공유", 12, SOFT, KR, "start")

# ── 아래: 삭제·화이트아웃 (실습 20) ───────────────────
S2 = YD + 104
section(S2, "삭제 · 화이트아웃", "rm a-view/etc/motd")
Z1 = S2 + 56
rails(S2 + 24, Z1 + 3 * ROW + 16)
msg("a-view", "a-upper", Z1, "1 rm /etc/motd", WARN, "warn", fam=MONO)
Z2 = Z1 + ROW - 4
chip("a-upper", Z2, "motd  c 0,0", WARN, fill=f"{WARN}22")
d.t(CX["a-upper"] + 64, Z2 + 4, "화이트아웃", 12, WARN, KR, "start", 600)
chip("image", Z2, "motd  22 B", MUTED)
d.t(CX["image"] + 64, Z2 + 4, "읽기 전용 · 그대로", 12, SOFT, KR, "start")
Z3 = Z1 + 2 * ROW
msg("a-view", "a-upper", Z3, "2 /etc/motd 조회", INFO, "info")
xb = CX["image"] - 40              # 아래로 내려가다 막히는 자리
d.line(CX["a-upper"] + 8, Z3, xb, Z3, BAD, 1.5, "5 4")
d.line(xb, Z3 - 12, xb, Z3 + 12, BAD, 2.4)
d.t((CX["a-upper"] + xb) / 2 + 4, Z3 - 10, "아래로 안 내려감", 12, BAD, KR, "middle", 600)
Z4 = Z3 + ROW
msg("a-upper", "a-view", Z4, "3 없음", BAD, "bad", dash="5 4")
msg("image", "b-view", Z4, "B 는 motd 그대로", INFO, "info", dash="5 4")
d.t(40, Z4 + 44, "지움 표시는 a-upper 에만 보임 · 디스크는 줄지 않음", 13, INK, KR, "start", 600)

LEG = Z4 + 68
d.legend(LEG, [("copy-up", ACC), ("위층 사본", OK), ("조회 · 비쳐 보임", INFO),
               ("화이트아웃", WARN), ("막힘", BAD)])
assert LEG + 40 <= H, (LEG, H)
d.save("05-01.union-mount-flows.svg")
print("ok 05-01.union-mount-flows")
