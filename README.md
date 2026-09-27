# 🇿🇦 SA Financial Crime & Fraud Intelligence Platform

## 📌 Business Problem
South African financial institutions face strict FICA and AML compliance requirements. This project simulates an enterprise-grade compliance pipeline that ingests real SA company data (CIPC), global sanctions lists (OpenSanctions), and market data (JSE/SARB) to calculate entity risk scores and flag suspicious activity.

## 🏗️ Architecture Diagram
```mermaid
graph TD
    subgraph Data Sources
        A[CIPC Bulk Data]
        B[OpenSanctions API/JSON]
        C[JSE & SARB Reports]
        D[Simulated Live Transactions]
    end

    subgraph Microsoft Fabric
        subgraph Lakehouse: FinCrime_Lakehouse
            subgraph Bronze Layer
                E[bronze_cipc_companies]
                F[bronze_sanctions_entities]
                G[bronze_jse_sarb_data]
                H[bronze_pipeline_logs]
            end
            subgraph Silver Layer
                I[silver_companies_clean]
                J[silver_sanctions_exploded]
                K[silver_market_data]
            end
            subgraph Gold Layer
                L[gold_sanctions_screening]
                M[gold_company_risk_scores]
                N[gold_transaction_summary]
            end
        end
        
        subgraph Real-Time Streaming
            O[Fabric Eventstream] --> P[KQL Database: live_transactions]
        end
    end

    subgraph Consumption
        Q[Power BI Compliance Dashboard]
    end

    A -->|Data Factory Copy| E
    B -->|Data Factory HTTP| F
    C -->|Fabric Notebook PySpark| G
    D -->|Python Simulator| O
    
    E & F & G -->|Notebook: Clean & Validate| I & J & K
    I & J & K -->|Notebook: Business Logic| L & M & N
    P -.->|FICA Alert Queries| Q
    L & M & N -->|Direct Lake / SQL Endpoint| Q