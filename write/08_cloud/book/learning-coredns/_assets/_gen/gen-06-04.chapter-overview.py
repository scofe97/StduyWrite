# 06-04 학습 목표 뒤 전체 지도 — 명세 밖 기능마다 얻는 것·내주는 대가·지금 상태를 한 격자에 놓는다.
# 본문 근거: 이 노트 결정 치트시트와 §2~§7 본문. 1.9.0 와일드카드 제거·1.8.0 transfer 플러그인은 릴리스 노트로 확인.
# 타입 스펙: type-dp-security-matrix — 기능(행) × 얻는 것·대가·지금(열) 격자가 논지다.
#           2026-10-03 절 제목을 이은 노드 사슬(focal 둘)에서 실제 값이 든 격자(focal 하나)로 다시 그렸다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 620
d = D(W, H, "LEARNING COREDNS · 06-04",
      "명세 밖 기능은 무엇을 주고 무엇을 받아 가는가",
      "kubernetes 플러그인의 명세 밖 기능을 행으로 놓고 얻는 것, 그 대가, 지금 상태를 견준다. "
      "대가는 이식성이거나 메모리·API 서버 부하이거나 둘 다이다.",
      "주황 행이 4절과 5절을 잇는 거래입니다")

COLS = [(20, 170, "명세 밖 기능"), (200, 180, "얻는 것"), (390, 210, "내주는 대가"),
        (610, 150, "지금"), (770, 90, "절")]
rows = [
    ("pods verified", "파드 신원 확인", "메모리 2배 안팎 · API 부하", "기본은 disabled", "§2"),
    ("와일드카드 질의", "ClusterIP 엔드포인트", "명세 밖 · 이름 불일치", "1.9.0 제거", "§3"),
    ("ndots:5 검색 경로", "짧은 이름", "외부 이름 질의 여섯 번", "kubelet 기본", "§4"),
    ("autopath", "질의 여섯 번을 한 번으로", "pods verified 메모리", "쓸 수 있음", "§5"),
    ("존 전송", "레코드를 한 번에 조망", "IXFR 없음 · BIND 비호환", "transfer 플러그인", "§6"),
    ("k8s_external", "외부 IP 를 이름으로", "클러스터 DNS 를 바깥에 노출", "쓸 수 있음", "§6"),
    ("레코드 좁히기", "테넌트 격리 · 클러스터 넘김", "명세에서 가장 멀다", "namespace_labels 추가", "§7"),
]
FOCAL = 3
Y0, PITCH, RH = 132, 54, 46

for x, w, head in COLS:
    d.t(x + 12, 118, head, 12, SOFT, KR, "start", 600)

for i, cells in enumerate(rows):
    y = Y0 + i * PITCH
    if i == FOCAL:
        d.tone(16, y - 2, 848, RH + 4, ACC, 8, "12", 1.4)
    for k, (x, w, _) in enumerate(COLS):
        if i != FOCAL:
            d.box(x, y, w, RH, PAPER2, RULE, 1.0, 6)
        txt = cells[k]
        if k == 4:
            d.t(x + w / 2, y + 28, txt, 13, ACC if i == FOCAL else MUTED, KR)
        elif k == 0:
            d.t(x + 12, y + 28, txt, 13, ACC if i == FOCAL else INK, KR, "start", 600)
        else:
            d.t(x + 12, y + 28, txt, 13, INK if k == 1 else MUTED, KR, "start")

d.t(20, 536, "§1 · 원서 문법 열넷 가운데 셋은 원서 이후 제거 · 1.6.0 · 1.7.0 · 1.8.0", 13, MUTED, KR, "start")
d.t(20, 560, "대가 · 이식성 · 메모리와 API 서버 · 또는 둘 다", 13, MUTED, KR, "start")

d.legend(578, [("한 이야기로 이어지는 거래", ACC)])
d.save("06-04.chapter-overview.svg")
