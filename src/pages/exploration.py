import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pendulum
import numpy as np

@st.cache(allow_output_mutation=True)
def read_data():
    df_logins = pd.read_parquet('./src/data/logins.parquet')
    df_payments = pd.read_parquet('./src/data/payments.parquet')

    df_payments["datetime"] = pd.to_datetime(df_payments.timestamp, unit='ms')
    df_payments["date"] = df_payments.datetime.dt.date
    df_payments["hour"] = df_payments.datetime.apply(lambda x: x.hour)
    df_payments["week"] = df_payments.datetime.apply(lambda x: x.hour)
    df_payments["month"] = df_payments.datetime.apply(lambda x: x.month)
    df_payments["week_of_month"] = df_payments.datetime.apply(lambda x: pendulum.instance(x).week_of_month)

    df_payments["weekday"] = df_payments.datetime.apply(lambda x: x.weekday())
    df_payments["day_of_week"] = df_payments.datetime.apply(lambda x: x.day_name())
    df_payments["week"] = df_payments.datetime.apply(lambda x: 'Workday' if x.weekday() < 5 else 'Weekend')

    df_payments['chargedback'] = df_payments.chargedback.apply(lambda x: 1 if x else 0)
    df_payments['signal'] = df_payments.chargedback.apply(lambda x: 'SIGNAL' if x else 'NON_SIGNAL')

    df_payments['total_payments_account'] = df_payments.groupby('account_id')['id'].transform('nunique')
    df_payments['total_accounts_device'] = df_payments.groupby('device_id')['account_id'].transform('nunique')
    df_payments['total_installation_device'] = df_payments.groupby('device_id')['installation_id'].transform('nunique')
    df_payments['total_value_account'] = df_payments.groupby('account_id')['value'].transform('sum')

    return df_logins, df_payments


