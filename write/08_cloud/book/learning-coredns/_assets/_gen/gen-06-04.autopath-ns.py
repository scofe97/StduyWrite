# 06-04 §5 「대가는 다시 메모리입니다」 — autopath 가 질의 하나를 받아 출발지 IP 로 네임스페이스를 찾고 검색 경로를 서버 안에서 도는 단계.
# README 근거(autopath, master, 2026-10-03 대조): "If the autopath plugin sees a query that matches the first element of the
#            configured search path, it will follow the chain of search path elements and return the first reply that is not
#            NXDOMAIN. On any failures, the original reply is returned." / "it relies on the kubernetes plugin's Pod cache to
#            resolve the client's IP address to a Pod."
# 예시 값: 출발지 192.0.2.7(문서용 주소)·네임스페이스 default 는 설명용이다. 응답 줄은 이 노트 §5 의 원서 출력 그대로.
# 타입 스펙: type-process — 질의가 단계 다섯을 차례로 지나고, 둘째 단계가 메모리를 요구하는 자리라는 것이 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, KR, MONO

W, H = 1000, 480
d = D(W, H, "LEARNING COREDNS · 06-04 §5",
      "출발지 IP 로 네임스페이스를 찾아야 검색 경로를 돈다",
      "autopath 는 질의가 검색 경로의 첫 항목으로 끝날 때만 움직인다. 출발지 IP 를 파드 캐시에서 찾아 네임스페이스를 알아내고, "
      "그 네임스페이스의 검색 경로를 서버 안에서 돌아 NXDOMAIN 이 아닌 첫 답을 CNAME 과 함께 돌려준다.",
      "주황 단계가 pods verified 를 요구하는 자리입니다")

steps = [
    ("1 · 질의 도착", ["example.com.default", ".svc.cluster.local", "출발지 192.0.2.7"], False),
    ("2 · 파드 캐시 조회", ["192.0.2.7", "= default 의 파드", "pods verified 가 채운 캐시"], True),
    ("3 · 검색 경로 세우기", ["default.svc.cluster.local", "svc.cluster.local", "cluster.local · 호스트"], False),
    ("4 · 서버 안에서 돌기", ["후보마다 내부 조회", "NXDOMAIN 이 아닌", "첫 답에서 멈춤"], False),
    ("5 · 응답", ["CNAME example.com.", "A 93.184.216.34", "왕복은 한 번"], False),
]
# 셋째 칸만 넓힌다 — default.svc.cluster.local(25자 mono)이 180 폭 칸을 넘었다(2026-10-03 렌더 확인)
BWS = [170, 170, 220, 170, 170]
BH, Y = 170, 140
XS = [20]
for w in BWS[:-1]:
    XS.append(XS[-1] + w + 12)

for i, (title, lines, focal) in enumerate(steps):
    x = XS[i]
    BW = BWS[i]
    if focal:
        d.tone(x, Y, BW, BH, ACC, 8, "12", 1.4)
    else:
        d.box(x, Y, BW, BH, PAPER2, RULE, 1.0, 8)
    d.t(x + 12, Y + 28, title, 13, ACC if focal else INK, KR, "start", 600)
    for j, ln in enumerate(lines):
        is_mono = not any("가" <= ch <= "힣" for ch in ln)
        d.t(x + 12, Y + 70 + j * 36, ln, 12, (ACC if focal and j == 2 else (INK if j < 2 else MUTED)),
            MONO if is_mono else KR, "start", 600 if j == 0 else 400)
    if i < 4:
        d.path(f"M {x + BW + 1} {Y + BH / 2} L {XS[i + 1] - 2} {Y + BH / 2}", MUTED, 1.2, m="ar")

d.t(20, 360, "첫 항목으로 안 끝나는 질의 · 그대로 통과 · 도중 실패 · 원래 응답", 13, MUTED, KR, "start")
d.t(20, 386, "알려진 버그 · IP 재할당이 watch 보다 빠르면 옛 네임스페이스의 검색 경로", 13, MUTED, KR, "start")

d.legend(420, [("pods verified 를 요구하는 단계", ACC)])
d.save("06-04.autopath-ns.svg")
