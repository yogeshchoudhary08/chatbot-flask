import requests
from bs4 import BeautifulSoup
from plyer import notification

def check_freelance_projects():
    # This is where you fetch your projects, example placeholder:
    
    projects = [
        {'budget': '$1000', 'description': 'Web development project to create an e-commerce site.'},
        {'budget': '$500', 'description': 'Python script automation for data scraping from websites.'},
        {'budget': '$750', 'description': 'Design and implement a chatbot using AI techniques.'},
        {'budget': '$1200', 'description': 'Full-stack development of a social media app.'},
        {'budget': '$450', 'description': 'Bug fixing and optimization of an existing Django application.'},
        {'budget': '$900', 'description': 'Mobile app development for Android platform using Kotlin.'},
        {'budget': '$1500', 'description': 'Develop ML model for predictive analytics on sales data.'},
        {'budget': '$1100', 'description': 'Data science project to analyze customer churn patterns.'},
        {'budget': '$1300', 'description': 'AI-based recommendation system for an online platform.'},
        {'budget': '$1000', 'description': 'Natural Language Processing (NLP) project for sentiment analysis.'},
        {'budget': '$1400', 'description': 'Build and deploy deep learning model for image classification.'},
    ]

    for project in projects:
        notification.notify(
            title=f"New Project: {project['budget']}",
            message=project['description'][:100],
            app_name="Freelance Bot"
        )

if __name__ == "__main__":
    check_freelance_projects()
