# 06-02 §4 — 기본 Corefile 의 각 줄이 무엇을 켜고, 왜 있고, 언제 지울 수 있는가.
# 원문 근거: 원서가 Example 6-11 을 한 줄씩 해설한 내용 그대로. pods insecure 는 "provided for
#            backward compatibility with the prior default cluster DNS solution, kube-dns" /
#            upstream 은 "unnecessary in versions 1.4 and later of CoreDNS" / cache 는 "The use of
#            the cache here is not ideal" / loop 은 "prevents intermittent, very-difficult-to-debug
#            DNS failures" / loadbalance 는 "randomly shuffles A/AAAA records in the response".
# 타입 스펙: type-dp-security-matrix — 행×열 격자에서 어느 조합이 되고 안 되는가가 논지다.
#           좌표는 스펙 §2 Layout formulas 를 쓰되 이 저장소 D() 머리글만큼 32 내린다. 색은 다크 스킨 계약.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, OK, BAD, WARN, KR, MONO

LEFT_PAD, RIGHT_PAD = 12, 48
COMP_COL_W, COMP_ROLE_GAP = 232, 12
ROLE_COL_W, ROLE_COL_GAP = 208, 16
HEADER_H, ROW_H, ROW_STRIDE = 52, 36, 40
HEADER_Y = 104

cols = [("왜 거기 있나", "줄의 사연"), ("지울 수 있는 조건", "없으면 무엇이 깨지나")]
lines = [
    ("errors", "오류를 로그로", ("없으면 SERVFAIL 만 남는다", "keep"), ("지우지 않는다", "keep")),
    ("health", "kubelet 이 부른다", ("프로브가 이 엔드포인트를 본다", "keep"), ("지우지 않는다", "keep")),
    ("kubernetes …", "클러스터 존에 권한", ("이 플러그인이 이 편의 주인공", "keep"), ("지우면 클러스터 DNS 가 아니다", "keep")),
    ("pods insecure", "kube-dns 하위 호환", ("폐기된 명세 부분을 켠다", "legacy"), ("파드 레코드가 필요 없으면", "drop")),
    ("upstream", "CNAME 되질의", ("1.4 이후 기본 동작", "legacy"), ("1.4 이상이면 지운다", "drop")),
    ("fallthrough …", "모르는 PTR 을 넘김", ("CIDR 을 다 못 적었을 때 안전장치", "keep"), ("CIDR 을 전부 열거했으면", "cond")),
    ("prometheus :9153", "메트릭을 연다", ("기본은 localhost 만 듣는다", "keep"), ("긁어 가지 않으면", "cond")),
    ("forward . …", "나머지를 상류로", ("앞선 플러그인이 안 잡은 질의", "keep"), ("외부 해석이 필요 없으면", "cond")),
    ("cache 30", "응답을 메모리에", ("클러스터 안에는 아낄 것이 없다", "waste"), ("클러스터 밖 질의가 없으면", "drop")),
    ("loop", "질의 루프 탐지", ("디버깅 불가능한 실패를 막는다", "keep"), ("지우지 않는다", "keep")),
    ("reload", "Corefile 재적재", ("30초마다 MD5 를 확인한다", "keep"), ("남기되 문법을 조심한다", "keep")),
    ("loadbalance", "A/AAAA 를 섞는다", ("첫 IP 만 쓰는 클라이언트를 위해", "keep"), ("헤드리스를 안 쓰면 이득이 적다", "cond")),
]

n_cols, n_rows = len(cols), len(lines)
W = LEFT_PAD + COMP_COL_W + COMP_ROLE_GAP + n_cols * ROLE_COL_W + (n_cols - 1) * ROLE_COL_GAP + RIGHT_PAD


def row_y(k):
    return 172 + k * ROW_STRIDE


def col_x(j):
    return LEFT_PAD + COMP_COL_W + COMP_ROLE_GAP + j * (ROLE_COL_W + ROLE_COL_GAP)


LEGEND_Y = row_y(n_rows - 1) + ROW_H + 20
H = LEGEND_Y + 44

d = D(W, H, "LEARNING COREDNS · 06-02 §4",
      "기본 Corefile 의 줄과 지울 수 있는 조건",
      "행이 기본 Corefile 의 지시어 열두 줄, 열이 그 줄을 판단하는 두 물음이다. "
      "지울 수 있는 줄과 지우면 안 되는 줄이 사연에 따라 갈린다.",
      "주황 줄이 저자들이 직접 고치겠다고 예고한 자리입니다")

d.box(LEFT_PAD, HEADER_Y, COMP_COL_W, HEADER_H, PAPER2, RULE, 0.8, 6)
d.t(LEFT_PAD + COMP_COL_W / 2, HEADER_Y + 24, "Corefile 의 줄", 12, INK, KR, "middle", 600)
d.t(LEFT_PAD + COMP_COL_W / 2, HEADER_Y + 42, "대 판단하는 물음", 12, MUTED)
for j, (nm, sub) in enumerate(cols):
    x = col_x(j)
    d.box(x, HEADER_Y, ROLE_COL_W, HEADER_H, PAPER2, RULE, 1.4, 6)
    d.t(x + ROLE_COL_W / 2, HEADER_Y + 22, nm, 13, INK, KR, "middle", 600)
    d.t(x + ROLE_COL_W / 2, HEADER_Y + 40, sub, 12, SOFT, KR)

STYLE = {"keep": (OK, "16"), "drop": (BAD, "16"), "cond": (WARN, "16"),
         "legacy": (MUTED, "14"), "waste": (ACC, "14")}

for k, (nm, hint, c1, c2) in enumerate(lines):
    y = row_y(k)
    focal = (nm == "cache 30")
    if focal:
        d.tone(LEFT_PAD, y, COMP_COL_W, ROW_H, ACC, 4, "12", 1.4)
    else:
        d.box(LEFT_PAD, y, COMP_COL_W, ROW_H, PAPER2, RULE, 0.8, 4)
    d.t(LEFT_PAD + 12, y + 23, nm, 12, ACC if focal else INK, MONO, "start", 600)
    d.t(LEFT_PAD + COMP_COL_W - 12, y + 23, hint, 12, MUTED, KR, "end")
    for j, (val, lvl) in enumerate((c1, c2)):
        x = col_x(j)
        col, op = STYLE[lvl]
        d.o.append(f'<rect x="{x}" y="{y}" width="{ROLE_COL_W}" height="{ROW_H}" rx="4" '
                   f'fill="{col}{op}" stroke="{RULE}" stroke-width="0.6"/>')
        d.t(x + ROLE_COL_W / 2, y + 23, val, 12, col, KR)

d.legend(LEGEND_Y, [("남긴다", OK), ("조건부", WARN), ("지운다", BAD), ("유산이라 켜 둔 것", MUTED), ("저자들이 고치는 줄", ACC)])
d.save("06-02.corefile-lines.svg")
