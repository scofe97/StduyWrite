# 타입 스펙: type-process
# 02-02.change-path — JDK-8245545 변경이 업데이트 저장소에서 배포판으로 들어오는 길
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 508

d = D(
    W, H,
    "CONTAINER · 02-02",
    "변경이 들어오는 길 — JDK-8245545 추적",
    "1·2단계 비공개 입구·일정을 옆에 두고, 원 이슈 JDK-8245545(Fix Version 24)와 3단계 jdk-updates 저장소에서 4단계 판별 백포트·태그·Corretto 빌드로 이어지는 경로와 6단계 릴리스 노트",
    lead="원 이슈 JDK-8245545(Fix Version 24)의 백포트 추적 · 1·2단계는 거쳤다는 자료 없음",
)

# ── 단계 머리 (1·2 옆 입구 + 3~6 주 흐름) ─────────────────────────────
COLS = [
    (16, 192, "1·2. 비공개 입구·일정", "거쳤다는 자료 없음", MUTED, False),
    (232, 160, "3. 업데이트 저장소", "jdk-updates", INFO, False),
    (420, 188, "4. 판별 백포트", "판별 이슈", ACC, True),
    (640, 184, "5. 태그 → 배포판", "태그·빌드", OK, False),
    (844, 140, "6. 릴리스 노트", "변경 공지", INFO, False),
]

