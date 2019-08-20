import os
import phonenumbers
from phonenumbers import geocoder
import re
import io
import sys
import pytest
import json
import pdb
# use for debugging
# pdb.set_trace()

def func(x):
  return x + 1

def cleanNumber(strs):
  return''.join(x for x in strs if x.isdigit())

def test_answer():
  assert func(3) == 4

def get_testFilePath(name):
  test_dir = os.path.dirname(os.path.abspath(__file__))
  datafile = os.path.join(test_dir,'{}'.format(name))
  return datafile

def test_openRelative():
  test_dir = os.path.dirname(os.path.abspath(__file__))
  datafile = os.path.join(test_dir,'datafile_test.txt')
  assert datafile == get_testFilePath('datafile_test.txt')

def test_fileNotEmpty():
  with open(get_testFilePath('datafile_test.txt'), 'r') as reader:
    if reader.readlines() != []:
      assert True

def test_testingCustomStream():
  stream = io.StringIO("some initial text data")
  streamMulti = io.StringIO("""some initial text data
  some initial text data2
  some initial text data3
  some initial text data4""")
  assert isinstance(stream.readline(), str)
  assert isinstance(streamMulti.readline(), str)


def test_phoneCleanup():
  strs = 'dsds +48 124 cat cat cat245 81243!!'
  newString = cleanNumber(strs)
  assert newString.isdigit()

def test_getPhoneNumbers():
  reader = io.StringIO("""History trip always room. c369e42170409b5a250f5ec8a86fa5bf +61353386215
   +447733795449 Bag show white artist town message field catch. 6d:a6:0f:0b:94:17
   Continue address throw difference discover. 43,221,224 +40756809984
   Continue address throw difference discover. 43,221,224 +40756809984""")
  for line in reader.readlines():
    # get numbers from line
    # "+" character REQUIRED for regex
    m = re.search(r"\+[\d]+", line)
    # check for uniqueness by removing non-number characters
    number = cleanNumber(m.group(0))
    assert m.group(0).isdigit() == False
    assert number.isdigit()

def test_countNumbers():
  reader = io.StringIO("""History trip always room. c369e42170409b5a250f5ec8a86fa5bf +61353386215
   +447733795449 Bag show white artist town message field catch. 6d:a6:0f:0b:94:17
   Continue address throw difference discover. 43,221,224 +40756809984
   Continue address throw difference discover. 43,221,224 +40756809984""")
  uniqueNumbers = []
  # key : value is number: count of repetitions per stream
  uniqueNumbersCount = {}
  finalNumberCount = {'61353386215': 1, '447733795449': 1, '40756809984': 2}
  for line in reader.readlines():
    m = re.search(r"\+[\d]+", line)
    number = cleanNumber(m.group(0))
    # show unique numbers and their count for the stream
    if number in uniqueNumbersCount.keys():
      uniqueNumbersCount[number] += 1
    else:
      uniqueNumbersCount[number] = 1
      uniqueNumbers.append(number)
  assert uniqueNumbersCount == finalNumberCount

def test_getCountryTest():
  ch_number = phonenumbers.parse("+447733795449", "US")
  # requires E164 format
  # E.164 numbers are formatted [+] [country code] [subscriber number including area code] and can have a maximum of fifteen digits
  # @see https://www.twilio.com/docs/glossary/what-e164
  geo = geocoder.description_for_number(ch_number, "en")
  assert geo ==  "United Kingdom"

@pytest.mark.skipif(sys.version_info < (3, 6), reason="requires python3.6 or higher")
def test_getMaxFromDic():
  stats = {'a':1000, 'b':3000, 'c': 100}
  maxKey = max(stats.keys(), key=(lambda k: stats[k]))
  print(maxKey)
  assert maxKey == "b"

def test_getMaxFromDicTwo():
  dic={0: 1.4984074067880424, 1: 1.0984074067880423, 2: 1.8984074067880425, 3: 2.2984074067880425, 4: 2.2984074067880425}
  max_value = max(dic.values())  # maximum value
  max_keys = [k for k, v in dic.items() if v == max_value] # getting all keys containing the `maximum`

  print(max_value, max_keys)
  assert max_value == dic[3]
  assert max_keys == [3,4]

def test_getMaxFromDicThree():
  mydict = {'A':4,'B':10,'C':0,'D':87}
  maximum = max(mydict, key=mydict.get)  # Just use 'min' instead of 'max' for minimum.
  print(maximum, mydict[maximum])
  # D 87
  assert maximum == 'D'
  assert mydict[maximum] == 87

def test_checkLineWithoutNumber():
  reader = io.StringIO("""History trip always room. c369e42170409b5a250f5ec8a86fa5bf +61353386215
   +447733795449 Bag show white artist town message field catch. 6d:a6:0f:0b:94:17
   Continue address throw difference discover. 43,221,224 +40756809984
   Continue address throw difference discover. 43,221,224 +40756809984
   Davidside, NY 84689""")
  for line in reader.readlines():
    m = re.search(r"\+[\d]+", line)
    if m != None:
      number = cleanNumber(m.group(0))
      assert m != None
      assert isinstance(number, str)

@pytest.mark.skip(reason="used only to test json output to file")
def test_jsonOutput():
  appDict = {
    'name': 'messenger',
    'playstore': True,
    'company': 'Facebook',
    'price': 100
  }
  app_json = json.dumps(appDict)
  with open(get_testFilePath('tests_results.json'), 'w') as json_file:
    json.dump(appDict, json_file)
  assert app_json

# @pytest.mark.skip(reason="waiting on test_countNumbers")
def test_getCountryMax():
  countryCount = {}
  countryWithMaxCount = None
  finalDic = {}
  reader = io.StringIO("""History trip always room. c369e42170409b5a250f5ec8a86fa5bf +61353386215
   +447733795449 Bag show white artist town message field catch. 6d:a6:0f:0b:94:17
   Continue address throw difference discover. 43,221,224 +40756809984
   Continue address throw difference discover. 43,221,224 +40756809984
   Davidside, NY 84689
   +61786844803 
   +61211549558 
   +61303024775""")
  for line in reader.readlines():
    m = re.search(r"\+[\d]+", line)
    if m != None:
      ch_number = phonenumbers.parse(m.group(0), "US")
      country = geocoder.description_for_number(ch_number, "en")
      print(country == "")
      if country in countryCount.keys():
        countryCount[country] += 1
      elif country == "":
        countryCount["notfound in {}".format(m.group(0))] = 1
      else:
        countryCount[country] = 1
  countryWithMaxCount = max(countryCount, key=countryCount.get)
  assert countryWithMaxCount == "Australia"
  assert countryCount[countryWithMaxCount] == 3

# @pytest.mark.skip(reason="waiting on test_countNumbers")
def test_getDataFromTestFile():
  uniqueNumbers = []
  uniqueNumbersCount = {}
  countryCount = {}
  countryWithMaxCount = None
  finalDic = {}
  with open(get_testFilePath('datafile.txt'), 'r') as reader:
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
  with open(get_testFilePath('tests_results.json'), 'w') as json_file:
    json.dump(finalDic, json_file)

  assert countryWithMaxCount == "Australia"
  assert countryCount[countryWithMaxCount] == 14210