# ClydeWhisper

ClydeWhisper is a Line bot that connects to the OpenAI API to assist English learners. By adding this channel to their chat room, users can have a tutor that corrects their conversations with friends in colloquial British English.

## Deploy in Local Environment

Follow these steps to set up ClydeWhisper in your local environment:

1. **Clone the Repository**
    `git clone [repository-link]`

2. **Activate Virtual Environment**

- **Windows**
  ```
  .\venv\Scripts\activate
  ```

- **macOS and Linux**
  ```
  source venv/bin/activate
  ```

3. **Install Dependencies**
    `pip install -r requirements.txt`

4. **Create Line Channel**
- Go to the LINE Developers Console and create a new channel.
- Note down the channel token and secrets.

5. **Use Ngrok**
- Download and install [ngrok](https://ngrok.com/).
- Use ngrok to create an HTTPS link and map it to your local port for the LINE webhook connection.
  ```
  ngrok http [your-local-port]
  ```

6. **Test LINE Webhook**
- Go to the LINE Developers Console and set the webhook URL to the HTTPS link provided by ngrok.
- Verify the webhook connection.

7. **Start Chatting!**
- Add the bot to your LINE chat room and start a conversation.

## Deploy on Render

[Provide steps for deploying on Render here.]


