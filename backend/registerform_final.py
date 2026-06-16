import json
import bcrypt
import boto3
import datetime
import jwt

def lambda_handler(event,context):
    try:
        ds=event.get("body")
        result=json.loads(ds)
        usrname=result.get("username")
        paswd=result.get("password")
        mail_id=result.get("email")
        dob=result.get("dob")
        e=paswd.encode('utf-8')
        salt=bcrypt.gensalt()
        ha=bcrypt.hashpw(e,salt)
        sa=ha.decode('utf-8')
        print(sa)

    except Exception as a:
        return{
            "body":json.dumps(f"Something Went Wrong,,{a} Data not found")
        }
    
    try:
        db=boto3.resource('dynamodb')
        table=db.Table('user_details')
        a=table.put_item(
            Item={
            "Username":usrname,
            "Password":sa,
            "email_id":mail_id,
            "DOB":dob
            }
            )
     

    except Exception as d:
        print(f"Something Went Wrong,{d} Could not be inserted")
        return {
            "statusCode": 500,
            "body": json.dumps(f"Something Went Wrong,{d} Could not be inserted")
        }

    ## JWT P
    try:
        secret_key="OKISADDDD"
        ctime=datetime.datetime.now(datetime.timezone.utc)
        expi=datetime.timedelta(hours =1)
        payload={
            "Username":usrname, 
            "iat":int(ctime.timestamp()),
            "exp":int((ctime+expi).timestamp()) 
        }

        token=jwt.encode(payload,secret_key,algorithm="HS256")
        cookie= f"auth_token={token}; Path=/; Max-Age=3600; HttpOnly; Secure; SameSite=Strict"

        return{
            "statusCode": 200,
            "headers": {
            "Content-Type": "application/json",
            "Set-Cookie": cookie 
        },
            "body": json.dumps({"message": "Cookie created successful!"})
    }
    
    except Exception as d:
        print(f"Something Went Wrong,{d} Could not create cookie")
        return {
            "statusCode": 500,
            "body": json.dumps(f"Something Went Wrong,{d} Could not create cookie")
        }
