import requests 
from bs4 import BeautifulSoup 
from datetime import datetime, timedelta
from csv_operation import  CSVOperation
MONTH = {
    'Jan':1,
    'Feb':2,
    'Mar':3,
    'Apr':4,
    'May':5,
    'Jun':6,
    'Jul':7,
    'Aug':8,
    'Sep':9,
    'Oct':10,
    'Nov':11,
    'Dec':12,
}

BASE_URL = "https://www.eia.gov/dnav/ng/hist/"
DURATION = {
    'daily': {   'page':'rngwhhdD.htm',
                 'sibling':0
                },
    'monthly':  {   'page':'rngwhhdM.htm',
                    'sibling':1
                }
}

class NaturalGasSpotPrice():
    def __init__(self, Duration):
        if Duration not in ['monthly', 'daily']:
            print("Duration either monthly or daily")
        page = DURATION[Duration]['page']
        self.duration = Duration
        self.url = BASE_URL+"{duration}".format(duration=page)
        self.sibling = DURATION[Duration]['sibling']
    
    def process_date(self, data):
        data = data.strip().replace(" ","")
        if data:
            self.year = data[:4]
            range_list = data[4:].split('to')
            month_date = range_list[0].split('-')
            month = MONTH[month_date[0]]
            date = month_date[1]
            return "{year}-{month}-{date}".format(date=date, month=month, year=self.year)

    def get_next_date(self, date_str):
        if date_str:
            datetime_object = datetime.strptime(date_str,'%Y-%m-%d')
            next_date = datetime_object + timedelta(days=1)
            return str(next_date.date())

    def process_year(self, data):
        if data:
            return data.strip()

    def get_data(self):
        r = requests.get(self.url) 
        data = BeautifulSoup(r.content, 'html5lib') 
        table = data.find('table', attrs = {'summary':'Henry Hub Natural Gas Spot Price (Dollars per Million Btu)'}) 
        if self.sibling:
            table = table.nextSibling
        list_data = []
        for row in table.findAll('tr'):
            begin=1
            date = None
            month = 1
            year = None
            for val in row.findAll('td'):
                # print(val.text)
                if self.duration == 'daily':
                    if begin:
                        date = self.process_date(val.text)
                    else:
                        if not date:
                            continue
                        list_data.append({'date':date,'price': val.text})
                        date = self.get_next_date(date)
                else:
                    if begin:
                        year = self.process_year(val.text)
                    else:
                        date = "{year}-{month}-01".format(year=year,month=month) 
                        list_data.append({'date':date,'price': val.text})
                        month += 1
                begin=0
        return list_data

scrap_data = NaturalGasSpotPrice('monthly')
data = scrap_data.get_data()
csv_obj = CSVOperation('monthly1.csv', ['date', 'price'])
csv_obj.write(data)
