from bs4 import BeautifulSoup
from re import sub, findall
from typing import Tuple, Dict, NoReturn
import requests
import pysnooper


def clear_html(infobox, elements, similar_projects, toc) -> NoReturn:
    if infobox:
        infobox.decompose()
    if elements.style:
        elements.style.decompose()
    if similar_projects:
        similar_projects.decompose()
    if toc:
        toc.decompose()
    pass


class Source:
    def __init__(self, definition_list):
        self.definition_list = definition_list
        self.link = dict()
        self.expressions: Dict[str, str] = dict()

    @pysnooper.snoop()
    def wikipedia(self, max_words, max_term_count, description_flag) -> Tuple[Dict[str, str], dict]:
        MAIN_URL = 'https://ru.wikipedia.org/wiki/'

        count = 0

        for definition in self.definition_list:
            if not definition.isdigit():
                r = requests.get(f'{MAIN_URL}{definition}')
                count += 1
                if r.status_code == 200:
                    soup = BeautifulSoup(r.text, 'html.parser')

                    infobox = soup.select_one('#mw-content-text > div > table:nth-child(2)')
                    elements = soup.find('div', class_='mw-parser-output')
                    similar_projects = soup.find(class_='ts-Родственные_проекты tright metadata plainlinks plainlist '
                                                        'ruwikiWikimediaNavigation')
                    toc = soup.find('div', id='toc')

                    clear_html(infobox, elements, similar_projects, toc)

                    # finding patten which looks like [1], [2] and removing them

                    try:
                        result = sub('\[\d{1,2}\]', '', elements.p.text)
                    except:
                        self.expressions[definition] = soup.ul.text
                        self.link[definition] = r.url
                        continue

                    whitespace = findall(r'\W', definition)
                    if not whitespace:
                        result_list = result.split(' ')
                    else:
                        self.expressions[definition] = result

                    if max_words.isdigit() and not whitespace:
                        try:
                            if ((':' not in result) or (len(result) > 63)) and (definition.capitalize() + '\n' != result):
                                self.expressions[definition] = ' '.join([result_list[index] for index in range(int(max_words))])
                                self.link[definition] = r.url
                            else:
                                self.expressions[definition] = soup.ul.text
                                self.link[definition] = r.url
                        except IndexError:
                            continue
                    else:
                        self.expressions[definition] = result
                    self.link[definition] = r.url

                else:
                    whitespace = findall(r'\W', definition)
                    if whitespace:
                        self.expressions[definition] = ' '

                    if description_flag == 'Нет' and not whitespace:
                        self.expressions[definition] = 'Not found'

                try:
                    if count == int(max_term_count):
                        break
                except ValueError:
                    continue

        return self.expressions, self.link

    @pysnooper.snoop()
    def mas(self, max_words, max_term_length, description_flag) -> Tuple[Dict[str, str], dict]:
        MAIN_URL = 'https://gufo.me/dict/mas/'

        count = 0
        print(self.definition_list)
        for definition in self.definition_list:
            if not definition.isdigit():
                print(definition)
                r = requests.get(f'{MAIN_URL}{definition.lower()}')
                count += 1
                if r.status_code == 200:
                    soup = BeautifulSoup(r.text, 'html.parser')

                    if len(soup.find_all('span')[4].text) > 16:
                        result = soup.find_all('span')[4].text
                    elif len(soup.find_all('span')[5].text) > 16:
                        result = soup.find_all('span')[5].text
                    else:
                        result = soup.find_all('span')[6].text

                    whitespace = findall(r'\W', definition)
                    if not whitespace:
                        result_list = result.split(' ')
                    else:
                        self.expressions[definition] = result

                    if max_words.isdigit() and not whitespace:
                        try:
                            self.expressions[definition] = ' '.join([result_list[index] for index in range(int(max_words))])
                        except IndexError:
                            self.expressions[definition] = result
                    else:
                        self.expressions[definition] = result

                    self.link[definition] = r.url


                else:
                    whitespace = findall(r'\W', definition)
                    if description_flag == 'Нет':
                        if whitespace:
                            self.expressions[definition] = " "
                        else:
                            self.expressions[definition] = 'No information'

                try:
                    if count == int(max_term_length):
                        break
                except ValueError:
                    continue

        return self.expressions, self.link


if __name__ == '__main__':
    value = Source(['версия'])
    print(value.mas())

