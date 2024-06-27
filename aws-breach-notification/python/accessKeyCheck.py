
def accessKeyCheckHandler(event, context):
    if 'detail' in event:
        event_details = []
        detail={
			'KeyGeneratedFor': event['detail']['responseElements']['accessKey']['userName']
		}
        event_details.append(detail)
        return event_details