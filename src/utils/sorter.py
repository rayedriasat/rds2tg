def sort_courses(courses):
    """Sort courses by seats and section numbers"""

    def parse_course_info(course_code):
        # Split code and section
        base, section = course_code.split(".")
        # Remove L from base code if present
        base_code = base.rstrip("L")
        # Convert section to integer for numerical sorting
        section_num = int(section)
        # Check if it's a lab section
        is_lab = "L" in base
        return base_code, section_num, is_lab

    def get_sort_key(course):
        base_code, section_num, is_lab = parse_course_info(
            course["course_code_section"]
        )
        seats = int(course["available_seats"])
        return (
            -seats,  # Available seats (descending)
            base_code,  # Base course code
            section_num,  # Section number (ascending)
            is_lab,  # Theory before lab
        )

    return sorted(courses, key=get_sort_key)
