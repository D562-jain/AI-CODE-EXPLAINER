import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# --- Page Setup and Custom Styling ---
st.set_page_config(
    page_title="AI Code Explainer",
    page_icon="🤖",
    layout="wide"
)

# Use Markdown for custom styling
st.markdown("""
<style>
    .main-header { 
        font-size: 2.5rem; 
        color: #2E86AB; 
        text-align: center;
        margin-bottom: 1rem;
    }
    .explanation-box { 
        background-color: #F8F9FA; 
        padding: 25px; 
        border-radius: 10px; 
        border-left: 5px solid #2E86AB; 
        margin-top: 20px;
        line-height: 1.6;
        font-size: 16px;
    }
    .stButton>button {
        background-color: #2E86AB; 
        color: white;
        width: 100%;
        border: none;
        padding: 12px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 16px;
        margin-top: 10px;
    }
    .stButton>button:hover {
        background-color: #1C6C8B; 
    }
    .info-box {
        background-color: #D1ECF1;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #0FA0CE;
        margin-top: 25px;
    }
    .success-box {
        background-color: #D4EDDA;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #28A745;
        margin-top: 20px;
    }
    .warning-box {
        background-color: #FFF3CD;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #FFC107;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- App Header and Description ---
st.markdown('<p class="main-header">🤖 AI Code Explainer</p>', unsafe_allow_html=True)
st.caption("Paste your code snippet below and get instant explanations powered by AI")

# --- Create two columns for a clean layout ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Your Code")
    # Text area for user code input
    code_input = st.text_area(
        "Paste your Python code here:",
        height=300,
        placeholder="def calculate_sum(a, b):\n    result = a + b\n    return result\n\nx = 5\ny = 10\ntotal = calculate_sum(x, y)\nprint(f\"The sum is: {total}\")",
        label_visibility="collapsed",
        key="code_input"
    )

    # Button to trigger the explanation
    explain_button = st.button("🧠 Explain My Code", use_container_width=True)

with col2:
    st.subheader("📖 Explanation")
    # This is an empty container to hold the explanation
    explanation_placeholder = st.empty()
    # Show a default message before the user interacts with the app
    explanation_placeholder.info("💡 Your AI-powered explanation will appear here after you click the button.")

# --- API Interaction Function ---
def generate_gemini_explanation(code):
    """
    Sends the user's code to the Google Gemini API and returns the AI's explanation.
    It uses the 'requests' library with the correct endpoint and JSON payload.
    """
    # Get the API key from the environment variables
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        return "GEMINI_API_KEY not found in .env file.", "error"

    # Define the API endpoint for Gemini
    API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

    # Construct the user prompt with clear instructions for the AI model
    prompt = f"""Explain this Python code in simple, clear English for beginner programmers:
{code}
Please provide a concise explanation that covers:
1. What the code does overall
2. How each function works (if any)
3. What the inputs and outputs are
4. Any important programming concepts demonstrated
Keep the explanation educational and easy to understand."""

    # Build the JSON payload required by the Gemini API
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": api_key
    }

    try:
        # Make the POST request to the API
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        
        # Raise an exception for HTTP errors (e.g., 401, 500)
        response.raise_for_status()
        
        result = response.json()
        
        # Check if the response contains the generated text
        if 'candidates' in result and len(result['candidates']) > 0 and 'parts' in result['candidates'][0]['content']:
            return result['candidates'][0]['content']['parts'][0]['text'].strip(), "gemini"
        
        return "No explanation generated from API.", "error"
        
    except requests.exceptions.RequestException as e:
        return f"API Connection Error: {str(e)}. Please check your internet connection or API key.", "error"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}", "error"

# --- Local Fallback Function ---
def generate_local_explanation(code):
    """
    A simple fallback function to provide a basic analysis if the API fails.
    This ensures the app doesn't break entirely without an API key.
    """
    explanation = "🔍 **Code Analysis:**\n\n"
    lines = [line.strip() for line in code.split('\n') if line.strip()]
    if not lines:
        return "Please enter some code to analyze."
    
    # Simple pattern matching to guess code's purpose
    functions = [line for line in lines if line.startswith('def ')]
    if functions:
        explanation += f"• **Functions defined:** {len(functions)}\n"
        for func in functions[:2]:
            func_name = func.split('def ')[1].split('(')[0].strip()
            explanation += f"  - `{func_name}` function\n"
    
    variables = [line for line in lines if ' = ' in line and not line.startswith(('#', 'def '))]
    if variables:
        explanation += f"• **Variables used:** {len(variables)}\n"
    
    patterns = {
        'for ': 'Contains `for` loops', 'if ': 'Uses conditional statements',
        'import ': 'Imports external libraries', 'print(': 'Displays output',
    }
    for pattern, description in patterns.items():
        if any(pattern in line for line in lines):
            explanation += f"• **{description}**\n"
    
    explanation += "\n💡 *For detailed AI explanation, add a valid GEMINI_API_KEY to your .env file*"
    return explanation

# --- Main App Logic ---
if explain_button:
    if not code_input.strip():
        st.warning("⚠️ Please enter some code first.")
    else:
        with st.spinner('🤔 Analyzing your code...'):
            explanation = None
            api_used = "local"
            
            api_key = os.getenv('GEMINI_API_KEY')
            
            # Check for API key and try to call the API
            if api_key:
                explanation, api_used = generate_gemini_explanation(code_input)
            
            # If API call fails or there's no API key, use the local fallback
            if not explanation or "error" in api_used:
                explanation = generate_local_explanation(code_input)
                api_used = "local"
            
            # Format and display the explanation
            formatted_explanation = f"""
<div class='explanation-box'>
<h4>🎯 Explanation (via {api_used.capitalize()})</h4>
{explanation}
</div>
"""
            explanation_placeholder.markdown(formatted_explanation, unsafe_allow_html=True)
            
            # Show a status message based on which method was used
            if api_used == "gemini":
                st.success("✅ Explanation generated using the Gemini API")
            else:
                if api_key:
                    st.error("❌ API failed. Using basic analysis. Please check your API key and connection.")
                else:
                    st.info("ℹ️ Using basic code analysis. Add your GEMINI_API_KEY to your .env file for AI explanations.")

# --- Footer with Instructions and Sample Code ---
st.markdown("---")
st.markdown("### 🚀 Sample Code to Try")

with st.expander("🧮 Simple Calculator Example"):
    st.code("""def add_numbers(a, b):
    return a + b

result = add_numbers(5, 3)
print(f"The sum is: {result}")""", language="python")

with st.expander("🔢 Factorial Function Example"):
    st.code("""def factorial(n):
    if n == 0:
    return 1
    else:
    return n * factorial(n-1)

result = factorial(5)
print(f"The factorial of 5 is: {result}")""", language="python")

st.markdown("---")
st.markdown("""
<div class='info-box'>
    <h4>ℹ️ Setup Instructions</h4>
    
    <p><strong>To get AI Explanations:</strong></p>
    <ol>
        <li>Get a free API key from the <a href="https://aistudio.google.com/app/apikey" target="_blank">Google AI Studio</a>.</li>
        <li>Create a file named <code>.env</code> in your project folder.</li>
        <li>Add this line to the file: <code>GEMINI_API_KEY=your_api_key_here</code>.</li>
    </ol>
    
    <p><strong>Install required packages:</strong></p>
    <code>pip install streamlit requests python-dotenv</code>
    
    <p><strong>Run the app:</strong></p>
    <code>streamlit run app.py</code>
</div>
""", unsafe_allow_html=True)

# --- My Custom Footer ---
st.markdown("---")
st.markdown("Created with ❤️ by **DISHA JAIN**")
