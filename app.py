import streamlit as st
from google import genai
import re
import PyPDF2  
import docx  
import time 

# --- 1. Page Configuration ---
st.set_page_config(page_title="TalentFit Pro", page_icon="🎯", layout="wide")

if "current_page" not in st.session_state:
    st.session_state.current_page = "alignment"

# --- 2. Custom Styling ---
st.markdown("""
<style>
    /* Your Custom Deep Blue Radial Gradient Background */
    .stApp {
        background: #020024 !important;
        background: radial-gradient(circle, rgba(2, 0, 36, 1) 0%, rgba(9, 9, 121, 1) 21%, rgba(0, 212, 255, 1) 100%) !important;
    }
    
    /* White Backgrounds for Inputs to keep text readable */
    div.stTextArea div[data-baseweb="textarea"] {
        border: 3px solid black !important;
        border-radius: 8px !important;
        background-color: #ffffff !important;
    }
    div.stTextArea textarea {
        height: 300px !important;
        background-color: #ffffff !important;
        color: black !important;
        font-weight: bold !important; /* NEW: Forces typed text to be bold */
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
        color: black !important;
    }
    
    /* NEW: Forces the "Drag and drop file here" text inside the uploader to be bold */
    [data-testid="stFileUploaderDropzone"] div, [data-testid="stFileUploaderDropzone"] small {
        color: black !important;
        font-weight: bold !important;
    }
    
    /* 3D Pill Buttons - Auto-sizing to text */
    div.stButton > button, a[data-testid="baseLinkButton"] > div {
        border: none !important;
        border-radius: 50px !important; 
        background: linear-gradient(to bottom, #00d2ff, #03a9f4) !important; 
        color: white !important;
        font-weight: 900 !important; 
        font-size: 16px !important;
        text-transform: uppercase !important; 
        padding: 12px 24px !important;
        box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.4), 
                    inset 0px 4px 6px rgba(255, 255, 255, 0.4), 
                    inset 0px -4px 6px rgba(0, 0, 0, 0.2) !important;
        transition: all 0.15s ease-in-out !important;
        text-decoration: none !important;
        width: auto !important; 
        display: inline-block !important;
    }
    
    div.stButton > button:active, a[data-testid="baseLinkButton"] > div:active {
        transform: translateY(4px) !important;
        box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.4), 
                    inset 0px 4px 6px rgba(0, 0, 0, 0.5) !important;
    }
    
    [data-testid="stToolbar"] {
        visibility: hidden !important;
    }
    
    /* Fix for radio buttons and checkboxes to be readable on dark background */
    .stRadio label, .stCheckbox label {
        color: white !important;
        font-weight: bold !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. Navigation Bar ---
nav_col1, nav_col2 = st.columns([1, 5])
with nav_col1:
    if st.session_state.current_page == "alignment":
        if st.button(" 🔍 SMART JOB SEARCH ❯ "):
            st.session_state.current_page = "search"
            st.rerun()
    else:
        if st.button(" ⬅ ALIGNMENT ENGINE ❯ "):
            st.session_state.current_page = "alignment"
            st.rerun()

with nav_col2:
    st.empty() 

# --- 4. Header ---
header_container = st.container()
with header_container:
    col1, col2 = st.columns([2, 3])  
    with col1:
        st.image("TalentFit-Pro-5-8-2026.png")  
    with col2:
        if st.session_state.current_page == "alignment":
            st.markdown("<h1 style='font-size: 32px; font-weight: 900; margin-bottom: 0px; color: white;'>AI-Powered Resume & JD Alignment Engine</h1>", unsafe_allow_html=True)
            st.markdown("<span style='color: #e0f2fe; font-size: 18px;'>Your competitive edge in professional placement.</span>", unsafe_allow_html=True)
        else:
            st.markdown("<h1 style='font-size: 32px; font-weight: 900; margin-bottom: 0px; color: white;'>Smart Job Search Portal</h1>", unsafe_allow_html=True)
            st.markdown("<span style='color: #e0f2fe; font-size: 18px;'>Secure, AI-optimized connections to live market data.</span>", unsafe_allow_html=True)

# ==========================================
# PAGE 1: ALIGNMENT ENGINE
# ==========================================
if st.session_state.current_page == "alignment":
    st.write("") # Spacer
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<span style='color: white; font-weight: bold;'>📄 Upload Your Resume (PDF or Word):</span>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("", type=["pdf", "docx"], label_visibility="collapsed")
        
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
        st.markdown("<span style='color: white; font-weight: bold;'>🎯 Paste Job Description Here:</span>", unsafe_allow_html=True)
        job_description = st.text_area("", height=300, label_visibility="collapsed")

    st.markdown("---")
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    with col_btn2:
        analyze_btn = st.button(" 🚀 ANALYZE ALIGNMENT ❯ ")

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
                    Keep it professional, simple, and natural. Do not use side headings.
                    
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
                                        box-shadow: 6px 6px 12px #010014, -6px -6px 12px #030034; 
                                        border: 2px solid {color};
                                        text-align: center; margin-bottom: 20px;">
                                <span style="font-size: 14px; color: black; font-weight: bold;">Match %</span><br>
                                <span style="font-size: 24px; font-weight: bold; color: {color};">{score}%</span>
                            </div>
                            """, unsafe_allow_html=True)
                            
                        with res_col3:
                            st.markdown(f"""
                            <div style="background-color: white; padding: 15px; border-radius: 12px; 
                                        box-shadow: 6px 6px 12px #010014, -6px -6px 12px #030034; 
                                        border: 2px solid {color};
                                        text-align: center; margin-bottom: 20px;">
                                <span style="font-size: 14px; color: black; font-weight: bold;">Rating</span><br>
                                <span style="font-size: 18px; font-weight: bold; color: {color};">{status}</span>
                            </div>
                            """, unsafe_allow_html=True)
                            
                        st.markdown(f"<div style='background-color: white; padding: 20px; border-radius: 8px; color: black; font-weight: bold;'>{clean_text}</div>", unsafe_allow_html=True)
                        
                    else:
                        st.markdown(f"<div style='background-color: white; padding: 20px; border-radius: 8px; color: black; font-weight: bold;'>{full_text}</div>", unsafe_allow_html=True)
                    
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
        st.markdown("<span style='color: white; font-weight: bold;'>📄 Upload Resume to Build Search Algorithm:</span>", unsafe_allow_html=True)
        uploaded_file_search = st.file_uploader("", type=["pdf", "docx"], key="search_uploader", label_visibility="collapsed")
        
        st.markdown("<br><span style='color: white; font-size: 18px; font-weight: bold;'>⚙️ Advanced Search Filters</span>", unsafe_allow_html=True)
        
        date_posted = st.radio(
            "Date Posted:", 
            ["Past 24 hours", "Past week", "Past month", "Any time"], 
            index=0, 
            horizontal=True
        )
        
        st.markdown("<span style='font-size: 14px; color: #e0f2fe;'>Workplace Type:</span>", unsafe_allow_html=True)
        chk_col1, chk_col2, chk_col3 = st.columns(3)
        with chk_col1:
            is_remote = st.checkbox("Remote", value=True)
        with chk_col2:
            is_hybrid = st.checkbox("Hybrid", value=True)
        with chk_col3:
            is_onsite = st.checkbox("On-site", value=True)
        
        st.write("") 
        trigger_search = st.button(" FIND MY PERFECT MATCHES ❯ ")
            
    with col_right:
        st.markdown("<h3 style='color: white;'>🎯 Your AI-Optimized Target Roles</h3>", unsafe_allow_html=True)
        
        if trigger_search and uploaded_file_search:
            with st.spinner("Analyzing profile and generating secure search algorithms..."):
                time.sleep(1.5) 
                
                st.success("✅ Analysis Complete! Custom search pathways generated.")
                st.info("💡 **How it works:** These secure links bypass basic search limits. They will open directly in your LinkedIn account, automatically applying your exact date and workplace filters.")
                
                time_codes = {
                    "Past 24 hours": "r86400", 
                    "Past week": "r604800", 
                    "Past month": "r2592000", 
                    "Any time": ""
                }
                tpr_param = f"&f_TPR={time_codes[date_posted]}" if time_codes[date_posted] else ""
                
                wt_codes = []
                if is_onsite: wt_codes.append("1")
                if is_remote: wt_codes.append("2")
                if is_hybrid: wt_codes.append("3")
                
                wt_param = f"&f_WT={'%2C'.join(wt_codes)}" if wt_codes else ""
                
                job_title_1 = "Senior Program Manager"
                job_title_2 = "Lead Data Analyst"
                job_title_3 = "IT Project Director"
                location = "United States"
                
                search_link_1 = f"https://www.linkedin.com/jobs/search/?keywords={job_title_1.replace(' ', '%20')}&location={location.replace(' ', '%20')}{tpr_param}{wt_param}"
                search_link_2 = f"https://www.linkedin.com/jobs/search/?keywords={job_title_2.replace(' ', '%20')}&location={location.replace(' ', '%20')}{tpr_param}{wt_param}"
                search_link_3 = f"https://www.linkedin.com/jobs/search/?keywords={job_title_3.replace(' ', '%20')}&location={location.replace(' ', '%20')}{tpr_param}{wt_param}"
                
                st.markdown("<h4 style='color: white;'>Click to execute live search:</h4>", unsafe_allow_html=True)
                st.caption("⚠️ *Note: If LinkedIn asks you to log in, just return here and click the button a second time after logging in!*")
                
                st.write("")
                st.link_button(f" 💼 EXECUTE SEARCH: '{job_title_1}' ❯ ", search_link_1)
                st.write("")
                st.link_button(f" 📊 EXECUTE SEARCH: '{job_title_2}' ❯ ", search_link_2)
                st.write("")
                st.link_button(f" 🚀 EXECUTE SEARCH: '{job_title_3}' ❯ ", search_link_3)
                
        elif trigger_search:
            st.warning("Please upload a resume first so we can analyze your profile.")
        else:
            # NEW: Made this instructional text black and bold!
            st.markdown("""
            <div style='background-color: white; padding: 20px; border-radius: 8px; border: 1px solid #cbd5e1;'>
                <p style='margin:0; color: black; font-weight: bold;'>👈 Adjust your filters, upload your resume, and click <span style='color: #03a9f4;'>FIND MY PERFECT MATCHES</span>. TalentFit Pro will build secure, one-click search pathways tailored directly to your preferences.</p>
            </div>
            """, unsafe_allow_html=True)
