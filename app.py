import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

# Page configuration - iOS style
st.set_page_config(
    page_title="Agentic Catalog",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/jinojtitus/Agentic_Catalog',
        'Report a bug': 'https://github.com/jinojtitus/Agentic_Catalog/issues',
        'About': "Agentic AI Catalog - iOS-style interface for managing AI agents"
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
@st.cache_data
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
                'monitoring': {'callsThisWeek': 1245, 'guardrailTriggers': 3, 'escalations': 1, 'avgResponseTime': '245ms', 'uptime': '99.8%'}
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
                'monitoring': {'callsThisWeek': 892, 'guardrailTriggers': 5, 'escalations': 2, 'avgResponseTime': '1.2s', 'uptime': '98.5%'}
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
                'monitoring': {'callsThisWeek': 0, 'guardrailTriggers': 0, 'escalations': 0, 'avgResponseTime': 'N/A', 'uptime': 'N/A'}
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
                'monitoring': {'callsThisWeek': 23, 'guardrailTriggers': 7, 'escalations': 3, 'avgResponseTime': '3.2s', 'uptime': '99.9%'}
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
                'monitoring': {'callsThisWeek': 12, 'guardrailTriggers': 2, 'escalations': 1, 'avgResponseTime': '45s', 'uptime': '99.5%'}
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
                'monitoring': {'callsThisWeek': 2156, 'guardrailTriggers': 12, 'escalations': 3, 'avgResponseTime': '2.1s', 'uptime': '99.9%'}
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
                    'monitoring': 'Prometheus + Grafana',
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
                'monitoring': {'callsThisWeek': 156, 'guardrailTriggers': 8, 'escalations': 5, 'avgResponseTime': '1.8s', 'uptime': '99.7%'}
            }
        ]
    }

def get_status_badge(status):
    status_map = {
        'approved': {'text': 'Approved ✅', 'class': 'status-approved'},
        'pilot': {'text': 'Pilot 🟡', 'class': 'status-pilot'},
        'draft': {'text': 'Draft 📝', 'class': 'status-draft'}
    }
    return status_map.get(status, {'text': status, 'class': ''})

