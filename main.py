"""
Main script for linearmodel package.

Example usage of the linearmodel package for statistical analysis and linear modeling.
"""
import warnings
from colorama import Fore, Style
import pandas as pd

from linearmodel.print_with_style import PrintWithStyle
import linearmodel.statistics as stats
import linearmodel.visualization as vis
from linearmodel.ordinary_least_squares import OrdinaryLeastSquares

def main():
    """
    Init main.
    """
    printWithStyle = PrintWithStyle()
    # Load data
    RTE_CSV_FILE = "eCO2mix_RTE_Annuel-Definitif_2020.csv"
    data = pd.read_csv(RTE_CSV_FILE, sep=';')

    # Remplacer les valeurs vides par NaN pour faciliter le traitement
    data.replace('', pd.NA, inplace=True)

    # Supprimer les lignes avec des valeurs manquantes dans la colonne 'Consommation'
    data.dropna(subset=['Consommation'], inplace=True)


    data = data.drop(columns=['Date', 'Heures','Prévision J-1','Prévision J'])
    
    # Convert data to float (this will convert non-numeric values to NaN)
    data = data.astype(float)

    # Display the first few rows of the DataFrame to verify data loading
    printWithStyle.print_with_style("Loaded data:", color=Fore.GREEN, bold=True)
    # Suppress numpy and pandas warnings
    warnings.filterwarnings("ignore", category=FutureWarning)
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    print(data.head())

    # Perform descriptive statistics
    descriptive_stats = stats.descriptive_statistics(data)
    printWithStyle.print_with_style("Descriptive statistics:", color=Fore.GREEN, bold=True)
    for stat, value in descriptive_stats.items():
        print(f"{Fore.BLUE}{Style.BRIGHT}  {stat}:{Style.RESET_ALL}{Fore.RESET} {Fore.WHITE}{Style.NORMAL}{value}{Style.RESET_ALL}")


    # Perform correlation analysis
    correlation_matrix = stats.correlation_analysis(data)
    printWithStyle.print_with_style("Correlation matrix:", color=Fore.GREEN, bold=True)
    printWithStyle.print_with_style(correlation_matrix, color=Fore.WHITE, bold=True)

    # Visualize data
    # Box plot for each energy production type
    energy_columns = ['Fioul', 'Charbon', 'Gaz', 'Nucléaire', 'Eolien',
                      'Solaire','Hydraulique','Pompage','Bioénergies','Ech. physiques']
    for col in energy_columns:
        vis.boxplot(data[col], xlabel=f'{col} (MW)', ylabel='', title=f'Box Plot: {col}')

    # Correlation matrix heatmap for selected columns
    selected_columns = ['Consommation', 'Fioul', 'Charbon', 'Gaz', 'Nucléaire', 'Eolien', 'Solaire',
                        'Hydraulique','Pompage','Bioénergies', 'Ech. physiques', 'Taux de Co2']
    selected_data = data[selected_columns]
    
    #For readabilty purpose we only take 10000 data size
    vis.heatmap(selected_data, xlabel='Features', ylabel='Features', title='Correlation Matrix', sample_size=10000)

    # Bar plot for 'Ech. physiques'
    vis.bar_plot(data['Ech. physiques'], xlabel='Category',
                 ylabel='Count', title='Importation / Exportation', bins=20)

    # Density plot for 'Taux de Co2'
    vis.density_plot(data['Taux de Co2'], xlabel='CO2 Emissions (g/kWh)',
                     ylabel='Density', title='Density Plot: CO2 Emissions')

    # Fit linear model using Ordinary Least Squares
     # Extract features (X) and target variable (y)
    X = data[['Fioul', 'Charbon', 'Gaz', 'Nucléaire', 'Eolien', 'Solaire',
              'Hydraulique', 'Pompage', 'Bioénergies']]
    y = data['Consommation']

    # Fit linear model using Ordinary Least Squares
    model = OrdinaryLeastSquares()
    model.fit(X, y)

    # Get coefficients of the fitted model
    coefficients = model.get_coefficients()
    printWithStyle.print_with_style("Coefficients:", color=Fore.GREEN, bold=True)

    # Calculate coefficient of determination (R-squared)
    r_squared = model.determination_coefficient(X, y)
    printWithStyle.print_with_style("Coefficient of Determination (R-squared):" + str(r_squared), color=Fore.GREEN, bold=True)

    # Calculate confidence intervals for coefficients
    confidence_intervals = model.confidence_intervals(X, y)
    printWithStyle.print_with_style("Confidence Intervals for Coefficients:", color=Fore.GREEN, bold=True)
    for i, col in enumerate(X.columns):
        print(f"{Fore.BLUE}{Style.BRIGHT}  {col}:{Style.RESET_ALL}{Fore.RESET} {Fore.WHITE}{Style.NORMAL} {confidence_intervals[i]}{Style.RESET_ALL}")

    # Visualize results
    model.plot_residuals(X, y)
    model.plot_qq_plot(X, y)

if __name__ == "__main__":
    main()  
