import os
import re
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd

PATTERN_PROTOCOL_REGEX = "http[s]?://"
ROOT_FOLDER_PATH = "./Data"
ROOT_URL = "https://www.quattroruote.it/tutte-le-auto/ricerca-per-marca.html"
N_MAX = 2


def remove_protocol_url(url):
    if isinstance(url, str):
        url = re.sub(PATTERN_PROTOCOL_REGEX, "", url)
    else:
        raise ValueError("The object that was passed was not a string")

    return url


def get_relative_path_folder_html(root_folder_path, url):
    if isinstance(root_folder_path, str) and isinstance(url, str):
        url_tokenized = remove_protocol_url(url).split("/")
        folder_path = root_folder_path + "/" + url_tokenized[-2]  # This folder will contain the html page
        html_file_path = folder_path + "/" + url_tokenized[-1]
    else:
        raise ValueError("The values of the function must be strings")

    return folder_path, html_file_path


def create_folders(folder_path):
    if isinstance(folder_path, str):
        try:
            if not (os.path.exists(folder_path)):
                os.mkdir(folder_path)
        except OSError:
            print("The creation of the directory " + folder_path + " has failed")
    else:
        raise ValueError("The object that was passed was not a string")


def save_html_file(root_folder_path, url_string):
    if isinstance(root_folder_path, str) and isinstance(url_string, str):
        folder_path, html_file_path = get_relative_path_folder_html(root_folder_path, url_string)

        print(folder_path, html_file_path)

        if not os.path.exists(html_file_path):
            create_folders(folder_path)

            url = urllib.request.urlopen(url_string)
            soup = BeautifulSoup(url, "html.parser")

            html_page = open(html_file_path, mode="w")
            html_page.write(soup.__str__())
            html_page.close()

    else:
        raise ValueError("The values of the function must be strings")


# The last one element must be True if the web site use relative path, otherwise False
def save_website(root_folder_path, url_string, relative_path_online, visited_pages, data):
    if isinstance(root_folder_path, str) and isinstance(url_string, str) and isinstance(relative_path_online, bool):
        url = urllib.request.urlopen(url_string)
        soup = BeautifulSoup(url, "html.parser")

        split_url = url_string.split("/")
        if relative_path_online:
            path = split_url[-2] + "/"
        else:
            path = url_string.removesuffix(split_url[-1])

        #save_html_file(root_folder_path, url_string)

        i = 0
        for link in soup.findAll("a", href=True):
            link_string = str(link["href"])

            if path in link_string:
                if relative_path_online:
                    # Building the full link
                    link_string = split_url[0] + "//" + split_url[2] + link_string  # todo da rivedere

                if link_string not in visited_pages:
                    # link_string += ".html"
                    visited_pages.add(link_string)
                    print("Vado qui:", link_string)
                    i += 1

                    if i > N_MAX:
                        break

                    pippo(link_string, data)
                    save_website(root_folder_path, link_string, relative_path_online, visited_pages, data)

    else:
        raise ValueError("The first two values of the function must be strings, the last one must be bool")

def pippo(url_string, data):
    if isinstance(url_string, str):
        url = urllib.request.urlopen(url_string)
        soup = BeautifulSoup(url, "html.parser")

        car = [None for i in range(7)]
        flag = [False for i in range(7)]
        for list in soup.findAll("ul", class_="c-featureslist c-featureslist--style1"):
            for childList in list.findChildren("li"):
                string = childList.text
                tokenized_string = string.split(":")

                for string in tokenized_string:
                    if flag[0]:
                        car[0] = string
                        print(car[0])
                        flag[0] = False
                        break

                    if flag[1]:
                        car[1] = string
                        flag[1] = False
                        break

                    if flag[2]:
                        car[2] = string
                        flag[2] = False
                        break

                    if flag[3]:
                        car[3] = string
                        flag[3] = False
                        break

                    if flag[4]:
                        car[4] = string
                        flag[4] = False
                        break

                    if flag[5]:
                        car[5] = string
                        flag[5] = False
                        break

                    if flag[6]:
                        car[6] = string
                        flag[6] = False
                        break

                    if string == "Modello":
                        flag[0] = True
                        break

                    if string == "Posti":
                        flag[1] = True
                        break

                    if string == "Porte":
                        flag[2] = True
                        break

                    if string == "Alimentazione":
                        flag[3] = True
                        break

                    if string == "Cilindrata":
                        flag[4] = True
                        break

                    if string == "Velocità Massima":
                        flag[5] = True
                        break

                    if string == "Accelerazione":
                        flag[6] = True
                    break

        print(car)



    else:
        raise ValueError("")


visited_pages = set()
create_folders(ROOT_FOLDER_PATH)
data = pd.DataFrame(columns=["Modello", "Posti", "Porte"])
print(data)
save_website(ROOT_FOLDER_PATH, ROOT_URL, True, visited_pages, data)