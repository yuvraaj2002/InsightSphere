import streamlit as st
import pickle
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.markdown(
    """
        <style>
               .block-container {
                    padding-top: 2rem;
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
def load_reduced_data():
    try:
        with open("artifacts/reduce_data.pkl", "rb") as f:
            loaded_arr = pickle.load(f)
        return loaded_arr
    except FileNotFoundError:
        print("Error: File not found.")
        return None
    except Exception as e:
        print("An error occurred:", e)
        return None



@st.cache_resource
def load_df():
    try:
        df = pd.read_csv("artifacts/data.csv")
        return df
    except FileNotFoundError:
        print("Error: File not found.")
        return None
    except Exception as e:
        print("An error occurred:", e)
        return None



def dataset_desc():
    Overview_col, Visualization_col = st.columns(spec=(1.3, 1), gap="large")
    with Overview_col:
        st.markdown(
            "<h1 style='text-align: left; font-size: 50px; '>Customer Segmentation dataset</h1>",
            unsafe_allow_html=True,
        )

        st.markdown(
            "<p style='font-size: 20px; text-align: left;'>Customer segmentation is the practice of dividing a customer base into groups of individuals that are similar in specific ways relevant to marketing, such as age, gender, interests and spending habits.</p>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='font-size: 20px; text-align: left;'>Companies employing customer segmentation operate under the fact that every customer is different and that their marketing efforts would be better served if they target specific, smaller groups with messages that those consumers would find relevant and lead them to buy something. Companies also hope to gain a deeper understanding of their customers' preferences and needs with the idea of discovering what each segment finds most valuable to more accurately tailor marketing materials toward that segment..</p>",
            unsafe_allow_html=True,
        )
        st.write("***")

        df = load_df()
        st.dataframe(df.tail(10))



    with Visualization_col:
        reduced_data = load_reduced_data()
        if reduced_data is not None:
            colors = np.random.rand(len(reduced_data), 3)

            # Create a 3D scatter plot using Plotly
            fig = make_subplots(specs=[[{"type": "scatter3d"}]])

            tsne_trace = go.Scatter3d(
                x=reduced_data[:, 0],
                y=reduced_data[:, 1],
                z=reduced_data[:, 2],
                mode="markers",
                marker=dict(size=6, color=colors),
                name="t-SNE",
            )

            fig.add_trace(tsne_trace)

            # Set plot title and axis labels
            fig.update_layout(
                title="t-SNE Visualization of Dimensionality Reduced Data",
                scene=dict(
                    xaxis_title="Comp 1", yaxis_title="Comp 2", zaxis_title="Comp 3"
                ),
                height=800,
            )

            # Render the plot within Streamlit app
            st.plotly_chart(fig)
        else:
            st.error("Unable to render the visualization")


dataset_desc()
