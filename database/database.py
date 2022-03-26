from datetime import datetime
import sys, os

class Database:
  def __init__(self, path='data/', use_headers=True, max_age_seconds=259200):
    self.rel_path = path
    self.use_headers = use_headers
    self.max_age_seconds = max_age_seconds

  @property
  def cur_time(self):
    return datetime.utcnow()
  
  @property
  def filename(self):
    return self.cur_time.strftime('weather_data_%d-%m-%Y.csv')

  @property
  def filepath(self):
    return os.path.join(self.abs_path, self.filename)

  @property
  def working_dir(self):
    return sys.path[0]

  @property
  def abs_path(self):
    return os.path.join(self.working_dir, self.rel_path)
