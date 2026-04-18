package main

import "fmt"

// ProviderFactory는 ProviderConfig를 생성하는 함수 타입
type ProviderFactory func(option map[string]string) ProviderConfig

// registry는 프로바이더 타입별 팩토리 함수를 저장
var registry = map[ProviderType]ProviderFactory{}

// Register는 새로운 프로바이더 팩토리를 등록합니다
func Register(t ProviderType, factory ProviderFactory) {
	if _, exists := registry[t]; exists {
		panic(fmt.Sprintf("provider %s already registered", t))
	}
	registry[t] = factory
}

// NewProvider는 타입에 맞는 프로바이더를 생성합니다
func NewProvider(t ProviderType, option map[string]string) ProviderConfig {
	if factory, exists := registry[t]; exists {
		return factory(option)
	}
	return nil
}

// ListProviders는 등록된 모든 프로바이더 타입을 반환합니다
func ListProviders() []ProviderType {
	types := make([]ProviderType, 0, len(registry))
	for t := range registry {
		types = append(types, t)
	}
	return types
}
