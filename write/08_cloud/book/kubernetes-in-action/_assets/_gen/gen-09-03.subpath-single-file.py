# 09-03 §2 — 디렉터리를 덮지 않고 파일 하나만 얹는다
# subPath 의 쓸모는 "기존 디렉터리를 가리지 않는다"에 있다. 그러니 마운트 전후의 디렉터리
# 내용을 나란히 놓아, 나머지 파일이 살아남는 것이 보여야 한다.
# 타입 스펙: type-dp-security-matrix.md — 세 디렉터리 뷰를 같은 형식으로 늘어놓고 어떤 파일이 남고 가려지는지를 대조한다.
#           행이 아니라 열로 늘어섰지만 같은 슬롯이 반복되는 격자다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, BAD, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1240, 640, "KUBERNETES IN ACTION · 09-03",
      "디렉터리째 덮을 것인가, 파일 하나만 얹을 것인가",
      "볼륨을 디렉터리에 통째로 마운트하면 그 아래 원래 있던 것이 전부 가려진다. subPath 는 "
      "볼륨 안의 한 항목만 지정한 파일 경로에 얹는다.",
      "/etc 에는 이미 이미지가 담아 둔 파일들이 있다")

def dir_view(x0, label, files, note, note_c):
    d.box(x0, 176, 360, 268, PAPER, RULE, 0.9, 8)
    d.t(x0 + 180, 204, label, 11, SOFT, KR)
    for i, (nm, c) in enumerate(files):
        y = 244 + i * 34
        d.t(x0 + 40, y, nm, 11, c, MONO, "start")
    d.t(x0 + 180, 416, note, 11, note_c, KR)

dir_view(60, "마운트 전 — 이미지의 /etc", [
    ("passwd", MUTED), ("hosts", MUTED), ("app.conf", MUTED), ("nginx/", MUTED)], "원래 있던 것들", SOFT)

dir_view(440, "디렉터리째 마운트하면", [
    ("app.conf", ACC), ("db.conf", ACC), ("(passwd 안 보임)", BAD),
    ("(hosts 안 보임)", BAD)], "볼륨 내용만 보인다", BAD)

dir_view(820, "subPath 로 파일 하나만", [
    ("passwd", MUTED), ("hosts", MUTED), ("app.conf", ACC), ("nginx/", MUTED)],
    "나머지가 그대로 살아 있다", OK)

d.path("M 424 300 L 436 300", MUTED, 1.4, m="ar")
d.path("M 804 300 L 816 300", MUTED, 1.4, m="ar")

d.t(24, 504, "그래서 설정 파일 하나만 갈아 끼울 때 subPath 를 쓴다. 다만 그 편의의 대가가 갱신을 못 받는 것이다 — "
             "다음 도식이 그 이유를 다룬다.", 11, MUTED, KR, "start")
d.t(24, 526, "우회하려면 볼륨을 다른 디렉터리에 통째로 마운트하고, 원하는 자리에 심링크를 이미지에 미리 만들어 둔다.",
     11, MUTED, KR, "start")
d.legend(552, [("볼륨에서 온 파일", ACC), ("가려진 것", BAD), ("살아남은 것", OK)])
d.save("09-03-subpath-single-file.svg")
print("ok")
