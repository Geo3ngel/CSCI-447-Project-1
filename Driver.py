import processData

print("Starting...")
db = processData.process_database_file("databases/soybean/soybean-small.data")
# db.to_string()
processData.data_correction(db.get_data(), 36)
print("Finished.")