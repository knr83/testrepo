
import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from plotly.offline import plot
import warnings
# Ignore all warnings
warnings.filterwarnings("ignore", category=FutureWarning)

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    plot(fig, auto_open=True)
    # fig.show()
    
    
    
tesla = yf.Ticker("TSLA")

tesla_data = tesla.history(period='max')
tesla_data.reset_index(inplace=True)

# print(tesla_data.head(n=5))


url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
html_data = requests.get(url).text
soup = BeautifulSoup(html_data, "html.parser")
tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])

lst = []

for row in soup.find("tbody").find_all('tr'):
    col = row.find_all("td")
    date = col[0].text
    revenue = col[1].text    
    lst.append({"Date":date, "Revenue":revenue})

    # !!!As of pandas 2.0, append (previously deprecated) was removed.
    # tesla_revenue = tesla_revenue._append({"Date":date, "Revenue":revenue}, ignore_index=True)    

df_extended = pd.DataFrame(lst, columns=tesla_revenue.columns)
tesla_revenue = pd.concat([tesla_revenue, df_extended])

tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"", regex=True)
tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]

# print(tesla_revenue.tail(n=5))

make_graph(tesla_data, tesla_revenue, 'Tesla')



gme = yf.Ticker("GME")

gme_data = gme.history(period='max')
gme_data.reset_index(inplace=True)

# print(gme_data.head(n=5))


url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
html_data = requests.get(url).text
soup = BeautifulSoup(html_data, "html.parser")
gme_revenue = pd.DataFrame(columns=["Date", "Revenue"])

lst = []

for row in soup.find("tbody").find_all('tr'):
    col = row.find_all("td")
    date = col[0].text
    revenue = col[1].text    
    lst.append({"Date":date, "Revenue":revenue})

    # !!!As of pandas 2.0, append (previously deprecated) was removed.
    # gme_revenue = tesla_revenue._append({"Date":date, "Revenue":revenue}, ignore_index=True)    

df_extended = pd.DataFrame(lst, columns=gme_revenue.columns)
gme_revenue = pd.concat([gme_revenue, df_extended])

gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(',|\$',"", regex=True)
gme_revenue.dropna(inplace=True)
gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]

# print(gme_revenue.tail(n=5))


make_graph(gme_data, gme_revenue, 'GameStop')

