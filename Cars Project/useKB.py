from pyswip import Prolog

prolog = Prolog()
prolog.consult("../data/knowledge_base.pl")


def addAssert(prolog, str):
    prolog.assertz(str)


def deleteAssert(prolog, str):
    prolog.retract(str)


def query(prolog, str):
    qr = (str + ".")
    return list(prolog.query(qr))


def fuelSearch():
    a = input("Quale tipologia di carburante ti interessa? ")
    a = a.lower()
    print(query(prolog, "fuelCar(X,\"" + a + "\")"))


def modelSearch():
    a = input("Di quale marca vuoi visualizzare i modelli disponibili? ")
    a = a.lower()
    print(query(prolog, "companyModel(\"" + a + "\", Y)"))


def companySearch():
    a = input("Di quale modello vuoi sapere la marca? ")
    a = a.lower()
    print(query(prolog, "companyModel(X,\"" + a + "\")"))


def budgetSearch():
    a = input("Quale fascia di prezzo di marca ti interessa (bassa/media/alta)? ")
    a = a.lower()
    if a == "bassa":
        a = "budget"
    elif a == "media":
        a = "medium"
    elif a == "alta":
        a = "highend"
    else:
        print("Scelta errata")
    print(query(prolog, "carsrange(X,\"" + a + "\")"))


def modelBodySearch():
    a = input("Quale tipologia di auto ti interessa (hatchback, sedan, wagon, hardtop, convertible)? ")
    a = a.lower()
    print(query(prolog, "modelBody(X,\"" + a + "\")"))


print("########## BENVENUTO ##########")
answer = input("Area di interesse:\n"
               "1) CARBURANTE \n"
               "2) MARCA->MODELLO \n"
               "3) MODELLO->MARCA \n"
               "4) TIPOLOGIA\n"
               "5) BUDGET\n"
               "X) USCITA\n"
               "Quale area di interesse visualizzare?: ")
while answer[0] != ("x") and answer[0] != ("X"):
    if answer[0] == "1":
        fuelSearch()
    elif answer[0] == "2":
        modelSearch()
    elif answer[0] == "3":
        companySearch()
    elif answer[0] == "4":
        modelBodySearch()
    elif answer[0] == "5":
        budgetSearch()
    else:
        print("RISPOSTA ERRATA!")
    answer = input("Quale area di interesse visualizzare?: ")
