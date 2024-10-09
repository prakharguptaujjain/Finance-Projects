# Stock Technical Analysis

Stock analysis using various indicators and methods.

## Installing Dependencies

Run `pip install -r requirements.txt` to install the required dependencies.

## Data

The notebook uses Blackrock (BLK) from Yahoo Finance from date 01-01-2021 to 01-01-2024. The data is stored in the file BLK.csv.

## Notebook

### Plots

- Line Plots
- Close Price over time
- Kernel Density Estimate (KDE) plot for Close - Price distribution
- Prediction Using Technical Indicators
- Moving Average (MA)
- Relative Strength Index (RSI)
- Bollinger Bands (BB)
- MACD (Moving Average Convergence Divergence)

### Prediction Methods

#### Correlation Analysis for (Method-1 and Method-2)

Examines the correlation matrix of selected technical indicators.

#### Method-1

Combines predictions from Moving Average, RSI, Bollinger Bands, and MACD using weighted indicators.

#### Method-2

Normalizes and combines indicators (MA, RSI, Rolling Mean, MACD_Line) with weighted values, then compares with upper and lower thresholds for prediction.

### Method-3

Indicators used : Moving Average , Relative Strength Index , On Balance Volume , Average Directional Index 
Using the closing prices from the previous 5 days and correlation, we determine the weights using the equation of least square optimisation.

#### Accuracy Calculation

Evaluates the accuracy of predictions from Method-1, Method-2, and Method-3.

#### Results

The final predictions from all methods are saved in a CSV file named Prediction.csv. The predictions are denoted as 'L' (Long), 'S' (Short), and 'X' (Not considered in the first 30 data points due to moving averages).

## License

MIT License

## Author

- [Prakhar Gupta](https://github.com/prakharguptaujjain)
- [Ashutosh](https://github.com/ashuashutosh2211)
- [Adarsh Raj Shrivastava](https://github.com/k3x9)
- [Saloni Garg](https://github.com/Saloni2004)
