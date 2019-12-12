def validate_password(password):
    adjacent_digits = False
    always_ascending = True
    for i in range(len(password) - 1):
        if (password[i] == password[i + 1]) and \
                ((i >= (len(password) - 2)) or (password[i] != password[i + 2])) and \
                ((i == 0) or (password[i] != password[i - 1])):
            adjacent_digits = True
        elif int(password[i]) > int(password[i + 1]):
            always_ascending = False

    return always_ascending & adjacent_digits


if __name__ == "__main__":
    count = 0
    for pw in range(109165, 576723):
        if validate_password(str(pw)):
            count += 1

    print(count)
