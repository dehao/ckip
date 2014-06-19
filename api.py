import urllib2
import csv
import json
url = "http://api.ly.g0v.tw/v0/collections/bills?l=38&sk=2&q={%22proposed_by%22:{%22$matches%22:%22%E4%BA%BA%22}}"
response = urllib2.urlopen(url);
data = json.loads(response.read())
jsondata = data["entries"]
jsonData = jsondata.encode('utf8')
print jsonData

f = csv.writer(open("api.csv", "wb+"))
f.writerow(["abstract", "proposed_by", "summary", "bill_id"])

for item in jsonData:
    f.writerow(item.get("abstract"))