package mocktest

import (
	"errors"
	"time"
)

// 과제 2: Mock 테스트
// UserService의 CreateOrder 메서드를 Mock을 사용해 테스트하세요.

// 에러 정의
var (
	ErrUserNotFound      = errors.New("user not found")
	ErrProductNotFound   = errors.New("product not found")
	ErrInsufficientStock = errors.New("insufficient stock")
)

// 도메인 모델
type User struct {
	ID    string
	Name  string
	Email string
}

type Product struct {
	ID    string
	Name  string
	Price float64
	Stock int
}

type Order struct {
	ID        string
	UserID    string
	ProductID string
	Quantity  int
	Total     float64
	CreatedAt time.Time
}

// Repository 인터페이스
type UserRepository interface {
	FindByID(id string) (*User, error)
}

type ProductRepository interface {
	FindByID(id string) (*Product, error)
	UpdateStock(id string, quantity int) error
}

// OrderService 주문 비즈니스 로직
type OrderService struct {
	userRepo    UserRepository
	productRepo ProductRepository
}

// NewOrderService 새 OrderService 생성
func NewOrderService(userRepo UserRepository, productRepo ProductRepository) *OrderService {
	return &OrderService{
		userRepo:    userRepo,
		productRepo: productRepo,
	}
}

// TODO: CreateOrder 구현
// 1. 사용자 존재 확인 (없으면 ErrUserNotFound)
// 2. 상품 존재 확인 (없으면 ErrProductNotFound)
// 3. 재고 확인 (부족하면 ErrInsufficientStock)
// 4. 재고 차감
// 5. 주문 생성 및 반환
func (s *OrderService) CreateOrder(userID, productID string, quantity int) (*Order, error) {
	// TODO: 구현
	return nil, errors.New("not implemented")
}
