# 10-03 §4 — 면죄에서 시작해 실험으로 가리고 튜닝으로 끝내는 흐름.
# 타입 스펙: type-process — 분석 단계가 차례로 이어지고 화살표가 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 §1 lanes 와 §2 공식을 쓰지 않고 카드 stride 로 놓는다
#           (visual-diagram-selection §알려진 공백 "주체 없는 단계 지도" 관례).
# ⚠ 2026-09-22 도식 검증: 01 단계 괄호를 "설정 점검(정적 성능 튜닝)"으로 뒤집어 적었다가 본문 표기(원서 이름 앞, 풀이는 괄호)로 맞췄다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 952, 392
CW, CH, GAP, X0, Y = 204, 148, 28, 32, 128

d = DK(W, H, "SYSTEMS PERFORMANCE · 10-03 §4",
       "네트워크 분석의 흐름",
       "내 호스트를 먼저 확인해 혐의를 좁히고, 실험으로 네트워크를 가린 뒤, 원인을 찾았을 때만 손잡이를 돌린다.",
       "실험의 자리는 애플리케이션 디버깅 앞입니다 — 네트워크를 먼저 가립니다")

STEPS = [
    ("01", "내 호스트 확인", ["모니터링 · USE", "정적 성능 튜닝(설정 점검)", "워크로드 특성화"], None),
    ("02", "원천 좁히기", ["지연 분석: 어느 구간", "TCP 분석: 무엇이 막나", "포트 고갈 조건 계산"], None),
    ("03", "실험으로 가리기", ["iperf: 대량 전송 한도", "앱보다 단순", "앱에 옮길 조건 확인"], ACC),
    ("04", "튜닝", ["근거 관측이 있을 때", "대가 확인 후 변경", "sysctl · setsockopt"], None),
]

for i, (n, name, body, c) in enumerate(STEPS):
    x = X0 + i * (CW + GAP)
    if c: d.tone(x, Y, CW, CH, c, 8)
    else: d.box(x, Y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.o.append(f'<rect x="{x + 16}" y="{Y + 16}" width="22" height="18" rx="9" '
               f'fill="{c if c else PAPER}" stroke="{c if c else RULE}" stroke-width="1"/>')
    d.t(x + 27, Y + 29, n, 9, PAPER if c else MUTED, MONO)
    d.t(x + 48, Y + 29, name, 14, c if c else INK, KR, "start", 600)
    for j, line in enumerate(body):
        d.t(x + 16, Y + 60 + j * 20, line, 13, MUTED, KR, "start")
    if i < 3:
        d.arrow([(x + CW, Y + CH / 2), (x + CW + GAP - 6, Y + CH / 2)], MUTED, "ar", 1.3)

YB = Y + CH + 40
d.t(X0, YB, "패킷 스니핑 · 카운터·지연 측정으로 답이 안 날 때 · 짧게 · 마지막 수단", 13, WARN, KR, "start")

d.legend(YB + 24, [("네트워크를 가리는 단계", ACC), ("나머지 단계", MUTED), ("마지막 수단", WARN)])
d.save("10-03.network-methodology-flow.svg")
