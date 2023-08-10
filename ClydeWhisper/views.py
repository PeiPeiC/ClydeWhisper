import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai
import logging
line_bot_api = LineBotApi('GqMeEhCAFWcHjGS9sDuIYzRl+J8i664MsTNo9VRVkbxprL1v97eHsozP6WkrEnE1I67nIgeUBdrNi5WSqjoxH1NwLpLHcjURteyqowUvkX8DaprCZQ4v2qiy3MnU4o1c2F8HjYa6Ivai+d2UklYoawdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('c842357d1a647b5e4cf0e111237ee389')
openai.api_key = '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'

@csrf_exempt
def line_webhook(request):
    if request.method == 'POST':
        signature = request.headers['X-Line-Signature']
        body = request.body.decode()
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            return HttpResponse(status=400)
        return HttpResponse(status=200)
    return HttpResponse(status=405)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    
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
    corrected_text = response.choices[0].text.strip()
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=corrected_text))

    logging.basicConfig(level=logging.DEBUG)
    logging.info(json.dumps(response, indent=4))
