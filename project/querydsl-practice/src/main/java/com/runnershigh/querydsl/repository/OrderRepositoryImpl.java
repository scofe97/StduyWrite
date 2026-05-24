package com.runnershigh.querydsl.repository;

import static com.runnershigh.querydsl.domain.QMember.member;
import static com.runnershigh.querydsl.domain.QOrder.order;
import static com.runnershigh.querydsl.domain.QOrderItem.orderItem;

import com.querydsl.core.types.OrderSpecifier;
import com.querydsl.core.types.Projections;
import com.querydsl.core.types.dsl.BooleanExpression;
import com.querydsl.core.types.dsl.Expressions;
import com.querydsl.jpa.JPAExpressions;
import com.querydsl.jpa.impl.JPAQuery;
import com.querydsl.jpa.impl.JPAQueryFactory;
import com.runnershigh.querydsl.domain.Order;
import com.runnershigh.querydsl.domain.OrderStatus;
import com.runnershigh.querydsl.dto.OrderSummaryDto;
import java.time.LocalDateTime;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.support.PageableExecutionUtils;

/**
 * 학습 노트:
 * - 01-03.기본 문법과 조인
 * - 01-04.동적 쿼리 (BooleanExpression 분해)
 * - 01-05.프로젝션과 DTO 매핑 (Projections.constructor)
 * - 01-06.페이징과 fetch join 함정 (PageableExecutionUtils, count 분리)
 */
@RequiredArgsConstructor
public class OrderRepositoryImpl implements OrderRepositoryCustom {

    private final JPAQueryFactory queryFactory;

    @Override
    public List<Order> search(OrderSearchCondition condition) {
        return baseQuery(condition)
                .orderBy(orderBySortKey(condition.getSortKey(), condition.isAscending()))
                .fetch();
    }

    @Override
    public Page<Order> searchPage(OrderSearchCondition condition, Pageable pageable) {
        // 컨텐츠 — fetch join 없는 단순 페이징.
        // 페치 조인 + Pageable 동시 사용은 HHH000104 — 메모리 페이징을 일으킨다.
        // 권장 패턴: 컨텐츠는 페이지 단위로 ID 만 끊고, 별도 쿼리로 fetch join 으로 채운다.
        // 본 메서드는 가장 단순한 안전 형태(@BatchSize 또는 EntityGraph 와 결합 가정).
        List<Order> content = baseQuery(condition)
                .offset(pageable.getOffset())
                .limit(pageable.getPageSize())
                .fetch();

        // count 쿼리 분리 — 컨텐츠가 0 또는 마지막 페이지 미만일 때 PageableExecutionUtils 가 count 호출 자체를 생략한다.
        JPAQuery<Long> countQuery = queryFactory
                .select(order.count())
                .from(order)
                .leftJoin(order.member, member)
                .where(
                        memberNameEq(condition.getMemberName()),
                        statusEq(condition.getStatus()),
                        orderDateGoe(condition.getOrderDateFrom()),
                        orderDateLoe(condition.getOrderDateTo())
                );

        return PageableExecutionUtils.getPage(content, pageable, countQuery::fetchOne);
    }

    @Override
    public List<OrderSummaryDto> findSummaries(OrderSearchCondition condition) {
        return queryFactory
                .select(Projections.constructor(OrderSummaryDto.class,
                        order.id,
                        member.username,
                        order.orderDate,
                        order.status,
                        // OrderItem 합계는 상관 서브쿼리 — 02-04 변형 모음 참고.
                        // multiply(...).sum() 체인은 QueryDSL 6.12 에서 타입 추론이 흔들려 numberTemplate 로 우회.
                        JPAExpressions
                                .select(Expressions.numberTemplate(Integer.class,
                                        "coalesce(sum({0} * {1}), 0)",
                                        orderItem.orderPrice, orderItem.count))
                                .from(orderItem)
                                .where(orderItem.order.eq(order))
                ))
                .from(order)
                .leftJoin(order.member, member)
                .where(
                        memberNameEq(condition.getMemberName()),
                        statusEq(condition.getStatus()),
                        orderDateGoe(condition.getOrderDateFrom()),
                        orderDateLoe(condition.getOrderDateTo())
                )
                .fetch();
    }

    private JPAQuery<Order> baseQuery(OrderSearchCondition condition) {
        return queryFactory
                .selectFrom(order)
                .leftJoin(order.member, member)
                .where(
                        memberNameEq(condition.getMemberName()),
                        statusEq(condition.getStatus()),
                        orderDateGoe(condition.getOrderDateFrom()),
                        orderDateLoe(condition.getOrderDateTo())
                );
    }

    private BooleanExpression memberNameEq(String name) {
        return name == null || name.isBlank() ? null : member.username.eq(name);
    }

    private BooleanExpression statusEq(OrderStatus status) {
        return status == null ? null : order.status.eq(status);
    }

    private BooleanExpression orderDateGoe(LocalDateTime from) {
        return from == null ? null : order.orderDate.goe(from);
    }

    private BooleanExpression orderDateLoe(LocalDateTime to) {
        return to == null ? null : order.orderDate.loe(to);
    }

    private OrderSpecifier<?> orderBySortKey(String sortKey, boolean asc) {
        // com.querydsl.core.types.Order 는 정렬 방향 enum (ASC/DESC).
        // 도메인 Order 엔티티와 이름이 충돌해 FQN 으로 구분한다.
        com.querydsl.core.types.Order direction =
                asc ? com.querydsl.core.types.Order.ASC : com.querydsl.core.types.Order.DESC;

        // 화이트리스트 — 허용된 키만 컬럼에 매핑 (잘못된 키·인젝션 방어).
        return switch (sortKey == null ? "" : sortKey) {
            case "orderDate"  -> new OrderSpecifier<>(direction, order.orderDate);
            case "memberName" -> new OrderSpecifier<>(direction, member.username);
            default           -> new OrderSpecifier<>(direction, order.id);
        };
    }
}
