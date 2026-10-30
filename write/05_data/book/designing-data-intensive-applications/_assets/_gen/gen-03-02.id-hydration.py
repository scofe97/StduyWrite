# 타입 스펙: type-sequence — 소셜 타임라인에서 ID만 캐시하고 읽기 시점에 게시물·사용자 저장소를 병렬 조회(hydrate)하는 시퀀스.
# 사실 출처: LIMIT 1000 은 노트 §4 SQL·원서 §Denormalization in the social networking case study. 저장소 명령·HTTP 경로는 원서에 없어 그리지 않는다.
# 노트 L120~L146(§4 소셜 타임라인의 ID hydration: post ID·sender ID만 구체화 타임라인에 저장, post ID로 본문·좋아요·답글 통계 가져옴, sender ID로 작성자 프로필·사진 가져옴, 애플리케이션 코드 조인, 병렬화 가능)
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import Seq, INK, MUTED, SOFT, RULE, ACC, OK, INFO, PAPER, PAPER2, KR, MONO

W = 880
LEG = 588
H = LEG + 56

class HydrationSeq(Seq):
    def lanes(self, names, y0=104, lane_w=210):
        LX = super().lanes([(nm, "") for nm, _ in names], y0, lane_w)
        for nm, sub in names:
            self.t(LX[nm], y0 + 37, sub, 11, MUTED, KR, "middle")
        return LX

    def seq_msg(self, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, is_mono=False):
        x1, x2 = self.LX[a], self.LX[b]
        d = 1 if x2 > x1 else -1
        self.path(f"M {x1 + 10 * d} {y} L {x2 - 12 * d} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        # 라벨 배경 마스크 (수직 레일 가림, 프레임 내부는 PAPER2, 외부는 PAPER)
        bg = PAPER2 if 288 <= y <= 476 else PAPER
        lw = sum(12 if '가' <= ch <= '힣' else 7.5 for ch in label) + 16
        self.o.append(f'<rect x="{mx - lw/2}" y="{y - 20}" width="{lw}" height="16" fill="{bg}"/>')
        self.t(mx, y - 8, label, 12, c, MONO if is_mono else KR, "middle", 600)
        if sub:
            sw = sum(11 if '가' <= ch <= '힣' else 7.0 for ch in sub) + 16
            self.o.append(f'<rect x="{mx - sw/2}" y="{y + 6}" width="{sw}" height="16" fill="{bg}"/>')
            self.t(mx, y + 18, sub, 11, MUTED, KR, "middle")

d = HydrationSeq(W, H, "03-02 · §4 ID HYDRATION", "소셜 타임라인의 ID 캐시와 읽기 시점 병렬 hydration",
                 "구체화 타임라인은 ID만 캐시하고, 읽기 시점에 게시물·사용자 저장소를 병렬 조회(hydrate)하여 최신 데이터를 결합한다.",
                 "빠르게 변하는 좋아요 수와 프로필 사진을 분리하고, 읽기 시점 애플리케이션 조인으로 결합합니다.")

# 5개 참여자 레인
lanes = [
    ("클라이언트", "타임라인 읽기"),
    ("타임라인 서비스", "애플리케이션 조인"),
    ("구체화 타임라인", "post ID · sender ID"),
    ("게시물 저장소", "본문 · 통계"),
    ("사용자 저장소", "프로필 · 사진"),
]

LX = d.lanes(lanes, y0=104, lane_w=140)
d.rails(564)

# 1. 클라이언트 요청 (y=168)
d.seq_msg("클라이언트", "타임라인 서비스", "타임라인 읽기 요청", 168, INK, "ar", sub=None)

# 2. 구체화 타임라인 ID 목록 조회 (y=216)
d.seq_msg("타임라인 서비스", "구체화 타임라인", "미리 계산된 ID 목록 조회", 216, OK, "ok", sub="LIMIT 1000")
d.seq_msg("구체화 타임라인", "타임라인 서비스", "post ID · sender ID 목록", 264, MUTED, "ar", dash="4 3", sub=None)

# 3. 병렬 hydration 프레임 (y=288 ~ 476)
fx1 = LX["타임라인 서비스"] - 48
fx2 = LX["사용자 저장소"] + 64
fw = fx2 - fx1
d.box(fx1, 288, fw, 188, PAPER2, INFO, 1.0)
d.box(fx1, 288, 150, 22, PAPER, INFO, 1.0)
d.t(fx1 + 75, 303, "PARALLEL [병렬 조회]", 11, INFO, KR, "middle", 600)

# 3-1. 게시물 조회 요청 및 응답
d.seq_msg("타임라인 서비스", "게시물 저장소", "post ID 로 본문 조회", 328, INFO, "info", sub="본문 · 좋아요·답글 수", is_mono=False)
d.seq_msg("게시물 저장소", "타임라인 서비스", "본문 · 최신 통계", 372, MUTED, "ar", dash="4 3", sub=None)

# 3-2. 사용자 프로필 조회 요청 및 응답
d.seq_msg("타임라인 서비스", "사용자 저장소", "sender ID 로 프로필 조회", 412, INFO, "info", sub="사용자명 · 프로필 사진", is_mono=False)
d.seq_msg("사용자 저장소", "타임라인 서비스", "최신 프로필", 456, MUTED, "ar", dash="4 3", sub=None)

# 4. 앱 계층 조인 결합 (y=492)
tx = LX["타임라인 서비스"]
d.tone(tx - 84, 492, 168, 28, ACC, 6, "18", 1.2)
d.t(tx, 510, "애플리케이션 코드 조인", 12, ACC, KR, "middle", 600)

# 5. 완성된 피드 반환 (y=544, focal ACC)
d.seq_msg("타임라인 서비스", "클라이언트", "hydrate 된 타임라인", 544, ACC, "acc", sub="최신 좋아요 수 · 프로필 사진", is_mono=False)

d.legend(LEG, [
    ("최종 응답 (focal)", ACC),
    ("ID 캐시 조회", OK),
    ("병렬 hydration 요청", INFO),
    ("데이터 반환 (응답)", MUTED)
])

d.save("03-02.id-hydration.svg")
