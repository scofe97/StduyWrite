# 05-01 §2 — 롤링 업그레이드 환경의 backward·forward 호환성과 미지 필드(photoURL) 소실 위험 시퀀스.
# 사실 출처: 05-01 §2(L52~L61), 원서 Ch.5 서두 backward·forward 정의(PDF p.2)와 Figure 5-1(PDF p.3, Person·favoriteNumber 42 갱신·photoURL 소실)
# 타입 스펙: type-sequence
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
LEG = 788
H = LEG + 56

class CompSeq(Seq):
    def lanes(self, names, y0=104, lane_w=210):
        # dd.Seq.lanes 는 부제를 MONO 로 찍는다. 한글 부제는 KR 로 갈라 쓴다(계약 §프리미티브가 한글을 mono 로).
        self.LX = {}; n = len(names)
        span = (self.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            self.LX[nm] = x
            self.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            self.t(x, y0 + 20, nm, 12, INK, KR, "middle", 600)
            self.t(x, y0 + 37, sub, 11, MUTED, KR if any("가" <= ch <= "힣" for ch in sub) else MONO)
        self.lane_top = y0 + 44
        return self.LX

    def seq_msg(self, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, is_mono=False):
        x1, x2 = self.LX[a], self.LX[b]
        d = 1 if x2 > x1 else -1
        self.path(f"M {x1 + 10 * d} {y} L {x2 - 12 * d} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        self.t(mx, y - 8, label, 12, c, MONO if is_mono else KR, "middle", 600)
        if sub:
            self.t(mx, y + 16, sub, 12, MUTED, KR, "middle")

    def seq_self(self, a, label, y, c=MUTED, sub=None, to_left=False):
        x = self.LX[a]
        if to_left:
            self.path(f"M {x - 10} {y - 10} L {x - 58} {y - 10} L {x - 58} {y + 10} L {x - 13} {y + 10}", c, 1.4, m="ar")
            self.t(x - 68, y - 4, label, 12, c, KR, "end", 600)
            if sub:
                self.t(x - 68, y + 15, sub, 12, MUTED, KR, "end")
        else:
            self.path(f"M {x + 10} {y - 10} L {x + 58} {y - 10} L {x + 58} {y + 10} L {x + 13} {y + 10}", c, 1.4, m="ar")
            self.t(x + 68, y - 4, label, 12, c, KR, "start", 600)
            if sub:
                self.t(x + 68, y + 15, sub, 12, MUTED, KR, "start")

d = CompSeq(W, H, "05-01 · BACKWARD & FORWARD COMPATIBILITY", "호환성 두 방향과 미지 필드 소실 위험 시퀀스",
            "새 코드가 옛 데이터를 읽는 backward 호환과 옛 코드가 새 데이터를 읽는 forward 호환의 미지 필드 보존 분기.",
            "backward 호환 판독 · forward 호환 읽기 · 미지 필드 소실 위험 · 미지 필드 명시 보존")

lanes = [
    ("새 코드 (v2)", "신규 버전 배포 노드"),
    ("공용 데이터베이스 (DB)", "공유 영속 저장소"),
    ("옛 코드 (v1)", "롤링 업그레이드 대기 노드"),
]
LX = d.lanes(lanes, y0=104, lane_w=196)
d.rails(768)

# --- Phase 1: backward(하위) 호환성 ---
d.tone(24, 156, 260, 24, OK, 4, "18", 1.0)
d.t(154, 172, "Phase 1: backward 호환 (하위 호환)", 12, OK, KR, "middle", 600)

d.seq_msg("옛 코드 (v1)", "공용 데이터베이스 (DB)", "옛 레코드 쓰기", 208, INFO, "info", sub="기존 형식 데이터 기록", is_mono=False)
d.seq_msg("공용 데이터베이스 (DB)", "새 코드 (v2)", "옛 레코드 읽기", 252, OK, "ok", dash="4 3", sub="옛 데이터 반환 (신규 필드 부재)", is_mono=False)
d.seq_self("새 코드 (v2)", "옛 스키마 명시 처리", 296, OK, sub="새 코드가 옛 형식을 알아 처리", to_left=False)

# --- Phase 2: forward(상위) 호환성과 미지 필드 소실 위험 (FOCAL) ---
d.tone(24, 336, 328, 24, ACC, 4, "20", 1.2)
d.t(188, 352, "Phase 2: forward 호환과 미지 필드 분기", 12, ACC, KR, "middle", 600)

# 새 코드가 신규 필드 photoURL 포함 레코드 작성
d.seq_msg("새 코드 (v2)", "공용 데이터베이스 (DB)", "새 레코드 쓰기 (photoURL 포함)", 388, ACC, "acc", sub="신규 필드 담긴 레코드 영속화", is_mono=False)

# 옛 코드가 새 레코드 읽기
d.seq_msg("공용 데이터베이스 (DB)", "옛 코드 (v1)", "새 레코드 읽기", 432, INFO, "info", dash="4 3", sub="신규 photoURL 필드 포함 데이터 수신", is_mono=False)

# 옛 코드가 모델 객체로 디코딩 (미지 필드 인식 불가, 오른쪽 레인이므로 왼쪽으로 루프)
d.seq_self("옛 코드 (v1)", "Person 객체 디코딩", 476, INFO, sub="옛 코드는 photoURL 필드를 모름", to_left=True)

# --- ALT 프레임: 미지 필드 처리 분기 ---
fx = 280
fw = 580
fy = 520
fh = 240

d.box(fx, fy, fw, fh, PAPER2, RULE, 1.0)
# Operator Tab
d.box(fx, fy, 48, 20, PAPER, RULE, 1.0)
d.t(fx + 24, fy + 14, "ALT", 9, MUTED, MONO, "middle", 600)

# Guard 1: 미지 필드 미보존 (소실 위험)
d.t(fx + 60, fy + 15, "[미지 필드 미보존 모델: 데이터 손실 위험]", 12, BAD, KR, "start", 600)

d.seq_msg("옛 코드 (v1)", "공용 데이터베이스 (DB)", "favoriteNumber 갱신 재작성", 568, BAD, "bad", sub="photoURL 필드가 누락된 채 쓰기 실행", is_mono=False)
d.tone(LX["공용 데이터베이스 (DB)"] - 116, 596, 232, 24, BAD, 4, "22", 1.0)
d.t(LX["공용 데이터베이스 (DB)"], 612, "photoURL 값 소실 (데이터 손실)", 12, BAD, KR, "middle")

# Region Divider
d.line(fx + 8, 636, fx + fw - 8, 636, RULE, 1.0, dash="4 3")

# Guard 2: 미지 필드 명시 보존 (바람직한 동작)
d.t(fx + 16, 654, "[미지 필드 명시 보존: 바람직한 동작]", 12, OK, KR, "start", 600)

d.seq_msg("옛 코드 (v1)", "공용 데이터베이스 (DB)", "favoriteNumber 갱신 재작성", 688, OK, "ok", sub="해석 못 한 photoURL 바이트 그대로 보존", is_mono=False)
d.tone(LX["공용 데이터베이스 (DB)"] - 116, 716, 232, 24, OK, 4, "20", 1.0)
d.t(LX["공용 데이터베이스 (DB)"], 732, "photoURL 보존", 12, OK, KR, "middle")

d.legend(LEG, [("신규 필드 기록 (focal)", ACC), ("데이터 손실 위험", BAD), ("호환 성공·필드 보존", OK), ("저장소 읽기·쓰기", INFO)])
d.save("05-01.compatibility.svg")
