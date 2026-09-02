# 11-01 전체 지도 — 절 여덟을 읽는 순서로 잇는다.
# 본문: "칸마다 절 번호와 그 절이 답하는 것 하나", "색이 붙은 칸이 저자가 이득의 대부분이라 적은 손잡이".
# 근거(원문 11.3.4 마지막): "Always define sidecar configurations for your workloads. This alone will
#       provide you with the majority of benefits."
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 답하는 것)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 카드 한 줄 stride 로 놓는다(01~10 과 같은 관례).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1240, 520
d = D(W, H, "ISTIO IN ACTION · 11-01",
      "컨트롤 플레인의 성능은 낡은 설정의 수명이다 — 읽는 순서",
      "11장 노트의 절 여덟을 읽는 순서로 이은 지도. 앞의 셋이 무엇이 느려지는지를 세우고, 가운데 둘이 "
      "그것을 어떻게 재는지를 정하며, 뒤의 셋이 손잡이를 순서대로 돌린다.",
      "자원 증설이 마지막인 이유가 이 순서 자체입니다")

CW, CH, GAP, X0 = 280, 96, 16, 36
Y1, Y2 = 104, 248
cards = [
    ("§1", "늦은 설정이 유령을 만든다", "없는 엔드포인트로 보낸다"),
    ("§2", "이벤트가 닿기까지 다섯 걸음", "일부러 늦추는 자리가 둘"),
    ("§3", "성능을 정하는 네 가지", "변경률 · 자원 · 수 · 크기"),
    ("§4", "지연 하나를 세 구간으로", "어디서 시간을 쓰는가"),
    ("§5", "포화 · 트래픽 · 오류", "방향이 처방을 가른다"),
    ("§6", "기본은 모두가 모두를 안다", "Sidecar 가 2MB 를 깎는다"),
    ("§7", "배칭 손잡이 넷", "지연 지표가 못 세는 구간"),
    ("§8", "자원은 마지막 손잡이", "오토스케일링은 아직 안 먹는다"),
]
FOCAL = 5
def pos(i):
    if i < 4: return X0 + i * (CW + GAP), Y1
    return X0 + (i - 4) * (CW + GAP), Y2
def card(i):
    x, Y = pos(i); n, title, q = cards[i]; focal = (i == FOCAL)
    if focal:
        d.o.append(f'<rect x="{x}" y="{Y}" width="{CW}" height="{CH}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, Y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, Y + 26, n, 11, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 16, Y + 52, title, 13, ACC if focal else INK, KR, "start", 600)
    d.t(x + 16, Y + 76, q, 11, MUTED, KR, "start")
for i in range(7):
    x1, y1 = pos(i); x2, y2 = pos(i + 1)
    if y1 == y2:
        d.arrow([(x1 + CW, y1 + CH / 2), (x2 - 2, y2 + CH / 2)], MUTED, "ar", 1.4)
    else:
        d.path(f"M {x1 + CW / 2} {y1 + CH} L {x1 + CW / 2} 224 L {x2 + CW / 2} 224 L {x2 + CW / 2} {y2 - 2}", MUTED, 1.4, m="ar")
for i in range(8):
    card(i)

d.t(32, 396, "손잡이의 순서는 일을 줄이는 것부터다 — 무시하기 · 묶기 · 좁히기를 다 해 본 뒤에 자원을 늘린다", 11, SOFT, KR, "start")
d.t(32, 420, "저자가 든 기준값 — 서비스 1,000개와 워크로드 2,000개를 vCPU 하나와 메모리 1.5GB 로 감당한다", 11, MUTED, KR, "start")
d.legend(444, [("이득의 대부분이 나온다고 적은 손잡이", ACC), ("그 앞뒤로 도는 손잡이", MUTED)])
d.save("11-01.chapter-overview.svg")
