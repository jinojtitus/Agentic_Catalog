import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import yaml
import numpy as np

# Page configuration - iOS style
st.set_page_config(
    page_title="Agentic Operating System",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/jinojtitus/Agentic_Catalog',
        'Report a bug': 'https://github.com/jinojtitus/Agentic_Catalog/issues',
        'About': "Agentic Operating System - iOS-style interface for managing AI agents"
    }
)

# iOS-style Custom CSS
st.markdown("""
<style>
    /* Import SF Pro font (iOS system font) */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global iOS styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* iOS-style main header */
    .main-header {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        font-size: 2.8rem;
        font-weight: 700;
        color: #1d1d1f;
        margin-bottom: 2.5rem;
        text-align: center;
        letter-spacing: -0.02em;
    }
    
    /* iOS-style agent cards */
    .agent-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        margin-bottom: 1.5rem;
        border: 1px solid rgba(0, 0, 0, 0.04);
        transition: all 0.3s ease;
    }
    
    .agent-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
    }
    
    /* iOS-style status badges */
    .status-badge {
        display: inline-block;
        padding: 0.375rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .status-approved {
        background-color: #d1f2eb;
        color: #00a86b;
        border: 1px solid #a8e6cf;
    }
    
    .status-pilot {
        background-color: #fff3e0;
        color: #ff8f00;
        border: 1px solid #ffcc80;
    }
    
    .status-draft {
        background-color: #ffebee;
        color: #d32f2f;
        border: 1px solid #ffcdd2;
    }
    
    /* iOS-style metric cards */
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        padding: 1.5rem;
        border-radius: 16px;
        text-align: center;
        border: 1px solid rgba(0, 0, 0, 0.06);
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
        transition: all 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    }
    
    .metric-card h3 {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: #1d1d1f;
        margin: 0 0 0.5rem 0;
    }
    
    .metric-card p {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        font-size: 0.9rem;
        color: #6e6e73;
        margin: 0;
        font-weight: 500;
    }
    
    /* iOS-style compliance table */
    .compliance-table {
        width: 100%;
        border-collapse: collapse;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
    }
    
    .compliance-table th,
    .compliance-table td {
        padding: 1rem 1.5rem;
        text-align: left;
        border-bottom: 1px solid rgba(0, 0, 0, 0.06);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .compliance-table th {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        font-weight: 600;
        color: #1d1d1f;
        font-size: 0.9rem;
    }
    
    .compliance-table td {
        color: #3c3c43;
        font-size: 0.9rem;
    }
    
    /* iOS-style buttons */
    .stButton > button {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        min-width: 120px !important;
        height: 44px !important;
        padding: 12px 24px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin-right: 12px !important;
        margin-bottom: 12px !important;
        border: none !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15) !important;
    }
    
    /* Primary button styling */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #007AFF 0%, #0051D5 100%) !important;
        color: white !important;
    }
    
    .stButton > button[kind="secondary"] {
        background: linear-gradient(135deg, #f2f2f7 0%, #e5e5ea 100%) !important;
        color: #1d1d1f !important;
    }
    
    /* Sidebar navigation buttons - iOS style */
    .stSidebar .stButton > button {
        width: 100% !important;
        min-width: 200px !important;
        height: 50px !important;
        padding: 14px 20px !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        border-radius: 12px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        margin-bottom: 8px !important;
        margin-right: 0 !important;
        text-align: left !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%) !important;
        color: #1d1d1f !important;
        border: 1px solid rgba(0, 0, 0, 0.06) !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
        transition: all 0.2s ease !important;
    }
    
    .stSidebar .stButton > button:hover {
        background: linear-gradient(135deg, #e3f2fd 0%, #f0f8ff 100%) !important;
        transform: translateX(4px) !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08) !important;
    }
    
    /* iOS-style expanders */
    .streamlit-expander {
        border: 1px solid rgba(0, 0, 0, 0.06) !important;
        border-radius: 16px !important;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04) !important;
        margin-bottom: 1rem !important;
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%) !important;
    }
    
    .streamlit-expander .streamlit-expanderHeader {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        color: #1d1d1f !important;
        padding: 1rem 1.5rem !important;
        border-radius: 16px 16px 0 0 !important;
    }
    
    .streamlit-expander .streamlit-expanderContent {
        padding: 1.5rem !important;
        border-radius: 0 0 16px 16px !important;
    }
    
    /* iOS-style tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px !important;
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%) !important;
        border-radius: 12px !important;
        padding: 4px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        padding: 8px 16px !important;
        transition: all 0.2s ease !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #007AFF 0%, #0051D5 100%) !important;
        color: white !important;
        box-shadow: 0 2px 8px rgba(0, 122, 255, 0.3) !important;
    }
    
    /* iOS-style metrics */
    .metric-container {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid rgba(0, 0, 0, 0.06);
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
        margin-bottom: 1rem;
    }
    
    /* iOS-style success/warning/error messages */
    .stSuccess {
        background: linear-gradient(135deg, #d1f2eb 0%, #a8e6cf 100%) !important;
        border: 1px solid #00a86b !important;
        border-radius: 12px !important;
        color: #00a86b !important;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fff3e0 0%, #ffcc80 100%) !important;
        border: 1px solid #ff8f00 !important;
        border-radius: 12px !important;
        color: #ff8f00 !important;
    }
    
    .stError {
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%) !important;
        border: 1px solid #d32f2f !important;
        border-radius: 12px !important;
        color: #d32f2f !important;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%) !important;
        border: 1px solid #2196f3 !important;
        border-radius: 12px !important;
        color: #1976d2 !important;
    }
    
    /* iOS-style form elements */
    .stSelectbox > div > div {
        border-radius: 12px !important;
        border: 1px solid rgba(0, 0, 0, 0.1) !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
    }
    
    .stTextInput > div > div > input {
        border-radius: 12px !important;
        border: 1px solid rgba(0, 0, 0, 0.1) !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }
    
    .stTextArea > div > div > textarea {
        border-radius: 12px !important;
        border: 1px solid rgba(0, 0, 0, 0.1) !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }
    
    /* iOS-style plotly charts */
    .js-plotly-plot {
        border-radius: 16px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08) !important;
        overflow: hidden !important;
    }
    
    /* iOS-style sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%) !important;
        border-right: 1px solid rgba(0, 0, 0, 0.06) !important;
    }
    
    /* iOS-style main content area */
    .main .block-container {
        background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%) !important;
    }
    
    /* Ensure form submit buttons are also equal size */
    .stForm > div > div > button {
        min-width: 120px !important;
        height: 44px !important;
        padding: 12px 24px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin-right: 12px !important;
        margin-bottom: 12px !important;
        border: none !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
    }
</style>
""", unsafe_allow_html=True)

# Sample data
@st.cache_data(ttl=300)  # Cache for 5 minutes
def generate_escalation_data(agent):
    """Generate comprehensive escalation data for an agent based on 100+ iterations"""
    
    # Base escalation data by agent type
    escalation_templates = {
        'orchestration': {
            'total_escalations': 47,
            'avg_resolution_time': '8.5m',
            'success_rate': 89,
            'critical_issues': 3,
            'daily_avg': 1.6,
            'pattern_analysis': {
                'Workflow Timeout': 35,
                'Dependency Failure': 28,
                'Resource Exhaustion': 20,
                'Validation Error': 12,
                'Business Rule Violation': 5
            },
            'patterns_identified': [
                {'pattern': 'Peak Load Escalations', 'description': 'Escalations spike during 2-4 PM business hours', 'frequency': 68},
                {'pattern': 'Cascade Failures', 'description': 'Single service failure triggers multiple escalations', 'frequency': 42},
                {'pattern': 'Resource Contention', 'description': 'Memory issues during high-volume processing', 'frequency': 31}
            ],
            'resolution_strategies': [
                {'strategy': 'Auto-retry with exponential backoff', 'effectiveness': 78},
                {'strategy': 'Circuit breaker pattern', 'effectiveness': 85},
                {'strategy': 'Resource scaling', 'effectiveness': 92}
            ],
            'prevention_measures': [
                'Implement proactive resource monitoring',
                'Add circuit breakers for external dependencies',
                'Optimize workflow execution paths',
                'Increase timeout thresholds during peak hours'
            ],
            'performance_improvements': [
                {'area': 'Workflow Optimization', 'improvement': '25% faster execution', 'impact': 'Reduced timeout escalations by 40%'},
                {'area': 'Resource Management', 'improvement': '30% better memory utilization', 'impact': 'Eliminated resource exhaustion escalations'},
                {'area': 'Error Handling', 'improvement': '50% better error recovery', 'impact': 'Improved success rate from 78% to 89%'}
            ]
        },
        'retrieval': {
            'total_escalations': 23,
            'avg_resolution_time': '4.2m',
            'success_rate': 94,
            'critical_issues': 1,
            'daily_avg': 0.8,
            'pattern_analysis': {
                'Query Timeout': 40,
                'Vector DB Error': 25,
                'No Results Found': 20,
                'Classification Error': 10,
                'Permission Denied': 5
            },
            'patterns_identified': [
                {'pattern': 'Complex Query Escalations', 'description': 'Multi-vector searches cause timeouts', 'frequency': 52},
                {'pattern': 'Index Performance', 'description': 'Vector index degradation during peak usage', 'frequency': 38},
                {'pattern': 'Classification Confidence', 'description': 'Low confidence classifications trigger escalations', 'frequency': 29}
            ],
            'resolution_strategies': [
                {'strategy': 'Query optimization and caching', 'effectiveness': 88},
                {'strategy': 'Index maintenance automation', 'effectiveness': 91},
                {'strategy': 'Confidence threshold adjustment', 'effectiveness': 76}
            ],
            'prevention_measures': [
                'Implement query result caching',
                'Schedule regular index maintenance',
                'Add query complexity analysis',
                'Optimize vector similarity calculations'
            ],
            'performance_improvements': [
                {'area': 'Query Performance', 'improvement': '60% faster queries', 'impact': 'Reduced timeout escalations by 70%'},
                {'area': 'Index Optimization', 'improvement': '40% better search accuracy', 'impact': 'Improved result relevance by 35%'},
                {'area': 'Caching Strategy', 'improvement': '80% cache hit rate', 'impact': 'Reduced database load by 50%'}
            ]
        },
        'monitoring': {
            'total_escalations': 31,
            'avg_resolution_time': '6.8m',
            'success_rate': 87,
            'critical_issues': 2,
            'daily_avg': 1.1,
            'pattern_analysis': {
                'Threshold Breach': 35,
                'Anomaly Detection': 30,
                'Compliance Violation': 20,
                'System Health': 10,
                'Data Quality': 5
            },
            'patterns_identified': [
                {'pattern': 'False Positive Anomalies', 'description': 'Normal business patterns flagged as anomalies', 'frequency': 45},
                {'pattern': 'Threshold Sensitivity', 'description': 'Overly sensitive thresholds trigger unnecessary escalations', 'frequency': 38},
                {'pattern': 'Data Quality Issues', 'description': 'Poor input data quality causes monitoring failures', 'frequency': 32}
            ],
            'resolution_strategies': [
                {'strategy': 'Adaptive threshold adjustment', 'effectiveness': 82},
                {'strategy': 'Machine learning anomaly detection', 'effectiveness': 89},
                {'strategy': 'Data quality validation', 'effectiveness': 85}
            ],
            'prevention_measures': [
                'Implement adaptive threshold algorithms',
                'Add data quality pre-processing',
                'Use ML-based anomaly detection',
                'Create business context-aware monitoring'
            ],
            'performance_improvements': [
                {'area': 'Anomaly Detection', 'improvement': '45% fewer false positives', 'impact': 'Reduced unnecessary escalations by 60%'},
                {'area': 'Threshold Management', 'improvement': 'Dynamic threshold adjustment', 'impact': 'Improved accuracy by 35%'},
                {'area': 'Data Quality', 'improvement': '90% data validation success', 'impact': 'Eliminated data quality escalations'}
            ]
        }
    }
    
    # Get template for agent type or use default
    template = escalation_templates.get(agent['patternType'], escalation_templates['orchestration'])
    
    # Generate recent events
    recent_events = [
        {
            'timestamp': '2025-01-20 14:32:15',
            'type': 'Workflow Timeout',
            'severity': 'High',
            'status': 'Resolved',
            'description': 'Payment processing workflow exceeded 30-second timeout limit during peak hours',
            'impact': '15 pending payments delayed, customer complaints received',
            'resolution': 'Implemented circuit breaker pattern and increased timeout to 45 seconds',
            'duration': '12 minutes',
            'lessons_learned': 'Peak hour load requires dynamic timeout adjustment'
        },
        {
            'timestamp': '2025-01-20 14:28:42',
            'type': 'Dependency Failure',
            'severity': 'Medium',
            'status': 'Investigating',
            'description': 'External banking API returned 503 error, affecting payment validation',
            'impact': 'Payment validation temporarily unavailable',
            'resolution': 'Switched to backup API endpoint, investigating root cause',
            'duration': 'Ongoing',
            'lessons_learned': 'Need better fallback mechanisms for critical dependencies'
        },
        {
            'timestamp': '2025-01-20 14:25:18',
            'type': 'Validation Error',
            'severity': 'Low',
            'status': 'Resolved',
            'description': 'Input data failed schema validation due to missing required field',
            'impact': 'Single transaction rejected, no customer impact',
            'resolution': 'Updated validation rules to handle optional fields gracefully',
            'duration': '3 minutes',
            'lessons_learned': 'Schema validation needs to be more flexible for edge cases'
        }
    ]
    
    # Generate critical issues
    critical_issues_list = [
        {
            'title': 'Peak Hour Performance Degradation',
            'root_cause': 'Insufficient resource allocation during 2-4 PM business hours',
            'business_impact': 'Customer satisfaction decreased by 15% due to processing delays',
            'recommended_actions': [
                'Implement auto-scaling based on load patterns',
                'Add resource monitoring and alerting',
                'Optimize database queries for peak usage',
                'Consider load balancing across multiple instances'
            ],
            'priority': 'High'
        },
        {
            'title': 'External API Dependency Risk',
            'root_cause': 'Single point of failure in banking API integration',
            'business_impact': 'Complete payment processing halt when API is unavailable',
            'recommended_actions': [
                'Implement multiple API provider fallbacks',
                'Add circuit breaker pattern with graceful degradation',
                'Create cached responses for common queries',
                'Establish SLA monitoring with providers'
            ],
            'priority': 'High'
        }
    ]
    
    # Generate action items
    action_items = [
        {
            'title': 'Implement Auto-scaling for Peak Hours',
            'description': 'Configure Kubernetes HPA to scale resources during 2-4 PM',
            'priority': 'High',
            'due_date': '2025-01-25'
        },
        {
            'title': 'Add Circuit Breaker Pattern',
            'description': 'Implement circuit breaker for external API calls to prevent cascade failures',
            'priority': 'High',
            'due_date': '2025-01-30'
        },
        {
            'title': 'Optimize Database Queries',
            'description': 'Review and optimize slow queries identified during peak hours',
            'priority': 'Medium',
            'due_date': '2025-02-05'
        }
    ]
    
    # Generate thresholds
    thresholds = [
        {'metric': 'Response Time', 'value': '30s', 'status': 'Active'},
        {'metric': 'Error Rate', 'value': '5%', 'status': 'Active'},
        {'metric': 'Memory Usage', 'value': '80%', 'status': 'Active'},
        {'metric': 'CPU Usage', 'value': '85%', 'status': 'Active'}
    ]
    
    # Generate escalation rules
    escalation_rules = [
        'Escalate to Level 2 if resolution time exceeds 5 minutes',
        'Immediate escalation for any Critical severity issues',
        'Auto-retry up to 3 times before escalation',
        'Notify stakeholders for High severity issues within 2 minutes'
    ]
    
    return {
        **template,
        'recent_events': recent_events,
        'critical_issues_list': critical_issues_list,
        'action_items': action_items,
        'thresholds': thresholds,
        'escalation_rules': escalation_rules
    }

@st.cache_data(ttl=300)  # Cache for 5 minutes
def parse_payment_intent(instruction_text):
    """Parse payment instruction text to extract structured intent"""
    import re
    
    # Default values
    intent = {
        'amount': 'Not specified',
        'beneficiary': 'Not specified',
        'date': 'Not specified',
        'urgency': 'Normal',
        'confidence': 0.85
    }
    
    # Extract amount (look for currency patterns) - improved to handle k/m suffixes better
    amount_patterns = [
        # Patterns with currency symbols and k/m suffixes
        r'\$[\d,]+(?:\.\d{2})?\s*(?:k|m|thousand|million)\b',
        r'\$[\d,]+(?:\.\d{2})?\s*(?:CAD|USD|EUR|GBP)',
        # Patterns without currency symbols but with k/m suffixes
        r'[\d,]+(?:\.\d{2})?\s*(?:k|m|thousand|million)\b',
        r'[\d,]+(?:\.\d{2})?\s*(?:CAD|USD|EUR|GBP)',
        # Standard currency patterns
        r'\$[\d,]+(?:\.\d{2})?',
        # Fallback for any number with k/m
        r'[\d,]+(?:\.\d{2})?\s*(?:k|m)\b',
    ]
    
    for pattern in amount_patterns:
        match = re.search(pattern, instruction_text, re.IGNORECASE)
        if match:
            amount_text = match.group(0)
            # Convert k/m suffixes to proper amounts
            if re.search(r'\bk\b', amount_text, re.IGNORECASE):
                # Extract number and multiply by 1000
                number_match = re.search(r'[\d,]+(?:\.\d{2})?', amount_text)
                if number_match:
                    number = float(number_match.group(0).replace(',', ''))
                    intent['amount'] = f"${number * 1000:,.0f}"
                else:
                    intent['amount'] = amount_text
            elif re.search(r'\bm\b', amount_text, re.IGNORECASE):
                # Extract number and multiply by 1,000,000
                number_match = re.search(r'[\d,]+(?:\.\d{2})?', amount_text)
                if number_match:
                    number = float(number_match.group(0).replace(',', ''))
                    intent['amount'] = f"${number * 1000000:,.0f}"
                else:
                    intent['amount'] = amount_text
            elif re.search(r'(?:thousand|million)', amount_text, re.IGNORECASE):
                # Handle word-based multipliers
                if 'thousand' in amount_text.lower():
                    number_match = re.search(r'[\d,]+(?:\.\d{2})?', amount_text)
                    if number_match:
                        number = float(number_match.group(0).replace(',', ''))
                        intent['amount'] = f"${number * 1000:,.0f}"
                    else:
                        intent['amount'] = amount_text
                elif 'million' in amount_text.lower():
                    number_match = re.search(r'[\d,]+(?:\.\d{2})?', amount_text)
                    if number_match:
                        number = float(number_match.group(0).replace(',', ''))
                        intent['amount'] = f"${number * 1000000:,.0f}"
                    else:
                        intent['amount'] = amount_text
            else:
                intent['amount'] = amount_text
            break
    
    # Extract beneficiary (look for vendor/supplier names)
    beneficiary_patterns = [
        r'(?:to|pay|send|transfer)\s+([A-Z][A-Za-z\s&]+?)(?:\s+by|\s+for|\s+urgently|\s+immediately|$)',
        r'(?:vendor|supplier|contractor|partner)\s+([A-Z][A-Za-z\s&]+?)(?:\s+by|\s+for|\s+urgently|\s+immediately|$)',
        r'([A-Z][A-Za-z\s&]+?)(?:\s+by|\s+for|\s+urgently|\s+immediately)',
    ]
    
    for pattern in beneficiary_patterns:
        match = re.search(pattern, instruction_text, re.IGNORECASE)
        if match:
            intent['beneficiary'] = match.group(1).strip()
            break
    
    # Extract date/time
    date_patterns = [
        r'(?:by|before|until)\s+(friday|monday|tuesday|wednesday|thursday|saturday|sunday)',
        r'(?:by|before|until)\s+(end\s+of\s+month|next\s+week|tomorrow|today)',
        r'(?:by|before|until)\s+(\d{1,2}/\d{1,2}/\d{2,4})',
        r'(?:by|before|until)\s+(\d{1,2}-\d{1,2}-\d{2,4})',
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, instruction_text, re.IGNORECASE)
        if match:
            intent['date'] = match.group(1).strip()
            break
    
    # Determine urgency
    urgency_keywords = {
        'urgent': ['urgent', 'urgently', 'asap', 'immediately', 'right away'],
        'high': ['high priority', 'important', 'critical', 'expedite'],
        'normal': ['normal', 'regular', 'standard']
    }
    
    text_lower = instruction_text.lower()
    for urgency, keywords in urgency_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            intent['urgency'] = urgency.title()
            break
    
    # Calculate confidence based on extracted fields
    confidence = 0.5
    if intent['amount'] != 'Not specified':
        confidence += 0.2
    if intent['beneficiary'] != 'Not specified':
        confidence += 0.2
    if intent['date'] != 'Not specified':
        confidence += 0.1
    
    intent['confidence'] = min(confidence, 0.95)
    
    return intent

@st.cache_data(ttl=1800)  # Cache for 30 minutes
def generate_codified_policies(agent):
    """Generate codified policies in YAML and JSON format for runtime observation"""
    
    # Extract policies from governance hooks
    policies_text = agent['governanceHooks']['policies']
    
    # Parse policies into structured format
    policy_lines = [line.strip() for line in policies_text.split('\n') if line.strip() and not line.strip().startswith('policies:')]
    
    # Generate structured policy data
    policy_data = {
        'agent_id': agent['id'],
        'agent_name': agent['name'],
        'version': '1.0.0',
        'last_updated': '2025-01-24T10:00:00Z',
        'policies': {
            'governance': {
                'compliance_tags': agent['governanceHooks']['complianceTags'],
                'approval_history': agent['governanceHooks']['approvalHistory'],
                'audit_logs': agent['governanceHooks']['auditLogs']
            },
            'runtime_guardrails': {
                'input_filters': agent['runtimeGuardrails']['inputFilters'],
                'output_validators': agent['runtimeGuardrails']['outputValidators'],
                'rate_controls': agent['runtimeGuardrails']['rateControls'],
                'scope_controls': agent['runtimeGuardrails']['scopeControls'],
                'kill_switch': agent['runtimeGuardrails']['killSwitch']
            },
            'escalation_mechanisms': {
                'tiered_escalation': agent['escalationMechanisms']['tieredEscalation'],
                'notification_channels': agent['escalationMechanisms']['notificationChannels'],
                'decision_journals': agent['escalationMechanisms']['decisionJournals']
            },
            'business_rules': policy_lines
        },
        'monitoring': {
            'calls_this_week': agent['monitoring']['callsThisWeek'],
            'guardrail_triggers': agent['monitoring']['guardrailTriggers'],
            'escalations': agent['monitoring']['escalations'],
            'uptime': agent['monitoring']['uptime'],
            'avg_response_time': agent['monitoring']['avgResponseTime']
        }
    }
    
    # Generate YAML
    yaml_content = f"""# Agent Policy Configuration
# Agent: {agent['name']} ({agent['id']})
# Generated: {policy_data['last_updated']}

agent:
  id: {agent['id']}
  name: {agent['name']}
  version: {policy_data['version']}
  lifecycle: {agent['lifecycle']}
  owner: {agent['owner']}

governance:
  compliance_tags:
{chr(10).join([f"    {tag}: {status}" for tag, status in agent['governanceHooks']['complianceTags'].items()])}
  approval_history: {agent['governanceHooks']['approvalHistory']}
  audit_logs:
    entries: {agent['governanceHooks']['auditLogs']['entries']}
    last_escalation: {agent['governanceHooks']['auditLogs']['lastEscalation']}

runtime_guardrails:
  input_filters:
{chr(10).join([f"    - {filter_type}" for filter_type in agent['runtimeGuardrails']['inputFilters']])}
  output_validators:
{chr(10).join([f"    - {validator}" for validator in agent['runtimeGuardrails']['outputValidators']])}
  rate_controls:
{chr(10).join([f"    {control}: {value}" for control, value in agent['runtimeGuardrails']['rateControls'].items()])}
  scope_controls:
{chr(10).join([f"    {scope}: {value}" for scope, value in agent['runtimeGuardrails']['scopeControls'].items()])}
  kill_switch:
    enabled: {agent['runtimeGuardrails']['killSwitch']['enabled']}
    triggers:
{chr(10).join([f"      - {trigger}" for trigger in agent['runtimeGuardrails']['killSwitch']['triggers']])}

escalation_mechanisms:
  tiered_escalation:
{chr(10).join([f"    - level: {level['level']}\n      action: {level['action']}\n      status: {level['status']}\n      timeout: {level['timeout']}" for level in agent['escalationMechanisms']['tieredEscalation']])}
  notification_channels:
{chr(10).join([f"    - {channel}" for channel in agent['escalationMechanisms']['notificationChannels']])}
  decision_journals:
    enabled: {agent['escalationMechanisms']['decisionJournals']['enabled']}
    required: {agent['escalationMechanisms']['decisionJournals']['required']}
    template: {agent['escalationMechanisms']['decisionJournals']['template']}

business_rules:
{chr(10).join([f"  - {rule}" for rule in policy_lines])}

monitoring:
  calls_this_week: {agent['monitoring']['callsThisWeek']}
  guardrail_triggers: {agent['monitoring']['guardrailTriggers']}
  escalations: {agent['monitoring']['escalations']}
  uptime: {agent['monitoring']['uptime']}
  avg_response_time: {agent['monitoring']['avgResponseTime']}
"""
    
    # Generate JSON
    json_content = json.dumps(policy_data, indent=2)
    
    # Generate runtime observation data
    compliance_rate = max(85, 100 - (agent['monitoring']['guardrailTriggers'] * 2))
    compliance_trend = np.random.choice([-2, -1, 0, 1, 2])
    active_policies = len(policy_lines) + len(agent['runtimeGuardrails']['inputFilters']) + len(agent['runtimeGuardrails']['outputValidators'])
    violations_24h = max(0, agent['monitoring']['guardrailTriggers'] - np.random.randint(0, 3))
    
    # Generate execution log
    execution_log = []
    for i in range(5):
        policies = ['Input Validation', 'Output Compliance', 'Rate Limiting', 'Scope Control', 'Kill Switch']
        statuses = ['compliant', 'warning', 'violation']
        status = np.random.choice(statuses, p=[0.7, 0.2, 0.1])
        execution_log.append({
            'policy': np.random.choice(policies),
            'timestamp': f"2025-01-24 {np.random.randint(8, 18):02d}:{np.random.randint(0, 60):02d}:{np.random.randint(0, 60):02d}",
            'status': status,
            'details': f"Policy executed with {status} status" if status != 'compliant' else None
        })
    
    # Generate validation results
    validation_results = []
    for policy in ['Input Filters', 'Output Validators', 'Rate Controls', 'Scope Controls', 'Kill Switch']:
        valid = np.random.choice([True, False], p=[0.8, 0.2])
        validation_results.append({
            'policy_name': policy,
            'valid': valid,
            'message': 'Policy configuration is valid' if valid else 'Policy configuration needs attention'
        })
    
    return {
        'yaml': yaml_content,
        'json': json_content,
        'compliance_rate': compliance_rate,
        'compliance_trend': compliance_trend,
        'active_policies': active_policies,
        'violations_24h': violations_24h,
        'execution_log': execution_log,
        'validation_results': validation_results
    }

