package com.runnershigh.querydsl.support;

import com.runnershigh.querydsl.domain.Address;
import com.runnershigh.querydsl.domain.Category;
import com.runnershigh.querydsl.domain.Item;
import com.runnershigh.querydsl.domain.Member;
import com.runnershigh.querydsl.domain.Order;
import com.runnershigh.querydsl.domain.OrderItem;
import com.runnershigh.querydsl.domain.OrderStatus;
import jakarta.persistence.EntityManager;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

/**
 * 결정론적 대량 시드 — 10,000명 회원, 100상품, 4 카테고리, 10,000 주문.
 * 모든 값이 인덱스에서 파생되므로 시드를 다시 적재해도 동일한 분포가 보장된다.
 */
public class TestDataLoader {

    public static final int DEFAULT_MEMBER_COUNT = 1_000;
    public static final int ITEM_COUNT = 100;
    public static final int CATEGORY_COUNT = 4;

    private static final String[] CITIES = {"Seoul", "Busan", "Incheon", "Daegu"};
    private static final String[] CATEGORY_NAMES = {"도서", "식품", "가전", "의류"};
    private static final LocalDateTime BASE_DATE = LocalDateTime.of(2026, 1, 1, 0, 0);

    private final EntityManager em;

    public TestDataLoader(EntityManager em) {
        this.em = em;
    }

    public Fixture loadBulk() {
        return loadBulk(DEFAULT_MEMBER_COUNT);
    }

    /**
     * memberCount 만큼 회원과 1:1 주문을 만든다. 카테고리/상품 수는 고정.
     * 회원 i (1-based): username=user_00001 형식, city=CITIES[(i-1)%4], age=20+((i-1)%40)
     * 상품 j (1-based): name=item_001 형식, price=1000*j, stock=100_000, category=cats[(j-1)%4]
     * 주문 i: 회원 i → 상품 ((i-1)%100)+1, count=1+((i-1)%5). i % 10 == 0 이면 CANCELED.
     */
    public Fixture loadBulk(int memberCount) {
        List<Category> categories = new ArrayList<>(CATEGORY_COUNT);
        for (int c = 0; c < CATEGORY_COUNT; c++) {
            Category cat = Category.builder().name(CATEGORY_NAMES[c]).build();
            em.persist(cat);
            categories.add(cat);
        }

        List<Item> items = new ArrayList<>(ITEM_COUNT);
        for (int j = 1; j <= ITEM_COUNT; j++) {
            Item it = Item.builder()
                    .name(String.format("item_%03d", j))
                    .price(1_000 * j)
                    .stockQuantity(100_000)
                    .category(categories.get((j - 1) % CATEGORY_COUNT))
                    .build();
            em.persist(it);
            items.add(it);
        }
        em.flush();

        int orderedCount = 0;
        int canceledCount = 0;
        Member firstMember = null;
        Member lastMember = null;
        for (int i = 1; i <= memberCount; i++) {
            String city = CITIES[(i - 1) % CITIES.length];
            int age = 20 + ((i - 1) % 40);
            Member m = Member.builder()
                    .username(String.format("user_%05d", i))
                    .email(String.format("user_%05d@runners.io", i))
                    .age(age)
                    .address(new Address(city, "street_" + i, String.format("%05d", 10_000 + i)))
                    .build();
            em.persist(m);
            if (i == 1) firstMember = m;
            if (i == memberCount) lastMember = m;

            Item target = items.get((i - 1) % ITEM_COUNT);
            int count = 1 + ((i - 1) % 5);
            Order ord = Order.create(m, BASE_DATE.plusMinutes(i),
                    OrderItem.create(target, target.getPrice(), count));
            if (i % 10 == 0) {
                ord.cancel();
                canceledCount++;
            } else {
                orderedCount++;
            }
            em.persist(ord);

            if (i % 500 == 0) {
                em.flush();
                em.clear();
                // 재참조용으로 첫/마지막 회원만 다시 끌어옴 (clear 후 detached 됨)
                if (firstMember != null) firstMember = em.find(Member.class, firstMember.getId());
                lastMember = em.find(Member.class, m.getId());
                // items/categories 도 detached → 다음 루프에서 다시 참조하려면 재조회
                for (int k = 0; k < items.size(); k++) {
                    items.set(k, em.find(Item.class, items.get(k).getId()));
                }
                for (int k = 0; k < categories.size(); k++) {
                    categories.set(k, em.find(Category.class, categories.get(k).getId()));
                }
            }
        }
        em.flush();
        em.clear();

        return new Fixture(memberCount, orderedCount, canceledCount,
                firstMember == null ? null : firstMember.getId(),
                lastMember == null ? null : lastMember.getId(),
                items.get(0).getId(),
                items.get(ITEM_COUNT - 1).getId(),
                categories.get(0).getId());
    }

    /**
     * 시드 식별자 + 분포 메타데이터.
     */
    public record Fixture(
            int memberCount,
            int orderedCount,
            int canceledCount,
            Long firstMemberId,
            Long lastMemberId,
            Long firstItemId,
            Long lastItemId,
            Long firstCategoryId
    ) {
        public String firstUsername() { return String.format("user_%05d", 1); }
        public String lastUsername()  { return String.format("user_%05d", memberCount); }
        public OrderStatus statusFor(int memberIndex1Based) {
            return memberIndex1Based % 10 == 0 ? OrderStatus.CANCELED : OrderStatus.ORDERED;
        }
    }
}
