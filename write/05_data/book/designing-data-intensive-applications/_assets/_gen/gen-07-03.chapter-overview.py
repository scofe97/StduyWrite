# 07-03 개요 — 키 하나(Get "Danube")의 요청이 라우팅 정보를 갖는 곳(§1)을 거쳐 샤드를 가진 노드로 가는 길을 가운데 두고,
#   그 샤드→노드 매핑을 유지하는 조율 서비스(§2), 샤드 이전으로 매핑을 바꾸는 리밸런싱(§3), 샤드를 테넌트별로 나누는 멀티테넌시(§4)를 붙인 지도.
#   절 제목을 이은 사슬이 아니라, 요청 한 건 주위에 각 절이 어디에 걸리는지를 보인다.
# 사실 출처: 07-03 본문 서두 L16(특정 키 → 해당 샤드 노드), §1 L30·L32·L34(세 방식과 시스템), L36(샤드 이전 때 라우팅 정보 변경),
#   §2 L42·L48(ZooKeeper·etcd·내장 Raft, 합의, 구독), §3 L58·L60·L62(DynamoDB, 연쇄 과부하, 관리자 승인), §4 L66·L70~L76(테넌트별 샤드, 격리, 셀, GDPR)
# 원서 대목: Figure 7-8 (Ch.7 PDF p.21) — Get "Danube", Ceara—Deluc → shard 2 → node 2
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
R1 = 112          # 1행: 요청 경로
R2 = 316          # 2행: 매핑을 둘러싼 절
RH = 112
LEG = R2 + RH + 40
H = LEG + 56

d = D(W, H, "07-03 · CHAPTER OVERVIEW", "요청 라우팅과 리밸런싱 전체 지도",
      'Get "Danube" 요청이 라우팅 정보를 갖는 곳(§1)을 거쳐 node 2 로 가고, 그 샤드→노드 매핑은 조율 서비스(§2)가 유지하며, '
      '리밸런싱(§3)의 샤드 이전이 매핑을 바꾸고, 멀티테넌시(§4)는 샤드를 테넌트별로 나눈다.',
      '키 하나의 요청 경로 · 라우팅 정보의 위치 · 매핑 조율 · 샤드 이전 · 테넌트별 샤드')

C1, C2, C3 = 24, 284, 656
W1, W2, W3 = 200, 312, 200

# ── 1행: 클라이언트 → §1 라우팅 정보를 갖는 곳 → 샤드를 가진 노드 ──────────────
cy1 = R1 + 74
d.box(C1, cy1 - 36, W1, 72, PAPER, RULE, 0.9)
d.t(C1 + W1 / 2, cy1 - 8, "클라이언트", 13, INK, KR, "middle", 600)
d.t(C1 + W1 / 2, cy1 + 16, 'Get "Danube"', 11.5, MUTED, MONO, "middle")

d.tone(C2, R1, W2, 150, INFO, 6, "14", 1.2)
d.chip(C2 + 26, R1 + 22, "§1", INFO, 11)
d.t(C2 + W2 / 2 + 10, R1 + 27, "라우팅 정보를 갖는 곳", 13, INK, KR, "middle", 600)
for j, txt in enumerate(["임의 노드 · Cassandra · Riak",
                         "라우팅 티어 · MongoDB mongos",
                         "클라이언트 · Cassandra 드라이버"]):
    ry = R1 + 46 + j * 32
    d.box(C2 + 16, ry, W2 - 32, 26, PAPER, RULE, 0.8, 4)
    d.t(C2 + W2 / 2, ry + 17, txt, 11.5, INK, KR, "middle")

d.box(C3, cy1 - 36, W3, 72, PAPER, RULE, 0.9)
d.t(C3 + W3 / 2, cy1 - 8, "node 2 · shard 2", 13, INK, MONO, "middle", 600)
d.t(C3 + W3 / 2, cy1 + 16, "Ceara — Deluc", 11.5, MUTED, MONO, "middle")

d.arrow([(C1 + W1, cy1), (C2 - 2, cy1)], MUTED, "ar")
d.t((C1 + W1 + C2) / 2, cy1 - 8, "요청", 11.5, MUTED, KR, "middle")
d.arrow([(C2 + W2, cy1), (C3 - 2, cy1)], MUTED, "ar")
d.t((C2 + W2 + C3) / 2, cy1 - 8, "전달", 11.5, MUTED, KR, "middle")

# ── 2행: §3 리밸런싱 → §2 매핑 조율 → (§1 구독) / §4 테넌트별 샤드 ──────────────
# §2 (focal)
d.tone(C2, R2, W2, RH, ACC, 6, "18", 1.4)
d.chip(C2 + 26, R2 + 22, "§2", ACC, 11)
d.t(C2 + W2 / 2 + 10, R2 + 27, "샤드→노드 매핑 조율", 13, INK, KR, "middle", 600)
d.t(C2 + W2 / 2, R2 + 58, "ZooKeeper · etcd · 내장 Raft", 11.5, ACC, KR, "middle")
d.t(C2 + W2 / 2, R2 + 84, "합의로 권위 매핑 유지 · split-brain 방지", 11.5, MUTED, KR, "middle")
d.arrow([(C2 + W2 / 2, R2), (C2 + W2 / 2, R1 + 152)], ACC, "acc")
d.t(C2 + W2 / 2 + 8, (R1 + 150 + R2) / 2 + 4, "매핑 구독", 11.5, ACC, KR, "start")

# §3
d.tone(C1, R2, W1, RH, WARN, 6, "14", 1.2)
d.chip(C1 + 26, R2 + 22, "§3", WARN, 11)
d.t(C1 + W1 / 2 + 12, R2 + 27, "리밸런싱", 13, INK, KR, "middle", 600)
for j, txt in enumerate(["자동 · DynamoDB", "수동 · 관리자 승인", "위험 · 연쇄 과부하"]):
    d.t(C1 + W1 / 2, R2 + 54 + j * 21, txt, 11.5, MUTED, KR, "middle")
cy2 = R2 + RH / 2
d.arrow([(C1 + W1, cy2), (C2 - 2, cy2)], WARN, "warn")
d.t((C1 + W1 + C2) / 2, cy2 - 8, "샤드 이전", 11.5, WARN, KR, "middle")

# §4
d.tone(C3, R2, W3, RH, OK, 6, "14", 1.2)
d.chip(C3 + 26, R2 + 22, "§4", OK, 11)
d.t(C3 + W3 / 2 + 12, R2 + 27, "멀티테넌시", 13, INK, KR, "middle", 600)
for j, txt in enumerate(["테넌트별 샤드 분리", "리소스·권한 격리 · 셀", "GDPR 삭제 · 데이터 레지던시"]):
    d.t(C3 + W3 / 2, R2 + 54 + j * 21, txt, 11.5, MUTED, KR, "middle")
d.line(C3 + W3 / 2, cy1 + 36, C3 + W3 / 2, R2, OK, 1.2, "4 4")
d.t(C3 + W3 / 2 - 8, (cy1 + 36 + R2) / 2 + 4, "테넌트별로 분리", 11.5, OK, KR, "end")

d.legend(LEG, [("라우팅 경로", INFO), ("매핑 조율", ACC), ("리밸런싱", WARN), ("테넌트별 샤드", OK)])
d.save("07-03.chapter-overview.svg")
