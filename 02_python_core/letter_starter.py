import sys

def generate(email):
    try:
        with open('employees.tsv', 'r') as f:
            lines = f.readlines()[1:]
            for line in lines:
                name, surname, emp_email = line.strip().split('\t')
                if emp_email == email:
                    return f"Dear {name}, welcome to our team. We are sure that it will be a pleasure to work with you. That's a precondition for the professionals that our company hires."
        return "Email not found in records"
    except FileNotFoundError:
        return "Employee database not found"

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(1)
    print(sys.argv[1])
    print(generate(sys.argv[1]))