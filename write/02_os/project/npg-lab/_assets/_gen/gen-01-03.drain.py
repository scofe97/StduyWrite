# 01-03-drain — 배포 종료 신호 t=0 기준 드레인 20초와 종료 코드 분기 시간축
# 본문 요구: 종료 신호 시각 0 에서 시작: 새 연결 거절, 가장 긴 요청(업스트림 기한 15초)이 끝나는 자리, 드레인 기한 20초, 그 뒤 Shutdown 이 ctx.Err() 를 돌려주면 exit 1 / 제때 끝나면 exit 0. 프록시가 하나라 꺼진 2초의 refused 를 회색으로. 값은 리허설 J4·ADR 0014 의 값만.
# 타입 스펙: type-timeline
# 사실 출처: 01-03.리버스 프록시 다운스트림 층 — 틈 시계·최소 속도·드레인.md:83-91, ADR 0014:15,63,71-73, ch09-deploy-drain-cut.md:20,36-43,50-52, Go server.go L3159-3178
import sys
from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent.parent
GEN_DIR = Path(__file__).resolve().parent
if str(ASSETS_DIR) not in sys.path:
    sys.path.insert(0, str(ASSETS_DIR))
if str(GEN_DIR) not in sys.path:
    sys.path.insert(0, str(GEN_DIR))

from dd import D, INK, MUTED, SOFT, RULE, PAPER, PAPER2, ACC, OK, WARN, BAD, INFO, KR, MONO

W = 960
H = 568

d = D(
    W,
    H,
    "TIMELINE · DEPLOYMENT DRAIN & EXIT CODE",
    "배포 드레인 20초와 종료 코드 분기 시간축",
    "종료 신호 t=0 에서 새 연결을 거절하고, 업스트림 최장 기한 15초보다 긴 20초 드레인 기한 동안 요청을 마친 뒤 제때 끝나면 exit 0, 기한 초과 시 exit 1 로 알리는 시간축",
    lead="드레인은 가장 긴 요청(업스트림 15초)보다 길어야 하며, Shutdown 기한 초과 시 exit 1 로 배포 도구에 실패를 알립니다.",
)

# 1. 상단 구간 막대 (y = 116 ~ 228)
# 전체 드레인 허용 구간 20s (t=0..20s, x: 80..600)
d.box(80, 116, 520, 32, fill=PAPER2, stroke=INFO, sw=1.2, r=4)
d.t(340, 137, "드레인 허용 구간 20s (Server.Shutdown)", 13, INK, KR, "middle", 600)

# 업스트림 최장 기한 15s (t=0..15s, x: 80..470)
d.tone(80, 156, 390, 32, WARN, r=4, op="14", sw=1.0)
d.t(275, 177, "가장 긴 요청 상한 15s (업스트림 기한)", 13, WARN, KR, "middle", 600)

# 꺼진 2초 (refused, t=0..2s, 회색) & 실측 처리 완료 (t=2..3.68s, OK)
d.tone(80, 196, 52, 32, SOFT, r=4, op="24", sw=1.0)
d.t(106, 216, "refused", 11, SOFT, MONO, "middle")

# 눈금 1초 = 26px (x = 80 + 26t) 이므로 t=2..3.68s 는 x=132..176. 라벨은 막대 오른쪽 밖에 둔다
d.tone(132, 196, 44, 32, OK, r=4, op="18", sw=1.0)
d.t(186, 216, "실측 3.68s 에 처리 중 등록 완료 (끊김 0건)", 13, OK, KR, "start", 600)

# 2. 시간축 기준선 (Timeline Baseline at y=264)
BASE_Y = 264
d.line(60, BASE_Y, 900, BASE_Y, RULE, 1.0)

# 눈금 및 사건 (0s, 2s, 15s, 20s, 30s)
# 0s (SIGTERM 수신, 새 연결 거절)
d.line(80, BASE_Y - 4, 80, BASE_Y + 4, SOFT, 0.8)
d.o.append(f'<circle cx="80" cy="{BASE_Y}" r="4" fill="{MUTED}"/>')
d.t(80, 282, "0s", 13, INK, MONO, "middle", 600)
d.t(80, 298, "새 연결 거절", 13, WARN, KR, "middle")
d.t(80, 314, "SIGTERM 수신", 13, MUTED, KR, "middle")

