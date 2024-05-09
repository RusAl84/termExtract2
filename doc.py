import docx

class DocxWorker:
    def __init__(self):
        self.path_to_docx = str()
        self.text_from_docx = list()

    def get_path(self, path_to_docx):
        self.path_to_docx = path_to_docx

    def open_and_extract(self):
        document = docx.Document(self.path_to_docx)
        for line in document.paragraphs:
            if '\n' in line.text:
                needed_line = line.text
                needed_line = needed_line[0:needed_line.find('\n')]
                self.text_from_docx.append(needed_line)
            else:
                self.text_from_docx.append(line.text)

        return self.text_from_docx
