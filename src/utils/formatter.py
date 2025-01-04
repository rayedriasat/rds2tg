def format_courses(courses):
    if not courses:
        return "No courses found."

    header = "Course.Section | Faculty | Schedule | Seats Available"
    separator = "-" * len(header)
    formatted_courses = [header, separator]

    for course in courses:
        formatted_courses.append(
            f"{course['available_seats']} | {course['faculty_name']} | {course['course_code_section']} | {course['schedule']}"
        )

    return "\n".join(formatted_courses)


def format_empty_response():
    return "No courses found."
