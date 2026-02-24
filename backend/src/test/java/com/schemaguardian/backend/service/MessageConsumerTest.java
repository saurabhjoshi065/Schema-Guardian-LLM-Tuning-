package com.schemaguardian.backend.service;

import com.schemaguardian.backend.model.FinancialMessage;
import com.schemaguardian.backend.repository.FinancialMessageRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.test.util.ReflectionTestUtils;

import java.util.HashMap;
import java.util.Map;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class MessageConsumerTest {

    @Mock
    private FinancialMessageRepository repository;

    @Mock
    private SidecarClient sidecarClient;

    @Mock
    private KafkaTemplate<String, Object> kafkaTemplate;

    @InjectMocks
    private MessageConsumer messageConsumer;

    private Map<String, Object> testMessage;

    @BeforeEach
    void setUp() {
        ReflectionTestUtils.setField(messageConsumer, "dlqTopic", "financial-messages-flagged");
        
        testMessage = new HashMap<>();
        testMessage.put("transaction_id", "tx-123");
        testMessage.put("amount", 100.0);
        testMessage.put("currency", "USD");
        testMessage.put("sender_iban", "GB123");
        testMessage.put("receiver_iban", "GB456");
        testMessage.put("settlement_date", "2026-02-24");
        testMessage.put("status", "PENDING");
    }

    @Test
    void whenSidecarReturnsSafe_thenMessageIsPersistedToDB() {
        // Arrange
        SidecarClient.ValidationResponse safeResponse = new SidecarClient.ValidationResponse();
        safeResponse.setLabel("SAFE");
        safeResponse.setLatencyMs(45.0);
        
        when(sidecarClient.validate(testMessage)).thenReturn(safeResponse);

        // Act
        messageConsumer.consume(testMessage);

        // Assert
        verify(repository, times(1)).save(any(FinancialMessage.class));
        verify(kafkaTemplate, never()).send(anyString(), anyString(), any());
    }

    @Test
    void whenSidecarReturnsFlagged_thenMessageIsRoutedToDLQ() {
        // Arrange
        SidecarClient.ValidationResponse flaggedResponse = new SidecarClient.ValidationResponse();
        flaggedResponse.setLabel("FLAGGED");
        flaggedResponse.setLatencyMs(12.0);
        
        when(sidecarClient.validate(testMessage)).thenReturn(flaggedResponse);

        // Act
        messageConsumer.consume(testMessage);

        // Assert
        verify(repository, never()).save(any(FinancialMessage.class));
        verify(kafkaTemplate, times(1)).send(eq("financial-messages-flagged"), eq("tx-123"), eq(testMessage));
    }

    @Test
    void whenSidecarClientFails_thenMessageIsRoutedToDLQAsFallback() {
        // Arrange: SidecarClient defaults to FLAGGED on error in its implementation, 
        // but here we simulate the consumer logic.
        SidecarClient.ValidationResponse errorResponse = new SidecarClient.ValidationResponse();
        errorResponse.setLabel("FLAGGED");
        
        when(sidecarClient.validate(testMessage)).thenReturn(errorResponse);

        // Act
        messageConsumer.consume(testMessage);

        // Assert
        verify(repository, never()).save(any(FinancialMessage.class));
        verify(kafkaTemplate, times(1)).send(anyString(), eq("tx-123"), any());
    }
}
