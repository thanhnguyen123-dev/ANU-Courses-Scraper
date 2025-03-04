import requests
import json

def fetch_anu_courses():
    url = 'https://programsandcourses.anu.edu.au/data/CourseSearch/GetCourses'
    
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

if __name__ == '__main__':
    fetch_anu_courses()