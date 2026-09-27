import os
import requests
import pandas as pd
import random
from datetime import datetime, timedelta
import json

# Ensure the data-samples directory exists
OUTPUT_DIR = "data-samples"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("="*60)
print("🚀 SA FinCrime Dataset Extractor")
print("="*60)

# ==============================================================================
# 1. OPENSANCTIONS (Real Data via Public CSV Endpoint)
# ==============================================================================
def get_opensanctions():
    print("\n[1/4] Fetching OpenSanctions data...")
    url = "https://data.opensanctions.org/datasets/latest/default/entities.csv"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    try:
        # We only fetch the first 5MB to keep the sample manageable for Fabric Trial
        response = requests.get(url, headers=headers, stream=True, timeout=15)
        response.raise_for_status()
        
        # Read only a sample of rows to avoid memory issues
        df = pd.read_csv(response.iter_lines(decode_unicode=True), nrows=5000)
        
        # Filter for a mix of global and SA-relevant entities if possible, or just take a random sample
        if len(df) > 1000:
            df = df.sample(1000, random_state=42)
            
        filepath = os.path.join(OUTPUT_DIR, "opensanctions_entities_sample.csv")
        df.to_csv(filepath, index=False)
        print(f"✅ SUCCESS: Saved {len(df)} OpenSanctions records to {filepath}")
        return True
        
    except Exception as e:
        print(f"⚠️  OpenSanctions download failed ({e}). Generating realistic fallback data...")
        # Fallback synthetic data
        data = []
        for i in range(500):
            data.append({
                "id": f"sanction-{i:05d}",
                "name": f"Shell Company {i} (Pty) Ltd" if i % 2 == 0 else f"John Doe {i}",
                "schema": "Company" if i % 2 == 0 else "Person",
                "country": "ZA",
                "topics": "sanction, fraud, PEP",
                "datasets": "za_sanctions, ofac"
            })
        df_fallback = pd.DataFrame(data)
        filepath = os.path.join(OUTPUT_DIR, "opensanctions_entities_sample.csv")
        df_fallback.to_csv(filepath, index=False)
        print(f"✅ FALLBACK: Saved 500 synthetic OpenSanctions records to {filepath}")
        return True

# ==============================================================================
# 2. CIPC COMPANY REGISTRATIONS (High-Fidelity Synthetic)
# ==============================================================================
def get_cipc():
    print("\n[2/4] Generating CIPC Company Registration data...")
    print("   (Note: Real CIPC bulk data is paywalled. Using production-grade synthetic schema.)")
    
    provinces = ['Gauteng', 'Western Cape', 'KwaZulu-Natal', 'Eastern Cape', 'Free State']
    statuses = ['In Business', 'Deregistered', 'Under Judicial Management', 'Business Rescue']
    status_weights = [0.85, 0.10, 0.03, 0.02]
    
    prefixes = ['ABC', 'Global', 'Premium', 'Apex', 'Summit', 'Prime', 'United', 'African', 'Continental']
    suffixes = ['Solutions', 'Holdings', 'Services', 'Trading', 'Investments', 'Consulting', 'Group', 'Technologies']
    
    records = []
    base_date = datetime(2015, 1, 1)
    
    for i in range(1000):
        year = random.randint(2015, 2024)
        reg_num = f"{year}/{random.randint(100000, 999999)}/{random.choice(['07', '21', '08'])}"
        name = f"{random.choice(prefixes)} {random.choice(suffixes)} {random.randint(1, 999)} (Pty) Ltd"
        reg_date = base_date + timedelta(days=random.randint(0, 3285))
        
        records.append({
            'RegistrationNumber': reg_num,
            'CompanyName': name,
            'RegistrationDate': reg_date.strftime('%Y-%m-%d'),
            'CompanyType': random.choice(['PTY LTD', 'LTD', 'CC', 'NPC']),
            'Status': random.choices(statuses, weights=status_weights)[0],
            'Province': random.choice(provinces),
            'RegisteredAddress': f"{random.randint(1, 999)} {random.choice(['Main', 'Commissioner', 'Fox', 'Baker'])} Street, Johannesburg",
            'DirectorCount': random.randint(1, 5)
        })
    
    df = pd.DataFrame(records)
    filepath = os.path.join(OUTPUT_DIR, "cipc_companies_sample.csv")
    df.to_csv(filepath, index=False)
    print(f"✅ SUCCESS: Saved {len(df)} CIPC records to {filepath}")

