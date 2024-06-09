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
    df.drop(['Unnamed: 0'],axis=1,inplace=True)
    return df


def plot_pie_charts(df):

    st.title("Univraiate Analysis")
    st.markdown(
        "<p style='font-size: 20px; text-align: left;'>Univariate analysis is a statistical technique that focuses on analyzing the characteristics of a single variable. This type of analysis is crucial as it simplifies understanding by isolating one variable, helps identify patterns and outliers, serves as a foundation for more complex analyses, informs decision-making, and aids in checking data quality. We will look at the distribution of categories using visual tools such as pie charts, bubble plots, and bar plots. Essentially, univariate analysis provides a clear and concise summary of individual variables, making it an essential first step in any data analysis process.</p>",
        unsafe_allow_html=True,
    )

    # Create subplot grid
    fig = ps.make_subplots(
        rows=1, cols=5,
        specs=[[{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}]]
    )

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

    # Update layout for elegance and add titles
    fig.update_layout(
        annotations=[
            dict(text='Gender distribution', x=0.05, y=1.15, font_size=12, showarrow=False, xanchor='center', yanchor='top'),
            dict(text='Ever Married distribution', x=0.25, y=1.15, font_size=12, showarrow=False, xanchor='center', yanchor='top'),
            dict(text='Graduated distribution', x=0.45, y=1.15, font_size=12, showarrow=False, xanchor='center', yanchor='top'),
            dict(text='Spending Score distribution', x=0.65, y=1.15, font_size=12, showarrow=False, xanchor='center', yanchor='top'),
            dict(text='Profession distribution', x=0.85, y=1.15, font_size=12, showarrow=False, xanchor='center', yanchor='top')
        ],
        height=400,
        width=1000,
        showlegend=False,
        legend=dict(x=0.05, y=0.95)
    )

    st.plotly_chart(fig, use_container_width=True)

    age_val_counts = df['Age'].value_counts().reset_index()
    age_val_counts.columns = ['Age', 'Count']

    # Create bubble plot
    fig = px.scatter(age_val_counts, x='Age', y='Count', size='Count',
                     labels={'Age': 'Age', 'Count': 'Count'},
                     title='Bubble plot of Age feature',
                     size_max=50)

    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig, use_container_width=True)

    # Create column layout
    bar_col1, bar_col2 = st.columns((1, 1))

    # Plot bar plot for Work_Experience
    with bar_col1:
        work_exp_counts = df['Work_Experience'].value_counts().reset_index()
        work_exp_counts.columns = ['Work_Experience', 'Count']
        fig5 = px.bar(work_exp_counts, x='Work_Experience', y='Count',
                      labels={'Work_Experience': 'Work Experience', 'Count': 'Count'},
                      title='Distribution of Work Experience', width=400)
        st.plotly_chart(fig5, use_container_width=True)

    # Plot bar plot for Family_Size
    with bar_col2:
        family_size_counts = df['Family_Size'].value_counts().reset_index()
        family_size_counts.columns = ['Family_Size', 'Count']
        fig7 = px.bar(family_size_counts, x='Family_Size', y='Count',
                      labels={'Family_Size': 'Family Size', 'Count': 'Count'},
                      title='Distribution of Family Size', width=400)
        st.plotly_chart(fig7, use_container_width=True)


