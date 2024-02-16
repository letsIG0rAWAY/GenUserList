import argparse
from transliterate import translit

def parseArguments() -> dict:
    parser = argparse.ArgumentParser(description="Generate userlist to brute force Active Directory environmen")
    parser.add_argument("-tfile", "--templatefile", required=True, type=str, help="path to file with username templates")
    parser.add_argument("-sufile", "--searchedusersfile", required=True, type=str, help="path to file with searched users")
    parser.add_argument("-enusfile", "--enumeratedusersfile", required=True, type=str, help='path to file to store enumerated usernames')
    args = parser.parse_args()
    argsdict = {}
    argsdict["templatefile"] = args.templatefile
    argsdict["searchedusersfile"] = args.searchedusersfile
    argsdict["enumeratedusersfile"] = args.enumeratedusersfile
    return argsdict

def handleName(searcheduserstr: str) -> list:
    trnamestr = translit(searcheduserstr, "ru", reversed=True).replace("'","")
    return trnamestr.lower().split()

def handleTemplate(templatestr: str) -> list:
    return templatestr.split()

def checkTemplate(searchedusermas: list, templatemas:list) -> bool:
    # функция зависит от правил, которые накладываются на содержимое файлов шаблонов и пользователей, которые описаны в README.md
    flag = True
    # полнота элементов. Количество составляющих в ФИО удовлетворяет количеству составляющих в шаблоне
    if "m" in templatemas and len(searchedusermas) < 3: flag = False
    # полнота элемента. Запрет использования полных версии при наличии менее двух букв.
    if "surname" in templatemas and len(searchedusermas[0]) < 2: flag = False
    if len(templatemas) > 1:
        if "name" in templatemas and len(searchedusermas[1]) < 2: flag = False
    if len(templatemas) > 2:
        if "middlename" in templatemas and len(searchedusermas[2]) < 2: flag = False
    return flag

def composeUsername(searchedusermas: list, templatemas:list) -> str:
    username = ""
    for templateel in templatemas:
        if "surname" == templateel: username += searchedusermas[0]
        elif "s" == templateel: username += searchedusermas[0][0]
        elif "name" == templateel: username += searchedusermas[1]
        elif "n" == templateel: username += searchedusermas[1][0]
        elif "middlename"== templateel: username += searchedusermas[2]
        elif "m" == templateel: username += searchedusermas[2][0]
        else: username += templateel
    return username

def generateUserList(templatesFilePath:str, searchedUsersFilePath:str, enumeratedUsersFilePath:str):
    with open(enumeratedUsersFilePath, "w") as enusfile:
        with open(templatesFilePath) as tfile:
            for templatestr in tfile:
                templatemas = handleTemplate(templatestr)
                with open(searchedUsersFilePath) as sufile:
                    for searcheduserstr in sufile:
                        searchedusermas = handleName(searcheduserstr)
                        if checkTemplate(searchedusermas, templatemas):
                            enusfile.write(composeUsername(searchedusermas, templatemas)+"\n")

if __name__ == "__main__":
    #templatesFilePath = "/home/kali/work/tools/infra/AD/GenUserList/templates.txt"
    #searchedUsersFilePath = "/home/kali/work/tools/infra/AD/GenUserList/searched_users.txt"
    #enumeratedUsersFilePath = "/home/kali/work/tools/infra/AD/GenUserList/enumerated_users.txt"
    argsdict = parseArguments()
    generateUserList(argsdict["templatefile"], argsdict["searchedusersfile"], argsdict["enumeratedusersfile"])