def landing_page():
    st.markdown('<h1 class="main-header">📱 Agentic Catalog</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #6e6e73; margin-bottom: 2rem; font-family: \'Inter\', -apple-system, BlinkMacSystemFont, \'Segoe UI\', sans-serif;">Manage and monitor your AI agents with iOS-style elegance</p>', unsafe_allow_html=True)
    
    data = load_agent_data()
    agents = data['agents']
    
    # Search and filters
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        search_term = st.text_input("🔍 Search by pattern, risk, domain...", key="search")
    
    with col2:
        pattern_filter = st.selectbox("Pattern Type", ["All"] + list(set([agent['patternName'] for agent in agents])))
    
    with col3:
        risk_filter = st.selectbox("Risk Level", ["All"] + list(set([agent['risk'] for agent in agents])))
    
    with col4:
        lifecycle_filter = st.selectbox("Lifecycle", ["All"] + list(set([agent['status'] for agent in agents])))
    
    # Filter agents
    filtered_agents = agents
    if search_term:
        filtered_agents = [agent for agent in filtered_agents if 
                          search_term.lower() in agent['name'].lower() or 
                          search_term.lower() in agent['useCase'].lower() or 
                          search_term.lower() in agent['patternName'].lower() or
                          search_term.lower() in agent['patternType'].lower()]
    
    if pattern_filter != "All":
        filtered_agents = [agent for agent in filtered_agents if agent['patternName'] == pattern_filter]
    
    if risk_filter != "All":
        filtered_agents = [agent for agent in filtered_agents if agent['risk'] == risk_filter]
    
    if lifecycle_filter != "All":
        filtered_agents = [agent for agent in filtered_agents if agent['status'] == lifecycle_filter]
    
    # Display agent cards
    st.markdown("### Agent Cards")
    
    cols = st.columns(2)
    for i, agent in enumerate(filtered_agents):
        with cols[i % 2]:
            status_info = get_status_badge(agent['status'])
            pattern_type_emoji = {
                'retrieval': '🔍',
                'orchestration': '🔄',
                'monitoring': '📊',
                'reasoning': '🧠',
                'classification': '📋',
                'supervision': '👥'
            }.get(agent['patternType'], '🤖')
            
            # Create expandable agent card
            with st.expander(f"{pattern_type_emoji} {agent['name']} - {status_info['text']}", expanded=False):
                # Agent Overview tab
                tab1, tab2, tab3, tab4, tab5 = st.tabs(["Agent Overview", "Pattern", "Policies", "Runtime", "Escalation"])
                
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
                                st.success(f"✅ {tag.upper()}")
                            else:
                                st.error(f"❌ {tag.upper()}")
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
                    st.markdown("**Governance Policies:**")
                    st.code(agent['governanceHooks']['policies'], language='yaml')
                    
                    st.markdown("**Compliance Status:**")
                    compliance_tags = agent['governanceHooks']['complianceTags']
                    for tag, status in compliance_tags.items():
                        if status:
                            st.success(f"✅ {tag}")
                        else:
                            st.error(f"❌ {tag}")
                    
                    st.markdown("**Approval History:**")
                    st.write(" → ".join(agent['governanceHooks']['approvalHistory']))
                
                with tab3:
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
                    st.write(f"Enabled: {'✅' if kill_switch['enabled'] else '❌'}")
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
                            st.success(f"Level {level['level']}: {level['action']} ✅")
                        elif level['status'] == 'pending':
                            st.warning(f"Level {level['level']}: {level['action']} ⏳")
                        else:
                            st.info(f"Level {level['level']}: {level['action']} ⏸️")
                        st.write(f"*Timeout: {level['timeout']}*")
                        st.write("---")
                    
                    st.markdown("**Notification Channels:**")
                    for channel in agent['escalationMechanisms']['notificationChannels']:
                        st.write(f"• {channel}")
                    
                    st.markdown("**Decision Journals:**")
                    decision_journals = agent['escalationMechanisms']['decisionJournals']
                    st.write(f"Enabled: {'✅' if decision_journals['enabled'] else '❌'}")
                    st.write(f"Required: {'✅' if decision_journals['required'] else '❌'}")
                    st.write(f"Template: {decision_journals['template']}")
            
    
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
    st.markdown("### 💳 High-Value Payment Processing Workflow")
    st.markdown("Experience the complete end-to-end payment processing workflow with anomaly detection, governance, and human-in-the-loop review.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🚀 Start Payment Workflow", type="primary"):
            st.session_state['current_page'] = 'payment_instruction'
            st.rerun()
    with col2:
        if st.button("📊 View Payment Audit"):
            st.session_state['current_page'] = 'payment_audit'
            st.rerun()
    with col3:
        if st.button("🚨 Payment Escalations"):
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
        'retrieval': '🔍',
        'orchestration': '🔄',
        'monitoring': '📊',
        'reasoning': '🧠'
    }.get(agent['patternType'], '🤖')
    
    st.markdown(f"<h1>{pattern_type_emoji} Agent: {agent['name']} <span class='status-badge {status_info['class']}'>{status_info['text']}</span></h1>", unsafe_allow_html=True)
    st.markdown(f"**Pattern:** {agent['patternName']} ({agent['patternType'].title()})")
    
    if st.button("← Back to Agentic Catalog"):
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
                    st.success(f"✅ {tag}")
                else:
                    st.error(f"❌ {tag}")
        
        st.markdown("### Approval Status")
        approval_history = agent['governanceHooks']['approvalHistory']
        for i, status in enumerate(approval_history):
            if i < len(approval_history) - 1:
                st.write(f"**{status}** →")
            else:
                st.write(f"**{status}** ✅")
        
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
        st.write(f"**Kill Switch Enabled:** {'✅' if kill_switch['enabled'] else '❌'}")
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
                st.success(f"**Level {level['level']}:** {level['action']} ✅")
            elif level['status'] == 'pending':
                st.warning(f"**Level {level['level']}:** {level['action']} ⏳")
            else:
                st.info(f"**Level {level['level']}:** {level['action']} ⏸️")
            
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
            st.write(f"**Enabled:** {'✅' if decision_journals['enabled'] else '❌'}")
        with col2:
            st.write(f"**Required:** {'✅' if decision_journals['required'] else '❌'}")
        with col3:
            st.write(f"**Template:** {decision_journals['template']}")
    
    with tab5:
        st.markdown("### Logs")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📥 Download CSV Logs"):
                st.success("CSV download initiated")
        with col2:
            if st.button("📊 View Live Logs"):
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
                st.success(f"✅ {tag} - Compliant")
            else:
                st.error(f"❌ {tag} - Non-compliant")

