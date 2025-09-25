# Agentic AI Catalog

A comprehensive Streamlit application for managing and monitoring AI agents in an enterprise environment. This application provides a complete governance, monitoring, and audit system for AI agents.

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