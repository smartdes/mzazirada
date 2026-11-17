from app.core.cache import STUDENT_CACHE

def process_ussd_session(phone_number: str, text: str) -> str:
    """
    Parses user input strings from Africa's Talking and returns CON or END menu responses.
    Input chains are asterisk-delimited, e.g., '', '1', '1*2'.
    """
    # Look up parent phone number in the fast in-memory cache
    student_data = STUDENT_CACHE.get(phone_number)
    if not student_data:
        return "END Sorry, your phone number is not registered in the MzaziRada system."

    # Split chained inputs into a list
    user_inputs = text.split("*") if text else []

    # Level 0: Main Menu (when text is empty on initial dial)
    if text == "":
        return (
            f"CON Welcome to MzaziRada!\n"
            f"Student: {student_data['name']}\n"
            f"1. Check Fee Balance\n"
            f"2. View Attendance\n"
            f"3. View Recent Grades"
        )

    # Level 1: First menu choice processing
    first_choice = user_inputs[0]

    if first_choice == "1":
        return (
            f"END Fee Balance for {student_data['name']} ({student_data['student_id']}):\n"
            f"Outstanding: {student_data['fees_due']}"
        )
    
    elif first_choice == "2":
        return (
            f"END Attendance Record for {student_data['name']}:\n"
            f"Status: {student_data['attendance']}"
        )
    
    elif first_choice == "3":
        return (
            f"END Recent Grades for {student_data['name']}:\n"
            f"{student_data['latest_grade']}"
        )
    
    else:
        return "END Invalid choice selected. Please try dialing again."
