import streamlit as st
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def app():

    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
    background-image: url("https://images.unsplash.com/photo-1501426026826-31c667bdf23d");
    background-size: 180%;
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

    st.markdown("<h1 style='text-align: center; color: purple;'>Demand Forecasting - By Department</h1>", unsafe_allow_html=True)

    st.markdown('This demonstration is using SARIMA - time series method')

    # @st.cache(allow_output_mutation=True)

    def load_file(data_file):
        time.sleep(3)
        df = pd.read_csv(data_file, parse_dates=['Date'], dtype={'Store':str, 'Dept':str})
        return df

    data_file = st.file_uploader('Select Your Sales Data CSV')

    dept = st.selectbox('Choose Department you want to show', (list(np.arange(1,45,1))))

    if data_file is not None:

        fig_dims = (9,7)
        output_df = pd.read_csv('./data/output.csv')

        col1, col2= st.columns(2)

        with col1:
            st.markdown('Show dataframe details')
            sales_df = load_file(data_file)
            st.dataframe(sales_df[sales_df['Store']==str(dept)])
                
        with col2:
            st.markdown('Sales Forecasting by Dept')
            df_store = output_df[output_df['Store']==dept].drop(columns=['Store'])
            idx = df_store.index[0]
            df_store = df_store.T
            df_store['Date'] = df_store.index
            df_store = df_store.reset_index(drop=True)
            df_store = df_store.rename(columns={idx:'Sales'})
            fig, ax = plt.subplots(figsize=fig_dims) # Set up the size of chart
            sns.lineplot(x='Date', y='Sales', data=df_store, err_style=None, ax=ax)
            plt.title('Sales Forecasting by Department')
            st.pyplot(fig)
    else:
        st.markdown('Please browse your input file!')