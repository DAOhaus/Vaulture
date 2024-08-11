from transformers import pipeline
from collections import Counter

def analyze_sentiments(messages, model_names, use_gpu=False):
    device = 0 if use_gpu else -1
    
    sentiment_votes = {message: [] for message in messages}
    
    for model_name in model_names:
        sentiment_analysis = pipeline("sentiment-analysis", model=model_name, device=device)
        results = sentiment_analysis(messages)
        
        for message, result in zip(messages, results):
            label = result['label']
            if label == 'POSITIVE':
                sentiment_votes[message].append('positive')
            elif label == 'NEGATIVE':
                sentiment_votes[message].append('negative')
            else:
                sentiment_votes[message].append('neutral')
    
    final_sentiments = {}
    for message, votes in sentiment_votes.items():
        vote_count = Counter(votes)
        final_sentiment = vote_count.most_common(1)[0][0]
        final_sentiments[message] = final_sentiment

    return final_sentiments

# List of model names to use
model_names = [
    "distilbert-base-uncased-finetuned-sst-2-english",
    "nlptown/bert-base-multilingual-uncased-sentiment",
    "FacebookAI/xlm-roberta-large",
    "microsoft/deberta-v3-large",
    "cardiffnlp/twitter-roberta-base-sentiment",
    "finiteautomata/bertweet-base-sentiment-analysis",
    "openai/gpt-2-xl",
    # "andthattoo/llama2-7b-crypto-Q3_K_M-GGUF" # Uncomment if supported in your environment
]

# Load messages from a text file
with open('twitter_messages.txt', 'r', encoding='utf-8') as file:
    messages = [line.strip() for line in file.readlines()]

use_gpu = True
final_sentiments = analyze_sentiments(messages, model_names, use_gpu=use_gpu)

# Print the final sentiments
for message, sentiment in final_sentiments.items():
    print(f"Message: {message} \nFinal Sentiment: {sentiment}\n")
