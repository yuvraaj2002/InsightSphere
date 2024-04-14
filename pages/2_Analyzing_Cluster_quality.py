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

@st.cache_resource
def load_minmax_data():
    try:
        # Load the numpy array from the pickle file
        with open("artifacts/minmax_data.pkl", 'rb') as f:
            minimax_data = pickle.load(f)
            return minimax_data
    except FileNotFoundError:
        st.error(f"Error: File not found.")
    except pickle.UnpicklingError:
        st.error("Error: Unable to unpickle the file. It may be corrupted or not a pickle file.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

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
def load_dbscan_clst():
    try:
        # Load the numpy array from the pickle file
        with open("artifacts/clusters_dbscan.pkl", 'rb') as f:
            clusters_dbscan = pickle.load(f)
            return clusters_dbscan
    except FileNotFoundError:
        st.error(f"Error: File not found.")
    except pickle.UnpicklingError:
        st.error("Error: Unable to unpickle the file. It may be corrupted or not a pickle file.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

@st.cache_resource
def load_agnes_clst():
    try:
        # Load the numpy array from the pickle file
        with open("artifacts/clusters_agnes.pkl", 'rb') as f:
            clusters_agnes = pickle.load(f)
            return clusters_agnes
    except FileNotFoundError:
        st.error(f"Error: File not found.")
    except pickle.UnpicklingError:
        st.error("Error: Unable to unpickle the file. It may be corrupted or not a pickle file.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

def plot_metrics():

    values = [0.38, 0.25, 0.29]
    labels = ['KMeans', 'DBSCAN', 'AGNES']

    # Creating bar plot
    fig = go.Figure(data=[go.Bar(x=labels, y=values)])

    # Adding title and axis labels
    fig.update_layout(title='Bar Plot of Silhouette scores', xaxis_title='Algorithms', yaxis_title='Scores')

    # Reduce the width of the plot
    fig.update_layout(width=600,height=400)  # Adjust the width as needed

    # Display the plot in Streamlit with specified height
    st.plotly_chart(fig, use_container_width=True)


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
        height=500,
        width=1000
    )

    # Display the plot in Streamlit
    st.plotly_chart(fig)


def performance_analysis():
    Visualization_col,description_col = st.columns(spec=(1.5, 1), gap="large")
    with Visualization_col:
        st.markdown(
            "<h1 style='text-align: left; font-size: 50px; '>Performance Analysis</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='font-size: 19px; text-align: left;'>Clusters are groups of data points that are similar to each other within the group and dissimilar to data points in other groups. The goal of clustering is to identify inherent structures within data without the need for labeled outcomes. By partitioning data into clusters, it becomes easier to understand the underlying patterns, associations, or groupings within the dataset.</p>",
            unsafe_allow_html=True,
        )

        st.markdown(
            "<p style='font-size: 19px; text-align: left;'>Evaluating clusters is critical for validating results, comparing algorithms, ensuring interpretability, supporting decision-making, and improving models. The silhouette score, a widely used metric, measures the similarity of data points within their clusters compared to neighboring clusters. Ranging from -1 to 1, a higher score indicates better-defined clusters, while a lower score suggests overlapping or poorly separated clusters. By assessing cluster quality, one can make informed decisions about the suitability of clustering techniques for their data and derive actionable insights from the resulting groups.</p>",
            unsafe_allow_html=True,
        )

    with description_col:
        with st.container(border=True):
            st.markdown(
                "<p style='font-size: 19px; text-align: left;background-color:#fbe0b4;padding:1rem;'>Explore clustering algorithms—K-Means, DBSCAN, and AGNES—by selecting one from the dropdown menu and clicking Visualize to see how each partitions the data. This interactive exploration reveals unique cluster structures formed by each algorithm, providing valuable insights into their behaviors.</p>",
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
                        ss_data = load_ss_data()
                        clusters_kmeans = load_kmeans_clst()
                        plot_clusters_3d(ss_data,clusters_kmeans,set(clusters_kmeans),"KMEANS")
                elif selected_option == "Density Based (DBSCAN)":
                    with Visualization_col:
                        minmax_data = load_minmax_data()
                        clusters_dbscan = load_dbscan_clst()
                        plot_clusters_3d(minmax_data, clusters_dbscan, set(clusters_dbscan), "DBSCAN")
                else:
                    with Visualization_col:
                        ss_data = load_ss_data()
                        clusters_agnes = load_agnes_clst()
                        plot_clusters_3d(ss_data, clusters_agnes, set(clusters_agnes), "AGNES")

            plot_metrics()


performance_analysis()