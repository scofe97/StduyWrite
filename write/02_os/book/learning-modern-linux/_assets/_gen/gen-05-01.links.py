# 05-01 §3 — 하드 링크와 심볼릭 링크의 파일 데이터 조회 순서 비교.
# 타입 스펙: type-process — 명령 cat 실행 시 디렉터리 항목에서 아이노드 및 데이터 블록으로 이어지는 단계별 경로 조회 흐름.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 620
d = D(W, H, "LEARNING MODERN LINUX · 05-01 §3",
      "하드 링크와 심볼릭 링크의 데이터 조회 순서",
      "cat 실행 시 하드 링크는 아이노드를 직접 참조해 1회에 도달하고, "
      "심볼릭 링크는 경로 문자열을 읽어 2회 조회를 거쳐 도달합니다.",
      "원본 삭제 시 하드 링크는 데이터 보존, 심볼릭 링크는 깨진 링크")

TW = 404
X1 = 24
X2 = 452
Y0 = 120

d.box(X1, Y0, TW, 330, PAPER2, OK, 1.2, 8)
d.t(X1 + 18, Y0 + 26, "하드 링크 조회 — cat somealias", 14, OK, KR, "start", 600)
d.t(X1 + 18, Y0 + 46, "아이노드 직접 참조 (1회 도달)", 11.5, MUTED, KR, "start")
d.line(X1 + 14, Y0 + 58, X1 + TW - 14, Y0 + 58, RULE, 0.8)

h_steps = [
    ("1. 디렉터리 항목 조회", "dentry 'somealias' 매핑 검색", INK),
    ("2. 아이노드 번호 직접 연결", "Inode 6302071 (Links: 2 · 크기 0B)", OK),
    ("3. 데이터 블록 읽기", "Inode 블록 포인터로 실제 데이터 도달", INK),
]
for k, (stitle, sdesc, sc) in enumerate(h_steps):
    sy = Y0 + 72 + k * 80
    d.box(X1 + 14, sy, TW - 28, 62, PAPER, sc, 1.0, 6)
    d.t(X1 + 26, sy + 22, stitle, 12, sc, KR, "start", 600)
    d.t(X1 + 26, sy + 44, sdesc, 11, MUTED, MONO if k == 1 else KR, "start")
    if k < 2:
        d.arrow([(X1 + TW / 2, sy + 62), (X1 + TW / 2, sy + 78)], MUTED, "ar", 1.2)

d.box(X2, Y0, TW, 330, PAPER2, ACC, 1.2, 8)
d.t(X2 + 18, Y0 + 26, "심볼릭 링크 조회 — cat somesoftalias", 14, ACC, KR, "start", 600)
d.t(X2 + 18, Y0 + 46, "경로 문자열 경유 (2회 도달)", 11.5, MUTED, KR, "start")
d.line(X2 + 14, Y0 + 58, X2 + TW - 14, Y0 + 58, RULE, 0.8)

s_steps = [
    ("1. 링크 파일 아이노드 조회", "Inode 6303540 (Links: 1 · Size: 6)", INK),
    ("2. 내용에서 대상 경로 추출", "문자열 'myfile' (6바이트) 읽기", ACC),
    ("3. 대상 경로 2차 탐색 및 도달", "Inode 6302071 검색 후 데이터 블록 읽기", OK),
]
for k, (stitle, sdesc, sc) in enumerate(s_steps):
    sy = Y0 + 72 + k * 80
    d.box(X2 + 14, sy, TW - 28, 62, PAPER, sc, 1.0, 6)
    d.t(X2 + 26, sy + 22, stitle, 12, sc, KR, "start", 600)
    d.t(X2 + 26, sy + 44, sdesc, 11, MUTED, MONO if k != 1 else KR, "start")
    if k < 2:
        d.arrow([(X2 + TW / 2, sy + 62), (X2 + TW / 2, sy + 78)], MUTED, "ar", 1.2)

BY = 466
BW = W - 48
d.box(X1, BY, BW, 86, PAPER2, RULE, 1.0, 8)
d.t(X1 + 20, BY + 24, "원본 파일 삭제(rm myfile) 시 동작 차이", 13.5, INK, KR, "start", 600)

d.box(X1 + 16, BY + 36, 400, 38, PAPER, OK, 0.8, 6)
d.t(X1 + 26, BY + 52, "somealias (하드 링크)", 11.5, OK, MONO, "start", 600)
d.t(X1 + 26, BY + 66, "Inode 6302071 링크 수 2→1 감소 · 데이터 보존", 11, MUTED, KR, "start")

d.box(X2, BY + 36, 400, 38, PAPER, ACC, 0.8, 6)
d.t(X2 + 10, BY + 52, "somesoftalias (심볼릭 링크)", 11.5, ACC, MONO, "start", 600)
d.t(X2 + 10, BY + 66, "경로 'myfile' 부재 · 깨진 링크(dangling link)", 11, MUTED, KR, "start")

d.legend(566, [("직접 참조 및 데이터", OK), ("경로 문자열 및 간접 참조", ACC),
               ("메타데이터 및 조회 절차", INK)])
d.save("05-01.links.svg")
print("ok 05-01.links")
