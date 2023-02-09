import streamlit as st
import pandas as pd

def show():
    st.write('# Chargeback Fraud Detection')

    st.write('### Definition')

    st.markdown("""
    **Chargeback fraud** occurs when consumers fraudulently attempt to **secure a refund** using the chargeback process. Instead of contacting the merchant directly for a refund, consumers dispute the transaction with their bank, thus initiating the chargeback process. Consumers will falsely complain that the product they ordered was delivered defective or not at all, that they did not authorize the transaction, or that they had requested the cancellation of a recurring transaction and were charged anyway. Whatever reason they give, chargeback fraud is when the real reason is something else entirely
    (https://www.cardinalcommerce.com/fraud/chargebacks/what-is-chargeback-fraud)
    """)

    st.write("### Example")

    st.markdown("""
    A consumer uses the iFood's app for a delivery in a different location than where he/she lives at the moment. Lets say for an example that this consumer order 2 sushi combos (\$200) to be delivered to a friends house. However, a little after the delivery is concluded with success the same consumer ask its cardhoulder for a refund claiming that someone took over its account and ordered in his place.
    Depending on the consumers's cardholder, the $200 will be refunded, eventhough it was a chargeback fraud. It would be really important for the iFood's app to known the consumer's location during its daily journey to be able to detect such chargeback frauds.

    If such data was available at the time of the order and the same consumer have already been many times in the order locations then a detector (model or specialist) would be able to label dispute such chargeback fraud.
    """)

    st.write("### Problem Mapping")
    st.write("#### Rare Event Detection (Temporal)")
    st.markdown("""
    **Types**:
    * **full length supervised time series classification**: detect if a rare event occured in a fixed period of time.
    * **early supervised time-series classification**: detect if a rare event will occur in the next period of time to be able to fixed or countermeasure.
    * **unbalanced non-temporal classification**: in some rare event detection applications, instances are transformed without considering the time dimension (similar to anomaly detection). 

    **Objective**: classifify the rare class
    
    **Metric**: AUC, Recall of the rare class

    **Techniques**:
    * Rare event logistic regression
    * Kullback-Leibler divergence
    * LSTMs
    * SVMs
    """)

    st.write("#### Anomaly Detection (Non-Temporal)")
    st.markdown("""
    **Types**: **highly unbalanced supervised classification**
    
    **Objective**: classifify the anomaly classes
    
    **Metric**: AUC, recall of the rare class

    **Classification Techniques**: popular supervised classifiers
    """)

    st.write("#### Honorable Mentions")

    st.markdown("""
    * **Novelty detection**: supervised classification task in which only one class is available to learn the classification model
    * **Outlier detection**: unsupervised classification of temporal or non-temporal data with the objective of finding the instance that highly deviates from others.
    """)