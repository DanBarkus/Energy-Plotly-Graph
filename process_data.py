import os
import csv

raw_data_folder = 'raw_data'
process_data_folder = 'processed_data'

weather_rows_to_keep = ['STATION','DATE','HourlyDryBulbTemperature','HourlyPrecipitation','HourlyRelativeHumidity','HourlyWindSpeed']

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

for weather_file in os.listdir(raw_data_folder):
    if weather_file.endswith('Weather.csv'):
        print(weather_file)
        output_list = []
        with open(os.path.join(raw_data_folder, weather_file), 'r') as w_file:
            weather_list = csv.DictReader(w_file)
            for event in weather_list:
                if event['REPORT_TYPE'].startswith('FM') and is_number(event['HourlyDryBulbTemperature']):
                    evt = {}
                    for row in weather_rows_to_keep:
                        if row == "HourlyPrecipitation":
                            if not is_number(event[row]):
                                event[row] = float(0.00)
                        evt[row] = event[row]
                    evt['STATION'] = weather_file.split('_')[0]
                    evt["DATE"] = evt["DATE"].replace('T', ' ')
                    evt['DATE'] = evt['DATE'].replace('-', '/')
                    output_list.append(evt)
        with open(os.path.join(process_data_folder, weather_file), 'w+') as out_file:
            headers = output_list[0].keys()
            writer = csv.DictWriter(out_file, headers)
            writer.writeheader()
            for row in output_list:
                writer.writerow(row)
