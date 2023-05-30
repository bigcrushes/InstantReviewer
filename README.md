# InstantReviewer

## What it does
Ever saw a product or new store and wondered what people have to say about it? Spending countless of hours reading numerous articles on their reviews? InstantReviewer provides an easier way to do this: Consolidating the buzz words surrounding the product to make reviewing products and stores easier.

## How to run
Install the dependencies using 

`pip install -r requirements.txt`

Then, run `app.py` and visit the localhost link provided!

Google might flag this as spam after a while. We provided some examples for McDonald's review in the repo and can be accessed on `/query/mcdonalds`. For the McDonald's example, the `results` in `scrapy.py` can be replaced by the commented out `results` if the Google scraping is detected as spam and we still want it to run normally for the example.

* Seems to have some issues with Macbook compatibility

## Future plans
- Delete wordclouds after generating webpages
- Improve UI/UX
- Include back button/allow searching again more easily
