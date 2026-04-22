"""Generate crime analytics datasets for CrimeWatch."""
import pandas as pd
import numpy as np
import json
import os

np.random.seed(7)
os.makedirs("data", exist_ok=True)

# ============================================================
# 1. CRIME RECORDS (City × Crime Type × Year × Month)
# ============================================================
CITIES = [
    ("Mumbai", "Maharashtra", 19.0760, 72.8777, 20.4),
    ("Delhi", "Delhi", 28.6139, 77.2090, 32.9),
    ("Bangalore", "Karnataka", 12.9716, 77.5946, 12.3),
    ("Hyderabad", "Telangana", 17.3850, 78.4867, 10.0),
    ("Chennai", "Tamil Nadu", 13.0827, 80.2707, 11.2),
    ("Kolkata", "West Bengal", 22.5726, 88.3639, 14.9),
    ("Pune", "Maharashtra", 18.5204, 73.8567, 6.6),
    ("Ahmedabad", "Gujarat", 23.0225, 72.5714, 8.4),
    ("Jaipur", "Rajasthan", 26.9124, 75.7873, 4.1),
    ("Lucknow", "Uttar Pradesh", 26.8467, 80.9462, 3.8),
    ("Surat", "Gujarat", 21.1702, 72.8311, 6.9),
    ("Kanpur", "Uttar Pradesh", 26.4499, 80.3319, 3.1),
    ("Nagpur", "Maharashtra", 21.1458, 79.0882, 2.9),
    ("Indore", "Madhya Pradesh", 22.7196, 75.8577, 2.4),
    ("Bhopal", "Madhya Pradesh", 23.2599, 77.4126, 2.0),
    ("Patna", "Bihar", 25.5941, 85.1376, 2.5),
    ("Chandigarh", "Punjab", 30.7333, 76.7794, 1.2),
    ("Coimbatore", "Tamil Nadu", 11.0168, 76.9558, 2.2),
    ("Visakhapatnam", "Andhra Pradesh", 17.6868, 83.2185, 2.2),
    ("Kochi", "Kerala", 9.9312, 76.2673, 2.1),
]

CRIME_TYPES = {
    "Theft": 1.0, "Assault": 0.45, "Fraud": 0.72, "Burglary": 0.52,
    "Vandalism": 0.38, "Robbery": 0.30, "Cybercrime": 0.68,
    "Drug Offense": 0.42, "Homicide": 0.08, "Harassment": 0.55
}

rows = []
for city, state, lat, lon, pop in CITIES:
    base_mult = np.random.uniform(0.7, 1.4)
    for yr in range(2019, 2025):
        year_factor = 1 + (yr - 2019) * 0.04 + np.random.uniform(-0.1, 0.1)
        for month in range(1, 13):
            seasonal = 1 + 0.15 * np.sin((month - 3) / 12 * 2 * np.pi)
            for ctype, weight in CRIME_TYPES.items():
                base = int(pop * weight * base_mult * year_factor * seasonal * np.random.uniform(8, 14))
                severity = np.random.choice(["Low", "Medium", "High", "Critical"],
                                             p=[0.45, 0.30, 0.18, 0.07])
                resolved = np.random.uniform(0.35, 0.78)
                rows.append({
                    "City": city, "State": state, "Lat": lat, "Lon": lon,
                    "Population_M": pop, "Year": yr, "Month": month,
                    "Crime_Type": ctype, "Cases": max(1, base),
                    "Severity": severity, "Resolution_Rate": round(resolved, 2),
                    "Arrests": int(base * resolved * np.random.uniform(0.6, 0.9)),
                    "Response_Time_Min": round(np.random.uniform(8, 45), 1),
                })

df = pd.DataFrame(rows)
df.to_csv("data/crime_data.csv", index=False)
print(f"✅ crime_data.csv: {len(df):,} rows · {df.City.nunique()} cities · {df.Crime_Type.nunique()} crime types")

