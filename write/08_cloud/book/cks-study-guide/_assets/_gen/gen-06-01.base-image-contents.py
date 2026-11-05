# 06-01 §1 — 같은 Node 26 이 올라가도 베이스 이미지에 따라 들어 있는 도구와 크기가 다르다.
# 본문 근거: 이 노트 ### 1 「베이스 이미지는 작을수록 들어 있는 것이 줄어든다」.
# 검증 근거: Docker 29.8.2 · linux/arm64 에서 node:latest · node:26-alpine · gcr.io/distroless/nodejs26-debian13:nonroot 를 받아
#            `command -v` 로 sh · bash · apt-get · apk · gcc · git · curl 유무를 확인했고, distroless 에서는 /bin/sh 실행이
#            `stat /bin/sh: no such file or directory` 로 실패하는 것을 확인했다. 크기는 `docker image inspect --format '{{.Size}}'` 값이다.
# 공식 근거: github.com/GoogleContainerTools/distroless 「Distroless images contain only your application and its runtime dependencies」.
# 타입 스펙: type-dp-security-matrix — 세 후보 이미지를 열로, 담긴 프로그램을 행으로 맞대는 있음·없음 격자.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 380
d = D(W, H, "CKS STUDY GUIDE · 06-01 §1",
      "같은 Node 26 이 올라가는 세 베이스 이미지",
      "node:latest, node:26-alpine, distroless nodejs26 세 이미지를 셸, 패키지 관리자, 컴파일러와 git과 curl, 크기의 네 행으로 비교한 도식이다. "
      "왼쪽에서 오른쪽으로 갈수록 들어 있는 도구가 줄어들고, 크기는 alpine 과 distroless 가 거의 같다.",
      "베이스가 작아질수록 셸과 패키지 관리자가 사라지지만 alpine 과 distroless 의 크기는 거의 같습니다")

CW, GAP, X0, Y0, CH = 264, 20, 24, 96, 232
cards = [
    ("node:latest", "Debian 13 · Node 26.13.0", WARN,
     [("셸", "sh · bash", WARN), ("패키지 관리자", "apt-get", WARN), ("gcc · git · curl", "있음", WARN)], "1.78GB"),
    ("node:26-alpine", "Alpine · Node 26.13.0", INFO,
     [("셸", "sh", WARN), ("패키지 관리자", "apk", WARN), ("gcc · git · curl", "없음", OK)], "256MB"),
    ("distroless nodejs26", "Debian 13 · Node 26", ACC,
     [("셸", "없음", OK), ("패키지 관리자", "없음", OK), ("gcc · git · curl", "없음", OK)], "254MB"),
]
for i, (name, sub, c, rows, size) in enumerate(cards):
    x = X0 + i * (CW + GAP)
    d.tone(x, Y0, CW, CH, c, 6, "14", 1.4 if c == ACC else 1.1)
    d.t(x + 14, Y0 + 28, name, 14, INK, MONO, "start", 600)
    d.t(x + 14, Y0 + 50, sub, 11, MUTED, KR, "start")
    d.line(x + 14, Y0 + 62, x + CW - 14, Y0 + 62, RULE, 0.8)
    for j, (k, v, vc) in enumerate(rows):
        ry = Y0 + 92 + j * 36
        d.t(x + 14, ry, k, 11, MUTED, KR, "start")
        d.chip(x + CW - 14 - (len(v) * (11.0 if any('가' <= ch <= '힣' for ch in v) else 6.8) + 14) / 2, ry - 4, v, vc, 11)
    d.line(x + 14, Y0 + 198, x + CW - 14, Y0 + 198, RULE, 0.8)
    d.t(x + 14, Y0 + 220, "베이스 크기", 11, MUTED, KR, "start")
    d.t(x + CW - 14, Y0 + 220, size, 13, INK, MONO, "end", 600)

d.legend(342 - 4, [("도구가 많음", WARN), ("셸·패키지 관리자와 busybox 도구", INFO), ("도구가 없음", ACC)])
d.save("06-01.base-image-contents.svg")