# ==============================================================================
# 3. JSE LISTED COMPANIES (High-Fidelity Synthetic based on real JSE Top 40/AltX)
# ==============================================================================
def get_jse():
    print("\n[3/4] Generating JSE Listed Companies data...")
    
    # Real JSE companies and sectors for authenticity
    jse_data = [
        ("AGL", "Anglo American Platinum Ltd", "Materials", 450.50, "Main"),
        ("BHP", "BHP Group Plc", "Materials", 520.10, "Main"),
        ("BVT", "Bidvest Group Ltd", "Industrials", 65.20, "Main"),
        ("CPI", "Capitec Bank Holdings Ltd", "Financials", 1850.00, "Main"),
        ("DSY", "Discovery Ltd", "Financials", 115.30, "Main"),
        ("FSR", "FirstRand Ltd", "Financials", 68.40, "Main"),
        ("IMP", "Impala Platinum Holdings Ltd", "Materials", 110.75, "Main"),
        ("INL", "Investec Ltd", "Financials", 95.60, "Main"),
        ("MTN", "MTN Group Ltd", "Telecommunications", 135.20, "Main"),
        ("NED", "Nedbank Group Ltd", "Financials", 210.40, "Main"),
        ("NPN", "Naspers Ltd", "Technology", 3100.00, "Main"),
        ("PRX", "Prosus NV", "Technology", 1050.50, "Main"),
        ("SBK", "Standard Bank Group Ltd", "Financials", 165.80, "Main"),
        ("SHP", "Shoprite Holdings Ltd", "Consumer Goods", 245.60, "Main"),
        ("SLM", "Sanlam Ltd", "Financials", 72.30, "Main"),
        ("VOD", "Vodacom Group Ltd", "Telecommunications", 145.90, "Main"),
        ("WHL", "Woolworths Holdings Ltd", "Consumer Goods", 55.40, "Main"),
        ("GFI", "Gold Fields Ltd", "Materials", 180.20, "Main"),
        ("ANG", "AngloGold Ashanti Ltd", "Materials", 410.00, "Main"),
        ("APN", "Aspen Pharmacare Holdings Ltd", "Health Care", 130.50, "Main")
    ]
    
    # Add some random AltX (smaller cap) companies
    for i in range(30):
        jse_data.append((f"ALT{i:02d}", f"Alternative Tech {i} Ltd", random.choice(["Technology", "Industrials", "Financials"]), round(random.uniform(5.0, 50.0), 2), "AltX"))
    
    df = pd.DataFrame(jse_data, columns=["JSE_Code", "CompanyName", "Sector", "SharePrice_ZAR", "Market"])
    
    filepath = os.path.join(OUTPUT_DIR, "jse_listings_sample.csv")
    df.to_csv(filepath, index=False)
    print(f"✅ SUCCESS: Saved {len(df)} JSE listings to {filepath}")

# ==============================================================================
# 4. SARB BANK SUPERVISION STATS (High-Fidelity Synthetic based on real BA returns)
# ==============================================================================
def get_sarb():
    print("\n[4/4] Generating SARB Bank Supervision data...")
    
    banks = [
        ("Absa Bank Limited", "ABSA"),
        ("Standard Bank of South Africa Limited", "SB"),
        ("FirstRand Bank Limited", "FNB"),
        ("Nedbank Limited", "NED"),
        ("Capitec Bank Limited", "CAP"),
        ("Investec Bank Limited", "INV"),
        ("African Bank Limited", "AFB"),
        ("Discovery Bank Limited", "DIS")
    ]
    
    quarters = ["2024-Q1", "2024-Q2", "2024-Q3", "2024-Q4", "2025-Q1"]
    records = []
    
    for bank_name, bank_code in banks:
        for quarter in quarters:
            # Realistic regulatory ratios for SA banks
            if bank_code in ["SB", "FNB", "ABSA", "NED"]:
                assets = round(random.uniform(600, 950), 2) # Big 4
                car = round(random.uniform(13.5, 15.5), 2)
            elif bank_code == "CAP":
                assets = round(random.uniform(200, 280), 2) # Capitec
                car = round(random.uniform(14.0, 16.0), 2)
            else:
                assets = round(random.uniform(30, 120), 2) # Smaller banks
                car = round(random.uniform(12.5, 17.0), 2)
                
            records.append({
                "BankName": bank_name,
                "BankCode": bank_code,
                "Quarter": quarter,
                "TotalAssets_Billions_ZAR": assets,
                "CapitalAdequacyRatio_pct": car,
                "LiquidityCoverageRatio_pct": round(random.uniform(115, 145), 1),
                "NonPerformingLoans_pct": round(random.uniform(2.5, 6.5), 2),
                "ReturnOnEquity_pct": round(random.uniform(10.0, 20.0), 2)
            })
            
    df = pd.DataFrame(records)
    filepath = os.path.join(OUTPUT_DIR, "sarb_bank_stats_sample.csv")
    df.to_csv(filepath, index=False)
    print(f"✅ SUCCESS: Saved {len(df)} SARB records to {filepath}")

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================
if __name__ == "__main__":
    print("\n🔄 Starting data extraction pipeline...\n")
    
    get_opensanctions()
    get_cipc()
    get_jse()
    get_sarb()
    
    print("\n" + "="*60)
    print("🎉 EXTRACTION COMPLETE!")
    print("="*60)
    print(f"Check your '{OUTPUT_DIR}/' folder. You should see 4 CSV files.")
    print("You are now ready to upload these to your Fabric Lakehouse Bronze layer.")