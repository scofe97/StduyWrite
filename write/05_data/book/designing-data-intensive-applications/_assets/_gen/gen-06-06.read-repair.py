# 06-06 §1 — 노드가 죽었을 때의 병렬 쓰기와 복귀 후 stale 읽기, 그리고 read repair로 최신 버전 되쓰기.
# 사실 출처: 06-06 본문 §1(L27~L37), DDIA 2판 Ch 6 Figure 6-12 (PDF p.41) — user 1234 병렬 쓰기(노드3 다운), user 2345 병렬 읽기(v6 stale 감지), read repair로 노드3에 v7 되쓰기.
# 타입 스펙: type-sequence
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, OK, BAD, WARN, KR, MONO

W = 880
LEG = 636
H = LEG + 56

def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO

class ReadRepairSeq(Seq):
    def seq_msg(self, a, b, label, y, c=MUTED, mk="ar", dash=None, is_mono=False):
        x1, x2 = self.LX[a], self.LX[b]
        d = 1 if x2 > x1 else -1
        self.path(f"M {x1 + 10 * d} {y} L {x2 - 12 * d} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        self.t(mx, y - 8, label, 12, c, MONO if is_mono else KR, "middle", 600)

    def seq_chip(self, a, txt, y, c, is_focal=False):
        x = self.LX[a]
        # 글자수에 맞게 너비 산출, 한글 1글자 12px
        w = len(str(txt)) * 10.0 + 16
        # 화면 경계 이탈 방지
        if x - w / 2 < 24:
            x = 24 + w / 2
        elif x + w / 2 > W - 24:
            x = W - 24 - w / 2
        fill = f"{c}22" if not is_focal else f"{ACC}2a"
        stroke = c if not is_focal else ACC
        sw = 1.1 if not is_focal else 1.4
        self.o.append(f'<rect x="{x - w / 2}" y="{y - 11}" width="{w}" height="22" rx="4" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
        self.t(x, y + 5, txt, 11, c, KR, "middle", 600 if is_focal else 400)

    def banner(self, y, txt, c, is_focal=False):
        x = 32
        w = W - 64
        fill = f"{c}1c" if not is_focal else f"{ACC}26"
        stroke = c if not is_focal else ACC
        sw = 1.1 if not is_focal else 1.4
        self.o.append(f'<rect x="{x}" y="{y - 12}" width="{w}" height="24" rx="4" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
        self.t(W / 2, y + 4, txt, 12, c, KR, "middle", 600)

d = ReadRepairSeq(W, H, "06-06 §1 · READ REPAIR SEQUENCE", "노드 다운 쓰기와 복귀 후 읽기 복구 시퀀스",
                  "레플리카 장애 중 성공한 병렬 쓰기 후, 복귀 노드에서 stale 값을 감지해 최신 버전을 되쓰는 과정을 보인다.",
                  "병렬 쓰기 수용 (w=2) · 노드 장애 복귀 · 병렬 읽기 (r=2) · 최신 버전 읽기 복구")

lanes = [
    ("클라이언트", "user 1234 · 2345"),
    ("레플리카 1", "Replica 1 (가용)"),
    ("레플리카 2", "Replica 2 (가용)"),
    ("레플리카 3", "Replica 3 (장애 후 복귀)"),
]
LX = d.lanes(lanes, y0=104, lane_w=176)
d.rails(612)

# 1. 쓰기 단계 (user 1234, w=2)
d.seq_msg("클라이언트", "레플리카 1", "set 'me-new.jpg' v7", 172, MUTED, "ar", is_mono=True)
d.seq_msg("레플리카 1", "클라이언트", "OK", 200, OK, "ok", dash="4 3")

d.seq_msg("클라이언트", "레플리카 2", "set 'me-new.jpg' v7", 228, MUTED, "ar", is_mono=True)
d.seq_msg("레플리카 2", "클라이언트", "OK", 256, OK, "ok", dash="4 3")

d.seq_msg("클라이언트", "레플리카 3", "쓰기 놓침 (노드 오프라인)", 284, BAD, "bad", dash="2 3")
d.seq_chip("레플리카 3", "노드 오프라인 ('me-old.jpg' v6 유지)", 312, BAD)

# 클라이언트 쓰기 성공 배너
d.banner(344, "OK 2개 수신 · 쓰기 성공으로 간주 (w=2)", OK)

# 2. 노드 3 복귀 및 읽기 단계 (user 2345, r=2)
d.seq_chip("레플리카 3", "노드 복귀 (v6 stale 상태)", 380, WARN)

d.seq_msg("클라이언트", "레플리카 1", "get picture_url", 414, MUTED, "ar", is_mono=True)
d.seq_msg("레플리카 1", "클라이언트", "'me-new.jpg' v7 (최신)", 438, OK, "ok", dash="4 3")

d.seq_msg("클라이언트", "레플리카 3", "get picture_url", 466, MUTED, "ar", is_mono=True)
d.seq_msg("레플리카 3", "클라이언트", "'me-old.jpg' v6 (옛 값)", 490, WARN, "warn", dash="4 3")

# stale 감지 배너 (focal)
d.banner(524, "버전 비교 (v7 > v6) · 최신 채택 및 Replica 3 stale 감지", ACC, is_focal=True)

# 3. Read Repair (읽기 복구)
d.seq_msg("클라이언트", "레플리카 3", "set 'me-new.jpg' v7 (read repair)", 560, ACC, "acc", is_mono=True)
d.seq_msg("레플리카 3", "클라이언트", "OK", 586, OK, "ok", dash="4 3")
d.seq_chip("레플리카 3", "최신 값으로 따라잡음 (v7)", 610, OK)

d.legend(LEG, [
    ("최신 쓰기·동기화 완료", OK),
    ("stale 상태·옛 값", WARN),
    ("노드 다운·쓰기 누락", BAD),
    ("read repair (focal)", ACC),
])
d.save("06-06.read-repair.svg")
