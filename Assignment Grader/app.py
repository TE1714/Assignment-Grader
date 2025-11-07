# import streamlit as st
# import os
# from pydantic import BaseModel, Field
# from langchain_google_genai import ChatGoogleGenerativeAI
# from dotenv import load_dotenv

# # ---------------------------
# # Load API Key
# # ---------------------------
# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# # ---------------------------
# # Mock Data
# # ---------------------------
# MOCK_COURSES = [{"id": "CS101", "name": "Introduction to Computer Science"}]
# MOCK_ASSIGNMENTS = {
#     "CS101": [{"id": "ASSIGN_01", "title": "Essay: The Impact of AI on Society"}]
# }
# MOCK_SUBMISSIONS = {
#     "ASSIGN_01": [
#         {
#             "student_id": "STUDENT_123",
#             "student_name": "Alex Johnson",
#             "submission_text": """Artificial Intelligence (AI) has profoundly reshaped society. 
# Its impact is seen in automation, which increases efficiency but also raises concerns 
# about job displacement. AI algorithms now power everything from recommendation engines 
# to medical diagnostics, offering unprecedented capabilities. However, we must address 
# ethical challenges like bias in AI models and the potential for misuse in surveillance. 
# The future of AI depends on responsible development and regulation to ensure its benefits 
# are shared by all.""",
#             "rubric": """
# - Clarity (10 pts): Is the main argument clear and easy to follow?
# - Evidence (15 pts): Are claims supported with specific examples?
# - Structure (5 pts): Is the essay well-organized with an introduction, body, and conclusion?
# - Total Points: 30
# """,
#         }
#     ]
# }

# # ---------------------------
# # Pydantic model for structured output
# # ---------------------------
# class GradingOutput(BaseModel):
#     detailed_feedback: str = Field(description="Detailed analysis for each rubric criterion.")
#     summary_feedback: str = Field(description="Concise summary of strengths and improvement areas.")
#     suggested_score: int = Field(description="Suggested numeric score based on rubric analysis.")

# # ---------------------------
# # Streamlit App
# # ---------------------------
# st.set_page_config(page_title="AI Assignment Grader", page_icon="🧠", layout="centered")
# st.title("📘 AI Assignment Grader")
# st.write("Analyze student submissions using **Gemini 2.5 Pro**.")

# # Course selection
# course_ids = [course["id"] for course in MOCK_COURSES]
# selected_course_id = st.selectbox("Select Course", course_ids)

# # Assignment selection
# assignments = MOCK_ASSIGNMENTS.get(selected_course_id, [])
# assignment_ids = [a["id"] for a in assignments]
# selected_assignment_id = st.selectbox("Select Assignment", assignment_ids)

# # Display submissions
# submissions = MOCK_SUBMISSIONS.get(selected_assignment_id, [])
# for submission in submissions:
#     st.subheader(f"Student: {submission['student_name']} ({submission['student_id']})")
#     st.code(submission["submission_text"], language="text")
    
#     if st.button(f"Analyze Submission for {submission['student_name']}"):

#         with st.spinner("Analyzing submission with Gemini 2.5 Pro..."):
#             try:
#                 # Initialize LLM
#                 llm = ChatGoogleGenerativeAI(
#                     model="gemini-2.5-pro",
#                     temperature=0.1,
#                     google_api_key=GOOGLE_API_KEY
#                 )

#                 # Bind structured output
#                 structured_llm = llm.with_structured_output(GradingOutput)

#                 # Combine rubric and submission into a single string prompt
#                 prompt_text = f"""
# Analyze this student's submission based on the rubric below.
# Provide:
# 1. Detailed feedback for each rubric criterion
# 2. A short summary
# 3. Suggested score out of total points

# Rubric:
# {submission['rubric']}

# Submission:
# {submission['submission_text']}
# """

#                 # Invoke the structured LLM with the string prompt
#                 response_model = structured_llm.invoke(prompt_text)

#                 # Display results
#                 st.success("✅ Analysis Complete!")
#                 st.subheader("Detailed Feedback")
#                 st.write(response_model.detailed_feedback)
#                 st.subheader("Summary Feedback")
#                 st.write(response_model.summary_feedback)
#                 st.subheader("Suggested Score")
#                 st.write(response_model.suggested_score)

#             except Exception as e:
#                 st.error(f"❌ Error during analysis: {e}")





import streamlit as st
import os
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# ---------------------------
# Load API Key
# ---------------------------
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# ---------------------------
# Pydantic model for structured output
# ---------------------------
class GradingOutput(BaseModel):
    detailed_feedback: str = Field(description="Detailed analysis for each rubric criterion.")
    summary_feedback: str = Field(description="Concise summary of strengths and improvement areas.")
    suggested_score: int = Field(description="Suggested numeric score based on rubric analysis.")

# ---------------------------
# Streamlit App
# ---------------------------
st.set_page_config(page_title="Dynamic AI Assignment Grader", page_icon="🧠", layout="centered")
st.title("📘 Dynamic AI Assignment Grader")
st.write("Analyze student submissions dynamically using **Gemini 2.5 Pro**.")

# ---------------------------
# Dynamic Inputs
# ---------------------------
course_name = st.text_input("Course Name (e.g., CS101)")
assignment_name = st.text_input("Assignment Title (e.g., Essay: The Impact of AI)")

st.subheader("Student Submission")
student_name = st.text_input("Student Name")
student_id = st.text_input("Student ID")
submission_text = st.text_area("Paste student's submission here")

st.subheader("Grading Rubric")
rubric_text = st.text_area("Paste the grading rubric here")
max_marks = st.number_input("Total Marks", min_value=1, value=30)

# ---------------------------
# Analysis Button
# ---------------------------
if st.button("Analyze Submission"):

    if not all([course_name, assignment_name, student_name, student_id, submission_text, rubric_text]):
        st.warning("Please fill in all fields before analyzing.")
    else:
        with st.spinner("Analyzing submission with Gemini 2.5 Pro..."):
            try:
                # Initialize LLM
                llm = ChatGoogleGenerativeAI(
                    model="gemini-2.5-pro",
                    temperature=0.1,
                    google_api_key=GOOGLE_API_KEY
                )

                # Bind structured output
                structured_llm = llm.with_structured_output(GradingOutput)

                # Create prompt dynamically
                prompt_text = f"""
Analyze this student's submission based on the rubric below.
Provide:
1. Detailed feedback for each rubric criterion
2. A short summary
3. Suggested score out of {max_marks}

Rubric:
{rubric_text}

Submission:
{submission_text}
"""

                # Invoke the structured LLM
                response_model = structured_llm.invoke(prompt_text)

                # Display results
                st.success(f"✅ Analysis Complete for {student_name} ({student_id})!")
                st.subheader("Detailed Feedback")
                st.write(response_model.detailed_feedback)
                st.subheader("Summary Feedback")
                st.write(response_model.summary_feedback)
                st.subheader("Suggested Score")
                st.write(response_model.suggested_score)

            except Exception as e:
                st.error(f"❌ Error during analysis: {e}")
