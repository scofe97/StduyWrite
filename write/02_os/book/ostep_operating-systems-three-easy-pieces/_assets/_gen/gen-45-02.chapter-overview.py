# 45-02 개념도 — 통로를 세우고, 그 안에서 인증하고, 신원을 이어 가는 세 구간을 왼쪽에서 오른쪽으로 놓고, 아래에서 믿음의 출발점이 받친다.
# 본문 요구(45-02 「학습 목표」 개념도 문단): 가운데 세 구간(통로 세우기 §1·§2, 통로 안에서 인증 §3, 신원 이어 가기 §5),
#           구간 끝의 보증 한계(§6 인증서의 좁은 보증, §5 쿠키의 남는 문제), 곁가지(도전 응답·인증 서버 §5, 규격·구현 결함 §4),
#           위의 이미 푼 도구(HTTPS §6, SSH §7), 아래의 믿음의 출발점(인증 기관 키 §6, 호스트 키 §7).
# 값 근거: 본문 핵심 요약과 §1~§7 의 `>` 요약. 낱말은 모두 본문에 있는 것이다.
# 타입 스펙: type-architecture — 구성요소를 존으로 묶고 라벨 붙은 화살표로 잇는 노드 그래프. 고른 이유: 이 편의 줄기가
#             「통로가 서야 인증이 서고 인증이 서야 신원을 잇는다」는 쌓는 순서와 그 아래 받침이라, 구간마다 관계 라벨이 붙은
#             화살표가 있어야 읽힌다. type-layers 는 층 사이에 라벨 붙은 화살표를 못 그리고 type-process 의 행 반복 슬롯은
#             옛 격자와 같은 모양이 된다. 스펙에 줄기 전용 공식은 없어 좌표는 4 의 배수 stride 로 직접 잡았다.
#             (옛 판의 7행 × 3열 격자 공식 열 x = 64 + j·344 는 쓰지 않는다.)
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, INFO, KR, MONO

W, H = 984, 836


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "ARCHITECTURE · 45-02 OVERVIEW",
      "통로를 세워 인증하고 신원을 이어 가며 믿음은 출발점에서 시작한다",
      "45-02 의 키워드 개념도. 가운데에 세 구간이 왼쪽에서 오른쪽으로 이어진다. 첫 구간은 통로 세우기로, 연결마다 새 키를 합의하고 "
      "서버가 서명해 상대를 확인하며, 보증은 서버의 인증서와 서명이 닿는 곳까지다. 둘째 구간은 선 통로 안에서 비밀번호로 클라이언트를 인증하는 것이고 "
      "도전 응답과 인증 서버는 곁가지다. 셋째 구간은 쿠키가 신원을 이어 가는 것이고 브라우저를 쓰는 다른 사람도 인증된다는 문제가 남는다. "
      "첫 구간의 보증 끝에서 규격 결함과 구현 결함을 가르는 곁가지가 나온다. 위에는 같은 문제를 이미 푼 HTTPS 와 SSH 가 있고, "
      "아래에는 미리 설치된 인증 기관 키와 첫 접속의 호스트 키라는 믿음의 출발점이 세 구간을 받친다.",
      lead="아래에서 위로 믿음이 받치고 가운데는 왼쪽에서 오른쪽으로 읽습니다. 화살표에 붙은 글자는 관계, 칩은 다루는 절입니다.")

NH = 64


def node(x, y, w, title, sub, c, sec):
    d.tone(x, y, w, NH, c, 6, "14", 1.1)
    d.chip(x + 24, y + 14, sec, c, 11)
    d.t(x + w / 2, y + 40, title, 14, c, kr(title), "middle", 600)
    d.t(x + w / 2, y + 58, sub, 13, MUTED, kr(sub), "middle")


# 위 — 이미 푼 도구
d.box(24, 108, 936, 88, "#161B22", RULE, 1.0, 8)
d.t(48, 158, "같은 문제를 푼 도구", 14, INK, KR, "start", 600)
node(260, 120, 330, "HTTPS", "HTTP 를 TLS 위에 · HSTS", OK, "§6")
node(614, 120, 330, "SSH", "TLS 와 따로 구현", OK, "§7")

# 가운데 — 세 구간
FX, FY, FW, FH = 24, 244, 936, 368
d.box(FX, FY, FW, FH, "#161B22", RULE, 1.0, 8)
CW = 216
C1, C2, C3 = 40, 384, 728
R1, R2, R3 = 304, 416, 528
for x, cap in ((C1, "통로 세우기"), (C2, "통로 안에서 인증"), (C3, "신원 이어 가기")):
    d.t(x, 272, cap, 13, MUTED, KR, "start", 600)
    d.line(x, 280, x + CW, 280, RULE, 0.8)

