from diffie_hellman import get_keys, User
from aes import encrypt, decrypt

users = [
    User(id=1, name='Alice'),
    User(id=2, name='Bob'),
    User(id=3, name='Charlie'),
]

us = get_keys(users)
for u in us:
    print(u.private_key)

"""1 - Add user\
2 - Remove user\
3 - Send message\
4 - Exit
"""

rec = True

while True:

    if len(users) > 1 and rec:
        get_keys(users)

    rec = False
    user_input = int(input("Next action: "))
    print()

    if user_input == 1:

        name = input("Enter name: ")
        id = users[-1].id + 1
        user = User(id=id, name=name)
        users.append(user)
        rec = True

    elif user_input == 2:

        user_id = int(input("Enter user id: "))
        for u in users:
            if u.id == user_id:
                users.remove(u)
                rec = True

        if not rec:
            print("User does not exist!")

    elif user_input == 3:

        user_id = int(input("Enter user id: "))
        user = None
        for u in users:
            if u.id == user_id:
                user = u

        if user is None:
            print("User does not exist!")
            continue

        message = input("Enter user message: ")
        enc_message = encrypt(message, str(user.private_key))
        print(enc_message)

        for u in users:
            dec_message = decrypt(enc_message, str(user.private_key))
            print(f"User {u.id} received message: ")
            print(dec_message)

    elif user_input == 4:
        break

    else:
        print("Invalid input! Try again.\n")
