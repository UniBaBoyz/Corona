from utils import removeSpaces


def userQuery():
    query = input("Insert query:")
    query = removeSpaces(query)
    tokenized_string = query.split(sep="and")
    print(tokenized_string)
    for string in tokenized_string:
        if string == "name":
            print("name")
        elif string == "fuel":
            print("fuel")


userQuery()
