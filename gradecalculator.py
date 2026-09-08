import sys 
def get_letter_grade(percentage):
    if percentage >= 90: return 'A'
    elif percentage >= 80: return 'B'
    elif percentage >= 70: return 'C'
    elif percentage >= 60: return 'D'
    else: return 'F'

def main():
    print("CLI Student Grade Calculator")
    student_name = input("Enter student's name: ")
    
    try:
        num_subjects = int(input("How many subjects? "))
        if num_subjects <= 0:
            print("Number of subjects must be greater than 0.")
            sys.exit(1)
    except ValueError:
        print("Invalid input. Please enter a whole number.")
        sys.exit(1)

    subjects = []
    total_score = 0
    max_total = num_subjects * 100

    for i in range(num_subjects):
        while True:
            subject_name = input(f"\nEnter name for Subject {i+1}: ").strip()
            try:
                score = float(input(f"Enter score for {subject_name} (0-100): "))
                if 0 <= score <= 100:
                    subjects.append((subject_name, score))
                    total_score += score
                    break
                print("Error: Score must be between 0 and 100.")
            except ValueError:
                print("Error: Please enter a valid number.")

    percentage = (total_score / max_total) * 100
    grade = get_letter_grade(percentage)

    print("Percentage:",percentage)
    print("Final Grade:",grade)

if __name__ == "__main__":
    main()