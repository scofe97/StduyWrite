package com.example.servicea.dto;

public class PaymentEvent {
    private String orderId;
    private String paymentId;
    private String status;  // COMPLETED, FAILED
    private long processedAt;

    public PaymentEvent() {}

    public PaymentEvent(String orderId, String paymentId, String status, long processedAt) {
        this.orderId = orderId;
        this.paymentId = paymentId;
        this.status = status;
        this.processedAt = processedAt;
    }

    public String getOrderId() { return orderId; }
    public void setOrderId(String orderId) { this.orderId = orderId; }
    public String getPaymentId() { return paymentId; }
    public void setPaymentId(String paymentId) { this.paymentId = paymentId; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    public long getProcessedAt() { return processedAt; }
    public void setProcessedAt(long processedAt) { this.processedAt = processedAt; }

    @Override
    public String toString() {
        return "PaymentEvent{orderId='" + orderId + "', paymentId='" + paymentId +
               "', status='" + status + "', processedAt=" + processedAt + "}";
    }
}
