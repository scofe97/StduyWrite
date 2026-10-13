# 타입 스펙: type-timeline — 연도 눈금(2003~2015, 1년 = 72px) 위에 구글 논문 셋과 그 뒤를 잇는 OLTP·OLAP·스트림·자원 관리 갈래의 논문·제품을 줄별로 놓는다. 눈금이 의미를 나르므로 간격은 실제 연도 그대로이고 같은 해 두 점은 아래 줄로 내린다.
# 사실 출처: GFS SOSP'03(2003), MapReduce OSDI 2004, Bigtable OSDI 2006, Hive VLDB'09(2009), Spark HotCloud'10(2010, usenix.org/legacy/event/hotcloud10), Dremel VLDB Vol.3 No.1(2010), Megastore CIDR'11(2011), Kafka NetDB'11(2011-06-12), Storm 오픈소스 공개 2011-09-19(Marz 글), Spanner OSDI 2012, 카파 Kreps 2014-07-02, Kubernetes 오픈소스 2014(kubernetes.io/docs/concepts/overview), Dataflow VLDB Vol.8 No.12(2015), Flink IEEE Data Eng. Bulletin(2015), Borg EuroSys'15(2015). 화살표: Borg→Kubernetes(Borg 논문 §8 "lessons from Borg are being applied to Kubernetes", ACM Queue 2016), Bigtable→Megastore→Spanner(Spanner 논문 §1, Megastore 논문), MapReduce→Hive(Hive 논문 §1), MapReduce→Spark(Spark 논문 §1).
# Layout conventions: x = 76 + 72·(연도-2003), 줄 기준선 y = 148·212·276(OLAP a)·332(OLAP b)·396(스트림 a)·452(스트림 b)·516, 이름은 기준선 아래 24, 줄 이름은 기준선과 같은 높이 왼쪽 끝, 연도 눈금 라벨 y=108. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 1000, 628
d = D(W, H, "BYTEBYTEGO · 05-02",
      "구글 논문 셋에서 세 갈래로",
      "연도 눈금 위에서 논문과 제품이 갈래별 줄로 나뉩니다. 2003년 GFS 부터 2015년 Borg 까지입니다",
      "연도는 논문 발표 또는 오픈소스 공개 시점입니다. 화살표는 한계를 이어받은 관계입니다")

X0, STRIDE = 76, 72


def xs(year):
    return X0 + STRIDE * (year - 2003)


def fam(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


# 연도 눈금 — 라벨과 줄을 가로지르는 점선
for yr in range(2003, 2016):
    d.t(xs(yr), 108, str(yr), 12, SOFT, MONO, "middle")
    d.line(xs(yr), 116, xs(yr), 564, RULE, 0.6, "2 4")

# 줄 구분선
for y in (188, 252, 372, 492):
    d.line(12, y, W - 40, y, RULE, 0.8)

# 줄 이름
tags = [(148, "뿌리", ACC), (212, "OLTP", INFO), (276, "OLAP", OK), (396, "스트림", WARN), (516, "자원", MUTED)]
for y, name, c in tags:
    d.t(12, y + 4, name, 13, c, fam(name), "start", 600)

# 줄 기준선
for y in (148, 212, 276, 332, 396, 452, 516):
    d.line(72, y, W - 40, y, RULE, 0.8)


def node(year, base, name, c, focal=False, sub=None):
    x = xs(year)
    if focal:
        d.o.append(f'<circle cx="{x}" cy="{base}" r="6" fill="{c}" stroke="{c}" stroke-width="1.4"/>')
    else:
        d.o.append(f'<circle cx="{x}" cy="{base}" r="5" fill="{PAPER}" stroke="{c}" stroke-width="1.4"/>')
    d.t(x, base + 24, name, 13, INK if not focal else c, fam(name), "middle", 600 if focal else 400)
    if sub:
        d.t(x, base + 44, sub, 13, MUTED, KR, "middle")


# 뿌리 논문 셋
node(2003, 148, "GFS", ACC, True)
node(2004, 148, "MapReduce", ACC, True)
node(2006, 148, "Bigtable", ACC, True)

# OLTP 갈래
node(2011, 212, "Megastore", INFO)
node(2012, 212, "Spanner", INFO)
# OLAP 갈래
node(2009, 276, "Hive", OK)
node(2010, 276, "Dremel", OK)
node(2010, 332, "Spark", OK)
# 스트림 처리 갈래
node(2011, 396, "Storm", WARN)
node(2014, 396, "카파", WARN)
node(2015, 396, "Dataflow", WARN)
node(2011, 452, "Kafka", WARN)
node(2015, 452, "Flink", WARN)
# 자원 관리
node(2014, 516, "Kubernetes", MUTED, sub="공개")
node(2015, 516, "Borg", MUTED, sub="논문")

# 한계를 이어받은 관계 — 모두 직각
d.arrow([(xs(2006), 180), (xs(2006), 212), (xs(2011) - 12, 212)], INFO, "info", 1.6)
d.arrow([(xs(2011) + 12, 212), (xs(2012) - 12, 212)], INFO, "info", 1.6)
d.arrow([(xs(2004), 180), (xs(2004), 276), (xs(2009) - 12, 276)], OK, "ok", 1.6)
d.arrow([(xs(2004), 276), (xs(2004), 332), (xs(2010) - 12, 332)], OK, "ok", 1.6)
# Borg 논문(2015)의 운영 경험이 Kubernetes(2014 공개)로 이어짐 — 오른쪽에서 왼쪽
d.arrow([(xs(2015) - 12, 516), (xs(2014) + 12, 516)], MUTED, "ar", 1.6)

d.legend(H - 44, [("뿌리 논문", ACC), ("OLTP 갈래", INFO), ("OLAP 갈래", OK), ("스트림 처리", WARN), ("자원 관리", MUTED)])
d.save("05-02.chapter-overview.svg")
