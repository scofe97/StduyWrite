# 06-04 §7 「NXDOMAIN 을 신호로 쓰기」 — ignore empty_service 가 어느 서비스의 응답을 어떻게 바꾸고, 클라이언트가 다음에 무엇을 하는가.
# 소스 근거(kubernetes.go master, 2026-10-03 대조): "If "ignore empty_service" option is set and no endpoints exist, return
#            NXDOMAIN unless it's a headless or externalName service" — ready 주소(Subsets[].Addresses)를 세고, 옵션이 없으면
#            ClusterIP 서비스는 svc.ClusterIPs 로 바로 레코드를 만든다. README: "services without any ready endpoint addresses".
# 타입 스펙: type-dp-security-matrix — 서비스 종류·상태(행) × 응답·클라이언트 동작(열) 격자에서 바뀌는 칸 하나가 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, BAD, KR, MONO

W, H = 880, 490
d = D(W, H, "LEARNING COREDNS · 06-04 §7",
      "바뀌는 칸은 ready 가 없는 ClusterIP 하나다",
      "ignore empty_service 는 헤드리스도 ExternalName 도 아닌 ClusterIP 서비스에만 걸린다. ready 엔드포인트가 없을 때 "
      "VIP 를 담은 성공 응답 대신 NXDOMAIN 을 내서, 클라이언트가 검색 경로의 다음 항목으로 넘어가게 한다.",
      "주황 칸이 옵션이 바꾸는 유일한 응답입니다")

COLS = [(20, 200, "서비스"), (230, 190, "기본 응답"), (430, 200, "ignore empty_service"), (640, 220, "클라이언트의 다음 걸음")]
rows = [
    (("ClusterIP", "ready 있음"), ("VIP 의 A", ""), ("VIP 의 A", "같음"), ("VIP 로 접속", "")),
    (("ClusterIP", "ready 없음"), ("VIP 의 A", "성공 응답"), ("NXDOMAIN", "이름이 없는 것처럼"), ("다음 검색 도메인", "보조 클러스터로 넘김")),
    (("헤드리스", "ready 없음"), ("헤드리스 규칙대로", ""), ("같음", "옵션 밖"), ("—", "")),
    (("ExternalName", ""), ("CNAME", ""), ("같음", "옵션 밖"), ("—", "")),
]
FOC = (1, 2)
Y0, PITCH, RH = 132, 70, 60

for x, w, head in COLS:
    d.t(x + 12, 118, head, 12, SOFT, KR if x != 430 else MONO, "start", 600)

for i, cells in enumerate(rows):
    y = Y0 + i * PITCH
    for k, (x, w, _) in enumerate(COLS):
        main, sub = cells[k]
        focal = (i, k) == FOC
        if focal:
            d.tone(x, y, w, RH, ACC, 6, "12", 1.4)
        else:
            d.box(x, y, w, RH, PAPER2, RULE, 1.0, 6)
        fam = MONO if main in ("ClusterIP", "ExternalName", "NXDOMAIN", "CNAME") else KR
        col = ACC if focal else (SOFT if main == "—" else INK)
        if i == 1 and k == 1:
            col = BAD
        if sub:
            d.t(x + 12, y + 26, main, 13, col, fam, "start", 600)
            d.t(x + 12, y + 46, sub, 12, MUTED, KR, "start")
        else:
            d.t(x + 12, y + 36, main, 13, col, fam, "start", 600)

d.t(20, 430, "기본 응답의 함정 · 백엔드가 없어도 VIP 가 오니 접속 단계에서야 실패를 안다", 13, MUTED, KR, "start")

d.legend(444, [("옵션이 바꾸는 칸", ACC), ("백엔드 없는 성공 응답", BAD)])
d.save("06-04.empty-service.svg")
