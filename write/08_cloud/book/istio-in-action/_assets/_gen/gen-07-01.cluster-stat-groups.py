# 07-01 §3 되살린 클러스터 통계의 묶음별 비중 — 원문 7.2.1 이 지면에 실은 61 줄을 세어 옮겼다.
# 세는 법: ch07.txt 에서 "cluster.outbound|80||catalog." 로 시작하는 줄을 접두별로 분류.
#          circuit_breakers 5 · internal 2 · ssl 8 · upstream_cx 24 · upstream_rq 22 = 61.
# 저자는 "출력이 방대해 생략했다"고 적으므로 이 61 은 프록시가 가진 전량이 아니라 지면에 실린 부분집합이다.
# 타입 스펙: type-treemap — 전체가 부분으로 쪼개지고 상대 크기가 논점이다. 면적 = 지표 개수, 셀 5개(4~8),
#           squarified 근사로 종횡비를 1 근처에 두고, 모든 셀에 data-share, accent 는 한 셀에만.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, KR, MONO

W, H = 1000, 560
d = D(W, H, "ISTIO IN ACTION · 07-01 §3",
      "되살렸을 때 나오는 통계는 무엇에 쏠려 있나",
      "면적이 지표 개수다. 원문 7.2.1 이 catalog 클러스터로 필터해 지면에 실은 61 줄을 접두별로 세었다. "
      "색이 붙은 칸이 6장에서 서킷 브레이킹 발동을 확인하려면 필요했던 묶음이다.",
      "커넥션과 요청 통계 둘이 지면에 실린 것의 4분의 3을 차지합니다")

# 셀 — (라벨, 개수, 참 점유율(%), x, y, w, h, 설명, focal)
# 열 폭은 총량에 비례해 나눈 뒤 4의 배수로 스냅했다. 상대 오차는 모두 2% 미만.
cells = [
    ("upstream_cx_*",      24, 39.3,  40, 104, 356, 340, "커넥션 생성·파기·바이트", False, "29"),
    ("upstream_rq_*",      22, 36.1, 400, 104, 324, 340, "요청 상태·재시도·대기",   False, "21"),
    ("ssl.*",               8, 13.1, 728, 104, 228, 176, "TLS 여부와 암호 스위트",  False, "1A"),
    ("circuit_breakers.*",  5,  8.2, 728, 284, 228, 112, "6장이 읽어야 했던 것",    True,  None),
    ("internal.*",          2,  3.3, 728, 400, 228,  44, None,                      False, "0A"),
]

for name, cnt, share, x, y, w, h, desc, focal, op in cells:
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" data-share="{share}" '
                   f'fill="{ACC}29" stroke="{ACC}" stroke-width="1.5"/>')
    else:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" data-share="{share}" '
                   f'fill="{INK}{op}" stroke="{INK}4D" stroke-width="1"/>')
    col = ACC if focal else INK
    if h >= 100:
        d.t(x + 16, y + 30, name, 13, col, MONO, "start", 600)
        d.t(x + 16, y + 50, f"{cnt} · {share}%", 9, MUTED, MONO, "start")
        if desc:
            d.t(x + 16, y + 76, desc, 12, MUTED, KR, "start")
    else:
        d.t(x + 16, y + 28, name, 12, col, MONO, "start", 600)
        d.t(x + w - 16, y + 28, f"{cnt} · {share}%", 9, MUTED, MONO, "end")

d.legend(496, [("6장이 필요로 한 묶음", ACC), ("밝을수록 지표가 많음", INK)])
d.t(W - 48, 518, "AREA = 원문 7.2.1 리스팅의 지표 개수 · n=61", 8, SOFT, MONO, "end")
d.save("07-01.cluster-stat-groups.svg")
