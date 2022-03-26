import file

class CSVFile(file.File):
    def __init__(self, path, headers, delimiter=','):
        super().__init__(path, delimiter.join(headers))
        self.headers = headers
        self.delimiter = delimiter

    @property
    def length(self):
        return len(self.body_lines)

    def insert(self, *values):
        self.append(self.delimiter.join([str(value) for value in values]))
