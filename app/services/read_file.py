import phonenumbers
from phonenumbers import geocoder
import json
import re

def cleanNumber(strs):
  return''.join(x for x in strs if x.isdigit())

def getDataFromTestFile(fname):
  uniqueNumbers = []
  uniqueNumbersCount = {}
  countryCount = {}
  countryWithMaxCount = None
  finalDic = {}
  # with open('datafile_test.txt', 'r') as reader:
  with open(fname, 'r') as reader:
    for line in reader.readlines():
      m = re.search(r"\+[\d]+", line)
      if m != None:
        number = cleanNumber(m.group(0))
        if number in uniqueNumbersCount.keys():
          uniqueNumbersCount[number]["count"] += 1
        else:
          uniqueNumbersCount[number] = {}
          uniqueNumbersCount[number]["count"] = 1
          uniqueNumbers.append(number)
        # count countries 
        ch_number = phonenumbers.parse(m.group(0), "US")
        country = geocoder.description_for_number(ch_number, "en")
        uniqueNumbersCount[number]["country"] = country
        if country in countryCount.keys():
          countryCount[country] += 1
        elif country == "":
          countryCount["notfound in {}".format(m.group(0))] = 1
        else:
          countryCount[country] = 1
  countryWithMaxCount = max(countryCount, key=countryCount.get)
  finalDic = {
    "all_unique_numbers": uniqueNumbers,
    "phone_count": uniqueNumbersCount,
    "country_count": countryCount,
    "country_with_max_count": countryWithMaxCount
  }
  return json.dumps(finalDic)