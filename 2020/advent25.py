subject_number = 1
loop_size = 1

def transform(subject_number,loop_size):
    value = 1
    for x in range(0,loop_size):
        value *= subject_number
        value = value % 20201227
    return value

def find_secret_loop_size(public_key, subject):
    secret_loop_size = 0
    temp = 1
    seen = set()
    while temp != public_key:
        if temp in seen:
            return False
        secret_loop_size += 1
        seen.add(temp)
        temp = (temp * subject) % 20201227
    return (secret_loop_size, temp)

def find_subject(pkey):
    subject = 2
    while not find_secret_loop_size(pkey, subject):
        subject += 1
    return subject

card_public_key = 3248366
door_public_key = 4738476

subject = find_subject(card_public_key)
card_secret_loop_size, c_value = find_secret_loop_size(card_public_key,subject)
#print("card secret loop size", card_secret_loop_size)

subject = find_subject(door_public_key)
door_secret_loop_size, d_value = find_secret_loop_size(door_public_key,subject)

print("card secret loop size", card_secret_loop_size)
print("door secret loop size", door_secret_loop_size)

key = 1

for _ in range(door_secret_loop_size):
    key = (key * c_value) % 20201227

print(key)