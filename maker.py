from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from reportlab.lib import colors
import os
import uuid


class ResumeGenerator:
    def __init__(self, data: dict,pdfName) -> None:
        """ Initializes the ResumeGenerator with the provided data.
        Args:
            data (dict): A dictionary containing resume data such as name, contact details, work experience
                            education, projects, skills, and additional details.
        pdfName (str): The name of the PDF file to be generated.
            
        """ 
        self.data = data
        self.elements = []

        if not os.path.exists("resumeFiles"):
            os.makedirs("resumeFiles")

        randomName = str(uuid.uuid4())
        self.pdf_path = os.path.join("resumeFiles", f"{pdfName}.pdf")
        self.doc = SimpleDocTemplate(self.pdf_path, pagesize=letter, leftMargin=25, rightMargin=10, topMargin=30, bottomMargin=10)

        self.runner()

    def runner(self) -> str:
        self._setup_styles()
        self._build_header_and_objective()
        self._build_work_experience()
        self._build_education()
        self._build_projects()
        self._build_skills()
        self._build_additional_details()

        self.doc.build(self.elements)
        #print(f"Successfully generated resume at: {self.pdf_path}")
        return self.pdf_path

    def _setup_styles(self):
        styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=16, textColor=colors.HexColor("#008bdc"))
        self.contact_style = ParagraphStyle('Contact', parent=styles['Normal'], fontSize=11, textColor=colors.HexColor("#555555"))
        self.section_heading = ParagraphStyle('SectionHeading', parent=styles['Heading5'], fontSize=12, textColor=colors.HexColor("#333333"), spaceAfter=10)
        self.body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=9, leading=15, textColor=colors.HexColor("#444444"))
        self.subheading_style = ParagraphStyle('Subheading', parent=styles['Heading6'], fontSize=9.8, leading=15, textColor=colors.HexColor("#333333"), spaceAfter=0)
        self.link_style = ParagraphStyle('Link', parent=self.subheading_style, textColor=colors.HexColor("#5555BB"))
        self.line_style = ParagraphStyle('Line', parent=styles['Normal'], fontSize=12, textColor=colors.HexColor("#C7CACB"), spaceAfter=10)

    def _build_header_and_objective(self):
        self.elements.append(Paragraph(self.data.get('name', 'Name Not Provided'), self.title_style))
        
        contact_parts = [
            self.data.get('email'),
            self.data.get('phone'),
            self.data.get('location')
        ]
        contact_string = " | ".join(part for part in contact_parts if part)
        if contact_string:
            self.elements.append(Paragraph(contact_string, self.contact_style))
        
        self.elements.append(Paragraph("____________________________________________________________________________________", self.line_style))
        self.elements.append(Spacer(1, 10))

        objective = self.data.get('objective', '')
        if objective:
            self.elements.append(Paragraph("CAREER OBJECTIVE", self.section_heading))
            self.elements.append(Paragraph(objective, self.body_style))
            self.elements.append(Spacer(1, 13))

    def _build_work_experience(self):
        experience = self.data.get('work_experience', [])
        if not experience:
            return

        self.elements.append(Paragraph("WORK EXPERIENCE", self.section_heading))
        for job in experience:
            title = job.get('title', 'Job Title')
            company = job.get('company', 'Company Name')
            duration = job.get('duration', 'Date Range')
            description = job.get('description', '')
            
            self.elements.append(Paragraph(f"{title} • {company} • {duration}", self.subheading_style))
            if description:
                self.elements.append(Paragraph(description, self.body_style))
            self.elements.append(Spacer(1, 12))

    def _build_education(self):
        education_list = self.data.get('education', [])
        if not education_list:
            return

        self.elements.append(Paragraph("EDUCATION", self.section_heading))
        for edu in education_list:
            degree = edu.get('degree', 'Degree Name')
            year = edu.get('year', 'Year')
            institution = edu.get('institution', 'Institution Name')

            self.elements.append(Paragraph(f"{degree} • {year}", self.subheading_style))
            self.elements.append(Paragraph(institution, self.body_style))
            self.elements.append(Spacer(1, 12))

    def _build_projects(self):
        projects = self.data.get('projects', [])
        if not projects:
            return

        heading = "PROJECT" if len(projects) == 1 else "PROJECTS"
        self.elements.append(Paragraph(heading, self.section_heading))

        for project in projects:
            name = project.get('projectName', 'Untitled Project')
            link = project.get('projectLink', '')
            desc = project.get('projectDesc', '')

            self.elements.append(Paragraph(name, self.subheading_style))
            if link:
                self.elements.append(Paragraph(f'<a href="{link}" target="_blank">{link}</a>', self.link_style))
            if desc:
                self.elements.append(Paragraph(desc, self.body_style))
            self.elements.append(Spacer(1, 12))
        self.elements.append(Spacer(1, 8))


    def _build_skills(self):
        skills = self.data.get('skills', [])
        if not skills:
            return

        self.elements.append(Paragraph("SKILLS", self.section_heading))
        
        bulleted_skills = [f"• {skill}" for skill in skills]

        num_columns = 3
        rows = [bulleted_skills[i:i + num_columns] for i in range(0, len(bulleted_skills), num_columns)]
        
        if rows and len(rows[-1]) < num_columns:
            rows[-1] += [''] * (num_columns - len(rows[-1]))

        if rows:
            skills_table = Table(rows, colWidths=[190] * num_columns)
            skills_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor("#333333")),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ]))
            self.elements.append(skills_table)
        self.elements.append(Spacer(1, 20))

    def _build_additional_details(self):
        details = self.data.get('additional_details', [])
        if not details:
            return

        self.elements.append(Paragraph("ACHIEVEMENTS", self.section_heading))
        for detail in details:
            self.elements.append(Paragraph(detail, self.body_style, bulletText='•'))


