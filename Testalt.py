import streamlit as st
import pandas as pd
from openbb_terminal.sdk import openbb
from openbb_terminal.config_terminal import theme  # noqa: F401
from openbb_terminal.helper_classes import TerminalStyle
from openbb_terminal import helper_funcs as helper  # noqa: F401
from openbb_terminal.reports import widget_helpers as widgets  # noqa: F401
from openbb_terminal.cryptocurrency.due_diligence.pycoingecko_model import (  # noqa: F401
    Coin,
)
from openbb_terminal.core.library.breadcrumb import Breadcrumb
from openbb_terminal.core.library.trail_map import TrailMap
from openbb_terminal.core.library.breadcrumb import MetadataBuilder

TerminalStyle().applyMPLstyle()
trail = ""
trail_map = TrailMap()
metadata = MetadataBuilder.build(trail=trail, trail_map=trail_map)
backgroundColor='#FFFFFF'


openbb = Breadcrumb(
    metadata=metadata,
    trail=trail,
    trail_map=trail_map,
)

#st.markdown('<style>body{background-color: Black;}</style>', unsafe_allow_html=True)
st.set_page_config(layout="wide")
st.set_option('deprecation.showPyplotGlobalUse', False)
col1, col2, col3, col4 = st.columns([25, 11, 4, 10])
with col1:
    st.title('Dashboard Powered By')
    st.write('Built by Alexander Schroer')

with col2:
    st.image("https://raw.githubusercontent.com/OpenBB-finance/OpenBBTerminal/main/images/openbb_logo.png", width=120)

with col3:
    st.markdown(""" 
    # And
                """)

with col4:
    st.image("https://raw.githubusercontent.com/mesmith027/streamlit-roboflow-demo/master/images/streamlit_logo.png",
             width=180)



def color_negative_red(val):
    if type(val) != 'str':
        color = 'green' if val > 0 else 'red'
        return f'color: {color}'

def color_positive_red(val):
    if type(val) != 'str':
        color = 'red' if val > 0 else 'green'
        return f'color: {color}'

col1, col2, col3 = st.columns([30, 30, 30])
# with col1:
#     st.subheader('Global Bonds')
#     data = openbb.economy.glbonds()
#     data[data.columns[1]] = data[data.columns[1]].apply(pd.to_numeric)
#     data[data.columns[2]] = data[data.columns[2]].apply(pd.to_numeric)
#     data[data.columns[3]] = data[data.columns[3]].apply(pd.to_numeric)

#     columns = data.columns[3]

#     st.dataframe(data.style.applymap(color_positive_red, subset=[columns]))


# with col2:
#     st.subheader('US Bonds')
#     data = openbb.economy.usbonds()
#     data[data.columns[1]] = data[data.columns[1]].apply(pd.to_numeric)
#     data[data.columns[2]] = data[data.columns[2]].apply(pd.to_numeric)
#     data[data.columns[3]] = data[data.columns[3]].apply(pd.to_numeric)

#     columns = data.columns[3]
#     st.dataframe(data.style.applymap(color_positive_red, subset=[columns]))

with col3:
    st.subheader('10y US Treasury Yield')
    st.line_chart(openbb.economy.treasury(maturities=['10y'], start_date='1976-12-31'))

col1, col2, col3 = st.columns(3)
with col1:
    st.subheader('Equity Futures')
    data = openbb.economy.future()
    data[['last', 'change']] = data[['last', 'change']].apply(pd.to_numeric)
    st.dataframe(data.style.applymap(color_negative_red, subset=['last', 'change']))

with col2:
    st.subheader('Commodities')
    data = openbb.economy.futures()

    data[['Chg', '%Chg']] = data[['Chg', '%Chg']].apply(pd.to_numeric)
    st.dataframe(data.style.applymap(color_negative_red, subset=['Chg', '%Chg']))

with col3:
    st.subheader('World Currencies')
    data = openbb.economy.currencies()
    data[['Chng']] = data[['Chng']].apply(pd.to_numeric)
    data[['%Chng']] = data[['%Chng']].apply(pd.to_numeric)
    st.dataframe(data.style.applymap(color_negative_red, subset=['Chng', '%Chng']))

st.title('Yield Spread 10y2y')
col1, col2 = st.columns([55, 55])
with col1:
    st.subheader('US 2y10y Spread')
    data=openbb.economy.treasury(maturities=['2y', '10y'], start_date='1976-12-31')
    data['10y-2y Spread']=data['Nominal_10-year']-data['Nominal_2-year']
    st.line_chart(data)

with col2:
    st.subheader('10y Real rate')
    data = openbb.economy.treasury(instruments=['inflation', 'nominal'], maturities=['10y'], start_date='2010-01-01')
    data['10y Real rate'] = data['Nominal_10-year'] - data['Inflation_10-year']
    st.line_chart(data)

col1, col2 = st.columns(2)
with col1:
    st.subheader('News')
    st.dataframe(openbb.news())

with col2:
    st.subheader('ECO Calender')
    st.dataframe(openbb.economy.events(['Germany','Spain','France','Italy','European Union','United Kingdom','United States','China']))

col1, col2 =st.columns([85,60])

with col1:
    st.subheader('ETF Movers')
    data=openbb.etf.disc.mover(sort_type='active')
    data[['Chg']] = data[['Chg']].apply(pd.to_numeric)
    data[['%Chg']] = data[['%Chg']].apply(pd.to_numeric)
    st.dataframe(data.style.applymap(color_negative_red, subset=['Chg', '%Chg']))

st.title('Economy')
col1, col2 = st.columns([55, 55])
with col1:
    st.pyplot(openbb.economy.inf_chart())
with col2:
    st.pyplot(openbb.economy.cpi_chart())

col1, col2 = st.columns([55, 55])
with col1:
    st.pyplot(openbb.economy.gdp_chart())
with col2:
    st.pyplot(openbb.economy.unemp_chart())


st.subheader(
    'Enter a ticker below to get price chart, Government Contracts, Insider Activity, and list of suppliers and customers')
text_input = st.text_input('Symbol')
if text_input:
    data = openbb.stocks.load(text_input)
    df_max_scaled = data.copy()
    st.pyplot(openbb.stocks.candle(symbol=text_input, ma=[50, 150]))

    col1, col2 = st.columns([1,1])
    with col1:
        st.subheader('Cash Flows for {}'.format(text_input))
        st.dataframe(openbb.stocks.fa.cash(symbol=text_input, quarterly=True, limit=5))

    with col2:
        st.subheader('Key Metrics for {}'.format(text_input))
        st.dataframe(openbb.stocks.fa.key(symbol=text_input))

col1, col2 = st.columns(2)
with col1:
    st.subheader('Revenue Forecast for {}'.format(text_input))
    st.dataframe(openbb.stocks.fa.revfc(text_input))

with col2:
    st.subheader('Key Metrics Growth of {}'.format(text_input))
    st.dataframe(openbb.stocks.fa.growth(text_input))

col1, col2 = st.columns(2)
with col1:
    st.subheader('Suppliers of {}'.format(text_input))
    st.dataframe(openbb.stocks.dd.supplier(text_input))

with col2:
    st.subheader('Customers of {}'.format(text_input))
    st.dataframe(openbb.stocks.dd.customer(text_input))