def governance_workflow():
    st.markdown('<h1 class="main-header">Governance Workflow – New Agent Card</h1>', unsafe_allow_html=True)
    
    if st.button("← Back to Agentic Catalog"):
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

def runtime_monitoring():
    st.markdown('<h1 class="main-header">Runtime Monitoring Dashboard</h1>', unsafe_allow_html=True)
    
    if st.button("← Back to Agentic Catalog"):
        st.session_state['current_page'] = 'landing'
        st.rerun()
    
    # Load agent data
    data = load_agent_data()
    agents = data['agents']
    
    # Overall metrics summary
    st.markdown("### 📊 System Overview")
    total_calls = sum(agent['monitoring']['callsThisWeek'] for agent in agents)
    total_escalations = sum(agent['monitoring']['escalations'] for agent in agents)
    total_guardrail_triggers = sum(agent['monitoring']['guardrailTriggers'] for agent in agents)
    avg_uptime = sum(float(agent['monitoring']['uptime'].replace('%', '')) for agent in agents) / len(agents)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total API Calls", f"{total_calls:,}")
    with col2:
        st.metric("Total Escalations", total_escalations)
    with col3:
        st.metric("Guardrail Triggers", total_guardrail_triggers)
    with col4:
        st.metric("Avg Uptime", f"{avg_uptime:.1f}%")
    
    st.markdown("---")
    
    # Agent-specific monitoring cards
    st.markdown("### 🤖 Agent Performance Monitoring")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.selectbox("Filter by Status", ["All"] + list(set(agent['status'] for agent in agents)))
    with col2:
        pattern_filter = st.selectbox("Filter by Pattern", ["All"] + list(set(agent['patternType'] for agent in agents)))
    with col3:
        risk_filter = st.selectbox("Filter by Risk Level", ["All"] + list(set(agent['risk'] for agent in agents)))
    
    # Filter agents
    filtered_agents = agents
    if status_filter != "All":
        filtered_agents = [a for a in filtered_agents if a['status'] == status_filter]
    if pattern_filter != "All":
        filtered_agents = [a for a in filtered_agents if a['patternType'] == pattern_filter]
    if risk_filter != "All":
        filtered_agents = [a for a in filtered_agents if a['risk'] == risk_filter]
    
    # Display agent monitoring cards
    for agent in filtered_agents:
        with st.expander(f"🔍 {agent['name']} - {agent['patternName']} ({agent['status'].title()})", expanded=False):
            
            # Agent header with status indicators
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            with col1:
                st.markdown(f"**{agent['name']}** ({agent['patternType'].title()})")
                st.markdown(f"*{agent['businessUseCase']}*")
            with col2:
                # Health status based on metrics
                uptime = float(agent['monitoring']['uptime'].replace('%', ''))
                if uptime >= 99.0:
                    st.success("🟢 Healthy")
                elif uptime >= 95.0:
                    st.warning("🟡 Warning")
                else:
                    st.error("🔴 Critical")
            with col3:
                st.markdown(f"**Risk:** {agent['risk']}")
            with col4:
                st.markdown(f"**Owner:** {agent['owner']}")
            
            # Performance metrics in tabs
            tab1, tab2, tab3, tab4 = st.tabs(["📈 Performance", "🛡️ Guardrails", "📊 Trends", "⚙️ Controls"])
            
            with tab1:
                st.markdown("#### Key Performance Indicators")
                
                # Main metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric(
                        "API Calls (7d)", 
                        agent['monitoring']['callsThisWeek'],
                        delta=f"+{agent['monitoring']['callsThisWeek'] - 100}" if agent['monitoring']['callsThisWeek'] > 100 else None
                    )
                with col2:
                    st.metric(
                        "Avg Response Time", 
                        f"{agent['monitoring'].get('avgResponseTime', '245')}ms",
                        delta="-15ms" if agent['monitoring'].get('avgResponseTime', 245) < 250 else "+5ms"
                    )
                with col3:
                    st.metric(
                        "Uptime", 
                        agent['monitoring']['uptime'],
                        delta="+0.2%" if float(agent['monitoring']['uptime'].replace('%', '')) > 99.0 else "-0.5%"
                    )
                with col4:
                    st.metric(
                        "Success Rate", 
                        f"{agent['monitoring'].get('successRate', '98.5')}%",
                        delta="+1.2%" if agent['monitoring'].get('successRate', 98.5) > 97.0 else "-0.8%"
                    )
                
                # Additional metrics
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Processing Stats:**")
                    st.write(f"• Total Transactions: {agent['monitoring'].get('totalTransactions', 1240):,}")
                    st.write(f"• Peak Load: {agent['monitoring'].get('peakLoad', '2.3K')} req/min")
                    st.write(f"• Error Rate: {agent['monitoring'].get('errorRate', '0.8')}%")
                
                with col2:
                    st.markdown("**Resource Usage:**")
                    st.write(f"• CPU Usage: {agent['monitoring'].get('cpuUsage', '45')}%")
                    st.write(f"• Memory: {agent['monitoring'].get('memoryUsage', '2.1')}GB")
                    st.write(f"• Queue Depth: {agent['monitoring'].get('queueDepth', '12')}")
            
            with tab2:
                st.markdown("#### Guardrail Status")
                
                # Guardrail triggers
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(
                        "Guardrail Triggers", 
                        agent['monitoring']['guardrailTriggers'],
                        delta=f"+{agent['monitoring']['guardrailTriggers'] - 2}" if agent['monitoring']['guardrailTriggers'] > 2 else None
                    )
                with col2:
                    st.metric(
                        "Escalations", 
                        agent['monitoring']['escalations'],
                        delta=f"+{agent['monitoring']['escalations'] - 1}" if agent['monitoring']['escalations'] > 1 else None
                    )
                
                # Guardrail details
                st.markdown("**Active Guardrails:**")
                guardrails = agent['runtimeGuardrails']
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Input Filters:**")
                    for filter_type in guardrails['inputFilters']:
                        st.write(f"• {filter_type}")
                    
                    st.markdown("**Output Validators:**")
                    for validator in guardrails['outputValidators']:
                        st.write(f"• {validator}")
                
                with col2:
                    st.markdown("**Rate Controls:**")
                    for control, value in guardrails['rateControls'].items():
                        st.write(f"• {control.replace('_', ' ').title()}: {value}")
                    
                    st.markdown("**Kill Switch:**")
                    kill_switch = guardrails['killSwitch']
                    status = "🟢 Active" if kill_switch['enabled'] else "🔴 Disabled"
                    st.write(f"• Status: {status}")
                    for trigger in kill_switch['triggers']:
                        st.write(f"  - {trigger}")
                
                # Recent guardrail events
                st.markdown("**Recent Events:**")
                events = [
                    {"time": "14:32:15", "type": "Input Filter", "message": "PII detected in input", "severity": "warning"},
                    {"time": "14:28:42", "type": "Rate Control", "message": "Rate limit approaching", "severity": "info"},
                    {"time": "14:25:18", "type": "Output Validator", "message": "Confidence below threshold", "severity": "warning"}
                ]
                
                for event in events:
                    severity_icon = "⚠️" if event['severity'] == 'warning' else "ℹ️" if event['severity'] == 'info' else "🚨"
                    st.write(f"{severity_icon} **{event['time']}** - {event['type']}: {event['message']}")
            
            with tab3:
                st.markdown("#### Performance Trends")
                
                # Generate sample trend data for the last 7 days
                dates = pd.date_range('2025-01-15', periods=7, freq='D')
                
                # API calls trend
                calls_trend = [agent['monitoring']['callsThisWeek'] + i*10 for i in range(7)]
                calls_df = pd.DataFrame({'Date': dates, 'API Calls': calls_trend})
                
                fig_calls = px.line(calls_df, x='Date', y='API Calls', title='API Calls Trend (7 days)')
                st.plotly_chart(fig_calls, use_container_width=True)
                
                # Response time trend
                response_times = [245, 238, 252, 241, 248, 235, 242]
                response_df = pd.DataFrame({'Date': dates, 'Response Time (ms)': response_times})
                
                fig_response = px.line(response_df, x='Date', y='Response Time (ms)', title='Response Time Trend (7 days)')
                st.plotly_chart(fig_response, use_container_width=True)
                
                # Error rate trend
                error_rates = [0.8, 1.2, 0.6, 0.9, 1.1, 0.7, 0.8]
                error_df = pd.DataFrame({'Date': dates, 'Error Rate (%)': error_rates})
                
                fig_error = px.line(error_df, x='Date', y='Error Rate (%)', title='Error Rate Trend (7 days)')
                st.plotly_chart(fig_error, use_container_width=True)
            
            with tab4:
                st.markdown("#### Runtime Controls")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Agent Controls:**")
                    if st.button(f"⏸️ Pause {agent['name']}", key=f"pause_{agent['id']}"):
                        st.warning(f"{agent['name']} paused")
                    
                    if st.button(f"🔄 Restart {agent['name']}", key=f"restart_{agent['id']}"):
                        st.info(f"{agent['name']} restarted")
                    
                    if st.button(f"🔧 Maintenance Mode", key=f"maintenance_{agent['id']}"):
                        st.warning(f"{agent['name']} in maintenance mode")
                
                with col2:
                    st.markdown("**Emergency Controls:**")
                    if st.button(f"🚨 Kill Switch", key=f"kill_{agent['id']}", type="secondary"):
                        st.error(f"Kill switch activated for {agent['name']}")
                    
                    if st.button(f"🛡️ Force Guardrails", key=f"guardrails_{agent['id']}"):
                        st.warning(f"Guardrails enforced for {agent['name']}")
                
                # Configuration
                st.markdown("**Runtime Configuration:**")
                with st.expander("View Current Configuration"):
                    st.json({
                        "max_concurrent_requests": agent['monitoring'].get('maxConcurrent', 100),
                        "timeout_seconds": agent['monitoring'].get('timeout', 30),
                        "retry_attempts": agent['monitoring'].get('retryAttempts', 3),
                        "circuit_breaker_threshold": agent['monitoring'].get('circuitBreaker', 5)
                    })
    
    # System-wide charts
    st.markdown("---")
    st.markdown("### 📈 System-Wide Trends")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Escalations over time
        escalation_data = pd.DataFrame({
            'Date': pd.date_range('2025-01-15', periods=7, freq='D'),
            'Escalations': [0, 1, 0, 2, 0, 1, 0]
        })
        
        fig = px.line(escalation_data, x='Date', y='Escalations', title='System Escalations Over Time')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Agent health distribution
        health_data = []
        for agent in agents:
            uptime = float(agent['monitoring']['uptime'].replace('%', ''))
            if uptime >= 99.0:
                health_data.append('Healthy')
            elif uptime >= 95.0:
                health_data.append('Warning')
            else:
                health_data.append('Critical')
        
        health_counts = pd.Series(health_data).value_counts()
        fig_health = px.pie(values=health_counts.values, names=health_counts.index, title='Agent Health Distribution')
        st.plotly_chart(fig_health, use_container_width=True)

