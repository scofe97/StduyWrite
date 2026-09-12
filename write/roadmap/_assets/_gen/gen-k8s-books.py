# 타입 스펙: type-tree
import sys

sys.path.insert(0, ".")

from dd import ACC, INFO, INK, KR, MONO, MUTED, PAPER, PAPER2, RULE, SOFT, D

rows = [
    ("1–4", "오브젝트·저장", [("Kubernetes in Action", "1~4단계 · 기초부터 저장까지", ["Pod·controller·Service", "probe·config·volume"])]),
    ("5–6", "구조·확장", [("Kubernetes: Up and Running", "5~6단계 · 구조와 확장", ["cluster·API", "CRD·controller"])]),
    ("6", "패턴", [("Kubernetes Patterns", "6단계 · 패턴별 선택", ["reconciliation·operator", "configuration·security"])]),
    ("6–7", "보안·운영", [("Container Security", "6~7단계 · 실행 경계", ["capability·seccomp", "image·runtime·host"])]),
]

W, TOP, ROW_H = 1000, 160, 132
H = TOP + len(rows) * ROW_H + 68
d = D(W, H, "WRITE · KUBERNETES BOOK FLOW", "Kubernetes 책 읽기 흐름", "오브젝트와 저장을 익힌 뒤 구조, 확장, 보안으로 이어지는 책의 범위를 배치했습니다.", "위에서 아래로 진행하며 단계 표의 오브젝트를 직접 확인합니다")
d.line(126, TOP + 38, 126, TOP + (len(rows) - 1) * ROW_H + 38, RULE, 1.4)
for i, (number, phase, cards) in enumerate(rows):
    y = TOP + i * ROW_H
    d.box(30, y, 192, 76, PAPER2, RULE, 1.0)
    d.t(48, y + 25, number, 12, INFO, MONO, "start", 600)
    d.t(126, y + 51, phase, 15, INK, KR, "middle", 600)
    for j, (title, timing, topics) in enumerate(cards):
        x = 258 + j * 362
        d.line(222 if j == 0 else x - 28, y + 38, x, y + 38, RULE, 1.0)
        d.box(x, y - 8, 520, 96, PAPER, ACC if i == 0 else INFO, 1.2)
        d.t(x + 16, y + 16, title, 14, INK, KR, "start", 600)
        d.t(x + 16, y + 39, timing, 13, SOFT, KR, "start")
        d.t(x + 16, y + 62, topics[0], 13, MUTED, KR, "start")
        d.t(x + 16, y + 81, topics[1], 13, MUTED, KR, "start")
d.legend(H - 44, [("첫 진입", ACC), ("단계별 독서", INFO)])
d.save("k8s-books.svg")
