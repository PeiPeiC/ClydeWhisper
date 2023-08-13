import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai
import logging
import os
from dotenv import load_dotenv
# Load the .env file
load_dotenv()

# Retrieve the values from the .env file
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
ClydeWhisper_OPENAI_API_KEY = os.getenv('ClydeWhisper_OPENAI_API_KEY')

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)
openai.api_key = ClydeWhisper_OPENAI_API_KEY


@csrf_exempt
def line_webhook(request):
    # logging.info("Entered handle_message function.")
    if request.method == 'POST':
        signature = request.headers['X-Line-Signature']
        body = request.body.decode()
        try:
            # logging.info("Before calling handler.handle.")
            handler.handle(body, signature)
            # logging.info("After calling handler.handle.")
        except InvalidSignatureError:
            return HttpResponse(status=400)
        except Exception as e:
            # logging.error(f"Error in handler.handle: {e}")
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
                    "content": "Firstly, optimise the provided chat text into natural colloquial British English, preferably using British Slang or buzzwords.\nSecondly, if there are any errors point them out\nFinally,from your optimised text, extract some vocabulary or collocation for Advanced English learners in bullet points \nDo not repeat the prompt!\n\n"
                }
            ],
            temperature=1,
            max_tokens=200,
            top_p=0.3,
            frequency_penalty=1.2,
            presence_penalty=1.2
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
