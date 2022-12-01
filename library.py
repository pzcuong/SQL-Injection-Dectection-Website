def write_csv_file(file, data):
  import csv
  with open(file, 'a', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(data)