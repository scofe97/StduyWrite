# 사실 출처: docs/configuration.md 「What to back up」 · 07-backup-restore.md:47-62 · 10-upgrade-v0.10.0.md:26
# 타입 스펙: type-dp-security-matrix
import os
import pathlib
import sys

_HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 1000, 620
d = D(
    W, H,
    "STORAGE & BACKUP · DATA DIRECTORY MATRIX",
    "Flats 데이터 디렉터리 구성과 백업 판정표",
    "복구 필수 여부, 비밀 포함 여부, 라이브 복사 위험도 매트릭스",
    lead="DB 하나로는 복구할 수 없으며 평문 비밀 키를 포함하므로 백업 자체를 격리합니다"
)

cols = [
    ("데이터 디렉터리 항목", 250),
    ("복구에 필수", 220),
    ("비밀값 포함", 220),
    ("켜진 채 복사 위험", 230),
]

rows = [
    {
        "item": "flats.db",
        "sub": "메타데이터 · 승인 DB",
        "cells": [
            ("필수", "메타데이터·이력 원천", OK, True),
            ("안전", "암호화 저장", OK, False),
            ("위험", "VACUUM INTO 필수", BAD, False),
        ]
    },
    {
        "item": "flats/<slug>/",
        "sub": "초안·버전·문서 DB",
        "cells": [
            ("필수", "실제 파일·문서 데이터", OK, True),
            ("해당 없음", "평문 파일·문서 DB", OK, False),
            ("위험", "실시간 쓰기 충돌", BAD, False),
        ]
    },
    {
        "item": "secret.key",
        "sub": "비밀값 암호화 키 (32B)",
        "cells": [
            ("필수", "없으면 비밀 복호화 불가", OK, True),
            ("포함 (평문)", "0600 권한 격리 필수", WARN, False),
            ("안전", "정적 키 파일", OK, False),
        ]
    },
    {
        "item": "config.json",
        "sub": "호스트 설정 (포트·정책)",
        "cells": [
            ("필수", "인스턴스 ID·바인딩 설정", OK, True),
            ("안전", "키 미포함 (0600)", OK, False),
            ("안전", "정적 설정 파일", OK, False),
        ]
    },
    {
        "item": "portal/ · tsnet/ 등",
        "sub": "네트워크 제공자 상태",
        "cells": [
            ("필수", "노드명·인증서 보존", OK, True),
            ("안전", "신원 상태 데이터", OK, False),
            ("안전", "정지 상태 복사 권장", OK, False),
        ]
    },
    {
        "item": "backups/",
        "sub": "마이그레이션 백업 DB",
        "cells": [
            ("선택", "구버전 스키마 백업본", MUTED, False),
            ("안전", "암호문 DB", OK, False),
            ("안전", "불변 파일", OK, False),
        ]
    },
    {
        "item": "runtime/",
        "sub": "문서 워커 실행 자산",
        "cells": [
            ("불필요", "기동 시 자동 재생성", MUTED, False),
            ("안전", "내장 JS 자산", OK, False),
            ("안전", "휘발성 자산", OK, False),
        ]
    },
    {
        "item": "cache/",
        "sub": "빌드 및 모듈 캐시",
        "cells": [
            ("불필요", "캐시 미스 시 재빌드", MUTED, False),
            ("안전", "캐시 데이터", OK, False),
            ("안전", "휘발성 데이터", OK, False),
        ]
    },
    {
        "item": "run/ · flats.lock",
        "sub": "소켓 및 프로세스 락",
        "cells": [
            ("불필요", "프로세스 종료 시 무효", MUTED, False),
            ("안전", "런타임 소켓", OK, False),
            ("위험", "복원 시 잠금 충돌 유발", BAD, False),
        ]
    },
]

x0 = 24
y0 = 96
col_xs = []
cur_x = x0
for title, w in cols:
    col_xs.append((cur_x, w))
    cur_x += w + 8

# 열 헤더
for i, (title, w) in enumerate(cols):
    cx, cw = col_xs[i]
    d.box(cx, y0, cw, 32, fill=PAPER2, stroke=RULE, sw=1.0)
    d.t(cx + cw / 2, y0 + 20, title, 11, INK, KR, "middle", 600)

# 행 데이터
row_h = 48
for r_idx, r in enumerate(rows):
    ry = y0 + 38 + r_idx * (row_h + 6)

    # 1열: 항목 명칭 및 부제
    cx, cw = col_xs[0]
    d.box(cx, ry, cw, row_h, fill=PAPER2, stroke=RULE, sw=0.9)
    d.t(cx + 14, ry + 19, r["item"], 11, INK, MONO if "/" in r["item"] or "." in r["item"] else KR, "start", 600)
    d.t(cx + 14, ry + 36, r["sub"], 9.5, MUTED, KR, "start")

    # 2~4열: 셀 데이터
    for c_idx, (status, desc, col, is_focal) in enumerate(r["cells"]):
        cx, cw = col_xs[c_idx + 1]
        stroke_c = ACC if is_focal else (col if col in (BAD, WARN) else RULE)
        sw = 1.2 if (is_focal or col in (BAD, WARN)) else 0.8
        d.box(cx, ry, cw, row_h, fill=PAPER2, stroke=stroke_c, sw=sw)

        d.t(cx + 14, ry + 20, status, 11, col, KR, "start", 600)
        d.t(cx + 14, ry + 36, desc, 9.5, MUTED, KR, "start")

out_path = _HERE.parent / "05-02-backup-set.svg"
d.save(str(out_path))
print(f"saved: {out_path}")
