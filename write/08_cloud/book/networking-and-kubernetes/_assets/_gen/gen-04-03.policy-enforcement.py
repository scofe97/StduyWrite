# 04-03.policy-enforcement — 라벨로 쓴 정책을 CNI 가 커널이 아는 형태로 번역한다
# 본문 요구: 「라벨을 주소로 번역하는 CNI」 — 커널은 라벨을 모른다. Calico 는 선택자에 맞는 엔드포인트 주소를 IP set 에 담고 Felix 가
#           다시 점검(기본 90초), Cilium 은 라벨에서 도출한 identity 로 보안을 표현한다(Pod 가 새로 떠도 identity 조회만 하면 된다).
# 타입 스펙: type-layers — 선언 층 → 번역 층 → 집행 층. 번역 층 하나만 focal 이고, 그 층 안에서 구현 둘을 나란히 둔다.
#           2026-11-08 출처 없는 값(eBPF 정책 맵 조회, 가짜 iptables 한 줄, 숫자 identity)을 걷고 문서에 있는 문장만 남겼다.
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 552
d = D(W, H, "NETWORKPOLICY · FROM LABELS TO KERNEL RULES",
      "커널은 라벨을 모른다. 그 사이를 CNI 가 번역한다",
      "정책은 라벨로 쓰지만 집행은 L3·L4 에서 이뤄지므로, Calico 는 선택자에 맞는 Pod 주소를 IP set 에 담고 "
      "Cilium 은 라벨에서 도출한 identity 로 보안을 표현해 커널에 내려보낸다.",
      lead="선언은 라벨 · 집행은 주소와 포트 · 그 사이가 번역 계층")

LX, LW = 56, 888
LEFT = LX + 20                        # 층 머리 x
CONTENT = LX + 248                    # 층 내용 시작 x


def head(y, tag, name, sub, c):
    d.t(LEFT, y + 24, tag, 11, c, MONO, "start", 600)
    d.t(LEFT, y + 48, name, 14, c if c is ACC else INK, KR, "start", 600)
    if sub: d.t(LEFT, y + 70, sub, 12, MUTED, KR, "start")


# 1 선언
Y1, H1 = 104, 88
d.box(LX, Y1, LW, H1, PAPER2, INFO, 1.2, 8)
head(Y1, "DECLARE", "NetworkPolicy", "사람이 쓰는 라벨", INFO)
d.t(CONTENT, Y1 + 40, "podSelector: app=demo-db", 12, INK, MONO, "start")
d.t(CONTENT + 312, Y1 + 40, "from: app=demo", 12, INK, MONO, "start")
d.t(CONTENT, Y1 + 64, "ports: 80/TCP", 12, INK, MONO, "start")

# 2 번역 (focal)
Y2, H2 = 216, 176
d.tone(LX, Y2, LW, H2, ACC, 8, "0F", 1.4)
head(Y2, "TRANSLATE", "CNI 에이전트", "API 서버 watch", ACC)
d.t(LEFT, Y2 + 94, "라벨 → 현재 Pod 목록", 12, MUTED, KR, "start")
CW, CH, CY = 296, 144, Y2 + 16
for i, (title, c, l1, l2, l3) in enumerate([
        ("Calico · 라벨 → IP set", INK, "선택자에 맞는 엔드포인트 주소", "IP set 에 담음", "iptables 에서는 90초마다 다시 점검"),
        ("Cilium · 라벨 → identity", INK, "라벨에서 도출한 Pod 의 신원", "같은 라벨의 Pod 는 identity 를 공유", "새 Pod 는 key-value store 조회만")]):
    cx = CONTENT + i * (CW + 16)
    d.box(cx, CY, CW, CH, PAPER, c, 1.1, 6)
    d.t(cx + 16, CY + 30, title, 13, c, KR, "start", 600)
    d.t(cx + 16, CY + 62, l1, 12, MUTED, KR, "start")
    d.t(cx + 16, CY + 88, l2, 12, INK, KR, "start")
    d.t(cx + 16, CY + 118, l3, 12, SOFT, KR, "start")

# 3 집행
Y3, H3 = 416, 72
d.box(LX, Y3, LW, H3, PAPER2, RULE, 1.1, 8)
head(Y3, "ENFORCE", "커널", None, MUTED)
d.t(CONTENT, Y3 + 44, "주소 · 포트 · 프로토콜", 13, INK, KR, "start", 600)
d.t(LX + LW - 24, Y3 + 44, "라벨 모름", 13, BAD, KR, "end", 600)

# 층 사이 — 머리 열에서 아래로
for ya, yb in ((Y1 + H1, Y2), (Y2 + H2, Y3)):
    d.arrow([(LX + 168, ya + 4), (LX + 168, yb - 8)], MUTED, "ar", 1.4)

d.legend(504, [("라벨로 말하는 층", INFO), ("번역하는 층", ACC), ("라벨을 모르는 집행 층", BAD)])
d.save("04-03.policy-enforcement.svg")
print("ok policy-enforcement")
