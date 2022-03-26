import os

class File:
    """Generic file object for storing data"""
    def __init__(self, path, header=''):
        """Constructor:\n - File(path, header='')\n\tpath: absolute or relative path of file\n\theader: optional header of file, will only be written if the file doesn't exist"""
        self.path = path
        self.header = header
        self.file_obj = None

    @property
    def abs_path(self):
        """Property returns absolute path of file"""
        return os.path.realpath(self.path)

    @property
    def dirname(self):
        """Property returns dirname of file"""
        return os.path.dirname(self.abs_path)

    @property
    def basename(self):
        """Property returns basename of file"""
        return os.path.basename(self.abs_path)

    @property
    def exists(self):
        """Property returns if file exists"""
        return os.path.isfile(self.abs_path)

    @property
    def is_open(self):
        """Property returns if file is open (i.e. if file_obj is not null)"""
        return bool(self.file_obj)

    def makedirs(self):
        """Recursively makes directories leading to file path"""
        os.makedirs(self.dirname, exist_ok=True)

    def initialise(self):
        """Method run to create file if it doesn't already exist. Writes file header"""
        if self.exists or self.is_open: return
        self.makedirs()
        self.open(mode='w+')
        if self.header: self.file_obj.write(self.header + '\n')
        self.close()

    def open(self, mode='a'):
        """Method used to open file_obj"""
        if self.is_open: return
        self.file_obj = open(self.abs_path, mode)

    def close(self):
        """Method closes the file and saves"""
        if not self.is_open: return
        self.file_obj.close()
        self.file_obj = None

    @property
    def file(self):
        """Property initialises file if it doesn't exist, opens the file if it's not open, then returns the file object"""
        self.initialise()
        if not self.is_open: self.open()
        return self.file_obj

    def append(self, data):
        """Method appends supplied line to file"""
        self.file.write(data + '\n')
        self.close()

    def delete(self):
        """Method deletes the file"""
        if not self.exists: return
        if self.is_open: self.close()
        os.remove(self.abs_path)

    @property
    def content(self):
        """Property returns the raw content of the file"""
        self.close()
        self.open(mode='r')
        content = self.file.read()
        self.close()
        return content

    @property
    def lines(self):
        """Property returns lines of the file"""
        return [line.strip('\n') for line in self.content.split('\n') if line != '']

    @property
    def body_lines(self):
        """Property returns lines of the file excluding the header"""
        return self.lines[1:] if self.lines[0] == self.header else self.lines

    @property
    def body(self):
        """Property returns the raw content of the file excluding the header"""
        return '\n'.join(self.body_lines)
