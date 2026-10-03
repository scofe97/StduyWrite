# 05-01 학습 목표 뒤 전체 지도 — 주소가 바뀔 때 누가 고치고 클라이언트는 언제 아는가를 방식별로 놓는다.
# 원문 근거: 2절의 다섯 칸(인자·hosts·DNS·SRV·레지스트리), 3절 "They must still rely on a TTL",
#            4~6절 etcd 플러그인(기본 TTL 300 · 리스 하한 30초), 7절 hosts(5초마다 확인)·pdsql·오케스트레이터.
# 타입 스펙: type-dp-security-matrix — 방식(행) × 갱신 주체·클라이언트 인지 시점(열) 격자가 논지다.
#           2026-10-03 절 제목을 이은 노드 사슬에서 실제 값이 든 격자로 다시 그렸다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 640
d = D(W, H, "LEARNING COREDNS · 05-01",
      "주소가 바뀌면 누가 고치고, 클라이언트는 언제 아는가",
      "방식마다 주소를 고치는 주체와 클라이언트가 변경을 알게 되는 시점을 나란히 놓았다. "
      "레지스트리와 etcd 는 고치는 쪽을 즉시로 바꾸지만, 일반 질의 경로의 클라이언트는 여전히 TTL 을 기다린다.",
      "주황 행이 이 장이 세우는 답입니다")

COLS = [(20, 200, "방식"), (230, 230, "주소가 바뀌면 누가 고치나"),
        (470, 280, "클라이언트가 아는 때"), (760, 100, "절")]
rows = [
    (("명령줄 인자", ""), ("의존 서비스 재설정", "전부 다시 띄운다"), ("재기동한 뒤", ""), "§2"),
    (("hosts 파일 배포", ""), ("모든 클라이언트 파일", "같은 호스트에서만"), ("파일이 바뀐 뒤", "경합 조건으로 실패"), "§2"),
    (("존 파일 DNS", ""), ("사람이 존 파일 수정", "시리얼 · 보조 서버 전송"), ("TTL 만료 뒤", "분~시간 단위"), "§2 · §3"),
    (("전용 레지스트리", "Consul 류"), ("서비스가 API 로 등록", "즉시"), ("TTL 만료 뒤", "별도 푸시면 더 빨리"), "§3"),
    (("CoreDNS + etcd", ""), ("서비스가 etcd 에 기록", "또는 오케스트레이터"), ("TTL 만료 뒤", "기본 300초 · 리스 하한 30초"), "§4~§6"),
    (("다른 저장소", "hosts · pdsql · 오케스트레이터"), ("파일 · DB · 오케스트레이터", "hosts 는 5초마다 확인"), ("TTL 만료 뒤", ""), "§7"),
]
FOCAL = 4
Y0, PITCH, RH = 132, 64, 56

for x, w, head in COLS:
    d.t(x + 12, 118, head, 12, SOFT, KR, "start", 600)

for i, cells in enumerate(rows):
    y = Y0 + i * PITCH
    if i == FOCAL:
        d.tone(16, y - 2, 848, RH + 4, ACC, 8, "12", 1.4)
    for k, (x, w, _) in enumerate(COLS):
        if i != FOCAL:
            d.box(x, y, w, RH, PAPER2, RULE, 1.0, 6)
        cell = cells[k]
        if k == 3:
            d.t(x + w / 2, y + 34, cell, 13, ACC if i == FOCAL else MUTED, KR)
            continue
        main, sub = cell
        if sub:
            d.t(x + 12, y + 24, main, 14, ACC if (i == FOCAL and k == 0) else INK, KR, "start", 600)
            d.t(x + 12, y + 44, sub, 12, MUTED, KR, "start")
        else:
            d.t(x + 12, y + 34, main, 14, ACC if (i == FOCAL and k == 0) else INK, KR, "start", 600)

d.t(20, 544, "1~3절 · 손으로 고치는 길이 왜 막히는가 · 4~6절 · CoreDNS 의 답", 13, MUTED, KR, "start")
d.t(20, 568, "7절 · etcd 밖의 대안 · 어느 길이든 일반 질의는 TTL 을 기다린다", 13, MUTED, KR, "start")

d.legend(592, [("이 장의 답", ACC)])
d.save("05-01.chapter-overview.svg")
