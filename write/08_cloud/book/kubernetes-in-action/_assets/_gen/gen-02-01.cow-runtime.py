# 02-01 §CoW 실측 — web1 만 바꿔도 나머지는 원본
# 본문 실측: docker run web1/web2 (nginx:alpine) → web1 에서만 index.html 수정.
#   web1 → "web1이 바꿈" · web2 → 원본 Welcome · 새 컨테이너(--rm) → 원본 Welcome
#   "web1 은 파일을 건드렸기 때문에 복사가 일어났고, web2 는 건드리지 않아서 원본을 봅니다."
# 타입 스펙: 결과 셋이 갈리는 이유가 '건드렸는가' 하나이므로 비교 행렬. 개념도(copy-on-write)는
#           층 구조를 지고, 이 장은 결과와 그 원인만 진다 — 두 장의 역할을 갈랐다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

# 좌표는 행렬 아래끝에서 산출한다 — 상수 y 를 두면 행 수가 바뀔 때 산문이 마지막 행을 뚫는다.
MTOP, ROW_H, GAP, NROWS = 196, 88, 12, 3
MBOT = MTOP + 24 + NROWS * (ROW_H + GAP) - GAP   # 508
NOTE_Y, BAND_Y1, LEG_Y = MBOT + 28, MBOT + 52, MBOT + 68
W, H = 1000, LEG_Y + 40
d = D(W, H, "KUBERNETES IN ACTION · 02-01",
      "갈림은 '건드렸는가' 하나에서 온다",
      "같은 nginx:alpine 이미지로 띄운 셋 중 web1 만 index.html 을 바꿨다. web1 은 자기 사본을 "
      "보고 나머지 둘은 원본을 본다. 이미지 레이어는 읽기 전용이라 몇 번을 바꿔도 불변이다.",
      lead="CoW 의 트리거는 공유 여부가 아니라 수정 시도다 — 건드리는 순간 그 파일만 복사된다")

ddx.band(d, 104, BAND_Y1, "web1 이 바꾼 뒤 새로 띄워도 이미지 원본에서 시작한다 — 이미지는 불변이다")

ddx.matrix(
    d, x0=36, hdr_y=MTOP, row_h=ROW_H, gap=GAP, focal_col=1,
    cols=[(200, "컨테이너"), (210, "파일을 건드렸나"),
          (240, "쓰기 레이어"), (240, "cat 으로 본 내용")],
    rows=[
        ([("web1", "먼저 띄운 쪽"), ("건드렸다", "echo 로 덮어썼다"),
          ("사본이 생겼다", "index.html 한 파일만"), ("web1이 바꿈", "자기 사본을 본다")], ACC),
        ([("web2", "같은 이미지"), ("안 건드렸다", "읽기만 했다"),
          ("비어 있다", "복사가 일어나지 않았다"), ("원본 Welcome", "베이스를 그대로 본다")], OK),
        ([("새 컨테이너", "--rm 으로 새로"), ("안 건드렸다", "방금 떴다"),
          ("비어 있다", "이미지에서 시작한다"), ("원본 Welcome", "이미지가 안 바뀌었다")], INFO),
    ])

d.t(36, NOTE_Y, "web1 의 수정은 web1 의 쓰기 레이어에만 있다 — 공유 이미지 레이어는 손대지 않는다.",
     12, MUTED, KR, "start")
d.legend(LEG_Y, [("건드린 쪽 — 사본이 생긴다", ACC), ("안 건드린 쪽", OK), ("새로 뜬 쪽", INFO)])
d.save("02-01-cow-runtime.svg")
print("ok cow-runtime")