# ============================================================
# 2. CRIME REPORTS (for text classification)
# ============================================================
reports = [
    # Theft (15)
    ("Wallet stolen from jacket pocket on crowded metro during rush hour.", "Theft"),
    ("Mobile phone snatched by two men on motorcycle near market street.", "Theft"),
    ("Purse pickpocketed while shopping at the busy festival bazaar.", "Theft"),
    ("Laptop bag taken from parked car with broken window glass.", "Theft"),
    ("Gold chain grabbed from woman walking alone late at night.", "Theft"),
    ("Backpack with valuables stolen from cafe table when owner stepped away.", "Theft"),
    ("Bicycle missing from apartment parking lot despite being locked.", "Theft"),
    ("Cash and jewelry taken from hotel room safe during stay.", "Theft"),
    ("Shop goods missing after suspicious customer visited yesterday afternoon.", "Theft"),
    ("Delivery package stolen from doorstep within hours of arrival.", "Theft"),
    ("Smartphone lifted from handbag during crowded temple visit.", "Theft"),
    ("Watch missing from gym locker after morning workout session.", "Theft"),
    ("Groceries and wallet stolen from shopping cart momentarily left alone.", "Theft"),
    ("Designer sunglasses taken from restaurant table during dinner.", "Theft"),
    ("Cash envelope disappeared from office desk during lunch break.", "Theft"),

    # Assault (12)
    ("Man attacked and beaten badly by group outside the nightclub.", "Assault"),
    ("Physical fight broke out between two neighbors over parking dispute.", "Assault"),
    ("Woman punched and pushed to ground by unknown attacker in park.", "Assault"),
    ("Bar brawl resulted in serious injuries needing hospital treatment.", "Assault"),
    ("Road rage incident escalated to physical violence between drivers.", "Assault"),
    ("Domestic abuse reported by neighbor hearing screams and crashes.", "Assault"),
    ("Student assaulted by seniors during college ragging incident reported.", "Assault"),
    ("Customer attacked shop owner after heated argument over refund.", "Assault"),
    ("Group fight erupted at wedding function leading to multiple injuries.", "Assault"),
    ("Taxi driver beaten by passengers refusing to pay the fare.", "Assault"),
    ("Delivery boy attacked for taking too long with food order.", "Assault"),
    ("Security guard assaulted while trying to stop trespassers at night.", "Assault"),

    # Fraud (12)
    ("Fake online shopping website took payment but never shipped products.", "Fraud"),
    ("Caller pretended to be bank officer and stole credit card details.", "Fraud"),
    ("Investment scheme promised huge returns but organizer disappeared with money.", "Fraud"),
    ("Forged property documents used to sell the same flat twice.", "Fraud"),
    ("Job offer scam demanded deposit for training that never happened.", "Fraud"),
    ("Fake lottery winning message tricked elderly person into sending money.", "Fraud"),
    ("Insurance claim submitted with fabricated accident report and false photos.", "Fraud"),
    ("Romance scam on dating app drained victim savings over months.", "Fraud"),
    ("UPI payment fraud where scammer reversed transactions after delivery.", "Fraud"),
    ("Fake charity collected donations claiming to help flood victims.", "Fraud"),
    ("Counterfeit currency notes passed off at small neighborhood shops.", "Fraud"),
    ("Business partner forged signatures to withdraw company funds illegally.", "Fraud"),

    # Burglary (10)
    ("House broken into through back window while family was on vacation.", "Burglary"),
    ("Shop shutters forced open at night and cash register emptied.", "Burglary"),
    ("Apartment burglarized during daytime when residents were at work.", "Burglary"),
    ("Warehouse broken into and electronics worth lakhs were stolen overnight.", "Burglary"),
    ("Office premises ransacked and computers taken through rooftop entry.", "Burglary"),
    ("Jewelry shop safe cracked open during early morning hours.", "Burglary"),
    ("Temple donation box broken and contents emptied after closing time.", "Burglary"),
    ("School laboratory raided and expensive equipment taken overnight.", "Burglary"),
    ("ATM machine forcibly opened using gas cutter at isolated location.", "Burglary"),
    ("Empty bungalow stripped of fixtures fittings and copper wiring.", "Burglary"),

    # Cybercrime (12)
    ("Phishing email stole login credentials and emptied savings account.", "Cybercrime"),
    ("Ransomware encrypted all company files demanding bitcoin payment.", "Cybercrime"),
    ("Fake social media account used to defame and harass victim online.", "Cybercrime"),
    ("Hacker accessed email and sent fraudulent messages to all contacts.", "Cybercrime"),
    ("Identity theft online opened multiple loan accounts under victim name.", "Cybercrime"),
    ("Dark web listing offered stolen personal data of thousands of users.", "Cybercrime"),
    ("Bitcoin wallet drained through sophisticated malware on mobile device.", "Cybercrime"),
    ("Deepfake video used to blackmail businessman for large ransom payment.", "Cybercrime"),
    ("Online banking OTP intercepted through SIM swap fraud technique.", "Cybercrime"),
    ("Credit card skimmer installed on ATM captured hundreds of card details.", "Cybercrime"),
    ("Corporate server breached and customer database leaked on underground forum.", "Cybercrime"),
    ("Fake customer support number tricked users into sharing banking passwords.", "Cybercrime"),

    # Vandalism (8)
    ("Public park benches smashed and graffiti painted on all walls.", "Vandalism"),
    ("Parked cars scratched with keys along entire street last night.", "Vandalism"),
    ("School windows broken and classroom furniture destroyed by intruders.", "Vandalism"),
    ("Statue in public square defaced with paint and rude slogans.", "Vandalism"),
    ("Bus stop shelter glass panels smashed during rowdy late night party.", "Vandalism"),
    ("Community hall walls spray painted with obscene gang related graffiti.", "Vandalism"),
    ("Shop signboards damaged and neon lights broken by drunk group.", "Vandalism"),
    ("Public toilets destroyed with plumbing fixtures ripped from walls.", "Vandalism"),

    # Robbery (8)
    ("Armed robbers held up bank tellers and escaped with large cash.", "Robbery"),
    ("Jewelry store robbed by masked men using guns and hammers.", "Robbery"),
    ("Petrol pump attendant threatened with knife and cash register emptied.", "Robbery"),
    ("Couple mugged at knifepoint while walking home after evening movie.", "Robbery"),
    ("Cash van attacked by gang who escaped with payroll money bags.", "Robbery"),
    ("Auto rickshaw driver robbed at night by armed passengers taking cash.", "Robbery"),
    ("Elderly couple tied up at home while intruders took valuables.", "Robbery"),
    ("Chain snatching by bike borne thieves targeting morning walkers.", "Robbery"),

    # Drug Offense (7)
    ("Large cache of narcotics seized during raid on suburban apartment.", "Drug Offense"),
    ("Peddler caught selling contraband near school premises to students.", "Drug Offense"),
    ("Party raid resulted in arrest of attendees for illegal substance possession.", "Drug Offense"),
    ("Shipment of illegal drugs intercepted at port during customs check.", "Drug Offense"),
    ("Chemist shop owner arrested for selling prescription drugs without papers.", "Drug Offense"),
    ("Synthetic drug manufacturing lab discovered in remote rural location.", "Drug Offense"),
    ("College student found dealing marijuana within campus hostel grounds.", "Drug Offense"),

    # Harassment (8)
    ("Woman stalked by former colleague who sends threatening messages daily.", "Harassment"),
    ("Neighbor repeatedly makes offensive comments and gestures toward family.", "Harassment"),
    ("Online trolling campaign targeting journalist with rape and death threats.", "Harassment"),
    ("Workplace bullying by supervisor creating hostile environment for team.", "Harassment"),
    ("Anonymous caller repeatedly disturbs elderly resident with prank calls.", "Harassment"),
    ("Tenant harassed by landlord demanding extra payments beyond agreement.", "Harassment"),
    ("Student continuously bullied by classmates causing severe mental distress.", "Harassment"),
    ("Ex-partner sending unwanted messages and showing up at workplace repeatedly.", "Harassment"),
]

