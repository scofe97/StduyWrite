# 08-01 §1 「원서의 이름표」 — 원서 표 8-1 의 지표 이름으로 쓴 경보 규칙이 지금 CoreDNS 에서 조용히 죽는 경로.
# 소스 근거: 1.7.0 릴리스 노트 "coredns_dns_response_rcode_count_total -> coredns_dns_responses_total"(본문 [^n170]).
#            Prometheus 에서 없는 시계열을 고르는 식은 오류가 아니라 빈 벡터를 돌려준다(본문 정답 8).
# 타입 스펙: type-flowchart — 규칙이 평가를 거쳐 경보에 이르는 단계마다 실제 값이 바뀌고, 마지막 칸의 침묵이 논지다.
#           경보 식의 임계값 1 은 설명용 예시 값이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, BAD, KR, MONO

W, H = 880, 510
d = D(W, H, "LEARNING COREDNS · 08-01 §1",
      "없는 지표를 묻는 경보는 조용히 죽는다",
      "원서의 이름으로 쓴 경보 규칙은 지금 CoreDNS 가 내놓지 않는 시계열을 찾는다. Prometheus 는 이를 오류로 보지 않고 빈 결과로 "
      "돌려주며, 빈 결과는 임계값을 넘을 수 없으니 경보는 울리지도 깨지지도 않는다.",
      "주황 칸이 아무 신호도 없는 끝입니다")

LX, LW, VX, VW = 20, 190, 230, 630
steps = [
    ("경보 규칙", "원서 이름 · 예시 임계값", 'rate(coredns_dns_response_rcode_count_total{rcode="SERVFAIL"}[5m]) > 1', None, INK, False),
    ("찾는 시계열", "지금 CoreDNS 기준", "시계열 0개", "지금 이름은 coredns_dns_responses_total (1.7.0)", BAD, False),
    ("평가 결과", "Prometheus", "빈 벡터", "오류가 아니므로 규칙 상태는 정상", INK, False),
    ("경보", "Alertmanager 로 가는 것", "아무것도 가지 않음", "울리지 않고 깨졌다는 신호도 없음", ACC, True),
]
Y0, PITCH, RH = 116, 82, 58
for i, (name, sub, main, note, col, focal) in enumerate(steps):
    y = Y0 + i * PITCH
    d.t(LX, y + 26, name, 14, INK, KR, "start", 600)
    d.t(LX, y + 46, sub, 12, MUTED, KR, "start")
    if focal:
        d.tone(VX, y, VW, RH, ACC, 6, "12", 1.4)
    else:
        d.box(VX, y, VW, RH, PAPER2, RULE, 1.0, 6)
    fam = KR if any("가" <= ch <= "힣" for ch in main) else MONO
    if note:
        d.t(VX + 14, y + 24, main, 13 if fam == KR else 12, col, fam, "start", 600)
        d.t(VX + 14, y + 45, note, 12, MUTED, KR, "start")
    else:
        d.t(VX + 14, y + 35, main, 12, col, fam, "start", 600)
    if i < len(steps) - 1:
        d.path(f"M {VX + VW / 2} {y + RH + 2} L {VX + VW / 2} {y + PITCH - 3}", MUTED, 1.3, m="ar")

d.t(20, 456, "대시보드도 같은 길 · 빈 그래프가 오류 없이 그려진다", 13, MUTED, KR, "start")

d.legend(470, [("신호 없는 끝", ACC), ("사라진 시계열", BAD)])
d.save("08-01.silent-alert.svg")
