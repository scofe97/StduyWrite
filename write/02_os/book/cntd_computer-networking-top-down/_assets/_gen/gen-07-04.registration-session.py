# 타입 스펙: type-swimlane — 역할을 가로지르며 넘겨받는 절차. 등록과 세션 수립이 네 참여자를 지난다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §7.4.3 Figure 7.42 —
#   등록과 PDU 세션 수립의 단계, 그리고 AMF 의 조율 역할은 원문 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, KR, MONO

W, H = 940, 644
d = D(W, H, "SECTION 7.4.3 · REGISTRATION AND SESSION ESTABLISHMENT",
      "신원을 밝히고 나서야 데이터 길이 열립니다",
      "등록은 서로를 인증하는 단계이고, 세션 수립은 IP 주소를 받고 터널을 여는 단계다. AMF 가 둘을 조율한다.",
      "단계 구성은 원문 Figure 7.42 의 것입니다")

LX, LW = 24, 156
CX0, CW = 196, 176
STAGES = ["1 · 연결 설정", "2 · 신원과 인증", "3 · 등록 완료", "4 · 세션 수립"]
LANES = [
    (150, "무선 기기", INFO, ["RRC 연결 설정", "신원 정보 제출", "", "세션 수립 요청"]),
    (246, "기지국", INFO, ["AMF 를 하나 고름", "", "", "무선 데이터 평면 구성"]),
    (342, "AMF", ACC, ["등록 요청 전달", "인증 기능에 위임", "가입 정보 등록", "SMF 를 하나 고름"]),
    (438, "그 밖의 코어 기능", OK, ["", "AUSF 가 상호 인증", "UDM 에 저장", "SMF 가 UPF 와 터널"]),
]
LH = 84
for i, s in enumerate(STAGES):
    d.t(CX0 + i * CW + CW / 2, 130, s, 11, SOFT, KR, "middle", 600)
d.line(CX0, 140, CX0 + len(STAGES) * CW, 140, RULE, 0.8)
for ly, name, c, cells in LANES:
    d.tone(LX, ly, LW, LH, c, 6, "12", 1.2)
    d.t(LX + LW / 2, ly + 50, name, 12, c, KR, "middle", 600)
    for i, txt in enumerate(cells):
        x = CX0 + i * CW
        if txt:
            d.tone(x + 6, ly + 14, CW - 12, LH - 28, c, 4, "22", 1.2)
            d.t(x + CW / 2, ly + 46, txt, 11, c, KR)
        else:
            d.box(x + 6, ly + 14, CW - 12, LH - 28, PAPER, RULE, 0.7, 4)
d.arrow([(CX0, 546), (CX0 + len(STAGES) * CW, 546)], SOFT, "soft", 1.2)
d.t(CX0 + len(STAGES) * CW / 2, 566, "시간", 10, SOFT, KR)

d.legend(588, [("기기와 기지국", INFO), ("조율하는 기능", ACC), ("나머지 코어 기능", OK)])

out = pathlib.Path(__file__).resolve().parent.parent / "07-04.registration-session.svg"
d.save(out)
print("→", out)
