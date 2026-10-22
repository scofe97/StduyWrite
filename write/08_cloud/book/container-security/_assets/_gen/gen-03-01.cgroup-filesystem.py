# 타입 스펙: type-tree — /sys/fs/cgroup 아래 자원 종류별 계층, memory 안의 mkdir 한 cgroup, 커널이 채운 파라미터·통계 파일을 왼쪽 → 오른쪽 트리로 보여 디렉토리 조작이 곧 cgroup 조작임을 보인다. focal 은 mkdir 로 생긴 liz/.
# 사실 출처: 노트 L55~L69(계층·파일), L77~L82(mkdir 과 커널이 채움), L144~L148(cgroup.procs), L167~L173(docker/<컨테이너 ID>)
# Layout conventions: 열 폭 [168,168,168,252], 열 간격 52, 노드 높이 52, 파일 행 stride 68(y=128·196·264·332), 모든 좌표 4의 배수. 연결선은 직각 버스.
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, OK, INFO, KR, MONO

W, H = 984, 476
NH = 52
COLS = [(36, 168), (256, 168), (476, 168), (696, 252)]


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


d = D(W, H, "TREE · 03-01 §2~3",
      "디렉토리를 만들면 커널이 그 안을 cgroup 파일로 채웁니다",
      "/sys/fs/cgroup 아래에 자원 종류마다 계층이 있고, memory 계층에서 mkdir memory/liz 로 cgroup liz 를 만들면 "
      "커널이 memory.limit_in_bytes · cgroup.procs 같은 쓰기 파일과 memory.usage_in_bytes · memory.max_usage_in_bytes 같은 읽기 통계 파일을 채운다. "
      "컨테이너를 시작하면 런타임이 docker 아래에 컨테이너 ID 이름의 cgroup 을 만든다.",
      lead="디렉토리 하나가 cgroup 하나이고, 값을 쓰는 파일이 곧 조작 수단입니다.")


def node(col, y, title, sub, c=None, mono_title=True):
    x, w = COLS[col]
    fit(title, 13, w - 16)
    fit(sub, 12, w - 16)
    if c:
        d.tone(x, y, w, NH, c, 6, "14" if c != ACC else "1F", 1.6 if c == ACC else 1.1)
    else:
        d.box(x, y, w, NH)
    d.t(x + w / 2, y + 22, title, 13, c or INK, MONO if mono_title else kr(title), "middle", 600)
    d.t(x + w / 2, y + 40, sub, 12, MUTED, kr(sub), "middle")


def bus(col_a, ya, col_b, ys, c=SOFT):
    # 부모 오른쪽 → 가운데 세로 버스 → 자식 왼쪽. 자식마다 짧은 화살표 하나
    xa = COLS[col_a][0] + COLS[col_a][1]
    xb = COLS[col_b][0]
    xm = xa + 24
    d.line(xa, ya, xm, ya, c, 1.2)
    d.line(xm, min(ys + [ya]), xm, max(ys + [ya]), c, 1.2)
    for y in ys:
        d.arrow([(xm, y), (xb - 4, y)], c, "soft", 1.2)


# 열 머리
d.t(COLS[1][0], 104, "자원 종류마다 계층", 12, MUTED, KR, "start", 600)
d.t(COLS[2][0], 104, "cgroup = 디렉토리", 12, MUTED, KR, "start", 600)
d.t(COLS[3][0], 104, "커널이 채운 파일", 12, MUTED, KR, "start", 600)

FILE_Y = [128 + 68 * i for i in range(4)]
CY = [y + NH // 2 for y in FILE_Y]
MID = (CY[0] + CY[3]) // 2          # 256

# 연결선 먼저
ROOT_Y = MID - NH // 2
T1 = {"pids": 128, "memory": MID - NH // 2, "etc": 332}
bus(0, MID, 1, [T1["pids"] + NH // 2, MID, T1["etc"] + NH // 2])
bus(1, MID, 2, [MID, T1["etc"] + NH // 2])
bus(2, MID, 3, CY)

# 노드
node(0, ROOT_Y, "/sys/fs/cgroup", "의사 파일시스템")
node(1, T1["pids"], "pids", "프로세스 개수 제한", mono_title=True)
node(1, T1["memory"], "memory", "계층의 최상위")
node(1, T1["etc"], "cpu · blkio …", "그 밖의 종류별 계층")
node(2, MID - NH // 2, "liz/", "mkdir memory/liz", ACC)
node(2, T1["etc"], "docker/", "<컨테이너 ID>/ 가 생김")
node(3, FILE_Y[0], "memory.limit_in_bytes", "쓰기 · 최대 메모리 한도", OK)
node(3, FILE_Y[1], "cgroup.procs", "쓰기 · PID 배정", OK)
node(3, FILE_Y[2], "memory.usage_in_bytes", "읽기 · 지금 쓰는 양", INFO)
node(3, FILE_Y[3], "memory.max_usage_in_bytes", "읽기 · 기록된 최고점", INFO)

d.legend(412, [("mkdir 로 만든 cgroup", ACC), ("쓰기 · 한도와 배정", OK), ("읽기 · 커널이 적는 통계", INFO)])
d.save(str(ASSETS / "03-01.cgroup-filesystem.svg"))
print("ok 03-01 cgroup-filesystem")