def Finding_answers(df):
    st.title("MultiVariate Analysis")
    st.markdown(
        "<p style='font-size: 20px; text-align: left;'>Multivariate analysis is a statistical technique used to understand the relationships between multiple variables simultaneously. Unlike univariate analysis, which examines a single variable, multivariate analysis considers the interactions and dependencies among several variables. This approach allows for a more comprehensive understanding of complex data sets and can uncover patterns, trends, and correlations that would be missed when analyzing variables in isolation.In our analysis, we will use multivariate techniques to discover the answers to the following ten questions, employing various visualization charts</p>",
        unsafe_allow_html=True,
    )
    st.write("***")


    # Create columns layout
    col1, col2 = st.columns(spec=(1, 1), gap="large")

    # Question 1: Is there a significant difference in the likelihood of being ever married between males and females?
    with col1:
        st.markdown(
            "<p style='font-size:17px; background-color: #C3E8FF; padding: 0.5rem'><strong>Question 1:</strong> Is there a significant difference in the likelihood of being ever married between males and females?</p>",
            unsafe_allow_html=True)
        fig1 = px.bar(df, x='Gender', y='Ever_Married', color='Gender', title='Ever Married by Gender',
                      labels={'Ever_Married': 'Ever Married Status'})
        st.plotly_chart(fig1)

    # Question 2: How does the age distribution differ between males and females?
    with col1:
        st.markdown(
            "<p style='font-size:17px; background-color: #C3E8FF; padding: 0.5rem'><strong>Question 2:</strong> How does the age distribution differ between males and females?</p>",
            unsafe_allow_html=True)
        fig2 = px.histogram(df, x='Age', color='Gender', title='Age Distribution by Gender',
                            labels={'Age': 'Age', 'count': 'Frequency'})
        st.plotly_chart(fig2)

    # Question 3: Are certain professions more likely to have individuals who are graduated compared to others?
    with col1:
        st.markdown(
            "<p style='font-size:17px; background-color: #C3E8FF; padding: 0.5rem'><strong>Question 3:</strong> Are certain professions more likely to have individuals who are graduated compared to others?</p>",
            unsafe_allow_html=True)
        fig3 = px.bar(df, x='Profession', y='Ever_Married', color='Profession', title='Ever Married by Profession',
                      labels={'Ever_Married': 'Ever Married Status'})
        st.plotly_chart(fig3)

    # Question 4: Is there a typical progression of work experience with age, and does it vary across genders?
    with col1:
        st.markdown(
            "<p style='font-size:17px; background-color: #C3E8FF; padding: 0.5rem'><strong>Question 4:</strong> Is there a typical progression of work experience with age, and does it vary across genders?</p>",
            unsafe_allow_html=True)
        fig4 = px.scatter(df, x='Age', y='Work_Experience', color='Gender', title='Work Experience by Age',
                          labels={'Age': 'Age', 'Work_Experience': 'Work Experience'})
        st.plotly_chart(fig4)

    # Question 5: Do males and females have different spending scores on average?
    with col1:
        st.markdown(
            "<p style='font-size:17px; background-color: #C3E8FF; padding: 0.5rem'><strong>Question 5:</strong> Do males and females have different spending scores on average?</p>",
            unsafe_allow_html=True)
        fig5 = px.box(df, x='Gender', y='Spending_Score', color='Gender', title='Spending Score by Gender',
                      labels={'Spending_Score': 'Spending Score'})
        st.plotly_chart(fig5)

    # Question 6: Is there a difference in family size between individuals who are ever married and those who are not?
    with col2:
        st.markdown(
            "<p style='font-size:17px; background-color: #C3E8FF; padding: 0.5rem'><strong>Question 6:</strong> Is there a difference in family size between individuals who are ever married and those who are not?</p>",
            unsafe_allow_html=True)
        fig6 = px.box(df, x='Ever_Married', y='Family_Size', color='Ever_Married',
                      title='Family Size by Ever Married Status',
                      labels={'Family_Size': 'Family Size'})
        st.plotly_chart(fig6)

    # Question 7: Which profession tends to have more or less work experience on average?
    with col2:
        st.markdown(
            "<p style='font-size:17px; background-color: #C3E8FF; padding: 0.5rem'><strong>Question 7:</strong> Which profession tends to have more or less work experience on average?</p>",
            unsafe_allow_html=True)
        fig7 = px.bar(df, x='Profession', y='Work_Experience', color='Profession',
                      title='Work Experience by Profession',
                      labels={'Work_Experience': 'Work Experience'})
        st.plotly_chart(fig7)

    # Question 8: Is there any correlation between age and spending score?
    with col2:
        st.markdown(
            "<p style='font-size:17px; background-color: #C3E8FF; padding: 0.5rem'><strong>Question 8:</strong> Is there any correlation between age and spending score?</p>",
            unsafe_allow_html=True)
        fig8 = px.scatter(df, x='Age', y='Spending_Score', trendline='ols',
                          title='Correlation between Age and Spending Score',
                          labels={'Age': 'Age', 'Spending_Score': 'Spending Score'})
        st.plotly_chart(fig8)

    # Question 9: Are certain professions more likely to have individuals who are graduated compared to others?
    with col2:
        st.markdown(
            "<p style='font-size:17px; background-color: #C3E8FF; padding: 0.5rem'><strong>Question 9:</strong> Are certain professions more likely to have individuals who are graduated compared to others?</p>",
            unsafe_allow_html=True)
        fig9 = px.bar(df, x='Profession', y='Ever_Married', color='Profession', title='Ever Married by Profession',
                      labels={'Ever_Married': 'Ever Married Status'})
        st.plotly_chart(fig9)

    with col2:
        st.markdown(
            "<p style='font-size:17px; background-color: #C3E8FF; padding: 0.5rem'><strong>Question 10:</strong> How does the age distribution vary between males and females?</p>",
            unsafe_allow_html=True)
        fig10 = px.histogram(df, x='Age', color='Gender', title='Age Distribution by Gender',
                             labels={'Age': 'Age', 'count': 'Frequency'}, marginal='violin')
        st.plotly_chart(fig10)


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
        "<p style='font-size: 20px; text-align: left;'>This module is specifically designed to provide a comprehensive analysis of the features or variables present in our dataset. As part of this analysis, we will conduct two types of analysis: univariate and multivariate. However, before delving into these analyses, it is essential to review some fundamental information about the dataset. Understanding the dataset's structure, including its dimensions, types of variables, and any preliminary statistics, will lay a solid foundation for the detailed univariate and multivariate analyses that follow. By examining both the individual characteristics of each variable and the intricate relationships between multiple variables, we aim to extract meaningful insights and uncover hidden patterns within the data.</p>",
        unsafe_allow_html=True,
    )

    col1, col2= st.columns(spec=(1, 1), gap="small")
    with col1:
        pass
    with col2:
        st.markdown(
            """
            <div style='background-color: #C3E8FF; padding:1rem;'>
                <ul>
                    <h5> Dimensionality Information </h5>
                    <li>There are total 8676 data points in the dataset</li>
                    <li>Total number of features in our dataset</li>
                    <li>There are 4 Nominal features and 1 Ordinal categorical feature</li>
                    <li>There is only single discrete numerical variable</li>
                     <li>In Total there are 2019 duplicate values</li>
                    <li>4 Features have less than 5% Nan values, 1 variable have more than 5% </li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.write("")
        with st.expander("Adjust dataframe configuration",expanded=True):
            genre = st.radio(
                label="Choose an option",
                options=["Show Top 10 Rows", "Show Bottom 10 Rows", "Show Random 10 Rows"],
                label_visibility="collapsed"
            )
            if genre == "Show Top 10 Rows":
                with col1:
                    st.dataframe(df.head(10))
            elif genre == "Show Bottom 10 Rows":
                with col1:
                    st.dataframe(df.tail(10))
            else:
                with col1:
                    st.dataframe(df.sample(10))




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