import fileIO

print("Starting...")
db = fileIO.process_database_file("databases/breast-cancer-wisconsin/wdbc.data")
db.to_string()
print("Finished.")