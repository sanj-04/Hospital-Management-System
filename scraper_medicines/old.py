import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def get_medicine_name(last_page_number, label):
  url = "https://www.1mg.com/drugs-all-medicines?page=1&label=a"
  response = requests.get(url)
  if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    soup.prettify()
    # with open('content.html', 'w') as file:
    #   file.write(str(response.content))

    # span_list = soup.find_all(
    #   "p", attrs={
    #     "class": "Card__productDescription__kL6Ho"
    #   }
    # )
    p_list = soup.findAll(
      name="p",
      attrs={
        "class": "Card__productName__qw2CE bodyMedium"
      }
    )

    medicines = []
    for index, ele in enumerate(p_list):
      medicines.append({
        "model": "dataStorage.medicine",
        "pk": index+1,
        "fields": {
          "medicine_name": ele.text,
          "is_active": True,
          "createTimestamp": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
          "updateTimestamp": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        }
      })

    # for ele in span_list[:5]:
    # for ele in p_list[:5]:
    #   print(f"{ele=}")

  with open("medicines_.json", "w") as json_file:
    json.dump(medicines, json_file, indent=4)