from datetime import datetime


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



