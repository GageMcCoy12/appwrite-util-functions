from appwrite.client import Client
from appwrite.services.account import Account  # <-- this is the correct import
from appwrite.exception import AppwriteException
import os

def main(context):
    try:
        # get user id and secret from query params
        user_id = context.req.query.get('userId')
        secret = context.req.query.get('secret')
        
        if not user_id or not secret:
            return context.res.json({
                'success': False,
                'message': 'Missing userId or secret'
            }, 400)
        
        # init appwrite client
        client = Client()
        client.set_endpoint('https://cloud.appwrite.io/v1')
        client.set_project(os.environ['APPWRITE_FUNCTION_PROJECT_ID'])
        client.set_key(os.environ['APPWRITE_API_KEY'])
        
        # update verification using Account service
        account = Account(client)
        result = account.update_verification(
            user_id=user_id,
            secret=secret
        )
        
        return context.res.json({
            'success': True,
            'message': 'Email verified successfully',
            'user': result
        })
        
    except AppwriteException as e:
        return context.res.json({
            'success': False,
            'message': str(e)
        }, 500)
    except Exception as e:
        return context.res.json({
            'success': False,
            'message': f'Unexpected error: {str(e)}'
        }, 500)
