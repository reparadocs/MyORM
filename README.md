To import:

from MyORM import *

To use:

    db = MyORM('DB_NAME_HERE')

Create a model to use in the db:

    class OBJ_NAME(Model):
      stringVar = CharField(50) /* stringVar is a variable name, 50 is the maxChars */
      intVar = IntegerField()
      boolVar = BooleanField()
      floatVar = FloatField()
      foreignVar = ForeignKeyField(ReferenceObj) /* Reference Obj is the Class you want to reference */
      dateVar = DateField()

      def __init__(self, l):
        self.rowid = l[0]
        self.stringVar = l[1]
        self.intVar = l[2]
        self.boolVar = l[3]
        self.floatVar = l[4]
        self.foreignVar = l[5]
        self.dateVar = l[6]

  /* The init method MUST BE like this, note the self.rowid = l[0] */

Fields have an optional null, unique, and default parameters:
  Null is default True
  Unique is default False
  Default is default None

    stringVar = CharField(50, null=True, unique=True, default="Hello")

    db.createTable(OBJ_NAME)

Drop a model in the db:

    db.dropTable(OBJ_NAME)

If you need to use raw SQL:

    db.execute("SQL_STATEMENT_HERE")

Creating a new object:

    testObj = OBJ_NAME([0, "Hello", 5, True, 5.0])
    db.insert(testObj)

Creating multiple objects:

    objs = []
    for i in range(5):
      objs.append(OBJ_NAME([0, "Hello", i, True, 5.0]))
    db.insert(objs)

Deleting Objects

    db.delete(testObj)

Updating Objects

    db.update(testObj)

Get all objects

    objs = db.getAll(OBJ_NAME)

Get some objects (in this example, objects with stringVar equal to "Hello")

    objs = db.filter(OBJ_NAME, 'stringVar = "Hello"')
