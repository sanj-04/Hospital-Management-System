import requests
from bs4 import BeautifulSoup
import json
import sys
from datetime import datetime
data = {
  "a": 334, "b": 334, "c": 334, "d": 334, "e": 334, "f": 334, "g": 334, "h": 166, "i": 242,
  "j": 74, "k": 217, "l": 334, "m": 334, "n": 334, "o": 334, "p": 334, "q": 52, "r": 334, "s": 334,
  "t": 334, "u": 125, "v": 334, "w": 99, "x": 79, "y": 28, "z": 313,
}
medicines = []

def get_medicine_name(last_page_number, label, total_count):
  count = total_count
  for page in range(1, last_page_number+1):
    url = f"https://www.1mg.com/drugs-all-medicines?page={page}&label={label}"
    response = requests.get(url)
    if response.status_code == 200:
      soup = BeautifulSoup(response.content, "html.parser")
      soup.prettify()
      p_list = soup.findAll(
        name="p",
        attrs={
          "class": "Card__productName__qw2CE bodyMedium"
        }
      )
      for index, ele in enumerate(p_list, start=1):
        medicines.append({
          "model": "dataStorage.medicine",
          "pk": index+count,
          "fields": {
            "medicine_name": ele.text,
            "is_active": True,
            "createTimestamp": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "updateTimestamp": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
          }
        })
      count+=len(p_list)
    print(f"{page=}, {label=}, {count=}")
  return count

# get_medicine_name(int(sys.argv[1]), str(sys.argv[2]))
total_count = 0
for key in data.keys():
  # print(f"{key=}, {data[key]=}")
  medicines = []
  total_count = get_medicine_name(int(data[key]), str(key), total_count)
  # with open(f"medicines_{str(sys.argv[2])}.json", "w") as json_file:
  with open(f"medicines_{str(key)}_{str(data[key])}.json", "w") as json_file:
    json.dump(medicines, json_file, indent=4)