# 12-01 §2 — Git 변경이 Argo CD 에 닿는 길은 둘이다. 조정 주기가 끌어오는 폴링(기본 120초 + 최대 60초 jitter)과, push 가 /api/webhook 으로 보내는 새로 고침 재촉.
#            두 길 모두 새로 고침까지만 일으키고, 동기화 여부는 앱의 자동 동기화 설정이 정한다.
# 본문 근거: 이 노트 ### 2 「Webhook 으로 새로 고침 재촉하기」.
# 검증 근거: kind v0.31.0 에 Argo CD v3.6.1 을 설치해 확인했다. 폴링 주기를 3600초로 늘린 앱은 push 만으로 20초 안에 감지하지 못했고,
#            맞는 URL·브랜치로 /api/webhook 에 POST 하면 2~10초 안에 새로 고침됐다(서버 로그 "refreshing app from webhook").
#            자동 동기화를 끈 앱에 같은 POST 를 보내면 OutOfSync 가 되고 클러스터 값은 그대로였다.
# 공식 근거: argo-cd v3.6.1 docs/faq.md(폴링 기본 주기), docs/operator-manual/webhook.md(/api/webhook, 새로 고침만).
# 타입 스펙: type-architecture — 왼쪽 저장소에서 두 길이 갈라져 가운데서 합쳐지고, 오른쪽에서 자동 동기화 설정에 따라 갈라지는 한 방향 흐름.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 488
d = D(W, H, "ARGO CD UP AND RUNNING · 12-01 §2",
      "Git 변경이 Argo CD 에 닿는 두 길",
      "왼쪽의 Git 저장소에서 변경을 알리는 길이 둘로 갈라진다. 위쪽 길은 조정 주기마다 Argo CD 가 저장소를 끌어와 조회하는 폴링이고 기본 간격은 120초에 최대 60초의 jitter 를 더한 값이다. "
      "아래쪽 길은 Git 서버가 push 때 argocd-server 의 /api/webhook 으로 요청을 보내 새로 고침을 재촉하는 Webhook 이다. 두 길은 가운데 새로 고침 단계에서 합쳐져 repo-server 가 최신 리비전을 읽고 앱을 비교한다. "
      "그 뒤는 앱의 자동 동기화 설정이 갈라서, 켜져 있으면 동기화하고 꺼져 있으면 OutOfSync 로 남겨 둔다.",
      "두 길 모두 새로 고침까지만 일으킵니다")

A_X, A_W = 24, 124
B_X, B_W = 186, 190
C_X, C_W = 414, 188
D_X, D_W = 640, 216
B1_Y, B2_Y, B_H = 140, 316, 92
A_Y, A_H = 228, 100
D1_Y, D2_Y, D_H = 160, 312, 84
MID = A_Y + A_H / 2

# Git 저장소
d.tone(A_X, A_Y, A_W, A_H, INFO, 6, "14", 1.1)
d.t(A_X + A_W / 2, A_Y + 38, "Git 저장소", 12.5, INK, KR, "middle", 600)
d.t(A_X + A_W / 2, A_Y + 64, "push 로", 12, MUTED)
d.t(A_X + A_W / 2, A_Y + 84, "새 커밋 생김", 12, MUTED)

# 폴링
d.box(B_X, B1_Y, B_W, B_H, PAPER2, RULE, 1.0)
d.t(B_X + B_W / 2, B1_Y + 30, "폴링 (끌어옴)", 12.5, INK, KR, "middle", 600)
d.t(B_X + B_W / 2, B1_Y + 54, "120초 + jitter 최대 60초", 12, MUTED)
d.t(B_X + B_W / 2, B1_Y + 76, "timeout.reconciliation", 11.5, MUTED, MONO)

# Webhook
d.box(B_X, B2_Y, B_W, B_H, PAPER2, RULE, 1.0)
d.t(B_X + B_W / 2, B2_Y + 30, "Webhook (재촉)", 12.5, INK, KR, "middle", 600)
d.t(B_X + B_W / 2, B2_Y + 54, "push 때 POST", 12, MUTED)
d.t(B_X + B_W / 2, B2_Y + 76, "/api/webhook", 11.5, MUTED, MONO)

# 새로 고침과 비교
d.tone(C_X, A_Y, C_W, A_H, ACC, 6, "14", 1.4)
d.t(C_X + C_W / 2, A_Y + 34, "새로 고침", 12.5, INK, KR, "middle", 600)
d.t(C_X + C_W / 2, A_Y + 58, "repo-server 가 리비전 조회", 12, MUTED)
d.t(C_X + C_W / 2, A_Y + 80, "앱 비교", 12, MUTED)

# 자동 동기화에 따른 결과
d.tone(D_X, D1_Y, D_W, D_H, OK, 6, "14", 1.2)
d.t(D_X + D_W / 2, D1_Y + 34, "자동 동기화 켬", 12.5, INK, KR, "middle", 600)
d.t(D_X + D_W / 2, D1_Y + 60, "이어서 동기화", 12, MUTED)
d.tone(D_X, D2_Y, D_W, D_H, WARN, 6, "14", 1.2)
d.t(D_X + D_W / 2, D2_Y + 34, "자동 동기화 끔", 12.5, INK, KR, "middle", 600)
d.t(D_X + D_W / 2, D2_Y + 60, "OutOfSync 로 두고 멈춤", 12, MUTED)

# 화살표
b1 = B1_Y + B_H / 2
b2 = B2_Y + B_H / 2
d.path(f"M {A_X + A_W + 2} {MID} L 167 {MID} L 167 {b1} L {B_X - 2} {b1}", MUTED, 1.4, m="ar")
d.path(f"M 167 {MID} L 167 {b2} L {B_X - 2} {b2}", MUTED, 1.4, m="ar")
d.path(f"M {B_X + B_W + 2} {b1} L 395 {b1} L 395 {MID - 20} L {C_X - 2} {MID - 20}", MUTED, 1.4, m="ar")
d.path(f"M {B_X + B_W + 2} {b2} L 395 {b2} L 395 {MID + 20} L {C_X - 2} {MID + 20}", MUTED, 1.4, m="ar")
d1 = D1_Y + D_H / 2
d2 = D2_Y + D_H / 2
d.path(f"M {C_X + C_W + 2} {MID} L 621 {MID} L 621 {d1} L {D_X - 2} {d1}", MUTED, 1.4, m="ar")
d.path(f"M 621 {MID} L 621 {d2} L {D_X - 2} {d2}", MUTED, 1.4, m="ar")

d.legend(448, [("저장소", INFO), ("감지 경로", PAPER2), ("새로 고침", ACC), ("동기화", OK), ("멈춤", WARN)])
d.save("12-01.detect-paths.svg")
