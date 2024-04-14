import streamlit as st
import pickle
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import colorsys


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


# Let's define a function to generate the pastel colors
def generate_pastel_colors(num_colors):
    pastel_colors = []
    for i in range(num_colors):
        # Equally spaced hues
        hue = (i * 1.61803398875) / num_colors  # Using the golden ratio for better distribution

        # Higher saturation for more vibrant colors
        saturation = 0.8

        # Lightness to create pastel effect
        lightness = 0.65  # Adjusted lightness for a wider range of colors
        rgb = colorsys.hls_to_rgb(hue, lightness, saturation)
        pastel_colors.append('#{:02x}{:02x}{:02x}'.format(int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)))

    return pastel_colors


def performance_analysis():
    Visualization_col,description_col = st.columns(spec=(1.5, 1), gap="large")
    with Visualization_col:
        st.markdown(
            "<h1 style='text-align: left; font-size: 50px; '>Performance Analysis</h1>",
            unsafe_allow_html=True,
        )
    with description_col:
        with st.container(border=True):

            st.title("Configuration")
            st.markdown(
                "<p style='font-size: 20px; text-align: left;background-color:#fbe0b4;padding:1rem;'>Companies employing customer segmentation operate under the fact that every customer is different and that their marketing efforts would be better served if they target specific, smaller groups with messages that those consumers would find relevant and lead them to buy something. Companies also hope to gain a deeper understanding of their customers' preferences and needs with the idea of discovering what each segment finds most valuable to more accurately tailor marketing materials toward that segment.</p>",
                unsafe_allow_html=True,
            )
            st.write("***")
            selected_option = st.selectbox(
                "Select Clustering algorithm:",
                ["Partition Based (KMEANS)", "Density Based (DBSCAN)", "Hierarchical (AGNES)"]
            )
            show_plot = st.button("Show 3D Scatter Plot",use_container_width=True)
            if show_plot:
                if selected_option == "Partition Based (KMEANS)":
                    with Visualization_col:
                        pass
                elif selected_option == "Partition Based (KMEANS)":
                    with Visualization_col:
                        pass
                else:
                    with Visualization_col:
                        pass


performance_analysis()