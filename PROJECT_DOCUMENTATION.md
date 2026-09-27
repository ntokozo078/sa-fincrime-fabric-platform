# SA Financial Crime & Fraud Intelligence Platform

## Executive Summary
A comprehensive real-time financial crime detection platform built on Microsoft Fabric, implementing the Medallion Architecture (Bronze → Silver → Gold) with streaming capabilities for live transaction monitoring.

## Architecture Overview

### Phase 1-3: Batch Processing (Medallion Architecture)
- **Bronze Layer**: Raw data ingestion from CIPC, OpenSanctions, JSE, and SARB
- **Silver Layer**: Data cleaning, standardization, and deduplication
- **Gold Layer**: Business logic, risk scoring, and sanctions screening

### Phase 4-5: Real-Time Streaming
- **Eventstream**: Live transaction ingestion via Custom App endpoint
- **KQL Database**: Real-time storage and query engine
- **Fraud Detection**: KQL queries for FICA threshold alerts, high-risk company tracking, and velocity spike detection

### Phase 6: Power BI Dashboard
- Interactive compliance dashboard with risk distribution, sanctions hits, and high-risk company details
- Real-time streaming data integration
- Slicers for risk category, province, and bank filtering

## Key Features

### 1. Fuzzy Matching for Sanctions Screening
- Implemented Levenshtein distance algorithm in PySpark
- 70% confidence threshold to catch name variations
- Successfully matched companies against OpenSanctions database

### 2. Rule-Based Risk Scoring Model
- Weighted scoring: Sanctions hit (+50), New company (+15), Low directors (+20), High-risk province (+10), JSE listed (-20)
- Risk categories: HIGH (≥70), MEDIUM (≥40), LOW (<40)
- Results: 14 HIGH, 42 MEDIUM, 835 LOW risk companies

### 3. Real-Time Fraud Detection
- Python transaction simulator generating realistic SA bank transactions
- Fabric Eventstream for sub-second ingestion
- KQL queries detecting:
  - FICA threshold violations (transactions > R100,000)
  - High-risk company transactions
  - Velocity spikes (>3 large transactions per hour)

## Technology Stack
- **Microsoft Fabric**: OneLake, Eventhouse, KQL Database, Eventstream
- **Apache Spark**: PySpark for data transformation
- **Python**: Transaction simulator, data processing
- **Power BI**: Interactive compliance dashboard
- **Delta Lake**: ACID transactions, schema enforcement

## Data Sources
1. **CIPC Companies**: 1,000 South African company registrations
2. **OpenSanctions**: 500 sanctioned entities (with 3 test matches)
3. **JSE Listings**: 50 Johannesburg Stock Exchange companies
4. **SARB Bank Stats**: 40 quarterly bank statistics
5. **Live Transactions**: Real-time streaming via Python simulator

## Pipeline Orchestration
- **Bronze Master Pipeline**: Ingests and validates all source data
- **Silver Master Pipeline**: Cleans and standardizes data (chained to Bronze)
- **Gold Notebooks**: Risk scoring, sanctions screening, master view creation

## Key Metrics
- **Total Companies Screened**: 891
- **Sanctions Hits**: 14 (1.57%)
- **High-Risk Companies**: 14
- **Real-Time Transactions**: Streaming at 1 transaction/2 seconds
- **FICA Alerts**: Transactions > R100,000 flagged automatically

## How to Run
1. Clone the repository
2. Set up Microsoft Fabric workspace
3. Run Bronze pipeline: `pl_bronze_master`
4. Silver pipeline auto-triggers via pipeline chaining
5. Run Gold notebooks in sequence
6. Start transaction simulator: `python streaming/transaction_simulator.py`
7. Open Power BI dashboard: `FinCrime_Compliance_Dashboard`

## Interview Talking Points
- Implemented Medallion Architecture for scalable data processing
- Built fuzzy matching with Levenshtein distance for sanctions screening
- Created rule-based risk scoring model with weighted factors
- Designed real-time streaming pipeline with Fabric Eventstream
- Used push-down architecture for Power BI performance optimization
- Handled schema evolution and data quality scoring throughout pipeline

## Author
Ntokozo Ntombela
Date: September 2026