from google import genai

class ResumeReranker:
    def __init__(self, api_key):
        # Initialize the GenAI client
        self.client = genai.Client(api_key=api_key)

    def create_prompt(self, job_description, resume):
        # Define a prompt for the LLM to evaluate resumes
        prompt_template = (
            "Given the job details: Title: '{title}', Description: '{description}', "
            "Location: '{location}', Required Skills: '{skills}', Required Experience: '{experience}', "
            "Required Education: '{education}', evaluate the following resume: '{resume}'. "
            "Provide a score from 0 to 1 based on how well the resume matches the job details, "
            "and give detailed feedback on the strengths and weaknesses of the resume. "
            "Format your response as 'Score: X Feedback: Y'."
        )

        # Create a detailed prompt for each resume
        resume_details = (
            f"Objective: {resume['objective']}\n"
            f"Skills: {resume['skills']}\n"
            f"Experience: {resume['experience']}\n"
            f"Education: {resume['education']}\n"
            f"Location: {resume['location']}\n"
            f"Certifications: {resume.get('certifications', 'None')}\n"
            f"Projects: {resume.get('projects', 'None')}\n"
            f"Languages: {resume.get('languages', 'None')}\n"
            f"Publications: {resume.get('publications', 'None')}\n"
            f"Volunteer Experience: {resume.get('volunteer_experience', 'None')}\n"
            f"Awards: {resume.get('awards', 'None')}\n"
            f"References: {resume.get('references', 'None')}"
        )

        return prompt_template.format(
            title=job_description["title"],
            description=job_description["description"],
            location=job_description["location"],
            skills=job_description["skills"],
            experience=job_description["experience"],
            education=job_description["education"],
            resume=resume_details
        )

    def rank_resumes(self, job_description, resumes):
        reranked_resumes = []

        for resume in resumes:
            prompt = self.create_prompt(job_description, resume)

            # Generate content using the GenAI model
            response = self.client.models.generate_content(
                model="gemini-2.0-flash", contents=prompt
            )

            # Parse the response to extract the score and feedback
            response_text = response.text
            score = 0.0
            feedback = "Unable to parse feedback."

            # Attempt to extract score and feedback using flexible parsing
            try:
                # Extract score
                score_start = response_text.find("Score:") + len("Score:")
                score_end = response_text.find("\n", score_start)
                score = float(response_text[score_start:score_end].strip())

                # Extract feedback
                feedback_start = response_text.find("Feedback:")
                feedback = response_text[feedback_start:].strip()
            except (IndexError, ValueError):
                pass

            # Append the resume, score, and feedback to the list
            reranked_resumes.append((resume, score, feedback))

        # Sort resumes by score in descending order
        reranked_resumes.sort(key=lambda x: x[1], reverse=True)

        return reranked_resumes

# Example usage
api_key = "AIzaSyAvX1jKQOx-e2XTrb13cDYeCS_sucEGKUA"
job_description = {
    "title": "Data Scientist",
    "description": "We are looking for a data scientist with expertise in Python, machine learning, and data visualization.",
    "location": "New York",
    "skills": "Python, machine learning, data visualization, cloud platforms, NLP",
    "experience": "3+ years in data science",
    "education": "Bachelor's degree in Computer Science or related field"
}

resumes = [
    {
        "objective": "Experienced data scientist with a strong background in Python, machine learning, and data visualization.",
        "skills": "Python, machine learning, data visualization, cloud platforms, NLP",
        "experience": "3 years as a data scientist",
        "education": "Bachelor's degree in Computer Science",
        "location": "New York",
        "certifications": "Certified Data Scientist",
        "projects": """
            1. Developed advanced machine learning models for data analysis using Python and cloud platforms.
            2. Created a data visualization tool using Python and D3.js.
            • Implemented a recommendation system using collaborative filtering.
            - Built a real-time data processing pipeline with Apache Kafka.
        """,
        "languages": "English",
        "publications": "Published research on machine learning techniques",
        "volunteer_experience": "Volunteered as a data science mentor",
        "awards": "Data Science Excellence Award",
        "references": "Available upon request"
    },
    {
        "objective": "Data scientist with expertise in machine learning and data analysis.",
        "skills": "Machine learning, data analysis, Python, R",
        "experience": "4 years in data analysis",
        "education": "Master's degree in Data Science",
        "location": "San Francisco",
        "certifications": "Data Analyst Certification",
        "projects": """
            1. Developed predictive models for customer behavior analysis.
            2. Automated data processing workflows using Python.
        """,
        "languages": "English, Spanish",
        "publications": "Co-authored a paper on data mining techniques",
        "volunteer_experience": "Organized data science workshops",
        "awards": "Best Data Science Project Award",
        "references": "Available upon request"
    }
    # Add more resumes as needed
]

from google import genai

