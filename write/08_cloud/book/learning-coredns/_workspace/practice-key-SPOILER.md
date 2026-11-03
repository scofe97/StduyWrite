# 1~4장 실습 진행 메모 (스포일러 — 학습자는 열지 않기)

진행 창이 시나리오를 낼 때 쓰는 메모입니다. 원인·정답·확인된 출력이 들어 있어 학습자가 먼저 읽으면 실습의 예측 단계가 사라집니다.

- 확인 환경: Docker `coredns/coredns:1.15.0`(linux/arm64), 맥북 dig 9.10.6, 2026-11-02. 확인할 때는 10.x 주소를 썼고, 실습에서는 문서용 대역으로 바꿔 냅니다(동작 동일).
- 학습자 실행은 brew 의 네이티브 `coredns` 로 합니다. 진행 순서: 신고 → 설정 조각 보여 주고 학습자가 입력(진행 창이 `cat` 으로 오타만 확인) → 원인·출력 예측 → 학습자 실행 → 채점 → 학습자가 고침 → 재확인.
- 주소 계획: ns1 `198.51.100.53`, db 옛 `198.51.100.10` → 새 `198.51.100.20`, coupon `198.51.100.30`, api `198.51.100.40`, hosts 덮어쓰기 `198.51.100.99`, 죽은 상위 DNS `192.0.2.1`.

## 공통 존 파일 (`db.shop.example`)

```
$TTL 30
@   IN SOA ns1.shop.example. admin.shop.example. 2026110201 1h 15m 7d 20
    IN NS  ns1.shop.example.
ns1 IN A   198.51.100.53
db  IN A   198.51.100.10
```

## S1 — DB 장애조치 후 옛 IP (file 다시 읽기)

- 설정: `shop.example { file db.shop.example { reload 2s } log }`
- 재현: db IP 를 `.20` 으로 고치되 시리얼은 그대로 → 몇 초 뒤 `dig` 해도 `.10`.
- 확인된 출력: 시리얼 그대로면 계속 `.10`, 로그에 reload 줄 없음. 시리얼을 `2026110202` 로 올리면 `[INFO] plugin/file: Successfully reloaded zone "shop.example." in "db.shop.example" with 2026110202 SOA serial` 뒤 `.20`.
- 원인: `file` 은 파일 내용이 아니라 SOA 시리얼이 달라졌을 때만 다시 읽는다. 관측 손잡이: `dig ... SOA +short` 로 서버가 들고 있는 시리얼 보기.
- 노트: `04-01` §2 reload, `02-02` SOA 시리얼.

## S2 — 고쳤는데 일부는 옛 IP (cache)

- 설정: S1 블록 맨 위에 `cache` 추가(플러그인 순서는 Corefile 이 아니라 plugin.cfg 순서라 위치 무관).
- 재현: db 를 한 번 조회(캐시에 들어감) → IP·시리얼 함께 고침 → 다시 조회.
- 확인된 출력: 고친 뒤에도 `.10`, TTL 이 30 → 26 → 8 로 줄다가 0 을 지난 뒤 `.20`(TTL 30 으로 다시 참). reload 로그는 이미 찍혀 있음.
- 원인: 캐시는 레코드 TTL 동안 옛 답을 준다(cache 기본 최대 3600s). 실무 대응: 장애조치 전에 TTL 을 미리 낮춰 두기(학습자가 `$TTL 5` 로 바꿔 재실험).
- 노트: `03-02` cache, `02-01` §7 캐싱.

## S3 — 새 레코드가 한동안 없음 (부정 캐시)

- 설정: S2 와 같음. coupon 레코드는 아직 없음.
- 재현: 배포 전 누군가 `coupon.shop.example` 조회 → NXDOMAIN → coupon 추가·시리얼 올림 → 다시 조회.
- 확인된 출력: 추가 뒤에도 NXDOMAIN, 권한 절 SOA 의 TTL 이 26 → 8 로 줄어듦. 0 지난 뒤 답이 나옴.
- 함정(노트와 다른 점, 학습자가 발견하게 둘 것): RFC 2308 은 부정 캐시 시간을 SOA `MINIMUM`(여기선 20)과 SOA 자신의 TTL 중 작은 값으로 정하지만, CoreDNS `file` 은 NXDOMAIN 에 SOA 를 레코드 TTL 그대로 실어 보내고(`$TTL 300`, `MINIMUM 20` 이면 SOA TTL 300 으로 나감) `cache` 는 메시지 안 레코드 TTL 의 최솟값만 쓴다(`plugin/pkg/dnsutil/ttl.go` `MinimalTTLWithMaximum`, MINIMUM 칸을 보지 않음). 그래서 이 조합에서 부정 캐시 시간은 `MINIMUM` 이 아니라 SOA 레코드의 TTL 을 따른다. 실습 뒤 `02-02` 부정 캐싱 TTL 절 보강 후보로 메인에 보고.
- 고치기(2026-11-03 실측): SOA 만 짧게 — 파일 맨 앞 `$TTL 30`, SOA 줄 뒤 `$TTL 300`(또는 `@ 30 IN SOA`). 없는 이름 SOA 30, NS 300 확인. Corefile 쪽은 `cache { denial 9984 30 }` 로 상한(첫 응답부터 30). 이미 캐시에 든 부정 답은 고쳐도 TTL 이 다할 때까지 남음.
- 노트: `02-02` 「부정 응답을 좌우하는 한 칸」, `03-02` cache `denial`.

