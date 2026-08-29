# 14-01 §고친 내장 롤은 되돌아갑니다
# "덮어쓴다" 로 그리면 틀린다. 공식 문서가 더 정확히 적듯 API 서버는 기동할 때마다
# *누락된* 권한과 *누락된* 주체를 채운다. 그래서 권한을 더한 변경은 살아남고
# 지운 변경만 되돌아온다 — 이 갈림이 재기동선 하나를 두고 세 줄을 나란히 놓아야 보인다.
# 애노테이션 줄에는 본문이 붙인 경고(빠진 채로 남아 클러스터가 안 돌 수 있다)를 같이 둔다.
# 타입 스펙: type-dp-security-matrix.md — 행이 세 가지 변경, 열이 두 국면(내가 한 변경 · 재기동 뒤)인
#           격자다. 행 높이·열 폭이 고정이고 독자의 동작은 "내 변경이 어느 행인가" 찾기다.
#           어긋나는 지점: 정본이 격자에 연결선을 금한다. 여기 화살표는 칸끼리 잇는 것이 아니라
#           세 행이 공유하는 단 하나의 전이(재기동)를 반복해 얹은 것이고, 가운데 세로 점선이
#           이미 그 경계를 긋는다. 칸이 권한값이 아니라 결과 문장인 것도 정본과 다르다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, MUTED, SOFT, INK, PAPER2, PAPER, RULE, KR, MONO
import ddx

W, H = 1240, 634
d = D(W, H, "KUBERNETES UP AND RUNNING · 14-01",
      "지운 권한만 되돌아온다",
      "API 서버는 기동할 때마다 자기 코드에 정의된 기본 ClusterRole 을 설치한다. 정확히는 "
      "기본 롤의 누락된 권한과 기본 바인딩의 누락된 주체를 채운다.",
      "그래서 더한 변경은 살아남고, 지운 변경만 사라진다")

LX, LW = 40, 600
DV = 668
RX, RW = 696, 520
Y0, RH, GAP = 200, 80, 18

d.t(DV, 152, "API 서버 재기동", 11, INK, KR, "middle", 600)
d.line(DV, 168, DV, Y0 + RH * 3 + GAP * 2 + 14, RULE, 1.2, "5 5")
d.t(LX, 178, "내가 한 변경", 11, SOFT, KR, "start")
d.t(RX, 178, "재기동 뒤", 11, SOFT, KR, "start")

ROWS = [("권한을 더했다", "내장 ClusterRole 에 규칙을 추가한다",
         "그대로 남는다", "채우기만 할 뿐 덜어내지 않는다", OK, False),
        ("권한을 지웠다", "내장 ClusterRole 에서 규칙을 제거한다",
         "지운 권한이 되돌아온다", "기본 롤의 누락된 권한을 다시 채운다", ACC, True),
        ("애노테이션을 먼저 달고 지웠다", 'rbac.authorization.kubernetes.io/autoupdate: "false"',
         "지운 채로 남는다", "기본 권한·주체가 빠져 클러스터가 동작하지 않을 수 있다", WARN, False)]

for i, (lt, ls, rt, rs, c, focal) in enumerate(ROWS):
    y = Y0 + i * (RH + GAP)
    cy = y + RH / 2
    d.box(LX, y, LW, RH, PAPER2, RULE, 1.0, 6)
    d.t(LX + LW / 2, cy - 2, ddx.fit(lt, 13, LW - 40, lt), 13, INK, KR, "middle", 600)
    mono = ls.startswith("rbac")
    d.t(LX + LW / 2, cy + 20, ls, 10 if mono else 11, SOFT, MONO if mono else KR)
    if focal:
        d.o.append(f'<rect x="{RX}" y="{y}" width="{RW}" height="{RH}" rx="6" '
                   f'fill="{c}12" stroke="{c}" stroke-width="1.4"/>')
    else:
        d.box(RX, y, RW, RH, PAPER2, c, 1.1, 6)
    d.t(RX + RW / 2, cy - 2, ddx.fit(rt, 13, RW - 40, rt), 13, c, KR, "middle", 600)
    d.t(RX + RW / 2, cy + 20, ddx.fit(rs, 11, RW - 40, rs), 11, c if focal else MUTED, KR)
    d.path(f"M {LX+LW} {cy} L {RX-4} {cy}", c if focal else MUTED, 1.5,
           m="acc" if focal else "ar")

NY = Y0 + RH * 3 + GAP * 2 + 34
d.t(LX, NY, "채워 넣는 대상은 둘이다 — 기본 클러스터 롤의 누락된 권한, 그리고 기본 클러스터 롤 바인딩의 누락된 주체.",
     11, MUTED, KR, "start")
d.t(LX, NY + 22, "애노테이션은 다른 수정을 하기 전에 먼저 단다. 고친 뒤에 달면 이미 덮여 쓴 다음이다.",
     11, MUTED, KR, "start")
d.t(LX, NY + 44, "애노테이션 도메인은 kubernetes.io 다. 뒤에 나올 집계 라벨의 k8s.io 와 다르니 "
                 "오타로 보고 고치면 그냥 무시된다.", 11, MUTED, KR, "start")

d.legend(NY + 70, [("되돌아온다", ACC), ("살아남는다", OK), ("남지만 위험하다", WARN)])
d.save("14-01.builtin-role-autoupdate.svg")
print("h 필요:", NY + 70 + 48, " 실제:", H)
