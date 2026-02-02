# EmpowerAI – AI Based Job Matching Platform

EmpowerAI is a full-stack Django web application that connects mentors and housewives through skill-based job opportunities using AI logic.

## 🔥 Key Features
- Role-based login (Mentor / Housewife)
- Mentors can post jobs and manage applicants
- Housewives can upload resume and apply for jobs
- Resume upload (PDF)
- Automatic skill extraction from resume
- AI-based job matching score
- Job ranking based on skill match
- Responsive UI using Bootstrap

## 🤖 AI / ML Logic
- Resume text extracted using PyPDF2
- Skills parsed using keyword-based NLP logic
- Job matching score calculated based on skill similarity
- Jobs sorted based on match percentage

## 🛠 Tech Stack
- Backend: Python, Django
- Frontend: HTML, CSS, Bootstrap
- Database: MySQL (Development)
- AI Logic: Python (NLP basics)
- Resume Parsing: PyPDF2
- Version Control: Git & GitHub

## 👤 User Roles
### Mentor
- Create job posts
- View applicants
- Shortlist or reject candidates

### Housewife
- Upload resume
- View matched jobs
- Apply for jobs
- Track application status

## ⚙️ Project Setup
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
