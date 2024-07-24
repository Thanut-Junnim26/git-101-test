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