# 45-02 §4 — SSL/TLS 보안 문제를 들으면 규격의 결함인지 구현의 결함인지부터 가르고, 구현 결함이면 영향받는 버전으로 조치 범위를 좁힌다.
# 본문 근거: 이 노트 §4 「규격 결함과 구현 결함」.
# 검증 근거: 2026-11-08 heartbleed.com — "OpenSSL 1.0.1 through 1.0.1f (inclusive) are vulnerable", "OpenSSL 1.0.1g is NOT vulnerable",
#            "Is this a design flaw in SSL/TLS protocol specification? No. This is implementation problem, i.e. programming mistake in popular OpenSSL library".
# 타입 스펙: type-flowchart — 판단 분기. 타원은 시작, 마름모는 판단(출구 둘, 모든 출구에 라벨), 사각형은 결과. 코랄은 가장 중요한 판단 하나에만 쓴다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INK, MUTED, SOFT, RULE, PAPER2, OK, INFO, KR, MONO

W, H = 880, 576
CX = 440
d = D(W, H, "OSTEP · 45-02 §4",
      "보안 문제 소식은 규격 결함인지 구현 결함인지부터 가른다",
      "SSL/TLS 보안 문제를 들으면 먼저 규격의 결함인지 묻는다. 규격의 결함이면 규격을 따르는 모든 구현이 같은 문제를 안는다. "
      "아니면 구현의 결함이고 다른 구현을 쓰는 쪽은 영향이 없을 수 있다. Heartbleed 는 규격 결함이 아니라 OpenSSL 구현의 프로그래밍 실수였고 1.0.1 부터 1.0.1f 까지만 영향을 받았으며 1.0.1g 는 영향이 없었다.",
      "규격 결함이면 모든 구현이, 구현 결함이면 그 구현을 쓰는 쪽만 조치한다")


def oval(cx, cy, w, h, text):
    d.o.append(f'<rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" rx="20" fill="{PAPER2}" stroke="{SOFT}" stroke-width="1.1"/>')
    d.t(cx, cy + 5, text, 13, INK, KR, "middle", 600)


def step(x, y, w, h, title, subs, c=None):
    if c:
        d.tone(x, y, w, h, c, 6, "14", 1.4)
    else:
        d.box(x, y, w, h)
    d.t(x + w / 2, y + 28, title, 14, c or INK, KR, "middle", 600)
    for i, s in enumerate(subs):
        d.t(x + w / 2, y + 50 + i * 18, s, 12, MUTED, KR)


def diamond(cx, cy, hw, hh, text, c):
    pts = f"{cx},{cy - hh} {cx + hw},{cy} {cx},{cy + hh} {cx - hw},{cy}"
    d.o.append(f'<polygon points="{pts}" fill="{c}14" stroke="{c}" stroke-width="1.4"/>')
    d.t(cx, cy + 5, text, 14, c, KR, "middle", 600)


oval(CX, 124, 224, 40, "보안 문제 소식을 들음")
d.arrow([(CX, 144), (CX, 180)], MUTED, "ar", 1.4)
diamond(CX, 232, 124, 52, "규격의 결함인가?", ACC)

# 예 → 오른쪽
d.arrow([(CX + 126, 232), (612, 232)], MUTED, "ar", 1.4)
d.t(CX + 156, 222, "예", 12, MUTED, KR, "middle", 600)
step(616, 196, 220, 72, "모든 구현이 같은 문제", ["규격을 따르는 구현 전부"])

# 아니오 → 아래
d.arrow([(CX, 286), (CX, 332)], MUTED, "ar", 1.4)
d.t(CX + 12, 314, "아니오", 12, MUTED, KR, "start", 600)
step(CX - 120, 336, 240, 72, "구현의 결함", ["다른 구현은 영향 없을 수 있음"])

# 예시
d.arrow([(CX, 410), (CX, 456)], MUTED, "ar", 1.4)
d.t(CX + 12, 438, "버전으로 좁힘", 12, MUTED, KR, "start", 600)
step(CX - 200, 460, 400, 92, "예: Heartbleed (CVE-2014-0160)",
     ["OpenSSL 1.0.1 ~ 1.0.1f 만 영향", "1.0.1g 는 영향 없음 · 규격 결함이 아님"], OK)

d.save("45-02.flaw-triage.svg")
