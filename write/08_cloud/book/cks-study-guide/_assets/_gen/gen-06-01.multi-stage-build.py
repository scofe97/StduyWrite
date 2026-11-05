# 06-01 §2 — 멀티 스테이지 빌드는 빌드 단계의 도구를 버리고 산출물 하나만 실행 단계로 복사한다.
# 본문 근거: 이 노트 ### 2 「멀티 스테이지 빌드로 빌드 도구를 이미지 밖에 두기」.
# 검증 근거: Docker 29.8.2 · linux/arm64 에서 Go 1.27.3 예제 앱을 단일 단계(golang:1.27.3-alpine3.24)와
#            멀티 스테이지(alpine:3.24 · gcr.io/distroless/static-debian13:nonroot)로 빌드해 크기를 `docker image inspect --format '{{.Size}}'` 로 쟀다.
#            단일 517,414,307 B · alpine 26,982,990 B · distroless 19,831,362 B. distroless 이미지에서 /app/go-sample-app 응답 Hello World 확인.
# 공식 근거: docs.docker.com/build/building/multi-stage/ 「selectively copy artifacts from one stage to another」.
# 타입 스펙: type-flowchart — 두 단계가 COPY --from 한 줄로 이어지고, 아래에 결과 크기를 막대로 맞댄다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 448
d = D(W, H, "CKS STUDY GUIDE · 06-01 §2",
      "멀티 스테이지 빌드가 남기는 것",
      "왼쪽 build 단계에서 테스트와 빌드를 마치고, COPY --from=build 한 줄로 실행 파일 하나만 오른쪽 실행 단계로 복사하는 도식이다. "
      "아래 막대는 단일 단계 517MB, alpine 실행 단계 27MB, distroless 실행 단계 19.8MB를 같은 비율로 보여 준다.",
      "빌드 도구는 앞 단계에 두고 실행 파일만 복사하면 최종 이미지가 517MB 에서 27MB 이하로 줄어듭니다")

BX, RX, SY, SW, SH = 24, 526, 96, 330, 150
d.tone(BX, SY, SW, SH, INFO, 6, "14", 1.2)
d.t(BX + 14, SY + 26, "build 단계", 13, INK, KR, "start", 600)
d.t(BX + 14, SY + 46, "golang:1.27.3-alpine3.24", 11, MUTED, MONO, "start")
d.t(BX + 14, SY + 78, "go test -v", 12, INK, MONO, "start")
d.t(BX + 14, SY + 100, "go build -o /out/go-sample-app", 12, INK, MONO, "start")
d.chip(BX + 14 + 78, SY + 128, "최종 이미지에서 빠짐", BAD, 11)

d.tone(RX, SY, SW, SH, ACC, 6, "14", 1.4)
d.t(RX + 14, SY + 26, "실행 단계", 13, INK, KR, "start", 600)
d.t(RX + 14, SY + 46, "gcr.io/distroless/static-debian13:nonroot", 11, MUTED, MONO, "start")
d.t(RX + 14, SY + 78, "/app/go-sample-app", 12, INK, MONO, "start")
d.t(RX + 14, SY + 100, "실행 파일 한 개", 12, MUTED, KR, "start")
d.chip(RX + 14 + 62, SY + 128, "최종 이미지에 남음", OK, 11)

d.path(f"M {BX + SW + 2} {SY + 75} L {RX - 2} {SY + 75}", ACC, 1.6, m="acc")
d.chip((BX + SW + RX) / 2, SY + 56, "COPY --from=build", ACC, 11)

d.t(24, 284, "최종 이미지 크기 (docker image inspect, linux/arm64)", 12, MUTED, KR, "start", 600)
bars = [("단일 단계 · golang:1.27.3-alpine3.24", 517.4, "517MB", WARN),
        ("멀티 스테이지 · alpine:3.24", 27.0, "27MB", INFO),
        ("멀티 스테이지 · distroless static", 19.8, "19.8MB", ACC)]
BX0, SCALE = 292, 0.95
for i, (lab, mb, txt, c) in enumerate(bars):
    y = 312 + i * 34
    d.t(24, y + 4, lab, 11, INK, KR, "start")
    w = max(mb * SCALE, 6)
    d.o.append(f'<rect x="{BX0}" y="{y - 10}" width="{w:.1f}" height="20" rx="3" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
    d.t(BX0 + w + 8, y + 4, txt, 12, INK, MONO, "start", 600)

d.legend(402, [("빌드 도구", INFO), ("실행에 필요한 것", ACC), ("단일 단계 결과", WARN)])
d.save("06-01.multi-stage-build.svg")
