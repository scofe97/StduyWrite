# 01-01 §2 FHS 3.0 두 분류 축 — Consultant special (2×2 scenario matrix).
# 타입 스펙: type-quadrant — 공유 가능 여부(가로)와 변경 여부(세로) 두 독립 축의 2×2 시나리오 격자.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 920, 624
d = D(W, H, "FHS 3.0 · CHAPTER 2 · TWO AXES",
      "공유 가능 여부 × 변경 여부 2×2 배치",
      "FHS 3.0 2장이 정의한 공유 가능 여부와 변경 여부 두 축 위의 대표 디렉터리 4개 사분면. 정적·공유 영역(/usr·/opt)이 읽기 전용 마운트 대상이다.",
      "가변 데이터를 /var 로 분리해 /usr 읽기 전용 마운트와 백업 주기 분리를 얻습니다")

CX, CY = 460, 332
d.arrow([(CX, CY), (CX, 128)], MUTED, "ar", 1.2)
d.arrow([(CX, CY), (CX, 536)], MUTED, "ar", 1.2)
d.arrow([(CX, CY), (124, CY)], MUTED, "ar", 1.2)
d.arrow([(CX, CY), (796, CY)], MUTED, "ar", 1.2)

d.t(CX, 114, "STATIC", 11, INK, MONO, "middle", 500)
d.t(CX, 556, "VARIABLE", 11, INK, MONO, "middle", 500)
d.t(112, CY + 4, "SHAREABLE", 11, INK, MONO, "end", 500)
d.t(808, CY + 4, "UNSHAREABLE", 11, INK, MONO, "start", 500)

CW, CH = 296, 160
cells = [
    (140, 148, "01 · STATIC / SHAREABLE", "/usr · /opt",
     "읽기 전용 마운트 · 호스트 공유", "배포판 바이너리 · 라이브러리 · 추가 패키지", "focal"),
    (484, 148, "02 · STATIC / UNSHAREABLE", "/etc · /boot",
     "호스트 고유 설정 · 부팅 파일", "/etc 실행 바이너리 금지 (스크립트만)", "static"),
    (140, 356, "03 · VARIABLE / SHAREABLE", "/var/mail · /var/spool/news",
     "호스트 간 공유 가능한 가변 영역", "/var/cache/man 등 공용 스풀 · 캐시", "var"),
    (484, 356, "04 · VARIABLE / UNSHAREABLE", "/var/run · /var/lock · /var/log",
     "호스트 고유 실행 상태 · 로그", "잦은 쓰기 · 로그·상태 별도 백업", "var"),
]

for x, y, tag, paths, l1, l2, kind in cells:
    if kind == "focal":
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        tag_c, path_c = ACC, ACC
    elif kind == "var":
        d.tone(x, y, CW, CH, INFO, r=8, op="12", sw=1.1)
        tag_c, path_c = INFO, INK
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
        tag_c, path_c = SOFT, INK
    d.t(x + 20, y + 28, tag, 11, tag_c, MONO, "start", 600)
    d.t(x + 20, y + 64, paths, 14, path_c, MONO, "start", 600)
    d.t(x + 20, y + 102, l1, 13, INK, KR, "start", 500)
    d.t(x + 20, y + 132, l2, 12, MUTED, KR, "start")

d.legend(576, [("읽기 전용 마운트 대상 (정적·공유)", ACC), ("/var 가변 데이터 영역", INFO)])
d.save("01-01.fhs-two-axes.svg")
