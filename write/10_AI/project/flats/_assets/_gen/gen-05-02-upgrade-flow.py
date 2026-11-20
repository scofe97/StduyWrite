# 사실 출처: docs/release.md 「Upgrading a host」 · 11-upgrade-v0.11.0.md:13-48 · 10-upgrade-v0.10.0.md:18-77 · internal/launchd/launchd.go:213-229
# 타입 스펙: type-process
import os
import pathlib
import sys

_HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 1000, 470
d = D(
    W, H,
    "HOST LIFECYCLE · UPGRADE PIPELINE",
    "Flats 호스트 업그레이드 절차",
    "서비스 정지, 전체 백업, 바이너리 교체, 스키마 마이그레이션 및 5대 검증",
    lead="다운그레이드 불가에 대비해 정지 후 전체 백업을 선행합니다"
)

cols = [
    ("1. 정지", "bootout"),
    ("2. 사전 백업", "cp -Rp"),
    ("3. 바이너리", "install.sh"),
    ("4. 기동", "bootstrap"),
    ("5. 검증", "5대 확인"),
]

x0 = 24
gap = 16
y0 = 104
col_w = 178

for i, (title, sub) in enumerate(cols):
    cx = x0 + i * (col_w + gap)

    d.box(cx, y0, col_w, 40, fill=PAPER2, stroke=RULE, sw=1.0)
    d.t(cx + col_w / 2, y0 + 18, title, 11, INK, KR, "middle", 600)
    d.t(cx + col_w / 2, y0 + 32, sub, 10, MUTED, MONO, "middle")

    by = y0 + 48
    bh = 280
    stroke_c = ACC if i == 3 else (OK if i == 4 else RULE)
    sw = 1.3 if (i == 3 or i == 4) else 1.0
    d.box(cx, by, col_w, bh, fill=PAPER2, stroke=stroke_c, sw=sw)

    if i < 4:
        d.arrow([(cx + col_w, by + bh / 2), (cx + col_w + gap, by + bh / 2)], c=MUTED, m="ar")

# 1열: 정지
c1_x = x0
d.box(c1_x + 10, 160, col_w - 20, 64, fill=PAPER, stroke=WARN, sw=0.9, r=4)
d.t(c1_x + 18, 180, "launchctl bootout", 11, WARN, MONO, "start", 600)
d.t(c1_x + 18, 198, "gui/<uid>/serve", 9.5, MUTED, MONO, "start")
d.t(c1_x + 18, 214, "exit 0 종료", 10, OK, KR, "start")

d.box(c1_x + 10, 234, col_w - 20, 64, fill=PAPER, stroke=RULE, sw=0.9, r=4)
d.t(c1_x + 18, 254, "포트 해제 확인", 11, INK, KR, "start", 600)
d.t(c1_x + 18, 272, "lsof LISTEN", 10, MUTED, MONO, "start")
d.t(c1_x + 18, 288, "리스너 없음", 10, OK, KR, "start")

d.box(c1_x + 10, 308, col_w - 20, 80, fill=PAPER, stroke=INFO, sw=0.9, r=4)
d.t(c1_x + 18, 328, "WAL 체크포인트", 11, INFO, KR, "start", 600)
d.t(c1_x + 18, 346, "-wal/-shm 소멸", 9.5, INK, MONO, "start")
d.t(c1_x + 18, 364, "단일 DB 수렴", 9.5, OK, KR, "start")

# 2열: 백업
c2_x = x0 + (col_w + gap)
d.box(c2_x + 10, 160, col_w - 20, 64, fill=PAPER, stroke=INFO, sw=0.9, r=4)
d.t(c2_x + 18, 180, "데이터 복사", 11, INFO, KR, "start", 600)
d.t(c2_x + 18, 198, "cp -Rp <data>", 9.5, MUTED, MONO, "start")
d.t(c2_x + 18, 214, "권한 보존 (0700)", 10, OK, KR, "start")

d.box(c2_x + 10, 234, col_w - 20, 64, fill=PAPER, stroke=OK, sw=0.9, r=4)
d.t(c2_x + 18, 254, "동일성 확인", 11, OK, KR, "start", 600)
d.t(c2_x + 18, 272, "diff -r <원본> <백업>", 9.5, MUTED, MONO, "start")
d.t(c2_x + 18, 288, "일치 (7.7M)", 10, OK, KR, "start")

