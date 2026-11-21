# 타입 스펙: type-nested
# 02-01.package-boundary — JDK 폴더 경계 안과 밖의 참조 구조
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 450

d = D(W, H, "CONTAINER · 02-01",
      "포장 방식별 파일 경계",
      "RPM 설치 시 발생하는 OS 참조(좌) vs tar 자급자족 구조(우)",
      lead="경계를 넘는 외부 OS 참조 유무 비교")

X_L = 24
COL_W = 444
COL_H = 300
Y0 = 90

# ── 좌측: RPM 패키지 JDK (경계 밖 참조) ─────────────────────────────
d.box(X_L, Y0, COL_W, COL_H, PAPER, RULE, 0.9, 8)
d.t(X_L + 16, Y0 + 24, "RPM 설치 (AL2023)", 12, BAD, KR, "start", 600)
d.chip(X_L + COL_W - 64, Y0 + 20, "외부 의존", BAD, 11)

JDK_BOX_Y = Y0 + 40
JDK_BOX_H = 120
d.tone(X_L + 12, JDK_BOX_Y, COL_W - 24, JDK_BOX_H, BAD, 6, "0E", 1.0)
d.t(X_L + 24, JDK_BOX_Y + 20, "JDK 경계 (JVM)", 11, INK, KR, "start", 600)

d.box(X_L + 24, JDK_BOX_Y + 32, 180, 72, PAPER2, RULE, 0.8, 4)
d.t(X_L + 34, JDK_BOX_Y + 52, "lib/cacerts", 11, WARN, MONO, "start")
d.t(X_L + 34, JDK_BOX_Y + 70, "symlink 포인터", 10, MUTED, KR, "start")
d.chip(X_L + 114, JDK_BOX_Y + 90, "포인터만 소유", WARN, 10)

d.box(X_L + 224, JDK_BOX_Y + 32, 196, 72, PAPER2, RULE, 0.8, 4)
d.t(X_L + 234, JDK_BOX_Y + 52, "libjavajpeg.so", 11, WARN, MONO, "start")
d.t(X_L + 234, JDK_BOX_Y + 70, "동적 라이브러리", 10, MUTED, KR, "start")
d.chip(X_L + 322, JDK_BOX_Y + 90, "외부 심볼 요구", WARN, 10)

OS_BOX_Y = Y0 + 176
OS_BOX_H = 110
d.box(X_L + 12, OS_BOX_Y, COL_W - 24, OS_BOX_H, PAPER2, RULE, 0.8, 6)
d.t(X_L + 24, OS_BOX_Y + 20, "외부 베이스 OS", 11, SOFT, KR, "start")

d.tone(X_L + 24, OS_BOX_Y + 32, 180, 64, BAD, 4, "12", 0.9)
d.t(X_L + 34, OS_BOX_Y + 52, "OS cacerts", 10, INK, MONO, "start")
d.t(X_L + 34, OS_BOX_Y + 70, "ca-certificates", 10, BAD, KR, "start")

d.tone(X_L + 224, OS_BOX_Y + 32, 196, 64, BAD, 4, "12", 0.9)
d.t(X_L + 234, OS_BOX_Y + 52, "libjpeg.so.62", 10, INK, MONO, "start")
d.t(X_L + 234, OS_BOX_Y + 70, "libjpeg-turbo", 10, BAD, KR, "start")

d.arrow([(X_L + 114, JDK_BOX_Y + 104), (X_L + 114, OS_BOX_Y + 30)], BAD, "bad", 1.3)
d.arrow([(X_L + 322, JDK_BOX_Y + 104), (X_L + 322, OS_BOX_Y + 30)], BAD, "bad", 1.3)

# ── 우측: tar 압축 해제 JDK (자급자족 완성형) ───────────────────────
X_R = X_L + COL_W + 24

d.box(X_R, Y0, COL_W, COL_H, PAPER, RULE, 0.9, 8)
d.t(X_R + 16, Y0 + 24, "tar 해제 (Corretto)", 12, OK, KR, "start", 600)
d.chip(X_R + COL_W - 64, Y0 + 20, "둘 다 내장", OK, 11)

d.tone(X_R + 12, JDK_BOX_Y, COL_W - 24, JDK_BOX_H, OK, 6, "0E", 1.0)
d.t(X_R + 24, JDK_BOX_Y + 20, "JDK 경계 (JVM)", 11, INK, KR, "start", 600)

d.box(X_R + 24, JDK_BOX_Y + 32, 180, 72, PAPER2, RULE, 0.8, 4)
d.t(X_R + 34, JDK_BOX_Y + 52, "lib/cacerts", 11, OK, MONO, "start")
d.t(X_R + 34, JDK_BOX_Y + 70, "실제 파일 (172KB)", 10, MUTED, KR, "start")
d.chip(X_R + 114, JDK_BOX_Y + 90, "자체 보관", OK, 10)

d.box(X_R + 224, JDK_BOX_Y + 32, 196, 72, PAPER2, RULE, 0.8, 4)
d.t(X_R + 234, JDK_BOX_Y + 52, "libjavajpeg.so", 11, OK, MONO, "start")
d.t(X_R + 234, JDK_BOX_Y + 70, "내장 JPEG 루틴", 10, MUTED, KR, "start")
d.chip(X_R + 322, JDK_BOX_Y + 90, "libjpeg 불필요", OK, 10)

d.box(X_R + 12, OS_BOX_Y, COL_W - 24, OS_BOX_H, PAPER2, RULE, 0.8, 6)
d.t(X_R + 24, OS_BOX_Y + 20, "외부 베이스 OS", 11, SOFT, KR, "start")
d.box(X_R + 24, OS_BOX_Y + 32, COL_W - 48, 64, PAPER, RULE, 0.7, 4)
d.t(X_R + COL_W // 2, OS_BOX_Y + 68, "두 파일은 참조 없음 · libc·글꼴은 OS 몫", 11, OK, KR, "middle", 600)

# 범례
LEG_Y = 404
d.legend(LEG_Y, [
    ("경계 이탈 외부 OS 참조", BAD),
    ("JDK 폴더 안에 있음", OK),
])

out_path = sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path(__file__).resolve().parent.parent / "02-01.package-boundary.svg")
d.save(out_path)
print("ok gen-02-01.package-boundary")
