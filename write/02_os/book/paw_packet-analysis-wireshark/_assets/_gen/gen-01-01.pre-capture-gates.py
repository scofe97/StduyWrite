# 01-01 §3 — 캡처를 시작하기 전에 통과해야 하는 관문. 원문 도해(Wireshark Packet Capture Setup Process)를
# 다섯 단계 그대로 옮기되 조건 분기를 살린다.
# 타입 스펙: type-flowchart — 조건에 따라 갈라지는 판단 논리. 도형이 종류를 나른다(타원=시작·끝,
#           사각형=단계, 마름모=판단, 점=병합). focal 은 가장 결과가 큰 판단 하나(정책 허용 여부).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, BAD, PAPER2, RULE, KR, MONO

W, H = 880, 880
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 01-01 §3",
      "캡처 전에 통과할 다섯 관문",
      "조직 정책 확인에서 시작해 OS 캡처 지원, 인터페이스와 promiscuous 모드, Wi-Fi 라면 monitor 모드를 거쳐 캡처를 시작하는 판단 흐름.",
      "첫 마름모가 기술이 아니라 권한을 묻습니다 — 여기서 아니오면 나머지는 볼 필요가 없습니다")

CX = 280
def oval(cx, y, w, h, txt, c=INK):
    d.o.append(f'<rect x="{cx - w / 2}" y="{y}" width="{w}" height="{h}" rx="20" '
               f'fill="{PAPER2}" stroke="{c}" stroke-width="1.1"/>')
    d.t(cx, y + h / 2 + 5, txt, 13, c, KR, "middle", 600)

def step(cx, y, w, h, title, sub):
    d.box(cx - w / 2, y, w, h, PAPER2, RULE, 1.0, 6)
    d.t(cx, y + 24, title, 14, INK, KR, "middle", 600)
    d.t(cx, y + 44, sub, 12, MUTED, KR)

def diamond(cx, y, hw, hh, txt, focal=False):
    cy = y + hh
    c = ACC if focal else INK
    fill = f"{ACC}12" if focal else PAPER2
    d.o.append(f'<polygon points="{cx},{y} {cx + hw},{cy} {cx},{y + 2 * hh} {cx - hw},{cy}" '
               f'fill="{fill}" stroke="{c}" stroke-width="{1.4 if focal else 1.1}"/>')
    d.t(cx, cy + 5, txt, 13, c, KR, "middle", 600)

Y_START, Y_D1, Y_S1, Y_S2, Y_D2, Y_S3, Y_S4, Y_END = 96, 156, 260, 344, 428, 556, 640, 728

# 연결선 먼저
d.arrow([(CX, Y_START + 40), (CX, Y_D1 - 4)], MUTED, "ar", 1.4)
d.arrow([(CX, Y_D1 + 76), (CX, Y_S1 - 4)], MUTED, "ar", 1.4)            # 예
d.arrow([(CX + 130, Y_D1 + 38), (556, Y_D1 + 38)], BAD, "bad", 1.4)     # 아니오
d.arrow([(CX, Y_S1 + 60), (CX, Y_S2 - 4)], MUTED, "ar", 1.4)
d.arrow([(CX, Y_S2 + 60), (CX, Y_D2 - 4)], MUTED, "ar", 1.4)
d.arrow([(CX + 130, Y_D2 + 38), (556, Y_D2 + 38)], MUTED, "ar", 1.4)    # 예 → monitor
d.path(f"M {CX} {Y_D2 + 76} V 520", MUTED, 1.4)                          # 아니오 → 병합점
d.path(f"M 680 {Y_D2 + 68} V 520 H {CX}", MUTED, 1.4)                    # monitor → 병합점
d.o.append(f'<circle cx="{CX}" cy="520" r="4" fill="{INK}"/>')
d.arrow([(CX, 524), (CX, Y_S3 - 4)], MUTED, "ar", 1.4)
d.arrow([(CX, Y_S3 + 60), (CX, Y_S4 - 4)], MUTED, "ar", 1.4)
d.arrow([(CX, Y_S4 + 60), (CX, Y_END - 4)], MUTED, "ar", 1.4)

oval(CX, Y_START, 140, 40, "시작")
diamond(CX, Y_D1, 130, 38, "조직 정책이 허용하는가?", focal=True)
step(CX, Y_S1, 280, 60, "OS 가 캡처를 지원하는가", "Linux 기본 · Windows 는 별도 설치")
step(CX, Y_S2, 280, 60, "인터페이스 선택 + promiscuous", "자기 앞 주소가 아닌 프레임까지 받는다")
diamond(CX, Y_D2, 130, 38, "Wi-Fi 인터페이스인가?")
step(CX, Y_S3, 280, 60, "캡처 시작", "선택한 인터페이스에서 프레임 수집")
step(CX, Y_S4, 280, 60, "필터 · 통계 · 저장으로 분석", "여기부터가 2장의 내용")
oval(CX, Y_END, 140, 40, "끝")
oval(648, Y_D1, 184, 40, "여기서 멈춘다", BAD)
step(680, Y_D2 + 8, 240, 60, "monitor 모드로 전환", "남의 프레임까지 보려면 필수")

d.t(CX + 14, Y_D1 + 96, "예", 11, MUTED, MONO, "start", 600)
d.t(483, Y_D1 + 26, "아니오", 11, BAD, KR, "middle", 600)
d.t(CX - 12, Y_D2 + 92, "아니오", 11, MUTED, KR, "end", 600)
d.t(CX + 200, Y_D2 + 26, "예", 11, MUTED, MONO, "middle", 600)

d.legend(800, [("결과가 가장 큰 판단", ACC), ("캡처를 시작하지 않는 경로", BAD)])
d.save("01-01.pre-capture-gates.svg")
