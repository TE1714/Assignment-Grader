import json
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from src.agent.prompt_templates import GRADING_PROMPT_TEMPLATE
from src.utils.config import GOOGLE_API_KEY

# --- Mock Data ---
MOCK_COURSES = [{"id": "CS101", "name": "Introduction to Computer Science"}]
MOCK_ASSIGNMENTS = {
    "CS101": [{"id": "ASSIGN_01", "title": "Essay: The Impact of AI on Society"}]
}
MOCK_SUBMISSIONS = {
    "ASSIGN_01": [
        {
            "student_id": "STUDENT_123",
            "student_name": "Alex Johnson",
            "submission_text": """Artificial Intelligence (AI) has profoundly reshaped society. 
            Its impact is seen in automation, which increases efficiency but also raises concerns 
            about job displacement. AI algorithms now power everything from recommendation engines 
            to medical diagnostics, offering unprecedented capabilities. However, we must address 
            ethical challenges like bias in AI models and the potential for misuse in surveillance. 
            The future of AI depends on responsible development and regulation to ensure its benefits 
            are shared by all.""",
            "rubric": """
            - Clarity (10 pts): Is the main argument clear and easy to follow?
            - Evidence (15 pts): Are claims supported with specific examples?
            - Structure (5 pts): Is the essay well-organized with an introduction, body, and conclusion?
            - Total Points: 30
            """,
        }
    ]
}
# --- End Mock Data ---

# --- Pydantic Model ---
class GradingOutput(BaseModel):
    detailed_feedback: str = Field(description="Markdown-formatted feedback per rubric criterion.")
    summary_feedback: str = Field(description="Concise summary of strengths and areas for improvement.")
    suggested_score: int = Field(description="An integer score based on the rubric analysis.")

# --- LMS Tools ---
@tool
def get_courses() -> list:
    """Fetches a list of available courses from the LMS."""
    print("TOOL: Fetching courses...")
    return MOCK_COURSES

@tool
def get_assignments_for_course(course_id: str) -> list:
    """Fetches the list of assignments for a given course ID."""
    print(f"TOOL: Fetching assignments for course {course_id}...")
    return MOCK_ASSIGNMENTS.get(course_id, [])

@tool
def get_submissions_for_assignment(assignment_id: str) -> list:
    """Fetches all student submissions for a given assignment ID."""
    print(f"TOOL: Fetching submissions for assignment {assignment_id}...")
    return MOCK_SUBMISSIONS.get(assignment_id, [])

@tool
def analyze_submission_with_llm(submission_text: str, rubric: str) -> dict:
    """
    Analyzes a student submission against a rubric using the Gemini LLM
    to generate feedback and a suggested score.
    """
    print("TOOL: Analyzing submission with Gemini LLM...")

    # ✅ Use supported Gemini model
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-pro-exp",  # ✅ Use this or "gemini-2.5-pro"
        temperature=0.1,
        google_api_key=GOOGLE_API_KEY
    )

    # Create structured output
    structured_llm = llm.with_structured_output(GradingOutput)

    # Combine template and structured model
    grading_chain = GRADING_PROMPT_TEMPLATE | structured_llm

    # Run the model
    response_model = grading_chain.invoke(
        {"submission_text": submission_text, "rubric": rubric}
    )

    return response_model.dict()

@tool
def post_grade_to_lms(student_id: str, assignment_id: str, grade: int, feedback: str):
    """Posts a final grade and feedback to the LMS (simulated)."""
    print("=" * 50)
    print("TOOL: Posting Final Grade to LMS (Simulated)")
    print(f"  -> Student ID: {student_id}")
    print(f"  -> Assignment ID: {assignment_id}")
    print(f"  -> Final Grade: {grade}")
    print(f"  -> Final Feedback:\n{feedback}")
    print("=" * 50)
    return "SUCCESS: Grade posted successfully to the LMS."
