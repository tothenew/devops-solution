import traceback
import boto3
import os
import re 
import sys
from urllib import request
sys.path.append(os.path.abspath('..'))
import config as config

def send_mail(notification):
    ses_recipient=notification._mail_ids.split(',')
    CHARSET = "UTF-8"
    secrets = config.get_secret()
    SES_SOURCE_EMAIL_ADDRESS = secrets['EMAIL_FROM']
    SES_REGION = secrets['SES_REGION']
    SES_Access_Key = secrets['ACCESS_KEY']
    SES_Secret_Key = secrets['ACCESS_SECRET_KEY']
    ses_payload = generate_ses_payload(notification)
    if notification._event_type == "info":
        ses_sub='AWS Security | '+notification._event_title+' | '
    else:
        ses_sub='AWS Security Breach | '
    ses_sub+=notification._event_name+' | '+notification._account_name+' | '+notification._account_id
    try:
        client = boto3.client('ses',region_name=SES_REGION,aws_access_key_id=SES_Access_Key,aws_secret_access_key=SES_Secret_Key)
        response = client.send_email(
            Destination={
                'ToAddresses': ses_recipient,
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': ses_payload,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': ses_sub,
                },
            },
            Source=SES_SOURCE_EMAIL_ADDRESS,
        )
        return True
    except Exception:
        traceback.print_exc()
        return False
  
