# Covid-19

Some play with python and charts to get going with quarantine boredom :P

Features:
- Updates with data from https://covid19.min-saude.pt/ponto-de-situacao-atual-em-portugal/
- Cache data to not overwhelm systems
- Logistic fit and statistics based on https://towardsdatascience.com/covid-19-infection-in-italy-mathematical-models-and-predictions-7784b4d7dd8d
- Charts!!!

![Chart of 28-03-2020](https://i.imgur.com/O77jAC8.png)

## Usage

Available metrics
`./covid19.py list`

Fetch data from a metric
`./covid19.py csv --attribute casosnovos`

Plot some charts
`./covid19.py plot --plot_file mychart.png`
