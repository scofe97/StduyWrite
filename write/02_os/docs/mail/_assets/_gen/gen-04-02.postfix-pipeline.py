# 사실 출처: Postfix OVERVIEW(https://www.postfix.org/OVERVIEW.html), master.5(https://www.postfix.org/master.5.html), QSHAPE_README(https://www.postfix.org/QSHAPE_README.html)
# 타입 스펙: type-data-flow
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 560
d = D(
    W, H,
    "POSTFIX ARCHITECTURE · DATA PIPELINE",
    "Postfix 메일 수신·큐잉·배달 파이프라인",
    "인바운드 연결 수락부터 cleanup 전처리, 디스크 큐 저장, qmgr 스케줄링, 외부 전송 및 지연 재시도 격리 흐름",
    "프로세스별 실행 권한(root / postfix)과 디스크·메모리 큐 분리 구조"
)

# 1. 5개 컬럼 스텝 헤더
cols = [
    {"num": "01", "name": "수신 · 로컬 제출", "x": 32, "w": 160},
    {"num": "02", "name": "정규화 · 전처리", "x": 212, "w": 160},
    {"num": "03", "name": "디스크 큐 저장", "x": 392, "w": 160},
    {"num": "04", "name": "배달 스케줄링", "x": 572, "w": 160},
    {"num": "05", "name": "전송 · 로컬 배달", "x": 752, "w": 176}
]

for c in cols:
    d.box(c["x"], 92, c["w"], 28, PAPER2, RULE, 0.8, r=4)
    d.t(c["x"] + 20, 110, c["num"], 11, ACC if c["num"] == "04" else MUTED, fam=MONO, weight=600)
    d.t(c["x"] + c["w"] // 2 + 10, 110, c["name"], 12, INK, fam=KR, weight=600)

# 2. 컴포넌트 박스들
# Step 01: 수신 및 제출
# smtpd (인바운드 네트워크)
d.box(36, 136, 152, 98, PAPER2, OK, 1.2)
d.t(112, 160, "smtpd(8)", 13, OK, fam=MONO, weight=600)
d.t(112, 180, "외부 인바운드 접수", 12, MUTED)
d.chip(112, 212, "postfix 비특권", OK, size=12)

# pickup (로컬 maildrop 감시)
d.box(36, 296, 152, 98, PAPER2, OK, 1.2)
d.t(112, 320, "pickup(8)", 13, OK, fam=MONO, weight=600)
d.t(112, 340, "maildrop 큐 감시", 12, MUTED)
d.chip(112, 372, "postfix 비특권", OK, size=12)

# Step 02: cleanup
d.box(216, 156, 148, 218, PAPER2, OK, 1.2)
d.t(290, 184, "cleanup(8)", 14, OK, fam=MONO, weight=600)
d.t(290, 212, "헤더 보완 · 주소 정규화", 12, INK)
d.t(290, 234, "trivial-rewrite 연계", 12, MUTED)
d.t(290, 256, "단일 큐 파일 생성", 12, MUTED)
d.t(290, 278, "qmgr 신규 도착 통지", 12, MUTED)
d.chip(290, 346, "postfix 비특권", OK, size=12)

# Step 03: 디스크 큐 (incoming / deferred)
# incoming queue
d.box(400, 136, 144, 98, PAPER2, INFO, 1.2)
d.t(472, 160, "incoming 큐", 13, INFO, fam=KR, weight=600)
d.t(472, 180, "신규 도착 메시지 대기", 12, MUTED)
d.chip(472, 212, "디스크 큐 파일", INFO, size=12)

# deferred queue
d.box(400, 296, 144, 98, PAPER2, INFO, 1.2)
d.t(472, 320, "deferred 큐", 13, INFO, fam=KR, weight=600)
d.t(472, 340, "일시 지연 메일 격리", 12, MUTED)
d.chip(472, 372, "디스크 큐 파일", INFO, size=12)

# Step 04: qmgr (배달 심장 · focal)
d.tone(580, 146, 148, 238, ACC, r=6, op="18", sw=1.5)
d.t(654, 172, "qmgr(8)", 14, ACC, fam=MONO, weight=600)
d.t(654, 192, "메일 배달 스케줄러", 12, INK, weight=600)

# qmgr 내부 active 큐 메모리 상자
d.box(590, 208, 128, 66, PAPER2, ACC, 1.0)
d.t(654, 230, "active 큐 (메모리)", 12, ACC, fam=KR, weight=600)
d.t(654, 252, "메모리 OOM 방지", 12, MUTED)

d.t(654, 304, "에이전트별 작업 분배", 12, MUTED)
d.chip(654, 356, "postfix 비특권", OK, size=12)

# Step 05: 배달 에이전트 (smtp / local)
# smtp
d.box(756, 136, 168, 98, PAPER2, OK, 1.2)
d.t(840, 160, "smtp(8)", 13, OK, fam=MONO, weight=600)
d.t(840, 180, "원격 MX 발송 (25)", 12, MUTED)
d.chip(840, 212, "postfix 비특권", OK, size=12)

# local
d.box(756, 296, 168, 98, PAPER2, WARN, 1.2)
d.t(840, 320, "local(8)", 13, WARN, fam=MONO, weight=600)
d.t(840, 340, "사서함 배달 · 파이프", 12, MUTED)
d.chip(840, 372, "root 특권 전환", WARN, size=12)


# 3. 화살표 연결 (모두 직각)
# smtpd -> cleanup (y=196에서 출발)
d.arrow([(188, 196), (202, 196), (202, 230), (216, 230)], OK, "ok", 1.4)

# pickup -> cleanup
d.arrow([(188, 344), (202, 344), (202, 290), (216, 290)], OK, "ok", 1.4)

# cleanup -> incoming queue
d.arrow([(364, 230), (382, 230), (382, 184), (400, 184)], INFO, "info", 1.4)
d.t(382, 166, "적재", 12, INFO, fam=KR, anchor="middle")

# incoming queue -> qmgr (active)
d.arrow([(544, 184), (562, 184), (562, 230), (580, 230)], ACC, "acc", 1.6)
d.t(562, 166, "진입", 12, ACC, fam=KR, anchor="middle")

# qmgr -> smtp
d.arrow([(728, 230), (742, 230), (742, 184), (756, 184)], OK, "ok", 1.4)

# qmgr -> local
d.arrow([(728, 290), (742, 290), (742, 344), (756, 344)], WARN, "warn", 1.4)

# smtp 실패 -> deferred queue (local 상자 오른쪽 바깥으로 안전하게 우회)
d.arrow([(924, 184), (938, 184), (938, 416), (472, 416), (472, 394)], BAD, "bad", 1.4, dash="4 3")
d.t(705, 434, "임시 실패 (4xx) 시 deferred 격리", 12, BAD, fam=KR, anchor="middle")

# deferred queue -> qmgr (active 재시도)
d.arrow([(472, 296), (472, 270), (580, 270)], MUTED, "ar", 1.4)
d.t(524, 262, "재시도 회수", 12, MUTED, fam=KR, anchor="middle")


# 4. 범례
d.legend(496, [
    ("비특권 데몬", OK),
    ("특권 필요", WARN),
    ("스케줄러", ACC),
    ("디스크 큐", INFO),
    ("지연 격리", BAD)
])

out = Path(__file__).parent.parent / "04-02.postfix-pipeline.svg"
d.save(str(out))
print(f"생성 완료: {out} ({W}x{H})")
