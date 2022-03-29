from datetime import datetime
import sys, os

from csvfile import CSVFile
from file import File

class Database:
  """Database object for managing a dynamic collection of CSVFiles"""
  def __init__(self, headers, path='data/', max_age_seconds=259200):
    """Constructor:\n - Database(headers, path='data/', max_age_seconds=259200)\n\theaders: headers for CSV Files (i.e. first row, or labels)\n\tpath (optional): path of directory where files are stored\n\tmax_age_seconds: max age of files; when clean() is called all files in the directory older than this age will be deleted. Default 3 days."""
    self.rel_path = path
    self.max_age_seconds = max_age_seconds
    self.headers = headers

  def get_filename(self, date_obj):
    """Returns the filename of the file for the supplied datetime object"""
    return date_obj.strftime('weather_data_%d-%m-%Y.csv')

  def get_filename_simple(self, utctimestamp):
    """Returns the filename of the file for the supplied UTC time stamp"""
    date_obj = datetime.utcfromtimestamp(utctimestamp)
    return self.get_filename(date_obj)

  @property
  def cur_time(self):
    """Returns the current UTC time as a datetime object"""
    return datetime.utcnow()
  
  @property
  def current_filename(self):
    """Returns the filename of the current file based of the current day"""
    return self.get_filename(self.cur_time)

  def get_filepath(self, filename):
    """Returns the absolute filepath of a file from it's filename"""
    return os.path.join(self.data_dir, filename)

  @property
  def current_filepath(self):
    """Returns the absolute filepath of the current file"""
    return self.get_filepath(self.current_filename)

  @property
  def data_dir(self):
    """Returns the absoulte path of the working directory where data is stored"""
    return os.path.join(sys.path[0], self.rel_path)

  @property
  def current_file(self):
    """Returns a CSVFile object of the current file"""
    return CSVFile(self.current_filepath, self.headers)

  @property
  def files(self):
    """Returns an array of File objects of all files in the data directory"""
    return [File(self.get_filepath(path)) for path in os.listdir(self.data_dir)]

  def clean(self):
    """Deletes all files older than max_age_seconds. Returns number of files deleted."""
    return len([file.delete() for file in self.files if file.age_seconds > self.max_age_seconds])

  def insert(self, *values):
    """Inserts supplied values into current file"""
    self.current_file.insert(*values)

  @property
  def content(self, key_delimiter='`', file_delimiter='¬'):
    """Returns content of all files in database. 2 tabs between file name and content, 4 tabs between files"""
    files = {file.basename: file.content for file in self.files}
    return file_delimiter.join([key_delimiter.join(pair) for pair in files.items()])
