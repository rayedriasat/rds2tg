import requests
from bs4 import BeautifulSoup
from config import WEBPAGE_URL


def scrape_courses():
    response = requests.get(WEBPAGE_URL)

    if response.status_code != 200:
        raise Exception("Failed to load the webpage.")

    soup = BeautifulSoup(response.content, "html.parser")
    courses = []

    # Find the table with the course data
    table = soup.find("table", {"id": "offeredCourseTbl"})
    if table is None:
        raise Exception("Failed to find the course table on the webpage.")
    rows = table.find_all("tr")[1:]  # Skip the header row

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 7:
            continue  # Skip rows that don't have enough columns

        course_code = cols[1].text.strip()
        section = cols[2].text.strip()
        faculty_name = cols[3].text.strip()
        schedule = cols[4].text.strip()
        available_seats = int(cols[6].text.strip())
        courses.append(
            {
                "course_code_section": f"{course_code}.{section}",
                "faculty_name": faculty_name,
                "schedule": schedule,
                "available_seats": available_seats,
            }
        )

    return courses
