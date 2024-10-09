import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
import yfinance as yf
from scipy.optimize import minimize
import plotly.graph_objs as go


class PortfolioOptimizer:
    def __init__(self , prices ):
        self.prices = prices 
        self.returns = prices.pct_change().dropna()
        self.risks = prices.pct_change().dropna().std()
        self.optimal_return = None
        
    def markowitz_optimization(self):
        returns = self.returns
        num_assets = len(returns.columns)
        returns_mean = returns.mean()
        cov_matrix = returns.cov()
        optimal_return = None

        # Define optimization function
        def portfolio_return(weights):
            return -np.dot(weights, returns_mean)

        def portfolio_variance(weights):
            return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

        # Define constraints and bounds for optimization
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = tuple((0,1) for asset in range(num_assets))

        # Initial guess (equal weighting)
        initial_guess = np.array(num_assets * [1. / num_assets,])

        # Perform optimization
        optimal_weights = minimize(portfolio_variance, initial_guess, method='SLSQP', bounds=bounds, constraints=constraints)
        optimal_risk = portfolio_variance(optimal_weights.x)
        optimal_return = -portfolio_return(optimal_weights.x)
        self.optimal_return = optimal_return
        return optimal_weights.x, optimal_risk, optimal_return

    def markowitz_optimization_for_target_return(self, target_return):
        returns = self.returns
        num_assets = len(returns.columns)
        returns_mean = returns.mean()
        cov_matrix = returns.cov()

        # Define optimization function
        def portfolio_variance(weights):
            return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

        # Define constraints and bounds for optimization
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
                       {'type': 'eq', 'fun': lambda x: np.dot(x, returns_mean) - target_return})
        bounds = tuple((0,1) for asset in range(num_assets))

        # Initial guess (equal weighting)
        initial_guess = np.array(num_assets * [1. / num_assets,])

        # Perform optimization
        optimal_weights = minimize(portfolio_variance, initial_guess, method='SLSQP', bounds=bounds, constraints=constraints)
        optimal_risk = portfolio_variance(optimal_weights.x)
        return optimal_weights.x, optimal_risk, target_return

    # def plot_efficient_frontier_(self):
    #     returns = self.returns 
    #     min_return = returns.mean().min()
    #     max_return = returns.mean().max()
    #     targets = np.linspace(min_return, max_return, 100)
    #     weights = []
    #     risks = []
    #     return_ = []
    # 
        # for i in range(len(targets)):
        #     w, ri, re = self.markowitz_optimization_for_target_return( targets[i])
        #     weights.append(w)
        #     risks.append(ri)
        #     return_.append(re)
        # plt.figure(figsize=(20, 5))
        # plt.plot(risks, return_)
        # plt.show()

    def plot_efficient_frontier_parabola(self):
        returns = self.returns 
        min_return = returns.mean().min()
        max_return = returns.mean().max()
        targets = np.linspace(min_return, max_return, 100)
        weights = []
        risks = []
        return_ = []

        for i in range(len(targets)):
            w, ri, re = self.markowitz_optimization_for_target_return( targets[i])
            weights.append(w)
            risks.append(ri)
            return_.append(re)

        # Create trace for the efficient frontier
        efficient_frontier_trace = go.Scatter(
            x=risks,
            y=return_,
            mode='lines',
            name='Efficient Frontier'
        )

        # Create a list of points for hover text
        hover_text = []
        for i in range(len(risks)):
            hover_text.append(
                f'Risks: {risks[i]:.4f}<br>Weights: {weights[i]}<br>Return: {return_[i]:.4f}')

        # Create trace for individual points with hover text
        efficient_frontier_points_trace = go.Scatter(
            x=risks,
            y=return_,
            mode='markers',
            name='Efficient Frontier Points',
            text=hover_text,
            hoverinfo='text'
        )

        # Create layout
        layout = go.Layout(
            title='Efficient Frontier',
            xaxis=dict(title='Volatility'),
            yaxis=dict(title='Return')
        )

        # Create figure
        fig = go.Figure(data=[efficient_frontier_trace,
                              efficient_frontier_points_trace], layout=layout)

        return fig

    def plot_efficient_frontier(self):
        returns = self.returns
        # min_return = returns.mean().min()
        min_return = self.optimal_return
        max_return = returns.mean().max()
        targets = np.linspace(min_return, max_return, 75)
        weights = []
        risks = []
        return_ = []

        for i in range(len(targets)):
            w, ri, re = self.markowitz_optimization_for_target_return( targets[i])
            weights.append(w)
            risks.append(ri)
            return_.append(re)

        # Create trace for the efficient frontier
        efficient_frontier_trace = go.Scatter(
            x=risks,
            y=return_,
            mode='lines',
            name='Efficient Frontier'
        )

        # Create a list of points for hover text
        hover_text = []
        for i in range(len(risks)):
            hover_text.append(
                f'Risks: {risks[i]:.4f}<br>Weights: {weights[i]}<br>Return: {return_[i]:.4f}')

        # Create trace for individual points with hover text
        efficient_frontier_points_trace = go.Scatter(
            x=risks,
            y=return_,
            mode='markers',
            name='Efficient Frontier Points',
            text=hover_text,
            hoverinfo='text'
        )

        # Create layout
        layout = go.Layout(
            title='Efficient Frontier',
            xaxis=dict(title='Volatility'),
            yaxis=dict(title='Return')
        )

        # Create figure
        fig = go.Figure(data=[efficient_frontier_trace,
                              efficient_frontier_points_trace], layout=layout)

        # Show plot
        # fig.show()
        return fig
        
    def plot_efficient_frontier_for_given_risk_tolerance_levels(self,  risk_tolerance1, risk_tolerance2):
        returns = self.returns
        min_return = self.optimal_return
        max_return = returns.mean().max()
        targets = np.linspace(min_return, max_return, 60 )
        weights = []
        risks = []
        return_ = []
        
        for i in range(len(targets)):
            w, ri, re = self.markowitz_optimization_for_target_return( targets[i])
            weights.append(w)
            risks.append(ri)
            return_.append(re)
        # print(risks)
        closest_risk1 = risk_tolerance1
        closest_risk2 = risk_tolerance2

        for i in range(len(risks) - 1):
            if(risks[i] <= risk_tolerance1 <= risks[i+1]):
                closest_risk1 = risks[i] if risk_tolerance1 - risks[i] < risks[i+1] - risk_tolerance1 else risks[i+1]
            if(risks[i] <= risk_tolerance2 <= risks[i+1]):
                closest_risk2 = risks[i] if risk_tolerance2 - risks[i] < risks[i+1] - risk_tolerance2 else risks[i+1]
        # print(closest_risk1 , closest_risk2)
        # Create trace for the efficient frontier
        efficient_frontier_trace = go.Scatter(
            x=risks,
            y=return_,
            mode='lines',
            name='Efficient Frontier'
        )

        # Create a list of points for hover text
        hover_text = []
        for i in range(len(risks)):
            hover_text.append(
                f'Risks: {risks[i]:.4f}<br>Weights: {weights[i]}<br>Return: {return_[i]:.4f}')

        # Create trace for individual points with hover text
        efficient_frontier_points_trace = go.Scatter(
            x=risks,
            y=return_,
            mode='markers',
            name='Efficient Frontier Points',
            text=hover_text,
            hoverinfo='text'
        )

        # Highlight closest risk tolerance levels
        closest_risk1_index = risks.index(closest_risk1)
        closest_risk2_index = risks.index(closest_risk2)

        # Create trace for closest risk tolerance levels
        closest_risk1_trace = go.Scatter(
            x=[risks[closest_risk1_index]],
            y=[return_[closest_risk1_index]],
            mode='markers',
            marker=dict(symbol='star', color='purple', size=15),
            name=f'Risk Tolerance {risk_tolerance1}'
        )

        closest_risk2_trace = go.Scatter(
            x=[risks[closest_risk2_index]],
            y=[return_[closest_risk2_index]],
            mode='markers',
            marker=dict(symbol='star', color='black', size=15),
            name=f'Risk Tolerance {risk_tolerance2}'
        )

        # Create layout
        layout = go.Layout(
            title='Efficient Frontier',
            xaxis=dict(title='Volatility'),
            yaxis=dict(title='Return')
        )

        # Create figure
        fig = go.Figure(data=[efficient_frontier_trace, efficient_frontier_points_trace, closest_risk1_trace, closest_risk2_trace], layout=layout)

        # Show plot
        # fig.show() 
        return fig


    def plot_efficient_frontier_for_given_target_return(self,  target_return ):
        returns = self.returns
        min_return = self.optimal_return
        max_return = returns.mean().max()
        targets = np.linspace(min_return, max_return, 60 )
        weights = []
        risks = []
        return_ = []
        print(min_return , max_return )
        for i in range(len(targets)):
            w, ri, re = self.markowitz_optimization_for_target_return( targets[i])
            weights.append(w)
            risks.append(ri)
            return_.append(re)
        # print(risks)
        closest_target = target_return

        for i in range(len(return_) - 1):
            if(return_[i] <= target_return <= return_[i+1]):
                if target_return - return_[i] < return_[i+1] - target_return :
                    closest_target = return_[i]
                else:
                    closest_target = return_[i+1]
        print(closest_target)
        # print(closest_risk1 , closest_risk2)
        # Create trace for the efficient frontier
        efficient_frontier_trace = go.Scatter(
            x=risks,
            y=return_,
            mode='lines',
            name='Efficient Frontier'
        )

        # Create a list of points for hover text
        hover_text = []
        for i in range(len(risks)):
            hover_text.append(
                f'Risks: {risks[i]:.4f}<br>Weights: {weights[i]}<br>Return: {return_[i]:.4f}')

        # Create trace for individual points with hover text
        efficient_frontier_points_trace = go.Scatter(
            x=risks,
            y=return_,
            mode='markers',
            name='Efficient Frontier Points',
            text=hover_text,
            hoverinfo='text'
        )


        closest_target_index = return_.index(closest_target) 
        closest_target_trace = go.Scatter(
            x = [risks[closest_target_index]] , 
            y = [return_[closest_target_index]] , 
            mode = 'markers' , 
            marker=dict(symbol='star', color='purple', size=15),
            name=f'Target Return  {target_return }'
            
        )
        # Highlight closest risk tolerance levels
        # closest_risk1_index = risks.index(closest_risk1)
        # closest_risk2_index = risks.index(closest_risk2)

        # # Create trace for closest risk tolerance levels
        # closest_risk1_trace = go.Scatter(
        #     x=[risks[closest_risk1_index]],
        #     y=[return_[closest_risk1_index]],
        #     mode='markers',
        #     marker=dict(symbol='star', color='purple', size=15),
        #     name=f'Risk Tolerance {risk_tolerance1}'
        # )

        # closest_risk2_trace = go.Scatter(
        #     x=[risks[closest_risk2_index]],
        #     y=[return_[closest_risk2_index]],
        #     mode='markers',
        #     marker=dict(symbol='star', color='black', size=15),
        #     name=f'Risk Tolerance {risk_tolerance2}'
        # )

        # Create layout
        layout = go.Layout(
            title='Efficient Frontier',
            xaxis=dict(title='Volatility'),
            yaxis=dict(title='Return')
        )

        # Create figure
        fig = go.Figure(data=[efficient_frontier_trace, efficient_frontier_points_trace , closest_target_trace ], layout=layout)

        # Show plot
        # fig.show() 
        return fig
    
    def markowitz_optimization_max_return(self , target_risk):
        returns = self.returns
        num_assets = len(returns.columns)
        returns_mean = returns.mean()
        cov_matrix = returns.cov()
    
        # Define optimization function (negative of portfolio return to convert maximization to minimization)
        def negative_portfolio_return(weights):
            return -np.dot(weights, returns_mean)
    
        # Define constraints and bounds for optimization
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
                       {'type': 'eq', 'fun': lambda x: np.sqrt(np.dot(x.T, np.dot(cov_matrix, x))) - target_risk})
        bounds = tuple((0,1) for asset in range(num_assets))
    
        initial_guess = np.array(num_assets * [1. / num_assets,])
    
        # Perform optimization
        optimal_weights = minimize(negative_portfolio_return, initial_guess, method='SLSQP', bounds=bounds, constraints=constraints)
        # optimal_risk = np.sqrt(np.dot(optimal_weights.x.T, np.dot(cov_matrix, optimal_weights.x)))
        optimal_return = -negative_portfolio_return(optimal_weights.x)
        
        return optimal_weights.x, optimal_return
    
            
    def plot_efficient_frontier_for_given_risk_tolerance(self,  risk_tolerance ):
        returns = self.returns
        min_return = self.optimal_return
        max_return = returns.mean().max()
        targets = np.linspace(min_return, max_return, 60 )
        weights = []
        risks = []
        return_ = []
        
        for i in range(len(targets)):
            w, ri, re = self.markowitz_optimization_for_target_return( targets[i])
            weights.append(w)
            risks.append(ri)
            return_.append(re)
        # print(risks)
        closest_risk = risk_tolerance

        for i in range(len(risks) - 1):
            if(risks[i] <= risk_tolerance <= risks[i+1]):
                closest_risk = risks[i] if risk_tolerance - risks[i] < risks[i+1] - risk_tolerance else risks[i+1]
            
        efficient_frontier_trace = go.Scatter(
            x=risks,
            y=return_,
            mode='lines',
            name='Efficient Frontier'
        )

        # Create a list of points for hover text
        hover_text = []
        for i in range(len(risks)):
            hover_text.append(
                f'Risks: {risks[i]:.4f}<br>Weights: {weights[i]}<br>Return: {return_[i]:.4f}')

        # Create trace for individual points with hover text
        efficient_frontier_points_trace = go.Scatter(
            x=risks,
            y=return_,
            mode='markers',
            name='Efficient Frontier Points',
            text=hover_text,
            hoverinfo='text'
        )

        # Highlight closest risk tolerance levels
        closest_risk1_index = risks.index(closest_risk)

        # Create trace for closest risk tolerance levels
        closest_risk1_trace = go.Scatter(
            x=[risks[closest_risk1_index]],
            y=[return_[closest_risk1_index]],
            mode='markers',
            marker=dict(symbol='star', color='purple', size=15),
            name=f'Risk Tolerance {risk_tolerance}'
        )

        # closest_risk2_trace = go.Scatter(
        #     x=[risks[closest_risk2_index]],
        #     y=[return_[closest_risk2_index]],
        #     mode='markers',
        #     marker=dict(symbol='star', color='black', size=15),
        #     name=f'Risk Tolerance {risk_tolerance2}'
        # )

        # Create layout
        layout = go.Layout(
            title='Efficient Frontier',
            xaxis=dict(title='Volatility'),
            yaxis=dict(title='Return')
        )

        # Create figure
        fig = go.Figure(data=[efficient_frontier_trace, efficient_frontier_points_trace, closest_risk1_trace ], layout=layout)

        # # Show plot
        # fig.show() 
        return fig