@st.cache_data(ttl=600)  # Cache for 10 minutes
def load_agent_data():
    return {
        'agents': [
            {
                'id': 'retriever-v1',
                'name': 'Retriever Agent v1',
                'patternType': 'retrieval',
                'patternName': 'Retriever-Augmented Agent',
                'status': 'approved',
                'useCase': 'Ops Doc Routing',
                'risk': 'Medium',
                'businessUseCase': 'Ops document classification & routing',
                'capabilities': [
                    'Document classification',
                    'Content extraction',
                    'Metadata tagging',
                    'Route determination'
                ],
                'boundaries': [
                    'No PII processing',
                    'Max document size: 10MB',
                    'No external API calls',
                    'Read-only operations'
                ],
                'dependencies': {
                    'vectorDB': 'Pinecone',
                    'llm': 'Azure OpenAI GPT-4',
                    'embeddings': 'text-embedding-ada-002',
                    'storage': 'Azure Blob Storage'
                },
                'owner': 'Ops AI Team',
                'lifecycle': 'Approved',
                'governanceHooks': {
                    'policies': """policies:
  - no PII storage
  - must log classification rationale
  - max processing time: 30 seconds
  - escalation required for high-risk documents
  - audit trail mandatory for all decisions""",
                    'auditLogs': {'entries': 12, 'lastEscalation': 'Sept 20, 2025'},
                    'complianceTags': {'GDPR': True, 'OSFI': True, 'FINTRAC': False, 'SOC2': True},
                    'approvalHistory': ['Submitted', 'Reviewed', 'Approved']
                },
                'runtimeGuardrails': {
                    'inputFilters': ['PII detection', 'Content sanitization', 'Size validation'],
                    'outputValidators': ['Hallucination check', 'Bias detection', 'Policy compliance'],
                    'rateControls': {'maxCallsPerMinute': 100, 'maxTokensPerCall': 2000},
                    'scopeControls': {'allowedDomains': ['internal.ops.com'], 'blockedContent': ['PII', 'financial_data']},
                    'killSwitch': {'enabled': True, 'triggers': ['error_rate > 5%', 'response_time > 30s']}
                },
                'escalationMechanisms': {
                    'tieredEscalation': [
                        {'level': 1, 'action': 'Auto-retry with stricter constraints', 'status': 'success', 'timeout': '30s'},
                        {'level': 2, 'action': 'Route to Ops Supervisor Agent', 'status': 'pending', 'timeout': '2m'},
                        {'level': 3, 'action': 'Human operator with full context', 'status': 'not-triggered', 'timeout': '5m'}
                    ],
                    'notificationChannels': ['Slack', 'Teams', 'ServiceNow'],
                    'decisionJournals': {'enabled': True, 'required': True, 'template': 'escalation_reasoning'}
                },
                'monitoring': {'callsThisWeek': 1245, 'guardrailTriggers': 3, 'escalations': 1, 'avgResponseTime': '245ms', 'uptime': '99.8%'},
                'runtime_tools': {
                    'llm_tools': [
                        {'name': 'Azure OpenAI GPT-4', 'purpose': 'Document analysis and classification', 'status': 'active'},
                        {'name': 'text-embedding-ada-002', 'purpose': 'Semantic vector generation', 'status': 'active'}
                    ],
                    'vector_tools': [
                        {'name': 'Pinecone Vector DB', 'purpose': 'Document similarity search', 'status': 'active'},
                        {'name': 'Azure Cognitive Search', 'purpose': 'Hybrid search capabilities', 'status': 'active'}
                    ],
                    'storage_tools': [
                        {'name': 'Azure Blob Storage', 'purpose': 'Document storage and retrieval', 'status': 'active'},
                        {'name': 'Azure Cosmos DB', 'purpose': 'Metadata and classification results', 'status': 'active'}
                    ],
                    'api_tools': [
                        {'name': 'Document Processing API', 'purpose': 'PDF parsing and text extraction', 'status': 'active'},
                        {'name': 'Classification API', 'purpose': 'Document type classification', 'status': 'active'}
                    ],
                    'governance_tools': [
                        {'name': 'Azure AI Content Safety', 'purpose': 'Content filtering and safety checks', 'status': 'active'},
                        {'name': 'Audit Logger', 'purpose': 'Compliance and decision logging', 'status': 'active'}
                    ]
                },
                'patternImplementations': {
                    'primary_patterns': ['Tool Use', 'Memory & Learning'],
                    'secondary_patterns': ['Reflection', 'Critic/Reviewer'],
                    'pattern_details': {
                        'Tool Use': {
                            'implementation': 'Uses vector database and embedding APIs for document retrieval',
                            'tools_used': ['Pinecone Vector DB', 'Azure OpenAI Embeddings', 'Azure Blob Storage'],
                            'configuration': {
                                'max_retry_attempts': 3,
                                'tool_whitelist_required': True,
                                'input_validation': True,
                                'output_sanitization': True
                            }
                        },
                        'Memory & Learning': {
                            'implementation': 'Learns from document classification patterns and improves routing accuracy',
                            'memory_type': 'Long-term pattern recognition',
                            'learning_mechanism': 'Feedback loop from classification accuracy',
                            'configuration': {
                                'short_term_memory_ttl': 3600,
                                'long_term_memory_summary_threshold': 30,
                                'memory_inspection_enabled': True
                            }
                        },
                        'Reflection': {
                            'implementation': 'Self-evaluates classification confidence and accuracy before routing',
                            'reflection_criteria': ['accuracy', 'confidence', 'compliance'],
                            'max_reflection_loops': 2,
                            'configuration': {
                                'reflection_notes_required': True,
                                'audit_logging': True,
                                'timeout_seconds': 30
                            }
                        },
                        'Critic/Reviewer \U0001F9D0': {
                            'implementation': 'Secondary validation of high-risk document classifications',
                            'critic_role': 'Quality assurance for document routing decisions',
                            'decision_authority': 'Primary agent with critic override',
                            'configuration': {
                                'evaluation_rubric_required': True,
                                'critic_output_tags': ['approve', 'revise', 'reject'],
                                'critique_traceability': True
                            }
                        }
                    }
                }
            },
            {
                'id': 'orchestrator-v2',
                'name': 'Orchestrator Agent v2',
                'patternType': 'orchestration',
                'patternName': 'Workflow Orchestrator Agent',
                'status': 'pilot',
                'useCase': 'Workflow Automation',
                'risk': 'High',
                'businessUseCase': 'Complex workflow orchestration and task management',
                'capabilities': [
                    'Multi-step workflow execution',
                    'Task coordination',
                    'Error handling and recovery',
                    'Resource management'
                ],
                'boundaries': [
                    'Max workflow duration: 5 minutes',
                    'No direct database writes',
                    'Limited to approved APIs',
                    'No external service calls'
                ],
                'dependencies': {
                    'workflowEngine': 'Temporal',
                    'messageQueue': 'RabbitMQ',
                    'database': 'PostgreSQL',
                    'monitoring': 'Prometheus'
                },
                'owner': 'Workflow Team',
                'lifecycle': 'Pilot',
                'governanceHooks': {
                    'policies': """policies:
  - workflow timeout: 5 minutes
  - must maintain audit trail
  - rollback capability required
  - all state changes must be logged""",
                    'auditLogs': {'entries': 8, 'lastEscalation': 'Sept 18, 2025'},
                    'complianceTags': {'GDPR': True, 'OSFI': False, 'FINTRAC': False, 'SOC2': True},
                    'approvalHistory': ['Submitted', 'Under Review']
                },
                'runtimeGuardrails': {
                    'inputFilters': ['Workflow validation', 'Resource limits', 'Permission checks'],
                    'outputValidators': ['State consistency', 'Output validation', 'Error handling'],
                    'rateControls': {'maxWorkflowsPerHour': 50, 'maxConcurrentWorkflows': 10},
                    'scopeControls': {'allowedWorkflows': ['ops_automation', 'data_processing'], 'blockedOperations': ['financial_transactions']},
                    'killSwitch': {'enabled': True, 'triggers': ['workflow_failure_rate > 10%', 'resource_usage > 80%']}
                },
                'escalationMechanisms': {
                    'tieredEscalation': [
                        {'level': 1, 'action': 'Retry with exponential backoff', 'status': 'success', 'timeout': '1m'},
                        {'level': 2, 'action': 'Escalate to Workflow Manager', 'status': 'pending', 'timeout': '3m'},
                        {'level': 3, 'action': 'Manual intervention required', 'status': 'not-triggered', 'timeout': '5m'}
                    ],
                    'notificationChannels': ['Slack', 'Email', 'PagerDuty'],
                    'decisionJournals': {'enabled': True, 'required': True, 'template': 'workflow_escalation'}
                },
                'monitoring': {'callsThisWeek': 892, 'guardrailTriggers': 5, 'escalations': 2, 'avgResponseTime': '1.2s', 'uptime': '98.5%'},
                'runtime_tools': {
                    'llm_tools': [
                        {'name': 'Azure OpenAI GPT-4', 'purpose': 'Workflow planning and orchestration', 'status': 'active'},
                        {'name': 'Claude-3-Sonnet', 'purpose': 'Complex reasoning and decision making', 'status': 'active'}
                    ],
                    'workflow_tools': [
                        {'name': 'Temporal Workflow Engine', 'purpose': 'Distributed workflow orchestration', 'status': 'active'},
                        {'name': 'Apache Airflow', 'purpose': 'Data pipeline orchestration', 'status': 'active'}
                    ],
                    'messaging_tools': [
                        {'name': 'RabbitMQ', 'purpose': 'Inter-agent communication', 'status': 'active'},
                        {'name': 'Apache Kafka', 'purpose': 'Event streaming and processing', 'status': 'active'}
                    ],
                    'database_tools': [
                        {'name': 'PostgreSQL', 'purpose': 'Workflow state and metadata storage', 'status': 'active'},
                        {'name': 'Redis', 'purpose': 'Caching and session management', 'status': 'active'}
                    ],
                    'monitoring_tools': [
                        {'name': 'Prometheus', 'purpose': 'Metrics collection and alerting', 'status': 'active'},
                        {'name': 'Grafana', 'purpose': 'Visualization and dashboards', 'status': 'active'}
                    ]
                },
                'patternImplementations': {
                    'primary_patterns': ['Orchestration', 'Planning'],
                    'secondary_patterns': ['Tool Use', 'Collaboration / Delegation', 'Exploration / Simulation'],
                    'pattern_details': {
                        'Orchestration': {
                            'implementation': 'Meta-agent coordinating multiple workflow steps and task management',
                            'coordination_scope': 'End-to-end workflow execution',
                            'global_state_management': True,
                            'configuration': {
                                'global_state_required': True,
                                'task_registry_enabled': True,
                                'escalation_policy': 'retry_fallback_human',
                                'modular_components': True
                            }
                        },
                        'Planning': {
                            'implementation': 'Breaks down complex workflows into executable sub-tasks',
                            'planning_depth': 'Multi-level task decomposition',
                            'plan_format': 'JSON workflow definitions',
                            'configuration': {
                                'max_plan_depth': 5,
                                'plan_format': 'json',
                                'required_fields': ['task_id', 'description', 'dependencies', 'success_criteria'],
                                'replan_on_failure': True
                            }
                        },
                        'Tool Use': {
                            'implementation': 'Integrates with workflow engine, message queue, and monitoring systems',
                            'tools_used': ['Temporal Workflow Engine', 'RabbitMQ', 'PostgreSQL', 'Prometheus'],
                            'configuration': {
                                'max_retry_attempts': 3,
                                'tool_whitelist_required': True,
                                'input_validation': True,
                                'rate_limiting': True
                            }
                        },
                        'Collaboration / Delegation': {
                            'implementation': 'Coordinates with specialized agents for different workflow steps',
                            'delegation_protocol': 'Structured handoff with context preservation',
                            'conflict_resolution': 'Workflow state arbitration',
                            'configuration': {
                                'role_declaration_required': True,
                                'handoff_packet_format': 'json',
                                'conflict_resolution': 'workflow_state_arbitration',
                                'circular_delegation_check': True
                            }
                        },
                        'Exploration / Simulation': {
                            'implementation': 'Simulates workflow execution paths before committing to execution',
                            'scenario_testing': 'Workflow path validation and optimization',
                            'configuration': {
                                'max_scenarios': 5,
                                'scenario_ranking_required': True,
                                'top_scenarios_retained': 2,
                                'assumption_documentation': True
                            }
                        }
                    }
                }
            },
            {
                'id': 'compliance-v1',
                'name': 'Compliance Monitor v1',
                'patternType': 'monitoring',
                'patternName': 'Compliance Monitor Agent',
                'status': 'draft',
                'useCase': 'Regulatory Checks',
                'risk': 'Low',
                'businessUseCase': 'Automated regulatory compliance monitoring',
                'capabilities': [
                    'Real-time compliance checking',
                    'Violation detection',
                    'Alert generation',
                    'Report generation'
                ],
                'boundaries': [
                    'Read-only access to systems',
                    'No data modification',
                    'Limited to approved data sources',
                    'No external communications'
                ],
                'dependencies': {
                    'complianceDB': 'Compliance Database',
                    'ruleEngine': 'Drools Rule Engine',
                    'alertSystem': 'PagerDuty',
                    'reporting': 'Tableau'
                },
                'owner': 'Compliance Team',
                'lifecycle': 'Draft',
                'governanceHooks': {
                    'policies': """policies:
  - daily compliance checks
  - immediate alert on violations
  - comprehensive logging required
  - all findings must be documented""",
                    'auditLogs': {'entries': 0, 'lastEscalation': 'N/A'},
                    'complianceTags': {'GDPR': True, 'OSFI': True, 'FINTRAC': True, 'SOC2': True, 'HIPAA': False},
                    'approvalHistory': ['Draft']
                },
                'runtimeGuardrails': {
                    'inputFilters': ['Data source validation', 'Access permission checks'],
                    'outputValidators': ['Compliance rule validation', 'Alert accuracy check'],
                    'rateControls': {'maxChecksPerHour': 1000, 'maxAlertsPerDay': 100},
                    'scopeControls': {'allowedDataSources': ['internal_systems'], 'blockedData': ['PII', 'financial_data']},
                    'killSwitch': {'enabled': True, 'triggers': ['false_positive_rate > 20%', 'system_overload']}
                },
                'escalationMechanisms': {
                    'tieredEscalation': [
                        {'level': 1, 'action': 'Send compliance alert', 'status': 'not-triggered', 'timeout': '1m'},
                        {'level': 2, 'action': 'Notify compliance officer', 'status': 'not-triggered', 'timeout': '5m'},
                        {'level': 3, 'action': 'Escalate to legal team', 'status': 'not-triggered', 'timeout': '15m'}
                    ],
                    'notificationChannels': ['Email', 'Teams', 'Slack'],
                    'decisionJournals': {'enabled': True, 'required': True, 'template': 'compliance_finding'}
                },
                'monitoring': {'callsThisWeek': 0, 'guardrailTriggers': 0, 'escalations': 0, 'avgResponseTime': 'N/A', 'uptime': 'N/A'},
                'runtime_tools': {
                    'llm_tools': [
                        {'name': 'Azure OpenAI GPT-4', 'purpose': 'Policy analysis and compliance checking', 'status': 'active'},
                        {'name': 'text-embedding-ada-002', 'purpose': 'Document similarity for compliance matching', 'status': 'active'}
                    ],
                    'compliance_tools': [
                        {'name': 'RegTech API', 'purpose': 'Regulatory requirement checking', 'status': 'active'},
                        {'name': 'Compliance Database', 'purpose': 'Policy and regulation storage', 'status': 'active'}
                    ],
                    'document_tools': [
                        {'name': 'Azure Form Recognizer', 'purpose': 'Document structure analysis', 'status': 'active'},
                        {'name': 'PDF Parser API', 'purpose': 'Document content extraction', 'status': 'active'}
                    ],
                    'audit_tools': [
                        {'name': 'Audit Logger', 'purpose': 'Compliance decision logging', 'status': 'active'},
                        {'name': 'Report Generator', 'purpose': 'Compliance report creation', 'status': 'active'}
                    ],
                    'governance_tools': [
                        {'name': 'Policy Engine', 'purpose': 'Rule-based compliance validation', 'status': 'active'},
                        {'name': 'Risk Assessment API', 'purpose': 'Compliance risk scoring', 'status': 'active'}
                    ]
                },
                'patternImplementations': {
                    'primary_patterns': ['Tool Use', 'Critic/Reviewer'],
                    'secondary_patterns': ['Memory & Learning', 'Reflection'],
                    'pattern_details': {
                        'Tool Use': {
                            'implementation': 'Integrates with compliance APIs and regulatory databases',
                            'tools_used': ['Compliance API', 'Regulatory Database', 'Audit Logging System'],
                            'configuration': {
                                'max_retry_attempts': 3,
                                'tool_whitelist_required': True,
                                'input_validation': True,
                                'output_sanitization': True
                            }
                        },
                        'Critic/Reviewer \U0001F9D0': {
                            'implementation': 'Reviews and validates compliance findings before reporting',
                            'critic_role': 'Compliance validation and quality assurance',
                            'decision_authority': 'Primary agent with compliance override',
                            'configuration': {
                                'evaluation_rubric_required': True,
                                'critic_output_tags': ['compliant', 'non_compliant', 'requires_review'],
                                'critique_traceability': True
                            }
                        },
                        'Memory & Learning': {
                            'implementation': 'Learns from compliance patterns and regulatory updates',
                            'memory_type': 'Regulatory knowledge base',
                            'learning_mechanism': 'Pattern recognition from compliance violations',
                            'configuration': {
                                'short_term_memory_ttl': 7200,
                                'long_term_memory_summary_threshold': 50,
                                'memory_inspection_enabled': True
                            }
                        },
                        'Reflection': {
                            'implementation': 'Self-evaluates compliance findings for accuracy and completeness',
                            'reflection_criteria': ['accuracy', 'completeness', 'regulatory_alignment'],
                            'max_reflection_loops': 2,
                            'configuration': {
                                'reflection_notes_required': True,
                                'audit_logging': True,
                                'timeout_seconds': 60
                            }
                        }
                    }
                }
            },
            {
                'id': 'payment-processor-v1',
                'name': 'Payment Processor v1',
                'patternType': 'orchestration',
                'patternName': 'Multi-step Orchestrator Agent',
                'status': 'approved',
                'useCase': 'High-Value Payment Processing',
                'risk': 'High',
                'businessUseCase': 'High-value payment execution with anomaly detection',
                'capabilities': [
                    'Parse natural language payment instructions',
                    'Detect anomalies in payment patterns',
                    'Verify source and destination accounts',
                    'Summarize scenario for human review',
                    'Execute payment via APIs'
                ],
                'boundaries': [
                    'Max payment amount: $5M CAD',
                    'Human approval required for > $100K',
                    'No direct bank account access',
                    'Limited to approved payment methods',
                    'Must maintain dual-factor confirmation for high-value payments'
                ],
                'dependencies': {
                    'llm': 'Azure OpenAI GPT-4',
                    'anomalyModel': 'RBC_Payment_Pattern_Model_v2',
                    'complianceAPI': 'Sanctions/KYC Service',
                    'paymentAPI': 'Core Banking Payment Gateway'
                },
                'owner': 'Treasury Operations',
                'lifecycle': 'Approved',
                'governanceHooks': {
                    'policies': """policies:
  - must require human approval for > $100K
  - must log anomaly score and decision rationale
  - must block sanctioned accounts
  - must validate source and destination accounts
  - must maintain audit trail for all decisions
  - must comply with AML regulations
  - must enable dual-factor confirmation for high-value payments
  - must enforce schema validation on all inputs""",
                    'auditLogs': {'entries': 156, 'lastEscalation': 'Sept 22, 2025'},
                    'complianceTags': {'GDPR': True, 'OSFI': True, 'FINTRAC': True, 'AML': True, 'Sanctions': True, 'SOC2': True},
                    'approvalHistory': ['Submitted', 'Reviewed', 'Approved']
                },
                'runtimeGuardrails': {
                    'inputFilters': [
                        'Dual factor confirmation (for > $100K)',
                        'Schema validation',
                        'PII detection',
                        'Amount validation',
                        'Account format check',
                        'Currency validation'
                    ],
                    'outputValidators': [
                        'Rationale logging',
                        'Confidence threshold (0.8)',
                        'Anomaly score validation',
                        'Compliance check',
                        'Amount limits',
                        'Account verification'
                    ],
                    'rateControls': {
                        'maxPaymentsPerHour': 10,
                        'maxAmountPerDay': 50000000,
                        'maxAmount': '5M CAD'
                    },
                    'scopeControls': {
                        'allowedCurrencies': ['CAD', 'USD'],
                        'blockedCountries': ['sanctioned_countries'],
                        'anomalyThreshold': 0.65
                    },
                    'killSwitch': {
                        'enabled': True,
                        'triggers': [
                            'anomaly_score > 0.9',
                            'failed_verifications > 3',
                            'system_error_rate > 5%',
                            'confidence_threshold < 0.8'
                        ]
                    }
                },
                'escalationMechanisms': {
                    'tieredEscalation': [
                        {
                            'level': 1,
                            'action': 'Auto-retry parsing with stricter schema',
                            'status': 'success',
                            'timeout': '30s'
                        },
                        {
                            'level': 2,
                            'action': 'Escalate to payment_supervisor_agent',
                            'status': 'pending',
                            'timeout': '2m'
                        },
                        {
                            'level': 3,
                            'action': 'Notify human reviewer (Treasury Ops)',
                            'status': 'not-triggered',
                            'timeout': '5m'
                        }
                    ],
                    'notificationChannels': ['Slack', 'Teams', 'Email', 'PagerDuty'],
                    'decisionJournals': {'enabled': True, 'required': True, 'template': 'payment_decision'}
                },
                'monitoring': {'callsThisWeek': 23, 'guardrailTriggers': 7, 'escalations': 3, 'avgResponseTime': '3.2s', 'uptime': '99.9%'},
                'runtime_tools': {
                    'llm_tools': [
                        {'name': 'Azure OpenAI GPT-4', 'purpose': 'Payment analysis and decision making', 'status': 'active'},
                        {'name': 'Claude-3-Sonnet', 'purpose': 'Complex financial reasoning', 'status': 'active'}
                    ],
                    'payment_tools': [
                        {'name': 'Stripe API', 'purpose': 'Payment processing and validation', 'status': 'active'},
                        {'name': 'PayPal API', 'purpose': 'Alternative payment processing', 'status': 'active'}
                    ],
                    'banking_tools': [
                        {'name': 'Banking API Gateway', 'purpose': 'Bank account verification', 'status': 'active'},
                        {'name': 'ACH Processing API', 'purpose': 'Automated clearing house transactions', 'status': 'active'}
                    ],
                    'security_tools': [
                        {'name': 'Fraud Detection API', 'purpose': 'Transaction fraud analysis', 'status': 'active'},
                        {'name': 'Encryption Service', 'purpose': 'Payment data encryption', 'status': 'active'}
                    ],
                    'compliance_tools': [
                        {'name': 'PCI DSS Validator', 'purpose': 'Payment card compliance checking', 'status': 'active'},
                        {'name': 'AML Screening API', 'purpose': 'Anti-money laundering checks', 'status': 'active'}
                    ]
                },
                'patternImplementations': {
                    'primary_patterns': ['Orchestration', 'Tool Use', 'Exploration / Simulation'],
                    'secondary_patterns': ['Reflection', 'Critic/Reviewer', 'Memory & Learning'],
                    'pattern_details': {
                        'Orchestration': {
                            'implementation': 'Coordinates multi-step payment processing workflow with anomaly detection',
                            'coordination_scope': 'End-to-end payment execution pipeline',
                            'global_state_management': True,
                            'configuration': {
                                'global_state_required': True,
                                'task_registry_enabled': True,
                                'escalation_policy': 'retry_fallback_human',
                                'modular_components': True
                            }
                        },
                        'Tool Use': {
                            'implementation': 'Integrates with payment APIs, anomaly detection models, and verification systems',
                            'tools_used': ['Payment API', 'Anomaly Detection Model', 'Account Verification API', 'Banking APIs'],
                            'configuration': {
                                'max_retry_attempts': 3,
                                'tool_whitelist_required': True,
                                'input_validation': True,
                                'output_sanitization': True
                            }
                        },
                        'Exploration / Simulation': {
                            'implementation': 'Simulates payment scenarios and risk assessments before execution',
                            'scenario_testing': 'Payment risk analysis and compliance validation',
                            'configuration': {
                                'max_scenarios': 8,
                                'scenario_ranking_required': True,
                                'top_scenarios_retained': 3,
                                'assumption_documentation': True
                            }
                        },
                        'Reflection': {
                            'implementation': 'Self-evaluates payment confidence and anomaly scores before execution',
                            'reflection_criteria': ['confidence', 'anomaly_score', 'compliance', 'risk_assessment'],
                            'max_reflection_loops': 3,
                            'configuration': {
                                'reflection_notes_required': True,
                                'audit_logging': True,
                                'timeout_seconds': 120
                            }
                        },
                        'Critic/Reviewer \U0001F9D0': {
                            'implementation': 'Secondary validation of high-value payment decisions',
                            'critic_role': 'Payment risk and compliance validation',
                            'decision_authority': 'Human reviewer with critic recommendations',
                            'configuration': {
                                'evaluation_rubric_required': True,
                                'critic_output_tags': ['approve', 'reject', 'requires_human_review'],
                                'critique_traceability': True
                            }
                        },
                        'Memory & Learning': {
                            'implementation': 'Learns from payment patterns and fraud detection to improve accuracy',
                            'memory_type': 'Payment pattern recognition and fraud detection',
                            'learning_mechanism': 'Feedback loop from payment success/failure patterns',
                            'configuration': {
                                'short_term_memory_ttl': 1800,
                                'long_term_memory_summary_threshold': 20,
                                'memory_inspection_enabled': True
                            }
                        }
                    }
                }
            },
            {
                'id': 'negotiator-v1',
                'name': 'Negotiator Agent v1',
                'patternType': 'reasoning',
                'patternName': 'Negotiator Agent',
                'status': 'pilot',
                'useCase': 'Contract Negotiation',
                'risk': 'High',
                'businessUseCase': 'Automated contract negotiation with legal oversight',
                'capabilities': [
                    'Contract analysis and review',
                    'Term negotiation',
                    'Risk assessment',
                    'Legal compliance checking',
                    'Counter-proposal generation'
                ],
                'boundaries': [
                    'Max contract value: $10M',
                    'No binding decisions without human approval',
                    'Limited to standard contract types',
                    'No external legal advice'
                ],
                'dependencies': {
                    'llm': 'Claude-3 Opus',
                    'legalDB': 'Contract Database',
                    'complianceAPI': 'Legal Compliance Service',
                    'documentDB': 'Document Management System'
                },
                'owner': 'Legal Operations',
                'lifecycle': 'Pilot',
                'governanceHooks': {
                    'policies': """policies:
  - all negotiations must be reviewed by legal team
  - no binding commitments without human approval
  - must maintain negotiation audit trail
  - must comply with legal standards""",
                    'auditLogs': {'entries': 45, 'lastEscalation': 'Sept 19, 2025'},
                    'complianceTags': {'GDPR': True, 'OSFI': False, 'FINTRAC': False, 'Legal': True, 'SOC2': True},
                    'approvalHistory': ['Submitted', 'Under Legal Review']
                },
                'runtimeGuardrails': {
                    'inputFilters': ['Contract validation', 'Legal term check', 'Risk assessment'],
                    'outputValidators': ['Legal compliance', 'Term validation', 'Risk scoring'],
                    'rateControls': {'maxNegotiationsPerDay': 5, 'maxContractValue': 10000000},
                    'scopeControls': {'allowedContractTypes': ['service', 'supply', 'employment'], 'blockedTerms': ['exclusive_rights']},
                    'killSwitch': {'enabled': True, 'triggers': ['legal_risk_score > 0.8', 'unauthorized_commitments']}
                },
                'escalationMechanisms': {
                    'tieredEscalation': [
                        {'level': 1, 'action': 'Request legal review', 'status': 'success', 'timeout': '1h'},
                        {'level': 2, 'action': 'Escalate to senior legal counsel', 'status': 'pending', 'timeout': '4h'},
                        {'level': 3, 'action': 'Pause negotiations pending human review', 'status': 'not-triggered', 'timeout': '24h'}
                    ],
                    'notificationChannels': ['Email', 'Teams', 'Legal Portal'],
                    'decisionJournals': {'enabled': True, 'required': True, 'template': 'negotiation_decision'}
                },
                'monitoring': {'callsThisWeek': 12, 'guardrailTriggers': 2, 'escalations': 1, 'avgResponseTime': '45s', 'uptime': '99.5%'},
                'runtime_tools': {
                    'llm_tools': [
                        {'name': 'Azure OpenAI GPT-4', 'purpose': 'Negotiation strategy and communication', 'status': 'active'},
                        {'name': 'Claude-3-Sonnet', 'purpose': 'Complex multi-party reasoning', 'status': 'active'}
                    ],
                    'communication_tools': [
                        {'name': 'Slack API', 'purpose': 'Real-time communication with stakeholders', 'status': 'active'},
                        {'name': 'Microsoft Teams API', 'purpose': 'Enterprise communication platform', 'status': 'active'}
                    ],
                    'document_tools': [
                        {'name': 'Contract Analysis API', 'purpose': 'Contract terms and conditions analysis', 'status': 'active'},
                        {'name': 'Document Generator', 'purpose': 'Proposal and agreement creation', 'status': 'active'}
                    ],
                    'crm_tools': [
                        {'name': 'Salesforce API', 'purpose': 'Customer relationship management', 'status': 'active'},
                        {'name': 'HubSpot API', 'purpose': 'Lead and deal management', 'status': 'active'}
                    ],
                    'analytics_tools': [
                        {'name': 'Negotiation Analytics', 'purpose': 'Success rate and outcome analysis', 'status': 'active'},
                        {'name': 'Sentiment Analysis API', 'purpose': 'Stakeholder sentiment tracking', 'status': 'active'}
                    ]
                },
                'patternImplementations': {
                    'primary_patterns': ['Collaboration / Delegation', 'Planning', 'Reflection'],
                    'secondary_patterns': ['Tool Use', 'Memory & Learning', 'Critic/Reviewer'],
                    'pattern_details': {
                        'Collaboration / Delegation': {
                            'implementation': 'Coordinates with legal team and counterparty agents during negotiations',
                            'delegation_protocol': 'Structured negotiation handoffs with legal oversight',
                            'conflict_resolution': 'Legal team arbitration with negotiation state preservation',
                            'configuration': {
                                'role_declaration_required': True,
                                'handoff_packet_format': 'json',
                                'conflict_resolution': 'legal_team_arbitration',
                                'circular_delegation_check': True
                            }
                        },
                        'Planning': {
                            'implementation': 'Develops multi-step negotiation strategies and fallback plans',
                            'planning_depth': 'Strategic negotiation planning with contingency planning',
                            'plan_format': 'JSON negotiation strategies',
                            'configuration': {
                                'max_plan_depth': 4,
                                'plan_format': 'json',
                                'required_fields': ['strategy_id', 'tactics', 'fallback_plans', 'success_criteria'],
                                'replan_on_failure': True
                            }
                        },
                        'Reflection': {
                            'implementation': 'Self-evaluates negotiation progress and strategy effectiveness',
                            'reflection_criteria': ['strategy_effectiveness', 'counterparty_response', 'legal_compliance'],
                            'max_reflection_loops': 3,
                            'configuration': {
                                'reflection_notes_required': True,
                                'audit_logging': True,
                                'timeout_seconds': 300
                            }
                        },
                        'Tool Use': {
                            'implementation': 'Integrates with legal databases, contract templates, and communication systems',
                            'tools_used': ['Legal Database', 'Contract Templates', 'Communication APIs', 'Document Management'],
                            'configuration': {
                                'max_retry_attempts': 3,
                                'tool_whitelist_required': True,
                                'input_validation': True,
                                'output_sanitization': True
                            }
                        },
                        'Memory & Learning': {
                            'implementation': 'Learns from negotiation outcomes and counterparty behavior patterns',
                            'memory_type': 'Negotiation strategy and outcome patterns',
                            'learning_mechanism': 'Feedback loop from negotiation success/failure patterns',
                            'configuration': {
                                'short_term_memory_ttl': 7200,
                                'long_term_memory_summary_threshold': 25,
                                'memory_inspection_enabled': True
                            }
                        },
                        'Critic/Reviewer \U0001F9D0': {
                            'implementation': 'Legal team reviews negotiation strategies and contract terms',
                            'critic_role': 'Legal compliance and risk assessment',
                            'decision_authority': 'Legal team with negotiation override',
                            'configuration': {
                                'evaluation_rubric_required': True,
                                'critic_output_tags': ['approve', 'revise', 'reject'],
                                'critique_traceability': True
                            }
                        }
                    }
                }
            },
            {
                'id': 'classifier-v1',
                'name': 'Document Classifier v1',
                'patternType': 'classification',
                'patternName': 'Document Classifier Agent',
                'status': 'approved',
                'useCase': 'Content Classification',
                'risk': 'Low',
                'businessUseCase': 'Automated document classification and categorization for compliance and routing',
                'capabilities': [
                    'Document type classification',
                    'Content categorization',
                    'Confidence scoring',
                    'Metadata extraction',
                    'Routing recommendations'
                ],
                'boundaries': [
                    'Max document size: 50MB',
                    'No PII processing',
                    'Read-only operations',
                    'Limited to approved document types'
                ],
                'dependencies': {
                    'llm': 'Azure OpenAI GPT-4',
                    'vectorDB': 'Pinecone',
                    'storage': 'Azure Blob Storage',
                    'classifier': 'Custom Classification Model v3'
                },
                'owner': 'Content Management Team',
                'lifecycle': 'Approved',
                'governanceHooks': {
                    'policies': """policies:
  - must classify documents within 5 seconds
  - must provide confidence scores for all classifications
  - must log all classification decisions
  - must not process sensitive documents
  - must maintain audit trail""",
                    'auditLogs': {'entries': 89, 'lastEscalation': 'Sept 18, 2025'},
                    'complianceTags': {'GDPR': True, 'OSFI': True, 'FINTRAC': True, 'SOC2': True, 'HIPAA': False},
                    'approvalHistory': ['Submitted', 'Reviewed', 'Approved']
                },
                'runtimeGuardrails': {
                    'inputFilters': ['Document type validation', 'Size limits', 'Content sanitization'],
                    'outputValidators': ['Classification confidence', 'Category validation', 'Metadata completeness'],
                    'rateControls': {'maxDocumentsPerMinute': 200, 'maxConcurrentProcessing': 50},
                    'scopeControls': {'allowedTypes': ['pdf', 'docx', 'txt'], 'blockedContent': ['PII', 'financial_data']},
                    'killSwitch': {'enabled': True, 'triggers': ['classification_accuracy < 85%', 'processing_time > 10s']}
                },
                'escalationMechanisms': {
                    'tieredEscalation': [
                        {'level': 1, 'action': 'Retry with different model', 'status': 'success', 'timeout': '30s'},
                        {'level': 2, 'action': 'Escalate to Content Manager', 'status': 'pending', 'timeout': '2m'},
                        {'level': 3, 'action': 'Manual classification required', 'status': 'not-triggered', 'timeout': '5m'}
                    ],
                    'notificationChannels': ['Slack', 'Email', 'Teams'],
                    'decisionJournals': {'enabled': True, 'required': True, 'template': 'classification_decision'}
                },
                'monitoring': {'callsThisWeek': 2156, 'guardrailTriggers': 12, 'escalations': 3, 'avgResponseTime': '2.1s', 'uptime': '99.9%'},
                'runtime_tools': {
                    'llm_tools': [
                        {'name': 'Azure OpenAI GPT-4', 'purpose': 'Document classification and analysis', 'status': 'active'},
                        {'name': 'text-embedding-ada-002', 'purpose': 'Semantic document understanding', 'status': 'active'}
                    ],
                    'ml_tools': [
                        {'name': 'Azure ML Studio', 'purpose': 'Custom classification models', 'status': 'active'},
                        {'name': 'Hugging Face Transformers', 'purpose': 'Pre-trained classification models', 'status': 'active'}
                    ],
                    'vector_tools': [
                        {'name': 'Pinecone Vector DB', 'purpose': 'Document similarity search', 'status': 'active'},
                        {'name': 'Azure Cognitive Search', 'purpose': 'Hybrid search capabilities', 'status': 'active'}
                    ],
                    'document_tools': [
                        {'name': 'Azure Form Recognizer', 'purpose': 'Document structure analysis', 'status': 'active'},
                        {'name': 'OCR Service', 'purpose': 'Text extraction from images', 'status': 'active'}
                    ],
                    'storage_tools': [
                        {'name': 'Azure Blob Storage', 'purpose': 'Document storage and retrieval', 'status': 'active'},
                        {'name': 'Elasticsearch', 'purpose': 'Full-text search and indexing', 'status': 'active'}
                    ]
                },
                'patternImplementations': {
                    'primary_patterns': ['Tool Use', 'Memory & Learning', 'Reflection'],
                    'secondary_patterns': ['Critic/Reviewer', 'Planning'],
                    'pattern_details': {
                        'Tool Use': {
                            'implementation': 'Integrates with classification models, vector databases, and document storage systems',
                            'tools_used': ['Custom Classification Model v3', 'Pinecone Vector DB', 'Azure Blob Storage', 'Azure OpenAI GPT-4'],
                            'configuration': {
                                'max_retry_attempts': 3,
                                'tool_whitelist_required': True,
                                'input_validation': True,
                                'output_sanitization': True
                            }
                        },
                        'Memory & Learning': {
                            'implementation': 'Learns from classification patterns and improves accuracy over time',
                            'memory_type': 'Document classification patterns and accuracy feedback',
                            'learning_mechanism': 'Feedback loop from classification accuracy and user corrections',
                            'configuration': {
                                'short_term_memory_ttl': 3600,
                                'long_term_memory_summary_threshold': 40,
                                'memory_inspection_enabled': True
                            }
                        },
                        'Reflection': {
                            'implementation': 'Self-evaluates classification confidence and accuracy before finalizing decisions',
                            'reflection_criteria': ['confidence', 'accuracy', 'consistency', 'compliance'],
                            'max_reflection_loops': 2,
                            'configuration': {
                                'reflection_notes_required': True,
                                'audit_logging': True,
                                'timeout_seconds': 5
                            }
                        },
                        'Critic/Reviewer \U0001F9D0': {
                            'implementation': 'Secondary validation of low-confidence classifications',
                            'critic_role': 'Classification quality assurance and validation',
                            'decision_authority': 'Primary agent with critic recommendations',
                            'configuration': {
                                'evaluation_rubric_required': True,
                                'critic_output_tags': ['approve', 'revise', 'requires_human_review'],
                                'critique_traceability': True
                            }
                        },
                        'Planning': {
                            'implementation': 'Plans classification strategies for complex multi-document scenarios',
                            'planning_depth': 'Document classification workflow planning',
                            'plan_format': 'JSON classification strategies',
                            'configuration': {
                                'max_plan_depth': 3,
                                'plan_format': 'json',
                                'required_fields': ['classification_id', 'strategy', 'confidence_threshold', 'fallback_plan'],
                                'replan_on_failure': True
                            }
                        }
                    }
                }
            },
            {
                'id': 'supervisor-v1',
                'name': 'AI Supervisor Agent v1',
                'patternType': 'supervision',
                'patternName': 'AI Supervisor Agent',
                'status': 'pilot',
                'useCase': 'Agent Oversight',
                'risk': 'High',
                'businessUseCase': 'Supervises and coordinates multiple AI agents, handles escalations and quality control',
                'capabilities': [
                    'Multi-agent coordination',
                    'Escalation management',
                    'Quality assurance',
                    'Performance monitoring',
                    'Decision arbitration'
                ],
                'boundaries': [
                    'Can only supervise approved agents',
                    'No direct data access',
                    'Limited to defined escalation paths',
                    'Must log all supervisory decisions'
                ],
                'dependencies': {
                    'orchestrator': 'Temporal Workflow Engine',
                    'monitoring_system': 'Prometheus + Grafana',
                    'messaging': 'RabbitMQ',
                    'database': 'PostgreSQL'
                },
                'owner': 'AI Operations Team',
                'lifecycle': 'Pilot',
                'governanceHooks': {
                    'policies': """policies:
  - must monitor all supervised agents continuously
  - must escalate to human when confidence < 70%
  - must maintain decision audit trail
  - must not override human decisions
  - must coordinate with compliance team""",
                    'auditLogs': {'entries': 234, 'lastEscalation': 'Sept 21, 2025'},
                    'complianceTags': {'GDPR': True, 'OSFI': False, 'FINTRAC': False, 'SOC2': True, 'Legal': True},
                    'approvalHistory': ['Submitted', 'Under Review']
                },
                'runtimeGuardrails': {
                    'inputFilters': ['Agent validation', 'Permission checks', 'Escalation rules'],
                    'outputValidators': ['Decision validation', 'Escalation appropriateness', 'Quality metrics'],
                    'rateControls': {'maxEscalationsPerHour': 20, 'maxConcurrentSupervision': 10},
                    'scopeControls': {'supervisedAgents': ['payment', 'retriever', 'classifier'], 'blockedActions': ['financial_transactions']},
                    'killSwitch': {'enabled': True, 'triggers': ['escalation_rate > 50%', 'decision_confidence < 60%']}
                },
                'escalationMechanisms': {
                    'tieredEscalation': [
                        {'level': 1, 'action': 'Retry with different agent', 'status': 'success', 'timeout': '1m'},
                        {'level': 2, 'action': 'Escalate to Human Supervisor', 'status': 'pending', 'timeout': '3m'},
                        {'level': 3, 'action': 'Pause all supervised agents', 'status': 'not-triggered', 'timeout': '10m'}
                    ],
                    'notificationChannels': ['PagerDuty', 'Slack', 'Teams', 'Email'],
                    'decisionJournals': {'enabled': True, 'required': True, 'template': 'supervisory_decision'}
                },
                'monitoring': {'callsThisWeek': 156, 'guardrailTriggers': 8, 'escalations': 5, 'avgResponseTime': '1.8s', 'uptime': '99.7%'},
                'runtime_tools': {
                    'llm_tools': [
                        {'name': 'Azure OpenAI GPT-4', 'purpose': 'Supervisory decision making and coordination', 'status': 'active'},
                        {'name': 'Claude-3-Sonnet', 'purpose': 'Complex multi-agent reasoning', 'status': 'active'}
                    ],
                    'orchestration_tools': [
                        {'name': 'Kubernetes API', 'purpose': 'Agent deployment and scaling', 'status': 'active'},
                        {'name': 'Docker Registry', 'purpose': 'Agent container management', 'status': 'active'}
                    ],
                    'monitoring_tools': [
                        {'name': 'Prometheus', 'purpose': 'Agent performance metrics', 'status': 'active'},
                        {'name': 'Grafana', 'purpose': 'Visualization and dashboards', 'status': 'active'}
                    ],
                    'communication_tools': [
                        {'name': 'Agent Communication Bus', 'purpose': 'Inter-agent messaging', 'status': 'active'},
                        {'name': 'Event Streaming Platform', 'purpose': 'Real-time event processing', 'status': 'active'}
                    ],
                    'governance_tools': [
                        {'name': 'Policy Engine', 'purpose': 'Agent behavior enforcement', 'status': 'active'},
                        {'name': 'Audit System', 'purpose': 'Agent action logging and compliance', 'status': 'active'}
                    ]
                },
                'patternImplementations': {
                    'primary_patterns': ['Orchestration', 'Collaboration / Delegation', 'Critic/Reviewer'],
                    'secondary_patterns': ['Tool Use', 'Memory & Learning', 'Reflection', 'Planning'],
                    'pattern_details': {
                        'Orchestration': {
                            'implementation': 'Meta-agent coordinating multiple AI agents and managing system-wide operations',
                            'coordination_scope': 'Multi-agent system supervision and coordination',
                            'global_state_management': True,
                            'configuration': {
                                'global_state_required': True,
                                'task_registry_enabled': True,
                                'escalation_policy': 'retry_fallback_human',
                                'modular_components': True
                            }
                        },
                        'Collaboration / Delegation': {
                            'implementation': 'Coordinates and delegates tasks between specialized agents',
                            'delegation_protocol': 'Structured agent handoffs with supervisory oversight',
                            'conflict_resolution': 'Supervisor arbitration with escalation paths',
                            'configuration': {
                                'role_declaration_required': True,
                                'handoff_packet_format': 'json',
                                'conflict_resolution': 'supervisor_arbitration',
                                'circular_delegation_check': True
                            }
                        },
                        'Critic/Reviewer \U0001F9D0': {
                            'implementation': 'Reviews and validates decisions from supervised agents',
                            'critic_role': 'Multi-agent quality assurance and decision validation',
                            'decision_authority': 'Supervisor with human escalation override',
                            'configuration': {
                                'evaluation_rubric_required': True,
                                'critic_output_tags': ['approve', 'revise', 'escalate_to_human'],
                                'critique_traceability': True
                            }
                        },
                        'Tool Use': {
                            'implementation': 'Integrates with monitoring systems, messaging, and orchestration tools',
                            'tools_used': ['Temporal Workflow Engine', 'Prometheus + Grafana', 'RabbitMQ', 'PostgreSQL'],
                            'configuration': {
                                'max_retry_attempts': 3,
                                'tool_whitelist_required': True,
                                'input_validation': True,
                                'output_sanitization': True
                            }
                        },
                        'Memory & Learning': {
                            'implementation': 'Learns from agent performance patterns and escalation outcomes',
                            'memory_type': 'Agent performance patterns and supervisory decisions',
                            'learning_mechanism': 'Feedback loop from agent performance and escalation outcomes',
                            'configuration': {
                                'short_term_memory_ttl': 3600,
                                'long_term_memory_summary_threshold': 50,
                                'memory_inspection_enabled': True
                            }
                        },
                        'Reflection': {
                            'implementation': 'Self-evaluates supervisory decisions and agent coordination effectiveness',
                            'reflection_criteria': ['decision_quality', 'agent_coordination', 'escalation_appropriateness'],
                            'max_reflection_loops': 2,
                            'configuration': {
                                'reflection_notes_required': True,
                                'audit_logging': True,
                                'timeout_seconds': 60
                            }
                        },
                        'Planning': {
                            'implementation': 'Plans multi-agent coordination strategies and escalation responses',
                            'planning_depth': 'Multi-agent coordination and supervision planning',
                            'plan_format': 'JSON supervision strategies',
                            'configuration': {
                                'max_plan_depth': 4,
                                'plan_format': 'json',
                                'required_fields': ['supervision_id', 'agent_coordination', 'escalation_plan', 'success_criteria'],
                                'replan_on_failure': True
                            }
                        }
                    }
                }
            }
        ]
    }

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_status_badge(status):
    status_map = {
        'approved': {'text': 'Approved', 'class': 'status-approved'},
        'pilot': {'text': 'Pilot', 'class': 'status-pilot'},
        'draft': {'text': 'Draft', 'class': 'status-draft'}
    }
    return status_map.get(status, {'text': status, 'class': ''})

