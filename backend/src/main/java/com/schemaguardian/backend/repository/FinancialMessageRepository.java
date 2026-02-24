package com.schemaguardian.backend.repository;

import com.schemaguardian.backend.model.FinancialMessage;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface FinancialMessageRepository extends JpaRepository<FinancialMessage, String> {
}
