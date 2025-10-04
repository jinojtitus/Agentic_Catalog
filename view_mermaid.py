import streamlit as st
import streamlit.components.v1 as components
import os

st.set_page_config(page_title="Mermaid Diagram Viewer", layout="wide")

st.title("Cash Services Process Diagrams")

# Create tabs
tab1, tab2, tab3 = st.tabs(["Deposit Processing", "Currency Processing", "Custom File"])

with tab1:
    st.header("Cash Services - Deposit Processing")
    
    # Check if file exists
    if os.path.exists("cash_services_deposit_processing.mmd"):
        with open("cash_services_deposit_processing.mmd", "r", encoding="utf-8") as f:
            deposit_mermaid_code = f.read()
        
        # Display the mermaid diagram
        html_code = f"""
        <html>
        <head>
            <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
            <script>
                mermaid.initialize({{ 
                    startOnLoad: true,
                    theme: 'default',
                    flowchart: {{
                        curve: 'linear',
                        htmlLabels: true,
                        useMaxWidth: true
                    }}
                }});
            </script>
        </head>
        <body>
            <div class="mermaid">
{deposit_mermaid_code}
            </div>
        </body>
        </html>
        """
        components.html(html_code, height=800)
        
        # Show the raw code in an expander
        with st.expander("View Mermaid Code"):
            st.code(deposit_mermaid_code, language="mermaid")
    else:
        st.error("File 'cash_services_deposit_processing.mmd' not found!")

with tab2:
    st.header("Cash Services - Currency Processing")
    
    # Check if file exists
    if os.path.exists("cash_services_currency_processing.mmd"):
        with open("cash_services_currency_processing.mmd", "r", encoding="utf-8") as f:
            currency_mermaid_code = f.read()
        
        # Display the mermaid diagram
        html_code = f"""
        <html>
        <head>
            <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
            <script>
                mermaid.initialize({{ 
                    startOnLoad: true,
                    theme: 'default',
                    flowchart: {{
                        curve: 'linear',
                        htmlLabels: true,
                        useMaxWidth: true
                    }}
                }});
            </script>
        </head>
        <body>
            <div class="mermaid">
{currency_mermaid_code}
            </div>
        </body>
        </html>
        """
        components.html(html_code, height=800)
        
        # Show the raw code in an expander
        with st.expander("View Mermaid Code"):
            st.code(currency_mermaid_code, language="mermaid")
    else:
        st.error("File 'cash_services_currency_processing.mmd' not found!")

with tab3:
    st.header("Custom Mermaid File Viewer")
    
    # File input
    uploaded_file = st.file_uploader("Choose a .mmd file", type=['mmd', 'md'])
    
    if uploaded_file is not None:
        # Read the uploaded file
        mermaid_code = uploaded_file.read().decode("utf-8")
        
        # Display the mermaid diagram
        html_code = f"""
        <html>
        <head>
            <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
            <script>
                mermaid.initialize({{ 
                    startOnLoad: true,
                    theme: 'default',
                    flowchart: {{
                        curve: 'linear',
                        htmlLabels: true,
                        useMaxWidth: true
                    }}
                }});
            </script>
        </head>
        <body>
            <div class="mermaid">
{mermaid_code}
            </div>
        </body>
        </html>
        """
        components.html(html_code, height=800)
        
        # Show the raw code in an expander
        with st.expander("View Mermaid Code"):
            st.code(mermaid_code, language="mermaid")
    
    # Also allow manual input
    st.subheader("Or paste Mermaid code directly:")
    manual_code = st.text_area("Enter Mermaid code:", height=300)
    
    if manual_code:
        # Display the mermaid diagram
        html_code = f"""
        <html>
        <head>
            <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
            <script>
                mermaid.initialize({{ 
                    startOnLoad: true,
                    theme: 'default',
                    flowchart: {{
                        curve: 'linear',
                        htmlLabels: true,
                        useMaxWidth: true
                    }}
                }});
            </script>
        </head>
        <body>
            <div class="mermaid">
{manual_code}
            </div>
        </body>
        </html>
        """
        components.html(html_code, height=800)
