// file-c.ts - 메인 앱 (Ch08: 다중 파일 연습)
// 이 파일은 file-a.ts와 file-b.ts의 함수들을 조합하여 사용합니다.

import { createUser, formatUser, validateEmail, User } from "./file-a";
import {
  createOrder,
  formatOrderSummary,
  canCancelOrder,
  updateOrderStatus,
  OrderItem,
  OrderStatus,
} from "./file-b";

// 샘플 사용자 생성
const user: User = createUser("Alice", "alice@example.com");
console.log("User created:", formatUser(user));

// 이메일 검증
if (validateEmail(user.email)) {
  console.log("Email is valid");
} else {
  console.error("Invalid email");
}

// 샘플 주문 아이템
const items: OrderItem[] = [
  { name: "Laptop", price: 1200, quantity: 1 },
  { name: "Mouse", price: 25, quantity: 2 },
  { name: "Keyboard", price: 75, quantity: 1 },
];

// 주문 생성
const order = createOrder(user, items);
console.log(formatOrderSummary(order));

// 주문 상태 변경
if (canCancelOrder(order)) {
  const cancelledOrder = updateOrderStatus(order, OrderStatus.CANCELLED);
  console.log("Order cancelled:", formatOrderSummary(cancelledOrder));
} else {
  console.log("Cannot cancel this order");
}

// 주문 처리 시뮬레이션
function processOrder(orderId: number): void {
  console.log(`Processing order ${orderId}...`);
  // 실제 처리 로직
}

// 주문 배송 시작
function shipOrder(orderId: number): void {
  console.log(`Shipping order ${orderId}...`);
  // 실제 배송 로직
}

processOrder(order.id);
const shippedOrder = updateOrderStatus(order, OrderStatus.SHIPPED);
shipOrder(shippedOrder.id);

console.log("Final order status:", shippedOrder.status);

// ============================================================================
// 다중 파일 편집 종합 연습 미션
// ============================================================================

// [미션 1] 윈도우 분할 마스터하기
// 1. :vsp file-a.ts - 수직 분할로 file-a.ts 열기
// 2. Ctrl+W v - 현재 윈도우를 수직 분할
// 3. Ctrl+W s - 수평 분할
// 4. Ctrl+W hjkl - 윈도우 간 이동
// 5. Ctrl+W = - 모든 윈도우 크기 균등하게
// 6. Ctrl+W _ - 현재 윈도우 높이 최대화
// 7. Ctrl+W | - 현재 윈도우 너비 최대화
// 8. Ctrl+W q - 현재 윈도우 닫기

// [미션 2] 버퍼 관리 마스터하기
// 1. :e file-a.ts - 파일 열기 (버퍼에 추가)
// 2. :e file-b.ts - 또 다른 파일 열기
// 3. :ls - 버퍼 목록 확인
//    출력: 1 file-a.ts, 2 file-b.ts, 3 file-c.ts
// 4. :b 1 - 1번 버퍼로 이동
// 5. :bn - 다음 버퍼
// 6. :bp - 이전 버퍼
// 7. :b file-a - 이름으로 버퍼 이동 (탭 자동완성 가능)
// 8. :bd - 현재 버퍼 닫기
// 9. Ctrl+^ - 이전 버퍼와 토글

// [미션 3] LSP 기능 활용 (NeoVim + LSP 필요)
// 1. 'User' 타입 위에서 gd - file-a.ts의 정의로 이동
// 2. 정의에서 gr - 모든 참조 위치 확인 (Telescope)
// 3. K - Hover 문서 보기
// 4. 'createUser' 위에서 <leader>rn - 함수명 변경 (모든 파일에 적용)
// 5. [d, ]d - 다음/이전 진단(에러/경고)으로 이동
// 6. <leader>ca - Code Action 메뉴 열기

// [미션 4] Telescope로 파일 찾기 (플러그인 필요)
// 1. <leader>ff - 파일 찾기 (find files)
// 2. <leader>fg - 텍스트 검색 (live grep)
// 3. <leader>fb - 버퍼 목록 (buffers)
// 4. <leader>fr - 최근 파일 (recent files)
// 5. <leader>fs - 심볼 검색 (symbols)

// [미션 5] 여러 파일에 걸친 리팩토링
// 시나리오: 'User' 타입의 'email' 필드를 'emailAddress'로 변경
// 1. file-a.ts에서 'email' 필드 정의 찾기
// 2. <leader>rn으로 'emailAddress'로 변경
// 3. LSP가 자동으로 모든 파일(a, b, c)에서 참조 변경
// 4. :wa로 모든 버퍼 저장

// [미션 6] 검색과 치환 조합
// 시나리오: 모든 파일에서 'console.log'를 'logger.info'로 변경
// 1. :args *.ts - 모든 TypeScript 파일을 args에 추가
// 2. :argdo %s/console\.log/logger.info/ge | update
//    - argdo: 모든 args에 대해 실행
//    - %s: 파일 전체 치환
//    - e: 에러 무시
//    - update: 변경사항 저장

// [미션 7] 복잡한 윈도우 레이아웃
// 최종 레이아웃 목표:
// +-------------------+-------------------+
// |                   |                   |
// |    file-a.ts      |    file-b.ts      |
// |    (User 정의)     |    (Order 정의)    |
// |                   |                   |
// +-------------------+-------------------+
// |              file-c.ts                |
// |         (메인 앱 - 통합)               |
// +---------------------------------------+
//
// 과정:
// 1. :e file-a.ts
// 2. :vsp file-b.ts (수직 분할)
// 3. Ctrl+W j 또는 Ctrl+W s (하단에 수평 분할)
// 4. :e file-c.ts
// 5. Ctrl+W = (크기 조정)

// [미션 8] QuickFix 활용 (컴파일 에러 탐색)
// 1. :make 또는 :!tsc (TypeScript 컴파일)
// 2. :copen - QuickFix 윈도우 열기 (에러 목록)
// 3. :cn - 다음 에러로 이동
// 4. :cp - 이전 에러로 이동
// 5. :cc - 현재 에러로 이동
// 6. :cclose - QuickFix 윈도우 닫기

// [미션 9] 세션 저장/복원
// 복잡한 윈도우 레이아웃을 세션으로 저장:
// 1. 원하는 레이아웃 구성 (위 미션 7 참조)
// 2. :mksession vim-practice-session.vim
// 3. Vim 종료 후 재시작
// 4. :source vim-practice-session.vim 또는
//    nvim -S vim-practice-session.vim

// [미션 10] 터미널 통합 (NeoVim)
// 1. :terminal - 터미널 열기 (같은 Vim 내)
// 2. Ctrl+W N - 터미널 Normal 모드로 전환
// 3. i 또는 a - 다시 터미널 모드로
// 4. :sp | terminal - 수평 분할로 터미널
// 5. :vsp | terminal - 수직 분할로 터미널

// ============================================================================
// 축하합니다! 모든 다중 파일 연습을 완료했습니다!
// ============================================================================
//
// 다음 단계:
// 1. 실제 프로젝트에 이 기법들을 적용해보세요
// 2. NeoVim + LSP 설정을 완료하여 gd, gr, K 등을 활용하세요
// 3. Telescope, Neo-tree 플러그인으로 더 빠른 네비게이션을 경험하세요
// 4. IdeaVim으로 IntelliJ에서도 같은 워크플로우를 사용하세요
//
// 추가 학습 자료:
// - :help buffers
// - :help windows
// - :help tabs
// - :help quickfix
// - :help sessions