class ResumeRanker:
    def __init__(self, api_key):
        # Initialize the GenAI client
        self.client = genai.Client(api_key=api_key)

    def create_prompt(self, job_description, resume):
        # Define a prompt for the LLM to evaluate resumes
        prompt_template = (
            "Given the job details: Title: '{title}', Description: '{description}', "
            "Location: '{location}', Required Skills: '{skills}', Required Experience: '{experience}', "
            "Required Education: '{education}', evaluate the following resume: '{resume}'. "
            "Provide a score from 0 to 1 based on how well the resume matches the job details, "
            "and give detailed feedback on the strengths and weaknesses of the resume. "
            "Format your response as 'Score: X Feedback: Y'."
        )

        # Create a detailed prompt for each resume
        resume_details = (
            f"Objective: {resume['objective']}\n"
            f"Skills: {resume['skills']}\n"
            f"Experience: {resume['experience']}\n"
            f"Education: {resume['education']}\n"
            f"Location: {resume['location']}\n"
            f"Certifications: {resume.get('certifications', 'None')}\n"
            f"Projects: {resume.get('projects', 'None')}\n"
            f"Languages: {resume.get('languages', 'None')}\n"
            f"Publications: {resume.get('publications', 'None')}\n"
            f"Volunteer Experience: {resume.get('volunteer_experience', 'None')}\n"
            f"Awards: {resume.get('awards', 'None')}\n"
            f"References: {resume.get('references', 'None')}"
        )

        return prompt_template.format(
            title=job_description["title"],
            description=job_description["description"],
            location=job_description["location"],
            skills=job_description["skills"],
            experience=job_description["experience"],
            education=job_description["education"],
            resume=resume_details
        )

    def rank_resumes(self, job_description, resumes):
        reranked_resumes = []

        for resume in resumes:
            prompt = self.create_prompt(job_description, resume)

            # Generate content using the GenAI model
            response = self.client.models.generate_content(
                model="gemini-2.0-flash", contents=prompt
            )

            # Parse the response to extract the score and feedback
            response_text = response.text
            score = 0.0
            feedback = "Unable to parse feedback."

            # Attempt to extract score and feedback using flexible parsing
            try:
                # Extract score
                score_start = response_text.find("Score:") + len("Score:")
                score_end = response_text.find("\n", score_start)
                score = float(response_text[score_start:score_end].strip())

                # Extract feedback
                feedback_start = response_text.find("Feedback:")
                feedback = response_text[feedback_start:].strip()
            except (IndexError, ValueError):
                pass

            # Append the resume, score, and feedback to the list
            reranked_resumes.append((resume, score, feedback))

        # Sort resumes by score in descending order
        reranked_resumes.sort(key=lambda x: x[1], reverse=True)

        return reranked_resumes

# Example usage
api_key = "AIzaSyAvX1jKQOx-e2XTrb13cDYeCS_sucEGKUA"
job_description = {
    "title": "Data Scientist",
    "description": "We are looking for a data scientist with expertise in Python, machine learning, and data visualization.",
    "location": "New York",
    "skills": "Python, machine learning, data visualization, cloud platforms, NLP",
    "experience": "3+ years in data science",
    "education": "Bachelor's degree in Computer Science or related field"
}

resumes = [
    {
        "objective": "Experienced data scientist with a strong background in Python, machine learning, and data visualization.",
        "skills": "Python, machine learning, data visualization, cloud platforms, NLP",
        "experience": "3 years as a data scientist",
        "education": "Bachelor's degree in Computer Science",
        "location": "New York",
        "certifications": "Certified Data Scientist",
        "projects": """
            1. Developed advanced machine learning models for data analysis using Python and cloud platforms.
            2. Created a data visualization tool using Python and D3.js.
            • Implemented a recommendation system using collaborative filtering.
            - Built a real-time data processing pipeline with Apache Kafka.
        """,
        "languages": "English",
        "publications": "Published research on machine learning techniques",
        "volunteer_experience": "Volunteered as a data science mentor",
        "awards": "Data Science Excellence Award",
        "references": "Available upon request"
    },
    {
        "objective": "Data scientist with expertise in machine learning and data analysis.",
        "skills": "Machine learning, data analysis, Python, R",
        "experience": "4 years in data analysis",
        "education": "Master's degree in Data Science",
        "location": "San Francisco",
        "certifications": "Data Analyst Certification",
        "projects": """
            1. Developed predictive models for customer behavior analysis.
            2. Automated data processing workflows using Python.
        """,
        "languages": "English, Spanish",
        "publications": "Co-authored a paper on data mining techniques",
        "volunteer_experience": "Organized data science workshops",
        "awards": "Best Data Science Project Award",
        "references": "Available upon request"
    }
    # Add more resumes as needed
]

ranker = ResumeReranker(api_key)
reranked_resumes = ranker.rank_resumes(job_description, resumes)

for resume, score, feedback in reranked_resumes:
    print("Feedback:", feedback)
    print("Score:", score)
    print("Resume:", resume)
  
