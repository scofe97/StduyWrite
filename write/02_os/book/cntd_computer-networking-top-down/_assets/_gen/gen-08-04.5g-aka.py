# 타입 스펙: type-sequence — 네 당사자가 시간 축을 따라 메시지를 넘기고 마지막에 판정이 난다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §8.8.2 Figure 8.33 (책 611~614쪽) —
#   다섯 단계, 인증 벡터 네 조각, 판정이 고향 망 AUSF 에서 이루어진다는 것은 원문 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, Seq, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, WARN, KR, MONO


def kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 11, c, kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 17, sub, 11, MUTED, kr(sub))


W, H = 1000, 664
d = SeqKR(W, H, "SECTION 8.8.2 · 5G AUTHENTICATION WITH EAP-AKA'",
          "판정은 방문 망이 아니라 고향 망이 합니다",
          "기기의 신원과 암호 정보가 SIM 과 고향 망에만 있기 때문이다. 4G 에서 방문 망이 하던 역할이 옮겨 왔다.",
          "다섯 단계와 인증 벡터는 원문 Figure 8.33 의 것입니다")
d.lanes([("기기", "SIM"), ("SEAF", "방문 망"), ("AUSF", "고향 망"), ("UDM", "고향 망")],
        y0=118, lane_w=200)
d.rails(452)

d.msg("기기", "SEAF", "등록 요청 · IMSI", 196, INFO)
d.msg("SEAF", "AUSF", "TLS 터널 위로", 236, OK)
d.msg("AUSF", "UDM", "인증 벡터 요청", 276, MUTED)
d.msg("UDM", "AUSF", "AV 네 조각", 316, WARN)
d.msg("AUSF", "SEAF", "논스 · 인증 토큰", 356, WARN)
d.msg("SEAF", "기기", "그대로 전달", 396, WARN)
d.state("기기", "XRES_C 계산", 428, ACC)
d.msg("기기", "AUSF", "XRES_C", 452, ACC)
d.state("AUSF", "XRES 와 대조 · 판정", 484, ACC)

PY = 508
d.box(24, PY, 470, 96, PAPER2, RULE, 1.0)
d.t(44, PY + 26, "인증 벡터 네 조각", 12, INK, KR, "start", 600)
d.line(44, PY + 38, 474, PY + 38, RULE, 0.8)
for i, ln in enumerate(["무작위 논스 · 인증 토큰(순서 번호 포함)",
                        "XRES(기대 응답) · 이후 열쇠 유도용 열쇠"]):
    d.t(44, PY + 62 + i * 22, ln, 11, MUTED, KR, "start")

d.tone(514, PY, 462, 96, ACC, 8, "16", 1.3)
d.t(534, PY + 26, "앵커 열쇠", 12, ACC, KR, "start", 600)
d.t(534, PY + 52, "인증이 끝나면 방문 망에 한 번짜리 대칭 열쇠를 넘깁니다.", 11, MUTED, KR, "start")
d.t(534, PY + 74, "기기도 같은 값을 스스로 계산합니다 — WiFi 의 PMK 와 같은 자리입니다.", 11, MUTED, KR, "start")

d.legend(616, [("기기가 여는 것", INFO), ("보호 통로", OK), ("고향 망이 만든 것", WARN), ("판정과 열쇠", ACC)])
out = pathlib.Path(__file__).resolve().parent.parent / "08-04.5g-aka.svg"
d.save(out); print("→", out.name)
