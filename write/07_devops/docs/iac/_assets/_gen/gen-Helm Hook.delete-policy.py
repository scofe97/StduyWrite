# 타입 스펙: type-process
# 4절 끝난 Hook 리소스는 누가 지우는가 — 삭제 정책별 리소스 잔류와 충돌
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 480

d = D(W, H, "HELM · HOOK DELETE POLICY",
      "Hook 삭제 정책별 리소스 잔류 시점과 업그레이드 충돌",
      "before-hook-creation 및 hook-succeeded 정상/실패 시점별 리소스 잔류 상태 및 immutable 충돌 메커니즘",
      lead="hook-succeeded 단독 지정 시 실패한 Job 이 남아 다음 업그레이드가 field is immutable 로 막힙니다")

# 열(Column) 좌표: 좌측 정책명(192) + 3개 단계 컬럼(각 224, 간격 16)
LABEL_X, LABEL_W = 24, 192
COLS = [
    (232, 224, "1. 실행 직후", "Job 실행 및 완료 시점"),
    (472, 224, "2. 다음 upgrade 직전", "클러스터 리소스 잔류"),
    (712, 224, "3. 다음 upgrade 실행", "새 릴리스 생성 시도"),
]

# 컬럼 헤더 렌더
HEAD_Y = 96
HEAD_H = 44
for x, w, title, sub in COLS:
    d.box(x, HEAD_Y, w, HEAD_H, PAPER2, RULE, 1.0)
    d.t(x + w // 2, HEAD_Y + 18, title, 13, INK, KR, "middle", 600)
    d.t(x + w // 2, HEAD_Y + 34, sub, 11, MUTED, KR, "middle")

ROWS = [
    {
        "label": "before-hook-creation",
        "label_sub": "어노테이션 미지정 기본값",
        "label_c": INFO,
        "focal": False,
        "steps": [
            ("Job 완료 보존", "hl-hokv-app-migrate 잔류", "완료 상태", INFO),
            ("Job 보존 잔류", "kubectl logs 조회 가능", "로그 확인", INFO),
            ("선삭제 후 재생성", "기존 Job 자동 삭제 후 생성", "UPGRADE 성공 (rev 9)", OK),
        ],
    },
    {
        "label": "hook-succeeded",
        "label_sub": "성공 직후 즉시 삭제",
        "label_c": INFO,
        "focal": False,
        "steps": [
            ("Job 즉시 삭제", "NotFound: job not found", "정리 완료", OK),
            ("Job 미잔류", "클러스터 리소스 없음", "충돌 부재", MUTED),
            ("새 Job 바로 생성", "이름 충돌 없이 생성", "UPGRADE 성공 (rev 5)", OK),
        ],
    },
    {
        "label": "hook-succeeded 단독",
        "label_sub": "실패 시 삭제 미수행",
        "label_c": BAD,
        "focal": True,
        "steps": [
            ("Job 실패 잔류", "Job Failed (failed: 1/1)", "조건 미달", WARN),
            ("실패 Job 잔류", "수정 재시도 전까지 방치", "오류 미해결", BAD),
            ("불변 필드 오류 차단", "spec.template is immutable", "UPGRADE 실패", BAD),
        ],
    },
]

ROW_Y0 = 152
ROW_H = 76
ROW_GAP = 12

for i, r in enumerate(ROWS):
    y = ROW_Y0 + i * (ROW_H + ROW_GAP)
    focal = r["focal"]

    # 좌측 정책 박스
    border_c = BAD if focal else (INFO if r["label_c"] == INFO else RULE)
    d.box(LABEL_X, y, LABEL_W, ROW_H, PAPER2, border_c, 1.2 if focal else 0.9)
    d.t(LABEL_X + LABEL_W // 2, y + 28, r["label"], 13, r["label_c"], MONO if "hook" in r["label"] else KR, "middle", 600)
    d.t(LABEL_X + LABEL_W // 2, y + 50, r["label_sub"], 11, MUTED, KR, "middle")

    # 단계별 3개 카드
    for j, (title, sub, chip_txt, c) in enumerate(r["steps"]):
        cx, cw, _, _ = COLS[j]
        c_border = c if (focal and j == 2) else (c if c in (OK, BAD) else RULE)
        d.box(cx, y, cw, ROW_H, PAPER, c_border, 1.2 if (focal and j == 2) else 0.9)
        d.t(cx + cw // 2, y + 24, title, 13, c if c in (OK, BAD, WARN) else INK, KR, "middle", 600)
        d.t(cx + cw // 2, y + 42, sub, 11, MUTED, MONO if any(k in sub for k in (":", "is", "rev")) else KR, "middle")
        
        # 상태 칩
        chip_w = sum(11.0 if "가" <= ch <= "힣" else 6.8 for ch in chip_txt) + 16
        d.o.append(f'<rect x="{cx + cw // 2 - chip_w / 2}" y="{y + 52}" width="{chip_w}" height="16" rx="3" fill="{c}18" stroke="{c}" stroke-width="0.8"/>')
        d.t(cx + cw // 2, y + 64, chip_txt, 11, c, KR if any("가" <= ch <= "힣" for ch in chip_txt) else MONO, "middle", 600)

        # 단계 간 화살표
        if j < 2:
            ax1 = cx + cw + 2
            ax2 = COLS[j + 1][0] - 2
            ay = y + ROW_H // 2
            d.arrow([(ax1, ay), (ax2, ay)], MUTED, "ar", 1.2)

# 범례
LEG_Y = 424
d.legend(LEG_Y, [
    ("정상 완료 및 통과", OK),
    ("리소스 보존", INFO),
    ("조건 미달 잔류", WARN),
    ("업그레이드 차단 오류", BAD),
])

out_path = sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path(__file__).resolve().parent.parent / "Helm Hook.delete-policy.svg")
d.save(out_path)
print("ok gen-Helm Hook.delete-policy")
