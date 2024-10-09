import streamlit as st
import app1 , app2 , app3
def main():
    st.title("Portfolio Optimizer")

    # Sidebar
    st.sidebar.title("Navigation")
    option = st.sidebar.selectbox("Go to", ["Home", "Portfolio Optimization", "Portfolio Optimization with Target Return", "Portfolio Optimization for Risk Tolerance"])

    if option == "Home":
        st.write("Welcome to the Portfolio Optimization App!")
        st.write("Please select an option from the sidebar to get started.")
        
        st.markdown("---")
        
        st.header("Introduction")
        st.write("""
        Welcome to the Portfolio Optimization App! This app provides tools for optimizing investment portfolios based on various criteria such as maximizing returns, achieving target returns, or managing risk tolerance levels.
        """)
        
        # st.image("https://example.com/your-image.png", caption="Image Caption", use_column_width=True)

        st.markdown("---")
        
        st.header("How to Use")
        st.write("""
        To get started, simply navigate through the sidebar options to access different optimization tools:
        
        - **Portfolio Optimization**: Optimize your portfolio to maximize returns.
        - **Target Return Optimization**: Optimize your portfolio to achieve a specific target return.
        - **Risk Tolerance Optimization**: Optimize your portfolio based on your risk tolerance level.
        
        Explore each option to learn more and utilize the tools provided for informed investment decisions.
        """)

        st.markdown("---")  

    elif option == "Portfolio Optimization":
        st.write("Portfolio Optimization")
        app1.main()
        # Add your portfolio optimization content here
    elif option == "Portfolio Optimization with Target Return":
        st.write("Portfolio Optimization for Target Return")
        app2.main()
        # Add your target return optimization content here
    elif option == "Portfolio Optimization for Risk Tolerance":
        st.write("Portfolio Optimization for Given Risk Tolerance Level")
        app3.main()
        # Add your risk tolerance optimization content here

if __name__ == "__main__":
    main()
