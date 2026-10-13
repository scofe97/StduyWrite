# 타입 스펙: type-dp-security-matrix — 격자 문법을 비교 행렬로 쓴다. 본초 자오선 양쪽의 두 점을 같은 행 구조(경도 비트 · 위도 비트 · 섞은 비트 · 접두사 질의 결과)로 나란히 놓아 첫 비트부터 갈리는 모양을 보인다. 초점은 B 의 첫 섞은 비트(A 의 접두사 질의를 놓치게 만드는 비트).
# 사실 출처: 추출본 v1.txt 3583~3597행(경도 비트와 위도 비트를 번갈아 코드 구성, `LIKE '01%'` 접두사 질의, 경도 [-180,0]=0·[0,180]=1, 위도 [-90,0]=0·[0,90]=1)을 이분 규칙으로 구현한 enc() 로 두 점의 비트를 계산,
#   Wikipedia Geohash(base32 알파벳 e=13·s=24, 본초 자오선·적도 양쪽의 가까운 두 점은 긴 접두사를 공유하지 못함, 글자 하나가 비트 다섯 개) https://en.wikipedia.org/wiki/Geohash.
#   두 점 좌표(경도 ±0.0001·위도 42.0)는 이 노트가 정한 예시이고 비트는 enc() 가 낸 값이다.
# Layout conventions: 비트 칸 36×36 stride 40, 점마다 행 셋(경도·위도·섞은) stride 40, 점 블록 사이 간격 36, 결과 타일 폭 144 간격 8. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO


def enc(lat, lon, n):
    la, lo, bits = [-90.0, 90.0], [-180.0, 180.0], ""
    for i in range(n):
        rng, v = (lo, lon) if i % 2 == 0 else (la, lat)
        m = (rng[0] + rng[1]) / 2
        if v >= m:
            bits += "1"; rng[0] = m
        else:
            bits += "0"; rng[1] = m
    return bits


W, H = 960, 496
d = D(W, H, "BYTEBYTEGO · 09-01 §3",
      "자오선 양쪽의 가까운 두 점은 첫 비트부터 갈린다",
      "경도 비트와 위도 비트를 번갈아 섞으면 A 는 0110…, B 는 1100… 이 되어 A 의 접두사 질의가 B 를 놓칩니다.",
      "비트는 이분 규칙으로 계산했고 글자는 base32 알파벳(e=13·s=24)으로 읽은 값입니다")

ALPHA = "0123456789bcdefghjkmnpqrstuvwxyz"
PTS = [("A", -0.0001, 42.0), ("B", 0.0001, 42.0)]
CX0, STR, CS = 116, 40, 36
ROWS = ["경도 비트", "위도 비트", "섞은 비트"]
prefix_q = None
y = 100
for idx, (name, lon, lat) in enumerate(PTS):
    bits = enc(lat, lon, 8)
    lonb, latb = bits[0::2], bits[1::2]
    if idx == 0:
        prefix_q = bits[:4]
    d.t(12, y + 16, f"점 {name}", 13, INK, KR, "start", 600)
    d.t(72, y + 16, f"경도 {lon:+.4f} · 위도 {lat:.1f}", 13, MUTED, KR, "start")
    ry = y + 28
    for r, lab in enumerate(ROWS):
        d.t(12, ry + r * 40 + 24, lab, 13, MUTED, KR, "start")
    for i, b in enumerate(bits):
        x = CX0 + i * STR
        src_lon = (i % 2 == 0)
        c = INFO if src_lon else WARN
        # 경도 행(짝수 칸)·위도 행(홀수 칸)·섞은 행(전부)
        rr = 0 if src_lon else 1
        d.tone(x, ry + rr * 40, CS, CS, c, 4, "14", 1.0)
        d.t(x + CS / 2, ry + rr * 40 + 24, b, 14, INK, MONO, "middle", 600)
        if i == 0 and name == "B":
            d.tone(x, ry + 80, CS, CS, ACC, 4, "14", 1.4)
            d.t(x + CS / 2, ry + 80 + 24, b, 14, ACC, MONO, "middle", 600)
        else:
            d.tone(x, ry + 80, CS, CS, c, 4, "14", 1.0)
            d.t(x + CS / 2, ry + 80 + 24, b, 14, INK, MONO, "middle", 600)
    five = enc(lat, lon, 5)
    ch = ALPHA[int(five, 2)]
    hit = bits[:4] == prefix_q
    tx = 468
    tiles = [
        (f"앞 4비트 {bits[:4]}", INFO),
        (f"첫 글자 {ch} · {five}", INFO),
        (f"'{prefix_q}%' · " + ("찾음" if hit else "놓침"), OK if hit else BAD),
    ]
    for k, (txt, c) in enumerate(tiles):
        x = tx + k * 152
        d.tone(x, ry + 80, 144, CS, c, 6, "14", 1.0)
        d.t(x + 72, ry + 80 + 23, txt, 12, INK, KR if any("가" <= ch2 <= "힣" for ch2 in txt) else MONO, "middle", 600)
    y += 28 + 3 * 40 + 36

d.legend(H - 48, [("경도에서 온 비트", INFO), ("위도에서 온 비트", WARN), ("B 의 첫 섞은 비트", ACC), ("찾음", OK), ("놓침", BAD)])
d.save("09-01.bit-interleave.svg")