def generate_ses_payload(notification):
    ses_payload = """
<html>
<head>
  <title></title>
</head>
<body>
  <table style="border-spacing:0;border-collapse:collapse;vertical-align:top;text-align:left;height:100%;width:100%;color:#222222;font-family:'Open Sans','Helvetica Neue','Helvetica',Helvetica,Arial,sans-serif;font-weight:normal;line-height:19px;font-size:14px;margin:0;padding:0" bgcolor="#f6f4f4">
    <tbody><tr style="vertical-align:top;padding:0" align="left">
      <td style="word-break:break-word;border-collapse:collapse!important;color:#222222;font-family:'Open Sans','Helvetica Neue','Helvetica',Helvetica,Arial,sans-serif;font-weight:normal;line-height:19px;font-size:14px;margin:0;padding:0" valign="top" align="center">
        <center style="width:100%;min-width:580px">
          <table style="border-spacing:0;border-collapse:collapse;vertical-align:top;text-align:left;width:100%;margin-top:25px;margin-bottom:25px;padding:0px">
            <tbody><tr style="vertical-align:top;padding:0" align="left">
              <td style="word-break:break-word;border-collapse:collapse!important;color:#222222;font-family:'Open Sans','Helvetica Neue','Helvetica',Helvetica,Arial,sans-serif;font-weight:normal;line-height:19px;font-size:14px;margin:0;padding:0" valign="top" align="center">
                <center style="width:100%;min-width:580px">

                  <table style="border-spacing:0;border-collapse:collapse;vertical-align:top;text-align:inherit;width:580px;margin:0 auto;padding:0">
                    <tbody><tr style="vertical-align:top;padding:0" align="left">
                      <td style="word-break:break-word;border-collapse:collapse!important;color:#222222;font-family:'Open Sans','Helvetica Neue','Helvetica',Helvetica,Arial,sans-serif;font-weight:normal;line-height:19px;font-size:14px;margin:0;padding:10px 0px 0px" valign="top" align="left">

                        <table style="border-spacing:0;border-collapse:collapse;vertical-align:top;text-align:left;width:580px;margin:0 auto;padding:0">
                          <tbody><tr style="vertical-align:top;padding:0" align="left">
                            <td style="word-break:break-word;border-collapse:collapse!important;min-width:0px;width:100%;color:#222222;font-family:'Open Sans','Helvetica Neue','Helvetica',Helvetica,Arial,sans-serif;font-weight:normal;line-height:19px;font-size:14px;margin:0;padding:0px 10px 10px 0px" valign="top" align="center">
                              <img src="https://s3.amazonaws.com/frontend.poc.tothenew.net/email-assets/Hawk_logo.png" style="width:200px;display:inline;outline:none!important;text-decoration:none!important;clear:both;border:0" align="none" class="CToWUd">
                            </td>
                            <td style="word-break:break-word;border-collapse:collapse!important;width:0px;color:#222222;font-family:'Open Sans','Helvetica Neue','Helvetica',Helvetica,Arial,sans-serif;font-weight:normal;line-height:19px;font-size:14px;margin:0;padding:0" valign="top" align="left"></td>
                          </tr>
                        </tbody></table>

                      </td>
                    </tr>
                  </tbody></table>

                </center>
              </td>
            </tr>
          </tbody></table>

          <table style="border-spacing:0;border-collapse:collapse;vertical-align:top;text-align:inherit;width:580px;margin:0 auto;padding:0" width="600" bgcolor="#efefef">
            <tbody>
            <tr style="vertical-align:top;padding:0;background-color:white" align="left">
              <td style="color:#343b41;word-break:break-word;border-collapse:collapse!important;margin:0;padding:25px 35px;font:400 16px/27px 'Helvetica Neue',Helvetica,Arial,sans-serif" valign="top" align="center">


<table style="border-spacing:0;border-collapse:collapse;vertical-align:top;text-align:left;width:100%;display:block;padding:0px">
  <tbody><tr style="vertical-align:top;padding:0" align="left">
    <td style="word-break:break-word;border-collapse:collapse!important;color:#222222;font-family:'Open Sans','Helvetica Neue','Helvetica',Helvetica,Arial,sans-serif;font-weight:normal;line-height:19px;font-size:14px;margin:0;padding:10px 0px 0px" valign="top" align="left">
      <table style="border-spacing:0;border-collapse:collapse;vertical-align:top;text-align:left;width:580px;margin:0 auto;padding:0">
        <tbody><tr style="vertical-align:top;padding:0" align="left">
          <td style="width:80%;word-break:break-word;border-collapse:collapse!important;color:#222222;font-family:'Open Sans','Helvetica Neue','Helvetica',Helvetica,Arial,sans-serif;font-weight:normal;line-height:19px;font-size:14px;margin:0;padding:0px 0px 10px" valign="top" align="center">
            <h3 align="left">[Alerting] Security Breach Notification</h3>
          </td>
          <td style="width:50%;word-break:break-word;border-collapse:collapse!important;color:#222222;font-family:'Open Sans','Helvetica Neue','Helvetica',Helvetica,Arial,sans-serif;font-weight:normal;line-height:19px;font-size:14px;margin:0;padding:0px 0px 10px" valign="top" align="right">
       
                        <img src="https://s3.amazonaws.com/frontend.poc.tothenew.net/email-assets/redHeart.png" alt="down-img" height="40px" width="40px" />
           
          </td>
        </tr>
      </tbody></table>
    </td>
  </tr>
</tbody></table>

<table style="border-spacing:0;border-collapse:collapse;vertical-align:top;text-align:left;width:100%;display:block;padding:0px">
  <tbody><tr style="vertical-align:top;padding:0" align="left">
    <td style="word-break:break-word;border-collapse:collapse!important;color:#222222;font-family:'Open Sans','Helvetica Neue','Helvetica',Helvetica,Arial,sans-serif;font-weight:normal;line-height:19px;font-size:14px;margin:0;padding:0 0px 0 0" valign="top" align="left">
      <table style="border-spacing:0;border-collapse:collapse;vertical-align:top;text-align:left;width:580px;margin:0 auto;padding:0">
        <tbody><tr style="vertical-align:top;padding:0" align="left">
          <td style="word-break:break-word;border-collapse:collapse!important;color:#222222;font-family:'Open Sans','Helvetica Neue','Helvetica',Helvetica,Arial,sans-serif;font-weight:normal;line-height:19px;font-size:14px;margin:0;padding:0px 0px 10px" valign="top" align="center">
<pre style="font-family:'Open Sans','Helvetica Neue','Helvetica',Helvetica,Arial,sans-serif;font-weight:normal;line-height:19px;font-size:20px;margin:0 0 10px;padding:0" align="left">

"""+notification._event_title+"""</pre>
          </td>
         </tr>
         
            </tbody></table>
    </td>
  </tr>
</tbody></table>

<table style="border: 1px solid Black;border-collapse: collapse;
         vertical-align:top;text-align:left;width:100%;font-family:'Open Sans','Helvetica Neue','Helvetica',Helvetica,Arial,sans-serif;line-height:1.3;word-break:normal;font-size:18px;margin:0 auto;padding:0;margin-right:auto;margin-left:0px;">
         <tr>
          <th colspan="2" style="font-weight:bold;border: 1px solid Black;margin:0;padding:0" align="center">Event Details</th></tr>
        <tr>
        <th style="font-weight:normal;border: 1px solid Black;margin:0;padding:0" align="left"; >AWSAccountID</th>
        <th style="font-weight:normal;border: 1px solid Black;margin:0;padding:0" align="right">"""+str(notification._account_id)+"""</th>
        </tr>
        <tr>
        <th style="font-weight:normal;border: 1px solid Black;margin:0;padding:0" align="left">Project</th>
        <th style="font-weight:normal;border: 1px solid Black;margin:0;padding:0" align="right">"""+notification._account_name+"""</th>
        </tr>
        <tr>
        <th style="font-weight:normal;border: 1px solid Black;margin:0;padding:0" align="left ">User</th>
        <th style="font-weight:normal;border: 1px solid Black;margin:0;padding:0" align="right">"""+notification._user+"""</th>
        </tr>
        <tr>
        <th style="font-weight:normal;border: 1px solid Black;margin:0;padding:0" align="left ">User Type</th>
        <th style="font-weight:normal;border: 1px solid Black;margin:0;padding:0" align="right">"""+notification._user_type+"""</th>
        </tr>
        <tr>
        <th style="font-weight:normal;border: 1px solid Black;margin:0;padding:0" align="left ">EventRegion</th>
        <th style="font-weight:normal;border: 1px solid Black;margin:0;padding:0" align="right">"""+notification._event_region+"""</th>
        </tr>
        <tr>
        <th style="font-weight:normal;border: 1px solid Black;margin:0;padding:0" align="left ">EventName</th>
        <th style="font-weight:normal;border: 1px solid Black;margin:0;padding:0" align="right">"""+notification._event_name+"""</th>
       </tr>
        <tr>
        <th style="font-weight:normal;border: 1px solid Black;margin:0;padding:0" align="left">EventTime</th>
        <th style="font-weight:normal;border: 1px solid Black;margin:0;padding:0" align="right">"""+str(notification._event_time)+"""</th>
        </tr>
        <tr>
        <th style="font-weight:normal;border: 1px solid Black;margin:0;padding:0" align="left">EventID</th>
        <th style="font-weight:normal;border: 1px solid Black;margin:0;padding:0" align="right">"""+str(notification._event_id)+"""</th>
        </tr>
        <tr>
        <th style="font-weight:normal;border: 1px solid Black;margin:0;padding:0" align="left">LayerVersion</th>
        <th style="font-weight:normal;border: 1px solid Black;margin:0;padding:0" align="right">"""+str(notification._layer_version)+"""</th>
        </tr></table>

        <br>

        <table style="border: 1px solid Black;border-collapse: collapse;font-family:'Open Sans','Helvetica Neue','Helvetica',Helvetica,Arial,sans-serif;line-height:1.3;word-break:normal;font-size:18px;
         vertical-align:top;text-align:left;width:100%;margin:0 auto;padding:0;margin-right:auto;margin-left:0px;">
         <tr>
          <th colspan="2" style="font-weight:bold;border: 1px solid Black;margin:0;padding:0" align="center">Resource Details</th></tr>
        <tr>

        """
    for event_detail in notification._event_details:  
        for key in event_detail:
            ses_payload += """<tr>
              <th style="font-weight:normal;border: 1px solid Black;margin:0;padding:0" align="left">"""+str(key)+"""</th>
        <th style="font-weight:normal;border: 1px solid Black;margin:0;padding:0" align="right">"""+str(event_detail[key])+"""</th>
            </tr>
       
    """  
    ses_payload += """</table>"""




    ses_payload += """     </text-decoration>
            </tr>
          </tbody></table>
          <font color="#888888">
            </font><font color="#888888">
          </font><table style="border-spacing:0;border-collapse:collapse;vertical-align:top;text-align:center;color:#999999;margin-top:20px;padding:0" bgcolor="#f6f4f4">
            <tbody><tr style="vertical-align:top;padding:0" align="left">
              <td style="word-break:break-word;border-collapse:collapse!important;color:#222222;font-family:'Open Sans','Helvetica Neue','Helvetica',Helvetica,Arial,sans-serif;font-weight:normal;line-height:19px;font-size:14px;margin:0;padding:10px 20px 0px 0px" valign="top" align="left">
                <font color="#888888">
                </font><table style="border-spacing:0;border-collapse:collapse;vertical-align:top;text-align:center;width:580px;margin:0 auto;padding:0">
                  <tbody><tr style="vertical-align:top;padding:0" align="left">
                    <td style="word-break:break-word;border-collapse:collapse!important;width:100%;color:#222222;font-family:'Open Sans','Helvetica Neue','Helvetica',Helvetica,Arial,sans-serif;font-weight:normal;line-height:19px;font-size:14px;margin:0;padding:0px 0px 10px" valign="top" align="center">
                      <table style="border-spacing:0;border-collapse:collapse;vertical-align:top;text-align:center;width:580px;margin:0 auto;padding:0">
                          <tbody>
                            <tr style="vertical-align:top;padding:0">
                              <td>
                                  <table>
                                    <tr>
                                      <td>
                                        <a href="https://www.linkedin.com/company/tothenew">
                                    <span style="background-image: url('https://s3.amazonaws.com/frontend.poc.tothenew.net/email-assets/social_icons.png');margin-left:2px;width: 25px;height: 22px;display: block;margin-top: 15px;"></span>
                                  </a>
                                      </td>
                                      <td>
                                        <a href="https://twitter.com/tothenew">
                                          <span style="background-image: url('https://s3.amazonaws.com/frontend.poc.tothenew.net/email-assets/social_icons.png');margin-left:2px;width: 25px;height: 22px;display: block;background-position: -40px 0px;margin-top: 15px;"></span>
                                        </a>
                                      </td>
                                      <td>
                                        <a href="https://www.facebook.com/TOTHENEWDigital/">
                                        <span style="background-image: url('https://s3.amazonaws.com/frontend.poc.tothenew.net/email-assets/social_icons.png');margin-left:2px;width: 25px;height: 22px;display: block;background-position: -76px 0px;margin-top: 15px;"></span>
                                      </a>
                                      </td>
                                      <td>
                                        <a href="https://www.youtube.com/c/tothenew">
                                          <span style="background-image: url('https://s3.amazonaws.com/frontend.poc.tothenew.net/email-assets/social_icons.png');margin-left:2px;width: 25px;height: 22px;display: block; background-position: -147px 0px;margin-left: 0;margin-top: 15px;"</span>
                                        </a>
                                      </td>
                                    </tr>
                                  </table>
                              </td>
                              <td align="right">
                                <p>
                                  <img src="https://s3.amazonaws.com/frontend.poc.tothenew.net/email-assets/footer-logo.png" height="35px"/>
                                </p>
                              </td>
                            </tr>
                          </tbody>
                      </table>
                      <font color="#888888">
                    </font></td>
                    <td style="word-break:break-word;border-collapse:collapse!important;width:0px;color:#222222;font-family:'Open Sans','Helvetica Neue','Helvetica',Helvetica,Arial,sans-serif;font-weight:normal;line-height:19px;font-size:14px;margin:0;padding:0" valign="top" align="left"></td>
                  </tr></tbody></table><font color="#888888">
              </font></td></tr></tbody></table><font color="#888888">
        </font></center><font color="#888888">
      </font></td></tr></tbody></table>
</body>
</html>"""
   
    return ses_payload
regex = '^[A-Za-z0-9._%+-]+@[a-zA-Z]*.com$'
def if_valid_email_address(email):  
    if(re.search(regex,email)):  
        return True   
    else:  
        return False