## S4 — 사내 이름이 밖으로 샘 (서버 블록 라벨)

- 설정: 라벨 오타 `shop.exmaple { file db.shop.example shop.example  log }` + `. { forward . 1.1.1.1  log }`
- 확인된 출력: `db.shop.example` → NXDOMAIN, 플래그에 `aa` 없음·`ra` 있음, 권한 절 SOA 가 `. ... a.root-servers.net.` 이고 TTL 86400. 시작 로그에 블록 이름이 `shop.exmaple.:1053` 으로 찍힘. 질의 시간 수십~백여 ms(외부 왕복).
- 원인: 질의 이름과 가장 길게 맞는 라벨의 블록이 받는다. 오타 라벨은 아무 이름에도 안 맞아 `.` 블록이 받고 외부로 넘긴다. `file` 인자의 존 이름을 맞게 써도 블록이 안 받으면 소용없다(존=데이터, 서버 블록=어떤 질의를 받을지).
- 노트: `03-01` §3 최장 일치, 4장 Phase 2 의 존/서버 블록 혼동과 직결.

## S5 — 상위 DNS 하나가 죽음 (forward)

- 설정: `. { forward . 192.0.2.1 1.1.1.1  log }` (192.0.2.1 은 응답 없는 문서용 주소)
- 확인된 출력: 처음 몇 번은 질의마다 대략 절반이 2,0xx ms, 나머지는 10 ms 안팎. 몇 초 뒤부터는 전부 10 ms 안팎(죽은 쪽을 건너뜀). 상태는 모두 NOERROR(뒤의 살아 있는 쪽으로 재시도).
- 원인: 기본 policy 가 random 이라 죽은 쪽을 고르면 타임아웃 뒤 다음 상위로 넘어간다. 오류가 난 뒤 0.5초 간격 확인이 시작되고 연속 실패가 `max_fails`(2)를 넘으면 down 으로 표시돼 건너뛴다.
- 이어서 해 볼 것(2026-11-03 실측, 0.5초 간격 12회 질의 ms): `policy sequential` → 2009·2009·2010 뒤로 전부 7~8(처음 몇 번은 늘 죽은 쪽 먼저, down 표시 뒤 건너뜀). `max_fails 0` → 2012·2010·7·7·23·17·2010·8·8·9·2009·8(down 표시를 안 해 끝까지 섞여 느림). 기본 → 2009·2008·7·2008 뒤 7~9.
- 노트: `03-02` forward `max_fails`·`health_check`·`policy`.

## S6 — auto 로 바꿨는데 새 존 하나만 안 됨

- 설정: `. { auto { directory zones  reload 2s }  log }`, `zones/db.order.example`, `zones/db.pay.example`, 새 팀은 `zones/coupon.example.db`(다른 팀 관례대로 이름 붙임).
- 확인된 출력: order·pay 는 NOERROR + `aa`, coupon 은 **REFUSED**. 로그에 `Inserting zone ... from: zones/db.pay.example` 같은 줄이 coupon 에는 없음.
- 원인: 기본 패턴 `db\.(.*)` 에 안 맞는 파일은 존이 되지 않고, 어느 존에도 속하지 않는 질의라 REFUSED. 고치기: 파일 이름 바꾸기 또는 패턴 지정.
- 노트: `04-01` §3 auto, 보강 후보 25(앵커 없는 정규식).

## S7 — hosts 로 하나 덮었더니 나머지 전부 실패

- 설정: `shop.example { hosts { 198.51.100.99 api.shop.example }  file db.shop.example  log }`, 존 파일에 api·db 둘 다 있음.
- 확인된 출력: api → `.99`, db → **SERVFAIL**(NXDOMAIN 아님). `fallthrough` 추가 뒤 db 정상.
- 원인: hosts 는 서버 블록 존(shop.example) 전체에 권한을 받고, 못 찾으면 fallthrough 없이는 다음 플러그인(file)에 안 넘긴다. NXDOMAIN 을 주려면 SOA 가 필요한데 hosts 에는 SOA 가 없어 SERVFAIL 로 답한다(`plugin/hosts/hosts.go:72-74` 주석). 플러그인 순서는 plugin.cfg 에서 hosts(66) 가 file(72) 보다 앞.
- 노트: `03-02` fallthrough, `04-01` §5 hosts(SOA 없음).
