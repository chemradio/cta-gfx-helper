from shared.database.db import DBHandler    

def test_db_handler():
    DBHandler.drop()
    DBHandler.insert({"order_id": "1", "status": "pending"})
    print(DBHandler.all())
    print(DBHandler.get_order(order_id="1"))
    DBHandler.update("1", {"status": "completed"})
    print(DBHandler.get_order(order_id="1"))
    DBHandler.delete("1")
    print(DBHandler.all())

    DBHandler.insert({"order_id": "1", "status": "pending"})
    DBHandler.insert({"order_id": "2", "status": "pending"})
    DBHandler.insert({"order_id": "3", "status": "pending"})
    DBHandler.insert({"order_id": "4", "status": "pending"})

    print(DBHandler.get_oldest_new_order())