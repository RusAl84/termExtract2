import os
import sys
from typing import NoReturn
import pysnooper
from PyQt5.QtGui import QIcon
from analysator import analyz
from source.source import Source
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from doc import DocxWorker
import docx
import json


class MainWidget(QMainWindow):
    def __init__(self):
        super(MainWidget, self).__init__()
        self.text = str()
        self.definition_list = list()
        self.expressions = dict()
        self.link = dict()
        self.docker = DocxWorker()
        uic.loadUi('./mainui.ui', self)

        self.textBrowser.setAcceptRichText(False)
        self.textBrowser.setOpenExternalLinks(True)
        self.pushButton.clicked.connect(self.btn_on_click)
        self.pushButton_2.clicked.connect(self.call_save)
        self.pushButton_3.clicked.connect(self.open_source_file)
        self.listWidget.itemClicked.connect(self.list_item_clicked)
        self.setWindowIcon(QIcon('./download.png'))

    def btn_on_click(self) -> NoReturn:
        self.listWidget.clear()
        flag = self.comboBox_5.currentText()
        self.definition_list = analyz(self.text, flag)


        self.choose_source()
        print(self.comboBox.currentText())
        print(self.comboBox_2.currentText())
        print(self.comboBox_3.currentText())

    @pysnooper.snoop()
    def load_source_text(self):
        self.textBrowser_2.append(self.text)

    def open_source_file(self):
        path = QFileDialog.getOpenFileName(self, 'Open file', './docx')[0]
        if os.path.exists(path):
            self.docker.get_path(path)
            text = self.docker.open_and_extract()
            self.text = text[0]
            self.load_source_text()

    @pysnooper.snoop()
    def list_item_clicked(self, item):
        self.textBrowser.clear()
        print(item.text())
        self.text_Browser(item.text())

    def choose_source(self):
        wikipedia = self.radioButton
        mas = self.radioButton_2

        if mas.isChecked():
            self.item_list_Widget('MAS')
        elif wikipedia.isChecked():
            self.item_list_Widget('Wiki')

    @pysnooper.snoop()
    def item_list_Widget(self, source_name) -> NoReturn:
        max_words = self.comboBox.currentText()
        max_term_count = self.comboBox_2.currentText()
        description_flag = self.comboBox_3.currentText()

        if source_name == 'Wiki':
            print('Here')
            self.expressions, self.link = Source(self.definition_list).wikipedia(max_words, max_term_count, description_flag)
        elif source_name == 'MAS':
            self.expressions, self.link = Source(self.definition_list).mas(max_words, max_term_count, description_flag)

        for _val, _it in self.expressions.items():
            self.listWidget.addItem(f'{_val}')


    @pysnooper.snoop()
    def text_Browser(self, word):
        print(self.link.items())
        if word in self.link:
            self.textBrowser.setHtml(f"""
                                {self.expressions[word]}<br/>
                                <a href={self.link[word]}>посмотреть в источке</a>""")
        else:

            self.textBrowser.setHtml(f"""<h1><b>{self.expressions[word]}</b></h1><br/>""")

    def call_save(self):
        self.save_result()

    @pysnooper.snoop()
    def save_result(self):
        if not os.path.exists('./result'):
            os.mkdir('./result')
        print(self.expressions)
        format = self.comboBox_4.currentText()

        if format == 'txt':
            with open(f'./result/{self.textEdit_2.toPlainText()}.txt', 'a', encoding='UTF-8') as f:
                    for _it, _val in self.expressions.items():
                        f.write(f'{_it}: {_val}\n')
        elif format == 'html':
            with open(f'./result/{self.textEdit_2.toPlainText()}.html', 'a') as html:
                html.write(f'<!DOCTYPE html>\n\
                            <html>\n\
                             <head>\n\
                               <title>Список терминов</title>\n\
                             </head>\n\
                             <body>\n')
                for _it, _val in self.expressions.items():
                    html.write(f'<p><b>{_it}</b>: {_val}</p>\n')

                html.write('</body>\n\
                        </html>')
        elif format == 'json':
            with open(f'./result/{self.textEdit_2.toPlainText()}.json', 'a') as js:
                json.dump(f'{self.expressions}', js, indent=4, ensure_ascii=False, sort_keys=True)

        elif format == 'docx':
            another_document = docx.Document()
            for item, value in self.expressions.items():
                another_document.add_paragraph(f'{item} : {value}')

            another_document.save(f'./result/{self.textEdit_2.toPlainText()}.docx')




if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("plastique")

    window = MainWidget()
    window.show()

    sys.exit(app.exec_())