def escalation_console():
    st.markdown('<h1 class="main-header">Escalation Console</h1>', unsafe_allow_html=True)
    
    if st.button("← Back to Agentic Catalog"):
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
        status_icon = "✅" if item["Status"] == "Success" else "⏳" if item["Status"] == "Pending" else "⏸️"
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
    
    if st.button("← Back to Agentic Catalog"):
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
        'Pattern Type': ['🔍 Retrieval', '🔄 Orchestration', '📊 Monitoring', '🔄 Orchestration', '🧠 Reasoning'],
        'Division': ['Operations', 'Operations', 'Risk Management', 'Treasury Operations', 'Legal Operations'],
        'Risk Level': ['Medium', 'High', 'Low', 'High', 'High'],
        'GDPR': ['✅', '✅', '✅', '✅', '✅'],
        'OSFI': ['✅', '❌', '✅', '✅', '❌'],
        'FINTRAC': ['❌', '❌', '✅', '✅', '❌'],
        'AML': ['❌', '❌', '✅', '✅', '❌'],
        'Sanctions': ['❌', '❌', '✅', '✅', '❌'],
        'SOC2': ['✅', '✅', '✅', '✅', '✅'],
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

def payment_instruction_entry():
    st.markdown('<h1 class="main-header">Payment Instruction</h1>', unsafe_allow_html=True)
    
    if st.button("← Back to Agentic Catalog"):
        st.session_state['current_page'] = 'landing'
        st.rerun()
    
    st.markdown("### Sample Instructions")
    st.markdown("Click on any sample instruction below to populate the input field:")
    
    # Sample instructions
    sample_instructions = [
        "Send $2M CAD to Vendor X by Friday",
        "Transfer $500K USD to Supplier ABC for invoice #12345",
        "Pay $1.5M CAD to Contractor Y by end of month",
        "Wire $750K USD to International Partner Z urgently",
        "Process payment of $300K CAD to Service Provider ABC",
        "Send $2.5M CAD to Vendor X for quarterly payment",
        "Transfer $1M USD to Supplier DEF for materials",
        "Pay $400K CAD to Contractor GHI by next week"
    ]
    
    # Create clickable sample instructions
    cols = st.columns(2)
    for i, instruction in enumerate(sample_instructions):
        with cols[i % 2]:
            if st.button(f"💳 {instruction}", key=f"sample_{i}"):
                st.session_state['sample_instruction'] = instruction
                st.rerun()
    
    st.markdown("---")
    st.markdown("### Instruction Input")
    
    # Get the selected sample instruction or use default
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
            st.session_state['extracted_intent'] = {
                'amount': '$2,000,000 CAD',
                'beneficiary': 'Vendor X',
                'date': 'Friday',
                'urgency': 'High',
                'confidence': 0.92
            }
            st.session_state['current_page'] = 'intent_verification'
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
            st.success(f"Confidence: {confidence:.2f} ✅")
        elif confidence >= 0.7:
            st.warning(f"Confidence: {confidence:.2f} ⚠️")
        else:
            st.error(f"Confidence: {confidence:.2f} ❌")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Confirm Intent"):
                st.session_state['current_page'] = 'intent_verification'
                st.rerun()
        with col2:
            if st.button("Retry Parsing"):
                del st.session_state['extracted_intent']
                st.rerun()

