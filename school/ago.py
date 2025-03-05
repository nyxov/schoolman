import yottadb
from yottadb import YDBError

try:
    gaga = yottadb.get(varname="^kino")
    print(type(gaga))
except YDBError:
    print("Generic case: handle any error issued by YottaDB")




try:
    yottadb.node_next(varname="^myglobal", subsarray=("sub1", "sub2"))
except YDBNodeEnd:
    print("Specific case: handle YDB_ERR_NODEEND differently")

try:
    yottadb.Key("^\x80").data
except YDBError as e:
    if yottadb.YDB_ERR_INVVARNAME == e.code():
        print("Invalid variable name")
    else:
        print("Unexpected error")