test_data = {
    'name': 'Aarav Sharma',
    'email': 'aarav.sharma@email.com',
    'phone': '+91 9876543210',
    'location': 'Bengaluru',
    'objective': (
        "Highly motivated software engineer with expertise in Java, Python, and cloud technologies. "
        "Eager to contribute to innovative projects and leverage strong problem-solving skills to "
        "develop robust and scalable applications."
    ),
    'work_experience': [
        {
            'title': 'Software Engineer • Internship',
            'company': 'Tech Solutions Inc., Bengaluru',
            'duration': 'Jan 2024 - Jun 2024',
            'description': "Developed and deployed microservices using Spring Boot and AWS, improving system efficiency by 15%."
        }
    ],
    'education': [
        {'degree': 'B.E, Computer Engineering', 'year': '2021 - 2025', 'institution': 'RV College of Engineering'},
        {'degree': 'Senior Secondary (XII), ISC', 'year': '2021', 'institution': 'St. Joseph\'s Boys\' High School'},
        {'degree': 'Secondary (X), ICSE', 'year': '2019', 'institution': 'St. Joseph\'s Boys\' High School'}
    ],
    'projects': [
        {'projectName': 'AI-Powered Chatbot', 'projectLink': 'https://github.com/example/chatbot', 'projectDesc': 'Designed and implemented a conversational AI chatbot using natural language processing (NLP).'},
        {'projectName': 'Smart Home Automation System', 'projectLink': '', 'projectDesc': 'Built an IoT-based system for controlling home appliances remotely via a mobile application.'}
    ],
    'skills': [
        'Java', 'Python', 'AWS', 'Spring Boot', 'SQL', 'MongoDB', 'REST APIs',
        'Data Structures', 'Algorithms', 'Machine Learning', 'Git', 'Docker'
    ],
    'additional_details': [
        "Hackathon Winner (2023)", "Volunteer at Local Community Center", "Published a research paper on distributed systems"
    ]
}


newDatax = {
  "selectedTemplateId": 1,
  "name": "Shivam Dhamejani",
  "email": "dhamejanishivam@gmail.com",
  "phone": "+919644971120",
  "location": "a",
  "objective": "a",
  "work_experience": [
    {
      "title": "a",
      "company": "a",
      "duration": "02/2022 - 02/2002",
      "description": "a"
    }
  ],
  "education": [
    {
      "degreeName": "a",
      "instituteName": "a",
      "startYear": "2022",
      "endYear": "2022",
      "location": "a"
    }
  ],
  "projects": [
    {
      "name": "a",
      "url": "",
      "description": "a"
    }
  ],
  "skills": [
    "a"
  ],
  "additional_details": [
    "a"
  ]
}

if __name__ == "__main__":
    import uuid 
    generator = ResumeGenerator(data=test_data, pdfName=str(uuid.uuid4()))