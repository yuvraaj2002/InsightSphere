import streamlit as st
import pickle
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import colorsys
import time


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

def plot_clusters_3d(data, clusters, unique_labels, algo):
    """
    Plots clusters in a 3D scatter plot.

    Parameters:
    data (numpy.ndarray): The data points.
    clusters (numpy.ndarray): Cluster assignments for each data point.
    unique_labels (numpy.ndarray): Unique cluster labels.
    algo (str): Name of the clustering algorithm.

    Returns:
    None
    """

    def generate_pastel_colors(num_colors):
        """Generates pastel colors."""
        colors = []
        for i in range(num_colors):
            hue = (i * 137.508) % 360
            colors.append(tuple([int(j * 255) for j in colorsys.hsv_to_rgb(hue / 360, 0.6, 0.9)]))
        return colors

    # Determine the number of unique clusters
    num_colors = len(unique_labels)

    # Generate pastel colors for clusters
    cluster_colors = generate_pastel_colors(num_colors)

    # Create a 3D scatter plot using Plotly
    fig = make_subplots(specs=[[{"type": "scatter3d"}]])

    # Plot each cluster separately
    for cluster_id in unique_labels:
        cluster_indices = np.where(clusters == cluster_id)[0]
        cluster_data = data[cluster_indices]

        # Using modulo to repeat colors
        cluster_color = cluster_colors[cluster_id % len(cluster_colors)]
        cluster_trace = go.Scatter3d(
            x=cluster_data[:, 0],
            y=cluster_data[:, 1],
            z=cluster_data[:, 2],
            mode='markers',
            marker=dict(size=6, color='rgb' + str(cluster_color)),  # Assigning specific color to each data point
            name=f'Cluster {cluster_id}'
        )
        fig.add_trace(cluster_trace)

    # Set plot title and axis labels
    fig.update_layout(
    title=f'3D Scatter Plot with {algo} Clusters',
    scene=dict(
        xaxis_title='Comp 1',
        yaxis_title='Comp 2',
        zaxis_title='Comp 3'
    ),
    height=750,
    width = 700,
)

    # Display the plot in Streamlit
    st.plotly_chart(fig)


@st.cache_resource
def load_kmeans_clst():
    try:
        # Load the numpy array from the pickle file
        with open("artifacts/clusters_kmeans.pkl", 'rb') as f:
            clusters_kmeans = pickle.load(f)
            return clusters_kmeans
    except FileNotFoundError:
        st.error(f"Error: File not found.")
    except pickle.UnpicklingError:
        st.error("Error: Unable to unpickle the file. It may be corrupted or not a pickle file.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")



@st.cache_resource
def load_ss_data():
    try:
        # Load the numpy array from the pickle file
        with open("artifacts/ss_data.pkl", 'rb') as f:
            ss_data = pickle.load(f)
            return ss_data
    except FileNotFoundError:
        st.error(f"Error: File not found.")
    except pickle.UnpicklingError:
        st.error("Error: Unable to unpickle the file. It may be corrupted or not a pickle file.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")


def download_summary(summary_text):
    """
    Creates a text file with the given summary text and offers download.
    """
    # Generate unique filename
    filename = f"summary_{int(time.time())}.txt"

    # Create the file and write the content
    with open(filename, "w") as file:
        file.write(summary_text)

    # Set content_type and headers
    content_type = "text/plain"
    headers = {
        "Content-Disposition": f"attachment; filename={filename}",
        "Content-type": content_type,
    }

    # Use st.download_button to offer download
    st.download_button(
        "Download Clusters summary",
        data=summary_text,
        file_name=filename,
        mime=content_type,
        use_container_width=True,
    )



