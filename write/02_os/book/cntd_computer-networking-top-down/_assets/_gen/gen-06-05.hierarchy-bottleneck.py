# 타입 스펙: type-deployment — 소프트웨어와 트래픽이 *어디서 도는가*. 존·랙·스위치라는 실제 배치에 링크 속도를 얹는다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §6.6.1 Figure 6.31 과 그 뒤의 병목 계산 —
#   호스트-TOR 10 Gbps, 스위치 간 100 Gbps, 랙 쌍 넷에서 40 흐름 → 흐름당 2.5 Gbps
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, BAD, KR, MONO

W, H = 1000, 578
d = D(W, H, "SECTION 6.6.1 · HIERARCHY AND ITS LIMIT",
      "계층은 규모를 풀고 호스트 간 용량을 막습니다",
      "경계 라우터에서 TOR 까지 세 티어로 내려가면 수십만 호스트까지 늘릴 수 있다. 대신 랙을 건너는 흐름이 위층 링크에서 서로를 깎아 먹는다.",
      "링크 속도와 흐름 수는 원문 §6.6.1 의 예 그대로입니다")

TIERS = [
    (116, "경계 라우터", "공개 인터넷과 잇습니다", INFO, "하나 이상"),
    (176, "접근 라우터", "이 아래 호스트가 하나의 서브넷", INFO, "원문 그림엔 둘"),
    (236, "티어 1 스위치", "부하 분산기가 여기 붙습니다", MUTED, "접근 라우터마다"),
    (296, "티어 2 스위치", "여러 랙을 묶습니다", MUTED, "티어 1 마다 여럿"),
    (356, "TOR — 티어 3", "랙 안 호스트를 묶습니다", OK, "예에서는 랙 여덟"),
]
LX, LW = 24, 300
for y, name, note, c, count in TIERS:
    d.tone(LX, y, LW, 48, c, 6, "14", 1.1)
    d.t(LX + 16, y + 22, name, 12, c, KR, "start", 600)
    d.t(LX + 16, y + 40, note, 10, MUTED, KR, "start")
    d.t(LX + LW - 16, y + 30, count, 10, MUTED, KR, "end")
for y in (164, 224, 284, 344):
    d.line(174, y, 174, y + 12, RULE, 1.1)

d.t(LX, 428, "모든 링크가 이더넷이고 구리와 광이 섞입니다.", 11, MUTED, KR, "start")
d.t(LX, 448, "ARP 브로드캐스트를 가두려고 서브넷을 다시", 11, MUTED, KR, "start")
d.t(LX, 468, "수백 호스트짜리 VLAN 서브넷으로 나눕니다.", 11, MUTED, KR, "start")

BX, BW = 372, 288
d.box(BX, 116, BW, 172, PAPER2, RULE, 1.0)
d.t(BX + 16, 140, "링크 속도", 11, INK, KR, "start", 600)
d.line(BX + 16, 150, BX + BW - 16, 150, RULE, 0.8)
d.t(BX + 16, 174, "호스트 ↔ TOR", 11, MUTED, KR, "start")
d.t(BX + BW - 16, 174, "10 Gbps", 11, OK, MONO, "end", 600)
d.t(BX + 16, 198, "스위치 ↔ 스위치", 11, MUTED, KR, "start")
d.t(BX + BW - 16, 198, "100 Gbps", 11, INFO, MONO, "end", 600)
d.t(BX + 16, 228, "같은 랙 안 두 호스트는", 11, MUTED, KR, "start")
d.t(BX + 16, 248, "언제나 10 Gbps 를 다 씁니다.", 11, INK, KR, "start", 600)
d.t(BX + 16, 270, "NIC 속도만이 상한입니다.", 11, MUTED, KR, "start")

d.tone(BX, 304, BW, 184, BAD, 7, "14", 1.4)
d.t(BX + 16, 328, "랙을 건너면 이야기가 달라집니다", 11, BAD, KR, "start", 600)
d.line(BX + 16, 338, BX + BW - 16, 338, RULE, 0.8)
for i, s in enumerate(["랙 1 의 호스트 10 대가 랙 5 로 보냅니다",
                       "랙 2·3·4 도 각각 랙 6·7·8 로 보냅니다",
                       "흐름 40 개가 같은 링크를 지납니다"]):
    d.t(BX + 16, 362 + i * 22, "·  " + s, 11, MUTED, KR, "start")
d.t(BX + BW / 2, 448, "100 Gbps ÷ 40 = 2.5 Gbps", 14, BAD, MONO, "middle", 600)
d.t(BX + BW / 2, 470, "NIC 속도 10 Gbps 의 4 분의 1 입니다", 11, MUTED, KR)

CX, CW = 688, 288
d.box(CX, 116, CW, 372, PAPER2, f"{ACC}44", 1.2, 7)
d.t(CX + 16, 140, "부하 분산기가 하는 두 가지", 11, ACC, KR, "start", 600)
d.line(CX + 16, 150, CX + CW - 16, 150, RULE, 0.8)
for i, s in enumerate(["애플리케이션마다 공개 IP 주소를 하나 둡니다",
                       "요청을 호스트들의 현재 부하에 맞춰 나눕니다",
                       "목적지 포트 번호로도 판단해 4 계층 스위치라",
                       "불리기도 합니다",
                       "NAT 처럼 공개·내부 주소를 바꿉니다",
                       "그래서 클라이언트가 호스트에 직접 못 닿고",
                       "내부 망 구조가 감춰집니다"]):
    d.t(CX + 16, 174 + i * 20, s if i in (3, 6) else "·  " + s, 11, MUTED, KR, "start")
d.line(CX + 16, 328, CX + CW - 16, 328, RULE, 0.8)
d.t(CX + 16, 352, "높은 가용성을 위해", 11, INK, KR, "start", 600)
for i, s in enumerate(["장비와 링크를 이중으로 둡니다",
                       "TOR 하나가 티어 2 스위치 둘에 붙고",
                       "접근 라우터와 티어 1·2 도 복제합니다"]):
    d.t(CX + 16, 376 + i * 20, "·  " + s, 11, MUTED, KR, "start")

d.line(24, 500, W - 48, 500, RULE, 0.8)
d.t(24, 520, "더 위층으로 올라가는 흐름일수록 이 문제가 심해집니다. 다음 절의 해법 셋이 여기서 나옵니다.",
     11, MUTED, KR, "start")

d.legend(538, [("부하 분산기", ACC), ("라우터 계층", INFO), ("랙에 닿는 층", OK), ("병목", BAD)])

out = pathlib.Path(__file__).resolve().parent.parent / "06-05.hierarchy-bottleneck.svg"
d.save(out)
print("→", out)
