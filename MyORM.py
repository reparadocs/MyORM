import sqlite3
import inspect

class MyORM:
  def __init__(self, name):
    self.name = name
    self.conn = sqlite3.connect(name + '.db')
    self.cursor = self.conn.cursor()

  def execute(self, statement):
    self.cursor.execute(statement)
    self.conn.commit()

  def _valToStr(self, val):
    if type(val) is str:
      return "'" + val + "'"
    else:
      return str(val)

  def createTable(self, model):
    statement = 'CREATE TABLE '
    statement += model.__name__ + ' ( '
    statement += 'ROWID INTEGER NOT NULL, '
    for name, field in model.__dict__.items():
      if field is None or isinstance(field, Field) == False:
        continue
      statement += name + ' ' + field.syntax
      if not field.null:
        statement += ' NOT NULL'
      if field.unique:
        statement += ' UNIQUE'
      if field.default is not None:
        statement += ' DEFAULT ' + str(field.default)
      statement += ', '
    statement += 'PRIMARY KEY(ROWID));'
    print statement
    self.execute(statement)

  def dropTable(self, model):
    statement = 'DROP TABLE ' + model.__name__ + ';'
    self.execute(statement)

  def _insert(self, item):
    statement = 'INSERT INTO ' + item.__class__.__name__
    fields = ''
    vals = ''
    for name, field in item.__class__.__dict__.items():
        if field is None or isinstance(field, Field) == False:
          continue
        value = item.__dict__[name]
        fields += name + ', '
        vals += self._valToStr(value) + ', '
    fields = fields[:-2]
    vals = vals[:-2]
    statement += ' (' + fields + ') VALUES (' + vals + ');'
    print statement
    self.execute(statement)
    return self.cursor.lastrowid

  def insert(self, item):
    if type(item) is list or type(item) is tuple:
      for i in item:
        i.rowid = self._insert(item)
    else:
      item.rowid = self._insert(item)
    return item

  def _delete(self, item):
    statement = 'DELETE FROM '
    if item.rowid is None:
      raise ValueError("Item not initialized")
    statement += item.__class__.__name__ + ' WHERE ROWID = ' + item.rowid + ';'
    self.execute(statement)
    return None

  def delete(self, item, **kwargs):
    if type(item) is list or type(item) is tuple:
      for i in item:
        i.rowid = self._delete(i)
    elif inspect.isclass(item):
      statement = 'DELETE FROM ' + item.__name__ + ' WHERE '
      for k, v in kwargs.items():
        statement += k + ' = ' + self._valToStr(v) + ' AND '
      statement = statement[:-4] + ';'
      self.execute(statement)
    else:
      item.rowid = self._delete(item)
    return item

  def _update(self, item):
    statement = 'UPDATE '
    if item.rowid is None:
      raise ValueError("Item not initialized")
    statement += item.__class__.__.name__ + ' SET '
    for name, field in item.__dict__.items():
      if field is None or not isinstance(field, Field):
        continue
      value = item.__dict__[name]
      statement += name + ' = ' + self._valToStr(value) + ', '
    statement = statement[:-2] + ' WHERE ROWID = ' + item.rowid + ';'
    self.execute(statement)
    return item.rowid

  def update(self, item):
    statement = 'UPDATE '
    if type(item) is list or type(item) is tuple:
      for i in item:
        i.rowid = self._update(i)
    else:
      item.rowid = self._update(i)
    return item

  def getAll(self, model):
    statement = 'SELECT * FROM ' + model.__name__ + ' ;'
    self.execute(statement)
    res = self.cursor.fetchall()
    models = []
    for r in res:
      models.append(model(list(r)))
    return models

  def filter(self, model, condition):
    statement = 'SELECT * FROM ' + model.__name__ + ' WHERE ' + condition + ';'
    self.execute(statement)
    res = self.cursor.fetchall()
    models = []
    for r in res:
      models.append(model(list(r)))
    return models

class Model(object):
  rowid = None
  def __init__(self, *args, **kwargs):
    for k, v in kwargs.items():
      setattr(self, k, v)

class Field(object):
  syntax = 'unset'

  def __init__(self, null=True, unique=False, default=None):
    self.null = null
    self.unique = unique
    self.default = default

class IntegerField(Field):
  def __init__(self, null=True, unique=False, default=None):
    self.syntax = 'INT'
    super(IntegerField, self).__init__(null, unique, default)

class CharField(Field):
  def __init__(self, maxChars, null=True, unique=False, default=None):
    self.syntax = 'VARCHAR(' + str(maxChars) + ')'
    super(CharField, self).__init__(null, unique, default)

class BooleanField(Field):
  def __init__(self, null=True, unique=False, default=None):
    self.syntax = 'BOOLEAN'
    super(CharField, self).__init__(null, unique, default)

class FloatField(Field):
  def __init__(self, null=True, unique=False, default=None):
    self.syntax = 'FLOAT'
    super(IntegerField, self).__init__(null, unique, default)

class ForeignKeyField(Field):
  def __init__(self, references, null=True, unique=False, default=None):
    self.syntax = 'INT REFERENCES ' + references.__name__ + '(ROWID)'
    super(ForeignKeyField, self).__init__(null, unique, default)

class DateField(Field):
  def __init__(self, null=True, unique=False, default=None):
    self.syntax = 'DATE'
    super(IntegerField, self).__init__(null, unique, default)