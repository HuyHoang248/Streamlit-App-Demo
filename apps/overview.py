import streamlit as st
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image


def date_split(dataset):
  dataset['Year'] = dataset.Date.dt.year
  dataset['Month'] = dataset.Date.dt.month
  dataset['Day'] = dataset.Date.dt.day
  dataset['Week_num'] = [item.isocalendar()[1] for item in dataset['Date']]

def app():

    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
    background-image: ("D:\Demand Forecasting\Viet\data\cool-background.png");
    background-size: 100%;
    background-position: top left;
    background-repeat: no-repeat;
    background-attachment: local;
    }}
    [data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
    }}
    </style>
    """
        
    st.markdown(page_bg_img, unsafe_allow_html=True)

    st.image('./image/weave.jpeg')

    st.markdown("<h1 style='text-align: center; color: purple;'>Demand Forecasting - Overview</h1>", unsafe_allow_html=True)

    st.markdown('This demonstration is using SARIMA - time series method')

    @st.cache(allow_output_mutation=True)
    def load_file(data_file):
        time.sleep(3)
        df = pd.read_csv(data_file, parse_dates=['Date'], dtype={'Store':str, 'Dept':str})
        return df
    

    data_file = st.file_uploader('Select Your Sales Data CSV')
    if data_file is not None:
        sales_df = load_file(data_file)

    if data_file is not None:
        

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(label='Accuracy Ratio - Current Month', value='76%', delta='3%')

        with col2:
            st.metric(label='Accuracy Ratio - Last Month', value='73%', delta='-5%')

        with col3:
            st.metric(label='Accuracy Ratio - YTD', value='74%', delta='1%')

        tab1, tab2, tab3 = st.tabs(["Sales Trends", "Model Validation", "Sales Analytics"])

        with tab1:
            
            st.markdown('Plot the weekly sales value to observe the seasonal pattern')
            # Plot the weekly sales value to observe the seasonal pattern
            fig_dims = (12,3)
            fig, ax = plt.subplots(figsize = fig_dims) # Set up the size of chart
            sns.lineplot(x='Date', y='Weekly_Sales', hue = 'Year', data=sales_df, err_style=None, ax=ax) # Plot chart
            plt.title('Sales Trend - 3 years')

            st.pyplot(fig,)

            
            st.markdown('Show dataframe details')
            
            st.dataframe(sales_df)

            st.button('Download')

            # st.download_button(label='Download', data= sales_df, file_name='sales_forecast.csv')
            
                
        
            



        with tab2:
            col1, col2= st.columns(2)

            date_split(sales_df)
            with col1:
                st.write('Sales Comparison')
                fig, ax = plt.subplots(figsize = fig_dims) # Set up the size of chart
                ax = sns.lineplot(x='Week_num', y='Weekly_Sales', hue='Year', data=sales_df, err_style=None, ax=ax)
                plt.title('Sales Comparison - Yearly')
                st.pyplot(fig)
                    
            with col2:
                st.write('Sales Comparison')
                fig, ax = plt.subplots(figsize = fig_dims) # Set up the size of chart
                sns.lineplot(x='Month', y='Weekly_Sales', hue='Year', data=sales_df, err_style=None, ax=ax)
                plt.title('Sales Comparison - Monthly')
                st.pyplot(fig)

            chart_out_df = pd.read_csv('./data/chart_output.csv') 
            validate_df = pd.read_csv('./data/validate.csv')
            chart_out_df.columns = ['Date', 'Weekly_Sales', 'Forecast']

            col1, col2 = st.columns(2)

            with col1:
                st.write('Validation with Testing Data')
                fig, ax = plt.subplots(figsize = fig_dims) # Set up the size of chart
                sns.lineplot(x='Date', y='Weekly_Sales',  data=validate_df, err_style=None, ax=ax)
                sns.lineplot(x='Date', y='forecast',  data=validate_df, err_style=None, ax=ax)
                plt.title('Cross Validate with Testing Data')
                st.pyplot(fig)

            with col2:
                st.write('Sales Forecasting')
                fig, ax = plt.subplots(figsize = fig_dims) # Set up the size of chart
                sns.lineplot(x='Date', y='Weekly_Sales',  data=chart_out_df, err_style=None, ax=ax)
                sns.lineplot(x='Date', y='Forecast',  data=chart_out_df, err_style=None, ax=ax)
                plt.title('Sales Forecasting')
                st.pyplot(fig)

        with tab3:
            image_1 = Image.open('D:\Demand Forecasting\Viet\data\output_bubble.png')
            image_2 = Image.open('D:\Demand Forecasting\Viet\data\output_web.png')
    # st.image(image_1, caption='Sales Forecase by Product')

            col1, col2 = st.columns([0.35, 0.6])

            with col1:
                st.image(image=image_1)

            with col2:
                st.image(image=image_2)
    else:
        st.markdown('Please browse your input file!')




