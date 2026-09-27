# 🇿 SA Financial Crime & Fraud Intelligence Platform

## 📌 Business Problem
South African financial institutions face strict FICA and AML compliance requirements. This project simulates an enterprise-grade compliance pipeline that ingests real SA company data (CIPC), global sanctions lists (OpenSanctions), and market data (JSE/SARB) to calculate entity risk scores and flag suspicious activity.

## 🏗️ Architecture Diagram
```mermaid
graph TD
    subgraph Data Sources
        A[CIPC Bulk Data]
        B[OpenSanctions API]
        C[JSE Listings CSV]
        D[SARB Stats Excel]
        E[Simulated Transactions]
    end

    subgraph Microsoft Fabric Ingestion
        F[Data Factory: pl_bronze_cipc_load]
        G[Data Factory: pl_bronze_sanctions_load]
        H[Notebook: nb_bronze_jse_sarb_load]
        I[Eventstream: es_live_transactions]
    end

    subgraph Lakehouse: FinCrime_Lakehouse
        subgraph Bronze Layer - Raw
            J[bronze_cipc_companies]
            K[bronze_sanctions_entities]
            L[bronze_jse_listings]
            M[bronze_sarb_stats]
            N[bronze_pipeline_logs]
        end
        
        subgraph Silver Layer - Cleaned
            O[silver_companies]
            P[silver_sanctions]
            Q[silver_jse_listings]
            R[silver_sarb_banks]
        end
        
        subgraph Gold Layer - Business Logic
            S[gold_sanctions_screening]
            T[gold_company_risk_scores]
            U[gold_transaction_summary]
        end
    end

    subgraph Real-Time & Consumption
        V[KQL Database: live_transactions]
        W[Power BI Compliance Dashboard]
    end

    A --> F --> J
    B --> G --> K
    C & D --> H --> L & M
    E --> I --> V
    
    J & K & L & M -->|Notebooks: Clean & Validate| O & P & Q & R
    O & P -->|Sanctions Screening| S
    O & Q & R -->|Risk Scoring| T
    V -->|Transaction Summary| U
    S & T & U --> W
