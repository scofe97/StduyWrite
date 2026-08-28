# 02-01 §레이어 공유와 해시 — 같은 해시는 한 벌만
# 본문 실측: nginx:alpine → sha256:91d5cf66… / redis:alpine → sha256:91d5cf66… (같다)
#           httpd:alpine → sha256:b2848c02… (다르다 → 별도 저장)
#       "내용이 1바이트만 달라도 해시가 완전히 달라지므로, '공유' 는 우연이 아니라 바이트 단위로
#        동일할 때만 성립합니다 — 그래서 팀이 베이스 이미지를 통일해야 이 절약을 얻습니다."
# 타입 스펙: type-dp-security-matrix.md — 세 이미지 × 해시 × 저장 결과라 비교 행렬. 판정 축은 해시다 — 그 열만 같으면
#           나머지가 따라온다. manifest 장이 구조를 지고, 이 장은 그 판정만 진다.
#           행은 이미지 셋, 열은 해시·저장·공유 여부인 격자다. focal 열이 해시라 그 열만 같으면
#           나머지가 따라온다는 것이 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

# 좌표는 행렬 아래끝에서 산출한다 — 상수 y 를 두면 행 수가 바뀔 때 산문이 마지막 행을 뚫는다.
MTOP, ROW_H, GAP, NROWS = 196, 88, 12, 3
MBOT = MTOP + 24 + NROWS * (ROW_H + GAP) - GAP   # 508
NOTE_Y, BAND_Y1, LEG_Y = MBOT + 28, MBOT + 52, MBOT + 68
W, H = 1000, LEG_Y + 40
d = D(W, H, "KUBERNETES IN ACTION · 02-01",
      "해시가 같아야 공유된다 — 우연이 아니다",
      "Docker 는 레이어 내용을 SHA256 으로 해싱해 같은 해시를 같은 내용으로 본다. nginx 와 "
      "redis 는 같은 alpine 스냅샷을 써서 해시가 같고, httpd 는 달라서 따로 저장된다.",
      lead="1바이트만 달라도 해시가 완전히 달라진다 — 그래서 베이스 이미지를 통일해야 절약이 생긴다")

ddx.band(d, 104, BAND_Y1, "해시 열 하나가 저장 결과를 결정한다")

ddx.matrix(
    d, x0=36, hdr_y=MTOP, row_h=ROW_H, gap=GAP, focal_col=1,
    cols=[(200, "이미지"), (280, "맨 아래 레이어 해시"),
          (200, "디스크 저장"), (210, "공유되나")],
    rows=[
        ([("nginx:alpine", "alpine 베이스"), ("sha256:91d5cf66…", "같다"),
          ("한 벌만", "redis 와 나눠 쓴다"), ("공유된다", "포인터로 가리킨다")], OK),
        ([("redis:alpine", "alpine 베이스"), ("sha256:91d5cf66…", "같다"),
          ("한 벌만", "nginx 와 나눠 쓴다"), ("공유된다", "포인터로 가리킨다")], OK),
        ([("httpd:alpine", "다른 alpine 스냅샷"), ("sha256:b2848c02…", "다르다"),
          ("따로 저장", "별도 레이어"), ("공유되지 않는다", "내용이 다르기 때문")], BAD),
    ])

d.t(36, NOTE_Y, "해시가 같다는 것은 레이어 내용이 바이트 단위로 같다는 뜻이다 — 그때만 Docker 가 "
             "하나만 저장하고 여럿이 가리킨다.", 12, MUTED, KR, "start")
d.legend(LEG_Y, [("같은 해시 — 공유된다", OK), ("다른 해시 — 따로 저장된다", BAD)])
d.save("02-01-layer-sharing-hash.svg")
print("ok layer-sharing-hash")
