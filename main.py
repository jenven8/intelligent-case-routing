from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
import uvicorn
from datetime import datetime
import re

app = FastAPI(
    title="Intelligent Case Routing API",
    description="AI-powered case classification and routing system",
    version="1.0.0"
)

class CaseData(BaseModel):
    subject: str
    description: str
    priority: Optional[str] = "Medium"
    customer_type: Optional[str] = "Individual"
    
class CaseAnalysis(BaseModel):
    case_id: str
    predicted_category: str
    confidence_score: float
    recommended_queue: str
    priority_level: str
    estimated_resolution_time: str
    suggested_actions: List[str]

class CaseClassifier:
    def __init__(self):
        # Rule-based classification for demo
        self.category_keywords = {
            "payroll": ["payroll", "salary", "wages", "tax withholding", "w2", "1099", "paycheck"],
            "banking": ["bank", "deposit", "withdrawal", "account", "routing", "transfer", "ach"],
            "fraud": ["fraud", "unauthorized", "suspicious", "dispute", "chargeback", "stolen"],
            "technical": ["app", "login", "password", "error", "bug", "crash", "sync"],
            "billing": ["bill", "charge", "fee", "payment", "invoice", "refund", "subscription"],
            "compliance": ["compliance", "audit", "regulation", "kyc", "aml", "verification"]
        }
        
        self.queue_mapping = {
            "payroll": "Payroll Support Team",
            "banking": "Banking Operations",
            "fraud": "Fraud Investigation",
            "technical": "Technical Support",
            "billing": "Billing Department",
            "compliance": "Compliance Team"
        }
        
        self.priority_keywords = {
            "high": ["urgent", "critical", "emergency", "fraud", "security", "breach"],
            "medium": ["issue", "problem", "help", "support"],
            "low": ["question", "inquiry", "information", "how to"]
        }

    def classify_case(self, case_data: CaseData) -> CaseAnalysis:
        text = f"{case_data.subject} {case_data.description}".lower()
        
        # Category classification
        category_scores = {}
        for category, keywords in self.category_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text)
            if score > 0:
                category_scores[category] = score / len(keywords)
        
        if not category_scores:
            predicted_category = "general"
            confidence = 0.5
            recommended_queue = "General Support"
        else:
            predicted_category = max(category_scores, key=category_scores.get)
            confidence = min(category_scores[predicted_category] * 2, 1.0)
            recommended_queue = self.queue_mapping.get(predicted_category, "General Support")
        
        # Priority classification
        priority_level = case_data.priority.lower()
        for priority, keywords in self.priority_keywords.items():
            if any(keyword in text for keyword in keywords):
                priority_level = priority
                break
        
        # Estimated resolution time
        resolution_times = {
            "high": "2-4 hours",
            "medium": "1-2 business days",
            "low": "3-5 business days"
        }
        
        # Suggested actions
        suggested_actions = self._get_suggested_actions(predicted_category, priority_level)
        
        case_id = f"CASE-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        return CaseAnalysis(
            case_id=case_id,
            predicted_category=predicted_category,
            confidence_score=round(confidence, 2),
            recommended_queue=recommended_queue,
            priority_level=priority_level.title(),
            estimated_resolution_time=resolution_times.get(priority_level, "2-3 business days"),
            suggested_actions=suggested_actions
        )
    
    def _get_suggested_actions(self, category: str, priority: str) -> List[str]:
        actions = {
            "payroll": [
                "Verify employee information",
                "Check payroll processing status",
                "Review tax withholding settings",
                "Escalate to payroll specialist if needed"
            ],
            "banking": [
                "Verify account details",
                "Check transaction history",
                "Review banking integration status",
                "Contact banking partner if required"
            ],
            "fraud": [
                "Immediately flag account for review",
                "Document all suspicious activity",
                "Escalate to fraud investigation team",
                "Implement temporary security measures"
            ],
            "technical": [
                "Gather system logs and error details",
                "Check for known issues",
                "Test reproduction steps",
                "Escalate to engineering if needed"
            ],
            "billing": [
                "Review billing history",
                "Check payment processing status",
                "Verify subscription details",
                "Process refund if applicable"
            ],
            "compliance": [
                "Review compliance requirements",
                "Gather necessary documentation",
                "Escalate to compliance team",
                "Ensure regulatory adherence"
            ]
        }
        
        base_actions = actions.get(category, [
            "Review case details thoroughly",
            "Gather additional information if needed",
            "Follow standard resolution procedures",
            "Escalate if resolution exceeds timeframe"
        ])
        
        if priority == "high":
            base_actions.insert(0, "URGENT: Prioritize immediate attention")
        
        return base_actions

# Initialize classifier
classifier = CaseClassifier()

@app.get("/")
async def root():
    return {
        "message": "Intelligent Case Routing API",
        "version": "1.0.0",
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "case-routing-api"
    }

@app.post("/analyze-case", response_model=CaseAnalysis)
async def analyze_case(case_data: CaseData):
    try:
        analysis = classifier.classify_case(case_data)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/model-info")
async def get_model_info():
    return {
        "model_type": "Rule-based Classifier",
        "categories": list(classifier.category_keywords.keys()),
        "queues": list(classifier.queue_mapping.values()),
        "last_updated": "2024-08-27",
        "accuracy": "85% (estimated)"
    }

@app.get("/categories")
async def get_categories():
    return {
        "categories": list(classifier.category_keywords.keys()),
        "queue_mapping": classifier.queue_mapping
    }

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