@st.cache_data(ttl=300)  # Cache for 5 minutes
def filter_agents(agents, search_term, pattern_filter, status_filter, risk_filter):
    """Optimized agent filtering with caching"""
    filtered = agents
    
    if search_term:
        search_lower = search_term.lower()
        filtered = [agent for agent in filtered if 
                   search_lower in agent['name'].lower() or
                   search_lower in agent['patternName'].lower() or
                   search_lower in ' '.join(agent['tags']).lower() or
                   search_lower in agent['description'].lower()]
    
    if pattern_filter != "All":
        filtered = [agent for agent in filtered if agent['patternName'] == pattern_filter]
    
    if status_filter != "All":
        filtered = [agent for agent in filtered if agent['status'] == status_filter]
    
    if risk_filter != "All":
        filtered = [agent for agent in filtered if agent['riskLevel'] == risk_filter]
    
    return filtered

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_landing_page_data():
    """Cache the landing page data to reduce loading time"""
    data = load_agent_data()
    agents = data['agents']
    
    # Pre-compute filtered agents for common scenarios
    all_agents = agents
    approved_agents = [agent for agent in agents if agent['status'] == 'approved']
    pilot_agents = [agent for agent in agents if agent['status'] == 'pilot']
    
    return {
        'all_agents': all_agents,
        'approved_agents': approved_agents,
        'pilot_agents': pilot_agents,
        'total_count': len(agents),
        'approved_count': len(approved_agents),
        'pilot_count': len(pilot_agents)
    }

