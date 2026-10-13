# 타입 스펙: type-dp-security-matrix — 전역 유일 ID 여섯 방식 × 요구 다섯의 가능·조건부·불가 격자(격자 문법을 비교 행렬로 사용). 초점은 다섯 요구를 조율 없이 모두 만족하는 스노플레이크의 확장성 칸.
# 사실 출처: 추출본 v1.txt 635~660행과 쪽 22 그림(요구 다섯 · DB auto-increment · UUID · DB ticket server · Redis A 1,3,5,7 / B 2,4,6,8 · Snowflake). RFC 9562 (UUIDv4 랜덤, UUIDv7 의 48비트 Unix ms 타임스탬프, 128비트). Flickr 코드 블로그 2010-02-08 (Tickets64 bigint, 홀수·짝수 두 서버, auto-increment-increment 2 · offset 1·2, 서버 쪽이 약간 어긋남). Redis INCR·INCRBY 문서(64비트 부호 있는 정수, INCRBY 는 증가폭 지정). twitter-archive/snowflake snowflake-2010 README(41+10+12 비트, 약 1초 이내 k-sorted, 조율 없음).
# Layout conventions: §2 공식 — left_pad 12, comp_col_w 224, role_col_w 120, role_col_gap 12, header_h 52, header_y 96, row_h 44 · stride 48.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

LEFT, COMP_W, GAP0, ROLE_W, ROLE_GAP, HDR_Y, HDR_H, ROW0, ROW_H, STRIDE = 12, 224, 12, 120, 12, 96, 52, 164, 44, 48
roles = [("전역 유일", "겹치지 않음"), ("시각 순", "대략 시간순"), ("숫자만", "수 하나로 표현"), ("64비트", "저장 8바이트"), ("확장성", "낮은 지연")]
rows = [
    ("DB auto-increment", "서버 한 대"),
    ("UUID v4", "랜덤"),
    ("UUID v7", "시각 기반"),
    ("티켓 서버 둘", "홀수 · 짝수"),
    ("Redis INCRBY 둘", "홀수 · 짝수"),
    ("스노플레이크", "41 · 10 · 12 비트"),
]
# 1=가능, 0=불가, 2=조건부
cells = [
    [(1, ""), (1, ""), (1, ""), (1, ""), (0, "한 대만")],
    [(1, "랜덤 비트"), (0, ""), (0, "16진 표기"), (0, "128비트"), (1, "")],
    [(1, ""), (1, "48비트 ms"), (0, "16진 표기"), (0, "128비트"), (1, "")],
    [(1, ""), (2, "어긋남"), (1, ""), (1, "bigint"), (2, "DB 경유")],
    [(1, ""), (2, "어긋남"), (1, ""), (1, "64비트 정수"), (2, "증가폭 재설정")],
    [(1, ""), (1, "대략 순서"), (1, ""), (1, "63비트"), (1, "")],
]
FOCAL = (5, 4)
W = LEFT + COMP_W + GAP0 + 5 * ROLE_W + 4 * ROLE_GAP + 48
H = ROW0 + 5 * STRIDE + ROW_H + 20 + 44
d = D(W, H, "BYTEBYTEGO · 01-02 §5",
      "여섯 ID 방식이 다섯 요구를 얼마나 채우는가",
      "한 곳의 번호표는 서버를 늘리지 못하고, 서버마다 따로 만들면 시각 순이나 64비트가 깨집니다",
      "요구 다섯 · 1차 자료 기준 판정")

d.box(LEFT, HDR_Y, COMP_W, HDR_H, PAPER2, RULE, 0.9, 6)
d.t(LEFT + COMP_W / 2, HDR_Y + 22, "ID 방식", 12, INK, KR, "middle", 600)
d.t(LEFT + COMP_W / 2, HDR_Y + 40, "× 요구", 12, MUTED, KR)

def rx(j):
    return LEFT + COMP_W + GAP0 + j * (ROLE_W + ROLE_GAP)

for j, (nm, sub) in enumerate(roles):
    d.box(rx(j), HDR_Y, ROLE_W, HDR_H, PAPER2, "rgba(191,192,192,0.45)", 0.9, 6)
    d.t(rx(j) + ROLE_W / 2, HDR_Y + 22, nm, 12, INK, KR, "middle", 600)
    d.t(rx(j) + ROLE_W / 2, HDR_Y + 40, sub, 12, MUTED, KR)

STATE = {1: ("가능", OK), 0: ("불가", BAD), 2: ("조건부", WARN)}
for i, (name, hint) in enumerate(rows):
    y = ROW0 + i * STRIDE
    d.box(LEFT, y, COMP_W, ROW_H, PAPER2, RULE, 0.8, 4)
    d.t(LEFT + 12, y + 18, name, 12, INK, KR if any("가" <= c <= "힣" for c in name) else MONO, "start", 600)
    d.t(LEFT + 12, y + 35, hint, 12, MUTED, KR if any("가" <= c <= "힣" for c in hint) else MONO, "start")
    for j in range(5):
        st, sub = cells[i][j]
        lab, c = STATE[st]
        x = rx(j)
        if (i, j) == FOCAL:
            d.tone(x, y, ROLE_W, ROW_H, ACC, 4, "14", 1.4)
            d.t(x + ROLE_W / 2, y + 27, lab, 12, ACC, KR, "middle", 600)
        else:
            d.tone(x, y, ROLE_W, ROW_H, c, 4, "10", 0.9)
            if sub:
                d.t(x + ROLE_W / 2, y + 19, lab, 12, c, KR, "middle", 600)
                d.t(x + ROLE_W / 2, y + 36, sub, 12, MUTED, KR if any("가" <= ch <= "힣" for ch in sub) else MONO, "middle")
            else:
                d.t(x + ROLE_W / 2, y + 27, lab, 12, c, KR, "middle", 600)

d.legend(H - 44, [("가능", OK), ("조건부", WARN), ("불가", BAD), ("조율 없이 확장", ACC)])
d.save("01-02.id-compare.svg")
