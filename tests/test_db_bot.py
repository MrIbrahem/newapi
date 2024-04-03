
import os
from datetime import datetime
from newapi.db_bot import LiteDB


def test():
    db_path = "/data/mdwiki/public_html/ncc/Tables/nc_files.db"
    if not os.path.exists(db_path):
        db_path = "I:/mdwiki/pybot/ncc_core/nc_import/bots/nc_files.db"

    nc_files_db = LiteDB(db_path)

    nc_files_db.create_table(
        "nc_files",
        {"id": int, "lang": str, "title": str, "views": int, "dat": str},
        pk="id",
        defaults={"views": 0},
    )

    nc_files_db.show_tables()

    # Insert sample data
    nc_files_db.insert(
        "nc_files",
        {
            "lang": "English",
            "title": "Sample Title 1",
            # "views": 100,
            "dat": datetime.now().strftime("%Y-%m-%d"),
        },
    )

    nc_files_db.insert(
        "nc_files",
        {
            "lang": "French",
            "title": "Sample Title 2",
            # "views": 200,
            "dat": datetime.now().strftime("%Y-%m-%d"),
        },
    )

    # Retrieve data
    data = nc_files_db.get_data("nc_files")
    for row in data:
        print(row)


def test2():
    db_path = "/data/mdwiki/public_html/ncc/Tables/nc_files.db"
    if not os.path.exists(db_path):
        db_path = "I:/mdwiki/pybot/ncc_core/nc_import/bots/nc_files.db"

    nc_files_db = LiteDB(db_path)

    print("________")
    # Select data
    # data = nc_files_db.select("nc_files", {"lang": "English"})
    # print(data)
    # for row in data:
    #     print(row)

    # Retrieve data
    data = nc_files_db.get_data("nc_files")
    for row in data:
        print(row)


if __name__ == "__main__":
    test()
    test2()
