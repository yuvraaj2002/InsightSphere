import streamlit as st
import pickle
import numpy as np
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


def dataset_desc():
    Overview_col, Visualization_col = st.columns(spec=(1.2, 1), gap="large")
    with Overview_col:
        st.title("Customer Segmentation dataset")

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