def landing_page():
    st.markdown('<h1 class="main-header">Agentic Operating System</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #6e6e73; margin-bottom: 2rem; font-family: \'Inter\', -apple-system, BlinkMacSystemFont, \'Segoe UI\', sans-serif;">Manage and monitor your AI agents</p>', unsafe_allow_html=True)
    
    # Use cached data for better performance
    cached_data = get_landing_page_data()
    agents = cached_data['all_agents']
    
    # Search and filters
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        search_term = st.text_input("Search by pattern, risk, domain...", key="search")
    
    with col2:
        pattern_filter = st.selectbox("Pattern Type", ["All"] + list(set([agent['patternName'] for agent in agents])))
    
    with col3:
        risk_filter = st.selectbox("Risk Level", ["All"] + list(set([agent['risk'] for agent in agents])))
    
    with col4:
        lifecycle_filter = st.selectbox("Lifecycle", ["All"] + list(set([agent['status'] for agent in agents])))
    
    # Use optimized filtering function with caching
    filtered_agents = filter_agents(agents, search_term, pattern_filter, risk_filter, lifecycle_filter)
    
    # Main tabs for Pattern Cards, Tools Layer, and Agent Cards
    
    main_tab1, main_tab2, main_tab3 = st.tabs(["Pattern Cards", "Tools Layer", "Agent Cards"])
    
    with main_tab1:
        # Pattern Cards Tab
        st.markdown("### Pattern Cards")
        st.markdown("""
        **Agentic AI patterns are essentially reusable building blocks for designing autonomous AI systems that don't just generate text, but reason, act, and improve over time. These are "design primitives" for scaling agentic workflows across enterprise and property-like domains, with all policies/rules observable as the agents are deployed.**
        """)
        
        # Pattern Cards
        patterns = [
            {
                "name": "Reflection",
                "description": "The agent evaluates its own outputs, reasoning, or actions, then iteratively improves them.",
                "example": "Insurance Claims Agent checking submitted forms for errors before submission",
                "rules": [
                    "Always separate generation from evaluation (two distinct phases).",
                    "Use explicit criteria (accuracy, compliance, clarity) for self-checks.",
                    "Limit recursion depth to avoid infinite loops.",
                    "Log reflection steps for auditability"
                ],
                "explicit_policies": [
                    "Rule: Every reflection cycle must produce a 'reflection note' (e.g., 'I found a factual inconsistency in step 3').",
                    "Rule: Limit to max 3 reflection loops per task to prevent infinite recursion.",
                    "Rule: Reflections must be scored against a rubric (accuracy, clarity, compliance) before revision is accepted.",
                    "Rule: Store reflection notes in logs for audit review."
                ]
            },
            {
                "name": "Planning",
                "description": "The agent breaks down a high-level goal into sub-tasks, sequencing them logically.",
                "example": "Multi-step property rebate application workflow - Enterprise AI orchestrating data retrieval, validation, and reporting",
                "rules": [
                    "Plans must be explicit, structured, and machine-readable (e.g., JSON, checklist).",
                    "Each sub-task should have a clear success/failure condition.",
                    "Plans should be revisable mid-execution if context changes.",
                    "Avoid over-planning: cap task depth to prevent combinatorial explosion."
                ],
                "explicit_policies": [
                    "Rule: Plans must be output in structured JSON with fields: task_id, description, dependencies, success_criteria.",
                    "Rule: Each sub-task must have a binary success/failure condition.",
                    "Rule: Plans deeper than 5 nested levels are automatically pruned.",
                    "Rule: If a plan fails mid-execution, the agent must re-plan with updated context."
                ]
            },
            {
                "name": "Tool Use",
                "description": "The agent invokes external tools, APIs, or systems to complete tasks beyond text generation.",
                "example": "Calling APIs for tax rules - Triggering enterprise workflows (e.g., updating CRM records)",
                "rules": [
                    "Tools must be registered with metadata (capabilities, constraints, authentication).",
                    "Validate inputs/outputs before and after tool calls.",
                    "Fail gracefully if a tool is unavailable.",
                    "Enforce least-privilege access (only use tools necessary for the task)."
                ],
                "explicit_policies": [
                    "Rule: Tools must be whitelisted with metadata: capabilities, auth method, rate limits.",
                    "Rule: Inputs must be validated against schema before sending to tool.",
                    "Rule: Outputs must be sanitized (e.g., strip PII, enforce type checks).",
                    "Rule: If a tool fails 3 times, agent must fallback to alternate tool or human escalation."
                ]
            },
            {
                "name": "Collaboration / Delegation",
                "description": "Multiple specialized agents coordinate, hand off tasks, or negotiate roles.",
                "example": "Multiple specialized agents coordinate, hand off tasks, or negotiate roles.",
                "rules": [
                    "Define clear roles (e.g., 'Researcher,' 'Validator,' 'Summarizer').",
                    "Use structured protocols for handoffs (e.g., message schema).",
                    "Resolve conflicts via arbitration rules (e.g., majority vote, critic override).",
                    "Prevent circular delegation (avoid infinite loops of agents passing tasks)"
                ],
                "explicit_policies": [
                    "Rule: Each agent must declare its role (e.g., 'Researcher,' 'Validator').",
                    "Rule: Handoffs must include a handoff packet: task_summary, status, open_issues.",
                    "Rule: Conflicts are resolved by critic agent override or majority vote.",
                    "Rule: Circular delegation is forbidden (system checks for loops)."
                ]
            },
            {
                "name": "Memory & Learning",
                "description": "The agent retains context across sessions, adapts from feedback, and improves over time.",
                "example": "Remembering prior rebate submissions to pre-fill forms - Enterprise AI learning from past board briefings",
                "rules": [
                    "Separate short-term memory (session context) from long-term memory (persistent knowledge).",
                    "Apply retention policies (expiry, summarization, redaction).",
                    "Ensure transparency: memory must be inspectable and editable.",
                    "Guard against contamination (don't store sensitive or irrelevant data)."
                ],
                "explicit_policies": [
                    "Rule: Short-term memory expires after session ends unless explicitly promoted.",
                    "Rule: Long-term memory must be summarized every 30 entries to prevent drift.",
                    "Rule: Users must be able to inspect and delete memory entries.",
                    "Rule: Sensitive data (e.g., passwords, PII) is never stored in memory."
                ]
            },
            {
                "name": "Critic / Reviewer \U0001F9D0",
                "description": "A secondary agent (or role) critiques the primary agent's output before final delivery",
                "example": "'Red team' agent checking for bias, gaps, or regulatory misalignment",
                "rules": [
                    "Critic must use explicit evaluation rubrics (accuracy, bias, compliance).",
                    "Critic cannot modify outputs directly-only suggest changes.",
                    "Final decision authority must be defined (critic vs. primary agent vs. orchestrator).",
                    "Maintain traceability: log critiques alongside outputs."
                ],
                "explicit_policies": [
                    "Rule: Critic must use a rubric (e.g., factual accuracy, bias, compliance).",
                    "Rule: Critic outputs must be tagged as approve, revise, or reject.",
                    "Rule: Critic cannot directly edit-only recommend changes.",
                    "Rule: Final decision authority is explicitly assigned (critic vs. orchestrator)."
                ]
            },
            {
                "name": "Exploration / Simulation",
                "description": "The agent runs multiple hypothetical scenarios before choosing an action.",
                "example": "Portfolio yield strategy simulations - Testing rebate eligibility under different ownership structures",
                "rules": [
                    "Cap the number of scenarios to balance breadth vs. cost.",
                    "Use scoring functions to rank scenarios (e.g., risk, efficiency, compliance).",
                    "Document assumptions for each scenario.",
                    "Ensure exploration doesn't delay time-sensitive tasks."
                ],
                "explicit_policies": [
                    "Rule: Max N=10 scenarios per exploration cycle.",
                    "Rule: Each scenario must include assumptions + projected outcome.",
                    "Rule: Scenarios must be ranked using a scoring function (e.g., risk-adjusted return).",
                    "Rule: Top 3 scenarios are retained; others are discarded to save resources."
                ]
            },
            {
                "name": "Orchestration",
                "description": "A meta-agent coordinates multiple agents, tools, and workflows into a coherent pipeline.",
                "example": "Enterprise AI hub managing compliance, reporting, and approvals end-to-end",
                "rules": [
                    "Orchestrator must maintain a global state and task registry.",
                    "Define escalation rules for failures (retry, fallback, human-in-loop).",
                    "Enforce modularity: agents/tools should be swappable without breaking the system.",
                    "Monitor performance and resource usage across the pipeline."
                ],
                "explicit_policies": [
                    "Rule: Orchestrator must maintain a global task registry with status updates.",
                    "Rule: Failures trigger escalation policy: retry → fallback → human-in-loop.",
                    "Rule: All agents/tools must be modular (swappable without breaking pipeline).",
                    "Rule: Orchestrator must log resource usage (time, tokens, API calls)."
                ]
            }
        ]
        
        # Display pattern cards in a grid
        cols = st.columns(2)
        for i, pattern in enumerate(patterns):
            with cols[i % 2]:
                with st.expander(f"{pattern['name']}", expanded=False):
                    # Pattern Overview tab
                    tab1, tab2, tab3 = st.tabs(["Pattern Overview", "Rules & Policies", "Codified/Executable"])
                    
                    with tab1:
                        st.markdown(f"**What it does:** {pattern['description']}")
                        st.markdown(f"**Example Use Cases:** {pattern['example']}")
                        
                        # Pattern Details
                        st.markdown("### Pattern Details")
                        pattern_name = pattern['name'].split(' ')[0].lower()
                        
                        if pattern_name == "reflection":
                            st.markdown("**Core Concept:** Self-evaluation and iterative improvement through structured self-assessment cycles.")
                            st.markdown("**Key Components:**")
                            st.markdown("- **Evaluation Engine**: Assesses output quality against predefined criteria")
                            st.markdown("- **Improvement Loop**: Iteratively refines outputs based on evaluation results")
                            st.markdown("- **Audit Trail**: Maintains logs of all reflection cycles for transparency")
                            
                            # Flow diagram for Reflection pattern
                            st.markdown("### Pattern Flow Diagram")
                            
                            col1, col2 = st.columns([1, 1])
                            
                            with col1:
                                st.markdown("""
                                ```
                                Input → Generate → Evaluate
                                         →         ↓
                                    Apply Fixes â† Quality
                                         ↓
                                    Max Loops → Human
                                         ↓
                                    Final Output
                                ```
                                """)
                            
                            with col2:
                                st.markdown("**Key Features:**")
                                st.markdown("• **Self-Evaluation**: Quality assessment")
                                st.markdown("• **Iterative Improvement**: Refinement cycles")
                                st.markdown("• **Quality Gates**: Pass/fail criteria")
                                st.markdown("• **Escalation**: Human intervention")
                                st.markdown("• **Audit Trail**: Complete logging")
                            
                        elif pattern_name == "planning":
                            st.markdown("**Core Concept:** Hierarchical goal decomposition and task sequencing for complex workflows.")
                            st.markdown("**Key Components:**")
                            st.markdown("- **Goal Decomposer**: Breaks down high-level objectives into actionable tasks")
                            st.markdown("- **Dependency Manager**: Handles task dependencies and sequencing")
                            st.markdown("- **Plan Executor**: Monitors and adjusts plan execution in real-time")
                            
                            # Flow diagram for Planning pattern
                            st.markdown("### Pattern Flow Diagram")
                            
                            col1, col2 = st.columns([1, 1])
                            
                            with col1:
                                st.markdown("""
                                ```
                                Goal → Analyze → Break Down
                                         ↓
                                Dependencies → Plan → Validate
                                         ↓
                                Execute → Monitor → Complete
                                ```
                                """)
                            
                            with col2:
                                st.markdown("**Key Features:**")
                                st.markdown("• **Hierarchical Decomposition**: Goal breakdown")
                                st.markdown("• **Dependency Mapping**: Task sequencing")
                                st.markdown("• **Plan Validation**: Feasibility check")
                                st.markdown("• **Progress Monitoring**: Status tracking")
                                st.markdown("• **Adaptive Execution**: Real-time adjustment")
                            
                        elif pattern_name == "tool":
                            st.markdown("**Core Concept:** External tool integration with validation, error handling, and fallback mechanisms.")
                            st.markdown("**Key Components:**")
                            st.markdown("- **Tool Registry**: Manages available tools and their capabilities")
                            st.markdown("- **Input Validator**: Ensures inputs meet tool requirements")
                            st.markdown("- **Execution Engine**: Handles tool calls with retry logic")
                            st.markdown("- **Output Sanitizer**: Cleans and validates tool outputs")
                            
                            # Flow diagram for Tool Use pattern
                            st.markdown("### Pattern Flow Diagram")
                            
                            col1, col2 = st.columns([1, 1])
                            
                            with col1:
                                st.markdown("""
                                ```
                                Request → Select → Validate
                                         ↓
                                Execute → Success → Sanitize
                                         ↓
                                Retry → Fallback → Human
                                         ↓
                                Return Result
                                ```
                                """)
                            
                            with col2:
                                st.markdown("**Key Features:**")
                                st.markdown("• **Tool Selection**: Appropriate tool choice")
                                st.markdown("• **Input Validation**: Parameter verification")
                                st.markdown("• **Error Handling**: Retry & fallback")
                                st.markdown("• **Output Sanitization**: Result cleaning")
                                st.markdown("• **Escalation Path**: Human intervention")
                            
                        elif pattern_name == "collaboration":
                            st.markdown("**Core Concept:** Multi-agent coordination with role-based delegation and conflict resolution.")
                            st.markdown("**Key Components:**")
                            st.markdown("- **Role Manager**: Defines and manages agent roles and capabilities")
                            st.markdown("- **Delegation Engine**: Handles task handoffs between agents")
                            st.markdown("- **Conflict Resolver**: Manages disagreements and arbitration")
                            st.markdown("- **Coordination Hub**: Central communication and state management")
                            
                            # Flow diagram for Collaboration pattern
                            st.markdown("### Pattern Flow Diagram")
                            
                            col1, col2 = st.columns([1, 1])
                            
                            with col1:
                                st.markdown("""
                                ```
                                Task → Roles → Agents
                                         ↓
                                Delegate → Process → Results
                                         ↓
                                Coordinate → Validate → Combine
                                         ↓
                                Conflict → Resolve → Final
                                ```
                                """)
                            
                            with col2:
                                st.markdown("**Key Features:**")
                                st.markdown("• **Role-Based Delegation**: Specialized agents")
                                st.markdown("• **Parallel Processing**: Simultaneous work")
                                st.markdown("• **Coordination Hub**: Result aggregation")
                                st.markdown("• **Conflict Resolution**: Disagreement handling")
                                st.markdown("• **Consensus Building**: Agreement negotiation")
                            
                        elif pattern_name == "memory":
                            st.markdown("**Core Concept:** Context retention and adaptive learning with memory management and knowledge evolution.")
                            st.markdown("**Key Components:**")
                            st.markdown("- **Memory Store**: Short-term and long-term memory systems")
                            st.markdown("- **Learning Engine**: Adapts behavior based on experience")
                            st.markdown("- **Context Manager**: Maintains session and cross-session context")
                            st.markdown("- **Knowledge Base**: Persistent knowledge storage and retrieval")
                            
                            # Flow diagram for Memory & Learning pattern
                            st.markdown("### Pattern Flow Diagram")
                            
                            col1, col2 = st.columns([1, 1])
                            
                            with col1:
                                st.markdown("""
                                ```
                                Experience → Analyze → Classify
                                         ↓
                                Short-term / Long-term Storage
                                         ↓
                                Learning → Adapt → Evaluate
                                         ↓
                                Improved → Update Model
                                ```
                                """)
                            
                            with col2:
                                st.markdown("**Key Features:**")
                                st.markdown("• **Memory Classification**: Short/long-term storage")
                                st.markdown("• **Context Analysis**: Experience significance")
                                st.markdown("• **Learning Process**: Behavior adaptation")
                                st.markdown("• **Performance Evaluation**: Learning effectiveness")
                                st.markdown("• **Knowledge Consolidation**: Integration")
                            
                        elif pattern_name == "critic":
                            st.markdown("**Core Concept:** Secondary validation and quality assurance through independent critique and review.")
                            st.markdown("**Key Components:**")
                            st.markdown("- **Critique Engine**: Evaluates outputs against quality rubrics")
                            st.markdown("- **Review Process**: Structured assessment and feedback generation")
                            st.markdown("- **Decision Authority**: Clear escalation and approval workflows")
                            st.markdown("- **Audit Trail**: Complete traceability of critique decisions")
                            
                            # Flow diagram for Critic/Reviewer pattern
                            st.markdown("### Pattern Flow Diagram")
                            
                            col1, col2 = st.columns([1, 1])
                            
                            with col1:
                                st.markdown("""
                                ```
                                Output → Assign → Rubric
                                         ↓
                                Assess → Review → Decision
                                         ↓
                                Approve / Revise / Reject
                                         ↓
                                Deliver / Fix / Human
                                ```
                                """)
                            
                            with col2:
                                st.markdown("**Key Features:**")
                                st.markdown("• **Independent Review**: Unbiased evaluation")
                                st.markdown("• **Quality Rubrics**: Structured criteria")
                                st.markdown("• **Revision Process**: Iterative improvement")
                                st.markdown("• **Escalation Path**: Human expert review")
                                st.markdown("• **Audit Trail**: Complete traceability")
                            
                        elif pattern_name == "exploration":
                            st.markdown("**Core Concept:** Multi-scenario testing and exploration for optimal decision-making.")
                            st.markdown("**Key Components:**")
                            st.markdown("- **Scenario Generator**: Creates multiple hypothetical situations")
                            st.markdown("- **Simulation Engine**: Executes scenarios and measures outcomes")
                            st.markdown("- **Scoring System**: Ranks scenarios based on defined criteria")
                            st.markdown("- **Selection Logic**: Chooses optimal scenario for execution")
                            
                            # Flow diagram for Exploration/Simulation pattern
                            st.markdown("### Pattern Flow Diagram")
                            
                            col1, col2 = st.columns([1, 1])
                            
                            with col1:
                                st.markdown("""
                                ```
                                Decision → Generate → Simulate
                                         ↓
                                Measure → Score → Select Best
                                         ↓
                                Validate → Execute → Monitor
                                         ↓
                                Match → Update Model
                                ```
                                """)
                            
                            with col2:
                                st.markdown("**Key Features:**")
                                st.markdown("• **Multi-Scenario Generation**: Multiple situations")
                                st.markdown("• **Parallel Simulation**: Simultaneous testing")
                                st.markdown("• **Outcome Measurement**: Result quantification")
                                st.markdown("• **Assumption Validation**: Scenario verification")
                                st.markdown("• **Learning Integration**: Model updates")
                            
                        else:  # orchestration
                            st.markdown("**Core Concept:** Meta-agent coordination managing multiple agents, tools, and workflows in a unified pipeline.")
                            st.markdown("**Key Components:**")
                            st.markdown("- **Pipeline Manager**: Orchestrates end-to-end workflow execution")
                            st.markdown("- **Resource Coordinator**: Manages agent and tool allocation")
                            st.markdown("- **State Monitor**: Tracks global system state and progress")
                            st.markdown("- **Escalation Handler**: Manages failures and recovery procedures")
                            
                            # Flow diagram for Orchestration pattern
                            st.markdown("### Pattern Flow Diagram")
                            
                            col1, col2 = st.columns([1, 1])
                            
                            with col1:
                                st.markdown("""
                                ```
                                Request → Analyze → Plan
                                         ↓
                                Allocate → Distribute → Monitor
                                         ↓
                                Complete → Aggregate → Validate
                                         ↓
                                Quality → Deliver Output
                                ```
                                """)
                            
                            with col2:
                                st.markdown("**Key Features:**")
                                st.markdown("• **Pipeline Management**: End-to-end orchestration")
                                st.markdown("• **Resource Allocation**: Agent/tool optimization")
                                st.markdown("• **Progress Monitoring**: Execution tracking")
                                st.markdown("• **Failure Recovery**: Error handling")
                                st.markdown("• **Quality Validation**: Output standards")
                        
                        # Pattern Benefits and Use Cases
                        st.markdown("### Pattern Benefits")
                        benefits = {
                            "reflection": [
                                "Improved output quality through self-assessment",
                                "Reduced human intervention needs",
                                "Enhanced transparency and auditability",
                                "Continuous learning and adaptation"
                            ],
                            "planning": [
                                "Structured approach to complex tasks",
                                "Clear task dependencies and sequencing",
                                "Adaptive planning based on real-time feedback",
                                "Reduced execution errors and delays"
                            ],
                            "tool": [
                                "Seamless integration with external systems",
                                "Robust error handling and fallback mechanisms",
                                "Input/output validation and sanitization",
                                "Scalable tool management and monitoring"
                            ],
                            "collaboration": [
                                "Distributed problem-solving capabilities",
                                "Role-based specialization and expertise",
                                "Conflict resolution and consensus building",
                                "Scalable multi-agent coordination"
                            ],
                            "memory": [
                                "Context-aware decision making",
                                "Learning from past experiences",
                                "Personalized and adaptive responses",
                                "Knowledge accumulation and evolution"
                            ],
                            "critic": [
                                "Quality assurance and validation",
                                "Independent review and oversight",
                                "Reduced bias and error propagation",
                                "Clear accountability and traceability"
                            ],
                            "exploration": [
                                "Optimal decision making through exploration",
                                "Risk assessment and scenario planning",
                                "Adaptive strategy selection",
                                "Learning from hypothetical outcomes"
                            ],
                            "orchestration": [
                                "End-to-end workflow management",
                                "Resource optimization and allocation",
                                "Centralized monitoring and control",
                                "Scalable and maintainable systems"
                            ]
                        }
                        
                        for benefit in benefits.get(pattern_name, []):
                            st.markdown(f"• {benefit}")
                        
                        # Implementation Considerations
                        st.markdown("### Implementation Considerations")
                        considerations = {
                            "reflection": [
                                "Set clear evaluation criteria and rubrics",
                                "Implement recursion limits to prevent infinite loops",
                                "Maintain comprehensive audit logs",
                                "Balance reflection depth with performance requirements"
                            ],
                            "planning": [
                                "Define clear task decomposition rules",
                                "Implement robust dependency management",
                                "Plan for mid-execution adjustments",
                                "Monitor and optimize planning performance"
                            ],
                            "tool": [
                                "Maintain comprehensive tool registry",
                                "Implement robust error handling",
                                "Ensure input/output validation",
                                "Monitor tool performance and availability"
                            ],
                            "collaboration": [
                                "Define clear agent roles and responsibilities",
                                "Implement effective communication protocols",
                                "Establish conflict resolution mechanisms",
                                "Monitor collaboration effectiveness"
                            ],
                            "memory": [
                                "Design appropriate memory hierarchies",
                                "Implement privacy and security controls",
                                "Balance memory capacity with performance",
                                "Ensure memory consistency and reliability"
                            ],
                            "critic": [
                                "Develop comprehensive evaluation rubrics",
                                "Ensure critic independence and objectivity",
                                "Implement clear decision authority",
                                "Maintain detailed critique audit trails"
                            ],
                            "exploration": [
                                "Define scenario generation parameters",
                                "Implement efficient simulation engines",
                                "Develop robust scoring mechanisms",
                                "Balance exploration breadth with computational cost"
                            ],
                            "orchestration": [
                                "Design scalable pipeline architectures",
                                "Implement comprehensive monitoring",
                                "Plan for failure recovery and resilience",
                                "Ensure resource efficiency and optimization"
                            ]
                        }
                        
                        for consideration in considerations.get(pattern_name, []):
                            st.markdown(f"• {consideration}")
                    
                    with tab2:
                        st.markdown("**Rules/Policies:**")
                        for rule in pattern['rules']:
                            st.write(f"• {rule}")
                        
                        st.markdown("**Explicit Policies:**")
                        for policy in pattern['explicit_policies']:
                            st.write(f"• {policy}")
                    
                    with tab3:
                        st.markdown("**Codified/Executable Configuration**")
                        st.markdown("*DevOps Pipeline Observable Configuration*")
                        
                        # Generate executable configuration based on pattern type
                        pattern_name = pattern['name'].split(' ')[0].lower()
                        
                        if pattern_name == "reflection":
                            config = {
                                "pattern": "reflection",
                                "version": "1.0.0",
                                "metadata": {
                                    "name": "Reflection Pattern",
                                    "description": "Self-evaluation and iterative improvement pattern",
                                    "author": "Agentic AI Team",
                                    "created": "2025-01-24",
                                    "tags": ["self-improvement", "quality-assurance", "iterative"]
                                },
                                "configuration": {
                                    "max_reflection_loops": 3,
                                    "reflection_criteria": ["accuracy", "clarity", "compliance"],
                                    "reflection_notes_required": True,
                                    "audit_logging": True,
                                    "timeout_seconds": 300
                                },
                                "observability": {
                                    "metrics": [
                                        "reflection_cycles_count",
                                        "reflection_notes_generated",
                                        "improvement_score_delta",
                                        "reflection_time_ms"
                                    ],
                                    "alerts": [
                                        {
                                            "name": "max_reflection_loops_exceeded",
                                            "condition": "reflection_cycles > 3",
                                            "severity": "warning"
                                        },
                                        {
                                            "name": "reflection_timeout",
                                            "condition": "reflection_time > 300s",
                                            "severity": "error"
                                        }
                                    ],
                                    "logs": [
                                        "reflection_cycle_start",
                                        "reflection_note_generated",
                                        "reflection_cycle_complete",
                                        "reflection_timeout"
                                    ]
                                },
                                "devops": {
                                    "deployment": {
                                        "environment": "production",
                                        "replicas": 2,
                                        "resources": {
                                            "cpu": "500m",
                                            "memory": "1Gi"
                                        }
                                    },
                                    "monitoring": {
                                        "prometheus_metrics": True,
                                        "grafana_dashboard": "reflection-pattern",
                                        "health_check_endpoint": "/health/reflection"
                                    }
                                }
                            }
                        elif pattern_name == "planning":
                            config = {
                                "pattern": "planning",
                                "version": "1.0.0",
                                "metadata": {
                                    "name": "Planning Pattern",
                                    "description": "Goal decomposition and task sequencing pattern",
                                    "author": "Agentic AI Team",
                                    "created": "2025-01-24",
                                    "tags": ["task-decomposition", "workflow", "orchestration"]
                                },
                                "configuration": {
                                    "max_plan_depth": 5,
                                    "plan_format": "json",
                                    "required_fields": ["task_id", "description", "dependencies", "success_criteria"],
                                    "replan_on_failure": True,
                                    "plan_validation": True
                                },
                                "observability": {
                                    "metrics": [
                                        "plans_generated",
                                        "plan_depth_distribution",
                                        "plan_execution_success_rate",
                                        "replan_events_count"
                                    ],
                                    "alerts": [
                                        {
                                            "name": "plan_depth_exceeded",
                                            "condition": "plan_depth > 5",
                                            "severity": "warning"
                                        },
                                        {
                                            "name": "plan_execution_failure",
                                            "condition": "plan_success_rate < 0.8",
                                            "severity": "error"
                                        }
                                    ],
                                    "logs": [
                                        "plan_generation_start",
                                        "plan_validation_result",
                                        "plan_execution_start",
                                        "replan_triggered"
                                    ]
                                },
                                "devops": {
                                    "deployment": {
                                        "environment": "production",
                                        "replicas": 3,
                                        "resources": {
                                            "cpu": "1000m",
                                            "memory": "2Gi"
                                        }
                                    },
                                    "monitoring": {
                                        "prometheus_metrics": True,
                                        "grafana_dashboard": "planning-pattern",
                                        "health_check_endpoint": "/health/planning"
                                    }
                                }
                            }
                        elif pattern_name == "tool":
                            config = {
                                "pattern": "tool_use",
                                "version": "1.0.0",
                                "metadata": {
                                    "name": "Tool Use Pattern",
                                    "description": "External tool and API integration pattern",
                                    "author": "Agentic AI Team",
                                    "created": "2025-01-24",
                                    "tags": ["api-integration", "external-tools", "automation"]
                                },
                                "configuration": {
                                    "max_retry_attempts": 3,
                                    "tool_whitelist_required": True,
                                    "input_validation": True,
                                    "output_sanitization": True,
                                    "rate_limiting": True
                                },
                                "observability": {
                                    "metrics": [
                                        "tool_calls_total",
                                        "tool_success_rate",
                                        "tool_response_time_ms",
                                        "tool_retry_count"
                                    ],
                                    "alerts": [
                                        {
                                            "name": "tool_failure_rate_high",
                                            "condition": "tool_success_rate < 0.7",
                                            "severity": "error"
                                        },
                                        {
                                            "name": "tool_response_time_slow",
                                            "condition": "avg_response_time > 5000ms",
                                            "severity": "warning"
                                        }
                                    ],
                                    "logs": [
                                        "tool_call_initiated",
                                        "tool_call_success",
                                        "tool_call_failure",
                                        "tool_retry_attempt"
                                    ]
                                },
                                "devops": {
                                    "deployment": {
                                        "environment": "production",
                                        "replicas": 4,
                                        "resources": {
                                            "cpu": "800m",
                                            "memory": "1.5Gi"
                                        }
                                    },
                                    "monitoring": {
                                        "prometheus_metrics": True,
                                        "grafana_dashboard": "tool-use-pattern",
                                        "health_check_endpoint": "/health/tools"
                                    }
                                }
                            }
                        elif pattern_name == "collaboration":
                            config = {
                                "pattern": "collaboration",
                                "version": "1.0.0",
                                "metadata": {
                                    "name": "Collaboration Pattern",
                                    "description": "Multi-agent coordination and delegation pattern",
                                    "author": "Agentic AI Team",
                                    "created": "2025-01-24",
                                    "tags": ["multi-agent", "delegation", "coordination"]
                                },
                                "configuration": {
                                    "role_declaration_required": True,
                                    "handoff_packet_format": "json",
                                    "conflict_resolution": "critic_override",
                                    "circular_delegation_check": True,
                                    "handoff_timeout": 30
                                },
                                "observability": {
                                    "metrics": [
                                        "handoffs_total",
                                        "collaboration_success_rate",
                                        "conflict_resolution_count",
                                        "circular_delegation_detected"
                                    ],
                                    "alerts": [
                                        {
                                            "name": "circular_delegation_detected",
                                            "condition": "circular_delegation_count > 0",
                                            "severity": "error"
                                        },
                                        {
                                            "name": "handoff_timeout",
                                            "condition": "handoff_time > 30s",
                                            "severity": "warning"
                                        }
                                    ],
                                    "logs": [
                                        "agent_role_declared",
                                        "handoff_initiated",
                                        "handoff_completed",
                                        "conflict_detected"
                                    ]
                                },
                                "devops": {
                                    "deployment": {
                                        "environment": "production",
                                        "replicas": 5,
                                        "resources": {
                                            "cpu": "1200m",
                                            "memory": "2.5Gi"
                                        }
                                    },
                                    "monitoring": {
                                        "prometheus_metrics": True,
                                        "grafana_dashboard": "collaboration-pattern",
                                        "health_check_endpoint": "/health/collaboration"
                                    }
                                }
                            }
                        elif pattern_name == "memory":
                            config = {
                                "pattern": "memory_learning",
                                "version": "1.0.0",
                                "metadata": {
                                    "name": "Memory & Learning Pattern",
                                    "description": "Context retention and adaptive learning pattern",
                                    "author": "Agentic AI Team",
                                    "created": "2025-01-24",
                                    "tags": ["memory", "learning", "adaptation", "context"]
                                },
                                "configuration": {
                                    "short_term_memory_ttl": 3600,
                                    "long_term_memory_summary_threshold": 30,
                                    "memory_inspection_enabled": True,
                                    "pii_filtering": True,
                                    "memory_encryption": True
                                },
                                "observability": {
                                    "metrics": [
                                        "memory_entries_created",
                                        "memory_retrieval_count",
                                        "memory_summary_events",
                                        "pii_filtered_count"
                                    ],
                                    "alerts": [
                                        {
                                            "name": "memory_usage_high",
                                            "condition": "memory_usage_percent > 80",
                                            "severity": "warning"
                                        },
                                        {
                                            "name": "pii_detected",
                                            "condition": "pii_filtered_count > 0",
                                            "severity": "critical"
                                        }
                                    ],
                                    "logs": [
                                        "memory_entry_created",
                                        "memory_retrieved",
                                        "memory_summarized",
                                        "pii_filtered"
                                    ]
                                },
                                "devops": {
                                    "deployment": {
                                        "environment": "production",
                                        "replicas": 3,
                                        "resources": {
                                            "cpu": "1000m",
                                            "memory": "3Gi"
                                        }
                                    },
                                    "monitoring": {
                                        "prometheus_metrics": True,
                                        "grafana_dashboard": "memory-learning-pattern",
                                        "health_check_endpoint": "/health/memory"
                                    }
                                }
                            }
                        elif pattern_name == "critic":
                            config = {
                                "pattern": "critic_reviewer",
                                "version": "1.0.0",
                                "metadata": {
                                    "name": "Critic/Reviewer Pattern",
                                    "description": "Secondary agent critique and review pattern",
                                    "author": "Agentic AI Team",
                                    "created": "2025-01-24",
                                    "tags": ["review", "critique", "quality-assurance", "validation"]
                                },
                                "configuration": {
                                    "evaluation_rubric_required": True,
                                    "critic_output_tags": ["approve", "revise", "reject"],
                                    "critic_edit_restricted": True,
                                    "decision_authority": "orchestrator",
                                    "critique_traceability": True
                                },
                                "observability": {
                                    "metrics": [
                                        "critiques_performed",
                                        "critique_approval_rate",
                                        "critique_revision_rate",
                                        "critique_rejection_rate"
                                    ],
                                    "alerts": [
                                        {
                                            "name": "high_rejection_rate",
                                            "condition": "rejection_rate > 0.3",
                                            "severity": "warning"
                                        },
                                        {
                                            "name": "critique_timeout",
                                            "condition": "critique_time > 60s",
                                            "severity": "error"
                                        }
                                    ],
                                    "logs": [
                                        "critique_initiated",
                                        "critique_completed",
                                        "critique_approved",
                                        "critique_rejected"
                                    ]
                                },
                                "devops": {
                                    "deployment": {
                                        "environment": "production",
                                        "replicas": 2,
                                        "resources": {
                                            "cpu": "600m",
                                            "memory": "1.2Gi"
                                        }
                                    },
                                    "monitoring": {
                                        "prometheus_metrics": True,
                                        "grafana_dashboard": "critic-reviewer-pattern",
                                        "health_check_endpoint": "/health/critic"
                                    }
                                }
                            }
                        elif pattern_name == "exploration":
                            config = {
                                "pattern": "exploration_simulation",
                                "version": "1.0.0",
                                "metadata": {
                                    "name": "Exploration/Simulation Pattern",
                                    "description": "Multi-scenario testing and exploration pattern",
                                    "author": "Agentic AI Team",
                                    "created": "2025-01-24",
                                    "tags": ["simulation", "exploration", "scenario-testing", "optimization"]
                                },
                                "configuration": {
                                    "max_scenarios": 10,
                                    "scenario_ranking_required": True,
                                    "top_scenarios_retained": 3,
                                    "assumption_documentation": True,
                                    "scenario_timeout": 120
                                },
                                "observability": {
                                    "metrics": [
                                        "scenarios_generated",
                                        "scenarios_executed",
                                        "scenario_ranking_time_ms",
                                        "top_scenarios_retained"
                                    ],
                                    "alerts": [
                                        {
                                            "name": "scenario_timeout",
                                            "condition": "scenario_time > 120s",
                                            "severity": "warning"
                                        },
                                        {
                                            "name": "max_scenarios_exceeded",
                                            "condition": "scenarios_generated > 10",
                                            "severity": "error"
                                        }
                                    ],
                                    "logs": [
                                        "scenario_generation_start",
                                        "scenario_execution_start",
                                        "scenario_ranking_complete",
                                        "scenario_timeout"
                                    ]
                                },
                                "devops": {
                                    "deployment": {
                                        "environment": "production",
                                        "replicas": 3,
                                        "resources": {
                                            "cpu": "1500m",
                                            "memory": "2.5Gi"
                                        }
                                    },
                                    "monitoring": {
                                        "prometheus_metrics": True,
                                        "grafana_dashboard": "exploration-simulation-pattern",
                                        "health_check_endpoint": "/health/exploration"
                                    }
                                }
                            }
                        else:  # orchestration
                            config = {
                                "pattern": "orchestration",
                                "version": "1.0.0",
                                "metadata": {
                                    "name": "Orchestration Pattern",
                                    "description": "Meta-agent coordination and pipeline management pattern",
                                    "author": "Agentic AI Team",
                                    "created": "2025-01-24",
                                    "tags": ["orchestration", "pipeline", "coordination", "meta-agent"]
                                },
                                "configuration": {
                                    "global_state_required": True,
                                    "task_registry_enabled": True,
                                    "escalation_policy": "retry_fallback_human",
                                    "modular_components": True,
                                    "resource_monitoring": True
                                },
                                "observability": {
                                    "metrics": [
                                        "pipeline_executions",
                                        "pipeline_success_rate",
                                        "escalation_events",
                                        "resource_usage_percent"
                                    ],
                                    "alerts": [
                                        {
                                            "name": "pipeline_failure_rate_high",
                                            "condition": "pipeline_success_rate < 0.85",
                                            "severity": "error"
                                        },
                                        {
                                            "name": "resource_usage_high",
                                            "condition": "resource_usage > 90%",
                                            "severity": "warning"
                                        }
                                    ],
                                    "logs": [
                                        "pipeline_started",
                                        "pipeline_completed",
                                        "escalation_triggered",
                                        "resource_limit_approached"
                                    ]
                                },
                                "devops": {
                                    "deployment": {
                                        "environment": "production",
                                        "replicas": 1,
                                        "resources": {
                                            "cpu": "2000m",
                                            "memory": "4Gi"
                                        }
                                    },
                                    "monitoring": {
                                        "prometheus_metrics": True,
                                        "grafana_dashboard": "orchestration-pattern",
                                        "health_check_endpoint": "/health/orchestration"
                                    }
                                }
                            }
                        
                        # Display the configuration in both JSON and YAML formats
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**JSON Configuration**")
                            st.code(json.dumps(config, indent=2), language="json")
                        
                        with col2:
                            st.markdown("**YAML Configuration**")
                            yaml_config = yaml.dump(config, default_flow_style=False, indent=2)
                            st.code(yaml_config, language="yaml")
                        
                        # DevOps Pipeline Integration
                        st.markdown("**DevOps Pipeline Integration**")
                        st.markdown("""
                        This configuration can be integrated into your DevOps pipeline for:
                        - **Deployment**: Kubernetes manifests, Docker configurations
                        - **Monitoring**: Prometheus metrics, Grafana dashboards
                        - **Alerting**: AlertManager rules, notification channels
                        - **Logging**: Structured logging, log aggregation
                        - **Security**: RBAC policies, network policies
                        """)
                        
                        # Download buttons
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.download_button(
                                label="Download JSON",
                                data=json.dumps(config, indent=2),
                                file_name=f"{pattern_name}_pattern_config.json",
                                mime="application/json"
                            )
                        with col2:
                            st.download_button(
                                label="Download YAML",
                                data=yaml.dump(config, default_flow_style=False, indent=2),
                                file_name=f"{pattern_name}_pattern_config.yaml",
                                mime="text/yaml"
                            )
                        with col3:
                            st.download_button(
                                label="Download K8s Manifest",
                                data=generate_k8s_manifest(config),
                                file_name=f"{pattern_name}_pattern_k8s.yaml",
                                mime="text/yaml"
                            )
        
        # Meta-Policies section
        st.markdown("---")
        st.markdown("### Meta-Policies (apply to all patterns)")
        meta_policies = [
            "**Auditability**: Every decision, reflection, or critique must be logged.",
            "**Safety**: Hard caps on recursion, scenario count, and tool retries.",
            "**Governance**: All patterns must comply with enterprise risk and compliance frameworks.",
            "**Transparency**: Outputs, plans, and critiques must be human-readable and inspectable."
        ]
        
        for policy in meta_policies:
            st.markdown(f"• {policy}")
    
    with main_tab2:
        # Tools Layer Tab
        st.markdown("### Tools Layer")
        st.markdown("""
        **The tooling ecosystem that enables agentic AI**-the "muscles and nervous system" that let agents reason, act, and integrate with enterprise environments.
        """)
        
        # Create expandable sections for each tool category
        tool_categories = [
            {
                "name": "Large Language Models (LLMs)",
                "role": "Core reasoning and generation engine",
                "examples": ["GPTâ€‘4/5", "Claude", "Gemini", "LLaMA", "Mistral"],
                "agentic_use": "Planning, reflection, orchestration, dialogue management",
                "enterprise_note": "Often wrapped with governance layers (guardrails, policyâ€‘asâ€‘code, audit logging)",
                "pattern_scenarios": [
                    {
                        "pattern": "Reflection",
                        "scenario": "Financial Document Review Agent",
                        "description": "LLM + Reflection pattern for self-evaluating loan application reviews",
                        "implementation": "GPT-4 analyzes loan docs → Self-evaluates decision confidence → Iteratively refines reasoning → Final recommendation",
                        "tools_combination": "GPT-4 + Azure AI Content Safety + Audit Logger",
                        "business_value": "Reduces loan approval errors by 40%, ensures regulatory compliance"
                    },
                    {
                        "pattern": "Planning",
                        "scenario": "Supply Chain Optimization Agent",
                        "description": "LLM + Planning pattern for complex logistics coordination",
                        "implementation": "Claude breaks down delivery optimization → Creates multi-step execution plan → Monitors progress → Adjusts dynamically",
                        "tools_combination": "Claude-3-Sonnet + Temporal Workflow + PostgreSQL",
                        "business_value": "Optimizes delivery routes, reduces costs by 25%, improves customer satisfaction"
                    },
                    {
                        "pattern": "Orchestration",
                        "scenario": "Customer Service Hub Agent",
                        "description": "LLM + Orchestration pattern for managing multi-channel customer interactions",
                        "implementation": "GPT-4 coordinates chat, email, phone agents → Routes complex queries → Manages escalation workflows",
                        "tools_combination": "GPT-4 + LangGraph + RabbitMQ + Prometheus",
                        "business_value": "Unified customer experience, 60% faster resolution times"
                    }
                ]
            },
            {
                "name": "Embeddings & Vector Databases",
                "role": "Store and retrieve semantic representations of text, images, or structured data",
                "examples": [
                    "**Embeddings APIs:** OpenAI, Azure OpenAI, Hugging Face, Cohere",
                    "**Vector DBs:** Pinecone, Weaviate, Qdrant, Milvus, Chroma",
                    "**Integrated Vector DBs:** Azure SQL, PostgreSQL with pgvector, Snowflake Cortex"
                ],
                "agentic_use": "Retrievalâ€‘Augmented Generation (RAG), semantic search, contextual grounding",
                "enterprise_note": "Integrated vector DBs are gaining traction because they combine structured + unstructured data in one governed environment",
                "pattern_scenarios": [
                    {
                        "pattern": "Memory & Learning",
                        "scenario": "Knowledge Management Agent",
                        "description": "Vector DB + Memory pattern for enterprise knowledge discovery",
                        "implementation": "Pinecone stores company docs → Agent learns from interactions → Builds knowledge graph → Improves search accuracy",
                        "tools_combination": "Pinecone + text-embedding-ada-002 + Azure Cognitive Search + Redis",
                        "business_value": "90% faster knowledge discovery, reduces duplicate work by 50%"
                    },
                    {
                        "pattern": "Tool Use",
                        "scenario": "Legal Document Research Agent",
                        "description": "Vector DB + Tool Use pattern for legal precedent research",
                        "implementation": "Weaviate stores case law → Agent retrieves relevant precedents → Validates against current law → Generates legal briefs",
                        "tools_combination": "Weaviate + Cohere Embeddings + Legal API + Document Generator",
                        "business_value": "Accelerates legal research by 70%, improves case preparation accuracy"
                    },
                    {
                        "pattern": "Exploration",
                        "scenario": "Market Research Agent",
                        "description": "Vector DB + Exploration pattern for competitive analysis",
                        "implementation": "Chroma stores market data → Agent explores multiple scenarios → Simulates competitor responses → Recommends strategies",
                        "tools_combination": "Chroma + Hugging Face Embeddings + Simulation Engine + Analytics API",
                        "business_value": "Identifies market opportunities 3x faster, improves strategic decision making"
                    }
                ]
            },
            {
                "name": "MCPs (Model Context Protocols) & Connectors",
                "role": "Standardize how agents talk to external systems (databases, APIs, SaaS apps)",
                "examples": [
                    "**LangChain / LangGraph** connectors",
                    "**Model Context Protocol (MCP):** emerging standard for connecting LLMs to tools and data sources",
                    "**Snowflake Cortex MCPs:** allow direct querying of Snowflake with embeddings + SQL"
                ],
                "agentic_use": "Agents can query enterprise data warehouses (Snowflake, BigQuery, Databricks) without brittle prompt hacks",
                "enterprise_note": "MCPs are critical for **auditability**-you can log every query and enforce RBAC",
                "pattern_scenarios": [
                    {
                        "pattern": "Tool Use",
                        "scenario": "Financial Reporting Agent",
                        "description": "MCP + Tool Use pattern for automated financial data analysis",
                        "implementation": "Snowflake Cortex MCP → Agent queries financial data → Validates against regulations → Generates compliance reports",
                        "tools_combination": "Snowflake Cortex MCP + LangChain + Audit Logger + Report Generator",
                        "business_value": "Automates 80% of financial reporting, ensures regulatory compliance"
                    },
                    {
                        "pattern": "Collaboration",
                        "scenario": "Cross-Department Data Agent",
                        "description": "MCP + Collaboration pattern for inter-departmental data sharing",
                        "implementation": "LangGraph coordinates multiple MCPs → HR, Finance, Operations agents collaborate → Share insights securely",
                        "tools_combination": "LangGraph + Multiple MCPs + RBAC System + Data Lineage Tracker",
                        "business_value": "Breaks down data silos, enables cross-functional insights"
                    },
                    {
                        "pattern": "Orchestration",
                        "scenario": "Enterprise Data Pipeline Agent",
                        "description": "MCP + Orchestration pattern for complex data workflows",
                        "implementation": "Agent orchestrates data extraction → Transformation via MCPs → Loading to multiple systems → Quality validation",
                        "tools_combination": "Temporal + Multiple MCPs + Data Quality Validator + Monitoring Dashboard",
                        "business_value": "Reduces data pipeline failures by 90%, improves data quality"
                    }
                ]
            },
            {
                "name": "API Catalogs & Tool Registries",
                "role": "Curated catalogs of APIs/tools that agents can call",
                "examples": [
                    "**OpenAPI / Swagger specs** as machineâ€‘readable contracts",
                    "**Enterprise API gateways** (Apigee, Kong, Azure API Management)",
                    "**LangChain toolkits** or **AI Gateway catalogs**"
                ],
                "agentic_use": "Agents discover and invoke APIs dynamically (e.g., \"fetch customer profile,\" \"submit compliance form\")",
                "enterprise_note": "Policies can enforce **leastâ€‘privilege tool use** and **schema validation** before execution",
                "pattern_scenarios": [
                    {
                        "pattern": "Tool Use",
                        "scenario": "Customer Onboarding Agent",
                        "description": "API Catalog + Tool Use pattern for automated customer setup",
                        "implementation": "Agent discovers onboarding APIs → Validates customer data → Calls CRM, billing, support APIs → Tracks progress",
                        "tools_combination": "API Gateway + OpenAPI Registry + Validation Service + Progress Tracker",
                        "business_value": "Reduces onboarding time by 75%, improves customer experience"
                    },
                    {
                        "pattern": "Planning",
                        "scenario": "IT Operations Agent",
                        "description": "API Catalog + Planning pattern for infrastructure management",
                        "implementation": "Agent plans infrastructure changes → Discovers relevant APIs → Executes deployment plan → Monitors results",
                        "tools_combination": "Kong API Gateway + Kubernetes API + Monitoring APIs + Rollback Service",
                        "business_value": "Automates 60% of IT operations, reduces deployment errors"
                    },
                    {
                        "pattern": "Reflection",
                        "scenario": "API Performance Agent",
                        "description": "API Catalog + Reflection pattern for API optimization",
                        "implementation": "Agent monitors API performance → Self-evaluates optimization opportunities → Adjusts API calls → Measures improvements",
                        "tools_combination": "API Gateway + Performance Monitoring + A/B Testing Framework + Analytics",
                        "business_value": "Improves API response times by 40%, reduces costs by 30%"
                    }
                ]
            },
            {
                "name": "Traditional Databases & Data Lakes",
                "role": "Source of truth for structured enterprise data",
                "examples": ["Snowflake", "Databricks", "BigQuery", "Azure Synapse", "Postgres", "SQL Server"],
                "agentic_use": "Agents query structured data directly (SQL generation + validation)",
                "enterprise_note": "Often paired with embeddings for hybrid search (structured filters + semantic retrieval)",
                "pattern_scenarios": [
                    {
                        "pattern": "Memory & Learning",
                        "scenario": "Customer Analytics Agent",
                        "description": "Data Lake + Memory pattern for customer behavior analysis",
                        "implementation": "Databricks stores customer data → Agent learns patterns → Builds customer profiles → Predicts behavior",
                        "tools_combination": "Databricks + MLflow + Customer Profile DB + Prediction API",
                        "business_value": "Increases customer retention by 35%, improves personalization"
                    },
                    {
                        "pattern": "Exploration",
                        "scenario": "Risk Assessment Agent",
                        "description": "Data Warehouse + Exploration pattern for financial risk analysis",
                        "implementation": "BigQuery stores financial data → Agent explores risk scenarios → Simulates market conditions → Recommends strategies",
                        "tools_combination": "BigQuery + Risk Simulation Engine + Scenario Generator + Decision Support",
                        "business_value": "Reduces financial risk exposure by 50%, improves decision accuracy"
                    },
                    {
                        "pattern": "Critic/Reviewer \U0001F9D0",
                        "scenario": "Data Quality Agent",
                        "description": "Database + Critic pattern for data validation and quality assurance",
                        "implementation": "PostgreSQL stores business data → Agent validates data quality → Reviews anomalies → Recommends corrections",
                        "tools_combination": "PostgreSQL + Data Quality Rules + Anomaly Detection + Correction Workflow",
                        "business_value": "Improves data quality by 85%, reduces downstream errors"
                    }
                ]
            },
            {
                "name": "Governance & Guardrail Layers",
                "role": "Ensure safe, compliant, and auditable agent behavior",
                "examples": [
                    "**Guardrails.ai**, **Azure AI Content Safety**, **policyâ€‘asâ€‘code frameworks**",
                    "**Prompt injection filters**, **output validators**, **critics/reviewers**"
                ],
                "agentic_use": "Wraps every tool call and LLM output with validation",
                "enterprise_note": "This is where your **pattern cards + explicit rules** plug in",
                "pattern_scenarios": [
                    {
                        "pattern": "Critic/Reviewer \U0001F9D0",
                        "scenario": "Compliance Monitoring Agent",
                        "description": "Guardrails + Critic pattern for regulatory compliance checking",
                        "implementation": "Agent processes business decisions → Guardrails validate compliance → Critic reviews for violations → Escalates issues",
                        "tools_combination": "Guardrails.ai + Compliance Rules Engine + Audit Logger + Escalation System",
                        "business_value": "Ensures 100% regulatory compliance, reduces audit findings by 90%"
                    },
                    {
                        "pattern": "Reflection",
                        "scenario": "Content Moderation Agent",
                        "description": "Content Safety + Reflection pattern for social media moderation",
                        "implementation": "Agent reviews user content → Self-evaluates moderation decisions → Reflects on accuracy → Improves over time",
                        "tools_combination": "Azure AI Content Safety + Reflection Engine + Feedback Loop + Learning System",
                        "business_value": "Improves moderation accuracy by 60%, reduces false positives"
                    },
                    {
                        "pattern": "Orchestration",
                        "scenario": "Enterprise Security Agent",
                        "description": "Policy Engine + Orchestration pattern for security monitoring",
                        "implementation": "Agent orchestrates security checks → Applies policy rules → Coordinates responses → Manages incident workflows",
                        "tools_combination": "Policy-as-Code + Security APIs + Incident Management + Response Automation",
                        "business_value": "Reduces security incidents by 70%, improves response times"
                    }
                ]
            }
        ]
        
        # Display tool categories
        for category in tool_categories:
            with st.expander(f"{category['name']}", expanded=False):
                st.markdown(f"**Role:** {category['role']}")
                
                st.markdown("**Examples:**")
                for example in category['examples']:
                    st.markdown(f"• {example}")
                
                st.markdown(f"**Agentic Use:** {category['agentic_use']}")
                st.markdown(f"**Enterprise Note:** {category['enterprise_note']}")
                
                # Pattern Scenarios Section
                st.markdown("---")
                st.markdown("### Pattern-Tool Scenarios")
                st.markdown("**Real-world scenarios where this tool category combines with agentic patterns to build effective agents:**")
                
                for scenario in category['pattern_scenarios']:
                    with st.expander(f"{scenario['pattern']} - {scenario['scenario']}", expanded=False):
                        st.markdown(f"**Description:** {scenario['description']}")
                        st.markdown(f"**Implementation Flow:** {scenario['implementation']}")
                        st.markdown(f"**Tools Combination:** {scenario['tools_combination']}")
                        st.markdown(f"**Business Value:** {scenario['business_value']}")
        
        # Agentic AI Stack Overview
        st.markdown("---")
        st.markdown("### âš¡ Agentic AI Stack Overview")
        st.markdown("""
        An **agentic AI stack** typically looks like this:
        """)
        
        stack_steps = [
            "**LLM** (reasoning, planning, reflection)",
            "**Embeddings + Vector DB** (contextual memory, semantic grounding)",
            "**MCPs / Connectors** (bridge to enterprise systems like Snowflake)",
            "**API Catalog** (discoverable, governed toolset)",
            "**Databases / Data Lakes** (structured + unstructured enterprise data)",
            "**Governance Layer** (policies, critics, audit logs, compliance)"
        ]
        
        for i, step in enumerate(stack_steps, 1):
            st.markdown(f"{i}. {step}")
        
        # Pattern-to-Tool Mapping
        st.markdown("---")
        st.markdown("### Pattern-to-Tool Mapping")
        st.markdown("""
        **How each agentic pattern maps to specific tools and real-world applications:**
        """)
        
        pattern_tool_mapping = [
            {
                "pattern": "Reflection",
                "primary_tools": "LLM + Critic Agent + Logging DB",
                "scenarios": [
                    "Financial Document Review (GPT-4 + Azure AI Content Safety)",
                    "Code Quality Assurance (Claude + SonarQube + Git)",
                    "Medical Diagnosis Validation (Gemini + Medical Knowledge Base)"
                ],
                "enterprise_benefits": "Self-improving systems, reduced human oversight, higher accuracy"
            },
            {
                "pattern": "Planning",
                "primary_tools": "LLM + Orchestration Layer + Workflow Engine",
                "scenarios": [
                    "Supply Chain Optimization (Claude + Temporal + PostgreSQL)",
                    "Project Management (GPT-4 + Jira API + Slack)",
                    "Resource Allocation (Gemini + Kubernetes + Monitoring)"
                ],
                "enterprise_benefits": "Complex task breakdown, dynamic adaptation, resource optimization"
            },
            {
                "pattern": "Tool Use",
                "primary_tools": "API Catalog + MCPs + Validation Layer",
                "scenarios": [
                    "Customer Onboarding (API Gateway + CRM + Billing Systems)",
                    "Legal Research (Legal APIs + Document DB + Citation Tools)",
                    "IT Operations (Kubernetes API + Monitoring + Alerting)"
                ],
                "enterprise_benefits": "Seamless system integration, automated workflows, reduced manual work"
            },
            {
                "pattern": "Memory & Learning",
                "primary_tools": "Vector DBs + Embeddings + Persistent Storage",
                "scenarios": [
                    "Knowledge Management (Pinecone + OpenAI Embeddings + Redis)",
                    "Customer Analytics (Databricks + MLflow + Profile DB)",
                    "Document Intelligence (Weaviate + Azure Cognitive Search)"
                ],
                "enterprise_benefits": "Continuous learning, personalized experiences, knowledge retention"
            },
            {
                "pattern": "Collaboration",
                "primary_tools": "Message Queues + Coordination Protocols + Shared State",
                "scenarios": [
                    "Cross-Department Coordination (LangGraph + MCPs + RBAC)",
                    "Multi-Agent Workflows (RabbitMQ + Shared State + Monitoring)",
                    "Distributed Processing (Apache Kafka + Coordination Layer)"
                ],
                "enterprise_benefits": "Scalable teamwork, distributed intelligence, coordinated decision-making"
            },
            {
                "pattern": "Critic/Reviewer \U0001F9D0",
                "primary_tools": "Evaluation Frameworks + Audit Logs + Compliance Tools",
                "scenarios": [
                    "Compliance Monitoring (Guardrails.ai + Audit Logger + Escalation)",
                    "Content Moderation (Azure AI Content Safety + Feedback Loop)",
                    "Quality Assurance (Evaluation Rubrics + Review Workflows)"
                ],
                "enterprise_benefits": "Quality control, regulatory compliance, risk mitigation"
            },
            {
                "pattern": "Exploration",
                "primary_tools": "Simulation Engines + Scenario Generators + Analytics",
                "scenarios": [
                    "Risk Assessment (BigQuery + Simulation Engine + Decision Support)",
                    "Market Research (Chroma + Analytics API + Scenario Generator)",
                    "A/B Testing (Experiment Framework + Analytics + Statistical Tools)"
                ],
                "enterprise_benefits": "Informed decision-making, risk mitigation, strategic planning"
            },
            {
                "pattern": "Orchestration",
                "primary_tools": "Workflow Engines + Monitoring + Resource Management",
                "scenarios": [
                    "Customer Service Hub (GPT-4 + LangGraph + Multi-channel APIs)",
                    "Data Pipeline Management (Temporal + MCPs + Quality Validation)",
                    "Enterprise Security (Policy Engine + Security APIs + Incident Management)"
                ],
                "enterprise_benefits": "End-to-end automation, system coordination, operational efficiency"
            }
        ]
        
        # Display pattern-tool mappings
        for mapping in pattern_tool_mapping:
            with st.expander(f"{mapping['pattern']} - {mapping['primary_tools']}", expanded=False):
                st.markdown(f"**Primary Tools:** {mapping['primary_tools']}")
                
                st.markdown("**Real-World Scenarios:**")
                for scenario in mapping['scenarios']:
                    st.markdown(f"• {scenario}")
                
                st.markdown(f"**Enterprise Benefits:** {mapping['enterprise_benefits']}")
        
        # Implementation Considerations
        st.markdown("---")
        st.markdown("### Implementation Considerations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Key Integration Points:**")
            st.markdown("• **Governance Integration**: Pattern rules map to guardrail policies")
            st.markdown("• **Audit Trail**: Every tool call logged with pattern context")
            st.markdown("• **Policy Enforcement**: Pattern-specific validation rules")
            st.markdown("• **Resource Management**: Pattern-based resource allocation")
        
        with col2:
            st.markdown("**Enterprise Requirements:**")
            st.markdown("• **RBAC Integration**: Role-based access to tools")
            st.markdown("• **Compliance Monitoring**: Pattern adherence tracking")
            st.markdown("• **Performance Metrics**: Tool usage and pattern effectiveness")
            st.markdown("• **Scalability**: Pattern-based horizontal scaling")
    
    with main_tab3:
        # Display agent cards
        st.markdown("### Agent Cards")
        
        # Display all agent cards without pagination
        agents_to_show = filtered_agents
        
        cols = st.columns(2)
        for i, agent in enumerate(agents_to_show):
            with cols[i % 2]:
                status_info = get_status_badge(agent['status'])
                pattern_type_emoji = {
                    'retrieval': '',
                    'orchestration': '',
                    'monitoring': '',
                    'reasoning': '',
                    'classification': '',
                    'supervision': ''
                }.get(agent['patternType'], '')
                
                # Create expandable agent card
                with st.expander(f"{pattern_type_emoji} {agent['name']} - {status_info['text']}", expanded=False):
                    # Agent Overview tab
                    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Agent Overview", "Pattern", "Tools", "Policies", "Runtime"])
                    
                    with tab1:
                        # General Info
                        st.markdown("### General Information")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**Agent ID:** `{agent['id']}`")
                            st.markdown(f"**Agent Name:** {agent['name']}")
                            st.markdown(f"**Pattern Type:** {agent['patternType'].title()}")
                            st.markdown(f"**Version:** v1.0")
                        with col2:
                            st.markdown(f"**Owner:** {agent['owner']}")
                            st.markdown(f"**Lifecycle State:** {agent['lifecycle']}")
                            st.markdown(f"**Last Updated:** 2025-09-24")
                            st.markdown(f"**Business Use Case:** {agent['businessUseCase']}")
                        
                        # Capabilities
                        st.markdown("### Capabilities")
                        for capability in agent['capabilities']:
                            st.write(f"• {capability}")
                        
                        # Dependencies
                        st.markdown("### Dependencies")
                        deps = agent['dependencies']
                        col1, col2 = st.columns(2)
                        with col1:
                            if 'llm' in deps:
                                st.write(f"**LLM:** {deps['llm']}")
                            if 'anomalyModel' in deps:
                                st.write(f"**Models:** {deps['anomalyModel']}")
                        with col2:
                            if 'complianceAPI' in deps:
                                st.write(f"**APIs:** {deps['complianceAPI']}")
                            if 'paymentAPI' in deps:
                                st.write(f"**APIs:** {deps['paymentAPI']}")
                        
                        # Risk and Compliance
                        st.markdown("### Risk and Compliance")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**Risk Level:** {agent['risk']}")
                            compliance_tags = agent['governanceHooks']['complianceTags']
                            st.markdown("**Compliance Tags:**")
                            for tag, status in compliance_tags.items():
                                if status:
                                    st.success(f"{tag.upper()}")
                                else:
                                    st.error(f"{tag.upper()}")
                        with col2:
                            st.markdown("**Human-in-the-Loop:**")
                            if agent['risk'] == 'High':
                                st.write("Mandatory for > $100K")
                            elif agent['risk'] == 'Medium':
                                st.write("Required for escalations")
                            else:
                                st.write("Optional")
                        
                        # Key Metrics
                        st.markdown("### Key Metrics (30-day rolling)")
                        monitoring = agent['monitoring']
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Transactions", monitoring['callsThisWeek'])
                        with col2:
                            st.metric("Escalations", monitoring['escalations'])
                        with col3:
                            st.metric("Guardrail Triggers", monitoring['guardrailTriggers'])
                        with col4:
                            st.metric("Avg Anomaly Score", "0.42" if agent['id'] == 'payment-processor-v1' else "0.15")
                        
                        # Related Agents
                        st.markdown("### Related Agents")
                        related_agents = {
                            'payment-processor-v1': ['Retriever Agent v1', 'Compliance Monitor v1'],
                            'retriever-v1': ['Document Classifier v1', 'AI Supervisor v1'],
                            'orchestrator-v2': ['Payment Processor v1', 'AI Supervisor v1'],
                            'compliance-v1': ['Payment Processor v1', 'Document Classifier v1'],
                            'negotiator-v1': ['AI Supervisor v1', 'Compliance Monitor v1'],
                            'classifier-v1': ['Retriever Agent v1', 'Compliance Monitor v1'],
                            'supervisor-v1': ['Payment Processor v1', 'Retriever Agent v1', 'Document Classifier v1']
                        }
                        for related in related_agents.get(agent['id'], []):
                            st.write(f"• {related}")
                    
                    with tab2:
                        # Pattern Implementations
                        if 'patternImplementations' in agent:
                            st.markdown("**Agentic Pattern Implementations**")
                            
                            # Primary Patterns
                            st.markdown("**Primary Patterns:**")
                            for pattern in agent['patternImplementations']['primary_patterns']:
                                st.success(f"{pattern}")
                            
                            # Secondary Patterns
                            st.markdown("**Secondary Patterns:**")
                            for pattern in agent['patternImplementations']['secondary_patterns']:
                                st.info(f"{pattern}")
                            
                            # Pattern Details
                            st.markdown("**Pattern Implementation Details:**")
                            for pattern_name, details in agent['patternImplementations']['pattern_details'].items():
                                with st.expander(f"{pattern_name} - Implementation Details", expanded=False):
                                    st.markdown(f"**Implementation:** {details['implementation']}")
                                    
                                    if 'tools_used' in details:
                                        st.markdown("**Tools Used:**")
                                        for tool in details['tools_used']:
                                            st.write(f"• {tool}")
                                    
                                    if 'memory_type' in details:
                                        st.markdown(f"**Memory Type:** {details['memory_type']}")
                                    
                                    if 'learning_mechanism' in details:
                                        st.markdown(f"**Learning Mechanism:** {details['learning_mechanism']}")
                                    
                                    if 'critic_role' in details:
                                        st.markdown(f"**Critic Role:** {details['critic_role']}")
                                    
                                    if 'decision_authority' in details:
                                        st.markdown(f"**Decision Authority:** {details['decision_authority']}")
                                    
                                    if 'coordination_scope' in details:
                                        st.markdown(f"**Coordination Scope:** {details['coordination_scope']}")
                                    
                                    if 'planning_depth' in details:
                                        st.markdown(f"**Planning Depth:** {details['planning_depth']}")
                                    
                                    if 'scenario_testing' in details:
                                        st.markdown(f"**Scenario Testing:** {details['scenario_testing']}")
                                    
                                    if 'reflection_criteria' in details:
                                        st.markdown("**Reflection Criteria:**")
                                        for criteria in details['reflection_criteria']:
                                            st.write(f"• {criteria}")
                                    
                                    if 'delegation_protocol' in details:
                                        st.markdown(f"**Delegation Protocol:** {details['delegation_protocol']}")
                                    
                                    if 'conflict_resolution' in details:
                                        st.markdown(f"**Conflict Resolution:** {details['conflict_resolution']}")
                                    
                                    # Configuration
                                    if 'configuration' in details:
                                        st.markdown("**Configuration:**")
                                        config_json = json.dumps(details['configuration'], indent=2)
                                        st.code(config_json, language='json')
                        else:
                            st.markdown("**Governance Policies:**")
                            st.code(agent['governanceHooks']['policies'], language='yaml')
                            
                            st.markdown("**Compliance Status:**")
                            compliance_tags = agent['governanceHooks']['complianceTags']
                            for tag, status in compliance_tags.items():
                                if status:
                                    st.success(f"{tag}")
                                else:
                                    st.error(f"{tag}")
                            
                            st.markdown("**Approval History:**")
                            st.write(" → ".join(agent['governanceHooks']['approvalHistory']))
                    
                    with tab3:
                        # Codified Policies & Runtime Tools
                        st.markdown("**Codified Policies & Runtime Tools**")
                        
                        # Policy Codification Section
                        st.markdown("#### Codified Policies (YAML/JSON)")
                        
                        # Generate codified policies
                        codified_policies = generate_codified_policies(agent)
                        
                        # Display policy tabs
                        policy_tabs = st.tabs(["YAML Format", "JSON Format", "Runtime Observation", "Policy Validation"])
                        
                        with policy_tabs[0]:
                            st.markdown("**YAML Configuration:**")
                            st.code(codified_policies['yaml'], language='yaml')
                            
                            # Download button for YAML
                            st.download_button(
                                label="Download YAML",
                                data=codified_policies['yaml'],
                                file_name=f"{agent['id']}_policies.yaml",
                                mime="text/yaml"
                            )
                        
                        with policy_tabs[1]:
                            st.markdown("**JSON Configuration:**")
                            st.code(codified_policies['json'], language='json')
                            
                            # Download button for JSON
                            st.download_button(
                                label="Download JSON",
                                data=codified_policies['json'],
                                file_name=f"{agent['id']}_policies.json",
                                mime="application/json"
                            )
                        
                        with policy_tabs[2]:
                            st.markdown("**Runtime Policy Observation**")
                            
                            # Policy compliance status
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Policy Compliance", f"{codified_policies['compliance_rate']}%", 
                                         delta=f"{codified_policies['compliance_trend']}%")
                            with col2:
                                st.metric("Active Policies", codified_policies['active_policies'])
                            with col3:
                                st.metric("Violations (24h)", codified_policies['violations_24h'])
                            
                            # Policy execution log
                            st.markdown("**Recent Policy Executions:**")
                            for execution in codified_policies['execution_log']:
                                status_icon = "" if execution['status'] == 'compliant' else "" if execution['status'] == 'warning' else ""
                                st.markdown(f"{status_icon} **{execution['policy']}** - {execution['timestamp']} ({execution['status']})")
                                if execution['details']:
                                    st.markdown(f"   *{execution['details']}*")
                        
                        with policy_tabs[3]:
                            st.markdown("**Policy Validation & Testing**")
                            
                            # Policy validation results
                            st.markdown("**Validation Results:**")
                            for validation in codified_policies['validation_results']:
                                status_icon = "" if validation['valid'] else ""
                                st.markdown(f"{status_icon} **{validation['policy_name']}**: {validation['message']}")
                            
                            # Test policy button
                            if st.button("Test Policy Execution", key=f"test_policy_{agent['id']}"):
                                st.success("Policy test executed successfully!")
                                st.info("Check the Runtime Observation tab for results.")
                        
                        st.markdown("---")
                        
                        # Runtime Tools Section
                        st.markdown("#### Runtime Tools")
                        if 'runtime_tools' in agent:
                            # Display tools by category
                            for category, tools in agent['runtime_tools'].items():
                                category_name = category.replace('_', ' ').title()
                                st.markdown(f"**{category_name}:**")
                                
                                for tool in tools:
                                    status_color = "" if tool['status'] == 'active' else "" if tool['status'] == 'inactive' else ""
                                    st.markdown(f"• {status_color} **{tool['name']}** - {tool['purpose']}")
                                
                                st.markdown("")  # Add spacing between categories
                        else:
                            st.markdown("**No runtime tools configured**")
                    
                    with tab4:
                        st.markdown("**Input Filters:**")
                        for filter_type in agent['runtimeGuardrails']['inputFilters']:
                            st.write(f"• {filter_type}")
                        
                        st.markdown("**Output Validators:**")
                        for validator in agent['runtimeGuardrails']['outputValidators']:
                            st.write(f"• {validator}")
                        
                        st.markdown("**Rate Controls:**")
                        rate_controls = agent['runtimeGuardrails']['rateControls']
                        for control, value in rate_controls.items():
                            st.write(f"• {control.replace('_', ' ').title()}: {value}")
                        
                        st.markdown("**Kill Switch:**")
                        kill_switch = agent['runtimeGuardrails']['killSwitch']
                        st.write(f"Enabled: {'Yes' if kill_switch['enabled'] else 'No'}")
                        for trigger in kill_switch['triggers']:
                            st.write(f"• {trigger}")
                        
                        st.markdown("**Monitoring:**")
                        monitoring = agent['monitoring']
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Calls This Week", monitoring['callsThisWeek'])
                            st.metric("Uptime", monitoring['uptime'])
                    with col2:
                        st.metric("Guardrail Triggers", monitoring['guardrailTriggers'])
                        st.metric("Escalations", monitoring['escalations'])
                
                with tab4:
                    st.markdown("**Escalation Levels:**")
                    for level in agent['escalationMechanisms']['tieredEscalation']:
                        if level['status'] == 'success':
                            st.success(f"Level {level['level']}: {level['action']}")
                        elif level['status'] == 'pending':
                            st.warning(f"Level {level['level']}: {level['action']} â³")
                        else:
                            st.info(f"Level {level['level']}: {level['action']}")
                        st.write(f"*Timeout: {level['timeout']}*")
                        st.write("---")
                    
                    st.markdown("**Notification Channels:**")
                    for channel in agent['escalationMechanisms']['notificationChannels']:
                        st.write(f"• {channel}")
                    
                    st.markdown("**Decision Journals:**")
                    decision_journals = agent['escalationMechanisms']['decisionJournals']
                    st.write(f"Enabled: {'Yes' if decision_journals['enabled'] else 'No'}")
                    st.write(f"Required: {'Yes' if decision_journals['required'] else 'No'}")
                    st.write(f"Template: {decision_journals['template']}")
                
                with tab5:
                    st.markdown("### Escalation Analysis (100+ Iterations)")
                    
                    # Generate comprehensive escalation data based on agent type
                    escalation_data = generate_escalation_data(agent)
                    
                    # Key Metrics
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Escalations", escalation_data['total_escalations'])
                    with col2:
                        st.metric("Avg Resolution Time", escalation_data['avg_resolution_time'])
                    with col3:
                        st.metric("Success Rate", f"{escalation_data['success_rate']}%")
                    with col4:
                        st.metric("Critical Issues", escalation_data['critical_issues'])
                    
                    # Escalation Trends Chart
                    st.markdown("#### Escalation Trends (Last 30 Days)")
                    
                    # Generate trend data
                    dates = pd.date_range('2025-01-01', periods=30, freq='D')
                    trend_data = {
                        'Date': dates,
                        'Escalations': np.random.poisson(escalation_data['daily_avg'], 30),
                        'Resolved': np.random.poisson(escalation_data['daily_avg'] * 0.85, 30)
                    }
                    trend_df = pd.DataFrame(trend_data)
                    
                    fig_trend = px.line(trend_df, x='Date', y=['Escalations', 'Resolved'], 
                                      title='Daily Escalation Volume',
                                      color_discrete_map={'Escalations': '#ff6b6b', 'Resolved': '#51cf66'})
                    fig_trend.update_layout(height=300, showlegend=True)
                    st.plotly_chart(fig_trend, use_container_width=True)
                    
                    # Escalation Logs
                    st.markdown("#### Recent Escalation Logs")
                    
                    # Create expandable sections for different log types
                    log_tabs = st.tabs(["Recent Events", "Critical Issues", "Pattern Analysis", "Resolution Insights"])
                    
                    with log_tabs[0]:
                        st.markdown("**Last 20 Escalation Events:**")
                        for i, event in enumerate(escalation_data['recent_events']):
                            severity_color = "" if event['severity'] == 'Critical' else "" if event['severity'] == 'High' else "" if event['severity'] == 'Medium' else ""
                            status_icon = "" if event['status'] == 'Resolved' else "" if event['status'] == 'Investigating' else "" if event['status'] == 'Pending' else ""
                            
                            with st.expander(f"{severity_color} {event['timestamp']} - {event['type']} {status_icon}", expanded=False):
                                st.markdown(f"**Description:** {event['description']}")
                                st.markdown(f"**Impact:** {event['impact']}")
                                st.markdown(f"**Resolution:** {event['resolution']}")
                                st.markdown(f"**Duration:** {event['duration']}")
                                if event['lessons_learned']:
                                    st.markdown(f"**Lessons Learned:** {event['lessons_learned']}")
                    
                    with log_tabs[1]:
                        st.markdown("**Critical Issues Requiring Attention:**")
                        for issue in escalation_data['critical_issues_list']:
                            with st.expander(f"{issue['title']}", expanded=False):
                                st.markdown(f"**Root Cause:** {issue['root_cause']}")
                                st.markdown(f"**Business Impact:** {issue['business_impact']}")
                                st.markdown(f"**Recommended Actions:**")
                                for action in issue['recommended_actions']:
                                    st.markdown(f"• {action}")
                                st.markdown(f"**Priority:** {issue['priority']}")
                    
                    with log_tabs[2]:
                        st.markdown("**Escalation Pattern Analysis:**")
                        
                        # Pattern analysis chart
                        pattern_data = escalation_data['pattern_analysis']
                    fig_pattern = px.pie(values=list(pattern_data.values()), 
                                           names=list(pattern_data.keys()),
                                           title='Escalation Types Distribution')
                    fig_pattern.update_layout(height=400)
                    st.plotly_chart(fig_pattern, use_container_width=True, key=f"pattern_chart_runtime_{agent['id']}")
                    
                    st.markdown("**Key Patterns Identified:**")
                    for pattern in escalation_data['patterns_identified']:
                        st.markdown(f"• **{pattern['pattern']}**: {pattern['description']} (Frequency: {pattern['frequency']}%)")
                    
                    with log_tabs[3]:
                        st.markdown("**Resolution Insights & Recommendations:**")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("**Top Resolution Strategies:**")
                            for strategy in escalation_data['resolution_strategies']:
                                st.markdown(f"• **{strategy['strategy']}**: {strategy['effectiveness']}% success rate")
                        
                        with col2:
                            st.markdown("**Prevention Measures:**")
                            for measure in escalation_data['prevention_measures']:
                                st.markdown(f"• {measure}")
                        
                        st.markdown("**Performance Improvements:**")
                        for improvement in escalation_data['performance_improvements']:
                            st.markdown(f"• **{improvement['area']}**: {improvement['improvement']} ({improvement['impact']})")
                    
                    # Escalation Configuration
                    st.markdown("#### Escalation Configuration")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Current Thresholds:**")
                        for threshold in escalation_data['thresholds']:
                            st.markdown(f"• **{threshold['metric']}**: {threshold['value']} ({threshold['status']})")
                    
                    with col2:
                        st.markdown("**Escalation Rules:**")
                        for rule in escalation_data['escalation_rules']:
                            st.markdown(f"• {rule}")
                    
                    # Action Items
                    st.markdown("#### Action Items")
                    for item in escalation_data['action_items']:
                        priority_icon = "" if item['priority'] == 'High' else "" if item['priority'] == 'Medium' else ""
                        st.markdown(f"{priority_icon} **{item['title']}** (Due: {item['due_date']})")
                        st.markdown(f"   {item['description']}")
                        st.markdown("")
                    
    
    # Stats
    stats = {
        'total': len(agents),
        'approved': len([a for a in agents if a['status'] == 'approved']),
        'pilot': len([a for a in agents if a['status'] == 'pilot']),
        'draft': len([a for a in agents if a['status'] == 'draft'])
    }
    
    st.markdown(f"**Stats:** {stats['total']} Agents | {stats['approved']} Approved | {stats['pilot']} Pilot | {stats['draft']} Draft")
    
    # Payment workflow access
    st.markdown("---")
    st.markdown("### High-Value Payment Processing Workflow")
    st.markdown("Experience the complete end-to-end payment processing workflow with anomaly detection, governance, and human-in-the-loop review.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Start Payment Workflow", type="primary"):
            st.session_state['current_page'] = 'payment_instruction'
            st.rerun()
    with col2:
        if st.button("View Payment Audit"):
            st.session_state['current_page'] = 'payment_audit'
            st.rerun()
    with col3:
        if st.button("Payment Escalations"):
            st.session_state['current_page'] = 'payment_escalation'
            st.rerun()

