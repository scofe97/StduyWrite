# 타입 스펙: type-tree — 신뢰가 뿌리 하나에서 갈라져 내려온다. 뿌리를 못 믿으면 아래가 전부 무너진다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §8.3.3 Public Key Certification (책 581~582쪽) —
#   CA 의 두 역할, 피자 장난 예, X.509 와 RFC 1422, 표 8.4 필드는 원문 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, BAD, KR, MONO

W, H = 1000, 600
d = D(W, H, "SECTION 8.3.3 · PUBLIC KEY CERTIFICATION",
      "신뢰는 뿌리 하나만큼만 갑니다",
      "인증서는 공개키와 신원을 묶어 CA 가 서명한 것이다. 그 서명을 믿는 근거는 CA 를 믿는 것뿐이다.",
      "CA 의 두 역할과 표준 이름은 원문 §8.3.3 의 것입니다")

RX, RW = 352, 296
d.tone(RX, 140, RW, 72, ACC, 8, "18", 1.4)
d.t(RX + RW / 2, 168, "인증기관 (CA)", 13, ACC, KR, "middle", 600)
d.t(RX + RW / 2, 190, "신원을 확인하고 인증서에 서명합니다", 11, MUTED, KR)

KIDS = [(56, "밥의 인증서", "공개키 + 신원", OK), (368, "앨리스의 인증서", "공개키 + 신원", OK),
        (680, "다른 개체의 인증서", "공개키 + 신원", OK)]
KY = 292
for x, name, sub, c in KIDS:
    d.tone(x, KY, 264, 72, c, 7, "14", 1.2)
    d.t(x + 132, KY + 30, name, 12, c, KR, "middle", 600)
    d.t(x + 132, KY + 52, sub, 11, MUTED, KR)
    d.path(f"M {RX + RW / 2} 216 L {RX + RW / 2} 256 L {x + 132} 256 L {x + 132} {KY - 4}",
           ACC, 1.3, m="acc")

PY = 400
d.box(24, PY, 470, 108, PAPER2, RULE, 1.0)
d.t(44, PY + 28, "CA 가 하는 일 둘", 12, INK, KR, "start", 600)
d.line(44, PY + 40, 474, PY + 40, RULE, 0.8)
for i, ln in enumerate(["1. 그 개체가 자기 말대로인지 확인합니다.",
                        "2. 공개키와 신원을 묶은 인증서를 만들어 서명합니다."]):
    d.t(44, PY + 66 + i * 22, ln, 11, MUTED, KR, "start")

d.tone(514, PY, 462, 108, BAD, 8, "14", 1.3)
d.t(534, PY + 28, "확인 절차는 표준으로 정해져 있지 않습니다", 12, BAD, KR, "start", 600)
d.t(534, PY + 56, "트루디가 아무 CA 에 걸어 들어가 \"나는 앨리스다\" 라고", 11, MUTED, KR, "start")
d.t(534, PY + 78, "말하고 인증서를 받는다면 그 CA 는 믿을 것이 못 됩니다.", 11, MUTED, KR, "start")

d.t(24, 540, "표준은 ITU X.509 와 RFC 1422 입니다. RFC 1422 는 X.509 와 호환되면서 열쇠 관리 절차를 더 얹습니다.",
    11, SOFT, KR, "start")
d.legend(556, [("신뢰의 뿌리", ACC), ("발급된 인증서", OK), ("뿌리가 약할 때", BAD)])
out = pathlib.Path(__file__).resolve().parent.parent / "08-02.certification.svg"
d.save(out); print("→", out.name)
