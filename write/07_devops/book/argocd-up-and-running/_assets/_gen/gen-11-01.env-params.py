# 11-01 §2 — generate 프로세스는 사이드카 OS 환경, Argo CD 빌드 환경(ARGOCD_APP_*), plugin.env 의 ARGOCD_ENV_<이름>, parameters 의 PARAM_<이름>·ARGOCD_APP_PARAMETERS 를 읽는다. plugin.yaml 이 알린(announce) 기본값은 UI 의 Parameters 탭에만 쓰이고 generate 로 전달되지 않는다.
# 본문 근거: 이 노트 ### 2 「플러그인에 값 넘기기와 운영 설정」.
# 검증 근거: kind v0.31.0 에 Argo CD v3.6.1 을 설치하고 echo-demo 플러그인의 generate 가 환경 변수를 ConfigMap 으로 찍게 해 확인했다.
#            plugin.env FOO=bar 는 ARGOCD_ENV_FOO 로 보였고 접두사 없는 FOO 는 비어 있었다. REV=test-$ARGOCD_APP_REVISION_SHORT 는 test-8088f4c 로 풀렸다.
#            parameters 의 string 은 PARAM_GREETING, array 는 PARAM_LIST_0·PARAM_LIST_1, map 은 PARAM_LABELS_TEAM·PARAM_LABELS_TIER 였고 ARGOCD_APP_PARAMETERS 에는 parameters 배열만 JSON 으로 담겼다.
#            plugin.yaml 의 static·dynamic 기본값만 있고 Application 에 parameters 를 주지 않은 첫 실행에서는 PARAM_* 가 모두 unset 이었다.
# 공식 근거: argo-cd v3.6.1 docs/operator-manual/config-management-plugins.md("Using environment variables in your plugin", "Plugin parameters"), docs/user-guide/build-environment.md.
# 타입 스펙: type-architecture — 왼쪽 값의 출처 네 가지에서 가운데 generate 로 모이는 흐름, 가운데에서 오른쪽 UI 로 가는 점선 한 가지(전달 아님).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 488
d = D(W, H, "ARGO CD UP AND RUNNING · 11-01 §2",
      "generate 프로세스가 읽는 값의 출처",
      "왼쪽 네 칸은 generate 프로세스가 읽는 값의 출처이다. 사이드카 OS 환경과 Argo CD 가 채우는 ARGOCD_APP_* 빌드 환경과 Application 의 plugin.env 에서 온 ARGOCD_ENV_ 접두사 변수와 parameters 에서 온 PARAM_ 변수와 ARGOCD_APP_PARAMETERS 가 가운데 generate 로 모인다. "
      "같은 값이 init 과 discover.find.command 에도 전달된다. "
      "오른쪽 UI Parameters 탭은 plugin.yaml 이 알린 기본값을 보여 주기만 하고 그 값은 generate 로 전달되지 않는다.",
      "plugin.yaml 의 기본값은 화면 표시용이고 generate 로 가는 값은 Application 에 적은 것입니다")

SX, SW = 24, 300
CX, CW = 408, 200
UX, UW = 692, 164
rows = [
    (104, SOFT, "사이드카 OS 환경", "PATH, HOME 같은 컨테이너 값"),
    (174, INFO, "Argo CD 빌드 환경", "ARGOCD_APP_NAME, ARGOCD_APP_REVISION"),
    (244, ACC, "plugin.env", "ARGOCD_ENV_<이름>"),
    (314, ACC, "parameters", "PARAM_<이름>, ARGOCD_APP_PARAMETERS"),
]
for y, c, t1, t2 in rows:
    if c == SOFT:
        d.box(SX, y, SW, 56, PAPER2, RULE, 1.0)
    else:
        d.tone(SX, y, SW, 56, c, 6, "14", 1.2)
    d.t(SX + SW / 2, y + 23, t1, 12.5, INK, KR, "middle", 600)
    d.t(SX + SW / 2, y + 44, t2, 11, MUTED, MONO)
    d.path(f"M {SX + SW + 2} {y + 28} L {CX - 2} {y + 28}", MUTED, 1.4, m="ar")

# generate
GY, GH = 104, 266
d.tone(CX, GY, CW, GH, OK, 6, "14", 1.4)
d.t(CX + CW / 2, GY + 36, "generate 프로세스", 12.5, INK, KR, "middle", 600)
d.t(CX + CW / 2, GY + 70, "plugin.yaml 의", 12, MUTED)
d.t(CX + CW / 2, GY + 92, "command, args", 11.5, MUTED, MONO)
d.t(CX + CW / 2, GY + 134, "읽은 환경 변수로", 12, MUTED)
d.t(CX + CW / 2, GY + 156, "stdout 에 YAML 을 찍는다", 12, MUTED)
d.t(CX + CW / 2, GY + GH + 26, "init·find.command 도 같은 값", 11.5, MUTED)

# UI 탭 (전달 아님)
d.box(UX, 104, UW, 100, PAPER2, RULE, 1.0)
d.t(UX + UW / 2, 134, "UI Parameters 탭", 12.5, INK, KR, "middle", 600)
d.t(UX + UW / 2, 158, "알린 기본값을 표시", 12, MUTED)
d.t(UX + UW / 2, 180, "static · dynamic", 11.5, MUTED, MONO)
d.path(f"M {CX + CW + 2} 154 L {UX - 2} 154", SOFT, 1.4, m="soft", dash="5 4")
d.chip((CX + CW + UX) / 2, 134, "표시만", SOFT, 11)

d.tone(UX, 240, UW, 70, BAD, 6, "14", 1.2)
d.t(UX + UW / 2, 270, "전달되지 않음", 12.5, INK, KR, "middle", 600)
d.t(UX + UW / 2, 292, "적은 값만 전달", 12, MUTED)

d.legend(448, [("OS", PAPER2), ("빌드 환경", INFO), ("사용자 입력", ACC), ("generate", OK), ("표시만", PAPER2), ("전달 안 됨", BAD)])
d.save("11-01.env-params.svg")
