# 타입 스펙: type-flowchart — 복사한 myping 이 소켓을 못 열어 막힌 자리에서 갈라지는 분기. 왼쪽은 setuid(chown root → chmod +s)로 root 전부, 오른쪽은 setcap(cap_net_raw+p)으로 raw 소켓 하나. focal 은 갈림길 마름모.
# 사실 출처: 노트 L111~L120(cp /bin/ping ./myping, Operation not permitted), L124~L128(chown root, chmod +s), L105·L138(s 표시, 스캐너 보고), L165~L170(setcap, getcap 출력), L174(ls 권한은 그대로), L178(root 전부 vs raw 소켓 하나)
# Layout conventions: 가운데 열 x=480 에서 복사·실행·마름모, 마름모 좌우 출구로 왼쪽 열(상자 x=60 w=288)·오른쪽 열(x=612 w=288)에 단계 두 개와 결과. 모든 좌표 4의 배수.
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, OK, BAD, INFO, KR, MONO

W, H = 960, 788


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


d = D(W, H, "FLOWCHART · 02-01 §4",
      "같은 ping 을 setuid 는 root 전부로, capability 는 raw 소켓 하나로 동작시킵니다",
      "cp /bin/ping ./myping 으로 복사한 myping 은 Operation not permitted 로 막힌다. 여기서 갈라진다. "
      "setuid 길은 chown root 와 chmod +s 로 root 권한 전부를 얻고, capability 길은 setcap cap_net_raw+p 로 CAP_NET_RAW 하나만 얻고 getcap 으로 확인한다.",
      lead="두 길 모두 ./myping 10.0.0.1 이 동작하지만, 딸려 오는 권한의 크기가 다릅니다.")

BW, BH = 288, 72
LXB, RXB = 60, 612
LC, RC = LXB + BW // 2, RXB + BW // 2


def step(x, y, num, title, cmd):
    fit(title, 13, BW - 16)
    fit(cmd, 12, BW - 16)
    d.box(x, y, BW, BH)
    d.t(x + 16, y + 24, num, 11, SOFT, MONO, "start")
    d.t(x + BW / 2, y + 28, title, 13, INK, KR, "middle", 600)
    d.t(x + BW / 2, y + 54, cmd, 12, INFO, MONO, "middle")


def result(x, y, c, title, sub1, sub2):
    fit(title, 14, BW - 16)
    fit(sub1, 12, BW - 16)
    fit(sub2, 12, BW - 16)
    d.tone(x, y, BW, 80, c, 6, "14", 1.2)
    d.t(x + BW / 2, y + 28, title, 14, c, kr(title), "middle", 600)
    d.t(x + BW / 2, y + 48, sub1, 12, MUTED, kr(sub1), "middle")
    d.t(x + BW / 2, y + 66, sub2, 12, MUTED, kr(sub2), "middle")


# 윗부분: 복사 → 실행 → 막힘
d.box(336, 100, 288, 56)
d.t(480, 124, "복사하면 s 비트가 안 딸려 옴", 13, INK, KR, "middle", 600)
d.t(480, 144, "cp /bin/ping ./myping", 12, INFO, MONO, "middle")
d.arrow([(480, 158), (480, 184)], SOFT, "soft", 1.3)

d.tone(312, 188, 336, 72, BAD, 6, "14", 1.2)
d.t(480, 214, "./myping 10.0.0.1", 12, INFO, MONO, "middle")
d.t(480, 242, "ping: socket: Operation not permitted", 12, BAD, MONO, "middle", 600)
d.arrow([(480, 262), (480, 296)], SOFT, "soft", 1.3)

# 마름모
DCX, DCY, DW, DH = 480, 348, 300, 104
pts = f"{DCX},{DCY-DH//2} {DCX+DW//2},{DCY} {DCX},{DCY+DH//2} {DCX-DW//2},{DCY}"
d.o.append(f'<polygon points="{pts}" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.6"/>')
d.t(DCX, DCY - 2, "raw 소켓 권한을", 13, ACC, KR, "middle", 600)
d.t(DCX, DCY + 18, "어떻게 줄까?", 13, ACC, KR, "middle", 600)

# 출구: 왼쪽 setuid, 오른쪽 capability
d.arrow([(DCX - DW // 2 - 2, DCY), (LC, DCY), (LC, 416)], BAD, "bad", 1.5)
d.chip((DCX - DW // 2 + LC) / 2, DCY, "setuid", BAD, 11, 5)
d.arrow([(DCX + DW // 2 + 2, DCY), (RC, DCY), (RC, 416)], OK, "ok", 1.5)
d.chip((DCX + DW // 2 + RC) / 2, DCY, "setcap", OK, 11, 5)

# 왼쪽 길
step(LXB, 420, "1", "소유자를 root 로", "sudo chown root ./myping")
d.arrow([(LC, 494), (LC, 520)], SOFT, "soft", 1.3)
step(LXB, 524, "2", "s 비트 켜기", "sudo chmod +s ./myping")
d.arrow([(LC, 598), (LC, 624)], BAD, "bad", 1.5)
result(LXB, 628, BAD, "root 권한 전부", "ls -l 에 s 가 보임", "이미지 스캐너가 신고")

# 오른쪽 길
step(RXB, 420, "1", "capability 붙이기", "sudo setcap 'cap_net_raw+p' ./myping")
d.arrow([(RC, 494), (RC, 520)], SOFT, "soft", 1.3)
step(RXB, 524, "2", "확인", "getcap ./myping")
d.arrow([(RC, 598), (RC, 624)], OK, "ok", 1.5)
result(RXB, 628, OK, "CAP_NET_RAW 하나", "ls -l 은 -rwxr-xr-x 그대로", "확인은 getcap 으로만")

d.legend(740, [("갈림길", ACC), ("막힘 · 과한 권한", BAD), ("최소 권한", OK), ("명령", INFO)])
d.save(str(ASSETS / "02-01.setuid-vs-capability.svg"))
print("ok 02-01 setuid-vs-capability")
