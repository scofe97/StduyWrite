# 타입 스펙: type-process — Prometheus 로컬 TSDB 의 2시간 블록이 컴팩션 블록을 거쳐 보존 기간에 지워지는 줄과, Thanos 컴팩터가 40시간 넘은 원본을 5m 로, 10일 넘은 5m 를 1h 로 내리는 줄을 같은 세 칸 격자에 놓은 두 줄 단계 지도. 두 번째 줄 아래에 해상도 셋을 모두 두면 저장이 약 3배가 된다는 값이 초점이다.
# 사실 출처: Prometheus v3.15.0 docs/storage.md L14(2시간 블록)·L22-L24(현재 블록은 메모리에 있고 WAL 로 장애에 대비)·L82-L85(컴팩션 블록은 보존의 10% 또는 31일 중 작은 쪽)·L94-L96(보존 기본 15d),
#   Thanos v0.42.4 docs/components/compact.md L6-L7·L166-L167(raw 40시간 → 5m, 5m 10일 → 1h)·L171(다운샘플링은 공간을 줄이지 않고 해상도를 모두 두면 약 3배까지 늘 수 있다).
# Layout conventions: 라벨 열 x=24 폭 200, 칸 폭 216·stride 244(x=244+244k), 행 y=116·232 높이 96, 화살표는 칸 사이 폭 24, 초점 상자 y=360 폭 704. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


W, H = 1000, 484
d = D(W, H, "BYTEBYTEGO · 08-03 §4",
      "Prometheus 는 블록을 합쳐 지우고 Thanos 는 해상도를 내린다",
      "2시간 블록·15d 보존과 40시간·10일 다운샘플링을 같은 세 칸 격자에 놓았습니다.",
      "Prometheus v3.15.0 · Thanos v0.42.4 문서 기준입니다")

LX, CX0, CS, CW, CH = 24, 244, 244, 216, 96
rows = [
    ("Prometheus 로컬", "로컬 저장소", 116, [
        ("현재 블록", "메모리 + WAL", "2시간 블록으로 묶임", INFO),
        ("컴팩션 블록", "보존 10% · 31일", "둘 중 작은 쪽", INFO),
        ("보존 만료", "기본 15d", "기간 지난 블록 삭제", WARN)]),
    ("Thanos 컴팩터", "오브젝트 스토리지", 232, [
        ("원본 해상도", "raw", "수집 그대로", INFO),
        ("5m 해상도", "40시간 넘은 블록", "5분 단위 집계", OK),
        ("1h 해상도", "10일 넘은 5m", "1시간 단위 집계", OK)]),
]
for name, sub, y, cells in rows:
    d.t(LX, y + 44, name, 13, INK, KR, "start", 600)
    d.t(LX, y + 68, sub, 13, MUTED, KR, "start")
    for k, (a, v, s, c) in enumerate(cells):
        x = CX0 + k * CS
        d.tone(x, y, CW, CH, c, 6, "14", 1.0)
        d.t(x + CW / 2, y + 30, a, 13, INK, _kr(a), "middle", 600)
        d.t(x + CW / 2, y + 56, v, 13, c, _kr(v), "middle", 600)
        d.t(x + CW / 2, y + 80, s, 13, MUTED, _kr(s), "middle")
        if k < 2:
            d.arrow([(x + CW + 2, y + CH / 2), (x + CS - 4, y + CH / 2)], MUTED, "ar", 1.4)

d.tone(CX0, 360, 704, 48, ACC, 6, "14", 1.4)
d.t(CX0 + 352, 390, "해상도 셋 보관 · 저장 최대 약 3배", 13, ACC, KR, "middle", 600)

d.legend(H - 44, [("원본·블록", INFO), ("다운샘플", OK), ("삭제", WARN), ("이 절의 초점", ACC)])
d.save("08-03.downsample-process.svg")
