# 06-06 §3 — happens-before와 버전 번호를 이용한 동시 쓰기 감지 및 siblings 보존 시퀀스.
# 사실 출처: 06-06 본문 §3(L55~L66), DDIA 2판 Ch 6 Figure 6-15 (PDF p.53) — 장바구니 예제의 두 클라이언트 동시 쓰기, 버전 번호 기반 인과 판정, siblings 보존, 다중 레플리카 version vector 확장.
# 타입 스펙: type-sequence
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, OK, BAD, WARN, KR, MONO

W = 880
LEG = 736
H = LEG + 56

def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO

class VersionVectorSeq(Seq):
    def seq_msg(self, a, b, label, y, c=MUTED, mk="ar", dash=None, is_mono=False):
        x1, x2 = self.LX[a], self.LX[b]
        d = 1 if x2 > x1 else -1
        self.path(f"M {x1 + 10 * d} {y} L {x2 - 12 * d} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        self.t(mx, y - 8, label, 12, c, MONO if is_mono else KR, "middle", 600)

    def seq_state(self, a, txt, y, c, is_focal=False):
        x = self.LX[a]
        w = len(str(txt)) * 9.5 + 20
        if x - w / 2 < 24:
            x = 24 + w / 2
        elif x + w / 2 > W - 24:
            x = W - 24 - w / 2
        fill = f"{c}22" if not is_focal else f"{ACC}2a"
        stroke = c if not is_focal else ACC
        sw = 1.1 if not is_focal else 1.4
        self.o.append(f'<rect x="{x - w / 2}" y="{y - 11}" width="{w}" height="22" rx="4" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
        self.t(x, y + 5, txt, 11, c, KR, "middle", 600 if is_focal else 400)

d = VersionVectorSeq(W, H, "06-06 §3 · HAPPENS-BEFORE & SIBLINGS", "동시 쓰기 감지와 장바구니 siblings 보존 시퀀스",
                     "두 클라이언트의 동시 쓰기 발생 시 인과 관계를 추적해 옛 값을 덮어쓰고 동시 값(siblings)을 보존한다.",
                     "happens-before 인과 판정 · 버전 번호 추적 · siblings 생성 · 다중 레플리카 version vector")

lanes = [
    ("클라이언트 1", "Client 1"),
    ("서버 (장바구니)", "Server (cart key)"),
    ("클라이언트 2", "Client 2"),
]
LX = d.lanes(lanes, y0=104, lane_w=210)
d.rails(616)

# Step 1: 클라이언트 1이 milk 추가 (초기 쓰기)
d.seq_msg("클라이언트 1", "서버 (장바구니)", "add milk (기반 버전 없음)", 168, INFO, "info", is_mono=False)
d.seq_state("서버 (장바구니)", "v1: [milk] 저장", 196, INFO)
d.seq_msg("서버 (장바구니)", "클라이언트 1", "반환: v1, [milk]", 228, MUTED, "ar", dash="4 3", is_mono=False)

# Step 2: 클라이언트 2가 동시에 eggs 추가 (동시 쓰기 발생)
d.seq_msg("클라이언트 2", "서버 (장바구니)", "add eggs (기반 버전 없음)", 272, WARN, "warn", is_mono=False)
d.seq_state("서버 (장바구니)", "동시 쓰기 감지 (v2: eggs, v1: milk)", 304, WARN)
d.seq_msg("서버 (장바구니)", "클라이언트 2", "반환: v2, siblings {[milk], [eggs]}", 344, MUTED, "ar", dash="4 3", is_mono=False)

# Step 3: 클라이언트 1이 flour 추가 (v1 기반 쓰기 - 인과 선행 및 덮어쓰기)
d.seq_msg("클라이언트 1", "서버 (장바구니)", "add flour (기반 버전: v1)", 388, ACC, "acc", is_mono=False)
d.seq_state("서버 (장바구니)", "v1 덮어쓰기 · v2 유지 (동시 siblings)", 420, ACC, is_focal=True)
d.seq_msg("서버 (장바구니)", "클라이언트 1", "반환: v3, siblings {[milk, flour], [eggs]}", 460, MUTED, "ar", dash="4 3", is_mono=False)

# Step 4: 클라이언트 2가 병합 후 ham 추가 (v2 기반 쓰기)
d.seq_msg("클라이언트 2", "서버 (장바구니)", "merge + add ham: [eggs, milk, ham] (기반: v2)", 504, OK, "ok", is_mono=False)
d.seq_state("서버 (장바구니)", "v2 덮어쓰기 · v3 유지 (병합 갱신)", 536, OK)
d.seq_msg("서버 (장바구니)", "클라이언트 2", "반환: v4, siblings {[milk, flour], [eggs, milk, ham]}", 576, MUTED, "ar", dash="4 3", is_mono=False)

# 5. 다중 레플리카 확장 설명 카드
CY = 624
CW = W - 64
CH = 88
d.box(32, CY, CW, CH, PAPER2, RULE, 1.0, r=6)
d.t(32 + CW / 2, CY + 22, "다중 레플리카 확장: Version Vector (버전 벡터)", 13, INK, KR, "middle", 600)
d.line(44, CY + 32, 32 + CW - 12, CY + 32, RULE, 0.8)

d.t(48, CY + 52, "레플리카별 버전 번호:", 12, ACC, KR, "start", 600)
d.t(210, CY + 52, "단일 버전 번호 대신 레플리카·키별 버전 번호 모음으로 추적", 11, INK, KR, "start")

d.t(48, CY + 72, "인과 문맥 전달:", 12, OK, KR, "start", 600)
d.t(210, CY + 72, "클라이언트 경유 전달로 덮어쓰기와 동시 쓰기(siblings) 구분", 11, MUTED, KR, "start")

d.legend(LEG, [
    ("인과 갱신·병합", OK),
    ("siblings 분기 (focal)", ACC),
    ("정상 쓰기·요청", INFO),
    ("동시 쓰기 감지", WARN),
])
d.save("06-06.version-vector.svg")
