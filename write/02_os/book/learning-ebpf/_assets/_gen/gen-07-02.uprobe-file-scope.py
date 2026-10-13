# 타입 스펙: type-architecture — 위 uprobe 프로그램 하나, 가운데 파일 셋(호스트 파일시스템의 libssl.so.3 · 컨테이너 A 의 다른 복사본 · 정적 링크 앱), 아래 같은 커널 띠. focal 은 프로브가 걸리는 호스트 파일.
# 사실 출처: libbpf v7.2 tools/lib/bpf/libbpf.c L13281~13289(섹션 형식 u[ret]probe/binary:function[+offset]),
#   커널 v7.2 kernel/trace/trace_uprobe.c L1105~1109(d_real_inode 로 얻은 inode 에 uprobe_register), 경로 문자열은 본문 §1 예제와 같다.
# Layout conventions: 존 셋 w=288 stride 304 x=24·328·632 y=196, 커널 띠 y=404. 연결선은 직각, 모든 좌표 4의 배수.
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 556
d = D(W, H, "LEARNING EBPF · 07-02 §1", "같은 SSL_write 를 가리켜도 프로브가 걸리는 파일은 하나뿐이다",
      "uprobe 는 경로 문자열이 아니라 그 경로가 가리키는 파일(inode)에 등록된다. 호스트의 libssl.so.3 에는 걸리고, 컨테이너 A 의 다른 복사본과 정적 링크 앱에는 걸리지 않는다.",
      "세 파일 모두 같은 커널 위에서 돕니다")

ZX = (24, 328, 632)
ZW, ZY, ZH = 288, 196, 164

# 연결선 먼저 — 위 프로그램 상자에서 세 파일로
BX, BY, BW, BH = 24, 100, 560, 52
cx = [x + ZW // 2 for x in ZX]
d.arrow([(cx[0], BY + BH), (cx[0], ZY - 4)], OK, "ok", 1.7)
d.arrow([(cx[0] + 80, BY + BH), (cx[0] + 80, 172), (cx[1], 172), (cx[1], ZY - 4)], BAD, "bad", 1.5, "5 4")
d.arrow([(cx[0] + 140, BY + BH), (cx[0] + 140, 164), (cx[2], 164), (cx[2], ZY - 4)], BAD, "bad", 1.5, "5 4")

d.box(BX, BY, BW, BH, PAPER2, RULE, 1.0, 6)
d.t(BX + 16, BY + 22, "uprobe 프로그램", 13, INK, KR, "start", 600)
d.t(BX + 16, BY + 42, 'SEC("uprobe//usr/lib/aarch64-linux-gnu/libssl.so.3:SSL_write")', 11, MUTED, MONO, "start")

zones = [
    ("호스트 파일시스템", "/usr/lib/aarch64-linux-gnu/libssl.so.3", "SSL_write", "프로브 걸림", OK, True),
    ("컨테이너 A 파일시스템", "/usr/lib/aarch64-linux-gnu/libssl.so.3", "같은 이름, 다른 파일", "프로브 안 걸림", BAD, False),
    ("정적 링크 앱", "실행 파일 안에 libssl 포함", "공유 라이브러리 없음", "프로브 안 걸림", BAD, False),
]
for x, (zn, f, sub, verdict, c, focal) in zip(ZX, zones):
    d.tone(x, ZY, ZW, ZH, c, 8, "1F" if focal else "10", 1.4 if focal else 1.2)
    d.t(x + 16, ZY + 26, zn, 13, c, KR, "start", 600)
    d.line(x + 12, ZY + 38, x + ZW - 12, ZY + 38, RULE, 0.8)
    d.t(x + ZW // 2, ZY + 72, f, 11, INK, MONO if "/" in f else KR)
    d.t(x + ZW // 2, ZY + 96, sub, 12, MUTED, MONO if sub.isascii() else KR)
    d.chip(x + ZW // 2, ZY + 132, verdict, c, 12)

# 커널 띠
d.box(24, 404, 896, 52, PAPER2, RULE, 1.0, 6)
d.t(40, 426, "커널", 13, INK, KR, "start", 600)
d.t(40, 444, "uprobe 등록 단위는 파일(inode)", 12, MUTED, KR, "start")
for x in cx:
    d.arrow([(x, ZY + ZH), (x, 400)], RULE, "ar", 1.0)

d.legend(H - 56, [("프로브 걸림", OK), ("프로브 안 걸림", BAD)])
d.save("07-02.uprobe-file-scope.svg")
