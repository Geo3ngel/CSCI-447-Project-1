import processData

print("Starting...")
db = processData.process_database_file("databases/breast-cancer-wisconsin/wdbc.data")
db.to_string()
print("Finished.")