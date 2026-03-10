# DTE Student Assistant - Comprehensive Knowledge Base
# Separate from logic for easier maintenance and expansion.

INTENTS = [
    {
        "patterns": ["hello", "hi", "hey", "greetings", "good morning", "good afternoon", "is anyone there", "help", "anybody help", "namaste"],
        "response": "Hello! I am your **DTE AI Expert**. I'm here to guide you through admissions, exams, scholarships, and your future career paths. How can I assist you today?"
    },
    {
        "patterns": ["admission", "how to join", "entry", "apply for diploma", "registration", "counselling", "cap process", "admission process", "eligibility", "enrollment", "application form", "join polytechnic", "cutoff marks"],
        "response": "The **Centralized Admission Process (CAP)** is handled via the official DTE portal. Admission typically begins in **May-June** after SSLC results. You need your 10th marks, 7-year study certificate, and reservation documents (Caste/Income) ready for the online application. Cutoffs depend on your category and branch popularity."
    },
    {
        "patterns": ["syllabus", "curriculum", "subjects", "what will i study", "course details", "branch syllabus", "c-20", "c20", "study material", "notes", "blue print"],
        "response": "Most DTE branches follow the **C-20 Curriculum**, which is outcome-based and industry-aligned. You can download the latest branch-wise syllabus PDFs, unit-wise blueprints, and academic calendars from the 'Academics' -> 'Syllabus' section of the DTE portal. Highly recommend checking the **Course Outcomes (COs)** for each subject!"
    },
    {
        "patterns": ["exam", "timetable", "test schedule", "semester exams", "when is the exam", "board exam", "theory exams", "practicals", "hall ticket", "exam circular"],
        "response": "DTE Board Exams (BTE) are typically held in **Nov/Dec** for Odd Semesters and **April/May** for Even Semesters. The final timetable is released on the official website about 2-3 weeks before exams. **Practical Exams** usually happen *before* theory exams—stay in touch with your department HOD for the internal schedule!"
    },
    {
        "patterns": ["results", "marks list", "pass", "fail", "score", "percentage", "marks card", "btelinx", "check results", "grade card"],
        "response": "You can check your results on the **BTE results portal (often BTELinx)** using your Register Number. Results usually come out 45-60 days after the last exam. If your results show 'W' (Withheld), immediately contact your college principal."
    },
    {
        "patterns": ["revaluation", "rv", "rt", "retotalling", "photocopy", "challenge valuation", "failed subjects"],
        "response": "If you're unhappy with your marks, you can apply for **Photocopy** or **Re-totalling (RV/RT)** within 1 week of result declaration. Fees apply per subject. If you have backlogs, you must clear them in the supplementary exams to be eligible for your final degree."
    },
    {
        "patterns": ["scholarship", "money", "free education", "fees backup", "financial aid", "SSP", "NSP", "OBC scholarship", "SC ST scholarship", "post matric", "minority scholarship"],
        "response": "The **State Scholarship Portal (SSP)** is the primary platform for Karnataka students. Ensure your Aadhaar is linked to your bank account and your RD numbers are valid. For SC/ST and OBC students, the amount is credited directly via DBT (Direct Benefit Transfer). Frequently check your SSP status for updates like 'Push to DBT'."
    },
    {
        "patterns": ["fees", "total cost", "college fees", "payment", "exam fee", "late fee", "examination fee", "challan"],
        "response": "Fees vary: Government colleges attract minimal fees (~₹4,000/year), Aided (~₹10,000/year), and Private (~₹25,000+/year). Exam fees (approx. ₹600) must be paid via the portal or designated banks before the deadline to avoid a ₹1000 late fine."
    },
    {
        "patterns": ["attendance", "75%", "shortage", "attendance rule", "condonation", "absent", "medical leave"],
        "response": "Students must maintain a minimum of **75% attendance** in each subject. If you fall below 75%, you will be **detained** and not allowed to write exams. Medical certificates may be accepted in extreme cases with a condonation fee, but only if you have at least 60% attendance."
    },
    {
        "patterns": ["internals", "internal marks", "cia", "ia tests", "assignment marks", "lab marks", "record marks", "viva"],
        "response": "Your **Continuous Internal Evaluation (CIE)** includes two internal tests, assignments, and lab records. These marks contribute significantly to your final SGPA. Lab attendance and record submission are mandatory to get full internal marks!"
    },
    {
        "patterns": ["dcet", "lateral entry", "b.e", "btech", "degree after diploma", "engineering entry", "karnataka examination authority", "kea", "entrance exam"],
        "response": "For Lateral Entry into the 2nd year of Engineering (B.E/B.Tech), you must qualify for the **DCET (Diploma Common Entrance Test)** conducted by KEA. The syllabus was updated recently—focus on Applied Math and Engineering science. DCET usually happens in **July/August**."
    },
    {
        "patterns": ["career", "job", "what after diploma", "salary", "junior engineer", "placement", "internship", "psu job"],
        "response": "Diplomates have huge demand! You can become a **Junior Engineer (JE)** in PWD, KPTCL, or BESCOM. Private companies like Tata, L&T, and Reliance also hire. Alternatively, pursue B.E via DCET or B.Voc for specialized skills. Don't forget to register on the **NATS portal** for apprenticeships!"
    },
    {
        "patterns": ["transfer", "migration", "change college", "branch change", "mutual transfer"],
        "response": "Branch changes are only permitted in the 3rd semester based on vacancy and merit. College transfers (Migration) also follow strict DTE norms and usually require a 'No Objection Certificate' (NOC) from both institutions."
    },
    {
        "patterns": ["thank you", "thanks", "helpful", "good bot", "you are great"],
        "response": "You're very welcome! I'm proud to help the diploma student community. Knowledge is power—study hard!"
    }
]

DTE_PERSONA = """
You are the "DTE AI EXPERT", the ultimate guide for Diploma students under the Department of Technical Education (DTE). 
Your intelligence is comparable to ChatGPT, but your heart and knowledge belong to the DTE student community.

CONTEXT:
You are an expert on the C-20 Curriculum, DCET (Diploma Common Entrance Test), Lateral Entry to B.E/B.Tech, SSP/NSP Scholarships, and the Centralized Admission Process (CAP).

GUIDELINES:
1. Provide deep, structured insights—go beyond one-sentence answers.
2. Use Markdown: # for headings, **bold** for key dates, and <ul> for lists.
3. If a student asks "How are you?", respond warmly as an AI companion.
4. For technical DTE queries (like 'DCET syllabus'), provide specific, reliable advice.
5. If the student's request is vague, ask clarifying questions like "Are you asking about the Odd or Even semester?"
"""
