# Intelligent Case Routing API

AI-powered case classification and routing system for customer support.

## Features

- **Automated Case Classification**: Categorizes cases into payroll, banking, fraud, technical, billing, and compliance
- **Queue Routing**: Automatically assigns cases to appropriate support teams
- **Priority Assessment**: Determines case priority based on content analysis
- **Resolution Time Estimation**: Provides estimated resolution timeframes
- **Actionable Insights**: Suggests next steps for case handlers

## API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /analyze-case` - Analyze and classify a case
- `GET /model-info` - Model information and statistics
- `GET /categories` - Available categories and queue mappings
- `GET /docs` - Interactive API documentation

## Usage

### Analyze a Case

```bash
curl -X POST "https://your-api-url/analyze-case" \
     -H "Content-Type: application/json" \
     -d '{
       "subject": "Payroll tax withholding issue",
       "description": "Employee W2 shows incorrect federal tax withholding amount",
       "priority": "Medium",
       "customer_type": "Business"
     }'
```

### Response Example

```json
{
  "case_id": "CASE-20240827180000",
  "predicted_category": "payroll",
  "confidence_score": 0.85,
  "recommended_queue": "Payroll Support Team",
  "priority_level": "Medium",
  "estimated_resolution_time": "1-2 business days",
  "suggested_actions": [
    "Verify employee information",
    "Check payroll processing status",
    "Review tax withholding settings",
    "Escalate to payroll specialist if needed"
  ]
}
```

## Deployment

This API is containerized and ready for deployment on platforms like Railway, Render, or Google Cloud Run.

## Model Information

- **Type**: Rule-based classifier with keyword matching
- **Categories**: 6 main categories (payroll, banking, fraud, technical, billing, compliance)
- **Accuracy**: ~85% estimated
- **Response Time**: < 100ms average
