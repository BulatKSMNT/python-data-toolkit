import sys
def call_center(clients, recipients):
    return list(set(clients) - set(recipients))

def potential_clients(participants, clients):
    return list(set(participants) - set(clients))

def loyalty_program(clients, participants):
    return list(set(clients) - set(participants))

def core():
    if len(sys.argv) != 2:
        return
    clients = ['andrew@gmail.com', 'jessica@gmail.com', 'ted@mosby.com',
               'john@snow.is', 'bill_gates@live.com', 'mark@facebook.com',
               'elon@paypal.com', 'jessica@gmail.com']
    participants = ['walter@heisenberg.com', 'vasily@mail.ru',
                    'pinkman@yo.org', 'jessica@gmail.com', 'elon@paypal.com',
                    'pinkman@yo.org', 'mr@robot.gov', 'eleven@yahoo.com']
    recipients = ['andrew@gmail.com', 'jessica@gmail.com', 'john@snow.is']

    task = sys.argv[1]

    if task == 'call_center':
        result = call_center(clients, recipients)
    elif task == 'potential_clients':
        result = potential_clients(participants, clients)
    elif task == 'loyalty_program':
        result = loyalty_program(clients, participants)
    else:
        raise Exception("Invalid task name")

    for email in sorted(result):
        print(email)


if __name__ == '__main__':
    core()