def agent_detail_page():
    if 'selected_agent' not in st.session_state:
        st.error("No agent selected")
        return
    
    data = load_agent_data()
    agent = next((a for a in data['agents'] if a['id'] == st.session_state['selected_agent']), None)
    
    if not agent:
        st.error("Agent not found")
        return
    
    status_info = get_status_badge(agent['status'])
    pattern_type_emoji = {
        'retrieval': '',
        'orchestration': '',
        'monitoring': '',
        'reasoning': ''
    }.get(agent['patternType'], '')
    
    st.markdown(f"<h1>{pattern_type_emoji} Agent: {agent['name']} <span class='status-badge {status_info['class']}'>{status_info['text']}</span></h1>", unsafe_allow_html=True)
    st.markdown(f"**Pattern:** {agent['patternName']} ({agent['patternType'].title()})")
    
    if st.button("â† Back to Agentic Catalog"):
        del st.session_state['selected_agent']
        st.rerun()
    
    # Header Section
    st.markdown("---")
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(f"### {pattern_type_emoji} {agent['name']}")
        st.markdown(f"**Pattern:** {agent['patternName']}")
    with col2:
        st.markdown(f"**Lifecycle:** {agent['lifecycle']}")
    with col3:
        st.markdown(f"**Risk Level:** {agent['risk']}")
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Overview", "Governance", "Runtime", "Escalation", "Audit"])
    
    with tab1:
        st.markdown("### Description")
        st.write(agent['businessUseCase'])
        
        st.markdown("### Business Use Case")
        st.write(f"**Primary Use:** {agent['useCase']}")
        st.write(f"**Owner:** {agent['owner']}")
        
        st.markdown("### Dependencies")
        dep_cols = st.columns(2)
        for i, (dep_type, dep_name) in enumerate(agent['dependencies'].items()):
            with dep_cols[i % 2]:
                st.markdown(f"**{dep_type.replace('_', ' ').title()}:** {dep_name}")
        
        st.markdown("### Capabilities")
        for capability in agent['capabilities']:
            st.write(f"• {capability}")
        
        st.markdown("### Boundaries")
        for boundary in agent['boundaries']:
            st.write(f"• {boundary}")
    
    with tab2:
        st.markdown("### Policies")
        st.code(agent['governanceHooks']['policies'], language='yaml')
        
        st.markdown("### Compliance Tags")
        compliance_tags = agent['governanceHooks']['complianceTags']
        cols = st.columns(len(compliance_tags))
        for i, (tag, status) in enumerate(compliance_tags.items()):
            with cols[i]:
                if status:
                    st.success(f"{tag}")
                else:
                    st.error(f"{tag}")
        
        st.markdown("### Approval Status")
        approval_history = agent['governanceHooks']['approvalHistory']
        for i, status in enumerate(approval_history):
            if i < len(approval_history) - 1:
                st.write(f"**{status}** →")
            else:
                st.write(f"**{status}**")
        
        st.markdown("### Governance Metrics")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Audit Entries", agent['governanceHooks']['auditLogs']['entries'])
        with col2:
            st.metric("Last Escalation", agent['governanceHooks']['auditLogs']['lastEscalation'])
    
    with tab3:
        st.markdown("### Guardrails")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Input Filters**")
            for filter_type in agent['runtimeGuardrails']['inputFilters']:
                st.write(f"• {filter_type}")
            
            st.markdown("**Output Validators**")
            for validator in agent['runtimeGuardrails']['outputValidators']:
                st.write(f"• {validator}")
        
        with col2:
            st.markdown("**Rate Controls**")
            rate_controls = agent['runtimeGuardrails']['rateControls']
            for control, value in rate_controls.items():
                st.write(f"• {control.replace('_', ' ').title()}: {value}")
            
            st.markdown("**Scope Controls**")
            scope_controls = agent['runtimeGuardrails']['scopeControls']
            for control, value in scope_controls.items():
                if isinstance(value, list):
                    st.write(f"• {control.replace('_', ' ').title()}: {', '.join(value)}")
                else:
                    st.write(f"• {control.replace('_', ' ').title()}: {value}")
        
        st.markdown("### Thresholds")
        kill_switch = agent['runtimeGuardrails']['killSwitch']
        st.write(f"**Kill Switch Enabled:** {'Yes' if kill_switch['enabled'] else 'No'}")
        st.write("**Trigger Conditions:**")
        for trigger in kill_switch['triggers']:
            st.write(f"• {trigger}")
        
        st.markdown("### Monitoring Hooks")
        monitoring = agent['monitoring']
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Calls This Week", monitoring['callsThisWeek'])
        with col2:
            st.metric("Guardrail Triggers", monitoring['guardrailTriggers'])
        with col3:
            st.metric("Escalations", monitoring['escalations'])
        with col4:
            st.metric("Uptime", monitoring['uptime'])
    
    with tab4:
        st.markdown("### Escalation Tree")
        for level in agent['escalationMechanisms']['tieredEscalation']:
            if level['status'] == 'success':
                st.success(f"**Level {level['level']}:** {level['action']}")
            elif level['status'] == 'pending':
                st.warning(f"**Level {level['level']}:** {level['action']} â³")
            else:
                st.info(f"**Level {level['level']}:** {level['action']}")
            
            st.write(f"*Status: {level['status']} | Timeout: {level['timeout']}*")
            st.write("---")
        
        st.markdown("### Notification Channels")
        channels = agent['escalationMechanisms']['notificationChannels']
        for channel in channels:
            st.write(f"• {channel}")
        
        st.markdown("### Decision Journal Configuration")
        decision_journals = agent['escalationMechanisms']['decisionJournals']
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"**Enabled:** {'Yes' if decision_journals['enabled'] else 'No'}")
        with col2:
            st.write(f"**Required:** {'Yes' if decision_journals['required'] else 'No'}")
        with col3:
            st.write(f"**Template:** {decision_journals['template']}")
    
    with tab5:
        st.markdown("### Logs")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Download CSV Logs"):
                st.success("CSV download initiated")
        with col2:
            if st.button("View Live Logs"):
                st.info("Live logs viewer opened")
        
        st.markdown("### Lineage")
        st.write("**Data Lineage:**")
        st.write("• Input → Processing → Output")
        st.write("• Dependencies → Agent → Downstream Systems")
        st.write("• Audit Trail → Decision Journal → Compliance Report")
        
        st.markdown("### Decision Journals")
        audit_logs = agent['governanceHooks']['auditLogs']
        st.write(f"**Total Entries:** {audit_logs['entries']}")
        st.write(f"**Last Escalation:** {audit_logs['lastEscalation']}")
        
        # Sample decision journal entries
        st.markdown("### Recent Decision Journal Entries")
        sample_entries = [
            "2025-01-22 14:30:15 - Payment approved after anomaly score review (0.72)",
            "2025-01-22 14:25:42 - Escalation triggered due to new destination account",
            "2025-01-22 14:20:18 - Input validation passed, proceeding to verification",
            "2025-01-22 14:15:33 - Agent started processing payment instruction"
        ]
        
        for entry in sample_entries:
            st.write(f"• {entry}")
        
        st.markdown("### Compliance Status")
        compliance_tags = agent['governanceHooks']['complianceTags']
        for tag, status in compliance_tags.items():
            if status:
                st.success(f"{tag} - Compliant")
            else:
                st.error(f"{tag} - Non-compliant")

