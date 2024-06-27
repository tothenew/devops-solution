
def PutBucketPublicAccessBlock(event,context):
	event_details = []
	if event['detail']['eventName'] == 'PutBucketAcl':
		if 'x-amz-acl' in event['detail']['requestParameters'].keys() and set.intersection(set(event['detail']['requestParameters']['x-amz-acl']), set(['public-read', 'public-read-write'])):
			detail={
					'SourceIPAddress': event['detail']["sourceIPAddress"],
					'ResourceName': event['detail']['requestParameters']['bucketName']
				}
			event_details.append(detail)
			return event_details
		else:
			return False

	elif event['detail']['eventName'] == 'PutBucketPublicAccessBlock':	
		RestrictPublicBuckets=event['detail']['requestParameters']['PublicAccessBlockConfiguration']['RestrictPublicBuckets']
		BlockPublicPolicy=event['detail']['requestParameters']['PublicAccessBlockConfiguration']['BlockPublicPolicy']
		BlockPublicAcls=event['detail']['requestParameters']['PublicAccessBlockConfiguration']['BlockPublicAcls']
		IgnorePublicAcls=event['detail']['requestParameters']['PublicAccessBlockConfiguration']['IgnorePublicAcls']
		if not RestrictPublicBuckets or not BlockPublicPolicy or not BlockPublicAcls or not IgnorePublicAcls :
			detail={
				'SourceIPAddress': event['detail']["sourceIPAddress"],
				'ResourceName': event['detail']['requestParameters']['bucketName']
			}
			event_details.append(detail)
			return event_details