# 타입 스펙: type-dp-security-matrix — 정책 없음 / ingress 8080 정책 / egress {} 정책 추가의 세 상태가 들어오는 연결·나가는 연결·허용된 요청의 응답을 어디까지 여는지 견주는 격자 (배정된 비교 타입은 스펙 목록에 없어 격자 문법의 이 타입으로 선언)
# 사실 출처: 추출본 cil12.txt 줄 44-58(정책 없음), 152-175(8080 허용·9113 타임아웃), 209-245(기본 허용→기본 거부, 나가는 연결 유지), 273-309(egress {} 뒤 이름 해석 타임아웃·응답 유지)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, BAD, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 436
LP, COMP_W, GAP, ROLE_W, ROLE_GAP = 12, 196, 12, 220, 14
HDR_Y, HDR_H = 96, 44
ROW_Y0, ROW_H, STRIDE = 152, 56, 68
RX = [LP + COMP_W + GAP + j * (ROLE_W + ROLE_GAP) for j in range(3)]


def fam(txt):
    return KR if any("가" <= c <= "힣" for c in txt) else MONO


d = D(W, H, "CILIUM UP AND RUNNING · 12-01 §2", "규칙이 붙은 방향만 기본 거부로 바뀐다",
      "정책 없음에서 ingress 8080 정책, egress {} 정책으로 갈수록 방향별로 닫히지만 허용된 요청의 응답은 계속 나간다",
      "방향마다 따로 판정되고 응답 패킷은 egress 규칙과 무관하다")

d.box(LP, HDR_Y, COMP_W, HDR_H, PAPER2, RULE, 0.9)
d.t(LP + COMP_W / 2, HDR_Y + 27, "적용 정책", 12, INK, KR, "middle", 600)
for j, nm in enumerate(["들어오는 연결", "나가는 연결", "허용된 요청의 응답"]):
    d.box(RX[j], HDR_Y, ROLE_W, HDR_H, PAPER2, SOFT, 1.0)
    d.t(RX[j] + ROLE_W / 2, HDR_Y + 27, nm, 12, INK, KR, "middle", 600)

rows = [
    ("정책 없음", "양방향 기본 허용",
     [("8080 · 9113 열림", OK), ("모든 목적지 열림", OK), ("정상 응답", OK)]),
    ("ingress 8080 정책", "ingress 만 기본 거부",
     [("8080 허용 · 9113 차단", INFO), ("외부 접속 유지", OK), ("정상 응답", OK)]),
    ("+ egress {} 정책", "양방향 기본 거부",
     [("8080 허용 · 9113 차단", INFO), ("이름 해석부터 차단", BAD), ("egress 차단에도 응답", ACC)]),
]

for i, (kind, mode, cells) in enumerate(rows):
    y = ROW_Y0 + i * STRIDE
    d.box(LP, y, COMP_W, ROW_H, PAPER2, RULE, 0.9, 4)
    d.t(LP + 12, y + 24, kind, 12, INK, fam(kind), "start", 600)
    d.t(LP + 12, y + 44, mode, 12, MUTED, KR, "start")
    for j, (txt, col) in enumerate(cells):
        if col == ACC:
            d.tone(RX[j], y, ROLE_W, ROW_H, ACC, r=4, op="16", sw=1.4)
            d.t(RX[j] + ROLE_W / 2, y + 33, txt, 12, ACC, fam(txt), "middle", 600)
        else:
            d.tone(RX[j], y, ROLE_W, ROW_H, col, r=4, op="14", sw=1.0)
            d.t(RX[j] + ROLE_W / 2, y + 33, txt, 12, INK, fam(txt), "middle")

d.legend(372, [("열림", OK), ("일부만 허용", INFO), ("차단", BAD), ("초점", ACC)])
d.save("12-01.default-deny-comparison.svg")