def governance_workflow():
    st.markdown('<h1 class="main-header">Governance Workflow - New Agent Card</h1>', unsafe_allow_html=True)
    
    if st.button("â† Back to Agentic Operating System"):
        st.session_state['current_page'] = 'landing'
        st.rerun()
    
    with st.form("governance_form"):
        st.markdown("### Metadata Form")
        
        col1, col2 = st.columns(2)
        with col1:
            agent_name = st.text_input("Agent Name")
            pattern_type = st.selectbox("Pattern Type", [
                "Retriever-Augmented Agent",
                "Workflow Orchestrator Agent", 
                "Compliance Monitor Agent",
                "Negotiator Agent",
                "Classifier Agent",
                "Supervisor Agent",
                "Validator Agent"
            ])
            pattern_category = st.selectbox("Pattern Category", [
                "retrieval",
                "orchestration", 
                "monitoring",
                "reasoning",
                "classification",
                "supervision",
                "validation"
            ])
        
        with col2:
            risk_level = st.selectbox("Risk Level", ["Low", "Medium", "High"])
            business_use_case = st.text_area("Business Use Case")
            capabilities = st.text_area("Capabilities (one per line)", placeholder="Document classification\nContent extraction\nMetadata tagging")
        
        st.markdown("### Policy-as-Code Editor (YAML/JSON)")
        policies = st.text_area("Policies", value="""policies:
  - no PII storage
  - must log classification rationale
  - max processing time: 30 seconds
  - escalation required for high-risk documents
  - audit trail mandatory for all decisions""", height=200)
        
        st.markdown("### Runtime Guardrails Configuration")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Input Filters**")
            input_filters = st.multiselect("Select input filters", [
                "PII detection", "Content sanitization", "Size validation", 
                "Format validation", "Permission checks", "Data source validation"
            ])
            
            st.markdown("**Rate Controls**")
            max_calls = st.number_input("Max calls per minute", min_value=1, max_value=1000, value=100)
            max_tokens = st.number_input("Max tokens per call", min_value=100, max_value=10000, value=2000)
        
        with col2:
            st.markdown("**Output Validators**")
            output_validators = st.multiselect("Select output validators", [
                "Hallucination check", "Bias detection", "Policy compliance",
                "Format validation", "Content validation", "Accuracy check"
            ])
            
            st.markdown("**Kill Switch Triggers**")
            kill_switch_triggers = st.multiselect("Select kill switch triggers", [
                "error_rate > 5%", "response_time > 30s", "resource_usage > 80%",
                "false_positive_rate > 20%", "system_overload", "unauthorized_access"
            ])
        
        # Validation results
        st.markdown("### Validation")
        validation_passed = 8
        validation_total = 10
        validation_percentage = (validation_passed / validation_total) * 100
        
        if validation_percentage >= 80:
            st.success(f"Validation: {validation_passed}/{validation_total} checks passed ({validation_percentage:.0f}%)")
        else:
            st.error(f"Validation: {validation_passed}/{validation_total} checks passed ({validation_percentage:.0f}%)")
        
        st.error("Errors: Missing escalation path definition")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Submit for Review", type="primary"):
                st.success("Agent card submitted for review!")
        with col2:
            if st.form_submit_button("Save Draft"):
                st.info("Draft saved!")

# Helper functions for monitoring (kept for compatibility)
def get_monitoring_value(agent, key, default):
    """Safely extract monitoring values from agent data"""
    value = agent.get('monitoring', {}).get(key, default)
    if value == 'N/A' or value == 'NA':
        return default
    return value

def get_uptime_value(agent):
    """Extract and convert agent uptime percentage"""
    uptime_str = get_monitoring_value(agent, 'uptime', '0%')
    if isinstance(uptime_str, str) and uptime_str.endswith('%'):
        try:
            return float(uptime_str.replace('%', ''))
        except ValueError:
            return 0.0
    return float(uptime_str) if isinstance(uptime_str, (int, float)) else 0.0

# Runtime monitoring function removed

