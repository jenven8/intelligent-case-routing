#!/bin/bash

# Test script for the Intelligent Case Routing API
# Usage: ./test_api.sh <your-railway-url>

if [ $# -eq 0 ]; then
    echo "Usage: $0 <api-url>"
    echo "Example: $0 https://intelligent-case-routing-production-abc123.up.railway.app"
    exit 1
fi

API_URL=$1
echo "🧪 Testing Intelligent Case Routing API at: $API_URL"
echo "=================================================="

# Test 1: Health Check
echo ""
echo "1. Testing health endpoint..."
curl -s "$API_URL/health" | python3 -m json.tool

# Test 2: Model Info
echo ""
echo "2. Testing model info endpoint..."
curl -s "$API_URL/model-info" | python3 -m json.tool

# Test 3: Case Analysis - Payroll Issue
echo ""
echo "3. Testing case analysis - Payroll Issue..."
curl -s -X POST "$API_URL/analyze-case" \
     -H "Content-Type: application/json" \
     -d '{
       "subject": "Payroll tax withholding issue",
       "description": "Employee W2 shows incorrect federal tax withholding amount for Q4",
       "priority": "High",
       "customer_type": "Business"
     }' | python3 -m json.tool

# Test 4: Case Analysis - Banking Issue
echo ""
echo "4. Testing case analysis - Banking Issue..."
curl -s -X POST "$API_URL/analyze-case" \
     -H "Content-Type: application/json" \
     -d '{
       "subject": "ACH transfer failed",
       "description": "Bank deposit was rejected due to routing number issue",
       "priority": "Medium"
     }' | python3 -m json.tool

# Test 5: Case Analysis - Fraud Issue
echo ""
echo "5. Testing case analysis - Fraud Issue..."
curl -s -X POST "$API_URL/analyze-case" \
     -H "Content-Type: application/json" \
     -d '{
       "subject": "Suspicious transaction detected",
       "description": "Unauthorized charges appearing on customer account",
       "priority": "High"
     }' | python3 -m json.tool

echo ""
echo "✅ API testing complete!"
echo "📖 Visit $API_URL/docs for interactive API documentation"
