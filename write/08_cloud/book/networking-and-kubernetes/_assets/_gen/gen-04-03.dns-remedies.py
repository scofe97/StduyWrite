# 04-03.dns-remedies — 질의 횟수를 줄이는 처방 셋은 고치는 자리로 갈린다
# 본문 요구: "처방은 고치는 자리로 갈립니다. 앱에서 고칠지, Pod 설정에서 고칠지, 서버에서 고칠지 …
#           가장 싼 것은 앱 쪽 … ndots 를 낮추면 짧은 서비스 이름이 안 풀릴 수 있어 … Autopath 는 CoreDNS 메모리가 는다"
# 타입 스펙: type-layers — 층이 곧 고치는 자리(앱 → Pod 설정 → DNS 서버). 층마다 무엇을 하고 무엇을 치르는지를
#           같은 칸에 반복한다. focal 은 가장 싼 앱 층 하나. 손으로 쓴 SVG 를 2026-09-15 생성기로 옮겼다.
from dd import D, INK, MUTED, SOFT, RULE, ACC, PAPER, PAPER2, KR, MONO

W, H = 1000, 440
d = D(W, H, "CLUSTER DNS · THREE WAYS TO CUT THE QUERIES",
      "질의 횟수를 줄이는 처방 셋",
      "클라이언트가 처음부터 완전한 이름을 쓰거나 임계값을 낮추거나 서버가 검색 경로를 대신 완성하는 "
      "세 가지로 질의 횟수를 줄인다.",
      lead="셋 다 줄이는 값은 검색 경로를 도는 횟수 · 갈리는 것은 고치는 자리")

LX, LW = 60, 880
LY0, LH = 144, 72
COL = {"tag": LX + 20, "name": LX + 116, "what": LX + 376, "cost": LX + 640}
HY = 128
d.t(COL["name"], HY, "고치는 자리", 12, SOFT, KR, "start", 600)
d.t(COL["what"], HY, "무엇을 하나", 12, SOFT, KR, "start", 600)
d.t(COL["cost"], HY, "치르는 값", 12, SOFT, KR, "start", 600)

LAYERS = [
    ("APP", "앱 코드", "이름 끝에 점", ("api.pay.example.com.", True), "검색 경로 생략", "문자열 한 글자", "가장 싼 처방"),
    ("POD", "Pod 설정", "dnsConfig", ("options ndots:2", True), "검색 경로 축소", "짧은 이름 해석 실패 위험", "Pod 마다 조정"),
    ("SERVER", "DNS 서버", "CoreDNS Autopath", ("검색 경로 대신 완성", False), "CNAME 으로 한 번에 응답", "CoreDNS 메모리 증가", "앱 무수정"),
]
for i, (tag, name, sub, (what, mono), what2, cost, cost2) in enumerate(LAYERS):
    y = LY0 + i * LH
    focal = i == 0
    if focal:
        d.tone(LX, y, LW, LH, ACC, 0, "12", 1.4)
    else:
        d.box(LX, y, LW, LH, PAPER2 if i % 2 else PAPER, RULE, 1.0, 0)
    d.t(COL["tag"], y + 40, tag, 11, ACC if focal else SOFT, MONO, "start", 600)
    d.t(COL["name"], y + 30, name, 15, ACC if focal else INK, KR, "start", 600)
    d.t(COL["name"], y + 52, sub, 12, MUTED, KR, "start")
    d.t(COL["what"], y + 30, what, 13, INK, MONO if mono else KR, "start", 600)
    d.t(COL["what"], y + 52, what2, 12, MUTED, KR, "start")
    d.t(COL["cost"], y + 30, cost, 13, ACC if focal else INK, KR, "start", 600)
    d.t(COL["cost"], y + 52, cost2, 12, MUTED, KR, "start")

d.legend(392, [("가장 싼 처방", ACC)])
d.save("04-03.dns-remedies.svg")
print("ok dns-remedies")