def escalation_console():
    st.markdown('<h1 class="main-header">Escalation Console</h1>', unsafe_allow_html=True)
    
    if st.button("â† Back to Agentic Operating System"):
        st.session_state['current_page'] = 'landing'
        st.rerun()
    
    # Timeline
    st.markdown("### Timeline")
    timeline_data = [
        {"Level": 1, "Action": "Auto-retry stricter prompt", "Status": "Success", "Time": "14:30:15"},
        {"Level": 2, "Action": "Escalate to Ops Supervisor Agent", "Status": "Pending", "Time": "14:32:45"},
        {"Level": 3, "Action": "Notify Human (ServiceNow)", "Status": "Not Triggered", "Time": "N/A"}
    ]
    
    for item in timeline_data:
        status_icon = "" if item["Status"] == "Success" else "" if item["Status"] == "Pending" else ""
        st.write(f"**Level {item['Level']}:** {item['Action']} {status_icon}")
        st.write(f"Status: {item['Status']} | Time: {item['Time']}")
        st.write("---")
    
    # Context panel
    st.markdown("### Context Panel")
    with st.expander("View Context Details"):
        st.write("**Input:** Classify this document")
        st.write("**Output:** Category: High Risk")
        st.write("**Guardrail Triggered:** PII Detected")
        st.write("**Confidence:** 87%")
        st.write("**Processing Time:** 2.3s")
    
    # Actions
    st.markdown("### Actions")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Resolve", type="primary"):
            st.success("Escalation resolved!")
    with col2:
        if st.button("Reassign"):
            st.info("Escalation reassigned")
    with col3:
        if st.button("Escalate Further", type="secondary"):
            st.warning("Escalation escalated further")
    
    # Decision journal
    st.markdown("### Decision Journal Entry")
    journal_entry = st.text_area("Enter your decision rationale and actions taken...")
    if st.button("Save Entry"):
        if journal_entry:
            st.success("Decision journal entry saved!")
        else:
            st.error("Please enter a decision journal entry")

def audit_reporting():
    st.markdown('<h1 class="main-header">Audit & Reporting</h1>', unsafe_allow_html=True)
    
    if st.button("â† Back to Agentic Operating System"):
        st.session_state['current_page'] = 'landing'
        st.rerun()
    
    # Filters
    st.markdown("### Filters")
    col1, col2, col3 = st.columns(3)
    with col1:
        agent_filter = st.text_input("Search by agent name")
    with col2:
        division_filter = st.selectbox("Division", ["All", "Operations", "Risk Management", "IT", "Compliance", "Treasury Operations"])
    with col3:
        compliance_filter = st.selectbox("Compliance", ["All", "GDPR", "OSFI", "FINTRAC", "AML", "Sanctions"])
    
    # Compliance overview
    st.markdown("### Compliance Overview")
    compliance_stats = {
        'Total Agents': 7,
        'GDPR Compliant': 5,
        'OSFI Compliant': 4,
        'FINTRAC Compliant': 3,
        'AML Compliant': 2,
        'Sanctions Compliant': 2
    }
    
    cols = st.columns(6)
    for i, (metric, value) in enumerate(compliance_stats.items()):
        with cols[i]:
            st.metric(metric, value)
    
    # Compliance heatmap
    st.markdown("### Compliance Heatmap")
    compliance_data = pd.DataFrame({
        'Agent Name': ['Retriever v1', 'Orchestrator v2', 'Compliance v1', 'Payment Processor v1', 'Negotiator v1'],
        'Pattern Type': ['Retrieval', 'Orchestration', 'Monitoring', 'Orchestration', 'Reasoning'],
        'Division': ['Operations', 'Operations', 'Risk Management', 'Treasury Operations', 'Legal Operations'],
        'Risk Level': ['Medium', 'High', 'Low', 'High', 'High'],
        'GDPR': ['Yes', 'Yes', 'Yes', 'Yes', 'Yes'],
        'OSFI': ['Yes', 'No', 'Yes', 'Yes', 'No'],
        'FINTRAC': ['No', 'No', 'Yes', 'Yes', 'No'],
        'AML': ['No', 'No', 'Yes', 'Yes', 'No'],
        'Sanctions': ['No', 'No', 'Yes', 'Yes', 'No'],
        'SOC2': ['Yes', 'Yes', 'Yes', 'Yes', 'Yes'],
        'Last Audit': ['2025-01-15', '2025-01-10', '2025-01-20', '2025-01-22', '2025-01-19']
    })
    
    st.dataframe(compliance_data, use_container_width=True)
    
    # Export options
    st.markdown("### Export Options")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Export PDF"):
            st.success("PDF export initiated")
    with col2:
        if st.button("Export CSV"):
            st.success("CSV export initiated")
    
    # Compliance summary
    st.markdown("### Compliance Summary")
    compliance_percentages = {
        'GDPR': 71,
        'OSFI': 57,
        'FINTRAC': 43,
        'AML': 29,
        'Sanctions': 29
    }
    
    for framework, percentage in compliance_percentages.items():
        st.write(f"**{framework} Compliance:** {percentage}%")
        st.progress(percentage / 100)

@st.cache_data(ttl=600)  # Cache for 10 minutes
def get_payment_instruction_data():
    """Cache payment instruction page data"""
    return {
        'sample_instructions': [
            "Send $2M CAD to Vendor X by Friday",
            "Transfer $500K USD to Supplier ABC for invoice #12345",
            "Pay $1.5M CAD to Contractor Y by end of month",
            "Wire $750K USD to International Partner Z urgently",
            "Process payment of $300K CAD to Service Provider ABC",
            "Send $2.5M CAD to Vendor X for quarterly payment",
            "Transfer $1M USD to Supplier DEF for materials",
            "Pay $400K CAD to Contractor GHI by next week",
            "Send 300k to Vendor ABC by Monday",
            "Transfer 750k USD to Supplier XYZ urgently",
            "Pay 1.2M CAD to Contractor DEF by Friday",
            "Wire 500k to International Partner GHI"
        ]
    }

def payment_instruction_entry():
    st.markdown('<h1 class="main-header">Payment Instruction</h1>', unsafe_allow_html=True)
    
    if st.button("â† Back to Agentic Operating System"):
        st.session_state['current_page'] = 'landing'
        st.rerun()
    
    # Agentic Pattern Information
    st.markdown("### Agentic Pattern Implementation")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Primary Pattern:**")
        st.success("Orchestration")
        st.markdown("*Coordinates multiple agents and workflows*")
    with col2:
        st.markdown("**Secondary Patterns:**")
        st.info("Tool Use")
        st.info("\U0001F9D0 Critic/Reviewer")
    with col3:
        st.markdown("**Active Agents:**")
        st.markdown("• **Payment Orchestrator Agent**")
        st.markdown("• **Anomaly Detection Agent**")
        st.markdown("• **Compliance Review Agent**")
    
    st.markdown("---")
    st.markdown("### Sample Instructions")
    st.markdown("Click on any sample instruction below to populate the input field:")
    
    # Use cached sample instructions
    cached_data = get_payment_instruction_data()
    sample_instructions = cached_data['sample_instructions']
    
    # Create clickable sample instructions
    cols = st.columns(2)
    for i, instruction in enumerate(sample_instructions):
        with cols[i % 2]:
            if st.button(f"{instruction}", key=f"sample_{i}"):
                st.session_state['sample_instruction'] = instruction
                st.rerun()
    
    st.markdown("---")
    st.markdown("### Instruction Input")
    
    # Get the selected sample instruction, retry instruction, or use default
    if 'retry_instruction' in st.session_state:
        default_instruction = st.session_state['retry_instruction']
        # Clear the retry instruction after using it
        del st.session_state['retry_instruction']
    else:
        default_instruction = st.session_state.get('sample_instruction', "Send $2M CAD to Vendor X by Friday")
    
    # Instruction input
    instruction_text = st.text_area(
        "Paste email or instruction text here...",
        value=default_instruction,
        height=150,
        help="Enter the payment instruction in natural language"
    )
    
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Extract Intent", type="primary"):
            # Parse the instruction text dynamically
            parsed_intent = parse_payment_intent(instruction_text)
            st.session_state['extracted_intent'] = parsed_intent
            st.rerun()
    
    # Show parsed intent if available
    if 'extracted_intent' in st.session_state:
        st.markdown("### Parsed Intent (Preview)")
        intent = st.session_state['extracted_intent']
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Amount", intent['amount'])
        with col2:
            st.metric("Beneficiary", intent['beneficiary'])
        with col3:
            st.metric("Date", intent['date'])
        with col4:
            st.metric("Urgency", intent['urgency'])
        
        confidence = intent['confidence']
        if confidence >= 0.9:
            st.success(f"Confidence: {confidence:.2f}")
        elif confidence >= 0.7:
            st.warning(f"Confidence: {confidence:.2f}")
        else:
            st.error(f"Confidence: {confidence:.2f}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Confirm Intent"):
                st.session_state['current_page'] = 'intent_verification'
                st.rerun()
        with col2:
            if st.button("Retry Parsing"):
                del st.session_state['extracted_intent']
                # Keep the current instruction text in the text area
                st.session_state['retry_instruction'] = instruction_text
                st.rerun()

def intent_verification():
    st.markdown('<h1 class="main-header">Intent Verification & Anomaly Detection</h1>', unsafe_allow_html=True)
    
    if st.button("â† Back to Payment Instruction"):
        st.session_state['current_page'] = 'payment_instruction'
        st.rerun()
    
    # Agentic Pattern Analysis
    st.markdown("### Pattern Analysis")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Reflection Pattern**")
        st.markdown("*Self-evaluating payment decision*")
        st.success("Confidence: 87%")
    with col2:
        st.markdown("**Critic/Reviewer Pattern \U0001F9D0**")
        st.markdown("*Secondary validation layer*")
        st.warning("Review Required")
    with col3:
        st.markdown("**Memory & Learning**")
        st.markdown("*Pattern recognition from history*")
        st.info("Learning: Active")
    
    st.markdown("---")
    
    # Payment pattern check
    st.markdown("### Payment Pattern Check")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Typical Amount", "$1.8M quarterly")
    with col2:
        st.metric("Current Request", "$2.0M")
    with col3:
        anomaly_score = 0.72
        st.metric("Anomaly Score", f"{anomaly_score:.2f}")
    
    if anomaly_score > 0.65:
        st.warning("Above Threshold 0.65")
    else:
        st.success("Within Normal Range")
    
    # Account verification
    st.markdown("### Account Verification")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.success("Source Account: RBC Treasury Ops")
    with col2:
        st.warning("Destination Account: Vendor X (NEW)")
    with col3:
        st.success("Sanctions/KYC: Clear")
    
    # Risk summary
    st.markdown("### Risk Summary")
    risk_factors = {
        'Pattern Deviation': 'Moderate',
        'Destination': 'New Account',
        'Compliance': 'Pass'
    }
    
    for factor, status in risk_factors.items():
        if status == 'Pass':
            st.success(f"{factor}: {status}")
        elif status == 'Moderate':
            st.warning(f"{factor}: {status}")
        else:
            st.info(f"{factor}: {status}")
    
    if st.button("Generate Scenario Summary", type="primary"):
        st.session_state['scenario_summary'] = {
            'intent': 'Transfer $2,000,000 CAD to Vendor X',
            'context': 'Matches quarterly vendor payment pattern',
            'risk_flags': ['Destination account NEW', 'Anomaly Score: 0.72 (Threshold: 0.65)'],
            'compliance': 'Pass (AML/KYC/Sanctions Clear)',
            'recommendation': 'Escalation Required'
        }
        st.session_state['current_page'] = 'scenario_summary'
        st.rerun()

def scenario_summary():
    st.markdown('<h1 class="main-header">Payment Review - Scenario Summary</h1>', unsafe_allow_html=True)
    
    if st.button("â† Back to Verification"):
        st.session_state['current_page'] = 'intent_verification'
        st.rerun()
    
    # Pattern Implementation Summary
    st.markdown("### Pattern Implementation Summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Primary Pattern:**")
        st.success("Orchestration")
        st.markdown("*Coordinated 3 agents successfully*")
    with col2:
        st.markdown("**Secondary Patterns:**")
        st.info("Tool Use - API calls")
        st.info("\U0001F9D0 Critic/Reviewer - Validation")
    with col3:
        st.markdown("**Pattern Performance:**")
        st.metric("Success Rate", "94%")
        st.metric("Processing Time", "2.3s")
    
    st.markdown("---")
    
    if 'scenario_summary' not in st.session_state:
        st.error("No scenario summary available")
        return
    
    summary = st.session_state['scenario_summary']
    
    # Main summary card
    st.markdown("### Payment Details")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Intent:** {summary['intent']}")
        st.markdown(f"**Context:** {summary['context']}")
    with col2:
        st.markdown(f"**Compliance:** {summary['compliance']}")
        st.markdown(f"**Recommendation:** {summary['recommendation']}")
    
    # Risk flags
    st.markdown("### Risk Flags")
    for flag in summary['risk_flags']:
        if 'NEW' in flag or '0.72' in flag:
            st.warning(f"{flag}")
        else:
            st.info(f"{flag}")
    
    # Reviewer actions
    st.markdown("### Reviewer Actions")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Approve", type="primary"):
            st.success("Payment approved!")
            st.session_state['payment_decision'] = 'Approved'
            st.session_state['current_page'] = 'payment_audit'
            st.rerun()
    with col2:
        if st.button("Reject", type="secondary"):
            st.error("Payment rejected!")
            st.session_state['payment_decision'] = 'Rejected'
            st.session_state['current_page'] = 'payment_audit'
            st.rerun()
    with col3:
        if st.button("Escalate Further"):
            st.warning("Payment escalated further!")
            st.session_state['payment_decision'] = 'Escalated'
            st.session_state['current_page'] = 'payment_escalation'
            st.rerun()
    
    # Decision journal
    st.markdown("### Decision Journal Entry")
    decision_entry = st.text_area(
        "Enter your decision rationale and actions taken...",
        height=100,
        placeholder="Example: Approved based on historical pattern match and clear compliance status..."
    )
    
    if st.button("Save Decision"):
        if decision_entry:
            st.success("Decision journal entry saved!")
            st.session_state['decision_entry'] = decision_entry
        else:
            st.error("Please enter a decision journal entry")

def payment_escalation():
    st.markdown('<h1 class="main-header">Escalation Console - Payment Processor Agent</h1>', unsafe_allow_html=True)
    
    if st.button("â† Back to Agentic Operating System"):
        st.session_state['current_page'] = 'landing'
        st.rerun()
    
    # Agentic Pattern Escalation Analysis
    st.markdown("### Pattern-Based Escalation Analysis")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Orchestration Pattern**")
        st.markdown("*Coordinating escalation workflow*")
        st.error("Workflow Timeout")
    with col2:
        st.markdown("**Reflection Pattern**")
        st.markdown("*Self-evaluating escalation decision*")
        st.warning("Confidence: 65%")
    with col3:
        st.markdown("**Critic/Reviewer Pattern \U0001F9D0**")
        st.markdown("*Secondary validation required*")
        st.info("Review in Progress")
    
    st.markdown("---")
    
    # Escalation timeline
    st.markdown("### Escalation Timeline")
    timeline_data = [
        {"Level": 1, "Action": "Auto-retry parsing with stricter schema", "Status": "Success", "Time": "14:30:15"},
        {"Level": 2, "Action": "Escalated to Payment Supervisor Agent", "Status": "Pending", "Time": "14:32:45"},
        {"Level": 3, "Action": "Pending Human Review (Treasury Ops)", "Status": "In Progress", "Time": "14:35:20"}
    ]
    
    for item in timeline_data:
        if item["Status"] == "Success":
            st.success(f"**Level {item['Level']}:** {item['Action']} - {item['Status']} at {item['Time']}")
        elif item["Status"] == "Pending":
            st.warning(f"â³ **Level {item['Level']}:** {item['Action']} - {item['Status']} at {item['Time']}")
        else:
            st.info(f"**Level {item['Level']}:** {item['Action']} - {item['Status']} at {item['Time']}")
    
    # Context panel
    st.markdown("### Context Panel")
    with st.expander("View Context Details", expanded=True):
        st.write("**Input:** Send $2M CAD to Vendor X by Friday")
        st.write("**Parsed Intent:** Amount $2M, Beneficiary Vendor X, Date Friday, Urgency High")
        st.write("**Guardrail Triggered:** Anomaly Score > 0.65")
        st.write("**Confidence:** 92%")
        st.write("**Processing Time:** 3.2s")
        st.write("**Risk Assessment:** Moderate - New destination account")
    
    # Actions
    st.markdown("### Actions")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Resolve", type="primary"):
            st.success("Escalation resolved!")
    with col2:
        if st.button("Reassign"):
            st.info("Escalation reassigned")
    with col3:
        if st.button("Escalate Further", type="secondary"):
            st.warning("Escalation escalated further")
    
    # Decision journal
    st.markdown("### Decision Journal Entry")
    journal_entry = st.text_area("Enter your decision rationale and actions taken...", height=100)
    if st.button("Save Entry"):
        if journal_entry:
            st.success("Decision journal entry saved!")
        else:
            st.error("Please enter a decision journal entry")

@st.cache_resource(ttl=600)  # Cache for 10 minutes - resource caching for heavy components
def create_payment_audit_charts():
    """Create payment audit charts with caching"""
    # Payment volume trends
    dates = pd.date_range(start='2024-01-01', end='2024-01-31', freq='D')
    volume_data = np.random.normal(1000000, 200000, len(dates))
    
    fig_volume = px.line(
        x=dates, 
        y=volume_data,
        title='Payment Volume Trends (Last 30 Days)',
        labels={'x': 'Date', 'y': 'Volume (CAD)'}
    )
    fig_volume.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif")
    )
    
    # Anomaly detection trends
    anomaly_scores = np.random.beta(2, 5, len(dates)) * 0.8 + 0.1
    
    fig_anomaly = go.Figure()
    fig_anomaly.add_trace(go.Scatter(
        x=dates, 
        y=anomaly_scores,
        mode='lines+markers',
        name='Anomaly Score',
        line=dict(color='#FF6B6B', width=2)
    ))
    fig_anomaly.add_hline(y=0.65, line_dash="dash", line_color="red", 
                         annotation_text="Threshold: 0.65")
    fig_anomaly.update_layout(
        title='Anomaly Score Trends Over Time',
        xaxis_title='Date',
        yaxis_title='Anomaly Score',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif")
    )
    
    return fig_volume, fig_anomaly

def payment_audit():
    st.markdown('<h1 class="main-header">Payment Audit & Compliance Dashboard</h1>', unsafe_allow_html=True)
    
    if st.button("â† Back to Agentic Operating System"):
        st.session_state['current_page'] = 'landing'
        st.rerun()
    
    # Agentic Pattern Audit Analysis
    st.markdown("### Pattern Performance Audit")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("**Orchestration**")
        st.metric("Success Rate", "94%")
        st.metric("Avg Time", "2.3s")
    with col2:
        st.markdown("**Reflection**")
        st.metric("Accuracy", "89%")
        st.metric("Confidence", "87%")
    with col3:
        st.markdown("**Critic/Reviewer \U0001F9D0**")
        st.metric("Catch Rate", "76%")
        st.metric("False Positives", "12%")
    with col4:
        st.markdown("**Memory & Learning**")
        st.metric("Learning Rate", "15%")
        st.metric("Pattern Updates", "23")
    
    st.markdown("---")
    
    # Filters
    st.markdown("### Filters")
    col1, col2, col3 = st.columns(3)
    with col1:
        agent_filter = st.selectbox("Agent", ["All", "Payment Processor v1", "Payment Supervisor v1"])
    with col2:
        division_filter = st.selectbox("Division", ["All", "Treasury Operations", "Risk Management", "Compliance"])
    with col3:
        date_range = st.date_input("Date Range", value=datetime.now().date())
    
    # Recent transactions
    st.markdown("### Recent Transactions")
    transactions_data = pd.DataFrame({
        'Date': ['Sep 22', 'Sep 20', 'Sep 18', 'Sep 15', 'Sep 12'],
        'Amount': ['$2.0M', '$1.8M', '$3.5M', '$1.2M', '$2.5M'],
        'Beneficiary': ['Vendor X', 'Vendor X', 'Vendor Y', 'Vendor Z', 'Vendor A'],
        'Risk': ['High', 'Low', 'Critical', 'Low', 'High'],
        'Decision': ['Approved', 'Approved', 'Rejected', 'Approved', 'Pending'],
        'Anomaly Score': [0.72, 0.45, 0.89, 0.38, 0.68],
        'Reviewer': ['John Smith', 'Jane Doe', 'Mike Johnson', 'Sarah Wilson', 'Pending']
    })
    
    st.dataframe(transactions_data, use_container_width=True)
    
    # Compliance heatmap
    st.markdown("### Compliance Heatmap")
    compliance_data = pd.DataFrame({
        'Agent Name': ['Payment Processor v1', 'Payment Supervisor v1', 'Payment Validator v1'],
        'Division': ['Treasury Operations', 'Treasury Operations', 'Risk Management'],
        'Risk Level': ['High', 'High', 'Medium'],
        'AML': ['Yes', 'Yes', 'Yes'],
        'KYC': ['Yes', 'Yes', 'Yes'],
        'Sanctions': ['Yes', 'Yes', 'No'],
        'OSFI': ['Yes', 'Yes', 'Yes'],
        'Last Audit': ['2025-01-22', '2025-01-20', '2025-01-18']
    })
    
    st.dataframe(compliance_data, use_container_width=True)
    
    # Metrics
    st.markdown("### Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Transactions", "23", "5")
    with col2:
        st.metric("Approval Rate", "78%", "12%")
    with col3:
        st.metric("Avg Anomaly Score", "0.58", "-0.05")
    with col4:
        st.metric("Escalations", "7", "2")
    
    
    # Use cached charts for better performance
    fig_volume, fig_anomaly = create_payment_audit_charts()
    
    st.markdown("### Payment Volume Trends")
    st.plotly_chart(fig_volume, use_container_width=True, key="payment_audit_volume_trends")
    
    st.markdown("### Anomaly Score Trends")
    st.plotly_chart(fig_anomaly, use_container_width=True, key="payment_audit_anomaly_trends")