reports_df = pd.DataFrame(reports, columns=['Report', 'Crime_Type'])
reports_df.to_csv("data/reports.csv", index=False)
print(f"✅ reports.csv: {len(reports_df)} reports across {reports_df.Crime_Type.nunique()} categories")

# ============================================================
# 3. CITY FACTS
# ============================================================
city_facts = {
    "Mumbai": "Financial capital of India with highest reported crime volume due to population density.",
    "Delhi": "National capital with elevated crime statistics particularly in theft and harassment.",
    "Bangalore": "Tech hub with growing cybercrime incidents alongside traditional offenses.",
    "Hyderabad": "Pearl city known for relatively better law enforcement response times.",
    "Chennai": "Coastal metropolis with moderate crime rates and strong community policing.",
    "Kolkata": "Cultural capital with unique crime patterns centered in specific districts.",
    "Pune": "Educational hub where student-related incidents form significant portion.",
    "Ahmedabad": "Commercial center with fraud and white collar crimes being prominent.",
    "Jaipur": "Tourist destination with theft incidents concentrated in heritage areas.",
    "Lucknow": "Cultural city with rising cybercrime awareness campaigns.",
}
with open("data/city_facts.json", "w") as f:
    json.dump(city_facts, f, indent=2)
print(f"✅ city_facts.json: {len(city_facts)} cities")

print("\n🎉 All datasets ready for CrimeWatch!")
