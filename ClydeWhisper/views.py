import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai
import logging
line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')
openai.api_key = 'YOUR_OPENAI_API_KEY'

@csrf_exempt
def line_webhook(request):
    logging.info("Entered handle_message function.")
    if request.method == 'POST':
        signature = request.headers['X-Line-Signature']
        body = request.body.decode()
        try:
            logging.info("Before calling handler.handle.")
            handler.handle(body, signature)
            logging.info("After calling handler.handle.")
        except InvalidSignatureError:
            return HttpResponse(status=400)
        except Exception as e:
            logging.error(f"Error in handler.handle: {e}")
            return HttpResponse(status=500)
        return HttpResponse(status=200)
    return HttpResponse(status=405)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    logging.info(f"Event object: {event}")
    logging.info(f"Message object: {event.message}")
    try:
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
            "role": "user",
            "content": event.message.text  
            },
            {        
            "role": "system",
            "content": "You will be provided with chat conversations, which might be in Chinese or English.\nFirstly, your task is to translate or optimise them into colloquial British English \nSecondly, point out errors in the original text and suggest better words choice for natural conversation, such as British slang.\nFinally, extract some vocabulary or collocation for Advanced English learners in bullet points from your suggested improvement.\n\n"
            }, 
        ],
        temperature=1,
        max_tokens=340,
        top_p=0.85,
        frequency_penalty=0.2,
        presence_penalty=0.2
        )
        logging.info(f"Response object: {response}")
        logging.info(f"Choices object: {response.choices}")
        corrected_text = response.choices[0].message.content.strip()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=corrected_text))
    except Exception as e:
        logging.error(f"Exception type: {type(e)}, Error message: {e}")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"Error: {e}"))

    # logging.basicConfig(level=logging.DEBUG)
    # logging.info(json.dumps(response, indent=4))
    