def cluster_analysis():
    analysis_col, visualization_col = st.columns(spec=(1.3, 1), gap="large")

    with analysis_col:
        st.markdown(
            "<h1 style='text-align: left; font-size: 45px; '>Clusters Analysis🔎</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='font-size: 20px; text-align: left;'>Among the various algorithms examined, the KMEANS algorithm emerged with the most favorable outcomes. Below, you'll discover a comprehensive outline of each cluster produced by the algorithm. Just click on the expander to unveil the summary. Additionally, you can download the detailed summary in a text file by clicking the button below.</p>",
            unsafe_allow_html=True,
        )
        st.write("")

        # Defining each cluster
        with st.expander("Cluster 0: The Mature Savers"):
            st.markdown(
                "<p style='font-size: 19px; text-align: left;'>Cluster 0 represents a group of individuals with an average age of approximately 52 years. They tend to have a moderate amount of work experience, with an average of around 2.85 years. In terms of spending habits, they exhibit a slightly conservative approach, with an average spending score of around 0.86. This group typically has a family size of around 3 members. Overall, Cluster 0 can be characterized as composed of mature individuals who prioritize saving and maintaining a stable financial situation.</p>",
                unsafe_allow_html=True,
            )
        with st.expander("Cluster 1: The Middle-aged Moderates"):
            st.markdown(
                "<p style='font-size: 19px; text-align: left;'>Cluster 1 consists of individuals with an average age of about 39 years. They have a relatively low amount of work experience, averaging around 2.87 years. In terms of spending behavior, they display a conservative approach, with an average spending score of approximately 0.56. The family size for this cluster is typically around 2 members. Cluster 1 can be seen as comprising middle-aged individuals who adopt a moderate approach to spending and prioritize financial stability.</p>",
                unsafe_allow_html=True,
            )
        with st.expander("Cluster 2: The Elderly Spenders"):
            st.markdown(
                "<p style='font-size: 19px; text-align: left;'>Cluster 2 represents an older demographic, with an average age of approximately 59 years. Despite their age, they still have a modest amount of work experience, averaging around 2.68 years. This group tends to have a slightly higher spending score compared to other clusters, with an average of around 0.85. The family size for this cluster is similar to others, averaging around 2 members. Cluster 2 can be characterized as comprising elderly individuals who are relatively comfortable with spending and maintaining financial independence.</p>",
                unsafe_allow_html=True,
            )
        with st.expander("Cluster 3: The Senior Frugalists"):
            st.markdown(
                "<p style='font-size: 19px; text-align: left;'>Cluster 3 consists of individuals with an average age of about 69 years, making them the oldest cluster. They have a moderate amount of work experience, averaging around 2.70 years. Despite their age, they exhibit a conservative approach to spending, with an average spending score of approximately 1.0. The family size for this cluster is typically around 2 members. Cluster 3 can be seen as comprising senior citizens who prioritize frugality and financial security.</p>",
                unsafe_allow_html=True,
            )
        with st.expander("Cluster 4: The Middle-aged Spenders"):
            st.markdown(
                "<p style='font-size: 19px; text-align: left;'>Cluster 4 consists of individuals with an average age of approximately 39 years, similar to Cluster 1. They have a slightly higher amount of work experience, averaging around 2.97 years. In terms of spending behavior, they exhibit a moderate approach, with an average spending score of approximately 0.50. The family size for this cluster is typically around 2 members. Cluster 4 can be characterized as comprising middle-aged individuals who strike a balance between spending and saving.</p>",
                unsafe_allow_html=True,
            )
        with st.expander("Cluster 5: The Young Thrifts"):
            st.markdown(
                "<p style='font-size: 19px; text-align: left;'>Cluster 5 represents a younger demographic, with an average age of around 29 years. They have a moderate amount of work experience, averaging around 2.76 years. Despite their youth, they display a conservative approach to spending, with an average spending score of approximately 0.19. The family size for this cluster is similar to others, averaging around 2 members. Cluster 5 can be seen as comprising young individuals who prioritize saving and financial planning from an early age.</p>",
                unsafe_allow_html=True,
            )
        with st.expander("Cluster 6: The Elderly Moderate Spenders"):
            st.markdown(
                "<p style='font-size: 19px; text-align: left;'>Cluster 6 consists of older individuals with an average age of approximately 65 years. They have a relatively high amount of work experience, averaging around 2.90 years. In terms of spending behavior, they adopt a moderate approach, with an average spending score of approximately 0.78. The family size for this cluster is typically around 2 members. Cluster 6 can be characterized as comprising elderly individuals who are comfortable with moderate spending and prioritize financial stability in their later years.</p>",
                unsafe_allow_html=True,
            )
        with st.expander("Cluster 7: The Young Spenders"):
            st.markdown(
                "<p style='font-size: 19px; text-align: left;'>Cluster 7 represents a younger demographic, with an average age of about 33 years. They have a moderate amount of work experience, averaging around 3.18 years. This group tends to have a slightly higher spending score compared to other clusters, with an average of around 0.31. The family size for this cluster is similar to others, averaging around 2 members. Cluster 7 can be seen as comprising young individuals who are comfortable with spending and enjoy financial freedom in their youth.</p>",
                unsafe_allow_html=True,
            )

        with st.expander("Cluster 8: The Young Savers"):
            st.markdown(
                "<p style='font-size: 19px; text-align: left;'>Cluster 8 consists of the youngest individuals, with an average age of approximately 20 years. They have a relatively low amount of work experience, averaging around 2.97 years. Despite their age, they exhibit a moderate approach to spending, with an average spending score of around 0.08. The family size for this cluster is typically around 4 members. Cluster 8 can be characterized as comprising young individuals who prioritize saving and financial planning from a young age.</p>",
                unsafe_allow_html=True,
            )


    with visualization_col:
        ss_data = load_ss_data()
        clusters_kmeans = load_kmeans_clst()
        plot_clusters_3d(ss_data, clusters_kmeans, set(clusters_kmeans), "KMEANS")
        summary_text = """
        Cluster 0: The Mature Savers
        Cluster 0 represents a group of individuals with an average age of approximately 52 years. They tend to have a moderate amount of work experience, with an average of around 2.85 years. In terms of spending habits, they exhibit a slightly conservative approach, with an average spending score of around 0.86. This group typically has a family size of around 3 members. Overall, Cluster 0 can be characterized as composed of mature individuals who prioritize saving and maintaining a stable financial situation.

        Cluster 1: The Middle-aged Moderates
        Cluster 1 consists of individuals with an average age of about 39 years. They have a relatively low amount of work experience, averaging around 2.87 years. In terms of spending behavior, they display a conservative approach, with an average spending score of approximately 0.56. The family size for this cluster is typically around 2 members. Cluster 1 can be seen as comprising middle-aged individuals who adopt a moderate approach to spending and prioritize financial stability.

        Cluster 2: The Elderly Spenders
        Cluster 2 represents an older demographic, with an average age of approximately 59 years. Despite their age, they still have a modest amount of work experience, averaging around 2.68 years. This group tends to have a slightly higher spending score compared to other clusters, with an average of around 0.85. The family size for this cluster is similar to others, averaging around 2 members. Cluster 2 can be characterized as comprising elderly individuals who are relatively comfortable with spending and maintaining financial independence.

        Cluster 3: The Senior Frugalists
        Cluster 3 consists of individuals with an average age of about 69 years, making them the oldest cluster. They have a moderate amount of work experience, averaging around 2.70 years. Despite their age, they exhibit a conservative approach to spending, with an average spending score of approximately 1.0. The family size for this cluster is typically around 2 members. Cluster 3 can be seen as comprising senior citizens who prioritize frugality and financial security.

        Cluster 4: The Middle-aged Spenders
        Cluster 4 consists of individuals with an average age of approximately 39 years, similar to Cluster 1. They have a slightly higher amount of work experience, averaging around 2.97 years. In terms of spending behavior, they exhibit a moderate approach, with an average spending score of approximately 0.50. The family size for this cluster is typically around 2 members. Cluster 4 can be characterized as comprising middle-aged individuals who strike a balance between spending and saving.

        Cluster 5: The Young Thrifts
        Cluster 5 represents a younger demographic, with an average age of around 29 years. They have a moderate amount of work experience, averaging around 2.76 years. Despite their youth, they display a conservative approach to spending, with an average spending score of approximately 0.19. The family size for this cluster is similar to others, averaging around 2 members. Cluster 5 can be seen as comprising young individuals who prioritize saving and financial planning from an early age.

        Cluster 6: The Elderly Moderate Spenders
        Cluster 6 consists of older individuals with an average age of approximately 65 years. They have a relatively high amount of work experience, averaging around 2.90 years. In terms of spending behavior, they adopt a moderate approach, with an average spending score of approximately 0.78. The family size for this cluster is typically around 2 members. Cluster 6 can be characterized as comprising elderly individuals who are comfortable with moderate spending and prioritize financial stability in their later years.

        Cluster 7: The Young Spenders
        Cluster 7 represents a younger demographic, with an average age of about 33 years. They have a moderate amount of work experience, averaging around 3.18 years. This group tends to have a slightly higher spending score compared to other clusters, with an average of around 0.31. The family size for this cluster is similar to others, averaging around 2 members. Cluster 7 can be seen as comprising young individuals who are comfortable with spending and enjoy financial freedom in their youth.

        Cluster 8: The Young Savers
        Cluster 8 consists of the youngest individuals, with an average age of approximately 20 years. They have a relatively low amount of work experience, averaging around 2.97 years. Despite their age, they exhibit a moderate approach to spending, with an average spending score of around 0.08. The family size for this cluster is typically around 4 members. Cluster 8 can be characterized as comprising young individuals who prioritize saving and financial planning from a young age.
        """
        download_summary(summary_text)



cluster_analysis()