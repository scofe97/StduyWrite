# 05-02 §4 — 가장 느린 HTTP 응답을 찾는 절차. 원문 http_01.pcap 예제의 세 단계를 판단 흐름으로.
# 타입 스펙: type-flowchart — 조건에 따라 갈라지는 판단 논리. focal 은 결과를 바꾸는 설정 하나
#           (재조립 해제). 도형이 종류를 나른다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, INFO, PAPER2, RULE, KR, MONO

W, H = 880, 636
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 05-02 §4",
      "가장 느린 응답을 찾는 순서",
      "원문이 제시하는 세 단계. 재조립 설정을 먼저 끄는 이유는 한 응답이 몇 개의 세그먼트로 쪼개져 왔는지를 세기 위해서다. 그 개수가 TCP 튜닝의 근거가 된다.",
      "첫 칸의 설정이 결과를 바꿉니다 — 켜 두면 세그먼트 수가 안 보입니다")

CX = 320
def oval(cx, y, w, h, txt, c=INK):
    d.o.append(f'<rect x="{cx - w / 2}" y="{y}" width="{w}" height="{h}" rx="20" '
               f'fill="{PAPER2}" stroke="{c}" stroke-width="1.1"/>')
    d.t(cx, y + h / 2 + 5, txt, 13, c, KR, "middle", 600)

def step(cx, y, w, h, title, sub, c=None, focal=False):
    if focal:
        d.o.append(f'<rect x="{cx - w / 2}" y="{y}" width="{w}" height="{h}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    elif c: d.tone(cx - w / 2, y, w, h, c, 6)
    else: d.box(cx - w / 2, y, w, h, PAPER2, RULE, 1.0, 6)
    col = ACC if focal else (c if c else INK)
    d.t(cx, y + 24, title, 13, col, KR, "middle", 600)
    d.t(cx, y + 44, sub, 11, MUTED, KR)

Y = [96, 196, 296, 396, 512]
d.arrow([(CX, Y[0] + 40), (CX, Y[1] - 4)], MUTED, "ar", 1.4)
for i in (1, 2, 3):
    d.arrow([(CX, Y[i] + 68), (CX, Y[i + 1] - 4)], MUTED, "ar", 1.4)

oval(CX, Y[0], 300, 40, "응답이 느린 요청을 찾는다")
step(CX, Y[1], 440, 68, "TCP 재조립을 끕니다",
     "Preferences | Protocols | TCP · Allow subdissector 해제", focal=True)
step(CX, Y[2], 440, 68, "http.time 을 열로 올립니다",
     "http.response.code == 200 패킷에서 가져옵니다")
step(CX, Y[3], 440, 68, "내림차순으로 정렬합니다",
     "맨 위 줄에서 요청 프레임 링크를 따라갑니다")
oval(CX, Y[4], 440, 40, "세그먼트 수가 곧 튜닝의 근거", OK)

d.t(CX + 260, Y[1] + 34, "재조립을 켜 두면", 11, MUTED, KR, "start")
d.t(CX + 260, Y[1] + 52, "continuation 이 합쳐져", 11, MUTED, KR, "start")
d.t(CX + 260, Y[1] + 70, "개수를 못 셉니다", 11, MUTED, KR, "start")

d.legend(H - 60, [("결과를 바꾸는 설정", ACC), ("얻는 것", OK)])
d.save("05-02.http-response-time.svg")
