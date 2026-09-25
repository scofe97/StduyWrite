# 05-03 실습 편 — 묶음 하나의 단계 흐름을 그리는 공용 틀. 위 줄은 단계 카드(하는 일), 아래 줄은 그 단계가 겨누는 어긋난 예측.
# 타입 스펙: type-flowchart — 단계를 실행 순서대로 같은 간격으로 잇는다. focal 은 Phase 1 에서 "잘못 알던 인과"로 분류된 축을 겨누는 단계.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, WARN, PAPER2, RULE, KR, MONO

def kr(s): return KR if any("가" <= c <= "힣" for c in str(s)) else MONO

def bundle(fname, eyebrow, title, desc, lead, steps, legend, per_row=4):
    """steps: (번호, 제목, 하는 일 1, 하는 일 2, 겨누는 축, focal, extra(책 밖 확장))"""
    CW, CH, GAP, X0 = 196, 118, 22, 24
    TAG_H, ROW, Y0 = 46, 118 + 46 + 40, 104
    rows = (len(steps) + per_row - 1) // per_row
    H = Y0 + rows * ROW + 40
    W = X0 * 2 + per_row * CW + (per_row - 1) * GAP
    d = D(W, H, eyebrow, title, desc, lead)
    for i, (num, t, l1, l2, axis, focal, extra) in enumerate(steps):
        r, c = divmod(i, per_row)
        x = X0 + c * (CW + GAP); y = Y0 + r * ROW
        col = ACC if focal else (INFO if extra else INK)
        d.box(x, y, CW, CH, PAPER2, col if (focal or extra) else RULE, 1.4 if focal else 1, 8)
        d.t(x + 14, y + 24, num, 12, MUTED, MONO, "start")
        if extra: d.t(x + CW - 14, y + 24, "책 밖", 11, INFO, KR, "end")
        d.t(x + CW / 2, y + 52, t, 14, col, KR, "middle", 600)
        d.t(x + CW / 2, y + 78, l1, 12, MUTED, kr(l1))
        d.t(x + CW / 2, y + 100, l2, 12, MUTED, kr(l2))
        # 아래 줄: 이 단계가 겨누는 Phase 1 의 어긋난 축
        d.tone(x, y + CH + 10, CW, TAG_H, ACC if focal else WARN, 6, "10", 1.0)
        d.t(x + 12, y + CH + 27, "겨누는 축", 11, SOFT, KR, "start")
        d.t(x + CW / 2, y + CH + 46, axis, 12, ACC if focal else WARN, kr(axis), "middle", 600)
        if c < per_row - 1 and i < len(steps) - 1:
            d.arrow([(x + CW + 4, y + CH / 2), (x + CW + GAP - 4, y + CH / 2)], MUTED, "ar", 1.4)
        elif i < len(steps) - 1:
            # 줄 바꿈: 마지막 카드 아래로 내려가 다음 줄 첫 카드로 ㄷ자 우회
            ny = y + ROW
            d.arrow([(x + CW / 2, y + CH + TAG_H + 14), (x + CW / 2, ny - 14), (X0 + CW / 2, ny - 14), (X0 + CW / 2, ny - 4)], MUTED, "ar", 1.4)
    d.legend(H - 40, legend)
    d.save(fname)
