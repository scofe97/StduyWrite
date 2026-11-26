# 타입 스펙: type-sequence
# 01-01 ### Shadow — 실요청 v1 응답 반환과 v2 비동기 미러 복제·응답 폐기·결과 비교 시퀀스
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import (Seq, PAPER, PAPER2, INK, MUTED, RULE, ACC,  # noqa: E402
                OK, WARN, BAD, INFO, KR, MONO)


def _fam(txt):
    return KR if any("가" <= ch <= "힣" for ch in str(txt)) else MONO


class KrSeq(Seq):
    """dd.Seq 서브클래스 — 한글 라벨에 KR 스택을 쓰고 비동기 오픈 화살표와 간격 배치를 지원한다."""

    def __init__(self, w, h, eyebrow, title, desc, lead=None):
        super().__init__(w, h, eyebrow, title, desc, lead=lead)
        # fire-and-forget 비동기 메시지용 오픈(속이 빈) 화살표 마커를 <defs> 닫기 직전에 삽입
        defs_end = self.o.index("</defs>")
        open_markers = [
            f'<marker id="acc-open" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto">'
            f'<polyline points="0,1 7,4 0,7" fill="none" stroke="{ACC}" stroke-width="1.3"/></marker>',
            f'<marker id="info-open" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto">'
            f'<polyline points="0,1 7,4 0,7" fill="none" stroke="{INFO}" stroke-width="1.3"/></marker>',
        ]
        self.o[defs_end:defs_end] = open_markers

    def lanes(self, names, y0=96, lane_w=152, x0=24, stride=188):
        self.LX = {}
        for i, (nm, sub) in enumerate(names):
            cx = x0 + lane_w // 2 + i * stride
            self.LX[nm] = cx
            self.box(cx - lane_w // 2, y0, lane_w, 48, PAPER2, RULE, 1.0)
            self.t(cx, y0 + 20, nm, 13, INK, _fam(nm), "middle", 600)
            self.t(cx, y0 + 38, sub, 12, MUTED, _fam(sub), "middle")
        self.lane_top = y0 + 48
        return self.LX

    def act(self, a, y1, y2):
        cx = self.LX[a]
        self.o.append(
            f'<rect x="{cx - 4}" y="{y1}" width="8" height="{y2 - y1}" '
            f'rx="2" fill="{PAPER2}" stroke="{MUTED}" stroke-width="0.8"/>'
        )

    def msg(self, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, lx=None):
        x1, x2 = self.LX[a], self.LX[b]
        d_dir = 1 if x2 > x1 else -1
        self.path(f"M {x1 + 4 * d_dir} {y} L {x2 - 5 * d_dir} {y}", c, 1.5, m=mk, dash=dash)
        mx = lx if lx is not None else (x1 + x2) // 2
        lfam = _fam(label)
        lsize = 13 if lfam == KR else 12
        self.t(mx, y - 10, label, lsize, c, lfam, "middle", 600)
        if sub:
            sfam = _fam(sub)
            ssize = 13 if sfam == KR else 12
            self.t(mx, y + 18, sub, ssize, MUTED, sfam, "middle")


W = 960
LEGEND_Y = 532
H = LEGEND_Y + 44  # 576 (margin = 576 - (532+24) = 20 >= 16)

d = KrSeq(
    W,
    H,
    "SEQUENCE · SHADOW TRAFFIC MIRRORING",
    "Shadow 요청 복제와 응답 폐기 시퀀스",
    "Istio mirror 프록시가 실트래픽을 v1으로 보내 응답을 반환하고, 같은 요청을 -shadow 헤더로 v2에 비동기 복제해 응답을 폐기한 뒤 결과를 비교하는 시퀀스",
    lead="프록시가 실요청은 v1 으로 응답하고 복제본은 v2 로 비동기 전송해 응답을 버린 뒤 결과를 비교합니다",
)

# ── 참여자 레인 ────────────────────────────────────────────────────────
actors = [
    ("사용자", "Client"),
    ("프록시", "Istio mirror"),
    ("v1 운영", "subset: v1"),
    ("v2 섀도", "subset: v2"),
    ("결과 비교", "로그 · 지표"),
]
LX = d.lanes(actors, y0=96, lane_w=152, x0=24, stride=188)
d.rails(516)

# ── 활성 막대 (Activation bars, z-order: 메시지 뒤) ─────────────────────
d.act("프록시", 172, 356)
d.act("v1 운영", 216, 320)
d.act("v2 섀도", 260, 320)
d.act("v2 섀도", 388, 424)
d.act("결과 비교", 444, 504)

# ── 메시지 교환 (시간순 위 -> 아래) ────────────────────────────────────
# 1. 사용자 -> 프록시 (실요청)
d.msg("사용자", "프록시", "요청 전송", 180, INFO, mk="info", sub="my-api")

# 2. 프록시 -> v1 (실트래픽 100%)
d.msg("프록시", "v1 운영", "weight: 100", 224, INFO, mk="info", sub="실트래픽 전달")

# 3. 프록시 -> v2 (비동기 fire-and-forget 복제, Focal ACC)
# 라벨은 v1-v2 사이 빈 간격에 두어 v1 생명선을 가리지 않는다
gap_v1_v2 = (LX["v1 운영"] + LX["v2 섀도"]) // 2
d.msg(
    "프록시",
    "v2 섀도",
    "mirror 100%",
    268,
    ACC,
    mk="acc-open",
    dash="5 4",
    sub="Host: -shadow",
    lx=gap_v1_v2,
)

# 4. v1 -> 프록시 (실응답 반환 — Return: dashed + filled)
d.msg("v1 운영", "프록시", "v1 처리 응답", 312, OK, mk="ok", dash="5 3")

# 5. 프록시 -> 사용자 (실사용자 응답 반환 — Return: dashed + filled)
d.msg("프록시", "사용자", "v1 응답 반환", 348, OK, mk="ok", dash="5 3", sub="실사용자 100%")

# 6. 쓰기 요청 복제 중복 변경 경고 칩 (v2 처리 직후, 활성 막대 밖 여유 공간)
cx_v2 = LX["v2 섀도"]
chip_w, chip_h = 224, 24
d.o.append(
    f'<rect x="{cx_v2 - chip_w // 2}" y="{352 - chip_h // 2}" width="{chip_w}" height="{chip_h}" '
    f'rx="6" fill="{PAPER}" stroke="{WARN}" stroke-width="1.2"/>'
)
d.t(cx_v2, 356, "쓰기 복제 · 데이터 중복 위험", 13, WARN, KR, "middle", 600)

# 7. v2 응답 폐기 (프록시 방향 점선 + X 폐기 표지)
drop_x = LX["v2 섀도"] - 136
drop_y = 408
d.path(f"M {LX['v2 섀도'] - 4} {drop_y} L {drop_x + 8} {drop_y}", BAD, 1.5, dash="5 3")
d.line(drop_x - 6, drop_y - 6, drop_x + 6, drop_y + 6, BAD, 2.0)
d.line(drop_x - 6, drop_y + 6, drop_x + 6, drop_y - 6, BAD, 2.0)
drop_lx = (LX["v2 섀도"] - 12 + drop_x) // 2
d.t(drop_lx, drop_y - 10, "v2 응답 폐기", 13, BAD, KR, "middle", 600)
d.t(drop_lx, drop_y + 18, "fire-and-forget", 12, MUTED, MONO, "middle")

# 8. v1 & v2 결과 기록 -> 결과 비교 (비동기 로그·지표 전송)
gap_v2_cmp = (LX["v2 섀도"] + LX["결과 비교"]) // 2
d.msg("v1 운영", "결과 비교", "v1 결과 기록", 456, INFO, mk="info-open", dash="4 4", lx=gap_v2_cmp)
d.msg("v2 섀도", "결과 비교", "v2 결과 대조", 492, INFO, mk="info-open", dash="4 4", lx=gap_v2_cmp)

# ── 범례 ───────────────────────────────────────────────────────────────
d.legend(
    LEGEND_Y,
    [
        ("실트래픽 · 비교", INFO),
        ("v1 응답 반환", OK),
        ("미러 복제", ACC),
        ("쓰기 중복 경고", WARN),
        ("v2 응답 폐기", BAD),
    ],
)

out_path = sys.argv[1] if len(sys.argv) > 1 else "01-01.shadow-mirror-sequence.svg"
d.save(out_path)
print(f"saved: {out_path}")
