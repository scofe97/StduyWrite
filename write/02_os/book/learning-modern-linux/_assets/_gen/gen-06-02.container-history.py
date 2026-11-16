# 06-02 §1 — 컨테이너 시도 다섯이 모두 같은 커널 재료 위에 서 있고, Docker 가 그 위에 얹은 둘이
#           OCI 핵심 명세 셋의 바탕이 된 구조.
# 원문("Containers"): "Containers are, per se, nothing new in Linux. However, they've enjoyed mainstream
#       adoption only due to Docker, starting in roughly 2014. Before that, we had a number of attempts
#       to introduce containers, often targeting system administrators rather than developers, including
#       the following: Linux-VServer (2001), OpenVZ (2005), LXC (2008), Let Me Contain That for You
#       (lmctfy) (2013)."
#       "What all of these approaches have in common is that they use the basic building blocks the Linux
#       kernel provides, such as namespaces or cgroups, to allow users to run applications."
#       "Docker innovated on the concept and introduced two groundbreaking elements: a standardized way
#       to define the packaging via container images and a human-friendly user interface (for example,
#       docker run)."
#       OCI 핵심 명세 셋 — Runtime(연산·생애 주기), Image format(메타데이터·층), Distribution(저장소 동작).
# 타입 스펙: type-timeline — 시간축 위의 사건. 그 아래에 모두가 딛는 커널 재료 띠, 위에 Docker 가 얹은 것과
#           그것이 바탕이 된 OCI 명세를 놓았다. accent 는 2014년 Docker 한 점.
# 축약: 시간축 간격은 연도 비례가 아니라 사건마다 같은 간격이다. 커널 기능 각각의 도입 시점은 §2 표에 있다.
#       본문은 Docker 가 누구를 겨냥했는지 따로 적지 않아, 시스템 관리자 대상이라는 표시는 앞의 넷에만 붙였다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 496
d = D(W, H, "LEARNING MODERN LINUX · 06-02 §1",
      "다섯 도구가 같은 커널 재료 위에 서 있다",
      "Linux-VServer(2001)·OpenVZ(2005)·LXC(2008)·lmctfy(2013)·Docker(2014) 가 모두 커널의 "
      "네임스페이스와 cgroups 를 써서 앱을 돌린다. 앞의 넷은 주로 시스템 관리자를 겨냥했다. Docker 는 "
      "그 위에 컨테이너 이미지라는 패키징 표준과 docker run 같은 사람 친화적 인터페이스를 얹었고, "
      "이것이 OCI 핵심 명세 셋(런타임·이미지 포맷·배포)의 바탕이 됐다.",
      "재료는 내내 같았고 바뀐 것은 그 위에 얹은 것입니다")

XS = [104 + i * 168 for i in range(5)]
BW = 144
AXY = 252                    # 시간축
TY, TH = 280, 44             # 도구 상자
KY, KH = 388, 40             # 커널 띠
SY, SH = 124, 72             # 위: OCI 명세 · Docker 가 얹은 것

# 연결선 먼저
for x in XS:
    d.line(x, TY + TH, x, KY, MUTED, 1.0)
d.path(f"M 40 {AXY} L 856 {AXY}", MUTED, 1.3, m="ar")
d.arrow([(XS[4] + 56, TY - 2), (XS[4] + 56, SY + SH + 6)], ACC, "acc", 1.4)
d.arrow([(XS[4] - BW / 2, SY + SH / 2), (XS[2] + BW / 2 + 4, SY + SH / 2)], OK, "ok", 1.4)
d.t((XS[3]), SY + SH / 2 - 10, "바탕", 12, OK, KR)

# 위: OCI 명세 셋
d.t(XS[0] - BW / 2, SY - 12, "OCI 핵심 명세 셋", 12, SOFT, KR, "start", 600)
for x, name, sub in zip(XS[:3], ("Runtime", "Image format", "Distribution"),
                        ("연산 · 생애 주기", "메타데이터 · 층", "저장소 동작")):
    d.tone(x - BW / 2, SY, BW, SH, OK)
    d.t(x, SY + 30, name, 13, OK, MONO, "middle", 600)
    d.t(x, SY + 52, sub, 12, MUTED, KR)

# 위: Docker 가 얹은 둘
d.t(XS[4] - BW / 2, SY - 12, "Docker 가 얹은 둘", 12, ACC, KR, "start", 600)
d.box(XS[4] - BW / 2, SY, BW, 32, PAPER2, ACC, 1.1, 6)
d.t(XS[4], SY + 21, "컨테이너 이미지", 12, INK, KR)
d.box(XS[4] - BW / 2, SY + 40, BW, 32, PAPER2, ACC, 1.1, 6)
d.t(XS[4], SY + 61, "$ docker run", 12, INK, MONO)

# 가운데: 시간축과 도구
tools = [("2001", "Linux-VServer"), ("2005", "OpenVZ"), ("2008", "LXC"),
         ("2013", "lmctfy"), ("2014", "Docker")]
for i, (x, (yr, name)) in enumerate(zip(XS, tools)):
    focal = (i == 4)
    c = ACC if focal else INFO
    d.o.append(f'<circle cx="{x}" cy="{AXY}" r="{8 if focal else 5}" fill="{c}" stroke="none"/>')
    d.t(x, AXY - 16, yr, 12.5, c, MONO, "middle", 600)
    if focal:
        d.o.append(f'<rect x="{x - BW / 2}" y="{TY}" width="{BW}" height="{TH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.tone(x - BW / 2, TY, BW, TH, INFO)
    d.t(x, TY + 27, name, 13, ACC if focal else INK, MONO, "middle", 600)

# 앞의 넷 묶음
BRY = TY + TH + 14
d.line(XS[0] - BW / 2, BRY, XS[3] + BW / 2, BRY, INFO, 1.0)
d.line(XS[0] - BW / 2, BRY - 6, XS[0] - BW / 2, BRY, INFO, 1.0)
d.line(XS[3] + BW / 2, BRY - 6, XS[3] + BW / 2, BRY, INFO, 1.0)
d.t((XS[1] + XS[2]) / 2, BRY + 20, "주로 시스템 관리자 대상", 12, INFO, KR)

# 아래: 커널 재료
d.box(24, KY, W - 48, KH, PAPER2, MUTED, 1.1, 6)
d.t(W / 2, KY + 25, "리눅스 커널 재료 — 네임스페이스 · cgroups", 13, INK, KR, "middle", 600)

d.legend(KY + KH + 24, [("같은 재료를 쓴 시도", INFO), ("Docker 가 얹은 것", ACC), ("OCI 명세", OK)])
d.save("06-02.container-history.svg")
print("ok 06-02.container-history", KY + KH + 24)
