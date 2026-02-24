package com.schemaguardian.backend.model;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import java.util.Map;

@Data
@Entity
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "processed_messages")
public class FinancialMessage {
    @Id
    private String transactionId;
    private Double amount;
    private String currency;
    private String senderIban;
    private String receiverIban;
    private String settlementDate;
    private String status;
    private LocalDateTime processedAt;
}
