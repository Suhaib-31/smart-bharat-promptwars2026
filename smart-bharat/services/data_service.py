"""
Smart Bharat - Static Civic Data
Curated reference data for the Government Service Finder and Document Guide
features. This acts as a reliable fallback/base layer, complemented by
live Gemini responses for personalized details.
"""

SERVICE_CATEGORIES = [
    {"id": "identity", "name": "Identity Documents", "icon": "id-card",
     "desc": "Aadhaar, PAN, Voter ID"},
    {"id": "passport", "name": "Passport & Travel", "icon": "plane",
     "desc": "Passport, Visa services"},
    {"id": "transport", "name": "Transport & License", "icon": "car",
     "desc": "Driving License, RC, Vehicle services"},
    {"id": "taxes", "name": "Taxes & Finance", "icon": "receipt",
     "desc": "Income Tax, GST, banking schemes"},
    {"id": "health", "name": "Health Services", "icon": "heart-pulse",
     "desc": "Ayushman Bharat, hospitals, insurance"},
    {"id": "education", "name": "Education & Scholarships", "icon": "graduation-cap",
     "desc": "Scholarships, school/college admissions"},
    {"id": "agriculture", "name": "Agriculture", "icon": "wheat",
     "desc": "PM-KISAN, crop insurance, subsidies"},
    {"id": "welfare", "name": "Welfare & Pension", "icon": "hand-heart",
     "desc": "Pension, disability, social security"},
]

DOCUMENT_GUIDES = {
    "passport": {
        "title": "Passport",
        "icon": "book-open",
        "documents": [
            "Proof of Address (Aadhaar/Utility Bill/Rent Agreement)",
            "Proof of Date of Birth (Birth Certificate/10th Marksheet)",
            "Passport-size photographs (as per specifications)",
            "Aadhaar Card",
            "Old Passport (if renewal)",
        ],
        "steps": [
            "Register on the Passport Seva Portal (passportindia.gov.in)",
            "Fill the online application form (fresh or reissue)",
            "Pay the applicable fee online",
            "Schedule an appointment at your nearest Passport Seva Kendra (PSK)",
            "Visit PSK with original documents for verification",
            "Police verification (if required)",
            "Passport dispatched via Speed Post",
        ],
        "tips": [
            "Book PSK appointments early morning for better slot availability",
            "Carry both original and self-attested photocopies of documents",
            "Tatkal scheme available for urgent passports at extra fee",
            "Track application status on the portal using your file number",
        ],
    },
    "driving-license": {
        "title": "Driving License",
        "icon": "car-front",
        "documents": [
            "Proof of Age (Birth Certificate/10th Marksheet)",
            "Proof of Address (Aadhaar/Utility Bill)",
            "Passport-size photographs",
            "Learner's License (for permanent DL)",
            "Medical Certificate (Form 1A, for transport vehicles)",
        ],
        "steps": [
            "Apply for Learner's License (LL) on parivahan.gov.in",
            "Pass the online LL test",
            "Practice driving for at least 30 days",
            "Apply for Permanent DL and book a driving test slot",
            "Pass the driving skill test at RTO",
            "Receive DL by post or download digital copy via DigiLocker",
        ],
        "tips": [
            "LL is valid for 6 months, apply for permanent DL within that window",
            "Use the Parivahan Sarathi portal for online slot booking",
            "Keep DigiLocker app handy for a digital copy of your license",
        ],
    },
    "birth-certificate": {
        "title": "Birth Certificate",
        "icon": "baby",
        "documents": [
            "Hospital discharge slip / birth proof from hospital",
            "Parents' Aadhaar Cards",
            "Proof of Address",
            "Marriage certificate of parents (if applicable)",
        ],
        "steps": [
            "Report birth to local municipal corporation/gram panchayat within 21 days",
            "Fill the birth registration form (usually done by hospital)",
            "Submit required documents to the Registrar of Births & Deaths",
            "Collect the birth certificate after verification",
            "For delayed registration, an affidavit and additional proof may be needed",
        ],
        "tips": [
            "Most hospitals register births automatically — confirm with them first",
            "Apply online via your state's e-district portal where available",
            "Delayed registration (after 1 year) requires a magistrate's order",
        ],
    },
    "income-certificate": {
        "title": "Income Certificate",
        "icon": "file-text",
        "documents": [
            "Aadhaar Card",
            "Proof of Address",
            "Salary slip / Form 16 / self-employment declaration",
            "Ration Card (if available)",
            "Passport-size photograph",
        ],
        "steps": [
            "Visit your state's e-district / Tehsildar portal",
            "Fill the income certificate application form",
            "Upload/attach supporting income documents",
            "Application reviewed by Revenue/Tehsildar office",
            "Certificate issued digitally or physically",
        ],
        "tips": [
            "Valid for 1 year from date of issue in most states",
            "Required for scholarships, caste-cum-income certificates, and welfare schemes",
        ],
    },
    "domicile": {
        "title": "Domicile Certificate",
        "icon": "home",
        "documents": [
            "Aadhaar Card",
            "Proof of residence for required duration (utility bills, rent agreement)",
            "School leaving certificate / education records",
            "Ration card (if available)",
        ],
        "steps": [
            "Apply through state e-district portal or Tehsildar office",
            "Fill domicile application with residence history",
            "Submit proof of continuous residence (usually 10-15 years depending on state)",
            "Verification by local revenue officials",
            "Certificate issued after approval",
        ],
        "tips": [
            "Required for state quota admissions and government jobs",
            "Processing time varies by state, typically 15-30 days",
        ],
    },
    "pension": {
        "title": "Pension Services",
        "icon": "piggy-bank",
        "documents": [
            "Aadhaar Card",
            "Age proof",
            "Bank account details (linked with Aadhaar)",
            "Income certificate (for social security pensions)",
            "Disability certificate (if applicable)",
        ],
        "steps": [
            "Identify the applicable scheme (EPS, NPS, Old Age Pension, etc.)",
            "Apply via EPFO portal (epfindia.gov.in) or state welfare portal",
            "Submit required KYC and bank details",
            "Verification by concerned department",
            "Pension credited monthly to linked bank account",
        ],
        "tips": [
            "Link Aadhaar with bank account for direct benefit transfer (DBT)",
            "Jeevan Pramaan (digital life certificate) simplifies annual verification",
        ],
    },
    "scholarship": {
        "title": "Scholarship",
        "icon": "award",
        "documents": [
            "Aadhaar Card",
            "Income Certificate",
            "Caste Certificate (if applicable)",
            "Previous year marksheets",
            "Bonafide/admission certificate from institution",
            "Bank account details",
        ],
        "steps": [
            "Register on National Scholarship Portal (scholarships.gov.in)",
            "Fill in personal, academic, and bank details",
            "Upload required documents",
            "Submit application before the deadline",
            "Institution verification and approval",
            "Scholarship amount disbursed via DBT",
        ],
        "tips": [
            "Apply early — portals close applications strictly on deadline",
            "Keep documents in PDF under prescribed size limits",
            "Check both central (NSP) and state-specific scholarship schemes",
        ],
    },
}

COMPLAINT_TYPES = [
    "Road & Infrastructure",
    "Water Supply",
    "Electricity",
    "Sanitation & Garbage",
    "Public Transport",
    "Corruption",
    "Noise Pollution",
    "Street Lighting",
    "Healthcare Facility",
    "Other",
]

COMPLAINT_STATUS_FLOW = ["Received", "In Progress", "Assigned", "Resolved"]
