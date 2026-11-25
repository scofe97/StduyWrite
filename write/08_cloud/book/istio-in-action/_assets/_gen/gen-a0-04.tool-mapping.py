# a0-04 §6 도구가 그 아래에서 무엇을 부르나 + ControlZ 여덟 항목.
# 본문(부록 D.2.1 끝 & D.2.2): "usually use the endpoints indirectly through other tools such as
#   Kiali, istioctl ... istioctl proxy-status uses /debug/syncz". ControlZ 는 9876, 여덟 항목,
#   가장 흔한 쓰임은 로깅 스코프 변경. (Istio 1.32: proxy-status 는 --xds-port 15012 직접 조회도 지원.)
# 타입 스펙: type-process — 도구(1열) -> 전달 경로(2열) -> 조회 대상(3열)의 세 행 프로세스 흐름.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER2, RULE, KR, MONO

W, H = 960, 560
d = D(W, H, "ISTIO IN ACTION · A0-04 §6",
      "운영 도구가 뒤에서 부르는 경로와 ControlZ",
      "평소에는 istioctl 이나 Kiali 가 디버그 엔드포인트와 ControlZ 를 대신 부른다. "
      "첫 행이 동기화 확인 경로이고, 셋째 행은 9876 을 여는 ControlZ 경로다.",
      lead="도구가 답을 못 줄 때만 엔드포인트를 직접 파고듭니다")

COLS = [(36, 260, "01 · 운영 도구"), (348, 256, "02 · 전달 경로"), (656, 268, "03 · 조회 대상")]
for x, w, title in COLS:
    d.t(x + w / 2, 118, title, 13, SOFT, KR, "middle", 600)
    d.line(x, 128, x + w, 128, RULE, 0.8)

ROWS = [
    (144, "istioctl proxy-status", "동기화 상태 확인",
          "xDS (15012) 또는 HTTP 8080", "끄기 전에 대체 경로 확인",
          "/debug/syncz", "nonce 비교 · SYNCED 판정", ACC, True),
    (232, "Kiali · istioctl", "메시 시각화 · 분석",
          "8080 HTTP / xDS", "직접 파고들기 전 1차 창구",
          "그 밖의 /debug/*", "메시 상태 · 데이터 플레인 설정", None, False),
    (320, "istioctl dashboard", "controlz 하위 명령",
          "port-forward 9876", "localhost 인트로스펙션",
          "ControlZ 웹 UI", "로깅 스코프 변경 · 프로세스 상태", INFO, False),
]

for y, t1, s1, t2, s2, t3, s3, c, focal in ROWS:
    H_ROW = 68
    for idx, (x, w, _) in enumerate(COLS):
        title, sub = [(t1, s1), (t2, s2), (t3, s3)][idx]
        if focal and idx in (0, 2):
            d.tone(x, y, w, H_ROW, ACC, 6, "12", 1.4)
            tc = ACC
        elif c and idx == 2:
            d.tone(x, y, w, H_ROW, c, 6, "12", 1.2)
            tc = c
        else:
            d.box(x, y, w, H_ROW, PAPER2, RULE, 1.0, 6)
            tc = INK
        fam1 = KR if any("가" <= ch <= "힣" for ch in title) else MONO
        d.t(x + 16, y + 28, title, 13, tc, fam1, "start", 600)
        d.t(x + 16, y + 52, sub, 13, MUTED, KR, "start")

    ym = y + H_ROW / 2
    mc = "acc" if focal else ("info" if c == INFO else "ar")
    ac = ACC if focal else (INFO if c == INFO else MUTED)
    dash = "4 3" if (not focal and c is None) else None
    d.arrow([(296, ym), (346, ym)], ac, mc, 1.4, dash=dash)
    d.arrow([(604, ym), (654, ym)], ac, mc, 1.4, dash=dash)

CY = 416
d.box(36, CY, 888, 68, PAPER2, RULE, 1.0, 6)
d.t(52, CY + 26, "ControlZ 여덟 항목 (주 용도: 로깅 스코프 변경)", 13, INFO, KR, "start", 600)
d.t(52, CY + 50, "로깅 스코프 · 메모리 사용량 · 환경변수 · 프로세스 정보 · 명령줄 인자 · 버전 정보 · 메트릭 · 시그널(SIGUSR1)", 13, INK, KR, "start")

d.legend(508, [("SYNCED 판정 핵심 경로", ACC), ("로깅 스코프 · 프로세스 조회", INFO)])
d.save("a0-04.tool-mapping.svg")
print("ok a0-04.tool-mapping")
