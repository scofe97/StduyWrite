# 08-01 §2 — 원서의 기본 로그 한 줄을 앞 · 큰따옴표 안(요청) · 큰따옴표 뒤(응답) 세 묶음으로 가른다.
# 본문 근거: 이 노트 §2 의 로그 줄(원서 예시 값)과 Common Log Format 문자열(log README).
# 타입 스펙: type-layers — 한 줄을 세 겹의 묶음으로 쌓아 경계가 어디인지를 보인다. 칸 값은 원서 줄 그대로다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 530
d = D(W, H, "LEARNING COREDNS · 08-01 §2",
      "큰따옴표가 요청과 응답을 가른다",
      "기본 로그 한 줄의 칸을 세 묶음으로 나눴다. 앞 두 칸은 누가 보냈는지, 큰따옴표 안은 받은 질의, 큰따옴표 뒤는 돌려준 응답이다. "
      "값은 원서 예시 줄 그대로다.",
      "주황 묶음이 큰따옴표 안의 요청입니다")

groups = [
    ("앞 · 누가 보냈나", [("127.0.0.1:54308", "출발지"), ("31656", "메시지 ID")], False),
    ("큰따옴표 안 · 요청", [("A IN www.nxdomain.com.", "유형 · 클래스 · 이름"), ("udp 45", "프로토콜 · 길이"),
                       ("false", "DO 비트"), ("4096", "버퍼")], True),
    ("큰따옴표 뒤 · 응답", [("NXDOMAIN", "응답 코드"), ("qr,rd,ra", "플래그"), ("128", "응답 크기"),
                       ("0.172121417s", "처리 시간")], False),
]


def cw(v, n):
    kr = sum(1 for ch in n if "가" <= ch <= "힣")
    return max(len(v) * 7.9, kr * 12.5 + (len(n) - kr) * 6.6) + 28


Y0, GH, GAP = 116, 96, 16
for i, (title, chips, focal) in enumerate(groups):
    y = Y0 + i * (GH + GAP)
    if focal:
        d.tone(20, y, 840, GH, ACC, 8, "12", 1.4)
    else:
        d.box(20, y, 840, GH, PAPER2, RULE, 1.0, 8)
    d.t(36, y + 24, title, 13, ACC if focal else INK, KR, "start", 600)
    x = 36
    for v, n in chips:
        w = cw(v, n)
        d.box(x, y + 36, w, 48, PAPER, RULE, 1.0, 4)
        d.t(x + 14, y + 56, v, 13, ACC if focal else INK, MONO, "start", 600)
        d.t(x + 14, y + 76, n, 12, MUTED, KR, "start")
        x += w + 12

d.t(20, 470, "시각 · 심각도 두 칸은 형식 문자열 밖 · 지금 텍스트 출력에는 시각이 없다", 13, MUTED, KR, "start")

d.legend(484, [("받은 질의", ACC)])
d.save("08-01.log-line.svg")
