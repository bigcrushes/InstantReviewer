from googlesearch import search
import urllib.request as urllib
from bs4 import BeautifulSoup
from wordcloud import WordCloud
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import nltk

# Download necessary nltk files
nltk.download('vader_lexicon')
nltk.download('wordnet')
nltk.download('stopwords')

def get_sentiment(query):
    # Sentiment Analyzer
    sia = SentimentIntensityAnalyzer()

    # Search results
    results = search(query + " review", lang='en', num_results=30)

    # results = ['https://www.ign.com/articles/pokemon-scarlet-and-violet-review', 'https://www.theguardian.com/games/2022/nov/17/pokemon-scarletviolet-review-poor-performance-holds-an-exciting-game-back', 'https://www.metacritic.com/game/switch/pokemon-violet', 'https://www.thegamer.com/pokemon-scarlet-violet-worth-it/', 'https://kotaku.com/pokemon-scarlet-and-violet-review-nintendo-switch-1849843125', 'https://www.cnn.com/cnn-underscored/reviews/pokemon-scarlet-violet', 'https://www.nintendolife.com/reviews/nintendo-switch/pokemon-scarlet-and-violet', 'https://apptrigger.com/2022/12/10/pokemon-scarlet-and-violet-review/', 'https://rpgamer.com/review/pokemon-violet-review/', 'https://www.pcmag.com/reviews/pokemon-scarletviolet-for-nintendo-switch', 'https://www.gamerbraves.com/pokemon-scarlet-violet-review-two-of-the-best-pokemon-switch-games-held-back-by-poor-performance/', 'https://www.gamespot.com/reviews/pokemon-scarlet-violet-review-a-braviary-new-world/1900-6417994/', 'https://www.engadget.com/pokemon-scarlet-and-violet-review-growth-and-growing-pains-140048933.html', 'https://www.washingtonpost.com/video-games/reviews/pokemon-scarlet-violet-review/', 'https://www.theverge.com/23462858/pokemon-violet-scarlet-review-nintendo-switch', 'https://www.polygon.com/reviews/23462736/pokemon-scarlet-and-violet-review-release-date-nintendo-switch', 'https://www.digitalspy.com/tech/a42219724/pokemon-scarlet-violet-review/', 'https://www.nine.com.au/product-reviews/tech/pokemon-scarlet-violet-nintendo-switch-review/02f34207-cedf-407d-87ca-87bbb4388225', 'https://www.imore.com/gaming/nintendo-switch/pokemon-scarlet-and-violet-for-nintendo-switch-review-best-and-worst-gen-of-all-time', 'https://aiptcomics.com/2022/12/12/pokemon-scarlet-and-violet-review/', 'https://www.videogameschronicle.com/news/pokemon-violet-is-now-the-lowest-rated-main-pokemon-game-on-metacritic/', 'https://www.express.co.uk/entertainment/gaming/1716937/Pokemon-Scarlet-review-Violet-Nintendo-Switch', 'https://switchplayer.net/2022/12/24/pokemon-scarlet-violet-review/', 'https://www.gameindustry.com/reviews/game-review/pokemon-violet-second-take-review/', 'https://www.rpgfan.com/review/pokemon-scarlet-violet/', 'https://pokemongohub.net/post/review/scarlet-violet-honest-review/', 'https://themakoreactor.com/reviews/pokemon-violet-review-one-month-later-patch-update/43971/', 'https://www.magneticmag.com/2022/12/pok%C3%A9mon-violet-review/', 'https://www.vooks.net/pokemon-scarlet-and-violet-review/', 'https://gamingrespawn.com/reviews/57966/pokemon-scarlet-violet-review/']

    # Open and read through all google search pages and get text
    compiled_text = []
    for url in list(results)[:10]:
        try:
            url_content = urllib.urlopen(url).read()
            text = BeautifulSoup(url_content, "lxml").text
            text_cleaned =  [word.lower() for word in text.split(' ') if word.isalpha() or word.isnumeric()]
            compiled_text.extend(text_cleaned)
        except:
            continue

    # Extract important words
    lemmatizer = WordNetLemmatizer()
    qry_words = query.lower().split(' ') + [lemmatizer.lemmatize(word) for word in query.lower().split(' ')]
    stop_words = list(set(stopwords.words('english'))) + qry_words + ['review', 'reviews']
    final_text = [lemmatizer.lemmatize(word) for word in compiled_text if word not in stop_words]

    # Categorise words into positive, neutral, negative
    negative_words = []
    positive_words = []
    neutral_words = []
    for word in final_text:
        score = sia.polarity_scores(word)
        if score['compound'] > 0.05:
            positive_words.append(word)
        if score['compound'] < -0.05:
            negative_words.append(word)
        else:
            neutral_words.append(word)

    # Get positive sentiment words
    positive_text = ' '.join(positive_words)
    wordcloud = WordCloud(max_font_size=100, max_words=100,
                      background_color="white",random_state=0).generate(positive_text)
    plt.figure(figsize=(12,10))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.title("Positive Sentiments"+'\n',size=20)
    plt.axis("off")
    plt.savefig(f'{query}_positive.png')

    # Get negative sentiment words
    negative_text = ' '.join(negative_words)
    wordcloud = WordCloud(max_font_size=100, max_words=100,
                      background_color="white",random_state=0).generate(negative_text)
    plt.figure(figsize=(12,10))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.title("Negative Sentiments"+'\n',size=20)
    plt.axis("off")
    plt.savefig(f'{query}_negative.png')

    # Get neutral sentiment words
    neutral_text = ' '.join(neutral_words)
    wordcloud = WordCloud(max_font_size=100, max_words=100,
                      background_color="white",random_state=0).generate(neutral_text)
    plt.figure(figsize=(12,10))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.title("Neutral Sentiments"+'\n',size=20)
    plt.axis("off")
    plt.savefig(f'{query}_neutral.png')

    return {"positive": len(positive_words), "negative": len(negative_words), "neutral": len(neutral_words),}

