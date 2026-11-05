# 06-02 §3 — Trivy 는 이미지에서 패키지 목록을 뽑아 취약점 DB 와 대조하고 심각도별 결과를 낸다.
# 본문 근거: 이 노트 ### 3 「알려진 취약점 스캔하기」.
# 검증 근거: aquasec/trivy:0.76.1 로 alpine·nodejs-hello-world·logstash 이미지를 스캔해
#            Report Summary 표와 Library·Vulnerability·Severity·Status·Installed Version·Fixed Version 열을 확인.
# 공식 근거: trivy.dev/docs/v0.76/guide/target/container_image, guide/scanner/vulnerability.
# 타입 스펙: type-swimlane — 스캔 흐름과 결과 읽기.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 432
d = D(W, H, "CKS STUDY GUIDE · 06-02 §3",
      "Trivy 가 이미지에서 취약점을 찾는 길",
      "위 레인은 trivy image 명령이 이미지에서 패키지 목록을 뽑아 취약점 DB 와 대조하고 결과 표를 내는 스캔 흐름이고, "
      "아래 레인은 결과 표에서 심각도와 고친 버전을 읽고 이미지를 교체하거나 파드를 지우는 결과 읽기 흐름이다.",
      "패키지 목록을 취약점 DB 와 맞춰 보고, 결과 표의 심각도와 고친 버전으로 다음 행동을 정합니다")

BW, BH, PITCH, X0 = 190, 76, 212, 24
LANE_X, LANE_W, LANE_H = 12, 856, 132
A_Y, S_Y = 96, 244


def lane(y, name):
    d.o.append(f'<rect x="{LANE_X}" y="{y}" width="{LANE_W}" height="{LANE_H}" rx="8" fill="{SOFT}0A" stroke="{SOFT}" stroke-width="0.9"/>')
    d.t(LANE_X + 12, y + 20, name, 12, MUTED, KR, "start", 600)


def lane_steps(y, items):
    by = y + 40
    for i, (title, sub, c) in enumerate(items):
        x = X0 + i * PITCH
        d.tone(x, by, BW, BH, c, 6, "14", 1.4 if c == ACC else 1.1)
        d.t(x + BW / 2, by + 32, title, 13, INK, KR, "middle", 600)
        d.t(x + BW / 2, by + 56, sub, 11, MUTED, MONO)
        if i < len(items) - 1:
            d.path(f"M {x + BW + 2} {by + BH / 2} L {x + PITCH - 2} {by + BH / 2}", MUTED, 1.4, m="ar")


lane(A_Y, "스캔")
lane_steps(A_Y, [
    ("trivy image", "alpine:3.13.4", INFO),
    ("패키지 목록", "OS · 언어 패키지", INFO),
    ("취약점 DB 대조", "패키지 이름과 버전", ACC),
    ("결과 표", "Library · Severity", SOFT),
])
lane(S_Y, "결과 읽기")
lane_steps(S_Y, [
    ("Severity", "--severity CRITICAL", ACC),
    ("Fixed Version", "고친 버전이 있는가", INFO),
    ("있으면", "새 버전 이미지로 교체", OK),
    ("바꿀 수 없으면", "파드 삭제", WARN),
])

d.legend(392, [("입력과 준비", INFO), ("판정하는 자리", ACC), ("결과", SOFT), ("조치", OK), ("대안", WARN)])
d.save("06-02.trivy-scan-flow.svg")
