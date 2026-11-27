# 06-03 §4 — quote-poststart 의 PostStart hook 과 nginx 서빙 흐름
# 본문: "lifecycle hook 에는 명령 여러 개를 직접 나열할 수 없으므로 sh -c 패턴을 씁니다."
#       "hook 이 완료되면 fortune 이 고른 인용문이 /usr/share/nginx/html/quote 에 저장되고 Nginx 가 서빙합니다."
#       "hook 호출이 완료될 때까지 컨테이너는 Waiting(ContainerCreating) · Pod 는 Pending"
#       "hook 이 0 이 아닌 종료 코드를 반환하면 컨테이너 전체 재시작 · FailedPostStartHook"
# 타입 스펙: type-flowchart.md — 타원(시작/끝), 사각형(단계), 마름모(종료코드 판정), 점(합류).
#           종료 코드 exit 0 여부가 컨테이너 재시작/Running 을 가르는 핵심 분기라 마름모만 focal.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 748
d = D(W, H, "KUBERNETES IN ACTION · 06-03",
      "postStart 는 nginx 와 병렬 시작 · exit 0 뒤 서빙",
      "컨테이너 생성 직후 sh -c 로 실행된 postStart hook 이 fortune 결과를 /usr/share/nginx/html/quote 에 쓴다. "
      "실패(exit ≠ 0)하면 컨테이너가 재시작되고, 성공해야 Pod 가 Running 으로 넘어가 HTTP :80 을 서빙한다.",
      lead="hook 실행 중에도 nginx 는 이미 기동 중 · 단 hook 완료 전까지 Pod 는 Pending")

ddx.band(d, 104, 688, "quote-poststart (nginx:alpine · containerPort 80)")

def oval(cx, cy, w, h, txt, sub, c):
    d.o.append(f'<rect x="{cx-w//2}" y="{cy-h//2}" width="{w}" height="{h}" rx="{h//2}" '
               f'fill="{c}14" stroke="{c}" stroke-width="1.2"/>')
    if sub:
        d.t(cx, cy - 4, ddx.fit(txt, 13, w - 24, txt), 13, c, KR, "middle", 600)
        d.t(cx, cy + 14, ddx.fit(sub, 11, w - 24, sub), 11, MUTED, MONO)
    else:
        d.t(cx, cy + 5, ddx.fit(txt, 13, w - 24, txt), 13, c, KR, "middle", 600)

