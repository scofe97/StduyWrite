# 타입 스펙: type-architecture — 침해된 컨테이너 하나에서 -v 마운트 대상 여섯으로 갈라지는 길과 각 길 끝의 결과. 점선 존은 / 마운트에 아래 경로가 모두 포함됨을 묶는다. focal 은 -v /:/hostroot 한 줄.
# 사실 출처: 노트 L196~L199(-v /:/hostroot · ls /hostroot/ 에 호스트 / · 호스트 root) · L205~L208(/etc · /bin 계열 · 호스트 로그 디렉토리 · /var/log 마운트 표) · L210(로그 파일은 symlink 이고 목적지 변경을 막을 수 없음) · L214~L216(/var/run/docker.sock · 데몬은 root)
# Layout conventions: 3열(컨테이너 x=36 w180 · 경로 x=300 w240 · 결과 x=608 w340), 행 h=52 stride 64, 1행만 점선 존 밖(y=116), 존 안 5행 y=228~. 컨테이너 출구는 x=252 직각 버스에서 행마다 수평 드롭. 모든 좌표 4의 배수.
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, BAD, PAPER2, KR, MONO

W, H = 984, 640


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


d = D(W, H, "ARCHITECTURE · 09-01 §4",
      "마운트한 경로 하나마다 호스트로 나가는 길이 하나씩 생깁니다",
      "침해된 컨테이너가 -v 로 / 를 마운트하면 ls /hostroot/ 에 호스트 루트가 보이고, 그 아래 /etc · /bin 계열 · 로그 디렉토리 · /var/log · /var/run/docker.sock 도 각각 따로 탈출 경로가 된다.",
      lead="호스트 루트를 마운트하면 아래 경로가 모두 포함되고, 개별 경로만 마운트해도 각자 탈출 경로가 됩니다.")

PX, PW = 300, 240   # 경로 열
OX, OW = 608, 340   # 결과 열
RH = 52
ROWS = [  # (y, 경로 텍스트, 경로 폰트, 결과 제목, 결과 부제)
    (116, "-v /:/hostroot", "m", "호스트 파일시스템 전체 접근", "ls /hostroot/"),
    (228, "/etc", "m", "/etc/passwd 수정", "cron · init · systemd 접근"),
    (292, "/bin · /usr/bin · /usr/sbin", "m12", "실행 파일 쓰기", "기존 실행 파일 덮어쓰기"),
    (356, "호스트 로그 디렉토리", "k", "로그 수정", "자기 행적 삭제"),
    (420, "/var/log · Kubernetes", "m", "kubectl logs 권한자에게 호스트 전체", "로그 symlink 의 목적지 변경"),
    (484, "/var/run/docker.sock", "m", "Docker 데몬(root)에 명령", "root 로 컨테이너 실행"),
]
BUS_X = 252
cys = [y + RH / 2 for y, *_ in ROWS]

# 존: 1행 아래 5행을 묶는 점선 (연결선·노드보다 먼저)
d.o.append(f'<rect x="284" y="184" width="272" height="368" rx="8" fill="none" stroke="rgba(191,192,192,0.35)" stroke-width="1.0" stroke-dasharray="6 5"/>')
d.t(300, 207, "/ 마운트에 포함", 12, MUTED, KR, "start")

# 연결선: 컨테이너 → 버스 → 행마다 드롭, 행마다 경로 → 결과
CT_Y = (cys[0] + cys[-1]) / 2 - 40
d.line(216, CT_Y + 40, BUS_X, CT_Y + 40, MUTED, 1.4)
d.line(BUS_X, cys[0], BUS_X, cys[-1], MUTED, 1.4)
for k, cy in enumerate(cys):
    c, m = (ACC, "acc") if k == 0 else (MUTED, "ar")
    d.arrow([(BUS_X, cy), (PX - 4, cy)], c, m, 1.4)
    d.arrow([(PX + PW + 2, cy), (OX - 4, cy)], BAD if k else ACC, "bad" if k else "acc", 1.4)

# 컨테이너
d.box(36, CT_Y, 180, 80, PAPER2, MUTED, 1.2, 6)
d.t(126, CT_Y + 34, "침해된 컨테이너", 14, INK, KR, "middle", 600)
d.t(126, CT_Y + 58, "docker run -v", 12, MUTED, MONO, "middle")

# 경로 · 결과
for k, (y, ptxt, pf, rt, rs) in enumerate(ROWS):
    focal = k == 0
    if focal:
        d.o.append(f'<rect x="{PX}" y="{y}" width="{PW}" height="{RH}" rx="6" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.6"/>')
    else:
        d.box(PX, y, PW, RH, PAPER2, MUTED, 1.0, 6)
    size = 12 if pf == "m12" else 13
    fit(ptxt, size, PW - 16)
    d.t(PX + PW / 2, y + RH / 2 + 5, ptxt, size, ACC if focal else INK, KR if pf == "k" else MONO, "middle", 600)

    if focal:
        d.o.append(f'<rect x="{OX}" y="{y}" width="{OW}" height="{RH}" rx="6" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.6"/>')
    else:
        d.tone(OX, y, OW, RH, BAD, 6, "14", 1.1)
    fit(rt, 13, OW - 24)
    fit(rs, 12, OW - 24)
    d.t(OX + 16, y + 22, rt, 13, ACC if focal else INK, kr(rt), "start", 600)
    d.t(OX + 16, y + 41, rs, 12, MUTED, MONO if rs.startswith("ls ") else kr(rs), "start")

d.legend(H - 56, [("/ 통째 마운트", ACC), ("개별 경로의 결과", BAD)])
d.save(str(ASSETS / "09-01.sensitive-mounts.svg"))
print("ok 09-01 sensitive-mounts")
