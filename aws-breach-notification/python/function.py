def evaluate(event,context):
    if  isinstance(event['detail']['requestParameters'],dict) and event['detail']["requestParameters"]["functionName"] == context.invoked_function_arn:
        event_details = []
        detail={
                'functionName': context.function_name
            }
        event_details.append(detail)
        return event_details