from rutermextract import TermExtractor
from typing import List


def analyz(text: str, flag: str) -> List[str]:
    term_extractor = TermExtractor()
    definition_list: List[str] = list()

    if flag == 'Нет':
        for term in term_extractor(text):
            definition_list.append(term.normalized)
            print(str(term.normalized.split(' ')))
    else:
        for term in term_extractor.__call__(text, nested=True):
            definition_list.append(term.normalized)
            print(str(term.normalized.split(' ')))

    return definition_list