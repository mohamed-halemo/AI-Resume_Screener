import fitz  
from typing import Dict, Optional
from groq import Groq
import os
from dotenv import load_dotenv
from backend.app.utils.resume_section_processor import ResumeSectionProcessor

load_dotenv()



class ResumeParser:
    """
    Parses a resume PDF file and extracts structured data
    either via local processing or by calling the Groq API.
    """

    def __init__(self, file_path, groq_api_key=None,model:str="llama3-8b-8192"):
        self.file_path = file_path
        self.groq_api_key = groq_api_key or os.getenv("GROQ_API_KEY",None)
        self.client = Groq(api_key=self.groq_api_key) if self.groq_api_key  else None
        self.model=model
        

        

    def _extract_plain_text(self, column_split_x: int = 300) -> str:
        """
        Extracts readable plain text from a PDF document,
        assuming a two-column layout split at `column_split_x`.
        """
        try:
            doc = fitz.open(self.file_path)
            all_column1: list[str] = []
            all_column2: list[str] = []
              # Regular expression for detecting URLs
            url_pattern = r'(https?:\/\/)?(www\.)?([a-zA-Z0-9\-]+\.[a-zA-Z]{2,})(\/[^\s]*)?'

            for page in doc:
                column1: list[tuple[float, str]] = []
                column2: list[tuple[float, str]] = []

                # Get text blocks and categorize them based on their x-coordinate
                blocks = page.get_text("blocks")

                for block in blocks:
                    x0, y0, x1, y1, text, *_ = block
                    text = text.strip()
                    if not text:
                        continue

                    if x0 < column_split_x:
                        column1.append((y0, text))
                    else:
                        column2.append((y0, text))

                # Sort top-to-bottom in each column
                column1_sorted = [text for y, text in sorted(column1, key=lambda x: x[0])]
                column2_sorted = [text for y, text in sorted(column2, key=lambda x: x[0])]

                all_column1.extend(column1_sorted)
                all_column2.extend(column2_sorted)
                

            # Merge both columns into a complete plain text document
            return "\n".join(all_column1 + all_column2)

        except Exception as e:
            print(f"[ERROR] Failed to extract text from PDF: {e}")
            return ""
        
    def _stringify_resume_data(self,data: dict) -> dict:
        """
        Recursively converts all values to strings, removing brackets/lists/dicts from resume data.
        """
        def to_str(value):
            if isinstance(value, list):
                # Convert list of dicts or list of values into a clean string
                if all(isinstance(item, dict) for item in value):
                    return "\n\n".join(
                        "\n".join(f"{k}: {v}" for k, v in item.items()) for item in value
                    )
                return ", ".join(map(str, value))
            elif isinstance(value, dict):
                return "\n".join(f"{k}: {to_str(v)}" for k, v in value.items())
            else:
                return str(value)

        return {k: to_str(v) for k, v in data.items()}

    def extract_resume_sections(self, column_split_x: int = 300) -> Dict[str, str]:
        """
        Returns a dictionary of resume sections extracted from the PDF using heuristics.
        """
        try:
            full_text = self._extract_plain_text(column_split_x=column_split_x)
            processor = ResumeSectionProcessor(full_text)
            return processor.sections
        except Exception as e:
            print(f"[ERROR] Failed to extract resume sections: {e}")
            return {}

    def extract_with_groq(self) -> Dict[str, Optional[str]]:
        """
        Uses the Groq API to extract structured information from resume text.
        Returns a dictionary of fields like name, skills, education, etc.
        """
        try:
            if not self.client:
                raise RuntimeError("Groq client is not initialized. Please assign it to `self.client`.")

            full_text = self._extract_plain_text()

            prompt = f"""
            You are an expert resume parser. Analyze the following resume text and extract the following fields:

            Core Resume Details:
            - objective
            - skills
            - experience
            - education
            - location
            - certifications
            - projects => "with their details and description"
            - languages
            - publications
            - volunteer_experience
            - awards
            - references

            Personal Information:
            - name
            - email
            - phone
            - address
            - linkedin
            - github
            - website

            Return the result as a JSON object with the exact field names shown above as keys.
            If any field is not found in the resume, return a dash ("-") as its value.

            Resume Text:
            {full_text}
            """

            chat_completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts structured data from resumes."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )

            content = chat_completion.choices[0].message.content
            resume_details=eval(content.split("```")[1])
            resume_details["Core Resume Details"]["personal_info"]=resume_details.get("Personal Information", {})
            resume_details["Core Resume Details"]['parsed_text']=full_text
            resume_details.pop("Personal Information", None)
            return self._stringify_resume_data(resume_details['Core Resume Details'])
        
        except Exception as e:
            print(f"[ERROR] Groq extraction failed: {e}")
            return {}
    



    

   
