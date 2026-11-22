# 사실 출처: 06-02.빌드 격리와 공격 표면.md 74~92행
# 타입 스펙: type-sequence
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import Seq, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO

def _w(txt, size):
    return sum(size * (1.0 if "가" <= c <= "힣" else 0.62) for c in str(txt)) + 12

class SeqCustom(Seq):
    def lanes_custom(s, names, y0=96, lane_w=180):
        s.LX = {}
        for nm, sub, x in names:
            s.LX[nm] = x
            s.box(x - lane_w // 2, y0, lane_w, 44, PAPER2, RULE, 1.0, 6)
            s.t(x, y0 + 19, nm, 12, INK, KR, "middle", 600)
            s.t(x, y0 + 35, sub, 11, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX

    def act(s, who, y_top, h):
        x = s.LX[who]
        s.o.append(f'<line x1="{x}" y1="{y_top}" x2="{x}" y2="{y_top + h}" stroke="rgba(245,245,243,0.08)" stroke-width="8"/>')
        s.o.append(f'<line x1="{x - 4}" y1="{y_top}" x2="{x - 4}" y2="{y_top + h}" stroke="{MUTED}" stroke-width="0.8"/>')
        s.o.append(f'<line x1="{x + 4}" y1="{y_top}" x2="{x + 4}" y2="{y_top + h}" stroke="{MUTED}" stroke-width="0.8"/>')

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, sub_c=MUTED):
        x1, x2 = s.LX[a], s.LX[b]
        d = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 8 * d} {y} L {x2 - 10 * d} {y}", c, 1.4, m=mk, dash=dash)
        mx = (x1 + x2) // 2
        # 라벨 배경
        lw = _w(label, 12)
        s.o.append(f'<rect x="{mx - lw/2}" y="{y - 21}" width="{lw}" height="17" rx="3" fill="{PAPER}"/>')
        s.t(mx, y - 8, label, 12, c, _kr(label), "middle", 600)
        if sub:
            sw = _w(sub, 11)
            s.o.append(f'<rect x="{mx - sw/2}" y="{y + 6}" width="{sw}" height="17" rx="3" fill="{PAPER}"/>')
            s.t(mx, y + 18, sub, 11, sub_c, _kr(sub))

    def selfmsg(s, a, label, y, c=MUTED, sub=None):
        x = s.LX[a]
        s.path(f"M {x + 8} {y - 12} L {x + 44} {y - 12} L {x + 44} {y + 12} L {x + 10} {y + 12}", c, 1.4, m="ar")
        lw = _w(label, 12)
        s.o.append(f'<rect x="{x + 52}" y="{y - 17}" width="{lw}" height="17" rx="3" fill="{PAPER}"/>')
        s.t(x + 52 + lw//2, y - 4, label, 12, c, _kr(label), "middle", 600)
        if sub:
            sw = _w(sub, 11)
            s.o.append(f'<rect x="{x + 52}" y="{y + 6}" width="{sw}" height="17" rx="3" fill="{PAPER}"/>')
            s.t(x + 52 + sw//2, y + 18, sub, 11, MUTED, _kr(sub))

W, H = 960, 560

d = SeqCustom(
    W, H,
    "JENKINS · FORK PR CREDENTIAL ATTACK PATH",
    "외부 기여 PR 과 시크릿 유출 경로",
    "비특권 사용자의 fork PR 에서 테스트 코드 수정을 통한 SCM 자격증명 탈취 및 단계별 방어 지점",
    lead="공격자는 Jenkinsfile 이 아닌 테스트 코드를 수정해 sh 스텝에 바인딩된 SCM 자격증명을 탈취합니다."
)

# 1. 4개 참여자 레인 정의
LANES = [
    ("외부 기여자 (fork)", "비특권 사용자", 152),
    ("원 저장소 Jenkinsfile", "sh 스텝 바인딩", 380),
    ("Jenkins 빌드", "Multibranch Pipeline", 612),
    ("자격증명", "SCM 스캔 자격증명", 840),
]
d.lanes_custom(LANES, y0=96, lane_w=176)

# 2. 레일 (수직 점선)
d.rails(472)

# 3. 액티베이션 바
d.act("외부 기여자 (fork)", 156, 28)
d.act("원 저장소 Jenkinsfile", 168, 140)
d.act("Jenkins 빌드", 220, 248)
d.act("자격증명", 276, 188)

# ── 4. 시퀀스 메시지 (본문 3절 공격 단계 1~3 및 방어 지점) ─────────────────

# 단계 1: 외부 기여자 PR 작성 (공격자는 Jenkinsfile 대신 테스트 코드 수정)
d.msg("외부 기여자 (fork)", "원 저장소 Jenkinsfile", "1. PR 작성 (테스트 코드 수정)", 176, WARN, "warn",
      sub="방어: Jenkinsfile 중앙화 (Inline Definition)", sub_c=OK)

# 단계 2: 원 저장소 Multibranch Pipeline 이 PR 감지 및 빌드 시작
d.msg("원 저장소 Jenkinsfile", "Jenkins 빌드", "2. PR 자동 감지 및 빌드 실행", 232, INFO, "info",
      sub="Multibranch Pipeline 브랜치·PR 감지")

# 단계 2-1: Jenkinsfile 이 sh 스텝에 자격증명 바인딩
d.msg("원 저장소 Jenkinsfile", "자격증명", "sh 스텝에 자격증명 바인딩", 288, MUTED, "ar",
      sub="방어: 권한 줄이기 (웹훅 등 최소 권한)", sub_c=OK)

# 단계 2-2: Jenkins 빌드가 수정된 테스트 코드 실행 (self-message)
d.selfmsg("Jenkins 빌드", "수정된 테스트 코드 실행", 344, WARN, sub="에이전트 sh 스텝 내 테스트 수행")

# 단계 3 [FOCAL]: 수정된 테스트 코드가 바인딩된 자격증명을 읽음 (탈취)
d.msg("Jenkins 빌드", "자격증명", "3. 바인딩된 자격증명 탈취", 400, ACC, "acc",
      sub="수정된 테스트가 SCM 자격증명 직접 읽기", sub_c=ACC)

# 단계 3-1: 탈취된 자격증명으로 다른 저장소 접근 위험 노출
d.msg("자격증명", "외부 기여자 (fork)", "다른 저장소 접근 위험 노출", 456, BAD, "bad", dash="4 3",
      sub="방어: 자격증명 범위 분리 (저장소별 토큰)", sub_c=OK)

# ── 5. 범례 ─────────────────────────────────────────────────────────────
LEG_Y = 504
d.legend(LEG_Y, [
    ("자격증명 탈취", ACC),
    ("공격 단계", WARN),
    ("정상 빌드", INFO),
    ("유출 위험", BAD),
    ("방어책", OK),
])

out_path = sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path(__file__).resolve().parent.parent / "06-02.fork-pr-credential.svg")
d.save(out_path)
print(f"saved: {out_path}")
