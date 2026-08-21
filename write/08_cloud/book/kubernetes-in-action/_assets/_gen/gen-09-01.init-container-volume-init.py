# 09-01 §4 — 볼륨이 먼저, 그다음 init 컨테이너
# 본문이 "매니페스트에서 볼륨을 앞에 정의하든 뒤에 정의하든 마찬가지"라고 못박는다. 그러니
# 매니페스트 순서가 아니라 실제 시작 순서를 축으로 삼아야 한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1240, 600, "KUBERNETES IN ACTION · 09-01",
      "볼륨이 먼저 서고, 그다음 채운다",
      "emptyDir 은 빈 채로 시작하므로 매번 손으로 데이터를 넣게 된다. init 컨테이너가 파일을 볼륨에 "
      "미리 복사해 두면 파드가 뜰 때 데이터베이스가 저절로 채워진다.",
      "매니페스트에 볼륨을 앞에 적든 뒤에 적든 이 순서다")

STEP = [("① 볼륨이 만들어진다", "initdb — 빈 디렉터리", None),
        ("② init 컨테이너 시작", "볼륨이 먼저 마운트된다", None),
        ("③ 파일을 볼륨에 복사", "cp insert-questions.js", ACC),
        ("④ init 컨테이너 종료", "복사가 끝나면 물러난다", None),
        ("⑤ 본 컨테이너 시작", "MongoDB 가 그 파일을 읽는다", OK)]
BW, GP = 216, 30
X0 = (1240 - (5 * BW + 4 * GP)) // 2
CX = [X0 + BW // 2 + i * (BW + GP) for i in range(5)]
for cx, (t, s, c) in zip(CX, STEP):
    if c is ACC:
        d.o.append(f'<rect x="{cx-BW//2}" y="212" width="{BW}" height="96" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>'); tc = ACC
    elif c:
        d.box(cx - BW // 2, 212, BW, 96, PAPER2, c, 1.2, 6); tc = c
    else:
        d.box(cx - BW // 2, 212, BW, 96, PAPER2, RULE, 1.1, 6); tc = INK
    d.t(cx, 246, ddx.fit(t, 12, BW - 16, t), 12, tc, KR, "middle", 600)
    d.t(cx, 274, ddx.fit(s, 10, BW - 14, s), 10, MUTED, KR)
for a, b in zip(CX, CX[1:]):
    d.path(f"M {a+BW//2+5} 260 L {b-BW//2-9} 260", MUTED, 1.4, m="ar")

d.o.append(f'<rect x="{CX[0]-BW//2}" y="348" width="{CX[4]+BW//2-(CX[0]-BW//2)}" height="52" rx="6" '
           f'fill="{INFO}0A" stroke="{INFO}" stroke-width="1.0" stroke-dasharray="6 5"/>')
d.t(620, 380, "initdb 볼륨 — 이 구간 내내 같은 디렉터리다", 11, INFO, KR)

d.t(24, 460, "init 컨테이너는 파일을 어디서든 가져올 수 있다. Git 저장소를 clone 해도 되고 자기 이미지에 담아 둬도 된다. "
             "여기서는 질문을 담은 이미지를 만들어 cp 로 복사한다.", 11, MUTED, KR, "start")
d.t(24, 482, "MongoDB 이미지는 시작 시 데이터베이스가 비어 있으면 /docker-entrypoint-initdb.d/ 의 .js·.sh 를 실행한다 — "
             "볼륨을 그 위치에 마운트해 두면 된다.", 11, MUTED, KR, "start")
d.legend(510, [("파일이 옮겨지는 지점", ACC), ("볼륨", INFO), ("읽는 쪽", OK)])
d.save("09-01-init-container-volume-init.svg")
print("ok")
