# Bookinfo Sample App

Istio의 공식 샘플 애플리케이션입니다.

## 설치

```bash
# Istio 설치 디렉토리에서
kubectl apply -f samples/bookinfo/platform/kube/bookinfo.yaml -n bookinfo
kubectl apply -f samples/bookinfo/networking/bookinfo-gateway.yaml -n bookinfo
```

## 구성 요소
- productpage (Python): 메인 페이지
- details (Ruby): 책 상세 정보
- reviews (Java): 리뷰 (v1: 별점 없음, v2: 검은 별, v3: 빨간 별)
- ratings (Node.js): 별점 데이터

## 접속
```bash
kubectl port-forward svc/productpage -n bookinfo 9080:9080
# http://localhost:9080/productpage
```
