# 07-01 §2 — 64비트 가상 주소가 절대값이 아니라 비트맵이라는 것.
# 본문이 요구한 형태: "48비트 비트맵은 PGD·PUD·PMD·PTE 4단계 indirection 을 거쳐 offset 에 닿는다."
# 칸 너비는 비트 수에 비례한다 — 상위 16비트가 왜 눈에 먼저 들어오는지가 그대로 보이게.
# 타입 스펙: type-dp-security-matrix — 격자 문법을 비트 구간 대조 행렬로 쓴다. 열은 비트 구간, 행은 주소 종류.
#           축약: 권한 격자가 아니라 한 행을 구간으로 가르는 1차원 스펙트럼이라 눈금 축을 헤더 행으로 세웠다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 492
LX, LW = 24, 112
HY, RH, RS = 116, 44, 52

# (라벨, 비트 범위, 너비) — 너비는 비트 수에 비례(16·9·9·9·9·12 = 64비트)
COLS = [("63:48", 16, 204), ("47:39", 9, 116), ("38:30", 9, 116),
        ("29:21", 9, 116), ("20:12", 9, 116), ("11:0", 12, 152)]
ROLES = ["부호 확장", "PGD 인덱스", "PUD 인덱스", "PMD 인덱스", "PTE 인덱스", "페이지 내 offset"]

d = DK(W, H, "LINUX KERNEL PROGRAMMING · 07-01 §2",
       "가상 주소는 값이 아니라 비트맵입니다",
       "x86_64 는 64비트 중 하위 48비트만 주소에 쓴다. 그 48비트는 PGD·PUD·PMD·PTE 네 인덱스와 페이지 내 offset 으로 갈리고, 남은 상위 16비트는 커널이면 전부 1, 유저면 전부 0 이라 주소만 보고 둘을 가릴 수 있다.",
       "칸 너비가 곧 비트 수입니다 — 상위 16비트가 주소의 4분의 1을 차지합니다")

xs, x = [], LX + LW + 4
for _, _, w in COLS:
    xs.append(x); x += w
RIGHT = x

# 헤더 — 비트 범위와 비트 수
d.box(LX, HY, LW, RH, PAPER2, RULE, 0.9)
d.t(LX + LW / 2, HY + 27, "비트 구간", 13, SOFT, KR)
for j, (rng, bits, w) in enumerate(COLS):
    focal = j == 0
    if focal:
        d.tone(xs[j], HY, w, RH, ACC, 6, "12", 1.4)
    else:
        d.box(xs[j], HY, w, RH, PAPER2, RULE, 0.9)
    d.t(xs[j] + w / 2, HY + 20, rng, 12, ACC if focal else INK, MONO, "middle", 600)
    d.t(xs[j] + w / 2, HY + 37, f"{bits}비트", 13, ACC if focal else MUTED, KR)

# 행 1 — 각 구간이 무엇을 고르는가
y = HY + RH + 8
d.box(LX, y, LW, RH, PAPER2, RULE, 0.9)
d.t(LX + LW / 2, y + 27, "역할", 13, SOFT, KR)
for j, (_, _, w) in enumerate(COLS):
    c = ACC if j == 0 else (INFO if j < 5 else OK)
    d.tone(xs[j], y, w, RH, c, 6, "14", 1.1)
    d.t(xs[j] + w / 2, y + 27, ROLES[j], 13, c, KR)

# 행 2·3 — KVA 와 UVA 의 상위 16비트가 갈린다
for i, (kind, top, tail, c) in enumerate([
        ("KVA — 커널에서 본 주소", "1111 1111 1111 1111", "0xffff …", INFO),
        ("UVA — 유저에서 본 주소", "0000 0000 0000 0000", "0x0000 …", OK)]):
    y = HY + RH + 8 + (i + 1) * RS
    d.box(LX, y, LW, RH, PAPER2, RULE, 0.9)
    d.t(LX + LW / 2, y + 20, kind.split(" — ")[0], 13, c, MONO, "middle", 600)
    d.t(LX + LW / 2, y + 37, kind.split(" — ")[1], 13, MUTED, KR)
    d.tone(xs[0], y, COLS[0][2], RH, ACC, 6, "12", 1.4)
    d.t(xs[0] + COLS[0][2] / 2, y + 27, top, 12, ACC, MONO)
    # 나머지 48비트는 주소마다 달라 칸마다 값을 적을 수 없다 — 한 칸으로 합쳐 그렇게 적는다.
    d.box(xs[1], y, RIGHT - xs[1], RH, PAPER2, RULE, 0.9)
    d.t((xs[1] + RIGHT) / 2, y + 27, tail + " 아래 48비트는 주소마다 다릅니다", 13, SOFT, KR)

BOT = HY + RH + 8 + 3 * RS
d.t(LX, BOT + 30, "상위 16비트만 보면 KVA 인지 UVA 인지 즉시 갈립니다 — 커널 주소는 0xffff 로, 유저 주소는 0x0000 으로 시작합니다.", 13, ACC, KR, "start")
d.t(LX, BOT + 54, "bit 63 은 페이징 테이블 selector 이기도 합니다 — 설정이면 커널 테이블, 클리어면 프로세스 테이블입니다.", 13, MUTED, KR, "start")
d.t(LX, BOT + 78, "9비트 인덱스가 네 번 반복되는 것이 4-level paging 입니다. 마지막 12비트는 4KB 페이지 안의 자리를 가리킵니다.", 13, MUTED, KR, "start")

d.legend(H - 56, [("상위 16비트 — 이 절의 논점", ACC), ("페이징 테이블 인덱스", INFO), ("페이지 내 offset", OK)])
d.save("07-01.va-bitmap.svg")
print("ok 07-01.va-bitmap")
