from flask import Flask, render_template, request, redirect, url_for
from scraper import get_sentiment

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form.get('query')
        return redirect(url_for(f'answer_query', query=query))
    return render_template('index.html')

@app.route('/query/<query>')
def answer_query(query):
   sentiments = get_sentiment(query)
   # Get comparison of positive vs negative sentiment
   total_sentiments = sentiments["positive"] + sentiments["negative"]
   positive_rate = sentiments["positive"] / total_sentiments * 100
   return render_template('query.html', query=query.upper(), sentiments=round(positive_rate,2))

if __name__ == '__main__':
    app.run(debug=True)
