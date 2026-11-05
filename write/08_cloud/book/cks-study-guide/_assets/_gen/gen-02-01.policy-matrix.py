# 02-01 §1 — NetworkPolicy 를 쌓을 때마다 backend Pod 로 들어오는 길이 달라진다.
# 본문 근거: 이 노트 §1 「정책을 하나씩 얹으면 열린 길이 줄고, 필요한 길만 다시 열립니다」.
# 책 쪽: "The frontend Pod can talk to the backend Pod as no communication restrictions have been put in place" /
#        "The other Pod residing in the default namespace can communicate with the backend Pod without problems" /
#        "Pods running in a different namespace cannot connect to the backend Pod anymore either" /
#        "The frontend Pod can now talk to the backend Pod ... Pods running outside of the g04 namespace still can't connect".
#        Example 2-1(g04 의 backend·frontend, default 의 other) · Example 2-2(default-deny-ingress) · Example 2-3(backend-ingress).
# 타입 스펙: type-dp-security-matrix — "어느 조합이 되고 안 되는가" 를 행(호출 경로) × 열(정책 단계) 격자로 비교한다.
# 축약: 스펙의 10~11px 라벨은 스타일 계약의 한글 12px 이상 규칙에 맞춰 키웠다. 행 높이를 56 으로 늘려 두 줄 라벨이 들어간다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, OK, BAD, KR, MONO

LEFT, COMP_W, GAP = 12, 224, 16
ROLE_W, ROLE_GAP = 200, 16
HEAD_Y, HEAD_H = 100, 60
ROW_Y0, ROW_H, STRIDE = 176, 56, 68
cols = [
    ("정책 없음", "NetworkPolicy 0개"),
    ("default-deny-ingress", "podSelector {} · Ingress"),
    ("+ backend-ingress", "tier=backend 에 frontend 만"),
]
rows = [
    ("frontend → backend", "g04 → g04 · TCP 3000"),
    ("other → backend", "default → g04 · TCP 3000"),
]
# (행, 열) → (결과, 소제목, 초점 여부)
cells = {
    (0, 0): ("허용", "wget 응답", False),
    (0, 1): ("차단", "wget 시간 초과", False),
    (0, 2): ("허용", "tier=frontend 만 통과", True),
    (1, 0): ("허용", "wget 응답", False),
    (1, 1): ("차단", "wget 시간 초과", False),
    (1, 2): ("차단", "wget 시간 초과", False),
}

n_roles = len(cols)
W = LEFT + COMP_W + GAP + n_roles * ROLE_W + (n_roles - 1) * ROLE_GAP + 48
rows_bottom = ROW_Y0 + (len(rows) - 1) * STRIDE + ROW_H
LEG_Y = rows_bottom + 28
H = LEG_Y + 44

d = D(W, H, "CKS STUDY GUIDE · 02-01 §1",
      "정책 단계별 backend 접근 가능 여부",
      "g04 네임스페이스의 backend Pod 로 향하는 TCP 3000 호출이 정책 없음, default-deny-ingress, "
      "default-deny-ingress 에 backend-ingress 를 더한 세 단계에서 허용되는지 차단되는지 비교한 행렬이다.",
      "정책을 얹을수록 열린 길이 줄고, frontend 한 곳만 다시 열립니다")


def col_x(j):
    return LEFT + COMP_W + GAP + j * (ROLE_W + ROLE_GAP)


# 헤더
d.box(LEFT, HEAD_Y, COMP_W, HEAD_H, PAPER2, RULE, 0.9)
d.t(LEFT + 16, HEAD_Y + 26, "호출 경로", 14, INK, KR, "start", 600)
d.t(LEFT + 16, HEAD_Y + 46, "출발 Pod → 대상 Pod", 12, MUTED, KR, "start")
for j, (name, sub) in enumerate(cols):
    x = col_x(j)
    d.box(x, HEAD_Y, ROLE_W, HEAD_H, PAPER2, RULE, 0.9)
    d.t(x + ROLE_W / 2, HEAD_Y + 26, name, 13, INK, MONO, "middle", 600)
    d.t(x + ROLE_W / 2, HEAD_Y + 46, sub, 12, MUTED, KR)

# 행
for i, (name, sub) in enumerate(rows):
    y = ROW_Y0 + i * STRIDE
    d.box(LEFT, y, COMP_W, ROW_H, PAPER2, RULE, 0.9)
    d.t(LEFT + 16, y + 24, name, 14, INK, MONO, "start", 600)
    d.t(LEFT + 16, y + 44, sub, 12, MUTED, KR, "start")
    for j in range(n_roles):
        x = col_x(j)
        verdict, note, focal = cells[(i, j)]
        c = ACC if focal else (OK if verdict == "허용" else BAD)
        d.tone(x, y, ROLE_W, ROW_H, c, 6, "1A" if not focal else "26", 1.4 if focal else 1.0)
        d.t(x + ROLE_W / 2, y + 24, verdict, 15, c, KR, "middle", 600)
        d.t(x + ROLE_W / 2, y + 44, note, 12, MUTED, KR)

d.legend(LEG_Y, [("허용", OK), ("차단", BAD), ("정책이 다시 연 길", ACC)])
d.save("02-01.policy-matrix.svg")