def show():
    st.write('# Data Exploration')

    _, df_payments = read_data()

    st.markdown("# Resume")
    colunas = st.columns(3)
    colunas[0].metric("Observation's Begin", pd.to_datetime(df_payments.timestamp.min(), unit='ms').strftime("%Y-%m-%d %H:%M:%S"))
    colunas[2].metric("Observation's End", pd.to_datetime(df_payments.timestamp.max(), unit='ms').strftime("%Y-%m-%d %H:%M:%S"))

    table_size = df_payments.shape[0]
    total_payments = df_payments.id.nunique()

    total_accounts = df_payments.account_id.nunique()
    total_devices = df_payments.device_id.nunique()
    total_installation = df_payments.installation_id.nunique()

    total_chargedback = df_payments.chargedback.sum()
    target_columns = st.columns(5)
    target_columns[0].metric('Table Size', table_size)
    target_columns[1].metric('Number of Payments', total_payments)
    target_columns[2].metric('Payments per Accounts', round(total_payments/total_accounts, 2))
    target_columns[3].metric('Accounts per Devices', round(total_accounts/total_devices, 2))
    target_columns[4].metric('Installation per Device', round(total_installation/total_devices, 2))

    target_columns[0].metric('Max Payments by Account', df_payments.total_payments_account.max())
    target_columns[1].metric('Max Account by Device', df_payments.total_accounts_device.max())
    target_columns[2].metric('Max Installation by Device', df_payments.total_installation_device.max())

    target_columns[3].metric('Number of Chargedbacks', total_chargedback)
    target_columns[4].metric('Chargedback Rate', round(total_chargedback/total_payments*100, 3))

    st.markdown("# Temporal Dimesion")
    colunas = st.columns(4)
    hour_selection = colunas[0].multiselect('Hour', range(0, 24))
    dayweek_selection = colunas[1].multiselect('Day of The Week', ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday'])
    weekmonth_selection = colunas[2].multiselect('Week of The Month', [1, 2, 3, 4, 5, 6])
    month_selection = colunas[3].multiselect('Month', [4, 5, 6, 7, 8, 9])

    date_selection = st.slider(
    "Date",
    min_value = df_payments.date.min(),
    max_value = df_payments.date.max(),
    value=(df_payments.date.min(), df_payments.date.max()))

    with st.expander("Temporal Dimesion", expanded=False):

        df_payments = df_payments[(df_payments.date >= date_selection[0]) & (df_payments.date <= date_selection[1])]

        if len(hour_selection) > 0:
            df_payments = df_payments[df_payments.hour.isin(hour_selection)]

        if len(dayweek_selection) > 0:
            df_payments = df_payments[df_payments.day_of_week.isin(dayweek_selection)]

        if len(weekmonth_selection) > 0:
            df_payments = df_payments[df_payments.week_of_month.isin(weekmonth_selection)]

        if len(month_selection) > 0:
            df_payments = df_payments[df_payments.month.isin(month_selection)]

        df_payments_date = df_payments.groupby(['date', 'signal']).agg(n = ('id', 'nunique')).reset_index()
        df_payments_date = pd.pivot_table(df_payments_date, values='n', index='date', columns='signal').reset_index()
        df_payments_date['signal_rate'] = (df_payments_date['SIGNAL']/df_payments_date['NON_SIGNAL']*100).round(2)
        df_payments_date.fillna(0, inplace=True)

        df_payments_hour = df_payments.groupby(['hour', 'signal']).agg(n = ('id', 'nunique')).reset_index()
        df_payments_hour = pd.pivot_table(df_payments_hour, values='n', index='hour', columns='signal').reset_index()
        df_payments_hour['signal_rate'] = (df_payments_hour['SIGNAL']/df_payments_hour['NON_SIGNAL']*100).round(2)
        df_payments_hour.fillna(0, inplace=True)

        df_payments_weekday = df_payments.groupby(['weekday', 'signal']).agg(n = ('id', 'nunique')).reset_index()
        df_payments_weekday = pd.pivot_table(df_payments_weekday, values='n', index='weekday', columns='signal').reset_index()
        df_payments_weekday['signal_rate'] = (df_payments_weekday['SIGNAL']/df_payments_weekday['NON_SIGNAL']*100).round(2)
        df_payments_weekday.fillna(0, inplace=True)

        df_payments_month = df_payments.groupby(['month', 'signal']).agg(n = ('id', 'nunique')).reset_index()
        df_payments_month = pd.pivot_table(df_payments_month, values='n', index='month', columns='signal').reset_index()
        df_payments_month['signal_rate'] = (df_payments_month['SIGNAL']/df_payments_month['NON_SIGNAL']*100).round(2)
        df_payments_month.fillna(0, inplace=True)

        df_payments_workday = df_payments.groupby(['week', 'signal']).agg(n = ('id', 'nunique'),
                                                                        total_days = ('weekday', 'nunique')).reset_index()
        df_payments_workday = pd.pivot_table(df_payments_workday, values='n', index='week', columns='signal').reset_index()
        df_payments_workday['signal_rate'] = (df_payments_workday['SIGNAL']/df_payments_workday['NON_SIGNAL']*100).round(2)
        df_payments_workday.fillna(0, inplace=True)
                                                  
        df_payments_weekmonth = df_payments.groupby(['week_of_month', 'signal']).agg(n = ('id', 'nunique')).reset_index()
        df_payments_weekmonth = pd.pivot_table(df_payments_weekmonth, values='n', index='week_of_month', columns='signal').reset_index()
        df_payments_weekmonth['signal_rate'] =(df_payments_weekmonth['SIGNAL']/df_payments_weekmonth['NON_SIGNAL']*100).round(2)
        df_payments_weekmonth.fillna(0, inplace=True)

        st.markdown("## Date")
        fig_hour = px.bar(df_payments_date, x="date", y="signal_rate", text="signal_rate")
        fig_hour.update_traces(textfont_size=14)
        st.plotly_chart(fig_hour, use_container_width=True)
        
        st.markdown("## Hour")
        fig_hour = px.bar(df_payments_hour, x="hour", y="signal_rate", text="signal_rate")
        fig_hour.update_traces(textfont_size=14)
        st.plotly_chart(fig_hour, use_container_width=True)
        
        st.markdown("## Day")
        fig_weekday = px.bar(df_payments_weekday, x="weekday", y="signal_rate", text="signal_rate")
        fig_weekday.update_traces(textfont_size=14)
        st.plotly_chart(fig_weekday, use_container_width=True)

        st.markdown("## Week")
        fig_weekmonth = px.bar(df_payments_weekmonth, x="week_of_month", y="signal_rate", text="signal_rate")
        fig_weekmonth.update_traces(textfont_size=14)
        st.plotly_chart(fig_weekmonth, use_container_width=True)

        st.markdown("## Workday")
        fig_workday = px.bar(df_payments_workday, x="week", y="signal_rate", text_auto=True)
        fig_workday.update_traces(textfont_size=14)
        st.plotly_chart(fig_workday, use_container_width=True)

        st.markdown("## Month")
        fig_month = px.bar(df_payments_month, x="month", y="signal_rate", text="signal_rate")
        fig_month.update_traces(textfont_size=14)
        st.plotly_chart(fig_month, use_container_width=True)


    st.markdown("# Non-Temporal Dimesion")
    @st.cache(allow_output_mutation=True)
    def bucketize_data(df_payments, interval):

        bins = [0, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, float('inf')]
        labels = ['00-0_1', '01-1_2', '02-2_4', '03-4_8', '04-8_16', '05-16_32',
                '06-32_64', '07-64_128', '08-128-256', '09-256-512', '10-512-1024', '11-1024-Inf']
        
        bins_value = [0, 50, 100, 250, 500, 1000, 2500, 5000, 10000, 25000, 50000, 100000, float('inf')]
        labels_values = ['00-0_50', '01-50_100', '02-100_250', '03-250_500', '04-500_1000', '05-1000_2500',
                '06-2500_5000', '07-5000_10000', '08-10000-25000', '09-25000-50000', '10-50000-100000', '11-100000-Inf']
        
        df_payments['fx_payments_account'] = pd.cut(df_payments['total_payments_account'], bins=bins, labels=labels)
        df_payments['fx_accounts_device'] = pd.cut(df_payments['total_accounts_device'], bins=bins, labels=labels)
        df_payments['fx_installation_device'] = pd.cut(df_payments['total_installation_device'], bins=bins, labels=labels)
        df_payments['fx_value'] = pd.cut(df_payments['total_value_account'], bins=bins_value, labels=labels_values)
        
        return df_payments, labels, labels_values

    df_payments, labels, labels_values = bucketize_data(df_payments, 30)

    colunas = st.columns(4)

    colunas = st.columns(4)
    min_payment = colunas[0].number_input('Min Payments by Account', value=0)
    max_payment = colunas[0].number_input('Max Payments by Account', value=df_payments.total_payments_account.max())
    fx_payment_selection = colunas[0].multiselect('Payments by Account', labels)

    min_account = colunas[1].number_input('Min Accounts by Device', value=0)
    max_account = colunas[1].number_input('Max Accounts by Device', value=df_payments.total_accounts_device.max())
    fx_accounts_selection = colunas[1].multiselect('Accounts by Device', labels)

    min_installation = colunas[2].number_input('Min Installations by Device', value=0)
    max_installation = colunas[2].number_input('Max Installations by Device', value=df_payments.total_installation_device.max())
    fx_installation_selection = colunas[2].multiselect('Installations by Device', labels)

    min_value = colunas[3].number_input('Min Transaction Value', value=0)
    max_value = colunas[3].number_input('Max Transaction Value', value=df_payments.total_value_account.max())
    fx_value_selection = colunas[3].multiselect('Transaction Value', labels_values)
    
    if len(fx_payment_selection) > 0:
        df_payments = df_payments[df_payments.fx_payments_account.isin(fx_payment_selection)]
    df_payments = df_payments[(df_payments.total_payments_account >= min_payment) & (df_payments.total_payments_account <= max_payment)]

    if len(fx_accounts_selection) > 0:
        df_payments = df_payments[df_payments.fx_accounts_device.isin(fx_accounts_selection)]
    df_payments = df_payments[(df_payments.total_accounts_device >= min_account) & (df_payments.total_accounts_device <= max_account)]

    if len(fx_installation_selection) > 0:
        df_payments = df_payments[df_payments.fx_installation_device.isin(fx_installation_selection)]
    df_payments = df_payments[(df_payments.total_installation_device >= min_installation) & (df_payments.total_installation_device <= max_installation)]

    if len(fx_value_selection) > 0:
        df_payments = df_payments[df_payments.fx_value.isin(fx_value_selection)]

    df_payments = df_payments[(df_payments.total_value_account >= min_value) & (df_payments.total_value_account <= max_value)]

    with st.expander("Non-Temporal Dimesion", expanded=True):
    
        st.markdown("## Transaction By Account")
        colunas = st.columns(2)
        fig_payments = go.Figure()
        fig_payments.add_trace(go.Histogram(x=df_payments[df_payments.signal == 'SIGNAL'].total_payments_account, name='SIGNAL', marker={'color': '#DB4437'}))
        fig_payments.add_trace(go.Histogram(x=df_payments[df_payments.signal == 'NON_SIGNAL'].total_payments_account, name='NON_SIGNAL', marker={'color': '#4285F4'}))
        fig_payments.update_layout(barmode='overlay')
        fig_payments.update_traces(opacity=0.75)
        colunas[0].plotly_chart(fig_payments, use_container_width=True)

        df_transaction_account = df_payments.groupby(['fx_payments_account', 'signal']).agg(n = ('id', 'nunique')).reset_index()
        df_transaction_account = pd.pivot_table(df_transaction_account, values='n', index='fx_payments_account', columns='signal').reset_index()
        df_transaction_account['signal_rate'] = (df_transaction_account['SIGNAL']/df_transaction_account['NON_SIGNAL']*100).round(2)
        df_transaction_account.fillna(0, inplace=True)
        df_transaction_account = df_transaction_account.set_index('fx_payments_account')
        colunas[1].table(df_transaction_account)

        st.markdown("## Accounts By Device")
        colunas = st.columns(2)
        fig_accounts = go.Figure()
        fig_accounts.add_trace(go.Histogram(x=df_payments[df_payments.signal == 'SIGNAL'].total_accounts_device, name='SIGNAL', marker={'color': '#DB4437'}))
        fig_accounts.add_trace(go.Histogram(x=df_payments[df_payments.signal == 'NON_SIGNAL'].total_accounts_device, name='NON_SIGNAL', marker={'color': '#4285F4'}))
        fig_accounts.update_layout(barmode='overlay')
        fig_accounts.update_traces(opacity=0.75)
        colunas[0].plotly_chart(fig_accounts, use_container_width=True)

        df_account_device = df_payments.groupby(['fx_accounts_device', 'signal']).agg(n = ('id', 'nunique')).reset_index()
        df_account_device = pd.pivot_table(df_account_device, values='n', index='fx_accounts_device', columns='signal').reset_index()
        df_account_device['signal_rate'] = (df_account_device['SIGNAL']/df_account_device['NON_SIGNAL']*100).round(2)
        df_account_device.fillna(0, inplace=True)
        df_account_device = df_account_device.set_index('fx_accounts_device')
        colunas[1].table(df_account_device)

        st.markdown("## Installation By Device")
        colunas = st.columns(2)
        fig_installation = go.Figure()
        fig_installation.add_trace(go.Histogram(x=df_payments[df_payments.signal == 'SIGNAL'].total_installation_device, name='SIGNAL', marker={'color': '#DB4437'}))
        fig_installation.add_trace(go.Histogram(x=df_payments[df_payments.signal == 'NON_SIGNAL'].total_installation_device, name='NON_SIGNAL', marker={'color': '#4285F4'}))
        fig_installation.update_layout(barmode='overlay')
        fig_installation.update_traces(opacity=0.75)
        colunas[0].plotly_chart(fig_installation, use_container_width=True)

        df_installation_device = df_payments.groupby(['fx_installation_device', 'signal']).agg(n = ('id', 'nunique')).reset_index()
        df_installation_device = pd.pivot_table(df_installation_device, values='n', index='fx_installation_device', columns='signal').reset_index()
        df_installation_device['signal_rate'] = (df_installation_device['SIGNAL']/df_installation_device['NON_SIGNAL']*100).round(2)
        df_installation_device.fillna(0, inplace=True)
        df_installation_device = df_installation_device.set_index('fx_installation_device')
        colunas[1].table(df_installation_device)

        st.markdown("## Value By Account")
        colunas = st.columns(2)
        fig_value = go.Figure()
        fig_value.add_trace(go.Histogram(x=df_payments[df_payments.signal == 'SIGNAL'].total_value_account, name='SIGNAL', marker={'color': '#DB4437'}))
        fig_value.add_trace(go.Histogram(x=df_payments[df_payments.signal == 'NON_SIGNAL'].total_value_account, name='NON_SIGNAL', marker={'color': '#4285F4'}))
        fig_value.update_layout(barmode='overlay')
        fig_value.update_traces(opacity=0.75)
        colunas[0].plotly_chart(fig_value, use_container_width=True)

        df_value_account = df_payments.groupby(['fx_value', 'signal']).agg(n = ('id', 'nunique')).reset_index()
        df_value_account = pd.pivot_table(df_value_account, values='n', index='fx_value', columns='signal').reset_index()
        df_value_account['signal_rate'] = (df_value_account['SIGNAL']/df_value_account['NON_SIGNAL']*100).round(2)
        df_value_account.fillna(0, inplace=True)
        df_value_account = df_value_account.set_index('fx_value')
        colunas[1].table(df_value_account)

