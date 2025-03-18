from config import SPACY_MODEL
import spacy
import math

model=spacy.load(SPACY_MODEL)
risk_categories = {
    "Data Privacy & Sharing": ["third-party", "data sharing", "sell your data", "personal information", "user tracking", "cookies", "data collection", "location tracking", "opt-out", "data retention", "data breach", "data profiling", "behavioral tracking", "cross-site tracking", "location services", "data aggregation", "advertiser data sharing", "biometric data collection", "automatic data collection", "store credit card information", "opt-out limitations"],
    "Financial & Refunds": ["no refund", "non-refundable", "auto-renewal", "billing cycle", "late payment", "cancellation fee", "chargeback", "hidden fees", "price changes", "payment authorization", "subscription fees", "pre-authorized payment", "in-app purchases", "currency conversion fees", "taxes and duties"],
    "Legal & Liability": ["limited liability", "indemnify", "hold harmless", "governing law", "binding arbitration", "no warranty", "disclaimer", "limitation of liability", "class action waiver", "legal jurisdiction", "waiver of rights", "force majeure", "dispute resolution", "attorney’s fees", "intellectual property infringement", "statutory rights waiver"],
    "User Rights & Restrictions": ["account termination", "service suspension", "content removal", "revocation of access", "non-transferable", "no resale", "restricted use", "intellectual property", "user-generated content", "license to use", "royalty-free", "worldwide license", "perpetual license", "non-exclusive license", "prohibited conduct", "user responsibility", "age restrictions", "account sharing", "usage limits"],
    "Communication & Marketing": ["email marketing", "opt-in", "push notifications", "third-party advertisements", "targeted ads", "affiliate links", "marketing communications", "unsolicited messages", "telemarketing", "SMS marketing"],
    "Termination & Suspension": ["immediate termination", "without notice", "at our discretion", "account deactivation", "service discontinuation", "temporary suspension", "service revocation"],
    "Content Ownership & Usage": ["user-generated content", "license to use", "royalty-free", "perpetual license", "global license", "non-exclusive license", "content modification", "content redistribution", "content sublicensing", "waiver of content rights", "public display rights"],
    "Security & Compliance": ["no security guarantee", "data encryption not guaranteed", "unauthorized access", "service vulnerabilities", "limited data protection", "compliance waiver", "security limitations", "no liability for breaches"],
    "Miscellaneous": ["terms subject to change", "sole discretion", "non-negotiable", "user consent required", "no responsibility for damages", "no service guarantee", "beta service disclaimer", "force majeure", "updates without notice", "automatic updates", "third-party services"]
}
def detector(text):
    doc = model(text)
    named_entities = {ent.text: ent.label_ for ent in doc.ents}
    
    risk_terms = []
    detected_risk_categories = [] 

    for key, value in risk_categories.items():
        matched = [r for r in value if r.lower() in text.lower()]
        if matched:
            risk_terms.extend(matched)
            detected_risk_categories.append(key)

    risk_terms = list(set(risk_terms))
    
    total_kw = sum(len(kw) for kw in risk_categories.values())  
    total_mkw = len(risk_terms)
    risk_ratio = total_mkw / total_kw  
    base_score = min(1.0, risk_ratio ** 0.8) * 70 
    category_score = len(detected_risk_categories) * 8 
    risk_score = min(100, base_score + category_score)  
    return named_entities, detected_risk_categories, risk_score, risk_terms
    



