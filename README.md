# Agentic AI Catalog

A comprehensive Streamlit application for managing and monitoring AI agents in an enterprise environment. This application provides a complete governance, monitoring, and audit system for AI agents.

## Application Summary

The Agentic AI Catalog is a sophisticated enterprise-grade platform designed to manage, monitor, and govern AI agents at scale. Built with Streamlit, it provides a complete lifecycle management system for AI agents, from initial registration through production deployment and ongoing monitoring.

### Key Capabilities

**Agent Lifecycle Management**
- Complete agent registration and metadata management
- Pattern-based agent classification and organization
- Lifecycle stage tracking (Draft, Pilot, Approved)
- Risk assessment and compliance monitoring

**Governance & Compliance**
- Policy-as-Code implementation with YAML/JSON support
- Real-time policy validation and enforcement
- Multi-framework compliance tracking (GDPR, OSFI, FINTRAC)
- Audit trail generation and compliance reporting

**Runtime Monitoring & Control**
- Real-time agent performance monitoring
- Escalation management and incident handling
- Guardrail enforcement and safety controls
- Resource usage tracking and optimization

**Payment Processing Workflow**
- End-to-end payment instruction processing
- Natural language intent extraction and parsing
- AI-powered anomaly detection and risk assessment
- Multi-level approval workflows with human oversight

**Enterprise Integration**
- Tool ecosystem management and cataloging
- API integration and connector frameworks
- Role-based access control (RBAC)
- Scalable architecture for enterprise deployment

### Target Users

- **AI/ML Engineers**: Agent development and deployment
- **Compliance Officers**: Policy management and audit oversight
- **Operations Teams**: Runtime monitoring and incident management
- **Business Stakeholders**: Performance dashboards and reporting
- **Financial Controllers**: Payment processing and risk management

### Technology Stack

- **Frontend**: Streamlit with custom iOS-style UI components
- **Data Visualization**: Plotly for interactive charts and diagrams
- **Data Processing**: Pandas for data manipulation and analysis
- **Architecture**: Modular design with caching and performance optimization
- **Integration**: Support for various AI/ML frameworks and enterprise systems

## Features

### 🏠 Landing Page
- Search and filter agents by pattern, risk level, and lifecycle stage
- Agent cards with status badges (Approved, Pilot, Draft)
- Real-time statistics and metrics

### 📋 Agent Detail Pages
- **Overview Tab**: Business use case, dependencies, owner, lifecycle
- **Governance Tab**: Policies (YAML editor), compliance tags, approval history
- **Runtime Tab**: Guardrails, monitoring metrics, control buttons
- **Escalation Tab**: Escalation levels, notification channels
- **Audit Tab**: Logs, decision journals, escalation history

### 🔧 Governance Workflow
- Metadata form for new agent registration
- Policy-as-Code editor with YAML/JSON support
- Real-time validation with error reporting
- Submit for review or save as draft functionality

### 📊 Runtime Monitoring Dashboard
- Key metrics: API calls, guardrail triggers, escalations
- Interactive charts showing escalation trends over time
- Agent health status monitoring
- Control buttons for pausing agents and kill switches

### 🚨 Escalation Console
- Timeline view of escalation levels and status
- Context panel with input/output details
- Action buttons: Resolve, Reassign, Escalate Further
- Decision journal entry system

### 📈 Audit & Reporting
- Compliance heatmap with GDPR, OSFI, FINTRAC status
- Filterable reports by agent, division, and compliance framework
- Export options for PDF and CSV reports
- Compliance summary with progress indicators

### 💳 Payment Process Workflow
The application includes a comprehensive payment processing workflow that demonstrates AI agent orchestration in a real-world enterprise scenario:

#### Workflow Overview
The payment process workflow showcases how multiple AI agents work together to handle high-value payment processing with built-in anomaly detection and governance controls.

#### Key Components
1. **Payment Instruction Entry**: Natural language payment instruction parsing with intent extraction
2. **Intent Verification**: AI-powered anomaly detection and risk assessment
3. **Scenario Summary**: Comprehensive review of payment details and risk factors
4. **Payment Escalation**: Automated escalation handling with human oversight
5. **Payment Audit**: Compliance monitoring and audit trail generation

#### Process Flow Steps
1. **Input Processing**: Parse natural language payment instructions (e.g., "Send $2M CAD to Vendor X by Friday")
2. **Intent Extraction**: Extract structured data including amount, beneficiary, date, and urgency
3. **Risk Assessment**: AI agents analyze payment for anomalies and compliance issues
4. **Approval Workflow**: Multi-level approval process with automated and human checkpoints
5. **Execution**: Secure payment processing with real-time monitoring
6. **Audit Trail**: Complete documentation and compliance reporting

#### AI Agents Involved
- **Payment Parser Agent**: Extracts structured data from natural language
- **Risk Assessment Agent**: Analyzes payment for anomalies and compliance
- **Approval Orchestrator**: Manages multi-level approval workflow
- **Compliance Monitor**: Ensures regulatory compliance (GDPR, OSFI, FINTRAC)
- **Audit Logger**: Maintains comprehensive audit trails

#### Human Interactions
- **Financial Controller**: Reviews high-value payments and complex scenarios
- **Compliance Officer**: Validates regulatory compliance and risk assessments
- **Operations Team**: Handles escalations and exception processing
- **Audit Team**: Reviews and validates payment processing logs

### 🔄 Process Flow Diagram
- **Executive-style Visualization**: Professional process flow diagram showing end-to-end workflows
- **Interactive Elements**: Clickable nodes with detailed information
- **Multi-tab Interface**: Separate tabs for workflow steps, AI agents, human interactions, and data flow
- **Real-time Updates**: Dynamic diagram generation based on current agent configurations
- **Export Capabilities**: Download process flow diagrams in various formats

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Agentic_Catalog
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Streamlit application:
```bash
streamlit run app.py
```

4. Open your browser and navigate to `http://localhost:8501`

## Usage

### Navigation
Use the sidebar navigation to switch between different sections:
- **Landing Page**: Browse and search agents
- **Governance Workflow**: Create new agent cards
- **Runtime Monitoring**: Monitor agent performance
- **Escalation Console**: Manage escalations
- **Audit & Reporting**: View compliance reports

### Agent Management
1. **View Agent Details**: Click "View Details" on any agent card
2. **Create New Agent**: Use the Governance Workflow page
3. **Monitor Performance**: Use the Runtime Monitoring dashboard
4. **Handle Escalations**: Use the Escalation Console

### Key Features
- **Real-time Search**: Filter agents by name, pattern, risk, or lifecycle
- **Interactive Charts**: Visualize escalation trends and metrics
- **Policy Management**: Edit and validate agent policies in YAML
- **Compliance Tracking**: Monitor GDPR, OSFI, and FINTRAC compliance
- **Export Capabilities**: Generate PDF and CSV reports

## Sample Data

The application includes sample data for demonstration:
- **Retriever Agent v1**: Approved agent for document routing
- **Orchestrator Agent v2**: Pilot agent for workflow automation
- **Compliance Monitor v1**: Draft agent for regulatory checks

## Customization

The application can be easily customized by:
- Modifying the `load_agent_data()` function to connect to your data source
- Updating the compliance frameworks in the audit section
- Adding new agent patterns and risk levels
- Customizing the policy validation rules

## Requirements

- Python 3.7+
- Streamlit 1.28.1
- Pandas 2.1.3
- Plotly 5.17.0

## License

This project is licensed under the MIT License.