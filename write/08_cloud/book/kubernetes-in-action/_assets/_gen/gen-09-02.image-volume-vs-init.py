# 09-02 §1 — 같은 결과, 더 짧은 경로
# 캡션이 "같은 결과, 더 짧은 경로"라고 결론을 준다. 그러니 두 방식을 나란히 놓되 단계 수가
# 눈에 띄게 달라야 하고, 무엇이 사라졌는지가 표시돼야 한다.
# 타입 스펙: type-process.md — 두 밴드가 같은 슬롯의 단계를 반복하되 하나는 넷, 하나는 둘이다. 단계 수의 차이가
#           논지라 지나가는 것이 구성 요소가 아니라 하는 일이다.
#           type-process 정본의 입력 계약은 역할 레인 1~6 이 전제인데 이 그림에 레인은 없다.
#           주체를 요구하지 않는 유일한 라우팅 규칙이 semantic-patterns 의
#           "Stage framework with semantic slots" 한 줄이라 그것을 근거로 둔다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO
import ddx

d = D(1240, 664, "KUBERNETES IN ACTION · 09-02",
      "같은 결과에 이르는 두 길",
      "파일을 컨테이너에 놓는 일은 같다. init 컨테이너는 그것을 복사로 하고, image 볼륨은 "
      "이미지 자체를 볼륨으로 마운트해 복사 단계를 없앤다.",
      "image 볼륨은 v1.31 alpha · v1.33 beta")

def road(y0, label, steps, c, focal, verdict, vc):
    ddx.band(d, y0, y0 + 216, label, x=24, w=1172)
    BW, GP = 200, 42
    X0 = 90
    CX = [X0 + BW // 2 + i * (BW + GP) for i in range(len(steps))]
    for cx, (t, s) in zip(CX, steps):
        d.box(cx - BW // 2, y0 + 76, BW, 84, PAPER2, c, 1.1, 6)
        d.t(cx, y0 + 108, ddx.fit(t, 12, BW - 16, t), 12, c, KR, "middle", 600)
        d.t(cx, y0 + 134, ddx.fit(s, 10, BW - 14, s), 10, MUTED, KR)
    for a, b in zip(CX, CX[1:]):
        d.path(f"M {a+BW//2+5} {y0+118} L {b-BW//2-9} {y0+118}", MUTED, 1.4, m="ar")
    # x=1000 은 4 단 행의 마지막 상자(816~1016)를 156px 덮었다. 단 수가 행마다 달라
    # 상자 오른쪽이 아니라 상자 아래 띠 가운데에 둔다 — 두 행이 같은 자리를 쓴다.
    if focal:
        ddx.focal_tag(d, 610, y0 + 190, verdict, 280)
    else:
        ddx.tag(d, 610, y0 + 190, verdict, vc, 280)

road(100, "init 컨테이너로 복사", [
    ("이미지를 만든다", "파일을 담아"), ("init 이 뜬다", "볼륨을 마운트"),
    ("cp 로 복사", "볼륨에 넣는다"), ("init 종료", "본 컨테이너 시작"),
], INFO, False, "네 단계 · 복사가 낀다", INFO)

road(340, "image 볼륨으로 마운트", [
    ("이미지를 만든다", "파일을 담아"), ("볼륨으로 마운트", "이미지 자체를"),
], OK, True, "두 단계 · 복사가 없다", None)

d.t(24, 596, "image 볼륨은 이미지를 읽기 전용으로 마운트한다. 파일을 옮기지 않으므로 복사 시간과 볼륨 공간이 "
             "들지 않고, 컨테이너가 뜨기 전에 이미 준비돼 있다.", 11, MUTED, KR, "start")
d.legend(616, [("복사로 옮긴다", INFO), ("그대로 마운트", OK), ("짧아진 경로", ACC)])
d.save("09-02-image-volume-vs-init.svg")
print("ok")