def intent_verification():
    st.markdown('<h1 class="main-header">Intent Verification & Anomaly Detection</h1>', unsafe_allow_html=True)
    
    if st.button("← Back to Payment Instruction"):
        st.session_state['current_page'] = 'payment_instruction'
        st.rerun()
    
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
        st.warning("⚠️ Above Threshold 0.65")
    else:
        st.success("✅ Within Normal Range")
    
    # Account verification
    st.markdown("### Account Verification")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.success("✅ Source Account: RBC Treasury Ops")
    with col2:
        st.warning("⚠️ Destination Account: Vendor X (NEW)")
    with col3:
        st.success("✅ Sanctions/KYC: Clear")
    
    # Risk summary
    st.markdown("### Risk Summary")
    risk_factors = {
        'Pattern Deviation': 'Moderate',
        'Destination': 'New Account',
        'Compliance': 'Pass'
    }
    
    for factor, status in risk_factors.items():
        if status == 'Pass':
            st.success(f"✅ {factor}: {status}")
        elif status == 'Moderate':
            st.warning(f"⚠️ {factor}: {status}")
        else:
            st.info(f"ℹ️ {factor}: {status}")
    
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
    st.markdown('<h1 class="main-header">Payment Review – Scenario Summary</h1>', unsafe_allow_html=True)
    
    if st.button("← Back to Verification"):
        st.session_state['current_page'] = 'intent_verification'
        st.rerun()
    
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
            st.warning(f"⚠️ {flag}")
        else:
            st.info(f"ℹ️ {flag}")
    
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
    st.markdown('<h1 class="main-header">Escalation Console – Payment Processor Agent</h1>', unsafe_allow_html=True)
    
    if st.button("← Back to Agentic Catalog"):
        st.session_state['current_page'] = 'landing'
        st.rerun()
    
    # Escalation timeline
    st.markdown("### Escalation Timeline")
    timeline_data = [
        {"Level": 1, "Action": "Auto-retry parsing with stricter schema", "Status": "Success", "Time": "14:30:15"},
        {"Level": 2, "Action": "Escalated to Payment Supervisor Agent", "Status": "Pending", "Time": "14:32:45"},
        {"Level": 3, "Action": "Pending Human Review (Treasury Ops)", "Status": "In Progress", "Time": "14:35:20"}
    ]
    
    for item in timeline_data:
        if item["Status"] == "Success":
            st.success(f"✅ **Level {item['Level']}:** {item['Action']} - {item['Status']} at {item['Time']}")
        elif item["Status"] == "Pending":
            st.warning(f"⏳ **Level {item['Level']}:** {item['Action']} - {item['Status']} at {item['Time']}")
        else:
            st.info(f"🔄 **Level {item['Level']}:** {item['Action']} - {item['Status']} at {item['Time']}")
    
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

