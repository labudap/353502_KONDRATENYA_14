from django.utils import timezone
from main.models import JobVacancy

# List of vacancies to create
vacancies = [
    {
        'title': 'Pharmacist',
        'description': 'Consulting clients on medications, dispensing prescription and over-the-counter drugs, monitoring medication expiration dates.',
        'requirements': '• Higher pharmaceutical education\n• 1+ years of experience\n• Knowledge of pharmacology\n• Cash register operation skills\n• Responsibility and attention to detail',
        'salary_range': 'from 1500 to 2000 BYN',
    },
    {
        'title': 'Clinical Pharmacist',
        'description': 'Managing pharmacy inventory, quality control of medicines, organizing storage of drugs, maintaining documentation.',
        'requirements': '• Higher pharmaceutical education\n• 3+ years of experience\n• Advanced knowledge of pharmacology\n• Personnel management skills\n• Knowledge of regulatory documentation',
        'salary_range': 'from 2000 to 2500 BYN',
    },
    {
        'title': 'Pharmacy Manager',
        'description': 'Managing the pharmacy, organizing staff work, monitoring compliance with pharmaceutical procedures, interacting with suppliers.',
        'requirements': '• Higher pharmaceutical education\n• 5+ years of experience\n• Pharmacy management experience\n• Knowledge of business processes\n• Leadership qualities',
        'salary_range': 'from 2500 to 3000 BYN',
    },
    {
        'title': 'Pharmacy Consultant',
        'description': 'Consulting customers on medical cosmetics and parapharmaceuticals, conducting presentations of new products.',
        'requirements': '• Secondary pharmaceutical education\n• 1+ years of experience\n• Knowledge of cosmetic brands\n• Sales skills\n• Communication skills',
        'salary_range': 'from 1300 to 1800 BYN',
    },
    {
        'title': 'Pharmacy Analyst',
        'description': 'Conducting quality control of medicines, analyzing documentation, maintaining quality reporting.',
        'requirements': '• Higher pharmaceutical education\n• 2+ years of experience\n• Knowledge of analysis methods\n• Attention to detail\n• Analytical thinking',
        'salary_range': 'from 1800 to 2200 BYN',
    },
    {
        'title': 'Procurement Manager',
        'description': 'Organizing and controlling the procurement of medicines, working with suppliers, optimizing warehouse stocks.',
        'requirements': '• Higher education\n• 2+ years of procurement experience\n• Knowledge of pharmaceutical market\n• Negotiation skills\n• Excel proficiency',
        'salary_range': 'from 2000 to 2500 BYN',
    },
    {
        'title': 'Pharmacy Technologist',
        'description': 'Preparation of pharmaceutical forms according to prescriptions and department requirements, quality control of prepared medications.',
        'requirements': '• Higher pharmaceutical education\n• 3+ years of experience\n• Knowledge of drug manufacturing technology\n• Knowledge of technical documentation\n• Accuracy',
        'salary_range': 'from 1700 to 2200 BYN',
    },
    {
        'title': 'Drug Registration Specialist',
        'description': 'Preparing documentation for drug registration, interaction with regulatory authorities.',
        'requirements': '• Higher pharmaceutical education\n• 2+ years of experience\n• Knowledge of regulatory requirements\n• English language B2 level\n• Attention to detail',
        'salary_range': 'from 2200 to 2700 BYN',
    },
    {
        'title': 'Medical Representative',
        'description': 'Promoting company products, working with doctors and pharmacies, conducting presentations, market monitoring.',
        'requirements': '• Higher medical/pharmaceutical education\n• 1+ years of experience\n• Presentation skills\n• Driving license\n• Communication skills',
        'salary_range': 'from 2000 to 3000 BYN',
    },
    {
        'title': 'Drug Information Specialist',
        'description': 'Providing information about medications to medical professionals and the public, conducting reference work.',
        'requirements': '• Higher pharmaceutical education\n• 2+ years of experience\n• Excellent knowledge of pharmacology\n• Database management skills\n• Excellent communication skills',
        'salary_range': 'from 1600 to 2100 BYN',
    },
]

# Delete existing vacancies
JobVacancy.objects.all().delete()

# Create new vacancies
for vacancy in vacancies:
    JobVacancy.objects.create(
        title=vacancy['title'],
        description=vacancy['description'],
        requirements=vacancy['requirements'],
        salary_range=vacancy['salary_range'],
        is_active=True,
        date_posted=timezone.now()
    )

print('Vacancies successfully created!') 