import csv

existing_file_path = 'temp_stocks.csv'

new_column_data = [100,200,300,400,500]

with open(existing_file_path, 'r', newline='') as file:
    reader = csv.reader(file)
    rows = list(reader)

for i, row in enumerate(rows):
    if i == 0:
        row.append('Current Price')
    else:
        row.append(new_column_data[i-1])

with open(existing_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(rows)