import streamlit as st

# from pages.Price_Prediction import Price_Prediction_Page
# from pages.Recommendation_System import Recommendation_System_Page
# from pages.Loan_Eligibility import load_eligibility_Page

# Set page configuration
st.set_page_config(
    page_title="InsightSphere",
    page_icon="🕵️‍♂️",
    layout="wide",
)

st.markdown(
    """
        <style>
               .block-container {
                    padding-top: 2rem;
                    padding-bottom: 0rem;
                    # padding-left: 2rem;
                    # padding-right:2rem;
                }
                .top-margin{
                    margin-top: 4rem;
                    margin-bottom:2rem;
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


# Main page function
def main_page():
    Overview_col, Img_col = st.columns(spec=(1.4, 1), gap="large")

    with Overview_col:

        # Content for main page
        st.markdown(
            "<h1 style='text-align: left; font-size: 65px; '>Ingsights Sphere</h1>",
            unsafe_allow_html=True,
        )
        st.write("")
        st.markdown(
            "<p style='font-size: 22px; text-align: left;'>Customer segmentation is vital for enhancing marketing efficiency and customer satisfaction. By analyzing demographics, interests, and purchasing behavior, businesses can customize marketing strategies for different customer segments. Our app utilizes sophisticated clustering algorithms such as KMeans, DBSCAN, and AGNES to derive valuable insights from your customer data. Whether you're a marketer focusing on specific segments or a strategist refining products, our tool supports informed decision-making. Our application consists of 3 modules⬇️</p>",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div>
                <ul>
                    <li><p style='font-size: 22px; text-align: left;'><em>Dataset Overview:</em> Gain a comprehensive understanding of your customer dataset's structure and variables.Explore key insights into customer demographics, interests, and spending habits at a glance.</p></li>
                    <li><p style='font-size: 22px; text-align: left;'><em>Clustering performance analysis:</em> Evaluate the effectiveness of different clustering algorithms (KMeans, DBSCAN, AGNES) in segmenting your customer data.Compare performance metrics such as silhouette score and cluster stability to determine the most suitable algorithm for your specific dataset.</p></li>
                    <li><p style='font-size: 22px; text-align: left;'><em>Individual Cluster Summary:</em> Dive deep into each segmented cluster to uncover unique traits and behaviors.Explore demographic profiles, purchasing patterns, and preferences of customers within each cluster for targeted marketing strategies.</p></li>
                </ul>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with Img_col:
        st.image("artifacts/Home.png")

        social_col1, social_col2, social_col3, social_col4 = st.columns(
            spec=(1, 1, 1, 1), gap="large"
        )
        with social_col1:
            st.link_button(
                "Github👨‍💻",
                use_container_width=True,
                url="https://github.com/yuvraaj2002",
            )

        with social_col2:
            st.link_button(
                "Linkedin🧑‍💼",
                use_container_width=True,
                url="https://www.linkedin.com/in/yuvraj-singh-a4430a215/",
            )

        with social_col3:
            st.link_button(
                "Twitter🧠",
                use_container_width=True,
                url="https://twitter.com/Singh_yuvraaj1",
            )

        with social_col4:
            st.link_button(
                "Blogs✒️", use_container_width=True, url="https://yuvraj01.hashnode.dev/"
            )


main_page()
