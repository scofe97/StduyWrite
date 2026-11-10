# 05-01 §8 — 유니온 마운트(OverlayFS)의 조회 · 쓰기(copy-up) · 삭제(whiteout) 흐름.
# 타입 스펙: type-process — 상위(upper)와 하위(lower) 층 사이의 3대 연산(조회 · 수정 복사 · 화이트아웃 삭제) 처리 흐름.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 640
d = D(W, H, "LEARNING MODERN LINUX · 05-01 §8",
      "유니온 마운트(OverlayFS)의 조회 · 수정 · 삭제 3대 흐름",
      "여러 디렉터리를 겹칠 때 상위(upper)와 하위(lower) 층 사이에서 일어나는 "
      "조회 우선순위, 쓰기 시 copy-up, 삭제 시 화이트아웃(c 0 0) 처리 흐름.",
      "하위 층은 불변으로 두고 상위 층에 변경분과 삭제 표식을 기록")

# 상단 3개 연산 흐름 카드
CW = 264
CH = 320
GAP = 14
X0 = 24
Y0 = 120

ops = [
    ("1. 파일 조회 (Read)", "Upper → Lower 하향 순회", INFO, [
        ("조회 시작", "merged 뷰에서 파일 요청", KR, INK),
        ("1차 탐색", "상위 upperdir 먼저 확인", KR, INFO),
        ("상위 발견 시", "upperdir 파일 즉시 반환", KR, OK),
        ("상위 부재 시", "lowerdir 로 내려가 조회", KR, MUTED),
        ("결론", "상위 층이 하위 층 가림", KR, ACC),
    ]),
    ("2. 파일 수정 (Write)", "쓰기 시점의 Copy-up", ACC, [
        ("수정 요청", "lowerdir 파일에 쓰기 시도", KR, INK),
        ("제약 조건", "하위 층은 읽기 전용(R/O)", KR, WARN),
        ("복사 동작", "lowerdir → upperdir 복사", MONO, ACC),
        ("수정 적용", "upperdir 복사본에 데이터 기록", KR, OK),
        ("결론", "원본 훼손 없는 독립 수정", KR, ACC),
    ]),
    ("3. 파일 삭제 (Delete)", "화이트아웃(Whiteout) 표식", WARN, [
        ("삭제 요청", "lowerdir 파일 삭제 시도", KR, INK),
        ("제약 조건", "하위 파일 직접 삭제 불가", KR, WARN),
        ("표식 생성", "upperdir 에 c 0 0 문자 노드", MONO, ACC),
        ("은폐 효과", "merged 뷰에서 파일 감춤", KR, OK),
        ("결론", "하위 보존 · 뷰에서만 삭제", KR, WARN),
    ]),
]

for i, (title, sub, col, items) in enumerate(ops):
    x = X0 + i * (CW + GAP)
    focal = (i == 1)
    if focal:
        d.o.append(f'<rect x="{x}" y="{Y0}" width="{CW}" height="{CH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.5"/>')
    else:
        d.box(x, Y0, CW, CH, PAPER2, col, 1.1, 8)

    d.t(x + CW / 2, Y0 + 26, title, 14, col, KR, "middle", 600)
    d.t(x + CW / 2, Y0 + 46, sub, 11, SOFT, KR, "middle")
    d.line(x + 12, Y0 + 58, x + CW - 12, Y0 + 58, RULE, 0.8)

    for j, (k, v, fam, c) in enumerate(items):
        iy = Y0 + 72 + j * 48
        d.box(x + 10, iy, CW - 20, 40, PAPER, RULE, 0.6, 5)
        d.t(x + 18, iy + 16, k, 11, SOFT, KR, "start")
        d.t(x + 18, iy + 30, v, 11, c, fam, "start", 600 if c in (ACC, WARN) else 400)

# 하단 OverlayFS 계층 배치 뷰
BY = 458
BW = W - 48
BH = 114
d.box(X0, BY, BW, BH, PAPER2, RULE, 1.0, 8)
d.t(X0 + 20, BY + 24, "OverlayFS 계층 구조와 컨테이너 매핑", 13.5, INK, KR, "start", 600)

layers = [
    ("merged 뷰", "통합 마운트 지점", "컨테이너 프로세스가 바라보는 단일 파일시스템 트리", INK),
    ("upperdir (R/W)", "상위 컨테이너 쓰기 층", "신규 생성 파일 · 수정된 파일(copy-up) · 화이트아웃(c 0 0)", ACC),
    ("lowerdir (R/O)", "하위 베이스 이미지 층", "컨테이너들이 공유하는 읽기 전용 기본 루트 파일시스템", OK),
]

for k, (hdr, sub1, sub2, c) in enumerate(layers):
    ly = BY + 36 + k * 24
    d.chip(X0 + 80, ly + 8, hdr, c, 11)
    d.t(X0 + 170, ly + 12, sub1, 11, c, KR, "start", 600)
    d.t(X0 + 350, ly + 12, sub2, 11, MUTED, KR, "start")

d.legend(588, [("조회 (Upper 우선)", INFO), ("수정 (Copy-up)", ACC),
               ("삭제 (Whiteout)", WARN), ("불변 베이스 층", OK)])
d.save("05-01.union-mount.svg")
print("ok 05-01.union-mount")
