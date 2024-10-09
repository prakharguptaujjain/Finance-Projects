import streamlit as st
import pandas as pd
import yfinance as yf
import shortselling
import no_short_selling
def main():

    # Take input for the number of companies
    num_companies = st.number_input("Enter the number of companies", min_value=2, step=1)

    # Load your DataFrame from an Excel file (Replace 'path/to/your/file.xlsx' with the actual path)
    df = pd.read_csv('yahootickers2.csv')
    df.dropna(inplace=True)  # Drop any NaN values
    df['Name'] = df['Name'].astype(str)  # Ensure 'Name' column is treated as string
    df = df[df['Name'].str[0].str.isalpha()]
    df = df.sort_values(by='Name')  # Sort DataFrame by company names
    sorted_companies = ["Select Company" ] + list(df["Name"])

    # Generate dropdowns for selecting companies
    selected_companies = []
    selected_tickers = []
    for i in range(num_companies):
        company = st.selectbox(f"Select Company {i+1}", options=sorted_companies) # Add more options as needed
        if(company != "Select Company"):
            selected_companies.append(company)
            selected_tickers.append(df.loc[df['Name'] == company, 'Ticker'].iloc[0])  # Retrieve ticker for selected company

    # Organize selected companies and their tickers in two columns
    

    allow_short_selling = st.radio("Allow Short Selling?", ("Yes", "No"))

    stocks = selected_tickers
    if st.button("Submit"):
        try:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("<h5>Selected Companies</h5>", unsafe_allow_html=True)
                for company in selected_companies:
                    st.write(company)

            with col2:
                st.markdown("<h5>Tickers</h5>", unsafe_allow_html=True)
                for ticker in selected_tickers:
                    st.write(ticker)
            
            start_date = pd.Timestamp.now() - pd.DateOffset(months=3)
            end_date = pd.Timestamp.now()

            prices = yf.download(stocks, start=start_date, end=end_date)['Adj Close']
            prices.fillna(prices.mean(), inplace=True)
            
            st.title("Markowitz Optimization Results ") 
            portfolio_optimizer = None 
            if( allow_short_selling == "Yes"):
                portfolio_optimizer = shortselling.PortfolioOptimizer(prices)
            else : 
                portfolio_optimizer = no_short_selling.PortfolioOptimizer(prices)

            
            optimal_weights, optimal_risk, optimal_return = portfolio_optimizer.markowitz_optimization()

            
            st.markdown(f"<h4>Optimal Risk - {round(optimal_risk * 100 , 3 )  } % </h4>" , unsafe_allow_html= True)
            st.markdown(f"<h4>Optimal Return - {round(optimal_return * 100  , 3 ) } % </h4>" , unsafe_allow_html= True)
            st.markdown("<h4>Optimal Weights  </h4>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("<h5>Selected Companies</h5>", unsafe_allow_html=True)
                for company in selected_companies:
                    st.write(company)

            with col2:
                st.markdown("<h5>Tickers</h5>", unsafe_allow_html=True)
                for w in optimal_weights:
                    w = round(w * 100 , 2 )  
                    st.write(str(w) + "%")
            
            returns = portfolio_optimizer.returns
            min_return = returns.mean().min()
            max_return = returns.mean().max()
            max_return = round(max_return  * 100 , 3 )  

           
            fig = portfolio_optimizer.plot_efficient_frontier()
            st.plotly_chart(fig)
        except:
            st.error("An error occurred while processing the data. Please ensure that the data is available and try again.")

            

if __name__ == "__main__":
    main()