# 구간 1 — 통로 세우기
node(C1, R1, CW, "연결마다 새 키", "순방향 비밀성", OK, "§1")
node(C1, R2, CW, "서버의 서명", "중간자를 막음", OK, "§2")
node(C1, R3, CW, "보증하는 범위", "인증서와 서명이 닿는 곳까지", INFO, "§6")
CX1 = C1 + CW // 2
d.arrow([(CX1, R1 + NH + 4), (CX1, R2 - 4)], MUTED, "ar", 1.4)
d.t(CX1 + 12, R1 + NH + 28, "상대를 알 수 없어", 13, MUTED, KR, "start", 600)
d.arrow([(CX1, R2 + NH + 4), (CX1, R3 - 4)], INFO, "info", 1.4)
d.t(CX1 + 12, R2 + NH + 28, "남는 문제", 13, MUTED, KR, "start", 600)

# 구간 2 — 통로 안에서 인증
node(C2, R1, CW, "도전 응답 · 인증 서버", "HMAC · Kerberos", MUTED, "§5")
node(C2, R2, CW, "비밀번호", "통로가 선 뒤에 보냄", OK, "§3")
node(C2, R3, CW, "규격 결함 · 구현 결함", "영향받는 범위가 갈림", MUTED, "§4")
CX2 = C2 + CW // 2
d.arrow([(CX2, R2 - 4), (CX2, R1 + NH + 4)], SOFT, "soft", 1.3, "4 3")
d.t(CX2 + 12, R1 + NH + 28, "비밀번호 밖의 방법", 13, MUTED, KR, "start", 600)

# 구간 3 — 신원 이어 가기
node(C3, R2, CW, "쿠키", "Secure · HttpOnly", OK, "§5")
node(C3, R3, CW, "남는 문제", "다른 사람도 인증됨", INFO, "§5")
CX3 = C3 + CW // 2
d.arrow([(CX3, R2 + NH + 4), (CX3, R3 - 4)], INFO, "info", 1.4)
d.t(CX3 + 12, R2 + NH + 28, "풀리지 않는", 13, MUTED, KR, "start", 600)

# 구간을 잇는 화살표
YM = R2 + NH // 2
d.arrow([(C1 + CW + 2, YM), (C2 - 4, YM)], OK, "ok", 1.5)
d.t((C1 + CW + C2) / 2, YM - 10, "통로가 서면", 13, MUTED, KR, "middle", 600)
d.arrow([(C2 + CW + 2, YM), (C3 - 4, YM)], OK, "ok", 1.5)
d.t((C2 + CW + C3) / 2, YM - 10, "다시 묻지 않게", 13, MUTED, KR, "middle", 600)
# 보증의 끝에서 곁가지로
YB = R3 + NH // 2
d.arrow([(C1 + CW + 2, YB), (C2 - 4, YB)], SOFT, "soft", 1.3, "4 3")
d.t((C1 + CW + C2) / 2, YB - 10, "문제 소식이 오면", 13, MUTED, KR, "middle", 600)

# 구간과 위아래의 관계
MX = 492
d.arrow([(MX, FY - 4), (MX, 200)], OK, "ok", 1.5)
d.t(MX + 12, FY - 16, "새로 짜지 않고 쓴다", 13, MUTED, KR, "start", 600)

# 아래 — 믿음의 출발점
BY = 660
d.tone(24, BY, 936, 104, ACC, 8, "1e", 1.4)
d.t(48, BY + 48, "믿음의 출발점", 16, ACC, KR, "start", 700)
d.t(48, BY + 72, "한계를 그대로 지님", 13, MUTED, KR, "start")
node(260, BY + 20, 330, "미리 설치된 인증 기관 키", "HTTPS · 브라우저", ACC, "§6")
node(614, BY + 20, 330, "첫 접속의 호스트 키", "SSH · known_hosts", ACC, "§7")
d.arrow([(MX, BY - 4), (MX, FY + FH + 4)], ACC, "acc", 1.5)
d.t(MX + 12, BY - 16, "믿음은 여기서 시작", 13, MUTED, KR, "start", 600)

d.legend(H - 40, [("남는 문제", INFO), ("대응", OK), ("믿음의 출발점", ACC), ("곁가지", MUTED)])
d.save("45-02.chapter-overview.svg")
print("ok 45-02 overview")
