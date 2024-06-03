import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.subplots as ps
import plotly.express as px
from plotly.subplots import make_subplots
import statsmodels.api as sm
import plotly.figure_factory as ff


st.markdown(
    """
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    # padding-left: 2rem;
                    # padding-right:2rem;
                }
                .block-button{
                    padding: 10px; 
                    width: 100%;
                    background-color: #c4fcce;
                }
        </style>
        """,
    unsafe_allow_html=True,
)


@st.cache_resource
def load_dataframe():
    df = pd.read_csv('artifacts/data.csv')
    return df


def plot_pie_charts(df):

    st.title("Univraiate Analysis")
    st.markdown(
        "<p style='font-size: 20px; text-align: left;'>In clustering algorithms like K-means, determining the number of clusters beforehand is crucial, unlike in density or hierarchical clustering methods. To address this, we employ two techniques: the Elbow Method and the Silhouette Method.The Elbow Method is a graphical approach where we plot the within-cluster sum of squares (WCSS) against the number of clusters. The point where the rate of decrease sharply changes represents a suitable value for k.On the other hand, the Silhouette Method calculates the silhouette score for each data point, measuring how similar it is to its own cluster compared to other clusters. This method provides a concise graphical representation of how well each data point lies within its cluster.</p>",
        unsafe_allow_html=True,
    )

    # Create subplot grid
    fig = ps.make_subplots(rows=1, cols=5,
                           specs=[[{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'},{'type': 'domain'}]])

    # Plotting pie charts
    fig.add_trace(
        go.Pie(labels=df['Gender'].value_counts().index, values=df['Gender'].value_counts().values, name='Gender',
               showlegend=True, legendgroup='group1'),
        row=1, col=1
    )

    fig.add_trace(
        go.Pie(labels=df['Ever_Married'].value_counts().index, values=df['Ever_Married'].value_counts().values,
               name='Ever Married', showlegend=True, legendgroup='group2'),
        row=1, col=2
    )

    fig.add_trace(
        go.Pie(labels=df['Graduated'].value_counts().index, values=df['Graduated'].value_counts().values,
               name='Graduated', showlegend=True, legendgroup='group3'),
        row=1, col=3
    )

    fig.add_trace(
        go.Pie(labels=df['Spending_Score'].value_counts().index, values=df['Spending_Score'].value_counts().values,
               name='Spending Score', showlegend=True, legendgroup='group4'),
        row=1, col=4
    )

    fig.add_trace(
        go.Pie(labels=df['Profession'].value_counts().index, values=df['Profession'].value_counts().values,
               name='Profession', showlegend=True, legendgroup='group5'),
        row=1, col=5
    )

    # Update layout for elegance
    fig.update_layout(
        title='',
        height=400,
        width=800,
        showlegend=False,
        legend=dict(x=0.05, y=0.95)
    )
    st.plotly_chart(fig, use_container_width=True)


def Finding_answers(df):
    st.title("MultiVariate Analysis")
    st.markdown(
        "<p style='font-size: 20px; text-align: left;'>In clustering algorithms like K-means, determining the number of clusters beforehand is crucial, unlike in density or hierarchical clustering methods. To address this, we employ two techniques: the Elbow Method and the Silhouette Method.The Elbow Method is a graphical approach where we plot the within-cluster sum of squares (WCSS) against the number of clusters. The point where the rate of decrease sharply changes represents a suitable value for k.On the other hand, the Silhouette Method calculates the silhouette score for each data point, measuring how similar it is to its own cluster compared to other clusters. This method provides a concise graphical representation of how well each data point lies within its cluster.</p>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(spec=(1,1), gap="large")
    with col1:
        # Question 1: Is there a significant difference in the likelihood of being ever married between males and females?
        with st.expander(
                "Question 1: Is there a significant difference in the likelihood of being ever married between males and females?",expanded=True):
            fig = px.bar(df, x='Gender', y='Ever_Married', color='Gender', title='Ever Married by Gender',
                         labels={'Ever_Married': 'Ever Married Status'})
            st.plotly_chart(fig)

        # Question 2: How does the age distribution differ between males and females?
        with st.expander("Question 2: How does the age distribution differ between males and females?",expanded=True):
            fig = px.histogram(df, x='Age', color='Gender', title='Age Distribution by Gender',
                               labels={'Age': 'Age', 'count': 'Frequency'})
            st.plotly_chart(fig)

        # Question 3: Are certain professions more likely to have individuals who are graduated compared to others?
        with st.expander(
                "Question 3: Are certain professions more likely to have individuals who are graduated compared to others?",expanded=True):
            fig = px.bar(df, x='Profession', y='Graduated', color='Profession', title='Graduation Status by Profession',
                         labels={'Graduated': 'Graduated Status'})
            st.plotly_chart(fig)

        # Question 4: Is there a typical progression of work experience with age, and does it vary across genders?
        with st.expander(
                "Question 4: Is there a typical progression of work experience with age, and does it vary across genders?",expanded=True):
            fig = px.scatter(df, x='Age', y='Work_Experience', color='Gender', title='Work Experience by Age',
                             labels={'Age': 'Age', 'Work_Experience': 'Work Experience'})
            st.plotly_chart(fig)

        # Question 5: Do males and females have different spending scores on average?
        with st.expander("Question 5: Do males and females have different spending scores on average?",expanded=True):
            fig = px.box(df, x='Gender', y='Spending_Score', color='Gender', title='Spending Score by Gender',
                         labels={'Spending_Score': 'Spending Score'})
            st.plotly_chart(fig)

    with col2:
        # Question 6: Is there a difference in family size between individuals who are ever married and those who are not?
        with st.expander(
                "Question 6: Is there a difference in family size between individuals who are ever married and those who are not?",expanded=True):
            fig = px.box(df, x='Ever_Married', y='Family_Size', color='Ever_Married',
                         title='Family Size by Ever Married Status',
                         labels={'Family_Size': 'Family Size'})
            st.plotly_chart(fig)

        # Question 7: Which profession tends to have more or less work experience on average?
        with st.expander("Question 7: Which profession tends to have more or less work experience on average?",expanded=True):
            fig = px.bar(df, x='Profession', y='Work_Experience', color='Profession',
                         title='Work Experience by Profession',
                         labels={'Work_Experience': 'Work Experience'})
            st.plotly_chart(fig)

        # Question 8: Is there any correlation between age and spending score?
        with st.expander("Question 8: Is there any correlation between age and spending score?",expanded=True):
            fig = px.scatter(df, x='Age', y='Spending_Score', trendline='ols',
                             title='Correlation between Age and Spending Score',
                             labels={'Age': 'Age', 'Spending_Score': 'Spending Score'})
            st.plotly_chart(fig)

        # Question 9: Are certain professions more likely to have individuals who are graduated compared to others?
        with st.expander(
                "Question 9: Are certain professions more likely to have individuals who are graduated compared to others?",expanded=True):
            fig = px.bar(df, x='Profession', y='Graduated', color='Profession', title='Graduated Status by Profession',
                         labels={'Graduated': 'Graduated Status'})
            st.plotly_chart(fig)

        # Question 10: How does the age distribution vary between males and females?
        with st.expander("Question 10: How does the age distribution vary between males and females?",expanded=True):
            fig = px.histogram(df, x='Age', color='Gender', title='Age Distribution by Gender',
                               labels={'Age': 'Age', 'count': 'Frequency'}, marginal='violin')
            st.plotly_chart(fig)


def cluster_analysis_visualization():
    st.markdown(
        "<p style='font-size: 20px; text-align: left;'>In clustering algorithms like K-means, determining the number of clusters beforehand is crucial, unlike in density or hierarchical clustering methods. To address this, we employ two techniques: the Elbow Method and the Silhouette Method.The Elbow Method is a graphical approach where we plot the within-cluster sum of squares (WCSS) against the number of clusters. The point where the rate of decrease sharply changes represents a suitable value for k.On the other hand, the Silhouette Method calculates the silhouette score for each data point, measuring how similar it is to its own cluster compared to other clusters. This method provides a concise graphical representation of how well each data point lies within its cluster.</p>",
        unsafe_allow_html=True,
    )
    st.write("")
    col1, col2 = st.columns(spec=(1, 1), gap="large")
    with col1:
        st.image('artifacts/Elbow_method.png')
    with col2:
        st.image('artifacts/Silhoutte_method.png')


def display_basic_details(df):
    st.markdown(
        "<p style='font-size: 20px; text-align: left;'>In clustering algorithms like K-means, determining the number of clusters beforehand is crucial, unlike in density or hierarchical clustering methods. To address this, we employ two techniques: the Elbow Method and the Silhouette Method.The Elbow Method is a graphical approach where we plot the within-cluster sum of squares (WCSS) against the number of clusters. The point where the rate of decrease sharply changes represents a suitable value for k.On the other hand, the Silhouette Method calculates the silhouette score for each data point, measuring how similar it is to its own cluster compared to other clusters. This method provides a concise graphical representation of how well each data point lies within its cluster.</p>",
        unsafe_allow_html=True,
    )

    col1, col2,col3 = st.columns(spec=(1, 1, 1), gap="large")
    with col1:
        st.markdown(
            """
            <div style='background-color: #FBE0B4; padding:1rem;'>
                <ul>
                    <h5> Dimensionality Information </h5>
                    <li>Total Number of data points in the dataset</li>
                    <li>Total number of features in our dataset</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            """
            <div style='background-color: #FBE0B4; padding:1rem;'>
                <ul>
                    <h5> Dimensionality Information </h5>
                    <li>Total Number of data points in the dataset</li>
                    <li>Total number of features in our dataset</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            """
            <div style='background-color: #FBE0B4; padding:1rem;'>
                <ul>
                    <h5> Dimensionality Information </h5>
                    <li>Total Number of data points in the dataset</li>
                    <li>Total number of features in our dataset</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )




def visualizations():

    # Calling the functions for loading the dataset and also the basic details
    df = load_dataframe()
    st.title("Introductory Information")
    display_basic_details(df)
    st.write("***")

    # Calling function to plot charts for the univariate analysis
    plot_pie_charts(df)
    st.write("***")


    Finding_answers(df)
    st.write("***")

    st.title("Analysis for Clustering")
    cluster_analysis_visualization()
    st.write("***")


visualizations()