d.box(c2_x + 10, 308, col_w - 20, 80, fill=PAPER, stroke=WARN, sw=0.9, r=4)
d.t(c2_x + 18, 328, "비밀 키 포함", 11, WARN, KR, "start", 600)
d.t(c2_x + 18, 346, "secret.key 평문", 9.5, MUTED, KR, "start")
d.t(c2_x + 18, 364, ".gitignore 제외", 9.5, INK, MONO, "start")

# 3열: 바이너리
c3_x = x0 + 2 * (col_w + gap)
d.box(c3_x + 10, 160, col_w - 20, 64, fill=PAPER, stroke=INFO, sw=0.9, r=4)
d.t(c3_x + 18, 180, "스크립트 실행", 11, INFO, KR, "start", 600)
d.t(c3_x + 18, 198, "sh install.sh", 10, MUTED, MONO, "start")
d.t(c3_x + 18, 214, "sudo 없음", 10, OK, KR, "start")

d.box(c3_x + 10, 234, col_w - 20, 64, fill=PAPER, stroke=OK, sw=0.9, r=4)
d.t(c3_x + 18, 254, "바이너리 교체", 11, OK, KR, "start", 600)
d.t(c3_x + 18, 272, "~/.local/bin/flats", 9.5, INK, MONO, "start")
d.t(c3_x + 18, 288, "v0.11.0 (3abe537)", 9.5, OK, MONO, "start")

d.box(c3_x + 10, 308, col_w - 20, 80, fill=PAPER, stroke=RULE, sw=0.9, r=4)
d.t(c3_x + 18, 328, "서비스 대기", 11, INK, KR, "start", 600)
d.t(c3_x + 18, 346, "mode: replace", 9.5, MUTED, MONO, "start")
d.t(c3_x + 18, 364, "정지 상태 유지", 9.5, OK, KR, "start")

# 4열: 기동 (Focal)
c4_x = x0 + 3 * (col_w + gap)
d.box(c4_x + 10, 160, col_w - 20, 64, fill=PAPER, stroke=ACC, sw=0.9, r=4)
d.t(c4_x + 18, 180, "서비스 로드", 11, ACC, KR, "start", 600)
d.t(c4_x + 18, 198, "launchctl enable", 9.5, MUTED, MONO, "start")
d.t(c4_x + 18, 214, "bootstrap", 9.5, INK, MONO, "start")

d.box(c4_x + 10, 234, col_w - 20, 64, fill=PAPER, stroke=WARN, sw=0.9, r=4)
d.t(c4_x + 18, 254, "자동 DB 백업", 11, WARN, KR, "start", 600)
d.t(c4_x + 18, 272, "<data>/backups/", 9.5, MUTED, MONO, "start")
d.t(c4_x + 18, 288, "flats.v15.*.db", 9.5, OK, MONO, "start")

d.box(c4_x + 10, 308, col_w - 20, 80, fill=PAPER, stroke=ACC, sw=0.9, r=4)
d.t(c4_x + 18, 328, "마이그레이션", 11, ACC, KR, "start", 600)
d.t(c4_x + 18, 346, "flats.uid 부여", 9.5, INK, MONO, "start")
d.t(c4_x + 18, 364, "구버전 롤백 거부", 9.5, BAD, KR, "start")

# 5열: 검증
c5_x = x0 + 4 * (col_w + gap)
checks = [
    ("flats version", "v0.11.0"),
    ("LISTEN", "7878 / 7879"),
    ("flats list", "7개 보존"),
    ("MCP tools", "36개 목록"),
    ("client check", "contract 2"),
]

for ci, (cmd, exp) in enumerate(checks):
    cy = 160 + ci * 46
    d.box(c5_x + 10, cy, col_w - 20, 40, fill=PAPER, stroke=OK, sw=0.9, r=4)
    d.t(c5_x + 18, cy + 16, cmd, 10, INK, MONO, "start", 600)
    d.t(c5_x + 18, cy + 30, exp, 9.5, OK, MONO, "start")

out_path = _HERE.parent / "05-02-upgrade-flow.svg"
d.save(str(out_path))
print(f"saved: {out_path}")
