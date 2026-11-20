# 사실 출처: docs/configuration.md:6-140 · docs/design.md:39-54 · observations.md:15 · 10-upgrade-v0.10.0.md:26
# 타입 스펙: type-tree
import pathlib
import sys

_HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 980, 680
d = D(
    W, H,
    "FLATS DATA DIRECTORY · TREE",
    "호스트 데이터 디렉터리 레이아웃 및 백업 정책 트리",
    "설정·키·메타데이터·플랫 저장소·네트워크 상태 계층 구조",
    lead="Where data lives 명세와 실측 기준 항목별 백업 필요 여부를 함께 표기합니다"
)

# Root node
rx, ry, rw, rh = W / 2 - 120, 96, 240, 42
d.box(rx, ry, rw, rh, PAPER2, ACC, 1.2)
d.t(W / 2, ry + 18, "<data>/ (0700)", 13, INK, MONO, "middle", 600)
d.t(W / 2, ry + 33, "호스트 데이터 루트 디렉터리", 10, MUTED, KR, "middle")

COLS = [
    (
        "설정 및 인증 키",
        "호스트 식별·암호화",
        [
            ("config.json", "운영자 설정 단일 소스", "필수", OK),
            ("secret.key", "32B AES 키 (0600)", "필수", OK),
            ("config-history/", "이전 설정 사본 10개", "선택", INFO),
            ("flats.lock", "독점 flock 잠금 파일", "제외", WARN),
        ]
    ),
    (
        "메타데이터 DB",
        "SQLite 상태·백업",
        [
            ("flats.db", "호스트 SQLite 메타데이터", "필수", OK),
            ("flats.db-wal", "WAL 트랜잭션 저널", "제외", WARN),
            ("flats.db-shm", "WAL 공유 메모리 인덱스", "제외", WARN),
            ("backups/", "마이그레이션 전 DB 사본", "보관", INFO),
        ]
    ),
    (
        "플랫 아티팩트",
        "flats/<slug>/ 저장소",
        [
            ("draft-revs/", "초안 리비전 파일", "필수", OK),
            ("versions/", "불변 버전 아티팩트", "필수", OK),
            ("data/db.sqlite", "플랫 SQLite 데이터", "필수", OK),
            ("snapshots/", "배포 전 DB 스냅샷", "권장", INFO),
            ("previews/", "미리보기 임시 데이터", "제외", WARN),
        ]
    ),
    (
        "네트워크·런타임",
        "상태 노드 및 캐시",
        [
            ("portal/", "릴레이 인증·알리아스", "필수", OK),
            ("tsnet/·netbird/", "오버레이 노드 키·상태", "필수", OK),
            ("runtime/docs/", "내장 문서 앱 모듈", "재생성", MUTED),
            ("run/*.sock", "워커 IPC 유닉스 소켓", "재생성", MUTED),
            ("logs/", "serve.out / err 로그", "제외", WARN),
            ("cache/wazero/", "WASM 컴파일 캐시", "재생성", MUTED),
        ]
    ),
]

col_w = 220
gap = 18
start_x = (W - (col_w * 4 + gap * 3)) / 2
branch_y = 175

# Trunk connection line
d.line(W / 2, ry + rh, W / 2, branch_y, RULE, 1.2)
d.line(start_x + col_w / 2, branch_y, start_x + 3 * (col_w + gap) + col_w / 2, branch_y, RULE, 1.2)

for i, (cat_title, cat_sub, items) in enumerate(COLS):
    cx = start_x + i * (col_w + gap)
    mid_x = cx + col_w / 2

    # Drop line from branch
    d.line(mid_x, branch_y, mid_x, branch_y + 20, RULE, 1.2)

    # Category header
    d.box(cx, branch_y + 20, col_w, 38, PAPER2, RULE, 1.0)
    d.t(mid_x, branch_y + 36, cat_title, 11, INK, KR, "middle", 600)
    d.t(mid_x, branch_y + 50, cat_sub, 9, SOFT, KR, "middle")

    # Items
    item_y = branch_y + 66
    for name, desc, tag, tag_color in items:
        d.box(cx, item_y, col_w, 48, PAPER, RULE, 0.8)
        # File name and tag badge
        d.t(cx + 8, item_y + 18, name, 10, INK, MONO, "start", 600)

        # Badge
        badge_w = len(tag) * 11 + 8
        bx = cx + col_w - badge_w - 6
        d.o.append(f'<rect x="{bx}" y="{item_y + 6}" width="{badge_w}" height="16" rx="3" fill="{tag_color}22" stroke="{tag_color}" stroke-width="0.8"/>')
        d.t(bx + badge_w / 2, item_y + 17, tag, 9, tag_color, KR, "middle", 600)

        # Description
        d.t(cx + 8, item_y + 36, desc, 9, MUTED, KR, "start")

        item_y += 54

d.legend(635, [
    ("백업 필수 (복구 시 영구 손실 방지)", OK),
    ("권장·보관 (설정 이력 및 이전 DB)", INFO),
    ("제외 (런타임 생성 또는 프로세스 잠금)", WARN),
    ("재생성 (호스트 기동 시 자동 복구)", MUTED),
])

out_path = _HERE.parent / "05-01-data-dir.svg"
d.save(str(out_path))
print(f"Generated {out_path}")
