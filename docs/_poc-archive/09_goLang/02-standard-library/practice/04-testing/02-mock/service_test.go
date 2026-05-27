package mocktest

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
	"github.com/stretchr/testify/require"
)

// 과제 2: Mock 테스트
// testify/mock을 사용하여 OrderService 테스트

// TODO: MockUserRepository 구현
type MockUserRepository struct {
	mock.Mock
}

func (m *MockUserRepository) FindByID(id string) (*User, error) {
	// TODO: 구현
	// args := m.Called(id)
	// if args.Get(0) == nil {
	//     return nil, args.Error(1)
	// }
	// return args.Get(0).(*User), args.Error(1)
	return nil, nil
}

// TODO: MockProductRepository 구현
type MockProductRepository struct {
	mock.Mock
}

func (m *MockProductRepository) FindByID(id string) (*Product, error) {
	// TODO: 구현
	return nil, nil
}

func (m *MockProductRepository) UpdateStock(id string, quantity int) error {
	// TODO: 구현
	return nil
}

// 테스트 케이스

func TestOrderService_CreateOrder_Success(t *testing.T) {
	// TODO: 정상 주문 생성 테스트
	// 1. Mock 생성
	// mockUserRepo := new(MockUserRepository)
	// mockProductRepo := new(MockProductRepository)

	// 2. 기대 동작 설정
	// mockUserRepo.On("FindByID", "user-1").Return(&User{ID: "user-1", Name: "John"}, nil)
	// mockProductRepo.On("FindByID", "prod-1").Return(&Product{ID: "prod-1", Price: 100, Stock: 10}, nil)
	// mockProductRepo.On("UpdateStock", "prod-1", 8).Return(nil)

	// 3. 서비스 생성 및 테스트
	// service := NewOrderService(mockUserRepo, mockProductRepo)
	// order, err := service.CreateOrder("user-1", "prod-1", 2)

	// 4. 검증
	// require.NoError(t, err)
	// assert.Equal(t, "user-1", order.UserID)
	// assert.Equal(t, 200.0, order.Total)

	// 5. Mock 호출 검증
	// mockUserRepo.AssertExpectations(t)
	// mockProductRepo.AssertExpectations(t)

	t.Skip("TODO: 구현 필요")
}

func TestOrderService_CreateOrder_UserNotFound(t *testing.T) {
	// TODO: 사용자 없음 에러 테스트
	// mockUserRepo.On("FindByID", "unknown").Return(nil, ErrUserNotFound)
	// ProductRepository는 호출되면 안 됨

	t.Skip("TODO: 구현 필요")
}

func TestOrderService_CreateOrder_ProductNotFound(t *testing.T) {
	// TODO: 상품 없음 에러 테스트

	t.Skip("TODO: 구현 필요")
}

func TestOrderService_CreateOrder_InsufficientStock(t *testing.T) {
	// TODO: 재고 부족 에러 테스트
	// Stock이 5인데 quantity가 10인 경우

	t.Skip("TODO: 구현 필요")
}

// 힌트:
// - mock.On("Method", args...).Return(values...)
// - mock.AssertExpectations(t)
// - mock.AssertCalled(t, "Method", args...)
// - mock.AssertNotCalled(t, "Method")

// 실행: go test -v ./practices/02-mock/

// 추가 참고를 위한 import 확인용
var _ = assert.Equal
var _ = require.NoError
