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
    results = list(search(query + " review", lang='en', num_results=30))

    # results = ['https://www.tripadvisor.com.sg/Restaurant_Review-g294265-d5430609-Reviews-McDonald_s-Singapore.html', 'https://www.facebook.com/mcdsg/reviews', 'https://eatbook.sg/tag/mcdonalds/', 'https://www.burpple.com/mcdonalds-parklane', 'https://mustsharenews.com/singapore-mcdonalds-world-best/', "https://sg.indeed.com/cmp/McDonald's/reviews", 'https://www.jobstreet.com.sg/en/companies/476235-hanbaobao-pte-ltd-licensee-of-mcdonalds/reviews', 'https://www.instagram.com/mcdsg/?hl=en', 'https://www.consumeraffairs.com/food/mcd.html', 'https://www.sitejabber.com/reviews/mcdonalds.com', 'https://girlstyle.com/sg/article/112872/mcdonalds-jjang-jjang-burger-review', 'https://www.glassdoor.sg/Overview/Working-at-McDonald-s-EI_IE432.11,21.htm', 'https://mothership.sg/2022/11/mcdonalds-world-cup-menu-review/', 'https://middleclass.sg/trending/bt21-mcdonalds-review/', 'https://youthopia.sg/read/taste-taste-mcdonalds-chicken-mccrispy-sweet-paprika-watermelon-twist-cone-calamansi-mcfizz-and-crisscut-fries/', 'https://www.productreview.com.au/listings/mcdonald-s', 'https://www.trustpilot.com/review/www.mcdonalds.co.uk', 'https://www.asiaone.com/lifestyle/i-tried-mcdonalds-remastered-quarter-pounder-cheese-thats-back-after-5-years-it-better', 'https://www.insider.com/singapore-salmon-burger-mcdonalds-menu-items-review-price-photos-2022-4', 'https://goodyfeed.com/prosperity-burger-mcdonalds/', 'https://www.mcdonalds.com/ca/en-ca/contact-us/talk-to-us.html', 'https://www.ambitionbox.com/reviews/mcdonalds-reviews', 'https://www.mcdonalds.com.sg/dessert-kiosk', 'https://www.safarway.com/en/property/mcdonalds-marine-cove', 'https://www.foodadvisor.com.sg/restaurant/mcdonalds-the-seletar-mall/', 'https://www.mcdonalds.com/ca/en-ca/contact-us/talk-to-us.html', 'https://goodyfeed.com/prosperity-burger-mcdonalds/', 'https://www.ambitionbox.com/reviews/mcdonalds-reviews', 'https://www.mcdonalds.com.sg/', 'https://www.safarway.com/en/property/mcdonalds-marine-cove', 'https://www.foodadvisor.com.sg/restaurant/mcdonalds-the-seletar-mall/', 'https://www.amazon.sg/Grinding-Out-Mcdonalds-Ray-Kroc/product-reviews/125013028X?reviewerType=all_reviews']

    # Open and read through all google search pages and get text
    compiled_text = []
    for url in results[:10]:
        try:
            url_content = urllib.urlopen(url, timeout=1).read()
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
    plt.savefig(f'static/{query.upper()}_positive.png')

    # Get negative sentiment words
    negative_text = ' '.join(negative_words)
    wordcloud = WordCloud(max_font_size=100, max_words=100,
                      background_color="white",random_state=0).generate(negative_text)
    plt.figure(figsize=(12,10))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.title("Negative Sentiments"+'\n',size=20)
    plt.axis("off")
    plt.savefig(f'static/{query.upper()}_negative.png')

    # Get neutral sentiment words
    neutral_text = ' '.join(neutral_words)
    wordcloud = WordCloud(max_font_size=100, max_words=100,
                      background_color="white",random_state=0).generate(neutral_text)
    plt.figure(figsize=(12,10))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.title("Neutral Sentiments"+'\n',size=20)
    plt.axis("off")
    plt.savefig(f'static/{query.upper()}_neutral.png')

    return {"positive": len(positive_words), "negative": len(negative_words), "neutral": len(neutral_words),}

