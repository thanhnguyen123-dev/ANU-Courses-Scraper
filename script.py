import requests
import json
from bs4 import BeautifulSoup
import time

def fetch_anu_courses():
    url = 'https://programsandcourses.anu.edu.au/data/CourseSearch/GetCourses'
    base_course_url = 'https://programsandcourses.anu.edu.au/2025/course/'
    
    # Query parameters matching the JavaScript version
    params = {
        'AppliedFilter': 'FilterByCourses',
        'Source': '',
        'ShowAll': 'true',
        'PageIndex': '0',
        'MaxPageSize': '10',
        'PageSize': 'Infinity',
        'SortColumn': '',
        'SortDirection': '',
        'InitailSearchRequestedFromExternalPage': 'false',
        'SearchText': '',
        'SelectedYear': '2025',
        'Careers[]': ['', '', '', ''],
        'GraduateAttributes[]': ['', '', ''],
        'OtherCriteria[]': ['', ''],
        'Sessions[]': ['', '', '', '', '', ''],
        'DegreeIdentifiers[]': ['', '', ''],
        'FilterByMajors': '',
        'FilterByMinors': '',
        'FilterBySpecialisations': '',
        'CollegeName': 'All Colleges',
        'ModeOfDelivery': 'All Modes'
    }

    try:
        # Make the request
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse the JSON response
        data = response.json()

        course_data = [
            course for course in data.get('Items', [])
            if not course.get('CourseCode', '').startswith('EXTN')
        ]

        for course in course_data:
            course_code = course.get('CourseCode')
            course_url = f"{base_course_url}{course_code}"

            extra_details = scrape_course_details(course_url)
            if extra_details:
                course.update(extra_details)
                print(f"Updated course: {course}")

        # Write the Items array to a JSON file with proper formatting
        with open('courses.json', 'w', encoding='utf-8') as f:
            json.dump(data['Items'], f, indent=2)
        
        print('Data has been written to courses.json')
        print(f"Total courses saved: {len(data['Items'])}")
        
    except requests.exceptions.RequestException as e:
        print(f'Error fetching data: {e}')
    except json.JSONDecodeError as e:
        print(f'Error parsing JSON: {e}')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')

def scrape_course_details(course_url):
    try:
        response = requests.get(course_url)
        print(f"Scraping {course_url}")
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        intro_div = soup.find('div', id='introduction')

        description = []
        prerequisites = []

        if intro_div:
            paragraphs = intro_div.find_all('p')
            description = [
                p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)
            ]

        prerequisites_div = soup.find('div', class_='requisite')
        if prerequisites_div:
            prerequisites = [
                prereq.strip() 
                for prereq in prerequisites_div.get_text().split('\n') 
                if prereq.strip()
            ]

        return {
            "description": description,
            "prerequisites": prerequisites
        }
    except requests.exceptions.RequestException as e:
        print(f'Error fetching course details: {e}')
        return None



if __name__ == '__main__':
    fetch_anu_courses()