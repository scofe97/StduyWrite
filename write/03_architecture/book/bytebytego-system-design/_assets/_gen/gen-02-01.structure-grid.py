# 타입 스펙: type-dp-security-matrix — 쓰임 3행 × (Memcached 값 · Redis 자료 구조 · Redis 값) 3열의 비교 행렬(격자 문법). 윗줄과 아랫줄이 같은 모양으로 이어지고 열마다 값이 어떻게 놓이는지가 갈린다. 초점은 열 머리 하나.
# 사실 출처: 추출본 v1.txt 1607~1618행(hash 클릭·댓글 수 · zset 댓글 사용자 정렬과 중복 제거 · bitmap 로그인 여부)과 PDF 쪽 65 그림,
#   Memcached 개요 문서(서버는 데이터 모양을 모르고 항목은 키·만료·플래그·원시 데이터, 직렬화해 올려야 하며 incr/decr 만 값을 단순하게 다룸) https://docs.memcached.org/,
#   redis.io 자료형 문서(hash·sorted set·bitmap). 키 post:7·post:7:users·login:20261012, 값 120·9·kim·lee·비트 42 는 이 편이 정한 예시 값이다.
# Layout conventions: §2 공식 — left_pad 12, comp_col_w 216, role_col_w 216, role_col_gap 16, header_h 44, 단 header_y 는 dd.py 제목 줄 때문에 96, row_h 48 · stride 56. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

LEFT, COMP_W, GAP0, ROLE_W, ROLE_GAP = 12, 216, 12, 216, 16
HDR_Y, HDR_H, ROW0, ROW_H, STRIDE = 96, 44, 152, 48, 56
W = LEFT + COMP_W + GAP0 + 3 * ROLE_W + 2 * ROLE_GAP + 48
H = ROW0 + 2 * STRIDE + ROW_H + 20 + 44
d = D(W, H, "BYTEBYTEGO · 02-01 §3",
      "Redis 는 값의 모양을 알고 Memcached 는 바이트만 다룬다",
      "같은 쓰임이 Memcached 에서는 직렬화한 값으로, Redis 에서는 자료 구조 하나로 놓입니다",
      "post:7 · 로그인 여부 · 예시 값")


def rx(j):
    return LEFT + COMP_W + GAP0 + j * (ROLE_W + ROLE_GAP)


d.box(LEFT, HDR_Y, COMP_W, HDR_H, PAPER2, RULE, 0.9, 6)
d.t(LEFT + COMP_W / 2, HDR_Y + 27, "쓰임", 12, INK, KR, "middle", 600)
heads = ["Memcached 값", "Redis 자료 구조", "Redis 값"]
for j, h in enumerate(heads):
    if j == 1:
        d.tone(rx(j), HDR_Y, ROLE_W, HDR_H, ACC, 6, "14", 1.4)
        d.t(rx(j) + ROLE_W / 2, HDR_Y + 27, h, 12, ACC, KR, "middle", 600)
    else:
        d.box(rx(j), HDR_Y, ROLE_W, HDR_H, PAPER2, "rgba(191,192,192,0.45)", 0.9, 6)
        d.t(rx(j) + ROLE_W / 2, HDR_Y + 27, h, 12, INK, KR, "middle", 600)

# (쓰임, 부제, Memcached 두 줄, Redis 구조 · 부제, Redis 값 두 줄)
rows = [
    ("글별 클릭·댓글 수", "", ("post:7:clicks=120", "post:7:comments=9"), ("hash", "필드마다 값"), ("post:7", "{clicks: 120, comments: 9}")),
    ("댓글 단 사용자 정렬", "중복 제거", ("post:7:users", '"kim:3,lee:1"'), ("zset", "점수로 정렬된 집합"), ("post:7:users", "{lee: 1, kim: 3}")),
    ("로그인 여부", "", ("login:20261012", "바이트 덩어리"), ("bitmap", "문자열 위의 비트"), ("login:20261012", "비트 42 = 1")),
]
for i, (name, hint, mc, (st, st_sub), rv) in enumerate(rows):
    y = ROW0 + i * STRIDE
    d.box(LEFT, y, COMP_W, ROW_H, PAPER2, RULE, 0.8, 4)
    if hint:
        d.t(LEFT + 12, y + 20, name, 12, INK, KR, "start", 600)
        d.t(LEFT + 12, y + 38, hint, 12, MUTED, KR, "start")
    else:
        d.t(LEFT + 12, y + 29, name, 12, INK, KR, "start", 600)
    d.box(rx(0), y, ROLE_W, ROW_H, PAPER2, RULE, 0.9, 4)
    for k, line in enumerate(mc):
        fam = KR if any("가" <= ch <= "힣" for ch in line) else MONO
        d.t(rx(0) + ROLE_W / 2, y + 20 + k * 18, line, 12, MUTED, fam)
    d.tone(rx(1), y, ROLE_W, ROW_H, INFO, 4, "10", 0.9)
    d.t(rx(1) + ROLE_W / 2, y + 20, st, 13, INFO, MONO, "middle", 600)
    d.t(rx(1) + ROLE_W / 2, y + 38, st_sub, 12, MUTED, KR)
    d.tone(rx(2), y, ROLE_W, ROW_H, INFO, 4, "10", 0.9)
    for k, line in enumerate(rv):
        fam = KR if any("가" <= ch <= "힣" for ch in line) else MONO
        d.t(rx(2) + ROLE_W / 2, y + 20 + k * 18, line, 12, INK if k else INFO, fam)

d.legend(H - 44, [("서버가 모르는 값", MUTED), ("서버가 아는 구조", INFO), ("이 절이 짚는 열", ACC)])
d.save("02-01.structure-grid.svg")