HDR_Y, HDR_H = 92, 44
for cx, cw, title, sub, col, is_focal in COLS:
    if is_focal:
        d.tone(cx, HDR_Y, cw, HDR_H, ACC, 6, "14", 1.3)
    else:
        d.box(cx, HDR_Y, cw, HDR_H, PAPER2, RULE, 1.0, 6)
    fam_sub = MONO if "jdk" in sub or "Corretto" in sub else KR
    d.t(cx + cw // 2, HDR_Y + 18, title, 13, ACC if is_focal else INK, KR, "middle", 600)
    d.t(cx + cw // 2, HDR_Y + 36, sub, 11, MUTED, fam_sub, "middle")

# ── 화살표 먼저 (z-order 규칙, 모두 직각 연결선) ───────────────────────
# 1·2단계 비공개 입구·일정 → 3단계 jdk-updates 상자 (객체 없는 유입선)
d.arrow([(208, 284), (230, 284)], MUTED, "ar", 1.3, "4 3")

# 원 이슈 JDK-8245545 (jdk-updates 밖, y=152..224) → 4단계 판별 백포트 셋
d.arrow([(392, 174), (418, 174)], ACC, "acc", 1.5)
d.arrow([(392, 192), (408, 192), (408, 278), (418, 278)], INFO, "info", 1.3)
d.arrow([(392, 210), (400, 210), (400, 360), (418, 360)], WARN, "warn", 1.3)

# 4단계 JDK-8367436 (jdk17u · 17.0.18) → 5단계 OpenJDK 태그 jdk-17.0.18-ga
d.arrow([(608, 192), (638, 192)], ACC, "acc", 1.5)

# 5단계 내부: jdk-17.0.18-ga → Corretto 17.0.18.8.1
d.arrow([(732, 244), (732, 290)], ACC, "acc", 1.5)

# ── 1·2단계: 비공개 입구·일정 (측면 분리 구역) ─────────────────────────
d.o.append(f'<rect x="16" y="152" width="192" height="244" rx="6" fill="{PAPER}" stroke="{MUTED}" stroke-width="1.0" stroke-dasharray="4 3"/>')

d.box(28, 164, 168, 96, PAPER2, RULE, 0.9, 6)
d.t(112, 184, "Vulnerability Group", 11, INK, MONO, "middle", 600)
d.t(112, 204, "비공개 포럼", 11, MUTED, KR, "middle")
d.t(112, 224, "OCA·비밀유지 동의", 11, MUTED, KR, "middle")
d.t(112, 244, "Oracle 리더 임명", 11, SOFT, KR, "middle")

d.box(28, 272, 168, 84, PAPER2, RULE, 0.9, 6)
d.t(112, 294, "Oracle CPU", 12, INK, MONO, "middle", 600)
d.t(112, 316, "취약점 패치 모음", 12, MUTED, KR, "middle")
d.t(112, 338, "1·4·7·10월 셋째 화요일", 11, SOFT, KR, "middle")

d.t(112, 380, "비공개 수정 유입", 12, MUTED, KR, "middle")

# ── 3단계 영역: 원 이슈(밖) + jdk-updates 저장소 상자(아래) ─────────────
# 원 이슈 JDK-8245545 (jdk-updates 상자 밖에 따로 배치)
d.tone(232, 152, 160, 72, ACC, 6, "14", 1.4)
d.t(312, 174, "JDK-8245545", 12, ACC, MONO, "middle", 600)
d.t(312, 194, "원 이슈 · Fix Version 24", 11, INK, KR, "middle")
d.t(312, 214, "TLS_RSA_* 끄기", 11, ACC, KR, "middle")

# jdk-updates 상자: jdk-updates 와 jdk17u · jdk21u 만 포함
d.box(232, 236, 160, 160, PAPER2, RULE, 1.0, 6)
d.t(312, 256, "jdk-updates", 12, INK, MONO, "middle", 600)
d.t(312, 274, "RDP2 이후", 11, MUTED, KR, "middle")

d.tone(244, 286, 136, 44, ACC, 4, "0E", 1.0)
d.t(312, 304, "jdk17u", 12, ACC, MONO, "middle", 600)
d.t(312, 322, "17.0.12~17.0.21", 10, MUTED, MONO, "middle")

d.tone(244, 340, 136, 44, INFO, 4, "0E", 1.0)
d.t(312, 358, "jdk21u", 12, INFO, MONO, "middle", 600)
d.t(312, 376, "21.0.8~21.0.13", 10, MUTED, MONO, "middle")

# ── 4단계: 판별 백포트 ───────────────────────────────────────────────
# 움직이는 객체 2: JDK-8367436 (jdk17u · 17.0.18 추적 대상)
d.tone(420, 152, 188, 80, ACC, 6, "14", 1.4)
d.t(514, 176, "JDK-8367436", 13, ACC, MONO, "middle", 600)
d.t(514, 198, "jdk17u · 17.0.18", 12, INK, MONO, "middle")
d.t(514, 220, "TLS_RSA_* 끄기", 12, ACC, KR, "middle")

# 형제 백포트: jdk21u · 21.0.10
d.tone(420, 244, 188, 68, INFO, 6, "10", 1.1)
d.t(514, 270, "JDK-8367434", 13, INFO, MONO, "middle", 600)
d.t(514, 294, "jdk21u · 21.0.10", 12, INK, MONO, "middle")

# 형제 백포트: 17.0.18-oracle (저장소 근거 없음 · 접미사 뜻 미확인)
d.tone(420, 324, 188, 72, WARN, 6, "10", 1.1)
d.t(514, 346, "JDK-8356230", 13, WARN, MONO, "middle", 600)
d.t(514, 366, "17.0.18-oracle", 11, INK, MONO, "middle")
d.t(514, 386, "접미사 뜻 확인 못함", 12, WARN, KR, "middle")

# ── 5단계: OpenJDK 태그 → Corretto 배포판 빌드 ─────────────────────────
# 움직이는 객체 3: jdk-17.0.18-ga
d.tone(640, 152, 184, 92, ACC, 6, "14", 1.4)
d.t(732, 176, "jdk-17.0.18-ga", 12, ACC, MONO, "middle", 600)
d.t(732, 200, "jdk.tls.disabledAlgorithms", 10, MUTED, MONO, "middle")
d.t(732, 226, "TLS_RSA_*", 12, INK, MONO, "middle", 600)

# 움직이는 객체 4: Corretto 17.0.18.8.1
d.tone(640, 292, 184, 96, OK, 6, "12", 1.2)
d.t(732, 316, "Corretto 17.0.18.8.1", 12, OK, MONO, "middle", 600)
d.t(732, 340, "TLS_RSA_* 끄기", 12, INK, KR, "middle")
d.t(732, 364, "동일 판 속성 일치", 12, MUTED, KR, "middle")

# ── 6단계: 릴리스 노트 ───────────────────────────────────────────────
d.tone(844, 152, 140, 118, INFO, 6, "12", 1.1)
d.t(914, 176, "JDK-8344767", 12, INFO, MONO, "middle", 600)
d.t(914, 198, "TLS_RSA_* 끄기", 12, INK, KR, "middle")
d.t(914, 220, "Fix Version:", 10, MUTED, MONO, "middle")
d.t(914, 238, "17.0.18-oracle", 10, WARN, MONO, "middle")
d.t(914, 256, "21.0.10-oracle", 10, INFO, MONO, "middle")

d.box(844, 292, 140, 96, PAPER2, RULE, 0.9, 6)
d.t(914, 320, "벤더 변경 기록", 13, INK, KR, "middle", 600)
d.t(914, 344, "Corretto 17", 11, MUTED, MONO, "middle")
d.t(914, 364, "CHANGELOG", 11, MUTED, MONO, "middle")

# ── 순서 안내 주석 한 줄 ─────────────────────────────────────────────
d.box(16, 412, 968, 28, PAPER2, RULE, 0.8, 4)
d.t(28, 430, "주석: 자료가 이 순서를 직접 적은 것 아님", 12, MUTED, KR, "start")

# ── 범례 ────────────────────────────────────────────────────────────
LEG_Y = 456
d.legend(LEG_Y, [
    ("17.0.18 추적", ACC),
    ("21.0.10", INFO),
    ("-oracle 미확인", WARN),
    ("Corretto", OK),
    ("비공개 수정 입구", MUTED),
])

out_path = sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path(__file__).resolve().parent.parent / "02-02.change-path.svg")
d.save(out_path)
print("ok gen-02-02.change-path")
