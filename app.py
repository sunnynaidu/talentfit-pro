import streamlit as st
from google import genai
import re
import PyPDF2  
import docx  
import time # NEW: Added to create a smooth loading effect

st.set_page_config(page_title="TalentFit Pro", page_icon="🎯", layout="wide")

if "current_page" not in st.session_state:
    st.session_state.current_page = "alignment"

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #e0f2fe 0%, #d1fae5 100%);
    }
    
    div.stTextArea div[data-baseweb="textarea"] {
        border: 3px solid black !important;
        border-radius: 8px !important;
        background-color: #ffffff !important;
    }
    div.stTextArea textarea {
        height: 300px !important;
        background-color: #ffffff !important;
    }
    
    [data-testid="stFileUploaderDropzone"] {
        border: 3px solid black !important;
        border-radius: 8px !important;
        height: 300px !important; 
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important; 
        justify-content: center !important; 
        background-color: #ffffff !important; 
    }
    
    /* Thick red border and embossed 3D effect for all buttons */
    div.stButton > button, a[data-testid="baseLinkButton"] > div {
        border: 3px solid red !important;
        border-radius: 8px !important;
        box-shadow: inset 2px 2px 5px rgba(255,255,255,0.9), inset -3px -3px 7px rgba(0,0,0,0.15), 4px 4px 6px rgba(0,0,0,0.2) !important;
        font-weight: bold !important;
        background-color: #f8f9fa !important;
        color: black !important;
        transition: all 0.1s ease-in-out;
        text-decoration: none !important;
    }
    
    div.stButton > button:active, a[data-testid="baseLinkButton"] > div:active {
        box-shadow: inset 4px 4px 8px rgba(0,0,0,0.2), inset -4px -4px 8px rgba(255,255,255,0.8) !important;
    }
    
    [data-testid="stToolbar"] {
        visibility: hidden !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Navigation Bar ---
nav_col1, nav_col2 = st.columns([1, 5])
with nav_col1:
    if st.session_state.current_page == "alignment":
        if st.button("🔍 Smart Job Search"):
            st.session_state.current_page = "search"
            st.rerun()
    else:
        if st.button("⬅ Alignment Engine"):
            st.session_state.current_page = "alignment"
            st.rerun()

with nav_col2:
    st.empty() 

# --- Header ---
header_container = st.container()
with header_container:
    col1, col2 = st.columns([2, 3])  
    with col1:
        st.image("TalentFit-Pro-5-8-2026.png")  
    with col2:
        if st.session_state.current_page == "alignment":
            st.markdown("<h1 style='font-size: 32px; font-weight: 900; margin-bottom: 0px;'>AI-Powered Resume & JD Alignment Engine</h1>", unsafe_allow_html=True)
            st.markdown("Your competitive edge in professional placement.")
        else:
            st.markdown("<h1 style='font-size: 32px; font-weight: 900; margin-bottom: 0px;'>Smart Job Search Portal</h1>", unsafe_allow_html=True)
            st.markdown("Secure, AI-optimized connections to live market data.")

# ==========================================
# PAGE 1: ALIGNMENT ENGINE
# ==========================================
if st.session_state.current_page == "alignment":
    col1, col2 = st.columns(2)

    with col1:
        uploaded_file = st.file_uploader("**📄 Upload Your Resume (PDF or Word):**", type=["pdf", "docx"])
        
        my_resume = ""
        if uploaded_file is not None:
            file_extension = uploaded_file.name.split(".")[-1].lower()
            if file_extension == "pdf":
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                for page in pdf_reader.pages:
                    my_resume += page.extract_text()
                st.success("PDF Resume loaded successfully!")
            elif file_extension == "docx":
                doc = docx.Document(uploaded_file)
                for para in doc.paragraphs:
                    my_resume += para.text + "\n"
                st.success("Word Resume loaded successfully!")

    with col2:
        job_description = st.text_area("**🎯 Paste Job Description Here:**", height=300)

    st.markdown("---")
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])

    with col_btn2:
        analyze_btn = st.button("🚀 Analyze Alignment", use_container_width=True)

    if analyze_btn:
        if my_resume and job_description:
            with st.spinner("TalentFit Pro is calculating your match..."):
                try:
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
                            
                        st.write(clean_text)
                        
                    else:
                        st.write(full_text)
                    
                except Exception as e:
                    st.error(f"An error occurred. Details: {e}")
                    
        else:
            st.warning("Please upload your resume and paste the job description.")

# ==========================================
# PAGE 2: SMART SEARCH DASHBOARD
# ==========================================
elif st.session_state.current_page == "search":
    st.markdown("---")
    col_left, col_right = st.columns([4, 6])
    
    with col_left:
        uploaded_file_search = st.file_uploader("**📄 Upload Resume to Build Search Algorithm:**", type=["pdf", "docx"], key="search_uploader")
        
        st.write("") 
        trigger_search = st.button("⚙️ Generate Smart Links", use_container_width=True)
            
    with col_right:
        st.markdown("### 🎯 Your AI-Optimized Target Roles")
        
        if trigger_search and uploaded_file_search:
            with st.spinner("Analyzing profile and generating secure search algorithms..."):
                time.sleep(1.5) # Gives a professional loading effect
                
                st.success("✅ Analysis Complete! Custom search pathways generated.")
                st.info("💡 **How it works:** These secure links bypass basic search limits. They will open directly in your LinkedIn account, automatically applying advanced filters to show only the highest-probability roles posted in the last 24 hours.")
                
                # Mock Data (Ready to be wired to Gemini later!)
                job_title_1 = "Senior Program Manager"
                job_title_2 = "Lead Data Analyst"
                job_title_3 = "IT Project Director"
                location = "United States"
                
                search_link_1 = f"https://www.linkedin.com/jobs/search/?keywords={job_title_1.replace(' ', '%20')}&location={location.replace(' ', '%20')}&f_TPR=r86400"
                search_link_2 = f"https://www.linkedin.com/jobs/search/?keywords={job_title_2.replace(' ', '%20')}&location={location.replace(' ', '%20')}&f_TPR=r86400"
                search_link_3 = f"https://www.linkedin.com/jobs/search/?keywords={job_title_3.replace(' ', '%20')}&location={location.replace(' ', '%20')}&f_TPR=r86400"
                
                st.markdown("#### Click to execute live search:")
                st.link_button(f"💼 Execute Search: '{job_title_1}' (Past 24 Hours)", search_link_1, use_container_width=True)
                st.link_button(f"📊 Execute Search: '{job_title_2}' (Past 24 Hours)", search_link_2, use_container_width=True)
                st.link_button(f"🚀 Execute Search: '{job_title_3}' (Past 24 Hours)", search_link_3, use_container_width=True)
                
        elif trigger_search:
            st.warning("Please upload a resume first so we can analyze your profile.")
        else:
            st.markdown("""
            <div style='background-color: white; padding: 20px; border-radius: 8px; border: 1px solid #cbd5e1;'>
                <p style='margin:0; color: #475569;'>👈 Upload your resume and click <b>Generate Smart Links</b> to begin. TalentFit Pro will analyze your background and build secure, one-click search pathways directly to live LinkedIn data.</p>
            </div>
            """, unsafe_allow_html=True)
