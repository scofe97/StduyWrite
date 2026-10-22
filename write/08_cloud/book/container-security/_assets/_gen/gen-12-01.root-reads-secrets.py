# 타입 스펙: type-sequence — 가운데 호스트 root 가 왼쪽 파일시스템에서는 tmpfs 경로를 찾아 파일을 열고, 오른쪽 /proc 에서는 PID 를 찾아 environ 을 읽어 시크릿을 얻는다. 두 경로가 같은 행에서 나란히 진행된다. focal 은 시크릿이 드러나는 두 응답.
# 사실 출처: 노트 L190~L198(mount -t tmpfs 출력, 경로로 접근), L200~L212(ps -C sh, sudo cat /proc/<PID>/environ, SECRET=mysecret), L216~L226(컨테이너 안 root 가 호스트 root)
# Layout conventions: 레인 셋 폭 212(root 가 가운데), 메시지 stride 72(y=212·284·356·428), 레인 머리 y=104, 상태 칩 y=508. 모든 좌표 4의 배수.
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import Seq, INK, MUTED, SOFT, RULE, ACC, INFO, PAPER, PAPER2, KR, MONO


def kr(t):
    return KR if any("가" <= c <= "힣" for c in str(t)) else MONO


class SeqKR(Seq):
    """계약 §프리미티브가 한글을 mono 로 내보내는 자리를 한글 스택·13/12px 로 바꾼다."""
    def lanes(s, names, y0=104, lane_w=210):
        s.LX = {}; n = len(names)
        span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 14, INK, kr(nm), "middle", 600)
            s.t(x, y0 + 37, sub, 12, MUTED, kr(sub))
        s.lane_top = y0 + 44
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dr = 1 if x2 > x1 else -1
        s.path(f"M {x1+10*dr} {y} L {x2-12*dr} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 13, c, kr(label), "middle", 600)
        if sub: s.t(mx, y + 17, sub, 12, MUTED, kr(sub))

    def state(s, a, txt, y, c):
        x = s.LX[a]
        w = sum(12 if "가" <= ch <= "힣" else 7.4 for ch in txt) + 24
        s.o.append(f'<rect x="{x-w/2}" y="{y-12}" width="{w}" height="24" rx="4" fill="{PAPER}"/>')
        s.o.append(f'<rect x="{x-w/2}" y="{y-12}" width="{w}" height="24" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 4, txt, 12, c, kr(txt))


W, H = 960, 596
d = SeqKR(W, H, "SEQUENCE · 12-01 §4",
          "호스트 root 는 파일이든 환경 변수든 두 경로 모두에서 시크릿을 읽습니다",
          "호스트 root 가 왼쪽에서는 mount -t tmpfs 로 시크릿 파일의 tmpfs 경로를 찾아 파일에 접근하고, "
          "오른쪽에서는 ps -C sh 로 프로세스 ID 를 찾아 /proc/<PID>/environ 에서 SECRET=mysecret 을 읽는다.",
          lead="파일은 tmpfs 경로로, 환경 변수는 /proc/<PID>/environ 으로 읽힙니다")

FS, RT, PR = "호스트 파일시스템", "호스트 root", "호스트 /proc"
d.lanes([(FS, "tmpfs"), (RT, "sudo"), (PR, "프로세스 환경")], y0=104, lane_w=212)
d.rails(484)

ROW = [212, 284, 356, 428]
DASH = "5 4"

# 행 1 — 경로 / PID 를 찾는다
d.msg(RT, FS, "mount -t tmpfs", ROW[0], MUTED, sub="마운트된 tmpfs 나열")
d.msg(RT, PR, "ps -C sh", ROW[0], MUTED, sub="프로세스 ID 찾기")
# 행 2 — 응답
d.msg(FS, RT, "/var/lib/kubelet/pods/…", ROW[1], MUTED, dash=DASH, sub="volumes/kubernetes.io~secret")
d.msg(PR, RT, "프로세스 ID", ROW[1], MUTED, dash=DASH, sub="sh 프로세스")
# 행 3 — 시크릿 접근
d.msg(RT, FS, "경로로 접근", ROW[2], MUTED, sub="출력의 디렉토리 이름 사용")
d.msg(RT, PR, "sudo cat /proc/<PID>/environ", ROW[2], MUTED, sub="환경 전체 읽기")
# 행 4 — 시크릿이 드러난다 (focal)
d.msg(FS, RT, "시크릿 파일 내용", ROW[3], ACC, mk="acc", dash=DASH, sub="tmpfs 안 파일")
d.msg(PR, RT, "SECRET=mysecret", ROW[3], ACC, mk="acc", dash=DASH, sub="환경으로 넘긴 값")

d.state(RT, "컨테이너 root = 호스트 root", 512, INFO)

d.legend(H - 56, [("명령", MUTED), ("시크릿 노출", ACC), ("점선은 응답", SOFT), ("호스트 권한", INFO)])
d.save(str(ASSETS / "12-01.root-reads-secrets.svg"))
print("ok 12-01 root-reads-secrets")
