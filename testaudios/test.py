from os import listdir
from os.path import isfile, join
import requests
import time

folder = './male_age20_german/noisy/ohne_stops'

onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]

def transcribe():
    for file in onlyfiles:
        filename = folder + '/' + file
        with open(filename, 'rb') as f:
            start = time.time_ns()
            r = requests.post('http://127.0.0.1:1222/', files={'file': f})
            print("Status Code:", r.status_code)
            print("Response Headers:", r.headers)
            print("Response Content:", r.text)
            try:
                response_json = r.json()
                end = time.time_ns()
                print("--------------------")
                print("Question:", file)
                print("Answer:", response_json.get('answer', 'N/A'))
                print("Time:", str(end - start))
            except ValueError:
                print("Received non-JSON response.")
                continue
            

transcribe()

#tiny: 0.3 sekunden