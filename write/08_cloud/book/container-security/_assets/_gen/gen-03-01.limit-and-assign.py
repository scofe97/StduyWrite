# 타입 스펙: type-flowchart — mkdir · 한도 쓰기 · PID 쓰기 세 단계가 모두 파일 조작이고, 그 셸에서 ls 를 실행하면 사용량이 한도를 넘는지로 갈려 Killed 라는 막다른 길에 닿는 분기. focal 은 커널이 판정하는 마름모.
# 사실 출처: 노트 L77~L79(mkdir), L139~L144(echo 100000 → 98304), L146~L151(echo 29903 > cgroup.procs, ls), L157~L159(Killed). 한도 이내 분기는 L115·L159 의 "다른 프로세스가 정상으로 계속 돌게" 에서 읽은 일반화.
# Layout conventions: 윗줄 세 단계 박스 폭 288 높이 72(x=36·360·684, y=116), 마지막 단계 아래로 꺾어 내려와 오른쪽 열에 ls 박스(y=264), 왼쪽으로 마름모(중심 x=480, y=300), 마름모 왼쪽 출구와 아래쪽 출구. 모든 좌표 4의 배수.
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, OK, BAD, INFO, KR, MONO

W, H = 984, 556


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


d = D(W, H, "FLOWCHART · 03-01 §4",
      "한도와 배정은 모두 파일 쓰기이고, 한도를 넘으면 커널이 프로세스를 죽입니다",
      "mkdir memory/liz 로 cgroup 을 만들고, echo 100000 > memory.limit_in_bytes 로 한도를 걸면 되읽은 값이 98304 로 페이지 단위에 맞춰진다. "
      "echo 29903 > cgroup.procs 로 셸을 배정한 뒤 그 셸에서 ls 를 실행하면 사용 메모리가 한도를 넘어 Killed 만 돌아온다. 한도 이내라면 그대로 실행된다.",
      lead="세 단계에 쓰는 것은 디렉토리 이름과 숫자뿐이고, 강제는 커널이 합니다.")

BW, BH = 288, 72
XS = [36, 360, 684]
Y0 = 116


def step(x, y, num, title, cmd, tag=None):
    fit(title, 13, BW - 16)
    fit(cmd, 12, BW - 16)
    d.box(x, y, BW, BH)
    d.t(x + 16, y + 24, num, 11, SOFT, MONO, "start")
    d.t(x + BW / 2, y + 28, title, 13, INK, KR, "middle", 600)
    d.t(x + BW / 2, y + 54, cmd, 12, INFO, MONO, "middle")
    if tag:
        fit(tag, 12, BW)
        d.t(x + BW / 2, y + BH + 22, tag, 12, MUTED, kr(tag), "middle")


# 연결 화살표 먼저
mid = Y0 + BH // 2
for a, b in ((0, 1), (1, 2)):
    d.arrow([(XS[a] + BW + 2, mid), (XS[b] - 4, mid)], SOFT, "soft", 1.3)

# 단계 3 아래 → ls 박스 위
LS_X, LS_Y = 684, 264
cx3 = XS[2] + BW // 2
d.arrow([(cx3, Y0 + BH + 40), (cx3, LS_Y - 4)], SOFT, "soft", 1.3)

step(XS[0], Y0, "1", "cgroup 만들기", "mkdir memory/liz")
step(XS[1], Y0, "2", "한도 걸기", "echo 100000 > memory.limit_in_bytes", "되읽으면 98304 · 페이지 단위로 맞춤")
step(XS[2], Y0, "3", "프로세스 배정", "echo 29903 > cgroup.procs", "그 셸이 이 cgroup 의 구성원")

# ls 박스
d.box(LS_X, LS_Y, BW, BH)
d.t(LS_X + 16, LS_Y + 24, "4", 11, SOFT, MONO, "start")
d.t(LS_X + BW / 2, LS_Y + 28, "셸에서 실행", 13, INK, KR, "middle", 600)
d.t(LS_X + BW / 2, LS_Y + 54, "ls", 12, INFO, MONO, "middle")

# 마름모
DCX, DCY, DW, DH = 400, 300, 240, 112
pts = f"{DCX},{DCY-DH//2} {DCX+DW//2},{DCY} {DCX},{DCY+DH//2} {DCX-DW//2},{DCY}"
d.o.append(f'<polygon points="{pts}" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.6"/>')
d.t(DCX, DCY - 2, "사용 메모리 > 한도?", 13, ACC, KR, "middle", 600)
d.t(DCX, DCY + 18, "커널이 판정", 12, MUTED, KR, "middle")
d.arrow([(LS_X - 2, LS_Y + BH // 2), (DCX + DW // 2 + 4, DCY)], SOFT, "soft", 1.3)

# 출구: 아래(예) = Killed, 왼쪽(아니오) = 그대로 실행
KX, KY, KW, KH = 280, 412, 240, 72
d.arrow([(DCX, DCY + DH // 2 + 2), (DCX, KY - 4)], BAD, "bad", 1.5)
d.chip(DCX + 36, DCY + DH // 2 + 20, "넘음", BAD, 11, 5)
d.tone(KX, KY, KW, KH, BAD, 6, "14", 1.2)
d.t(KX + KW / 2, KY + 30, "Killed", 14, BAD, MONO, "middle", 600)
d.t(KX + KW / 2, KY + 54, "ls 만으로도 한도 초과", 12, MUTED, KR, "middle")

OX, OY, OW, OH = 36, 264, 156, 72
d.arrow([(DCX - DW // 2 - 2, DCY), (OX + OW + 4, DCY)], OK, "ok", 1.5)
d.chip(OX + OW + 52, DCY - 20, "이내", OK, 11, 5)
d.tone(OX, OY, OW, OH, OK, 6, "14", 1.2)
d.t(OX + OW / 2, OY + 30, "그대로 실행", 13, OK, KR, "middle", 600)
d.t(OX + OW / 2, OY + 54, "다른 프로세스는 계속", 12, MUTED, KR, "middle")

d.legend(512, [("판정", ACC), ("한도 이내", OK), ("막다른 길", BAD), ("명령", INFO)])
d.save(str(ASSETS / "03-01.limit-and-assign.svg"))
print("ok 03-01 limit-and-assign")
