
def cloudtrail(event,context):
	event_details = []
	detail={
			'SourceIPAddress': event['detail']["sourceIPAddress"],
			'ResourceName': event['detail']['requestParameters']['name']
		}
	event_details.append(detail)
	return event_details