def step(cx, cy, w, h, title, sub1, sub2, c):
    d.box(cx - w // 2, cy - h // 2, w, h, PAPER2, c, 1.1, 6)
    if sub2:
        d.t(cx, cy - 18, ddx.fit(title, 13, w - 16, title), 13, c,
            MONO if all(ord(ch) < 128 for ch in title) else KR, "middle", 600)
        d.t(cx, cy + 4, ddx.fit(sub1, 11, w - 16, sub1), 11, MUTED,
            MONO if all(ord(ch) < 128 for ch in sub1) else KR)
        d.t(cx, cy + 22, ddx.fit(sub2, 11, w - 16, sub2), 11, SOFT,
            MONO if all(ord(ch) < 128 for ch in sub2) else KR)
    else:
        d.t(cx, cy - 8, ddx.fit(title, 13, w - 16, title), 13, c,
            MONO if all(ord(ch) < 128 for ch in title) else KR, "middle", 600)
        d.t(cx, cy + 14, ddx.fit(sub1, 11, w - 16, sub1), 11, MUTED,
            MONO if all(ord(ch) < 128 for ch in sub1) else KR)

# Nodes
START = (500, 160, 280, 48)
HOOK = (240, 268, 320, 84)
NGINX_UP = (760, 268, 300, 84)
DIA = (240, 396, 108, 42)
FAIL = (240, 520, 300, 68)
FILE = (516, 396, 200, 68)
MERGE = (760, 396)
SERVE = (760, 520, 300, 68)
END = (760, 616, 260, 44)

oval(*START, "컨테이너 생성", "nginx:alpine · :80", INFO)

# Split to parallel branches (postStart hook | nginx main)
d.path(f"M {START[0]} {START[1]+24} L {START[0]} 204", MUTED, 1.5)
d.path(f"M {START[0]} 204 L {HOOK[0]} 204 L {HOOK[0]} {HOOK[1]-42-6}", INFO, 1.5, m="info")
d.path(f"M {START[0]} 204 L {NGINX_UP[0]} 204 L {NGINX_UP[0]} {NGINX_UP[1]-42-6}", WARN, 1.5, m="warn")
d.chip(500, 204, "병렬 실행", INFO, 11)

step(*HOOK, "postStart exec (sh -c)",
     "apk add fortune · curl -fSL (5s/30s)", "fortune > /usr/share/nginx/html/quote", INFO)

step(*NGINX_UP, "nginx 메인 프로세스 기동",
     "Waiting (ContainerCreating)", "Pod Pending · logs/port-forward 대기", WARN)

# Hook -> Decision diamond
d.path(f"M {HOOK[0]} {HOOK[1]+42+4} L {HOOK[0]} {DIA[1]-DIA[3]-6}", MUTED, 1.5, m="ar")
dx, dy = DIA[2], DIA[3]
d.o.append(f'<path d="M {DIA[0]} {DIA[1]-dy} L {DIA[0]+dx} {DIA[1]} L {DIA[0]} {DIA[1]+dy} '
           f'L {DIA[0]-dx} {DIA[1]} Z" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(DIA[0], DIA[1] + 5, "hook exit 0 ?", 13, ACC, MONO, "middle", 600)

# Exit != 0 (down) -> FailedPostStartHook
d.path(f"M {DIA[0]} {DIA[1]+dy+4} L {DIA[0]} {FAIL[1]-34-6}", BAD, 1.5, m="bad")
d.chip(DIA[0], 458, "exit ≠ 0", BAD, 11)
step(*FAIL, "FailedPostStartHook", "Warning 이벤트 · 컨테이너 전체 재시작", None, BAD)

# Exit == 0 (right) -> quote file -> Merge dot
d.path(f"M {DIA[0]+dx+4} {DIA[1]} L {FILE[0]-100-6} {DIA[1]}", OK, 1.6, m="ok")
d.chip(382, DIA[1], "0", OK, 11)
step(*FILE, ".../html/quote", "인용문 파일 생성 완료", None, OK)

# Merge dot (nginx up + quote file -> serve)
d.path(f"M {FILE[0]+100+4} {FILE[1]} L {MERGE[0]-10} {FILE[1]}", OK, 1.6, m="ok")
d.path(f"M {NGINX_UP[0]} {NGINX_UP[1]+42+4} L {NGINX_UP[0]} {MERGE[1]-10}", WARN, 1.5, m="warn")
d.o.append(f'<circle cx="{MERGE[0]}" cy="{MERGE[1]}" r="5" fill="{INK}"/>')

# Merge -> Serve -> End
d.path(f"M {MERGE[0]} {MERGE[1]+6} L {MERGE[0]} {SERVE[1]-34-6}", OK, 1.6, m="ok")
step(*SERVE, "nginx HTTP :80 서빙", "port-forward 1080:80 응답", None, OK)
d.path(f"M {SERVE[0]} {SERVE[1]+34+4} L {SERVE[0]} {END[1]-22-6}", OK, 1.6, m="ok")
oval(*END, "Pod Running · READY 1/1", None, OK)

d.t(36, 668, "hook 성공 출력은 미기록 (파일 저장 필요) · 자기 컨테이너 httpGet hook 은 재시작 루프 위험",
     12, MUTED, KR, "start")
d.legend(704, [("생성 · 훅 실행", INFO), ("완료 전 대기", WARN), ("종료 코드 판정", ACC),
               ("서빙 · Running", OK), ("실패 · 재시작", BAD)])
d.save("06-03-poststart-fortune-flow.svg")
print("ok poststart-fortune-flow")
