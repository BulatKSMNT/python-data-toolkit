import sys


def core(input_file):
    with open(input_file, 'r') as f:
        emails = f.read().splitlines()

    employees = []
    for email in emails:
        if not email:
            continue
        name_part = email.split('@')[0]
        name, surname = name_part.split('.')
        employees.append({
            'Name': name.capitalize(),
            'Surname': surname.capitalize(),
            'E-mail': email
        })

    with open('employees.tsv', 'w') as f:
        f.write("Name\tSurname\tE-mail\n")
        for emp in employees:
            f.write(f"{emp['Name']}\t{emp['Surname']}\t{emp['E-mail']}\n")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(1)
    core(sys.argv[1])