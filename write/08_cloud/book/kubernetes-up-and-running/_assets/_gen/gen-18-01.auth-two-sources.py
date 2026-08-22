# 18-01 §인증 — 출처는 둘뿐입니다
# 본문이 "클라이언트가 인증 정보를 얻는 자리는 둘뿐" 이라 못 박으므로, 여러 방식을 나열하는
# 그림이 아니라 *갈림길 하나* 여야 한다. 갈림의 기준도 본문이 준다 — 코드가 클러스터 밖에서
# 도는가 안에서 도는가. 그래서 질문을 위에 두고 아래로 두 갈래만 낸다.
# 두 갈래에 같은 세 칸(읽는 것 · 클라이언트 호출 · 걸리는 자리)을 같은 높이로 두어야
# 대조가 형태로 보인다. 오른쪽 걸리는 자리는 이 노트가 실측한 403 이라 초점을 준다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, MUTED, SOFT, INK, PAPER2, PAPER, RULE, INFO, KR, MONO
import ddx

W, H = 1240, 664
d = D(W, H, "KUBERNETES UP AND RUNNING · 18-01",
      "인증 정보가 오는 자리는 둘뿐이다",
      "API 서버가 HTTP 서버이므로 인증도 HTTP 의 것이다. 클라이언트는 kubeconfig 파일에서 "
      "읽거나 Pod 의 컨텍스트에서 조립한다.",
      "kind 로컬 클러스터 실측 — 오른쪽 아래 403 은 실제로 받은 응답이다")

QY = 116
# 갈림길 칩이 곧 분기점이다. 칩 아래에서 두 갈래를 내면 패널 윗변(152)까지 14px 뿐이라
# 줄기를 세울 자리가 없다 — 그래서 칩의 좌·우 변에서 옆으로 나가 각 패널의 중심 열에서
# 아래로 꺾는다. 칩 폭은 dd.chip 과 같은 셈(한글 1em + pad 7 양쪽)으로 구한다.
QTXT = "코드가 어디서 도는가"
QW = len(QTXT) * 11.0 + 14
d.chip(W / 2, QY, QTXT, SOFT, 11)

PW, PX = 590, (24, 626)
Y0, CH = 152, 384
Y1 = Y0 + CH

PANELS = [
    ("밖에서 돈다", "kubeconfig 파일", INFO,
     [("$KUBECONFIG", "있으면 기본 위치보다 우선한다"),
      ("${HOME}/.kube/config", "기본 위치"),
      ("외부 실행 파일", "클라우드는 이것이 토큰을 만든다")],
     [("config.load_kube_config()", "Python"),
      ("Config.defaultClient()", "Java"),
      ("KubernetesClientConfiguration.BuildDefaultConfig()", ".NET")],
     WARN, "토큰을 만드는 실행 파일이 없다",
     "코드를 컨테이너로 옮기면 CLI 도구가 따라오지 않는다"),
    ("안에서 돈다", "Pod 의 컨텍스트", ACC,
     [("/var/run/secrets/…/token", "ServiceAccount 토큰"),
      ("/var/run/secrets/…/ca.crt", "인증 기관 인증서"),
      ("kubernetes.default.svc", "고정 DNS 이름 · 10.96.0.1:443")],
     [("config.load_incluster_config()", "Python"),
      ("ClientBuilder.cluster().build()", "Java"),
      ("KubernetesClientConfiguration.InClusterConfig()", ".NET")],
     BAD, "기본 ServiceAccount 는 403 이다",
     "인증은 통과했고 인가에서 막힌 것이다"),
]

for (x, (eb, title, c, reads, calls, wc, whead, wsub)) in zip(PX, PANELS):
    d.box(x, Y0, PW, CH, PAPER2, c, 1.2, 8)
    d.t(x + 20, Y0 + 26, eb, 12, c, KR, "start", 600)
    d.t(x + PW - 20, Y0 + 26, title, 11, MUTED, KR, "end")
    d.line(x + 20, Y0 + 42, x + PW - 20, Y0 + 42, RULE, 0.8)
    col = x + PW / 2
    d.arrow([(W / 2 + (QW / 2 if col > W / 2 else -QW / 2), QY), (col, QY), (col, Y0 - 10)],
            c, "acc" if c is ACC else "info", 1.3)

    d.t(x + 20, Y0 + 66, "읽는 것", 9, SOFT, KR, "start")
    for j, (k, v) in enumerate(reads):
        yy = Y0 + 78 + j * 32
        d.box(x + 20, yy, PW - 40, 26, PAPER, RULE, 0.8, 4)
        # 한글을 mono 로 찍으면 자간이 벌어진다 (스타일 계약 타이포그래피)
        kf = MONO if all(ord(ch) < 128 for ch in k) else KR
        d.t(x + 32, yy + 17, ddx.fit(k, 11, 250, k), 11, c, kf, "start")
        d.t(x + PW - 32, yy + 17, ddx.fit(v, 10, 250, v), 10, MUTED, KR, "end")

    d.t(x + 20, Y0 + 190, "클라이언트 호출", 9, SOFT, KR, "start")
    for j, (k, v) in enumerate(calls):
        yy = Y0 + 202 + j * 32
        d.box(x + 20, yy, PW - 40, 26, PAPER, RULE, 0.8, 4)
        d.t(x + 32, yy + 17, ddx.fit(k, 10, 420, k), 10, INK, MONO, "start")
        d.t(x + PW - 32, yy + 17, v, 9, SOFT, MONO, "end")

    d.o.append(f'<rect x="{x+20}" y="{Y0+312}" width="{PW-40}" height="56" rx="5" '
               f'fill="{wc}12" stroke="{wc}" stroke-width="1.2"/>')
    d.t(x + PW / 2, Y0 + 336, ddx.fit(whead, 12, PW - 80, whead), 12, wc, KR, "middle", 600)
    d.t(x + PW / 2, Y0 + 356, ddx.fit(wsub, 10, PW - 80, wsub), 10, wc, KR)

BY = Y1 + 30
d.line(24, BY, W - 48, BY, RULE, 0.8)
d.t(24, BY + 24, "어느 쪽이든 인증을 통과하는 것과 리소스를 읽을 권한을 갖는 것은 다른 일이다. "
                 "기본 ServiceAccount 로 버전 조회는 되고 Pod 목록은 안 된다.",
    11, MUTED, KR, "start")
d.legend(BY + 40, [("클러스터 밖", INFO), ("클러스터 안", ACC),
                   ("환경이 달라지면 깨진다", WARN), ("실측한 거부", BAD)])
d.save("../18-01.auth-two-sources.svg")
print("필요 h:", BY + 40 + 48, "· 실제:", H)
