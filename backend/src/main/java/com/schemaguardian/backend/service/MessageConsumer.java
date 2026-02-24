package com.schemaguardian.backend.service;

import com.schemaguardian.backend.model.FinancialMessage;
import com.schemaguardian.backend.repository.FinancialMessageRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.Map;

@Slf4j
@Service
@RequiredArgsConstructor
public class MessageConsumer {

    private final FinancialMessageRepository repository;
    private final SidecarClient sidecarClient;
    private final KafkaTemplate<String, Object> kafkaTemplate;

    @Value("${kafka.topics.dlq}")
    private String dlqTopic;

    @KafkaListener(topics = "${kafka.topics.inbound}")
    public void consume(Map<String, Object> message) {
        log.info("Received message: {}", message.get("transaction_id"));

        // 1. Forward to LLM Sidecar for semantic validation
        SidecarClient.ValidationResponse response = sidecarClient.validate(message);
        log.info("Validation Result: {} ({}ms)", response.getLabel(), response.getLatencyMs());

        if ("SAFE".equals(response.getLabel())) {
            // 2. Persist to PostgreSQL if SAFE
            FinancialMessage entity = FinancialMessage.builder()
                    .transactionId((String) message.get("transaction_id"))
                    .amount(Double.valueOf(message.get("amount").toString()))
                    .currency((String) message.get("currency"))
                    .senderIban((String) message.get("sender_iban"))
                    .receiverIban((String) message.get("receiver_iban"))
                    .settlementDate((String) message.get("settlement_date"))
                    .status((String) message.get("status"))
                    .processedAt(LocalDateTime.now())
                    .build();
            
            repository.save(entity);
            log.info("Message {} persisted to DB.", entity.getTransactionId());
        } else {
            // 3. Route to DLQ if FLAGGED
            kafkaTemplate.send(dlqTopic, (String) message.get("transaction_id"), message);
            log.warn("Message {} FLAGGED and routed to DLQ topic: {}", message.get("transaction_id"), dlqTopic);
        }
    }
}