# 2s (단일 프록시 재시작 refused 구간 끝 · 옛 드레인 기한)
d.line(132, BASE_Y - 4, 132, BASE_Y + 4, SOFT, 0.8)
d.o.append(f'<circle cx="132" cy="{BASE_Y}" r="4" fill="{SOFT}"/>')
d.t(132, 282, "2s", 13, SOFT, MONO, "middle", 600)
d.t(132, 334, "옛 1.99s 잘림", 13, WARN, KR, "middle")

# 15s (업스트림 최장 기한)
d.line(470, BASE_Y - 4, 470, BASE_Y + 4, SOFT, 0.8)
d.o.append(f'<circle cx="470" cy="{BASE_Y}" r="4" fill="{WARN}"/>')
d.t(470, 282, "15s", 13, WARN, MONO, "middle", 600)
d.t(470, 298, "업스트림 15s", 13, WARN, KR, "middle")
d.t(470, 314, "가장 긴 요청 상한", 13, MUTED, KR, "middle")

# 20s (드레인 기한 · focal) — 축 위 구간과 축 아래 분기 구간으로 분리하여 텍스트 겹침 방지
d.line(600, 108, 600, BASE_Y, ACC, 1.8, dash="4 3")
d.line(600, 328, 600, 350, ACC, 1.8, dash="4 3")
d.o.append(f'<circle cx="600" cy="{BASE_Y}" r="8" fill="none" stroke="{ACC}" stroke-width="2.0"/>')
d.o.append(f'<circle cx="600" cy="{BASE_Y}" r="5" fill="{ACC}"/>')
d.t(600, 98, "드레인 기한 20s", 14, ACC, KR, "middle", 600)
d.t(600, 282, "20s", 13, ACC, MONO, "middle", 600)
d.t(600, 298, "드레인 20s", 13, ACC, KR, "middle")
d.t(600, 314, "종료 분기", 13, ACC, KR, "middle")

# 30s (쿠버네티스 강제 종료)
d.line(860, BASE_Y - 4, 860, BASE_Y + 4, SOFT, 0.8)
d.o.append(f'<circle cx="860" cy="{BASE_Y}" r="4" fill="{INFO}"/>')
d.t(860, 282, "30s", 13, INFO, MONO, "middle", 600)
d.t(860, 298, "쿠버네티스 30s", 13, INFO, KR, "middle")
d.t(860, 314, "강제 종료 상한", 13, MUTED, KR, "middle")

# 3. 종료 코드 분기 (y = 350 ~ 416)
# 좌측 분기 (제때 완료 -> exit 0)
d.arrow([(600, 350), (320, 350), (320, 368)], c=OK, m="ok", sw=1.4)
d.tone(180, 368, 280, 48, OK, r=6, op="18", sw=1.2)
d.t(320, 388, "제때 완료 (≤20s): 정상 종료", 13, OK, KR, "middle", 600)
d.t(320, 404, "끊긴 요청 0건 · exit 0", 13, INK, KR, "middle")

# 우측 분기 (기한 초과 -> exit 1)
d.arrow([(600, 350), (740, 350), (740, 368)], c=BAD, m="bad", sw=1.4)
d.tone(600, 368, 280, 48, BAD, r=6, op="18", sw=1.2)
d.t(740, 388, "기한 초과 (>20s): ctx.Err()", 13, BAD, KR, "middle", 600)
d.t(740, 404, "잔여 요청 로그 · exit 1", 13, INK, KR, "middle")

# 4. 하단 비교 카드: 리허설 J4 실측과 ADR 0014 서열 (y = 432 ~ 508)
d.box(60, 432, 840, 76, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(80, 452, "리허설 J4 실측과 ADR 0014 서열", 13, INK, KR, "start", 600)
d.t(80, 474, "고치기 전(드레인 2s): 1.99s 잘림 · 손님 eof 2건 · exit 0 착시", 13, WARN, KR, "start")
d.t(80, 494, "고친 뒤(드레인 20s): 3.68s 완료 · 손님 eof 0건 · 정상 exit 0 달성", 13, OK, KR, "start")

# 5. 범례
d.legend(524, [
    ("드레인 기한 20s", ACC),
    ("정상 exit 0", OK),
    ("최장 기한 15s", WARN),
    ("초과 exit 1", BAD),
    ("k8s 상한 30s", INFO),
])

out_path = ASSETS_DIR / "01-03-drain.svg"
d.save(str(out_path))
print(f"saved: {out_path}")
