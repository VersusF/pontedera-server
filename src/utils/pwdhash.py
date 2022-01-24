import bcrypt


def main():
    print("Insert password")
    pwd = input("> ")
    salt = bcrypt.gensalt()
    pwd_hash = bcrypt.hashpw(pwd.encode("utf8"), salt)
    print("Password hash")
    print(pwd_hash.decode("utf8"))
    print("Before putting this in the .env file remember to prefix $ (dollar) with a \ (backslash)")
    print("Paste this in the .env file")
    print(pwd_hash.decode("utf8").replace("$", "\\$"))


if __name__ == "__main__":
    main()
