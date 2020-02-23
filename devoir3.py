# coding : utf-8
# Bonjour! Ici je tenterai de recenser toutes les espèces menacées au Québec ainsi que la date à laquelle elles ont été ajoutées à la liste. 

import requests, csv
from bs4 import BeautifulSoup

fichier = "especesMenacees.csv"

url = "https://mffp.gouv.qc.ca/la-faune/especes/liste-especes-vulnerables/"

entete = {
    "User-Agent" : "Ariane Chevrier, étudiante en journalisme à l'UQAM. Cette requête est envoyée dans le cadre d'un cours de journalisme de données."
}

contenu = requests.get(url, headers=entete)

page = BeautifulSoup(contenu.text, "html.parser")

# print(page) Le HTML de la page imprime bien

nomsFaune = page.find_all("div", class_="table-container")
# print(nomsFaune) Ce print me permet d'imprimer le contenu de tous les tableaux des espèces menacées ou vulnérables.

for nom in nomsFaune:
    especes = nom.find_all("h3")
    # print(especes)
    for espece in especes:
        # print("*"*10)
        # print(espece.text)
        # J'ai pu sortir tous les types d'animaux menacés.
        especesFinales = espece.text

        animaux = nom.find_all("a")
        # print(animaux)
        # Ce print me permet de générer le contenu des tableaux en-dessous des espèces. Mammifères [a href=https://>Alose savoureuse</a>, <a href=https: .... etc]
        for animal in animaux:
            # print(animal)
            prenom = animal.text
            # print(prenom)
            prenomsFinaux = prenom

            profil = animal["href"]
            # print(profil)
            # print("*"*10)
            # Jusqu'ici, j'ai réussi à sortir tous les noms des animaux avec l'URL vers leur profil. Les types d'animaux séparent également les différentes espèces. J'ai une section mammifères, une section poissons, une section tortues, etc. 
            # Ma prochaine étape, assez corsée pour moi, serait de travailler dans chaque URL pour aller chercher leur statut. Ils sont menacés/vulnérables depuis quand?



            url2 = profil
            entete2 = {
                "User-Agent" : "Ariane Chevrier, étudiante en journalisme à l'UQAM. Ces requêtes sont envoyées dans le cadre de mon cours de journalisme de données."
            }
            contenu2 = requests.get(url2, headers=entete2)
            pages2 = BeautifulSoup(contenu2.text, "html.parser")

            presqueStatut = pages2.find_all("table", id="AutoNumber2")
            # print(presqueStatut)
            for statut in presqueStatut:
                # print(statut)
                enfinStatut = statut.find_next("a")
                # print(enfinStatut.text)
                unJourStatut = enfinStatut.find_next("a")
                # print(unJourStatut)
                momentDonneStatut = unJourStatut.find_next("a")
                # print(momentDonneStatut.text)
                # (print("*"*10))
                statutFinal = momentDonneStatut.text

                # Tous ces find_next m'ont permis d'aller chercher le texte du statut. Comme chaque balise "a" avait un "onclick" qui portait le nom de l'espèce, j'ai dû me fier à la position de la balise pour ressortir le statut.
                # Je ne pouvais me fier au "onlick", car il ne fonctionnait que pour une espèce à la fois. 

            images = pages2.find_all("p", class_="credits")
            for image in images:
                photos = image.find("img")
                photo = photos["src"]
                # print("*"*10)
                # print(photo)

                # Je suis allée chercher le fichier de l'image, mais comme il ne s'affiche pas et n'est pas un URL, je ne suis pas certaine que ce soit pertinent.
                # Je vois sur internet qu'il faudrait installer quelque chose dans python pour traiter les images. Je vais m'en tenir qu'au nom de fichier, en imaginant les images! ;-)
                # Il me reste donc à créer mon fichier csv. 

                infos = [especesFinales, prenomsFinaux, profil, statutFinal, photo]

                enfin = open(fichier, "a")
                fini = csv.writer(enfin)
                fini.writerow(infos)