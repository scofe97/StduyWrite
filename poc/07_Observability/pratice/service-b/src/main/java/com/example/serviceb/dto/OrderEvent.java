package com.example.serviceb.dto;

public class OrderEvent {
    private String orderId;
    private String productId;
    private int quantity;
    private String status;

    public OrderEvent() {}

    public OrderEvent(String orderId, String productId, int quantity, String status) {
        this.orderId = orderId;
        this.productId = productId;
        this.quantity = quantity;
        this.status = status;
    }

    public String getOrderId() { return orderId; }
    public void setOrderId(String orderId) { this.orderId = orderId; }
    public String getProductId() { return productId; }
    public void setProductId(String productId) { this.productId = productId; }
    public int getQuantity() { return quantity; }
    public void setQuantity(int quantity) { this.quantity = quantity; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }

    @Override
    public String toString() {
        return "OrderEvent{orderId='" + orderId + "', productId='" + productId +
               "', quantity=" + quantity + ", status='" + status + "'}";
    }
}