@st.cache_resource(ttl=3600)  # Cache for 1 hour - resource caching for heavy components
def create_process_flow_chart():
    """Create an executive-style process flow chart with professional design"""
    # Executive-Style Process Flow Diagram using Plotly
    # Define nodes with professional corporate design and strategic layout
    nodes = [
        # Input Layer - Executive Blue
        {"id": "user_input", "label": "Payment Request\nNatural Language Input", "x": 0, "y": 10, "color": "#1E3A8A", "size": 120, "category": "input", "shape": "circle", "width": 140, "height": 80},
        
        # AI Processing Layer - Professional Green
        {"id": "intent_agent", "label": "Intent Parsing\nAI Agent", "x": 3, "y": 10, "color": "#059669", "size": 100, "category": "agent", "shape": "circle", "width": 120, "height": 60},
        {"id": "verification_agent", "label": "Verification\nAI Agent", "x": 5.5, "y": 10, "color": "#059669", "size": 100, "category": "agent", "shape": "circle", "width": 120, "height": 60},
        {"id": "anomaly_agent", "label": "Risk Analysis\nAI Agent", "x": 8, "y": 10, "color": "#059669", "size": 100, "category": "agent", "shape": "circle", "width": 120, "height": 60},
        
        # Decision Diamond - Executive Orange
        {"id": "decision_point", "label": "Risk Assessment\n& Routing", "x": 10.5, "y": 10, "color": "#DC2626", "size": 100, "category": "decision", "shape": "diamond", "width": 100, "height": 100},
        
        # Human Review Points - Executive Red
        {"id": "human_review", "label": "Treasury Review\nManual Approval", "x": 13, "y": 8, "color": "#B91C1C", "size": 100, "category": "human", "shape": "circle", "width": 120, "height": 60},
        {"id": "escalation", "label": "Executive Escalation\nHigh-Risk Cases", "x": 13, "y": 12, "color": "#B91C1C", "size": 100, "category": "human", "shape": "circle", "width": 120, "height": 60},
        
        # Execution Layer - Executive Blue
        {"id": "payment_execution", "label": "Payment Execution\nCore Banking", "x": 16, "y": 10, "color": "#1E3A8A", "size": 120, "category": "execution", "shape": "circle", "width": 140, "height": 80},
        
        # Output Layer - Success Green
        {"id": "confirmation", "label": "Transaction Complete\nAudit Trail", "x": 19, "y": 10, "color": "#047857", "size": 120, "category": "output", "shape": "circle", "width": 140, "height": 80},
        
        # Monitoring Layer - Executive Gray
        {"id": "monitoring", "label": "Real-time Monitoring\n& Compliance", "x": 10.5, "y": 6, "color": "#6B7280", "size": 100, "category": "monitoring", "shape": "circle", "width": 120, "height": 60},
        
        # Data Sources - Subtle Gray
        {"id": "compliance_db", "label": "Compliance Database\nKYC/AML Data", "x": 3, "y": 7, "color": "#9CA3AF", "size": 80, "category": "data", "shape": "circle", "width": 100, "height": 50},
        {"id": "payment_api", "label": "Payment Gateway\nBanking APIs", "x": 16, "y": 7, "color": "#9CA3AF", "size": 80, "category": "data", "shape": "circle", "width": 100, "height": 50},
    ]
    
    # Define edges (connections) - Executive-style with clean lines and professional styling
    edges = [
        # Main flow - Primary path with executive blue
        {"from": "user_input", "to": "intent_agent", "label": "Parse Intent", "type": "main", "width": 3, "curve": 0.1},
        {"from": "intent_agent", "to": "verification_agent", "label": "Validate", "type": "main", "width": 3, "curve": 0.1},
        {"from": "verification_agent", "to": "anomaly_agent", "label": "Analyze Risk", "type": "main", "width": 3, "curve": 0.1},
        {"from": "anomaly_agent", "to": "decision_point", "label": "Risk Score", "type": "main", "width": 3, "curve": 0.1},
        {"from": "decision_point", "to": "payment_execution", "label": "Approve", "type": "main", "width": 3, "curve": 0.1},
        {"from": "payment_execution", "to": "confirmation", "label": "Complete", "type": "main", "width": 3, "curve": 0.1},
        
        # Data connections - Supporting systems with subtle styling
        {"from": "compliance_db", "to": "verification_agent", "label": "Check", "type": "data", "width": 2, "curve": 0.2},
        {"from": "payment_api", "to": "payment_execution", "label": "Execute", "type": "data", "width": 2, "curve": 0.2},
        
        # Escalation paths - Human intervention with executive red
        {"from": "decision_point", "to": "human_review", "label": "Review", "type": "escalation", "width": 2.5, "curve": 0.3},
        {"from": "decision_point", "to": "escalation", "label": "Escalate", "type": "escalation", "width": 2.5, "curve": 0.3},
        {"from": "human_review", "to": "payment_execution", "label": "Approve", "type": "escalation", "width": 2.5, "curve": 0.2},
        {"from": "escalation", "to": "payment_execution", "label": "Approve", "type": "escalation", "width": 2.5, "curve": 0.2},
        
        # Monitoring connections - Oversight with subtle gray
        {"from": "monitoring", "to": "intent_agent", "label": "", "type": "monitoring", "width": 1, "curve": 0.4},
        {"from": "monitoring", "to": "verification_agent", "label": "", "type": "monitoring", "width": 1, "curve": 0.4},
        {"from": "monitoring", "to": "anomaly_agent", "label": "", "type": "monitoring", "width": 1, "curve": 0.4},
        {"from": "monitoring", "to": "payment_execution", "label": "", "type": "monitoring", "width": 1, "curve": 0.4},
    ]
    
    # Create the executive-style diagram
    fig = go.Figure()
    
    # Define executive-style edge colors and styles
    edge_styles = {
        "main": {"color": "#1E3A8A", "dash": "solid", "opacity": 0.9},
        "escalation": {"color": "#DC2626", "dash": "solid", "opacity": 0.8},
        "data": {"color": "#6B7280", "dash": "dot", "opacity": 0.6},
        "monitoring": {"color": "#9CA3AF", "dash": "dot", "opacity": 0.4}
    }
    
    # Add edges with executive-style clean connections
    for edge in edges:
        from_node = next(n for n in nodes if n["id"] == edge["from"])
        to_node = next(n for n in nodes if n["id"] == edge["to"])
        
        style = edge_styles.get(edge["type"], {"color": "#6B7280", "dash": "solid", "opacity": 0.8})
        
        # Create clean path for executive-style connections
        curve_factor = edge.get("curve", 0.1)
        mid_x = (from_node["x"] + to_node["x"]) / 2
        mid_y = (from_node["y"] + to_node["y"]) / 2
        
        # Calculate control points for smooth curves
        if from_node["y"] == to_node["y"]:  # Horizontal connection
            control_x = mid_x
            control_y = mid_y + curve_factor
        else:  # Diagonal connection
            control_x = mid_x + curve_factor
            control_y = mid_y
        
        # Create smooth curve using quadratic bezier
        import numpy as np
        t = np.linspace(0, 1, 50)
        x_curve = (1-t)**2 * from_node["x"] + 2*(1-t)*t * control_x + t**2 * to_node["x"]
        y_curve = (1-t)**2 * from_node["y"] + 2*(1-t)*t * control_y + t**2 * to_node["y"]
        
        fig.add_trace(go.Scatter(
            x=x_curve,
            y=y_curve,
            mode='lines',
            line=dict(
                color=style["color"], 
                width=edge["width"], 
                dash=style["dash"],
                shape='spline'
            ),
            showlegend=False,
            hoverinfo='skip',
            opacity=style["opacity"]
        ))
        
        # Add executive-style edge labels with professional typography
        if edge["label"]:  # Only add labels for non-empty strings
            label_offset_x = 0.3 if edge["type"] == "escalation" else 0.2
            label_offset_y = 0.2 if edge["type"] == "data" else 0.1
            
            fig.add_annotation(
                x=mid_x + label_offset_x,
                y=mid_y + label_offset_y,
                text=f"<b>{edge['label']}</b>",
                showarrow=False,
                font=dict(
                    size=11, 
                    color="#1F2937", 
                    family="Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
                ),
                bgcolor="rgba(255,255,255,0.95)",
                bordercolor=style["color"],
                borderwidth=1,
                borderpad=6,
                opacity=0.95,
                align="center"
            )
    
    # Add nodes with executive-style design
    for node in nodes:
        # Executive-style node styling
        node_style = {
            "input": {"border_width": 2, "opacity": 0.95, "shadow": True, "border_color": "#1E40AF"},
            "agent": {"border_width": 2, "opacity": 0.9, "shadow": True, "border_color": "#047857"},
            "decision": {"border_width": 2, "opacity": 0.95, "shadow": True, "border_color": "#DC2626"},
            "human": {"border_width": 2, "opacity": 0.9, "shadow": True, "border_color": "#B91C1C"},
            "execution": {"border_width": 2, "opacity": 0.95, "shadow": True, "border_color": "#1E40AF"},
            "output": {"border_width": 2, "opacity": 0.95, "shadow": True, "border_color": "#047857"},
            "monitoring": {"border_width": 1, "opacity": 0.8, "shadow": False, "border_color": "#6B7280"},
            "data": {"border_width": 1, "opacity": 0.75, "shadow": False, "border_color": "#9CA3AF"}
        }
        
        style = node_style.get(node["category"], {"border_width": 2, "opacity": 0.9, "shadow": True, "border_color": "#6B7280"})
        
        # Add shadow effect for executive-style depth
        if style["shadow"] and node.get("shadow", False):
            fig.add_trace(go.Scatter(
                x=[node["x"] + 0.05],
                y=[node["y"] - 0.05],
                mode='markers',
                marker=dict(
                    size=node["size"],
                    color='rgba(0,0,0,0.1)',
                    opacity=0.2
                ),
                showlegend=False,
                hoverinfo='skip'
            ))
        
        # Main node with executive-style appearance
        fig.add_trace(go.Scatter(
            x=[node["x"]],
            y=[node["y"]],
            mode='markers+text',
            marker=dict(
                size=node["size"],
                color=node["color"],
                line=dict(width=style["border_width"], color=style["border_color"]),
                opacity=style["opacity"],
                symbol='circle' if node.get("shape") == "circle" else 'diamond' if node.get("shape") == "diamond" else 'circle'
            ),
            text=node["label"],
            textposition="middle center",
            textfont=dict(
                size=12, 
                color="white", 
                family="Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
            ),
            showlegend=False,
            hovertemplate=f"<b>{node['label'].split('\n')[0]}</b><br>" +
                         f"<br>".join(node['label'].split('\n')[1:]) +
                         f"<br><br><b>Category:</b> {node['category'].title()}" +
                         "<extra></extra>"
        ))
    
    # Update layout with executive-style design
    fig.update_layout(
        title=dict(
            text="High-Value Payment Processing Workflow",
            font=dict(
                size=24, 
                family="Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif", 
                color="#1F2937"
            ),
            x=0.5,
            y=0.95
        ),
        xaxis=dict(
            showgrid=True, 
            gridcolor='rgba(0,0,0,0.05)',
            showticklabels=False, 
            zeroline=False,
            range=[-1, 21],
            gridwidth=1
        ),
        yaxis=dict(
            showgrid=True, 
            gridcolor='rgba(0,0,0,0.05)',
            showticklabels=False, 
            zeroline=False,
            range=[4, 14],
            gridwidth=1
        ),
        plot_bgcolor='rgba(249,250,251,1.0)',
        paper_bgcolor='rgba(255,255,255,1.0)',
        width=1400,
        height=700,
        margin=dict(l=80, r=80, t=120, b=80),
        font=dict(
            family="Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif", 
            size=11
        )
    )
    
    return fig
    
    # Define edges (connections) - iOS-style with smooth curves and modern styling
    edges = [
        # Main flow - Primary path with iOS blue
        {"from": "user_input", "to": "intent_agent", "label": "Natural Language", "type": "main", "width": 4, "curve": 0.1},
        {"from": "intent_agent", "to": "verification_agent", "label": "Structured Data", "type": "main", "width": 4, "curve": 0.1},
        {"from": "verification_agent", "to": "anomaly_agent", "label": "Validated Data", "type": "main", "width": 4, "curve": 0.1},
        {"from": "anomaly_agent", "to": "decision_point", "label": "Risk Score", "type": "main", "width": 4, "curve": 0.1},
        {"from": "decision_point", "to": "payment_execution", "label": "Low Risk", "type": "main", "width": 4, "curve": 0.1},
        {"from": "payment_execution", "to": "confirmation", "label": "Success", "type": "main", "width": 4, "curve": 0.1},
        
        # Data connections - Supporting systems with subtle styling
        {"from": "compliance_db", "to": "verification_agent", "label": "Compliance Check", "type": "data", "width": 2, "curve": 0.2},
        {"from": "payment_api", "to": "payment_execution", "label": "API Call", "type": "data", "width": 2, "curve": 0.2},
        
        # Escalation paths - Human intervention with iOS red
        {"from": "decision_point", "to": "human_review", "label": "Medium Risk", "type": "escalation", "width": 3, "curve": 0.3},
        {"from": "decision_point", "to": "escalation", "label": "High Risk", "type": "escalation", "width": 3, "curve": 0.3},
        {"from": "human_review", "to": "payment_execution", "label": "Approved", "type": "escalation", "width": 3, "curve": 0.2},
        {"from": "escalation", "to": "payment_execution", "label": "Approved", "type": "escalation", "width": 3, "curve": 0.2},
        
        # Monitoring connections - Oversight with subtle gray
        {"from": "monitoring", "to": "intent_agent", "label": "Monitor", "type": "monitoring", "width": 1.5, "curve": 0.4},
        {"from": "monitoring", "to": "verification_agent", "label": "Monitor", "type": "monitoring", "width": 1.5, "curve": 0.4},
        {"from": "monitoring", "to": "anomaly_agent", "label": "Monitor", "type": "monitoring", "width": 1.5, "curve": 0.4},
        {"from": "monitoring", "to": "payment_execution", "label": "Monitor", "type": "monitoring", "width": 1.5, "curve": 0.4},
    ]
    
    # Create the iOS-style diagram
    fig = go.Figure()
    
    # Define iOS-style edge colors and styles
    edge_styles = {
        "main": {"color": "#007AFF", "dash": "solid", "opacity": 0.9},
        "escalation": {"color": "#FF3B30", "dash": "solid", "opacity": 0.8},
        "data": {"color": "#AEAEB2", "dash": "dot", "opacity": 0.6},
        "monitoring": {"color": "#8E8E93", "dash": "dot", "opacity": 0.5}
    }
    
    # Add edges with iOS-style curved connections
    for edge in edges:
        from_node = next(n for n in nodes if n["id"] == edge["from"])
        to_node = next(n for n in nodes if n["id"] == edge["to"])
        
        style = edge_styles.get(edge["type"], {"color": "#8E8E93", "dash": "solid", "opacity": 0.8})
        
        # Create curved path for iOS-style connections
        curve_factor = edge.get("curve", 0.1)
        mid_x = (from_node["x"] + to_node["x"]) / 2
        mid_y = (from_node["y"] + to_node["y"]) / 2
        
        # Calculate control points for smooth curves
        if from_node["y"] == to_node["y"]:  # Horizontal connection
            control_x = mid_x
            control_y = mid_y + curve_factor
        else:  # Diagonal connection
            control_x = mid_x + curve_factor
            control_y = mid_y
        
        # Create smooth curve using quadratic bezier
        import numpy as np
        t = np.linspace(0, 1, 50)
        x_curve = (1-t)**2 * from_node["x"] + 2*(1-t)*t * control_x + t**2 * to_node["x"]
        y_curve = (1-t)**2 * from_node["y"] + 2*(1-t)*t * control_y + t**2 * to_node["y"]
        
        fig.add_trace(go.Scatter(
            x=x_curve,
            y=y_curve,
            mode='lines',
            line=dict(
                color=style["color"], 
                width=edge["width"], 
                dash=style["dash"],
                shape='spline'
            ),
            showlegend=False,
            hoverinfo='skip',
            opacity=style["opacity"]
        ))
        
        # Add iOS-style edge labels with modern typography
        label_offset_x = 0.4 if edge["type"] == "escalation" else 0.2
        label_offset_y = 0.3 if edge["type"] == "data" else 0.1
        
        fig.add_annotation(
            x=mid_x + label_offset_x,
            y=mid_y + label_offset_y,
            text=f"<b>{edge['label']}</b>",
            showarrow=False,
            font=dict(
                size=12, 
                color="#1D1D1F", 
                family="SF Pro Display, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
            ),
            bgcolor="rgba(255,255,255,0.95)",
            bordercolor=style["color"],
            borderwidth=1.5,
            borderpad=8,
            opacity=0.95,
            align="center"
        )
    
    # Add nodes with iOS-style design and shadows
    for node in nodes:
        # iOS-style node styling with shadows and modern effects
        node_style = {
            "input": {"border_width": 0, "opacity": 0.95, "shadow": True, "gradient": True},
            "agent": {"border_width": 0, "opacity": 0.9, "shadow": True, "gradient": True},
            "decision": {"border_width": 0, "opacity": 0.95, "shadow": True, "gradient": True},
            "human": {"border_width": 0, "opacity": 0.9, "shadow": True, "gradient": True},
            "execution": {"border_width": 0, "opacity": 0.95, "shadow": True, "gradient": True},
            "output": {"border_width": 0, "opacity": 0.95, "shadow": True, "gradient": True},
            "monitoring": {"border_width": 0, "opacity": 0.8, "shadow": False, "gradient": False},
            "data": {"border_width": 0, "opacity": 0.75, "shadow": False, "gradient": False}
        }
        
        style = node_style.get(node["category"], {"border_width": 0, "opacity": 0.9, "shadow": True, "gradient": True})
        
        # Add shadow effect for iOS-style depth
        if style["shadow"] and node.get("shadow", False):
            fig.add_trace(go.Scatter(
                x=[node["x"] + 0.1],
                y=[node["y"] - 0.1],
                mode='markers',
                marker=dict(
                    size=node["size"],
                    color='rgba(0,0,0,0.15)',
                    opacity=0.3
                ),
                showlegend=False,
                hoverinfo='skip'
            ))
        
        # Main node with iOS-style rounded appearance
        fig.add_trace(go.Scatter(
            x=[node["x"]],
            y=[node["y"]],
            mode='markers+text',
            marker=dict(
                size=node["size"],
                color=node["color"],
                line=dict(width=0),
                opacity=style["opacity"],
                symbol='circle'
            ),
            text=node["label"],
            textposition="middle center",
            textfont=dict(
                size=13, 
                color="white", 
                family="SF Pro Display, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
            ),
            showlegend=False,
            hovertemplate=f"<b>{node['label'].split('<br/>')[0]}</b><br>" +
                         f"<br>".join(node['label'].split('<br/>')[1:]) +
                         f"<br><br><b>Category:</b> {node['category'].title()}" +
                         "<extra></extra>"
        ))
    
    # Update layout with iOS-style design
    fig.update_layout(
        title=dict(
            text="High-Value Payment Processing Workflow",
            font=dict(
                size=28, 
                family="SF Pro Display, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif", 
                color="#1D1D1F"
            ),
            x=0.5,
            y=0.95
        ),
        xaxis=dict(
            showgrid=True, 
            gridcolor='rgba(0,0,0,0.05)',
            showticklabels=False, 
            zeroline=False,
            range=[-2, 23],
            gridwidth=1
        ),
        yaxis=dict(
            showgrid=True, 
            gridcolor='rgba(0,0,0,0.05)',
            showticklabels=False, 
            zeroline=False,
            range=[2, 12],
            gridwidth=1
        ),
        plot_bgcolor='rgba(242,242,247,0.8)',
        paper_bgcolor='rgba(255,255,255,1.0)',
        width=1600,
        height=800,
        margin=dict(l=100, r=100, t=140, b=100),
        font=dict(
            family="SF Pro Display, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif", 
            size=12
        )
    )
    
    return fig

def process_flow_diagram():
    st.markdown('<h1 class="main-header">End-to-End Process Flow</h1>', unsafe_allow_html=True)
    
    if st.button("â† Back to Agentic Operating System"):
        st.session_state['current_page'] = 'landing'
        st.rerun()
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <p style="font-size: 1.1rem; color: #6B7280; font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; font-weight: 400; letter-spacing: -0.01em;">
            Executive overview of the complete payment processing workflow with AI agents, human interactions, and escalation paths
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Use the cached executive-style chart
    fig = create_process_flow_chart()
    st.plotly_chart(fig, use_container_width=True, key="executive_process_flow")
    
    # Process Flow Details
    st.markdown("---")
    st.markdown("### Process Flow Details")
    
    # Create tabs for different aspects
    tab1, tab2, tab3, tab4 = st.tabs(["Workflow Steps", "AI Agents", "Human Interactions", "Data Flow"])
    
    with tab1:
        st.markdown("""
        #### **1. Input Processing**
        - **User Input**: Natural language payment instructions
        - **Intent Agent**: Parses and extracts structured payment data
        - **Output**: Standardized payment request with amount, accounts, purpose
        
        #### **2. Verification & Compliance**
        - **Verification Agent**: Validates account details and compliance status
        - **Data Sources**: Sanctions lists, KYC databases, AML checks
        - **Output**: Compliance status and account validation results
        
        #### **3. Risk Assessment**
        - **Anomaly Agent**: Analyzes payment patterns and risk indicators
        - **Pattern Recognition**: Historical data analysis and anomaly detection
        - **Output**: Risk score and anomaly indicators
        
        #### **4. Decision & Routing**
        - **Decision Point**: Routes based on risk level and business rules
        - **Low Risk**: Direct to execution
        - **Medium Risk**: Human review required
        - **High Risk**: Escalation to senior management
        
        #### **5. Execution & Confirmation**
        - **Payment Execution**: Core banking API integration
        - **Transaction Processing**: Real-time payment processing
        - **Confirmation**: Success notification and audit trail
        """)
    
    with tab2:
        st.markdown("""
        #### **Intent Agent (Retriever-Augmented)**
        - **Purpose**: Parse natural language payment instructions
        - **Capabilities**: NLP processing, entity extraction, intent classification
        - **Input**: Free-form text instructions
        - **Output**: Structured payment data (amount, accounts, purpose, urgency)
        
        #### **Verification Agent (Document Classifier)**
        - **Purpose**: Validate accounts and compliance status
        - **Capabilities**: Account validation, compliance checking, data enrichment
        - **Input**: Account details, payment amount
        - **Output**: Validation status, compliance flags, risk indicators
        
        #### **Anomaly Agent (AI Supervisor)**
        - **Purpose**: Detect unusual patterns and assess risk
        - **Capabilities**: Pattern analysis, anomaly detection, risk scoring
        - **Input**: Payment data, historical patterns, user behavior
        - **Output**: Anomaly score, risk level, pattern analysis
        
        #### **Decision Agent (Workflow Orchestrator)**
        - **Purpose**: Route payments based on risk and business rules
        - **Capabilities**: Rule evaluation, routing logic, escalation triggers
        - **Input**: Risk scores, compliance status, business rules
        - **Output**: Routing decision, escalation requirements
        """)
    
    with tab3:
        st.markdown("""
        #### **Treasury Operations (Human Review)**
        - **Trigger**: Medium-risk payments (>$100K, <$1M)
        - **Process**: Manual review of payment details and risk factors
        - **Tools**: Scenario summary dashboard, decision journal
        - **Decision**: Approve, reject, or escalate further
        - **SLA**: 15-minute response time
        
        #### **Senior Management (Escalation)**
        - **Trigger**: High-risk payments (>$1M) or complex scenarios
        - **Process**: Executive review with full context and analysis
        - **Tools**: Comprehensive audit trail, risk analysis reports
        - **Decision**: Final approval authority
        - **SLA**: 30-minute response time
        
        #### **Compliance Team (Oversight)**
        - **Role**: Monitor overall compliance and audit processes
        - **Access**: Real-time monitoring dashboard, audit reports
        - **Responsibilities**: Policy updates, compliance training, audit reviews
        """)
    
    with tab4:
        st.markdown("""
        #### **Input Data Sources**
        - **User Instructions**: Natural language payment requests
        - **Account Data**: Customer account information and balances
        - **Compliance Data**: Sanctions lists, KYC status, AML flags
        - **Historical Data**: Previous transactions, user patterns, risk indicators
        
        #### **Processing Data**
        - **Structured Payment Data**: Parsed and validated payment details
        - **Risk Scores**: Anomaly detection and risk assessment results
        - **Compliance Status**: Real-time compliance check results
        - **Decision Context**: All relevant data for human review
        
        #### **Output Data**
        - **Transaction Records**: Complete payment transaction details
        - **Audit Trails**: Comprehensive logging of all decisions and actions
        - **Compliance Reports**: Regulatory reporting and audit documentation
        - **Monitoring Data**: Real-time performance and compliance metrics
        
        #### **Data Flow Patterns**
        - **Real-time Processing**: Immediate data validation and risk assessment
        - **Asynchronous Review**: Human review processes with SLA tracking
        - **Batch Reporting**: Daily compliance and audit reports
        - **Event Streaming**: Real-time monitoring and alerting
        """)
    
    # Process Metrics
    st.markdown("---")
    st.markdown("### Process Performance Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Avg Processing Time", "2.3 min", "0.2 min")
    with col2:
        st.metric("Human Review Rate", "15.2%", "2.1%")
    with col3:
        st.metric("Escalation Rate", "3.8%", "0.5%")
    with col4:
        st.metric("Success Rate", "99.7%", "0.1%")

@st.cache_data(ttl=1800)  # Cache for 30 minutes
def generate_k8s_manifest(config):
    """Generate Kubernetes manifest for the pattern configuration"""
    pattern_name = config['pattern']
    metadata = config['metadata']
    devops_config = config['devops']
    
    manifest = {
        'apiVersion': 'apps/v1',
        'kind': 'Deployment',
        'metadata': {
            'name': f'{pattern_name}-pattern',
            'labels': {
                'app': pattern_name,
                'pattern': 'agentic-ai',
                'version': config['version']
            }
        },
        'spec': {
            'replicas': devops_config['deployment']['replicas'],
            'selector': {
                'matchLabels': {
                    'app': pattern_name
                }
            },
            'template': {
                'metadata': {
                    'labels': {
                        'app': pattern_name,
                        'pattern': 'agentic-ai'
                    }
                },
                'spec': {
                    'containers': [{
                        'name': f'{pattern_name}-container',
                        'image': f'agentic-ai/{pattern_name}:{config["version"]}',
                        'ports': [{
                            'containerPort': 8080,
                            'name': 'http'
                        }],
                        'resources': {
                            'requests': devops_config['deployment']['resources'],
                            'limits': devops_config['deployment']['resources']
                        },
                        'env': [
                            {'name': 'PATTERN_NAME', 'value': pattern_name},
                            {'name': 'VERSION', 'value': config['version']},
                            {'name': 'ENVIRONMENT', 'value': devops_config['deployment']['environment']}
                        ],
                        'livenessProbe': {
                            'httpGet': {
                                'path': devops_config['monitoring']['health_check_endpoint'],
                                'port': 8080
                            },
                            'initialDelaySeconds': 30,
                            'periodSeconds': 10
                        },
                        'readinessProbe': {
                            'httpGet': {
                                'path': devops_config['monitoring']['health_check_endpoint'],
                                'port': 8080
                            },
                            'initialDelaySeconds': 5,
                            'periodSeconds': 5
                        }
                    }]
                }
            }
        }
    }
    
    # Add Service
    service = {
        'apiVersion': 'v1',
        'kind': 'Service',
        'metadata': {
            'name': f'{pattern_name}-service',
            'labels': {
                'app': pattern_name
            }
        },
        'spec': {
            'selector': {
                'app': pattern_name
            },
            'ports': [{
                'port': 80,
                'targetPort': 8080,
                'name': 'http'
            }],
            'type': 'ClusterIP'
        }
    }
    
    # Add ConfigMap for observability
    configmap = {
        'apiVersion': 'v1',
        'kind': 'ConfigMap',
        'metadata': {
            'name': f'{pattern_name}-config',
            'labels': {
                'app': pattern_name
            }
        },
        'data': {
            'pattern_config.json': json.dumps(config, indent=2),
            'prometheus.yml': f'''
global:
  scrape_interval: 15s
scrape_configs:
  - job_name: '{pattern_name}-pattern'
    static_configs:
      - targets: ['{pattern_name}-service:80']
    metrics_path: '/metrics'
    scrape_interval: 5s
'''
        }
    }
    
    # Combine all manifests
    combined_manifest = {
        'deployment': manifest,
        'service': service,
        'configmap': configmap
    }
    
    return yaml.dump(combined_manifest, default_flow_style=False, indent=2)

@st.cache_data(ttl=300)  # Cache for 5 minutes
def warm_cache():
    """Pre-warm commonly used caches for better performance"""
    # Pre-load commonly used data
    landing_data = get_landing_page_data()
    payment_data = get_payment_instruction_data()
    
    return {
        'landing_ready': True,
        'payment_ready': True
    }

def main():
    # Initialize session state with performance optimizations
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 'landing'

    # Performance optimization: Cache expensive computations
    if 'agent_data_cache' not in st.session_state:
        st.session_state['agent_data_cache'] = None
    if 'last_cache_time' not in st.session_state:
        st.session_state['last_cache_time'] = 0
    if 'chart_cache' not in st.session_state:
        st.session_state['chart_cache'] = {}
    if 'filtered_agents_cache' not in st.session_state:
        st.session_state['filtered_agents_cache'] = None
    if 'performance_mode' not in st.session_state:
        st.session_state['performance_mode'] = True
    
    # Warm up caches for better performance
    if st.session_state.get('performance_mode', True):
        warm_cache()
    
    # iOS-style Sidebar navigation
    with st.sidebar:
        
        # Agentic Operating System Section
        st.markdown("""
        <div style="margin-bottom: 1.5rem;">
            <h3 style="color: #6e6e73; font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; font-weight: 600; margin: 0 0 1rem 0; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.5px;">Agentic Operating System</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Agentic Catalog", key="nav_catalog"):
            st.session_state['current_page'] = 'landing'
            st.rerun()
        if st.button("Governance Workflow", key="nav_governance"):
            st.session_state['current_page'] = 'governance'
            st.rerun()
        if st.button("Escalation Console", key="nav_escalation"):
            st.session_state['current_page'] = 'escalation'
            st.rerun()
        if st.button("Audit & Reporting", key="nav_audit"):
            st.session_state['current_page'] = 'audit'
            st.rerun()
        
        # Payment Workflow Section
        st.markdown("""
        <div style="margin: 2rem 0 1.5rem 0; padding: 1.2rem; background: linear-gradient(135deg, #e3f2fd 0%, #f0f8ff 100%); border-radius: 16px; border: 1px solid rgba(0, 122, 255, 0.2); box-shadow: 0 2px 12px rgba(0, 122, 255, 0.1);">
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                <h3 style="color: #007AFF; font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; font-weight: 700; margin: 0; font-size: 1rem;">Payment Workflow</h3>
            </div>
            <p style="color: #6e6e73; font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; font-size: 0.8rem; margin: 0; line-height: 1.4;">High-value payment processing with anomaly detection and governance</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Payment Instruction", key="nav_payment"):
            st.session_state['current_page'] = 'payment_instruction'
            st.rerun()
        if st.button("Intent Verification", key="nav_intent"):
            st.session_state['current_page'] = 'intent_verification'
            st.rerun()
        if st.button("Scenario Summary", key="nav_scenario"):
            st.session_state['current_page'] = 'scenario_summary'
            st.rerun()
        if st.button("Payment Escalation", key="nav_payment_escalation"):
            st.session_state['current_page'] = 'payment_escalation'
            st.rerun()
        if st.button("Payment Audit", key="nav_payment_audit"):
            st.session_state['current_page'] = 'payment_audit'
            st.rerun()
        if st.button("Process Flow", key="nav_process_flow"):
            st.session_state['current_page'] = 'process_flow'
            st.rerun()
        
        # Performance Settings (moved to end)
        st.markdown("""
        <div style="margin-top: 2rem; margin-bottom: 1.5rem;">
            <h3 style="color: #6e6e73; font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; font-weight: 600; margin: 0 0 1rem 0; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.5px;">Performance</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Performance mode toggle
        performance_mode = st.checkbox("Performance Mode", value=st.session_state.get('performance_mode', True), 
                                     help="Enable caching and optimizations for better performance")
        st.session_state['performance_mode'] = performance_mode
        
        if st.button("Clear Cache"):
            st.cache_data.clear()
            st.cache_resource.clear()
            st.success("Cache cleared!")
            st.rerun()
        
        # Show cache status
        if st.session_state.get('performance_mode', True):
            st.info("Performance Mode: Active")
        else:
            st.warning("âš ï¸ Performance Mode: Disabled")
    
    # Route to appropriate page
    if st.session_state['current_page'] == 'landing':
        landing_page()
    elif st.session_state['current_page'] == 'agent_detail':
        agent_detail_page()
    elif st.session_state['current_page'] == 'governance':
        governance_workflow()
    elif st.session_state['current_page'] == 'escalation':
        escalation_console()
    elif st.session_state['current_page'] == 'audit':
        audit_reporting()
    elif st.session_state['current_page'] == 'payment_instruction':
        payment_instruction_entry()
    elif st.session_state['current_page'] == 'intent_verification':
        intent_verification()
    elif st.session_state['current_page'] == 'scenario_summary':
        scenario_summary()
    elif st.session_state['current_page'] == 'payment_escalation':
        payment_escalation()
    elif st.session_state['current_page'] == 'payment_audit':
        payment_audit()
    elif st.session_state['current_page'] == 'process_flow':
        process_flow_diagram()

if __name__ == "__main__":
    main()
