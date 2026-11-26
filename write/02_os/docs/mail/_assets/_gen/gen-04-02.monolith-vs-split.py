# 사실 출처: RFC 1135(https://www.rfc-editor.org/rfc/rfc1135), Postfix OVERVIEW(https://www.postfix.org/OVERVIEW.html), master.5(https://www.postfix.org/master.5.html), Sendmail 8.12(https://www.sendmail.org/~ca/email/sm-812.html)
# 타입 스펙: type-layers
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 540
d = D(
    W, H,
    "SECURITY ARCHITECTURE · MONOLITH VS PRIVILEGE SEPARATION",
    "단일 root 모놀리스 vs 최소 권한 분리 모델",
    "Sendmail의 단일 프로세스 전면 root 구조와 Postfix의 master 하위 비특권 프로세스 격리 구조 비교",
    "네트워크 파싱 취약점 발생 시 시스템 침해 범위(전체 root 장악 vs 비특권 격리)"
)

# 1. 왼쪽 스택: 전통 Sendmail (단일 바이너리 · 전면 root)
d.tone(40, 96, 420, 350, BAD, r=8, op="0a", sw=1.4)
d.box(40, 96, 420, 44, PAPER2, BAD, 1.2, r=8)
d.t(250, 123, "전통 Sendmail (단일 바이너리 · root 실행)", 13, BAD, fam=KR, weight=600)

layers_sendmail = [
    {"num": "01", "name": "네트워크 수신 · SMTP 명령 처리 (포트 25)", "sub": "root 권한 직접 수신 (1988 모리스 웜 DEBUG 악용 등)", "y": 148},
    {"num": "02", "name": "주소 파싱 · 룰셋 변환 (sendmail.cf)", "sub": "난해한 주소 재작성 룰셋", "y": 210},
    {"num": "03", "name": "스풀 큐 디렉터리 입출력 (/var/spool/mqueue)", "sub": "단일 큐 관리 및 임시 파일 경쟁 상태 위험", "y": 272},
    {"num": "04", "name": "로컬 배달 및 외부 전송 (.forward · 파이프)", "sub": "수신자 프로그램 파이프 실행 (전면 root 위험)", "y": 334}
]

for l in layers_sendmail:
    d.box(54, l["y"], 392, 54, PAPER2, BAD, 0.9, r=4)
    d.t(66, l["y"] + 20, l["num"], 10, BAD, fam=MONO, anchor="start", weight=600)
    d.t(90, l["y"] + 20, l["name"], 12, INK, fam=KR, anchor="start", weight=600)
    d.t(66, l["y"] + 39, l["sub"], 11, MUTED, fam=KR, anchor="start")

d.tone(40, 396, 420, 36, BAD, r=4, op="18", sw=1.2)
d.t(250, 419, "침해 범위: 파싱 결함 하나로 시스템 전체 root 장악", 12, BAD, fam=KR, weight=600)


# 2. 오른쪽 스택: 현대 Postfix (최소 권한 분리 다중 프로세스)
d.box(500, 96, 420, 44, PAPER2, OK, 1.2, r=8)
d.t(710, 123, "현대 Postfix (master 하위 권한 격리)", 13, OK, fam=KR, weight=600)

# master 데몬 (특권 상주 감시자)
d.box(514, 148, 392, 54, PAPER2, WARN, 1.2, r=4)
d.t(526, 168, "00", 10, WARN, fam=MONO, anchor="start", weight=600)
d.t(550, 168, "master(8) 데몬 (상주 감시자 · 프로세스 생성)", 12, INK, fam=KR, anchor="start", weight=600)
d.t(526, 187, "외부 패킷 파싱 안 함 · IPC 소켓 감시만 수행", 11, WARN, fam=KR, anchor="start")

# 권한 격리 경계선
d.line(500, 210, 920, 210, OK, 1.0, dash="4 3")

# 비특권 샌드박스 영역 (postfix)
d.tone(500, 216, 420, 230, OK, r=6, op="08", sw=1.2)

layers_postfix = [
    {"num": "01", "name": "smtpd(8) · pickup(8) (네트워크 / 로컬 접수)", "sub": "postfix 비특권 실행 · chroot 감금 가능", "y": 222},
    {"num": "02", "name": "cleanup(8) · trivial-rewrite(8) (정규화)", "sub": "복잡한 헤더 파싱을 비특권 샌드박스에 격리", "y": 280},
    {"num": "03", "name": "qmgr(8) · smtp(8) (스케줄링 및 외부 전송)", "sub": "활성 큐 관리 · 지연 메일 deferred 디스크 격리", "y": 338}
]

for l in layers_postfix:
    d.box(514, l["y"], 392, 50, PAPER2, OK, 0.9, r=4)
    d.t(526, l["y"] + 19, l["num"], 10, OK, fam=MONO, anchor="start", weight=600)
    d.t(550, l["y"] + 19, l["name"], 12, INK, fam=KR, anchor="start", weight=600)
    d.t(526, l["y"] + 37, l["sub"], 11, MUTED, fam=KR, anchor="start")

d.tone(500, 396, 420, 36, OK, r=4, op="18", sw=1.2)
d.t(710, 419, "침해 범위: 네트워크 침해 발생 시 비특권 샌드박스에 국한", 12, OK, fam=KR, weight=600)


# 3. 범례
d.legend(476, [
    ("전체 root 장악 위험", BAD),
    ("비특권 격리 계층", OK),
    ("최소 특권 감시자", WARN)
])

out = Path(__file__).parent.parent / "04-02.monolith-vs-split.svg"
d.save(str(out))
print(f"생성 완료: {out} ({W}x{H})")
