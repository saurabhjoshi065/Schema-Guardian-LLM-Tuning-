package com.schemaguardian.backend.service;

import lombok.Data;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.boot.web.client.RestTemplateBuilder;

import java.time.Duration;
import java.util.Map;

@Service
public class SidecarClient {

    private final RestTemplate restTemplate;
    private final String sidecarUrl;

    public SidecarClient(RestTemplateBuilder builder, 
                         @Value("${sidecar.url}") String sidecarUrl,
                         @Value("${sidecar.timeout-ms}") int timeout) {
        this.restTemplate = builder
                .setConnectTimeout(Duration.ofMillis(timeout))
                .setReadTimeout(Duration.ofMillis(timeout))
                .build();
        this.sidecarUrl = sidecarUrl;
    }

    public ValidationResponse validate(Map<String, Object> message) {
        ValidationRequest request = new ValidationRequest(message);
        try {
            return restTemplate.postForObject(sidecarUrl, request, ValidationResponse.class);
        } catch (Exception e) {
            // Default to FLAGGED if sidecar is unreachable for safety
            ValidationResponse fallback = new ValidationResponse();
            fallback.setLabel("FLAGGED");
            return fallback;
        }
    }

    @Data
    public static class ValidationRequest {
        private final Map<String, Object> message;
    }

    @Data
    public static class ValidationResponse {
        private String label;
        private double latencyMs;
    }
}
