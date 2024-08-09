from transformers import pipeline

def analyze_sentiments(messages, model_name="distilbert-base-uncased-finetuned-sst-2-english", use_gpu=False):
    # Set device to GPU if available and use_gpu is True
    device = 0 if use_gpu else -1

    # Load the sentiment-analysis pipeline using the specified model
    sentiment_analysis = pipeline("sentiment-analysis", model=model_name, device=device)

    # Analyze the sentiment of each message
    results = sentiment_analysis(messages)

    # Convert the results to a more readable format
    sentiment_tags = []
    for result in results:
        label = result['label']
        score = result['score']

        # Classify as positive, neutral, or negative
        if label == 'POSITIVE':
            sentiment_tags.append('positive')
        elif label == 'NEGATIVE':
            sentiment_tags.append('negative')
        else:
            sentiment_tags.append('neutral')  # Assuming there is a neutral label or handle other cases
    return sentiment_tags

# Example usage
messages = [
    "I love this product!",
    "It's okay, nothing special.",
    "This is the worst experience I've ever had."
]


messages = [
    """🐋Whale trade alert

weETH/WETH

Swapped 99.44 $weETH for 103.77 $WETH

👀 Check, Track, Analyze and Trade on https://app.kattana.io/ETH/0x7A415B19932c0105c82FDB6b720bb01B0CC2CAe3
#cryptocurrency #Kattana #DEX #Trade
👍 Like and follow to support"""
]

# You can change the model name here to any other model you prefer
model_name="distilbert-base-uncased-finetuned-sst-2-english"
# model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
# model_name = "FacebookAI/xlm-roberta-large"
# model_name = "microsoft/deberta-v3-large"
# model_name = "cardiffnlp/twitter-roberta-base-sentiment"
# model_name = "finiteautomata/bertweet-base-sentiment-analysis"
# model_name = "openai/gpt-2-xl"
model_name = "andthattoo/llama2-7b-crypto-Q3_K_M-GGUF"
use_gpu = True

sentiment_tags = analyze_sentiments(messages, model_name=model_name, use_gpu=use_gpu)
for message, sentiment in zip(messages, sentiment_tags):
    print(f"Message: {message} \nSentiment: {sentiment}\n")