def payment_audit():
    st.markdown('<h1 class="main-header">Payment Audit & Compliance Dashboard</h1>', unsafe_allow_html=True)
    
    if st.button("← Back to Agentic Catalog"):
        st.session_state['current_page'] = 'landing'
        st.rerun()
    
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
        'Risk': ['⚠️', '✅', '❌', '✅', '⚠️'],
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
        'AML': ['✅', '✅', '✅'],
        'KYC': ['✅', '✅', '✅'],
        'Sanctions': ['✅', '✅', '❌'],
        'OSFI': ['✅', '✅', '✅'],
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
    
    # Export options
    st.markdown("### Export Options")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Export PDF Report"):
            st.success("PDF report export initiated")
    with col2:
        if st.button("Export CSV Data"):
            st.success("CSV data export initiated")
    
    # Anomaly trend chart
    st.markdown("### Anomaly Score Trends")
    anomaly_data = pd.DataFrame({
        'Date': pd.date_range('2025-01-15', periods=7, freq='D'),
        'Anomaly Score': [0.45, 0.52, 0.38, 0.72, 0.68, 0.55, 0.61],
        'Threshold': [0.65] * 7
    })
    
    fig = px.line(anomaly_data, x='Date', y=['Anomaly Score', 'Threshold'], 
                  title='Anomaly Score Trends Over Time')
    fig.add_hline(y=0.65, line_dash="dash", line_color="red", 
                  annotation_text="Threshold: 0.65")
    st.plotly_chart(fig, use_container_width=True)

