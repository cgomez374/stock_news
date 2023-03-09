import requests

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALPHA_API_KEY = 'INSERT API KEY HERE'
alpha_endpoint = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={STOCK}&interval=60min&&apikey={ALPHA_API_KEY}'

NEWS_API_KEY = 'INSERT API KEY HERE'
news_from_date = ''
news_endpoint = f'https://newsapi.org/v2/everything?q=tesla&from={news_from_date}&sortBy=publishedAt&language=en&apiKey={NEWS_API_KEY}'

# STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

# Get Data

stock_data = requests.get(alpha_endpoint).json()['Time Series (60min)']
intraday_close_prices = [(key.replace('20:00:00', '').strip(), value['4. close']) for (key, value) in stock_data.items() if '20:00:00' in key]
yesterday = intraday_close_prices[0][0]
yesterday_closing_price = float(intraday_close_prices[0][1])

day_before = intraday_close_prices[1][0]
day_before_closing_price = float(intraday_close_prices[1][1])

print(f'Closing Price For {yesterday} was {yesterday_closing_price}!')
print(f'Closing Price For {day_before} was {day_before_closing_price}!')

# Determine if change in price

difference = yesterday_closing_price - day_before_closing_price
diff_percentage = round(abs((difference / yesterday_closing_price) * 100))
is_difference = False

if difference < 0:
    print(f'Down by {diff_percentage}%!')
    is_difference = True
elif difference > 0:
    print(f'Up by {diff_percentage}%!')
    is_difference = True

# STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

if is_difference:
    print('Top News:')
    news_from_date = day_before
    news_data = requests.get(news_endpoint).json()['articles']
    top_three_list = [(news_data[i]['title'], news_data[i]['description']) for i in range(3)]

    for article in top_three_list:
        print(f'\n=={article[0]}==\n{article[1]}')

