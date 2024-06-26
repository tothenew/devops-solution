def accessKeyCheckHandler(event, context):
    print("inside accessKeychcekHandler")
    if 'detail' in event:
        print("inside detail")
        event_details = []
        detail={
			'KeyDeletedFor': event['detail']['requestParameters']['userName']
		}
        event_details.append(detail)
        
        return event_details