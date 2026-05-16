package com.runnershigh.querydsl.support;

import com.runnershigh.querydsl.domain.Address;
import com.runnershigh.querydsl.domain.Category;
import com.runnershigh.querydsl.domain.Item;
import com.runnershigh.querydsl.domain.Member;
import com.runnershigh.querydsl.domain.Order;
import com.runnershigh.querydsl.domain.OrderItem;
import jakarta.persistence.EntityManager;
import java.time.LocalDateTime;

/**
 * 테스트용 더미 데이터 빌더.
 * 각 테스트 클래스에서 호출해 시나리오에 맞는 그래프를 만든다.
 */
public class TestDataLoader {

    private final EntityManager em;

    public TestDataLoader(EntityManager em) {
        this.em = em;
    }

    /**
     * 회원 4명 + 카테고리 2개 + 상품 4개 + 주문 3건의 기본 그래프.
     * - alice(서울, 25), bob(서울, 31), charlie(부산, 28), dave(부산, 40)
     * - 카테고리: 도서 / 식품
     * - 상품: 자바책(2만), 코틀린책(2.5만), 사과(1천), 우유(2.5천)
     * - 주문: alice—자바책×1, bob—사과×10+우유×2, charlie—코틀린책×1+자바책×2(취소)
     */
    public Fixture loadDefault() {
        Member alice = Member.builder()
                .username("alice").email("alice@runners.io").age(25)
                .address(new Address("Seoul", "Gangnam", "06000"))
                .build();
        Member bob = Member.builder()
                .username("bob").email("bob@runners.io").age(31)
                .address(new Address("Seoul", "Mapo", "04000"))
                .build();
        Member charlie = Member.builder()
                .username("charlie").email("charlie@runners.io").age(28)
                .address(new Address("Busan", "Haeundae", "48000"))
                .build();
        Member dave = Member.builder()
                .username("dave").email("dave@runners.io").age(40)
                .address(new Address("Busan", "Suyeong", "48200"))
                .build();
        em.persist(alice);
        em.persist(bob);
        em.persist(charlie);
        em.persist(dave);

        Category book = Category.builder().name("도서").build();
        Category food = Category.builder().name("식품").build();
        em.persist(book);
        em.persist(food);

        Item javaBook = Item.builder().name("자바 인 액션").price(20_000).stockQuantity(100).category(book).build();
        Item kotlinBook = Item.builder().name("코틀린 핸드북").price(25_000).stockQuantity(50).category(book).build();
        Item apple = Item.builder().name("사과").price(1_000).stockQuantity(500).category(food).build();
        Item milk = Item.builder().name("우유").price(2_500).stockQuantity(200).category(food).build();
        em.persist(javaBook);
        em.persist(kotlinBook);
        em.persist(apple);
        em.persist(milk);

        Order aliceOrder = Order.create(alice, LocalDateTime.of(2026, 5, 1, 10, 0),
                OrderItem.create(javaBook, 20_000, 1));
        Order bobOrder = Order.create(bob, LocalDateTime.of(2026, 5, 2, 11, 30),
                OrderItem.create(apple, 1_000, 10),
                OrderItem.create(milk, 2_500, 2));
        Order charlieOrder = Order.create(charlie, LocalDateTime.of(2026, 5, 3, 9, 0),
                OrderItem.create(kotlinBook, 25_000, 1),
                OrderItem.create(javaBook, 20_000, 2));
        charlieOrder.cancel();
        em.persist(aliceOrder);
        em.persist(bobOrder);
        em.persist(charlieOrder);

        em.flush();
        em.clear();

        return new Fixture(alice, bob, charlie, dave, book, food, javaBook, kotlinBook, apple, milk,
                aliceOrder, bobOrder, charlieOrder);
    }

    public record Fixture(
            Member alice, Member bob, Member charlie, Member dave,
            Category book, Category food,
            Item javaBook, Item kotlinBook, Item apple, Item milk,
            Order aliceOrder, Order bobOrder, Order charlieOrder
    ) {}
}
