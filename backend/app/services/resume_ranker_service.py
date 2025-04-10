import spacy
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re

class ResumeRanker:
    def __init__(self):
        # Load the pre-trained sentence transformer model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        # Load the spaCy model for NER
        self.nlp = spacy.load('en_core_web_sm')

    def compute_similarity(self, text1, text2):
        # Encode the texts into embeddings
        emb1 = self.model.encode([text1])
        emb2 = self.model.encode([text2])
        # Compute and return the cosine similarity between the embeddings
        return cosine_similarity(emb1, emb2)[0][0]

    def extract_entities_and_keywords(self, text):
        # Use spaCy to extract entities and keywords from text
        doc = self.nlp(text)
        entities = [ent.text for ent in doc.ents if ent.label_ in ['ORG', 'PERSON', 'GPE', 'LOC', 'PRODUCT']]
        # Extract keywords using noun chunks
        keywords = [chunk.text for chunk in doc.noun_chunks if chunk.text.lower() not in entities]
        return entities + keywords

    def split_projects(self, projects_text):
        # Use regex to split projects by numbers or bullet points
        projects = re.split(r'\n\s*(?:\d+\.\s*|\•\s*|\-\s*)', projects_text.strip())
        return [proj for proj in projects if proj]  # Filter out empty strings

    def rank_resume(self, job_description, resume):
        # Extract entities and keywords from job description and resume
        job_entities_keywords = self.extract_entities_and_keywords(job_description["description"])
        resume_entities_keywords = self.extract_entities_and_keywords(resume["objective"])

        # Extract and split project information from the resume
        resume_projects = self.split_projects(resume.get("projects", ""))
        print(resume_projects)
        # Compute similarity for each project and aggregate scores above the threshold
        project_scores = []
        for project in resume_projects:
            score = self.compute_similarity(" ".join(job_entities_keywords), project)
            if score > 0.5:
                project_scores.append(score)

        # Aggregate project scores
        if project_scores:
            project_similarity = sum(project_scores) / len(project_scores)
        else:
            project_similarity = 0
        
        # Compute similarity for each component
        similarity_scores = {
            "skills": self.compute_similarity(job_description["skills"], resume["skills"]),
            "experience": self.compute_similarity(job_description["experience"], resume["experience"]),
            "education": self.compute_similarity(job_description["education"], resume["education"]),
            "location": self.compute_similarity(job_description["location"], resume["location"]),
            "entities_keywords": self.compute_similarity(" ".join(job_entities_keywords), " ".join(resume_entities_keywords)),
            "projects": project_similarity
        }

        # Define weights for each component to calculate the final aggregated score
        weights = {
            "skills": 0.25,
            "experience": 0.25,
            "education": 0.15,
            "location": 0.1,
            "entities_keywords": 0.15,
            "projects": 0.1
        }

        # Calculate the final aggregated score as a weighted sum of the component scores
        final_score = sum(similarity_scores[component] * weights[component] for component in similarity_scores)
        return final_score, similarity_scores

# Example usage
job_description = {
    "title": "Data Scientist",
    "description": "We are looking for a data scientist with expertise in Python, machine learning, and data visualization.",
    "location": "New York",
    "skills": "Python, machine learning, data visualization, cloud platforms, NLP",
    "experience": "3+ years in data science",
    "education": "Bachelor's degree in Computer Science or related field"
}

resume = {
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
}

