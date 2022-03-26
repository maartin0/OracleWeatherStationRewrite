import file

class CSVFile(file.File):
    """CSVFile object for storing data in CSV format"""
    def __init__(self, path, headers, delimiter=','):
        """Constructor:\n - CSVFile(path, headers, delimiter=',')\n\tpath: relative or absolute path of the file\n\theaders: list of file headers (i.e. first row of csv file)\n\tdelimiter (optional): optional alternative delimiter for the file"""
        super().__init__(path, delimiter.join(headers))
        self.headers = headers
        self.delimiter = delimiter

    @property
    def length(self):
        """Property returns number of lines in file"""
        return len(self.body_lines)

    def __len__(self):
        """Method returns number of lines in file"""
        return self.length

    def insert(self, *values):
        """Method inserts supplied values as arguments as a row in the file"""
        self.append(self.delimiter.join([str(value) for value in values]))
