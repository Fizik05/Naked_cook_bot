from types import NoneType
from bs4 import BeautifulSoup


class Step:
    def __init__(self):
        self.image = ""
        self.description = ""


def GettingSoup(response):
    """Обязательная хуйня."""
    return BeautifulSoup(response, 'html.parser')


def GettingName(response):
    """Получение названия."""
    soup = GettingSoup(response)
    main = soup.find('div', id='main')
    main1 = main.find('div', class_="container wrap columns is-centered")
    main2 = main1.find('main', class_="column is-relative is-centered")
    return main2.find('h1').text


def GettingRightHalf(response):
    """Обязательная хуйня."""
    soup = GettingSoup(response)
    main = soup.find('div', id='main')
    main1 = main.find('div', class_="container wrap columns is-centered")
    cont = main1.find('div', class_='content')
    return cont.find('div', class_="recipe-top columns")


def GettingIngridients(response):
    """Возвращаем массив с ингридиентами."""
    columns = GettingRightHalf(response)
    for i in columns:
        half = i
    metacont = half.find_all('meta')
    del metacont[0]
    ingrs = []
    for tag in metacont:
        ingrs.append(tag.get('content'))

    result = ""
    for i in ingrs:
        result += i + "\n"
    return result


def GettingNumServings(response):
    """Возвращаем кол-во порций."""
    columns = GettingRightHalf(response)
    for i in columns:
        half = i
    return half.find('div', id="kolvo_porcij_switcher_c").find('input').get('value')


def GettingSteps(response):
    """Возвращаем шаги с картинками."""
    soup = GettingSoup(response)
    main = soup.find('div', id='main')
    main1 = main.find('div', class_="container wrap columns is-centered")
    cont = main1.find('div', class_='content')
    sect = cont.find('section', id="pt_steps")
    ol = sect.find('ol', class_='instructions')
    Steps = []
    for step in ol:
        temp = Step()
        temp1 = step.find('a')
        if (temp1 is None) or (temp1 is NoneType) or (temp1 == -1):
            continue
        else:
            temp.description = temp1.get('title')
            temp.image = temp1.get('href')
            Steps.append(temp)
    return Steps


def WritingToFile(response):
    """Запись в файл."""
    with open("D:/123/ingrs.txt", 'w', encoding='utf-8') as f:
        f.write(GettingName(response) + '\n')
        f.write('' + '\n')
        f.write("Получится " + GettingNumServings(response) + " порций"+'\n')
        f.write('' + '\n')
        ingrs = GettingIngridients()
        for i in ingrs:
            f.write(i+'\n')
        f.write('' + '\n')
        steps = GettingSteps()
        for i in steps:
            f.write(i.image+' '+i.description+'\n')


def main():
    WritingToFile()


if __name__ == "__main__":
    main()
