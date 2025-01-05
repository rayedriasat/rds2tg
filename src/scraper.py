import requests
from bs4 import BeautifulSoup
from config import WEBPAGE_URL
import logging
import os

logger = logging.getLogger(__name__)


def scrape_courses():
    try:
        SESSION_COOKIE = os.getenv("SESSION_COOKIE")
        CAPTCHA_TOKEN = os.getenv("CAPTCHA_TOKEN")
        headers = {
            "Cookie": f"ci_session={SESSION_COOKIE}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.",
            "Local-Storage": '{"_grecaptcha":' + CAPTCHA_TOKEN + "}",
        }
        response = requests.get(WEBPAGE_URL, verify=False, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        courses = []

        # Find the table with the course data
        table = soup.find("table", {"id": "offeredCourseTbl"})
        if table is None:
            logger.error("Failed to find the course table on the webpage")
            return []  # Return empty list instead of raising exception

        rows = table.find_all("tr")[1:]  # Skip the header row

        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 7:
                continue

            course_code = cols[1].text.strip()
            section = cols[2].text.strip()
            faculty_name = cols[3].text.strip()
            schedule = cols[4].text.strip()
            try:
                available_seats = int(cols[6].text.strip())
            except ValueError:
                available_seats = 0  # Default value if parsing fails

            courses.append(
                {
                    "course_code_section": f"{course_code}.{section}",
                    "faculty_name": faculty_name,
                    "schedule": schedule,
                    "available_seats": available_seats,
                }
            )

        return courses

    except requests.RequestException as e:
        logger.error(f"Failed to scrape courses: {str(e)}")
        return []  # Return empty list on error
