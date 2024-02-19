import praw, requests, json

# Initialize the Reddit instance with your credentials
reddit = praw.Reddit(
    client_id='yclient_id',
    client_secret='your_client_secret',
    user_agent='your_user_agent'
)

url = 'https://api.gptzero.me/v2/predict/text'

headers = {
    'x-api-key': 'gptzero_api_key'
}
# Define the subreddit where the bot will monitor comments
subreddit = reddit.subreddit('subreddit')

# Define the bot's behavior when it detects a "!checkAI" reply
def check_ai_reply(comment):
    # Check if the comment is a reply to a command
    if comment.is_root:
        return

    parent_comment = comment.parent()

    # Check if the parent comment contains the "!checkAI" command
    if parent_comment.body.startswith('!checkAI'):
        # Extract the message content from the parent comment
        message_content = parent_comment.body[len('!checkAI'):].strip()
        print(f'Message content from comment {parent_comment.id}: {message_content}')
        body = {
            'document': message_content
        }
        response = requests.post(url, headers=headers, data=json.dumps(body))
        if response.status_code ==   200:
            response_data = response.json()
            average_generated_prob = response_data['documents'][0]['average_generated_prob']
            comment.reply(f'Parent message contains {average_generated_prob*100}% AI generated code')


# Monitor the subreddit for new comments
for comment in subreddit.stream.comments():
    check_ai_reply(comment)
