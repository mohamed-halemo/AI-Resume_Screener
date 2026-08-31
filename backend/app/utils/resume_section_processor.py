
from typing import Dict, Optional
from difflib import get_close_matches
import re



class ResumeSectionProcessor:
    """
    Processes raw resume text and extracts standardized sections
    using predefined heuristics and mappings.
    """

    DEFAULT_SECTIONS = {
        "objective": ["objective", "career goal", "summary", "professional summary"],
        "skills": ["skills", "technical skills", "tools", "skills & technologies"],
        "experience": ["experience", "work history", "employment", "professional experience", "professional experience & projects"],
        "education": ["education", "academic background"],
        "certifications": ["certifications", "licenses"],
        "projects": ["projects", "project work"],
        "languages": ["languages", "spoken languages"],
        "publications": ["publications"],
        "volunteer_experience": ["volunteer", "volunteering"],
        "awards": ["awards", "honors"],
        "references": ["references"],
        "location": ["location", "address"],
        "personal_info": ["personal information", "contact", "bio"]
    }

    def __init__(self, text: str):
        self.parsed_text=text
        self.lines = [line.strip() for line in text.splitlines() if line.strip()] if text else []
        self.sections: Dict[str, str] = self.extract_sections()
        self._fill_missing_sections()

    def extract_sections(self) -> Dict[str, str]:
        """
        Detect and extract known sections from the resume text.
        Returns a dictionary mapping section keys to their content.
        """
        section_map: Dict[str, str] = {}
        current_section: Optional[str] = None
        section_content_buffer: list[str] = []

        if not self.lines:
            section_map["parsed_text"] = "-"
            return section_map

        try:
            for line in self.lines:
                normalized = line.strip().lower()
                matched_key = self.match_section_name(normalized)

                if matched_key:
                    # If we're switching to a new section, save the previous one
                    if current_section and section_content_buffer:
                        content = "\n".join(section_content_buffer).strip()
                        section_map.setdefault(current_section, "")
                        section_map[current_section] += ("\n" if section_map[current_section] else "") + content
                        section_content_buffer = []
                    current_section = matched_key
                elif current_section:
                    section_content_buffer.append(line)

            # Save any remaining buffered section at the end
            if current_section and section_content_buffer:
                content = "\n".join(section_content_buffer).strip()
                section_map.setdefault(current_section, "")
                section_map[current_section] += ("\n" if section_map[current_section] else "") + content

            section_map['parsed_text'] = self.parsed_text
            
            section_map.setdefault('personal_info',self._extract_personal_info_from_text())

        except Exception as e:
            section_map = {key: "-" for key in self.DEFAULT_SECTIONS}
            section_map['parsed_text'] = "-"
            section_map['error'] = f"Failed to extract sections: {str(e)}"

        

        return section_map

    def _fill_missing_sections(self) -> None:
        """
        Ensure all standard sections are included, even if empty.
        Missing sections are filled with a dash ("-").
        """
        for key in self.DEFAULT_SECTIONS:
            self.sections.setdefault(key, "-")

    def match_section_name(self, line: str) -> Optional[str]:
        """
        Attempt to match a given line against known section names.
        Uses direct string matching and fuzzy matching via difflib.

        Returns the matched section key or None.
        """
        word_count = len(line.split())

        # Avoid long lines unless they use "&" (e.g., "Skills & Technologies")
        if (word_count > 2 and '&' not in line) or ('&' in line and word_count > 3):
            return None

        for key, variations in self.DEFAULT_SECTIONS.items():
            if any(variant in line for variant in variations):
                return key
            match = get_close_matches(line, variations, n=1, cutoff=0.9)
            if match:
                return key
        return None

    def get(self, section_name: str) -> str:
        """
        Return the content of a specific section (if present).
        Defaults to "-" if the section is not found.
        """
        return self.sections.get(section_name, "-")
    

    
    def _extract_personal_info_from_text(self) -> Optional[Dict[str, str]]:
        """
        Attempt to extract personal information (name, email, phone, etc.)
        from the full raw text.
        """
       

        text = self.parsed_text


        # Try name from the top line
        if self.lines:
            first_line = self.lines[0]
            words = re.findall(r'\b[a-zA-Z]+\b', first_line)
            name = " ".join(words) if words else "-"
        else:
            name = "-"

        

        # Email
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        email = email_match.group() if email_match else "-"

        # Phone - accepts international formats
        phone_match = re.search(
            r'(?<!\w)(\+?\d{1,4}[\s\-\.]?)?(\(?\d{2,4}\)?[\s\-\.]?)?(\d{3,4}[\s\-\.]?\d{3,4})(?!\w)', text)
        phone = re.sub(r'[^\d+]', '', phone_match.group()) if phone_match else "-"

        # LinkedIn
        linkedin_match = re.search(r'(https?:\/\/)?(www\.)?linkedin\.com\/[^\s\n]+', text)
        linkedin = linkedin_match.group().strip() if linkedin_match else "-"

        # GitHub
        github_match = re.search(r'(https?:\/\/)?(www\.)?github\.com\/[^\s\n]+', text)
        github = github_match.group().strip() if github_match else "-"



        result = (f'name: {name}\n'
                 f'email: {email}\n'
                 f'phone: {phone}\n'
                 f'linkedin: {linkedin}\n'
                 f'github: {github}\n'
                 f'address: -\n'
                 f'website: -')
        return result

