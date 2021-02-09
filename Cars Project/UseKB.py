from pyswip import Prolog

prolog = Prolog()
prolog.consult("../data/knowledge_base.pl")


def addAssert (prolog, str):
    #prolog.assertz("fuel(diesel)")
    prolog.assertz(str)


def deleteAssert (prolog, str):
    #prolog.assertz("fuel(diesel)")
    prolog.retract(str)


def query (prolog, str):
    qr = (str +".")
    #q = list(prolog.query("modRequest(X, Y).")
    print(qr)
    return list(prolog.query(qr))


def fuelSearch():
    a= input("Quale tipologia di carburante ti interessa? ")
    a = a.lower()
    pippo = ("fuel(" + a + ")")
    addAssert(prolog, pippo)
    print(query(prolog, "companyModel(X, Y)"))
    deleteAssert(prolog, pippo)


def modelSearch():
    a= input("Di quale marca vuoi visualizzare i modelli disponibili? ")
    a = a.lower()
    print(query(prolog, "companyModel(\"" + a + "\", Y)"))


def modelBodySearch():
    a = input("Quale tipologia di auto ti interessa (hatchback, sedan, wagon, hardtop, convertible)? ")
    a = a.lower()
    print(query(prolog, "modelBody(X,\"" + a + "\")"))


print("########## BENVENUTO ##########")

#fuelSearch()

#modelSearch()

modelBodySearch()
