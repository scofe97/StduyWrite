# 타입 스펙: type-flowchart — 비트 16칸 블룸 필터에 user:1·2·3 을 넣은 뒤 user:404 는 비트 하나가 0 이라 없음이 확정되고 user:6 은 비트가 모두 1 이라 있을 수 있음으로 갈리는 판단 두 갈래. 갈래마다 같은 네 단계(키 · 위치 · 비트 · 판정)가 반복되어 판정 마름모 대신 마지막 상자가 분기를 나른다(조건 분기를 열 둘로 편 축약).
# 사실 출처: 교육용 계산이다(Redis 구현이 아니다). 위치 = SHA-256(키) 의 앞 4바이트와 다음 4바이트를 각각 정수로 읽어 16 으로 나눈 나머지, 값은 이 생성기가 hashlib 로 직접 계산한다.
#   없음은 보장하고 있음은 추정한다는 성질은 redis.io Bloom filter 문서, 책의 블룸 필터 설명은 추출본 v1.txt 1699~1710행과 PDF 쪽 69 그림(비트 배열 1 0 0 1 1, 키가 없으면 캐시·DB 를 거치지 않음).
# Layout conventions: 비트 칸 폭 48·높이 36·stride 52, 판단 열 둘 폭 300(x=100·520), 상자 높이 36·stride 64, 판정 상자 높이 64. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
import hashlib
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

M = 16


def pos(key):
    dg = hashlib.sha256(key.encode()).digest()
    return int.from_bytes(dg[:4], "big") % M, int.from_bytes(dg[4:8], "big") % M


INSERTS = ["user:1", "user:2", "user:3"]
bits = [0] * M
owner = {}
for n, k in enumerate(INSERTS, 1):
    for p in pos(k):
        bits[p] = 1
        owner.setdefault(p, n)
Q_NO, Q_FP = "user:404", "user:6"
no, fp = pos(Q_NO), pos(Q_FP)
assert [bits[p] for p in no] == [1, 0] and [bits[p] for p in fp] == [1, 1], (no, fp, bits)

W, H = 960, 564
d = D(W, H, "BYTEBYTEGO · 02-01 §2",
      "블룸 필터는 비트 하나가 0 이면 없다고 확정한다",
      "user:1·2·3 을 넣은 16칸 필터에서 user:404 는 막히고 user:6 은 통과해 DB 가 확인합니다",
      "해시 두 개 · 비트 16칸 · 교육용 계산")

X0, CW, CS, Y0, CH = 76, 48, 52, 104, 36
for lab, y in (("비트", Y0 + 23), ("칸 번호", Y0 + 56), ("켠 키", Y0 + 76)):
    d.t(12, y, lab, 12, SOFT, KR, "start")
for i in range(M):
    x = X0 + i * CS
    if bits[i]:
        d.tone(x, Y0, CW, CH, INFO, 4, "22", 1.0)
        d.t(x + CW / 2, Y0 + 24, "1", 13, INFO, MONO, "middle", 600)
        d.t(x + CW / 2, Y0 + 76, str(owner[i]), 12, INFO, MONO)
    else:
        d.box(x, Y0, CW, CH, PAPER2, RULE, 0.8, 4)
        d.t(x + CW / 2, Y0 + 24, "0", 13, MUTED, MONO)
    d.t(x + CW / 2, Y0 + 56, str(i), 12, MUTED, MONO)
for p in no:
    d.o.append(f'<rect x="{X0 + p * CS - 2}" y="{Y0 - 2}" width="{CW + 4}" height="{CH + 4}" rx="5" fill="none" stroke="{ACC}" stroke-width="1.6"/>')
for p in fp:
    d.o.append(f'<rect x="{X0 + p * CS - 2}" y="{Y0 - 2}" width="{CW + 4}" height="{CH + 4}" rx="5" fill="none" stroke="{WARN}" stroke-width="1.6"/>')


def column(x, w, key, ps, bvals, verdict, sub, c):
    cx = x + w / 2
    rows = [(f"조회 {key}", INK), (f"h1={ps[0]} · h2={ps[1]}", INK), (f"비트 {ps[0]}={bvals[0]} · {ps[1]}={bvals[1]}", INK)]
    y = 232
    for txt, tc in rows:
        d.box(x, y, w, 36, PAPER2, RULE, 0.9, 4)
        d.t(cx, y + 23, txt, 13, tc, KR if any("가" <= ch <= "힣" for ch in txt) else MONO, "middle", 600 if y == 232 else 400)
        d.arrow([(cx, y + 38), (cx, y + 60)], MUTED, "ar", 1.4)
        y += 64
    d.tone(x, y, w, 64, c, 4, "14", 1.4)
    d.t(cx, y + 26, verdict, 14, c, KR, "middle", 600)
    d.t(cx, y + 48, sub, 12, MUTED, KR)


column(100, 300, Q_NO, no, [bits[p] for p in no], "0 이 있어 없음 확정", "캐시·DB 로 가지 않음", ACC)
column(520, 300, Q_FP, fp, [bits[p] for p in fp], "모두 1 이라 있을 수 있음", "실제로는 없음 · DB 가 확인", WARN)

d.legend(H - 44, [("1 로 켜진 칸", INFO), ("user:404 가 읽는 칸", ACC), ("user:6 이 읽는 칸", WARN)])
d.save("02-01.bloom-bits.svg")
