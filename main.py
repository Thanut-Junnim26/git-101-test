from typing import List
from datetime import datetime
import boto3
import json


CLIENT = boto3.client('ce')

def result_cost(month: tuple):
    
    result = CLIENT.get_cost_and_usage(
        TimePeriod = {
            'Start': f"{month[0]}",
            'End': f"{month[1]}"
        },
        Granularity = 'MONTHLY',
        # Filter = {
        #     "And": [{
        #         "Dimensions": {
        #             "Key": "SERVICE",
        #             "Values": ["Amplify"]
        #         }
        #     }, {
        #         "Not": {
        #             "Dimensions": {
        #                 "Key": "RECORD_TYPE",
        #                 "Values": ["Credit", "Refun40
        #             }
        #         }
        #     }, 
        #     ]
        # },
        Metrics = ["UnblendedCost"],
        GroupBy = [
            {
                'Type': 'DIMENSION',
                'Key': 'SERVICE'
            },
            # {
            #     'Type': 'DIMENSION',
            #     'Key': 'USAGE_TYPE'
            # }
        ]
    )

    return result

def get_costs(result: dict, start_date: str, end_date: str, granularity: str) -> dict:
    costs = {}

    if granularity == 'm':
        granularity = 'Monthly'
    else:
        granularity = 'Daily'

    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")


    for period in result['ResultsByTime']:
        period_start_date = datetime.strptime(period['TimePeriod']['Start'], "%Y-%m-%d")
        period_end_date = datetime.strptime(period['TimePeriod']['End'], "%Y-%m-%d")


        if period_start_date >= start_date and period_end_date <= end_date:
            total_cost = 0.0
            service_costs = {}

            for group in period['Groups']:
                service_name = group['Keys'][0].replace('AWS', '').strip()
                amount = float(group['Metrics']['UnblendedCost']['Amount'])
                total_cost += amount
                service_costs[service_name] = f'{amount:.2f} USD'

            costs[f"{period['TimePeriod']['Start']} to {period['TimePeriod']['End']}"] = {
                'Total': f'{total_cost:.2f} USD',
                'Services': service_costs
            }

    return costs

def get_cost_each_month(months: list, year: int) -> List[tuple]:
    import calendar
    
    lst = []
    for month in range(months[0], months[1]+1):
        month: int
        
        day_end = calendar.monthrange(year, month) # weekly of month = assume (4, 31)
        first_date = f"{year}-{str(month).zfill(2)}-01"
        end_date = f"{year}-{str(month).zfill(2)}-{day_end[1]}"
        
        lst.append((first_date, end_date))
    print(lst)
    return lst
    

def lambda_handler(event, context):
    months: list = [1, 12]
    year: int = datetime.today().year
    
    lst_of_month = get_cost_each_month(months=months, year=year)
    # lst_of_month = [('2024-08-01', '2024-08-31'), ('2024-09-01', '2024-09-30'), ('2024-10-01', '2024-10-31'), ('2024-11-01', '2024-11-30'), ('2024-12-01', '2024-12-31')]  

    for month in lst_of_month:
        # month = ('2024-08-01', '2024-08-31')
        # month[0] = '2024-08-01'
        try:
            result = result_cost(month=month)
            
            print("get reslut of cost")
            
            # print("get_costs(result=result, start_date=f"{month[0]}", end_date=f"{month[1]}", granularity="MONTHLY")")
            print('-'*100)
        except Exception as e:
            print(f"this error {e}")

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
        }
    


# --> input = year, month
#  --> output = ('2024-02-01', '2024-02-29')

# --> input = year, month
# --> output = function

