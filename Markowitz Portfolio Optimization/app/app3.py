import streamlit as st
import pandas as pd
import yfinance as yf
import shortselling , no_short_selling

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
    risk_tolerance =  target_return = st.number_input("Enter the Risk Tolerance Level ", value=0.0 )

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
    
            prices = prices = yf.download(stocks, start=start_date, end=end_date)['Adj Close']
            prices.fillna(prices.mean(), inplace=True)
            # st.title("Markowitz Optimization Results ") 
            portfolio_optimizer = None 
            if( allow_short_selling == "Yes"):
                portfolio_optimizer = shortselling.PortfolioOptimizer(prices)
            else : 
                portfolio_optimizer = no_short_selling.PortfolioOptimizer(prices)
    
            
            portfolio_optimizer.markowitz_optimization()
            weights , expected_return = portfolio_optimizer.markowitz_optimization_max_return( risk_tolerance/100 ) 
            exp = round(expected_return , 4) * 100 
            st.markdown(f"<h5>Expected Return is {exp} %</h5>" , unsafe_allow_html=True)
            # st.write(weights)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("<h5>Selected Companies</h5>", unsafe_allow_html=True)
                for company in selected_companies:
                    st.write(company)
    
            with col2:
                st.markdown("<h5>Weights </h5>", unsafe_allow_html=True)
                for w in weights:
                    w = round(w , 4 ) * 100 
                    st.write(f"{w}%")
            try:
                fig = portfolio_optimizer.plot_efficient_frontier_for_given_risk_tolerance(target_return/100) 
                st.plotly_chart(fig)
            except:
                returns = portfolio_optimizer.returns
                min_risk = returns.std().min() * 100 
                max_risk = returns.std().max() * 100 
                st.write("Selected Risk Tolerance Level can't be achieved ") 
                st.write(f"Minimum Risk : {min_risk}") 
                st.write(f"Maximum Risk : {max_risk}")
        except:
            st.error("An error occurred while processing the data. Please ensure that the data is available and try again.")

        
if __name__ == "__main__":
    main()
