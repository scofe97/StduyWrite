# 05-01 §2 — 파드 생성 요청은 네임스페이스 레이블의 모드에 따라 거절, 감사 기록, 경고 셋 중 하나로 처리된다.
# 본문 근거: 이 노트 ### 2 「Pod Security Admission 으로 네임스페이스에 기준 걸기」.
# 검증 근거: kind v1.35.0 에서 enforce=restricted 네임스페이스는 위반 파드를 Forbidden 으로 거절했고, warn=baseline 네임스페이스는
#            hostNetwork 파드를 만들면서 Warning 을 냈다. audit 은 이 클러스터에 감사 로그를 켜지 않아 관측하지 않았고
#            공식 문서의 서술을 근거로 그렸다.
# 공식 근거: kubernetes.io 「Pod Security Admission」 — 모드 표.
# 타입 스펙: type-flowchart — 한 입력이 모드에 따라 세 갈래로 갈라진다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 392
d = D(W, H, "CKS STUDY GUIDE · 05-01 §2",
      "위반 파드가 모드별로 처리되는 길",
      "파드 생성 요청이 PodSecurity 어드미션에서 네임스페이스 레이블을 만나 enforce, audit, warn 중 걸린 모드마다 갈라지는 도식이다. "
      "enforce 는 파드를 거절하고 audit 은 감사 로그에 기록하며 warn 은 사용자에게 경고한다.",
      "네임스페이스에 건 모드마다 따로 검사해 거절·감사 기록·경고를 함께 낼 수 있습니다")

BW, BH = 316, 64
BX = 540
Y = [96, 176, 256]


def step(x, y, w, title, sub, c, op="14", sw=1.2):
    d.tone(x, y, w, 72, c, 6, op, sw)
    d.t(x + w / 2, y + 30, title, 13, INK, KR, "middle", 600)
    d.t(x + w / 2, y + 54, sub, 11, MUTED, MONO)


step(24, 172, 172, "Pod 생성 요청", "kubectl apply", INFO)
step(250, 172, 212, "PodSecurity 어드미션", "네임스페이스 레이블", ACC, "14", 1.4)
d.path("M 198 208 L 248 208", MUTED, 1.4, m="ar")

branches = [
    ("enforce 모드", "파드 거절 · 403 Forbidden", BAD),
    ("audit 모드", "허용 · 감사 로그에 annotation", INFO),
    ("warn 모드", "허용 · 사용자 콘솔에 경고", WARN),
]
d.path("M 464 208 L 502 208", MUTED, 1.5)
for y, (title, sub, c) in zip(Y, branches):
    d.tone(BX, y, BW, BH, c, 6, "14", 1.2)
    d.t(BX + 14, y + 26, title, 13, INK, KR, "start", 600)
    d.t(BX + 14, y + 48, sub, 11, MUTED, KR, "start")
    yc = y + BH / 2
    mk = {BAD: "bad", INFO: "info", WARN: "warn"}[c]
    if abs(yc - 208) < 1:
        d.path(f"M 502 208 L {BX - 2} 208", c, 1.5, m=mk)
    else:
        d.path(f"M 502 208 L 502 {yc} L {BX - 2} {yc}", c, 1.5, m=mk)

d.legend(344, [("검사 지점", ACC), ("거절", BAD), ("허용 + 기록", INFO), ("허용 + 경고", WARN)])
d.save("05-01.psa-modes.svg")
