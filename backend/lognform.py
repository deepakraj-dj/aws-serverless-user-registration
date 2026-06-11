import json
import bcrypt
import boto3


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
        return {
            "statusCode": 200,
            "body": json.dumps("Data has been stored")
        }

    except Exception as d:
        print(f"Something Went Wrong,{d} Could not be inserted")
        


    




