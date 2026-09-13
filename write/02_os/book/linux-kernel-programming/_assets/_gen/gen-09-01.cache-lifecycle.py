# 09-01 §1~§3 — custom slab cache 의 3단계가 실제로 어떤 호출 순서로 일어나는가.
# 본문이 요구한 형태: "생성(init/probe) → 사용(alloc/free) → 파괴(exit/remove)" + "생성자는 새 페이지를 할당할 때마다 호출된다".
# 타입 스펙: type-sequence — 주체 셋 사이의 시간순 메시지. ctor 가 alloc 당 한 번이 아니라는 것이 논점이다.
import sys; sys.path.insert(0, ".")
from ddk import SeqK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER2, RULE, KR, MONO

W, H = 976, 752

d = SeqK(W, H, "LINUX KERNEL PROGRAMMING · 09-01 §1~§3",
         "생성자는 alloc 당 한 번이 아닙니다",
         "custom slab cache 의 3단계 수명주기. 모듈 init 에서 캐시를 만들고, 쓰는 동안 객체를 빌렸다 반납하고, exit 에서 캐시를 부순다. 생성자(ctor)는 kmem_cache_alloc() 호출당 한 번이 아니라 캐시가 새 페이지를 받을 때마다 호출되므로, alloc 한 번에 여러 번 도는 일이 흔하다.",
         "세 단계 모두 프로세스 컨텍스트에서만 부를 수 있습니다")

d.lanes([("내 모듈", "module"), ("slab 계층", "kmem_cache"), ("페이지 할당자", "buddy system")], 104, 224)

d.msg("내 모듈", "slab 계층", "kmem_cache_create()", 196, INFO, sub="name · size · align · flags · ctor")
d.msg("slab 계층", "페이지 할당자", "새 페이지 요청", 260, MUTED)
d.selfmsg("slab 계층", "ctor × N", 324, ACC, sub="페이지를 받을 때마다 객체마다 돕니다")
d.msg("slab 계층", "내 모듈", "struct kmem_cache *", 388, OK, "ok", sub="전역에 보관합니다")
d.msg("내 모듈", "slab 계층", "kmem_cache_alloc()", 452, INFO, sub="둘째 인자는 GFP 플래그입니다")
d.msg("slab 계층", "내 모듈", "객체 하나의 KVA", 516, OK, "ok")
d.msg("내 모듈", "slab 계층", "kmem_cache_free()", 572, MUTED, dash="4 4", sub="캐시로 반납할 뿐 페이지는 안 풀립니다")
d.msg("내 모듈", "slab 계층", "kmem_cache_destroy()", 636, WARN, "warn", sub="모듈 exit · 드라이버 remove 에서")

d.rails(664)

d.legend(H - 56, [("모듈이 부르는 쪽", INFO), ("돌려받는 값", OK), ("생성자 — 이 절의 논점", ACC), ("마지막 단계", WARN)])
d.save("09-01.cache-lifecycle.svg")
print("ok 09-01.cache-lifecycle")
