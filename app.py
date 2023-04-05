import plotly.express as px
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from collections import Counter


class ProblemStatement:

    def __init__(self):
        st.title('The Problem Statement.')
        st.markdown('---')

        st.subheader("To analyze the factors that affect hotel bookings and cancellations in order to optimize revenue and occupancy rates for the hotel.")

        st.markdown('###### This problem statement aims to investigate the factors that contribute to successful hotel bookings and cancellations. By identifying these factors, the hotel can optimize its revenue and occupancy rates, which are crucial for its sustainability and growth.')

        st.markdown('---')

        st.subheader('The following questions guided me for the analysis: ')

        st.text("""
1. What are the most common types of bookings (e.g., number of adults, number of children,\n type of meal plan, room type)?\n
2. How does the lead time (i.e., the time between booking and arrival) affect the booking status?\n
3. Are there any patterns in the booking and cancellation behavior of repeated guests?\n
4. How do market segments differ in terms of booking and cancellation rates?\n
5. What is the relationship between the average price per room and the booking status?\n
6. Are there any specific requests (e.g., car parking space, number of special requests)\n that are more likely to lead to successful bookings?\n
7. Can we predict the likelihood of a booking being cancelled based on the available data?\n

        """)
        st.markdown('---')

        st.text('By answering these questions, the hotel can gain insights into the factors\n that contribute to successful bookings and cancellations, and use this information to \nimprove its revenue and occupancy rates')


class MyDashBoard:

    def __init__(self):
        st.title(':hotel: HOTEL RESERVATION DASHBOARD')
        st.markdown('---')
        self.dataset = pd.read_csv('./hotel_reservation.csv')
        st.sidebar.header('Please use this Filter.')

        self.booking_status = st.sidebar.multiselect('filter by booking status', options=self.dataset['booking_status'].unique(), default=self.dataset['booking_status'].unique())

        self.arrival_year = st.sidebar.multiselect('filter by arrival year', options=self.dataset['arrival_year'].unique(), default=self.dataset['arrival_year'].unique())

        self.market_segment = st.sidebar.multiselect('filter by market segment', options=self.dataset['market_segment_type'].unique(), default=self.dataset['market_segment_type'].unique())

        self.type_of_meal_plan = st.sidebar.multiselect('filter by type of meal planned', options=self.dataset['type_of_meal_plan'].unique(), default=self.dataset['type_of_meal_plan'].unique())

        self.room_type_reserved = st.sidebar.multiselect('filter by room type reserved', options=self.dataset['room_type_reserved'].unique(), default=self.dataset['room_type_reserved'].unique())


    def my_query(self):
        select_df = self.dataset.query('booking_status == @self.booking_status & arrival_year == @self.arrival_year & market_segment_type == @self.market_segment & type_of_meal_plan == @self.type_of_meal_plan & room_type_reserved == @self.room_type_reserved')
        if len(select_df) < 1:
            select_df = self.dataset
        return select_df
    

    def get_KPIs(self):
        adult_col, child_col, avg_room, special_request = st.columns(4)
        total_avg_room = int(self.my_query()['avg_price_per_room'].sum())
        total_adults = int(self.my_query()['no_of_adults'].sum())
        total_children = int(self.my_query()['no_of_children'].sum())
        total_special_request = int(self.my_query()['no_of_special_requests'].sum())
        with adult_col:
            st.text('Number of adults')
            st.subheader(total_adults)
        with child_col:
            st.text('Number of children')
            st.subheader(total_children)
        with avg_room:
            st.text('Total average price\n per room ')
            st.subheader(f'US $ {total_avg_room}')
        with special_request:
            st.text('Total special requests')
            st.subheader(total_special_request)
        st.markdown('---')

    
    def room_type_plot(self):
        sales_by_room = self.my_query().groupby(by=['room_type_reserved']).sum()[['avg_price_per_room']].sort_values(by='avg_price_per_room')
        fig = px.bar(sales_by_room,
                     x='avg_price_per_room',
                     y=sales_by_room.index,
                     orientation='h',
                     title='Total average price by room type',
                     template='plotly_white',
                     color_discrete_sequence=['#0083B8'] * len(sales_by_room)
                     )
        st.plotly_chart(fig)

    
    def likely_meal_type(self):
        meal_type = self.my_query()['type_of_meal_plan']
        fig = px.bar(meal_type,
                     x=Counter(meal_type).values(),
                     y=meal_type.unique(),
                     orientation='h',
                     title='Prefered meal by number of reservation',
                     template='plotly_white',
                     color_discrete_sequence=['#0083B8'] * len(meal_type)
                     )
        st.plotly_chart(fig)

    
    def likely_market_segment(self):
        market_type = self.my_query()['market_segment_type']
        fig = px.bar(market_type,
                     x=Counter(market_type).values(),
                     y=market_type.unique(),
                     orientation='h',
                     title='Prefered market segment used of reservation',
                     template='plotly_white',
                     color_discrete_sequence=['#0083B8'] * len(market_type)
                     )
        st.plotly_chart(fig)
    

    def main(self):
        self.get_KPIs()
        self.room_type_plot()
        self.likely_market_segment()
        self.likely_meal_type()
        st.subheader('Data set table')
        st.dataframe(self.my_query())



if __name__ == "__main__":
    st.set_page_config(page_title='hotel reservation', page_icon=":hotel:", layout='wide')
    with st.sidebar:
        selected = option_menu("Main Menu", ["Home", 'Problem Statement'], 
        icons=['house', 'gear'], menu_icon="cast", default_index=0)
    if selected == 'Home':
        obj = MyDashBoard()
        obj.main()
    else:
        ProblemStatement()

