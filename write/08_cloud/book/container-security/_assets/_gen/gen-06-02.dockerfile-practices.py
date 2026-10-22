# 타입 스펙: type-tree — 루트 공격 표면 아래 세 갈래(코드 · 권한 · 변조 경로)로 Dockerfile 권고 아홉 항목을 묶는다. 묶음 이름은 이 도식의 분류이고 책의 목차가 아니다. focal 은 RUN 편집 권한 제한(노트가 가장 강한 경고로 꼽은 대목).
# 사실 출처: 노트 L66~L92(Dockerfile 보안 모범 사례 본문 전부), L80~L82(RUN 경고)
# Layout conventions: 루트 w=200 중앙 · 버스 y=168 · 묶음 노드 w=288 x=20·348·676 · 잎 w=248 h=56 stride 72, 세로 척추 x=묶음 x+24, 모든 좌표 4의 배수.
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, OK, WARN, BAD, INFO, KR, MONO, RULE

W, H = 984, 548
GX = [20, 348, 676]
GW = 288
LW, LH, LSTRIDE = 248, 56, 72
LY0 = 260


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


d = D(W, H, "CONTAINER SECURITY · 06-02 §2",
      "Dockerfile 권고는 모두 공격 표면을 줄이는 쪽을 가리킵니다",
      "공격 표면 아래에 코드를 줄이는 권고, 권한을 줄이는 권고, 변조 경로를 닫는 권고가 각각 셋씩 걸려 있다.",
      "Dockerfile 의 키워드마다 어느 표면을 줄이는지 짝지었습니다.")

GROUPS = [
    ("코드를 줄인다", [
        ("최소 베이스 이미지", "FROM scratch · distroless", False),
        ("멀티스테이지 빌드", "바이너리만 다음 단계로", False),
        ("불필요한 코드 제외", "패키지 · 라이브러리 · 실행 파일", False),
    ]),
    ("권한을 줄인다", [
        ("비root 사용자", "모든 Dockerfile 에 USER", False),
        ("setuid 바이너리 제외", "권한 상승 경로", False),
        ("민감 디렉토리 마운트 금지", "/etc · /bin", False),
    ]),
    ("변조 경로를 닫는다", [
        ("RUN 편집 권한 제한", "신뢰하는 팀원 + 코드 리뷰", True),
        ("비밀 데이터 제외", "자격증명 · 비밀번호", False),
        ("필요한 것은 전부 포함", "런타임 패키지 설치 없음", False),
    ]),
]

# 커넥터는 노드보다 먼저 그린다
RX, RY, RW, RH = (W - 200) // 2, 100, 200, 48
rcx = RX + RW // 2
BUS_Y, GY, GH = 168, 188, 44
gcx = [x + GW // 2 for x in GX]
d.line(rcx, RY + RH, rcx, BUS_Y, SOFT, 1.0)
d.line(gcx[0], BUS_Y, gcx[2], BUS_Y, SOFT, 1.0)
for cx in gcx:
    d.line(cx, BUS_Y, cx, GY, SOFT, 1.0)
for i, (gname, leaves) in enumerate(GROUPS):
    sx = GX[i] + 24
    last_cy = LY0 + (len(leaves) - 1) * LSTRIDE + LH // 2
    d.line(sx, GY + GH, sx, last_cy, SOFT, 1.0)
    for k in range(len(leaves)):
        cy = LY0 + k * LSTRIDE + LH // 2
        d.line(sx, cy, GX[i] + 40, cy, SOFT, 1.0)

d.box(RX, RY, RW, RH, "#161B22", RULE, 1.0)
d.t(rcx, RY + 30, "공격 표면", 16, INK, KR, "middle", 600)

for i, (gname, leaves) in enumerate(GROUPS):
    fit(gname, 14, GW - 16)
    d.tone(GX[i], GY, GW, GH, INFO, 6, "14", 1.1)
    d.t(gcx[i], GY + 28, gname, 14, INFO, KR, "middle", 600)
    for k, (title, sub, focal) in enumerate(leaves):
        lx, ly = GX[i] + 40, LY0 + k * LSTRIDE
        fit(title, 13, LW - 16)
        fit(sub, 12, LW - 16)
        if focal:
            d.tone(lx, ly, LW, LH, ACC, 6, "1F", 1.4)
        else:
            d.box(lx, ly, LW, LH, "#161B22", RULE, 1.0)
        d.t(lx + LW / 2, ly + 24, title, 13, INK, kr(title), "middle", 600)
        d.t(lx + LW / 2, ly + 44, sub, 12, MUTED, kr(sub), "middle")

d.legend(LY0 + 2 * LSTRIDE + LH + 28, [("권고 묶음", INFO), ("가장 날카로운 경고", ACC)])
d.save(str(ASSETS / "06-02.dockerfile-practices.svg"))
print("ok 06-02 dockerfile-practices")
