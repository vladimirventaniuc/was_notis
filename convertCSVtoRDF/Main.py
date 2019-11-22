import pandas as pd
from rdflib import Graph, URIRef, BNode, Literal, Namespace
from random import randint
from rdflib.namespace import RDF, FOAF

def read_notaries():
    print("read notaries")
    list_of_notaries = []
    dfs = pd.read_excel("notari.xlsx")
    for index, row in dfs.iterrows():
        # print(index, row["Nume si prenume"])
        lastNameFirstName = row["Nume si prenume"].split(" ");
        lastName = lastNameFirstName[0]
        firstName = ' '.join(lastNameFirstName[1:]).strip()
        room = row["Camera"].strip()
        address = row["Adresa sediu"]
        city = row["Localitate"]
        county = row["Judet"]
        phoneNo = "0" + str(random_with_N_digits(9))
        notary = {
            "lastName" : lastName,
            "firstName" : firstName,
            "room" : room,
            "address":address,
            "city":city,
            "county":county,
            "phoneNo":phoneNo
        }
        list_of_notaries.append(notary)
        # TO DO ACTE

    return list_of_notaries
def read_translators():
    print("read notaries")
    list_of_translators = []
    dfs = pd.read_excel("traducatori.xlsx")
    for index, row in dfs.iterrows():
        # print(index, row["Nume si prenume"])
        lastNameFirstName = row["Nume si prenume"].split(" ");
        lastName = lastNameFirstName[0]
        firstName = ' '.join(lastNameFirstName[1:]).strip()
        court_of_Appeal = row["Curtea de Apel"]
        languages = row["Limbi"].replace(" ","").split(",")
        county = row["judet"]
        phoneNo = editPhoneNumber(row["Telefon"])
        authorisationNo = row["Numar autorizatie"]
        translator = {
            "lastName": lastName,
            "firstName": firstName,
            "county": county,
            "phoneNo": phoneNo,
            "county": county,
            "court_of_appeal": court_of_Appeal,
            "languages": languages,
            "authorisation_no":authorisationNo
        }
        list_of_translators.append(translator)
        # print(translator)
        # TO DO ACTE
    return list_of_translators

def editPhoneNumber(phoneNo):
    phoneNo = str(phoneNo)
    if(len(phoneNo) == 0):
        return "0" + str(random_with_N_digits(9))
    else:
        phoneNo = phoneNo.replace(" ","").replace("/","").replace(".","")
        if len(phoneNo)>=10:
            return  phoneNo[:10]
        else:
            return "0" + str(random_with_N_digits(9))
def random_with_N_digits(n):
        range_start = 10 ** (n - 1)
        range_end = (10 ** n) - 1
        return randint(range_start, range_end)

def createRDF(list_of_notaries, list_of_translators):

    notaryClass = URIRef("https://www.merriam-webster.com/dictionary/notary%20public")
    translatorClass = URIRef("https://www.merriam-webster.com/dictionary/translator")
    addressClass = URIRef("https://dictionary.cambridge.org/dictionary/english/address")
    gg = Graph()
    gg.add((notaryClass, RDF.type, FOAF.Person))
    gg.add((translatorClass, RDF.type, FOAF.Person))

    for i in range(10):
        notary = list_of_notaries[i]
        identificator = str(notary["firstName"] +"_"+ notary["lastName"]).replace(" ","_")
        # print(identificator)
        address = URIRef("https://address.org/id/" + str(notary["city"]).replace(" ","_"))
        person = URIRef("http://example.org/people/"+identificator)
        gg.add((person, RDF.type, notaryClass))
        gg.add((person, FOAF.firstName, Literal(notary["firstName"])))
        gg.add((person, FOAF.lastName, Literal(notary["lastName"])))
        gg.add((person, FOAF.phoneNo, Literal(notary["phoneNo"])))
        gg.add((address, FOAF.street, Literal(notary["address"])))
        gg.add((address, FOAF.county, Literal(notary["county"])))
        gg.add((address, FOAF.city, Literal(notary["city"])))
        gg.add((person, FOAF.address, address))
        #TO DO DOCUMENTS


    for i in range(10):
        translator = list_of_translators[i]
        identificator = str(translator["firstName"] + "_" + translator["lastName"]).replace(" ", "_")
        #print(identificator)
        print(translator["languages"])
        address = URIRef("https://address.org/id/" + translator["court_of_appeal"].replace(" ", "_"))
        language = URIRef("https://en.wikipedia.org/wiki/Language"+identificator)
        person = URIRef("http://example.org/people/" + identificator)
        gg.add((person, RDF.type, translatorClass))
        gg.add((person, FOAF.firstName, Literal(translator["firstName"])))
        gg.add((person, FOAF.lastName, Literal(translator["lastName"])))
        gg.add((person, FOAF.phoneNo, Literal(translator["phoneNo"])))
        gg.add((address, FOAF.county, Literal(translator["county"])))
        gg.add((address, FOAF.city, Literal(translator["court_of_appeal"])))
        gg.add((person, FOAF.address, address))
        gg.add((person, FOAF.languages, Literal(translator["languages"])))

    file2 = open("output2.txt", "wb")
    file2.write(gg.serialize(format='pretty-xml'))

def main():
    list_of_notaries= read_notaries()
    list_of_translators = read_translators()
    createRDF(list_of_notaries, list_of_translators)



if __name__ == '__main__':
    main()

