# 타입 스펙: type-swimlane — 행마다 한 방향, 레인을 건너는 화살표가 인계다. 막히는 인계에 강조색.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §6.3.4 Figure 6.14 —
#   CMTS 와 케이블 모뎀 사이 하향 채널 i · 상향 채널 j, 구간 [t1,t2] 의 미니슬롯 배치와 채널 폭·처리량 수치
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, KR, MONO

W, H = 940, 568
d = D(W, H, "SECTION 6.3.4 · DOCSIS",
      "케이블 망은 세 갈래를 한꺼번에 씁니다",
      "FDM 으로 채널을 가르고, 상향 채널을 TDM 처럼 미니슬롯으로 자르고, 그 중 요청용 슬롯만 랜덤 접속으로 남긴다.",
      "채널 폭과 처리량은 원문 §6.3.4 의 수치입니다")

LX, LW, RX = 24, 176, 760

d.box(LX, 128, LW, 60, PAPER2, RULE, 1.0)
d.t(LX + LW / 2, 152, "CMTS", 13, INK, MONO, "middle", 600)
d.t(LX + LW / 2, 172, "케이블 헤드엔드", 11, MUTED, KR)
d.box(RX, 128, 156, 60, PAPER2, RULE, 1.0)
d.t(RX + 78, 152, "케이블 모뎀", 13, INK, KR, "middle", 600)
d.t(RX + 78, 172, "수천 대", 11, MUTED, KR)

d.tone(LX, 212, W - 72, 76, INFO, 6, "0E", 1.0)
d.t(LX + 16, 236, "하향 채널 i", 11, INFO, KR, "start", 600)
d.t(LX + 16, 256, "24 ~ 192 MHz · 최대 약 1.6 Gbps", 11, MUTED, MONO, "start")
d.t(LX + 16, 276, "CMTS 하나만 보내므로 다중 접속 문제가 없습니다", 11, MUTED, KR, "start")
d.arrow([(500, 250), (RX - 8, 250)], INFO, "info", 1.6)
d.chip(626, 250, "MAP 메시지", INFO, 11)

d.tone(LX, 300, W - 72, 76, OK, 6, "0E", 1.0)
d.t(LX + 16, 324, "상향 채널 j", 11, OK, KR, "start", 600)
d.t(LX + 16, 344, "6.4 ~ 96 MHz · 최대 약 1 Gbps", 11, MUTED, MONO, "start")
d.t(LX + 16, 364, "여러 모뎀이 같은 주파수를 나눠 써서 충돌이 날 수 있습니다", 11, MUTED, KR, "start")
d.arrow([(RX - 8, 338), (500, 338)], OK, "ok", 1.6)
d.chip(626, 338, "데이터와 요청", OK, 11)

d.t(24, 410, "상향 구간 t1 부터 t2 까지는 이렇게 나뉩니다", 12, INK, KR, "start", 600)
MY, MH, REQ_W, ASG_W = 424, 44, 320, 560
d.tone(24, MY, REQ_W - 4, MH, ACC, 6, "1E", 1.5)
d.t(24 + (REQ_W - 4) / 2, MY + 20, "요청용 미니슬롯", 11, ACC, KR, "middle", 600)
d.t(24 + (REQ_W - 4) / 2, MY + 36, "랜덤 접속 · 충돌 가능", 10, ACC, KR)
d.tone(24 + REQ_W, MY, ASG_W, MH, OK, 6, "14", 1.1)
d.t(24 + REQ_W + ASG_W / 2, MY + 20, "배정된 미니슬롯 — 데이터 프레임", 11, OK, KR, "middle", 600)
d.t(24 + REQ_W + ASG_W / 2, MY + 36, "CMTS 가 명시적으로 허가해 충돌이 없습니다", 10, MUTED, KR)

d.line(24, 490, W - 48, 490, RULE, 0.8)
d.t(24, 510, "모뎀은 상향이 바쁜지도 충돌이 났는지도 감지하지 못합니다. 다음 하향 제어 메시지에 배정이 없으면 충돌로 추론해 백오프합니다.",
     11, MUTED, KR, "start")

d.legend(528, [("랜덤 접속이 남은 자리", ACC), ("하향", INFO), ("상향", OK)])

out = pathlib.Path(__file__).resolve().parent.parent / "06-02.docsis.svg"
d.save(out)
print("→", out)
