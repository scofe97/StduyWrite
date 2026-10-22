# 타입 스펙: type-layers — 위에서 아래로 [유저 공간] · [시스템 콜 인터페이스] · [커널 공간]. 유저 공간의 세 프로세스(컨테이너 둘, 호스트 하나)가 하나의 인터페이스로 모여 커널 하나에 닿는다. focal 은 커널.
# 사실 출처: 노트 L49(유저 공간·커널 권한 수준·시스템 콜), L51~L58(300종 이상·예 여섯), L60(glibc·Go syscall), L62(같은 커널에 시스템 콜)
# Layout conventions: 바깥 폭 816(x=72), 유저 공간 y=100~220 안에 앱 상자 3개(폭 248, 간격 20, y=140~204), 인터페이스 y=268 h=72, 커널 y=396 h=72. 모든 좌표 4의 배수.
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, OK, BAD, INFO, KR, MONO

W, H = 960, 544


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


d = D(W, H, "LAYERS · 02-01 §1",
      "컨테이너 안이든 밖이든 모든 프로세스는 같은 시스템 콜 인터페이스로 하나의 커널에 닿습니다",
      "위에서 아래로 유저 공간, 시스템 콜 인터페이스, 커널 공간. 유저 공간의 컨테이너 A 앱, 컨테이너 B 앱, 호스트 프로세스가 "
      "모두 시스템 콜 인터페이스를 거쳐 커널 하나로 모인다. 인터페이스에는 read, write, open, execve, chown, clone 등 300여 종이 있다.",
      lead="유저 공간은 낮은 권한이라 파일 접근도 커널에 부탁해야 하고, 그 부탁의 창구가 시스템 콜입니다.")

OX, OW = 72, 816

# 유저 공간 묶음
d.o.append(f'<rect x="{OX}" y="100" width="{OW}" height="120" rx="6" fill="{MUTED}12" stroke="{MUTED}" stroke-width="1.0"/>')
d.t(OX + 16, 124, "L3", 9, SOFT, MONO, "start")
d.t(OX + 48, 126, "유저 공간 — 낮은 권한", 13, INK, KR, "start", 600)

AW, AH, AY = 248, 64, 140
AXS = [88, 356, 624]
APPS = [
    ("컨테이너 A 의 앱", "glibc · Go syscall 경유"),
    ("컨테이너 B 의 앱", "glibc · Go syscall 경유"),
    ("호스트의 프로세스", "같은 방식으로 호출"),
]

# 앱 → 인터페이스 화살표(상자보다 먼저 그려 선이 뒤로 간다)
for x in AXS:
    d.arrow([(x + AW / 2, AY + AH + 2), (x + AW / 2, 264)], MUTED, "ar", 1.4)

for x, (t1, t2) in zip(AXS, APPS):
    fit(t1, 13, AW - 16)
    fit(t2, 12, AW - 16)
    d.box(x, AY, AW, AH)
    d.t(x + AW / 2, AY + 27, t1, 13, INK, KR, "middle", 600)
    d.t(x + AW / 2, AY + 49, t2, 12, MUTED, kr(t2), "middle")

# 시스템 콜 인터페이스
IY = 268
d.o.append(f'<rect x="{OX}" y="{IY}" width="{OW}" height="72" rx="6" fill="{INFO}12" stroke="{INFO}" stroke-width="1.0"/>')
d.t(OX + 16, IY + 24, "L2", 9, SOFT, MONO, "start")
d.t(OX + 16, IY + 50, "시스템 콜 인터페이스", 16, INK, KR, "start", 600)
d.t(OX + OW - 16, IY + 32, "read · write · open · execve · chown · clone", 12, MUTED, MONO, "end")
d.t(OX + OW - 16, IY + 52, "300여 종 · 커널 버전마다 다름", 12, MUTED, KR, "end")

# 인터페이스 → 커널: 한 줄로 모인다
KY = 396
d.arrow([(OX + OW / 2, IY + 74), (OX + OW / 2, KY - 4)], ACC, "acc", 1.8)
d.t(OX + OW / 2 + 16, IY + 98, "요청이 한 곳으로", 12, MUTED, KR, "start", 600)

# 커널 공간 (focal)
d.o.append(f'<rect x="{OX}" y="{KY}" width="{OW}" height="72" rx="6" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.6"/>')
d.t(OX + 16, KY + 24, "L1", 9, SOFT, MONO, "start")
d.t(OX + 16, KY + 50, "커널 공간 — 높은 권한", 16, ACC, KR, "start", 600)
d.t(OX + OW - 16, KY + 32, "커널은 하나뿐", 13, INK, KR, "end", 600)
d.t(OX + OW - 16, KY + 52, "호스트의 모든 컨테이너가 공유", 12, MUTED, KR, "end")

d.legend(496, [("유저 공간", MUTED), ("인터페이스", INFO), ("공유되는 커널", ACC)])
d.save(str(ASSETS / "02-01.syscall-boundary.svg"))
print("ok 02-01 syscall-boundary")
