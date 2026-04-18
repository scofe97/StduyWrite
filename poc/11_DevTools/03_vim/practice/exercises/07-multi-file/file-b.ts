// file-b.ts - 주문 서비스 (Ch08: 다중 파일 연습)
// 이 파일은 주문 관련 타입과 함수를 정의합니다.
// file-a.ts의 User 타입을 import하여 사용합니다.

import { User } from "./file-a";

export interface Order {
  id: number;
  userId: number;
  items: OrderItem[];
  total: number;
  status: OrderStatus;
  createdAt: Date;
}

export interface OrderItem {
  name: string;
  price: number;
  quantity: number;
}

export enum OrderStatus {
  PENDING = "PENDING",
  PROCESSING = "PROCESSING",
  SHIPPED = "SHIPPED",
  DELIVERED = "DELIVERED",
  CANCELLED = "CANCELLED",
}

export function createOrder(user: User, items: OrderItem[]): Order {
  const total = calculateTotal(items);
  return {
    id: Date.now(),
    userId: user.id,
    items,
    total,
    status: OrderStatus.PENDING,
    createdAt: new Date(),
  };
}

export function calculateTotal(items: OrderItem[]): number {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

export function formatOrderSummary(order: Order): string {
  const itemCount = order.items.reduce((sum, item) => sum + item.quantity, 0);
  return `Order #${order.id}: ${itemCount} items, Total: $${order.total.toFixed(2)}`;
}

export function canCancelOrder(order: Order): boolean {
  return order.status === OrderStatus.PENDING || order.status === OrderStatus.PROCESSING;
}

export function updateOrderStatus(order: Order, newStatus: OrderStatus): Order {
  return {
    ...order,
    status: newStatus,
  };
}

// LSP 기능 연습 미션 (NeoVim + LSP 설정 필요):
// 1. 'User' 타입 위에 커서를 두고 gd (go to definition) → file-a.ts로 이동
// 2. gr (go to references) → User가 사용된 모든 위치 확인
// 3. K (hover) → User 타입 정보 보기
// 4. 'createOrder' 함수명에서 <leader>rn (rename) → 이름 변경
// 5. 'OrderStatus' 위에서 gI (go to implementation) → enum 정의로 이동

// 버퍼 관리 연습:
// 1. :e file-c.ts 로 세 번째 파일 열기
// 2. :ls 로 버퍼 목록 확인 (a, b, c 모두 표시됨)
// 3. :b 1 로 첫 번째 버퍼(file-a.ts)로 이동
// 4. :bd 로 현재 버퍼 닫기
// 5. Ctrl+^ 로 이전 버퍼와 현재 버퍼 토글