def main():
    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 'landing'
    
    # iOS-style Sidebar navigation
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h2 style="color: #1d1d1f; font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; font-weight: 700; margin: 0;">📱 Navigation</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Agentic Operating System Section
        st.markdown("""
        <div style="margin-bottom: 1.5rem;">
            <h3 style="color: #6e6e73; font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; font-weight: 600; margin: 0 0 1rem 0; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.5px;">Agentic Operating System</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🏠 Agentic Catalog", key="nav_catalog"):
            st.session_state['current_page'] = 'landing'
            st.rerun()
        if st.button("📋 Governance Workflow", key="nav_governance"):
            st.session_state['current_page'] = 'governance'
            st.rerun()
        if st.button("📊 Runtime Monitoring", key="nav_monitoring"):
            st.session_state['current_page'] = 'monitoring'
            st.rerun()
        if st.button("🚨 Escalation Console", key="nav_escalation"):
            st.session_state['current_page'] = 'escalation'
            st.rerun()
        if st.button("📈 Audit & Reporting", key="nav_audit"):
            st.session_state['current_page'] = 'audit'
            st.rerun()
        
        # Payment Workflow Section
        st.markdown("""
        <div style="margin: 2rem 0 1.5rem 0; padding: 1.2rem; background: linear-gradient(135deg, #e3f2fd 0%, #f0f8ff 100%); border-radius: 16px; border: 1px solid rgba(0, 122, 255, 0.2); box-shadow: 0 2px 12px rgba(0, 122, 255, 0.1);">
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                <span style="font-size: 1.2rem; margin-right: 0.5rem;">💳</span>
                <h3 style="color: #007AFF; font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; font-weight: 700; margin: 0; font-size: 1rem;">Payment Workflow</h3>
            </div>
            <p style="color: #6e6e73; font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; font-size: 0.8rem; margin: 0; line-height: 1.4;">High-value payment processing with anomaly detection and governance</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("💳 Payment Instruction", key="nav_payment"):
            st.session_state['current_page'] = 'payment_instruction'
            st.rerun()
        if st.button("🔍 Intent Verification", key="nav_intent"):
            st.session_state['current_page'] = 'intent_verification'
            st.rerun()
        if st.button("📋 Scenario Summary", key="nav_scenario"):
            st.session_state['current_page'] = 'scenario_summary'
            st.rerun()
        if st.button("🚨 Payment Escalation", key="nav_payment_escalation"):
            st.session_state['current_page'] = 'payment_escalation'
            st.rerun()
        if st.button("📊 Payment Audit", key="nav_payment_audit"):
            st.session_state['current_page'] = 'payment_audit'
            st.rerun()
    
    # Route to appropriate page
    if st.session_state['current_page'] == 'landing':
        landing_page()
    elif st.session_state['current_page'] == 'agent_detail':
        agent_detail_page()
    elif st.session_state['current_page'] == 'governance':
        governance_workflow()
    elif st.session_state['current_page'] == 'monitoring':
        runtime_monitoring()
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

if __name__ == "__main__":
    main()
