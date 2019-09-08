from csv_operation import  CSVOperation
from natural_gas_spot_price import NaturalGasSpotPrice

scrap_data = NaturalGasSpotPrice('daily') #monthly/daily get report accordingly
data = scrap_data.get_data()
csv_obj = CSVOperation('daily1.csv', ['date', 'price'])
csv_obj.write(data)
