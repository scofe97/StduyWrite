# 44-02 §3 — 전체 디스크 암호화에서 키는 passphrase 에서 만들어져 부팅 뒤 메모리에 올라오고 장치에는 암호문만 놓이므로, 장치를 다른 기계로 옮기면 암호문만 읽힌다.
# 본문 근거: 이 노트 §3 「저장 데이터 암호화가 지키는 범위」의 소절 「전체 디스크 암호화와 키의 위치」·「막지 못하는 것과 막는 것」.
# 본문 3절과 겹치지 않게 이 그림에는 보관함 실험(정답 5)의 값을 쓰지 않는다. 보관함은 vault-key 도식이 맡는다.
# 공식 근거: NIST SP 800-38E(저장 장치 데이터 기밀성을 위한 XTS-AES), Linux 커널 문서 dm-crypt(`aes-xts-plain64`).
# 타입 스펙: type-architecture — 경계(원래 기계 · 다른 기계)로 묶은 존 안에 구성요소를 놓고 화살표로 값이 흐르는 길을 잇는다.
#           장치는 원래 기계 존에서 다른 기계 존으로 옮겨 가므로 두 존 사이를 점선 화살표가 건넌다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INK, MUTED, SOFT, RULE, PAPER2, OK, INFO, KR, MONO

W, H = 1000, 484
BW, BH = 136, 64
d = D(W, H, "OSTEP · 44-02 §3",
      "장치를 떼어 가면 암호문만 읽힌다",
      "왼쪽 존은 원래 기계다. 부팅할 때 사용자가 passphrase 를 입력하면 키가 만들어져 메모리에 놓이고, 응용이 쓴 평문은 OS 버퍼를 거쳐 암호화 계층에서 암호문이 되어 장치에 놓인다. "
      "오른쪽 존은 장치를 옮긴 다른 기계다. 그 기계에는 키가 없어서 OS 가 원시 블록을 읽어도 암호문뿐이다.",
      "원래 기계는 키가 메모리에 있어 평문을 만들고, 옮긴 기계는 키가 없어 암호문만 읽는다")

COLS = (28, 228, 428)
ROWS = (132, 236, 340)


def zone(x, y, w, h, name):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{SOFT}0A" stroke="{SOFT}" stroke-width="0.9"/>')
    d.t(x + 16, y + 24, name, 12, MUTED, KR, "start", 600)


def node(x, y, title, sub, c=None, w=BW, dash=False):
    if dash:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{BH}" rx="6" fill="none" stroke="{MUTED}" stroke-width="1.1" stroke-dasharray="4 4"/>')
    elif c:
        d.tone(x, y, w, BH, c, 6, "14", 1.5 if c == ACC else 1.1)
    else:
        d.box(x, y, w, BH, PAPER2, RULE, 1.0, 6)
    d.t(x + w / 2, y + 26, title, 13, c or INK, KR, "middle", 600)
    d.t(x + w / 2, y + 48, sub, 12, MUTED, KR if any("가" <= ch <= "힣" for ch in sub) else MONO)


def harrow(x1, x2, y, label, c=MUTED, m="ar", dash=None):
    d.arrow([(x1 + 2, y), (x2 - 4, y)], c, m, 1.4, dash)
    d.t((x1 + x2) / 2, y - 9, label, 12, c, KR, "middle", 600)


# 존
zone(12, 88, 568, 332, "원래 기계 — 키가 메모리에 있음")
zone(612, 88, 376, 332, "다른 기계 — 장치를 옮긴 뒤")

# 위 줄: 키가 생기는 길
node(COLS[0], ROWS[0], "사용자", "부팅 때 입력")
node(COLS[1], ROWS[1 - 1], "키 유도", "passphrase 로", INFO)
node(COLS[2], ROWS[0], "키", "디스크 키 · 메모리에", OK)
harrow(COLS[0] + BW, COLS[1], ROWS[0] + BH / 2, "입력")
harrow(COLS[1] + BW, COLS[2], ROWS[0] + BH / 2, "계산")

# 가운데 줄: 데이터가 흐르는 길
node(COLS[0], ROWS[1], "응용", "평문 데이터")
node(COLS[1], ROWS[1], "OS 버퍼", "평문")
node(COLS[2], ROWS[1], "암호화 계층", "aes-xts-plain64", INFO)
harrow(COLS[0] + BW, COLS[1], ROWS[1] + BH / 2, "쓰기")
harrow(COLS[1] + BW, COLS[2], ROWS[1] + BH / 2, "넘김")
cx = COLS[2] + BW / 2
d.arrow([(cx, ROWS[0] + BH + 2), (cx, ROWS[1] - 4)], OK, "ok", 1.4)
d.t(cx + 10, ROWS[0] + BH + 26, "키 사용", 12, OK, KR, "start", 600)

# 아래 줄: 장치
node(COLS[2], ROWS[2], "장치", "암호문 블록")
d.arrow([(cx, ROWS[1] + BH + 2), (cx, ROWS[2] - 4)], MUTED, "ar", 1.4)
d.t(cx + 10, ROWS[1] + BH + 26, "암호문 쓰기", 12, MUTED, KR, "start", 600)

# 다른 기계
node(628, ROWS[0], "복호 키", "이 기계에 없음", dash=True)
node(628, ROWS[2], "다른 OS", "원시 블록 읽기")
node(828, ROWS[2], "읽은 결과", "암호문뿐", ACC)
harrow(628 + BW, 828, ROWS[2] + BH / 2, "읽기")
d.arrow([(696, ROWS[0] + BH + 2), (696, ROWS[2] - 4)], MUTED, "ar", 1.2, "3 5")
d.t(706, ROWS[1] + 12, "키를 줄 수 없음", 12, MUTED, KR, "start")

# 장치 이동 — 존 사이를 건넌다
d.arrow([(COLS[2] + BW + 2, ROWS[2] + BH / 2), (624, ROWS[2] + BH / 2)], ACC, "acc", 1.5, "5 4")
d.t(596, ROWS[2] + BH / 2 - 9, "이동", 12, ACC, KR, "middle", 600)

d.legend(436, [("평문이 있는 곳", SOFT), ("암호화가 일어나는 곳", INFO), ("키가 있는 곳", OK), ("읽은 결과", ACC)])
d.save("44-02.key-location.svg")
