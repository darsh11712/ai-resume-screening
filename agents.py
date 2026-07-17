from crewai import Agent,Task,Crew
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()


llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="groq/llama-3.3-70b-versatile",
    temperature=0
)

resume_evaluator = Agent(
    role="Resume Evaluator",
    goal="Determine if the resume matches the job description",
    backstory="You are an HR Expert evaluating resumes for a job",
    verbose=True,
    llm=llm
)

def get_screening_tasks(
    resume_text,
    job_text,
    required_degree,
    min_cgpa
):
    return [
        Task(
            description=f"""
### RESUME TEXT ###
{resume_text}

### JOB DESCRIPTION ###
{job_text}

### SCREENING RULES ###
Required Degree: {required_degree}
Minimum CGPA: {min_cgpa}

Check the following:

1. Degree must be completed.
2. Degree must match the required degree.
3. CGPA must be equal to or greater than the minimum CGPA.
4. If 10th or 12th percentages are available, consider them.
5. If 10th or 12th percentages are not available, do not reject the candidate.
6. Compare candidate skills with the job description.
7. Calculate a Match Score between 0 and 100.
8. Identify important missing skills.

### INSTRUCTIONS ###
Respond using EXACTLY this format:

Shortlisted: Yes or No
Match Score: <0-100>
Missing Skills: <comma separated skills or None>
Reason: <concise explanation>

DO NOT say anything else.
Begin directly with 'Shortlisted:'.
""",
            agent=resume_evaluator,
            expected_output="""
Shortlisted: Yes or No
Match Score: 0-100
Missing Skills: skill1, skill2 or None
Reason: A concise explanation
"""
        )
    ]