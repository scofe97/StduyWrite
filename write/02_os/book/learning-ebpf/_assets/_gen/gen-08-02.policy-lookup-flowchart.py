# 타입 스펙: type-flowchart — 같은 출발지 10.0.0.68 의 패킷 셋이 받는 Pod 쪽에서 IP 캐시 맵 조회 → 정책 맵 조회 → 판정 마름모를 지나 전달·폐기·프록시로 갈라진다. focal 은 항목이 없어 폐기되는 결과 하나.
# 사실 출처: runners-high write/08_cloud/book/cilium-up-and-running/12-01 §3 (10.0.0.68 → identity 22727, (22727, Ingress, TCP, 8080) ALLOW, 항목 없는 TCP 9113 은 기본 거부),
#   같은 문서 3절 끝(결과는 전달·폐기·사용자 공간 프록시), 13-01(L7 규칙 필드 rules.http), 추출본 ebpf8.txt 1070~1082행(규칙에 안 맞으면 폐기, 라벨이 정한 identity 로 해시 표 조회),
#   Cilium v1.20.2 bpf/include/bpf/ctx/skb.h 26~27행(CTX_ACT_OK=TC_ACT_OK, CTX_ACT_DROP=TC_ACT_SHOT). 맵 이름은 본문에만 쓰고 도식 라벨은 문서의 Map Name 열(IP cache · Policy)을 쓴다.
#   방향: 출발지 IP 로 identity 를 푸는 것은 받는 엔드포인트의 ingress 정책 경우라 시작 노드를 "받는 Pod 로 가는 패킷"으로 두고 훅 이름은 쓰지 않는다.
# Layout conventions: 행 중심 y=176·288·400(stride 112), 시작 타원 x=24 w=176, 단계 상자 x=232·440 w=176·208 h=64, 마름모 중심 x=744 반폭 68·반높이 44, 결과 x=840 w=104. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 520
d = D(W, H, "LEARNING EBPF · 08-02 §3",
      "받는 Pod 로 가는 패킷은 두 단계 조회로 전달·프록시·폐기가 갈린다",
      "출발지 10.0.0.68 은 IP cache 에서 identity 22727 로 풀린다. Pod A 의 정책 맵에 (22727, Ingress, TCP, 8080) 항목이 있으면 전달하고 TCP 9113 은 항목이 없어 TC_ACT_SHOT 으로 폐기한다. Pod B 의 항목에 rules.http 가 있으면 프록시로 보낸다.",
      "IP 를 identity 로 풀고 정책 맵에서 그 identity 와 묶은 identity 로 찾습니다")

def kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

# 열 머리
for x, w, lab in ((24, 176, "패킷"), (232, 176, "1단계"), (440, 208, "2단계"), (676, 136, "항목?"), (840, 104, "동작")):
    d.t(x + w // 2, 116, lab, 13, SOFT, KR, "middle", 600)

ROWS = [
    (176, "10.0.0.68 → :8080", "Pod A", "(22727, Ingress, TCP, 8080)", "있음", "전달", "TC_ACT_OK", OK, False),
    (288, "10.0.0.68 → :9113", "Pod A", "(22727, Ingress, TCP, 9113)", "없음", "폐기", "TC_ACT_SHOT", ACC, True),
    (400, "10.0.0.68 → :8080", "Pod B · L7", "8080 · rules.http", "있음", "프록시", "L7 규칙", INFO, False),
]
for y, pkt, who, key, ans, res, code, c, focal in ROWS:
    mk = {OK: "ok", ACC: "acc", INFO: "info"}[c]
    # 화살표 먼저
    d.arrow([(200, y), (228, y)], MUTED, "ar", 1.4)
    d.arrow([(408, y), (436, y)], MUTED, "ar", 1.4)
    d.arrow([(648, y), (676, y)], MUTED, "ar", 1.4)
    d.arrow([(812, y), (836, y)], c, mk, 1.5)
    # 시작 타원
    d.o.append(f'<rect x="24" y="{y - 32}" width="176" height="64" rx="20" fill="{PAPER2}" stroke="{RULE}" stroke-width="1"/>')
    d.t(112, y - 4, pkt, 12, INK, MONO, "middle", 600)
    d.t(112, y + 18, who, 13 if kr(who) == KR else 12, MUTED, kr(who))
    # 조회 1
    d.box(232, y - 32, 176, 64, PAPER2, RULE, 1.0, 6)
    d.t(320, y - 4, "IP cache", 13, INK, MONO, "middle", 600)
    d.t(320, y + 18, "identity 22727", 12, MUTED, MONO)
    # 조회 2
    d.box(440, y - 32, 208, 64, PAPER2, RULE, 1.0, 6)
    d.t(544, y - 4, "Policy", 13, INK, MONO, "middle", 600)
    d.t(544, y + 18, key, 11, MUTED, MONO)
    # 마름모
    cx = 744
    pts = f"{cx-68},{y} {cx},{y-44} {cx+68},{y} {cx},{y+44}"
    d.o.append(f'<polygon points="{pts}" fill="{PAPER2}" stroke="{c}" stroke-width="1.2"/>')
    d.t(cx, y + 5, ans, 13, INK, KR, "middle", 600)
    # 결과
    if focal:
        d.o.append(f'<rect x="840" y="{y - 32}" width="104" height="64" rx="6" fill="{c}1F" stroke="{c}" stroke-width="1.4"/>')
    else:
        d.tone(840, y - 32, 104, 64, c, 6, "12", 1.2)
    d.t(892, y - 4, res, 13, c, KR, "middle", 600)
    d.t(892, y + 18, code, 13 if kr(code) == KR else 11, MUTED, kr(code))

d.legend(H - 56, [("전달", OK), ("프록시", INFO), ("항목 없어 폐기", ACC)])
d.save("08-02.policy-lookup-flowchart.svg")
