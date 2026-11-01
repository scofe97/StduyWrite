# 06-02 §4 — 기본 Corefile 의 각 줄이 무엇을 켜고, 왜 있고, 언제 지울 수 있는가.
# 본문 근거: 이 노트 §4(L143-L232), 결정 치트시트(L310-L330).
# 원서 근거: 원서 6장 p.18 Example 6-11(Kubernetes Corefile) 및 p.19-21 줄별 해설.
#            pods insecure(p.19), upstream(p.19-20), fallthrough(p.20), cache(p.20), loop(p.20-21), reload(p.21), loadbalance(p.21).
# 현행 근거: 1.7.0 릴리스 노트(upstream 제거), CoreDNS README(reload SHA512, loadbalance MX, cache 5초 하한).
# 타입 스펙: type-dp-security-matrix — 행×열 격자에서 어느 조합이 되고 안 되는가가 논지다.
#           좌표는 스펙 §2 Layout formulas 를 쓰되 이 저장소 D() 머리글만큼 32 내린다. 색은 다크 스킨 계약.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, OK, BAD, WARN, KR, MONO

LEFT_PAD, RIGHT_PAD = 20, 28
COMP_COL_W, COMP_ROLE_GAP = 276, 16
ROLE_COL_W, ROLE_COL_GAP = 264, 12
HEADER_H, ROW_H, ROW_STRIDE = 52, 36, 40
HEADER_Y = 104

cols = [("왜 거기 있나", "줄의 사연"), ("지울 수 있는 조건", "없으면 무엇이 깨지나")]
lines = [
    ("errors", "오류를 로그로", ("없으면 흔적 없음", "keep"), ("유지 · 추적 필수", "keep")),
    ("health", "kubelet 감시용", ("/health 프로브", "keep"), ("유지 · 프로브용", "keep")),
    ("kubernetes …", "클러스터 존에 권한", ("Service·Endpoints 로 응답", "keep"), ("유지 · 본체", "keep")),
    ("pods insecure", "kube-dns 하위 호환", ("폐기된 파드 IP 명세", "legacy"), ("파드 조회 안 쓸 때", "drop")),
    ("upstream", "CNAME 되질의", ("1.7.0 에서 제거", "legacy"), ("반드시 제거 · 기동 오류", "drop")),
    ("fallthrough …", "모르는 PTR 을 넘김", ("CIDR 누락 대비 안전장치", "keep"), ("CIDR 전부 적을 때", "cond")),
    ("prometheus :9153", "메트릭 노출", (":9153 이면 모든 주소", "keep"), ("메트릭 안 볼 때", "cond")),
    ("forward . …", "나머지를 상류로", ("처리 못 한 질의 전달", "keep"), ("외부 이름 안 쓸 때 (추론)", "cond")),
    ("cache 30", "응답을 메모리에", ("클러스터 내부 질의 이득 미미", "waste"), ("클러스터 안 질의만 다룰 때", "drop")),
    ("loop", "질의 루프 탐지", ("간헐 실패 방지", "keep"), ("유지 · 루프 방어", "keep")),
    ("reload", "Corefile 재적재", ("원서 MD5 · 현행 SHA512", "keep"), ("유지 · 문법 오류 주의", "keep")),
    ("loadbalance", "A·AAAA 섞음", ("첫 IP 편중 방지", "keep"), ("헤드리스 없으면 이득 적음 (추론)", "cond")),
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
d.t(LEFT_PAD + COMP_COL_W / 2, HEADER_Y + 42, "행마다 지시어 하나", 12, MUTED)
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

d.legend(LEGEND_Y, [("유지", OK), ("조건부", WARN), ("제거", BAD), ("하위 호환", MUTED), ("개선 대상", ACC)])
d.save("06-02.corefile-lines.svg")
