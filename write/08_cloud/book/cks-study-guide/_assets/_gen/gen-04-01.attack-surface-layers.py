# 04-01 핵심 요약 — 노드를 굳히는 일은 공격 표면을 줄이는 네 층으로 나뉜다. 본문 ### 1~4 의 순서와 같다.
# 본문 근거: 이 노트 「핵심 요약」과 본문 정리 ### 1~4 의 첫 문장.
# 검증 근거: ubuntu:24.04 컨테이너와 kind v1.35.0 노드에서 systemctl · apt purge · usermod · chown · chmod · ss · ufw ·
#            apparmor_parser · seccomp Localhost 프로파일을 실행해 동작을 확인했다.
# 타입 스펙: type-layers — 층마다 줄이는 대상과 쓰는 명령을 나란히 두고, 층 사이 화살표는 본문 순서를 뜻한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 330
d = D(W, H, "CKS STUDY GUIDE · 04-01 SUMMARY",
      "노드를 굳히는 네 층",
      "패키지와 서비스, 계정과 권한, 포트와 방화벽, 커널 도구의 네 층이 각각 무엇을 줄이고 어떤 명령을 쓰는지 나란히 보인 도식이다.",
      "층마다 줄이는 대상이 다르고 앞 층이 뚫려도 뒤 층이 피해 범위를 좁힙니다")

BW, BH, GAP, X0, Y0 = 196, 168, 24, 12, 96
layers = [
    ("패키지·서비스", "쓰지 않는 프로그램", "systemctl", "apt purge", INFO),
    ("계정·권한", "불필요한 로그인과 쓰기", "usermod · chown", "chmod", INFO),
    ("포트·방화벽", "밖에서 닿는 길", "ss -ltpn", "ufw", INFO),
    ("커널 도구", "침해 뒤에 할 수 있는 일", "AppArmor", "seccomp", ACC),
]
for i, (name, target, c1, c2, c) in enumerate(layers):
    x = X0 + i * (BW + GAP)
    d.tone(x, Y0, BW, BH, c, 6, "14", 1.4 if c == ACC else 1.1)
    d.t(x + BW / 2, Y0 + 30, name, 14, INK, KR, "middle", 600)
    d.line(x + 14, Y0 + 44, x + BW - 14, Y0 + 44, RULE, 0.8)
    d.t(x + 14, Y0 + 66, "줄이는 대상", 12, MUTED, KR, "start")
    d.t(x + 14, Y0 + 88, target, 12, INK, KR, "start")
    d.t(x + 14, Y0 + 118, "쓰는 명령", 12, MUTED, KR, "start")
    d.t(x + 14, Y0 + 140, c1, 12, INK, MONO, "start")
    d.t(x + 14, Y0 + 158, c2, 12, INK, MONO, "start")
    if i < 3:
        d.path(f"M {x + BW + 2} {Y0 + 84} L {x + BW + GAP - 2} {Y0 + 84}", MUTED, 1.4, m="ar")

d.legend(286, [("호스트 안에서 줄이기", INFO), ("마지막 방어선", ACC)])
d.save("04-01.attack-surface-layers.svg")
