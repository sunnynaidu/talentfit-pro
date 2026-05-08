import streamlit as st
from google import genai
import re

# --- 1. Page Configuration ---
st.set_page_config(page_title="TalentFit Pro", page_icon="🎯", layout="wide")

# --- 2. Custom Styling ---
# --- 2. Custom Styling ---
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #e0f2fe 20%, #d1fae5 100%);
    }
    div.stTextArea div[data-baseweb="textarea"] {
    }
    div.stTextArea div[data-baseweb="textarea"] {
        border: 3px solid black !important;
        border-radius: 8px !important;
    }
    div.stTextArea textarea {
        border: 3px solid black !important;
        border-radius: 8px !important;
    }
    div.stButton > button {
        border: 2px solid red !important;
    }
    /* This hides the GitHub Icon and Deploy button at the top right */
    [data-testid="stToolbar"] {
        visibility: hidden !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. Header ---
header_container = st.container()

with header_container:
    col1, col2 = st.columns([2, 3])  
    with col1:
        st.image("TalentFit-Pro-5-8-2026.png")  
    with col2:
        st.markdown("<h1 style='font-size: 32px; font-weight: 900; margin-bottom: 0px;'>AI-Powered Resume & JD Alignment Engine</h1>", unsafe_allow_html=True)
        st.markdown("Your competitive edge in professional placement.")

# --- 4. Main Layout (Side-by-Side Columns) ---
col1, col2 = st.columns(2)

with col1:
    my_resume = st.text_area("**📄 Paste Your Resume Here:**", height=300)

with col2:
    job_description = st.text_area("**🎯 Paste Job Description Here:**", height=300)

# --- 5. Centered Analyze Button ---
st.markdown("---")
col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])

with col_btn2:
    analyze_btn = st.button("🚀 Analyze Alignment", use_container_width=True)

# --- 6. AI Engine Logic ---
if analyze_btn:
    if my_resume and job_description:
        
        with st.spinner("TalentFit Pro is calculating your match..."):
            try:
                # This securely pulls your API key from the Streamlit vault!
                api_key = st.secrets["GEMINI_API_KEY"]
                client = genai.Client(api_key=api_key)
                
                prompt_instructions = f"""
                You are an expert Technical Recruiter. Compare the resume to the job description.
                
                IMPORTANT: You MUST start your response with exactly this format:
                <SCORE>XX</SCORE>
                where XX is just the number representing the match percentage.
                
                Then provide:
                1. Missing Keywords: Identify exact keywords, tools, or skills missing.
                2. Resume Upgrades: Suggest 2 new bullet points for the resume.
                Keep it professional, simple, and natural.
                
                My Resume: {my_resume}
                Job Description: {job_description}
                """
                
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt_instructions
                )
                
                full_text = response.text
                score_match = re.search(r'<SCORE>(\d+)</SCORE>', full_text)
                
                st.success("Analysis Complete!")
                
                if score_match:
                    score = int(score_match.group(1))
                    clean_text = re.sub(r'<SCORE>\d+</SCORE>', '', full_text).strip()
                    
                    if score <= 50:
                        status = "Poor"
                        color = "red"
                    elif score <= 75:
                        status = "Good"
                        color = "green"
                    else:
                        status = "Excellent"
                        color = "#FFBF00" 
                        
                    res_col1, res_col2, res_col3 = st.columns([2, 1, 1])
                    
                    with res_col2:
                        st.markdown(f"""
                        <div style="background-color: white; padding: 15px; border-radius: 12px; 
                                    box-shadow: 6px 6px 12px #b8c4d4, -6px -6px 12px #ffffff; 
                                    border: 1px solid red;
                                    text-align: center; margin-bottom: 20px;">
                            <span style="font-size: 14px; color: #64748b;">Match %</span><br>
                            <span style="font-size: 24px; font-weight: bold; color: {color};">{score}%</span>
                        </div>
                        """, unsafe_allow_html=True)
                        
                    with res_col3:
                        st.markdown(f"""
                        <div style="background-color: white; padding: 15px; border-radius: 12px; 
                                    box-shadow: 6px 6px 12px #b8c4d4, -6px -6px 12px #ffffff; 
                                    border: 1px solid red;
                                    text-align: center; margin-bottom: 20px;">
                            <span style="font-size: 14px; color: #64748b;">Rating</span><br>
                            <span style="font-size: 18px; font-weight: bold; color: {color};">{status}</span>
                        </div>
                        """, unsafe_allow_html=True)
                        
                    st.subheader("Actionable Feedback:")
                    st.write(clean_text)
                    
                else:
                    st.subheader("Actionable Feedback:")
                    st.write(full_text)
                
            except Exception as e:
                st.error(f"An error occurred. Details: {e}")
                
    else:
        st.warning("Please paste both your resume and the job description.")
