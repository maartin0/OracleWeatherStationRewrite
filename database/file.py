import os

class File:
    def __init__(self, path, header=''):
        self.path = path
        self.header = header
        self.file_obj = None

    @property
    def abs_path(self):
        return os.path.realpath(self.path)

    @property
    def dirname(self):
        return os.path.dirname(self.abs_path)

    @property
    def basename(self):
        return os.path.basename(self.abs_path)

    @property
    def exists(self):
        return os.path.isfile(self.abs_path)

    @property
    def is_open(self):
        return bool(self.file_obj)

    def makedirs(self):
        os.makedirs(self.dirname, exist_ok=True)

    def initialise(self):
        if self.exists or self.is_open: return
        self.makedirs()
        self.open(mode='w+')
        if self.header: self.file_obj.write(self.header + '\n')
        self.close()

    def open(self, mode='a'):
        if self.is_open: return
        self.file_obj = open(self.abs_path, mode)

    def close(self):
        if not self.is_open: return
        self.file_obj.close()
        self.file_obj = None

    @property
    def file(self):
        self.initialise()
        if not self.is_open: self.open()
        return self.file_obj

    def append(self, data):
        self.file.write(data + '\n')
        self.close()

    def delete(self):
        if not self.exists: return
        if self.is_open: self.close()
        os.remove(self.abs_path)

    @property
    def content(self):
        self.close()
        self.open(mode='r')
        content = self.file.read()
        self.close()
        return content

    @property
    def lines(self):
        return [line.strip('\n') for line in self.content.split('\n') if line != '']

    @property
    def body_lines(self):
        return self.lines[1:] if self.lines[0] == self.header else self.lines

    @property
    def body(self):
        return '\n'.join(self.body_lines)
