import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Sample data
data = {
    'Country': ['USA', 'Canada', 'Germany', 'UK', 'France'],
    'Population': [331000000, 37700000, 83700000, 67800000, 65200000]
}
time_data = {
    'Year': np.arange(2000, 2021),
    'USA': np.random.randint(300000000, 350000000, size=21),
    'Canada': np.random.randint(33000000, 40000000, size=21),
    'Germany': np.random.randint(80000000, 85000000, size=21),
    'UK': np.random.randint(60000000, 70000000, size=21),
    'France': np.random.randint(60000000, 70000000, size=21),
}

# Create DataFrames
population_df = pd.DataFrame(data)
time_df = pd.DataFrame(time_data)

class ChartInteractor:
    def __init__(self, bar_chart, line_chart, countries):
        self.bar_chart = bar_chart
        self.line_chart = line_chart
        self.countries = countries
        
        # Get the figure from the bar chart's axes
        self.figure = self.bar_chart[0].figure
        
        # Connect the click event to the handler
        self.figure.canvas.mpl_connect('button_press_event', self.on_click)

    def on_click(self, event):
        """Handle click events on the bar chart."""
        if event.inaxes == self.bar_chart[0].axes:  # Check if click is in bar chart axes
            for i, bar in enumerate(self.bar_chart):
                # Use bar.get_bbox().contains to check if the click is inside the bar
                if bar.get_bbox().contains(event.x, event.y):
                    self.update_line_chart(self.countries[i])
                    break
                print((bar.get_bbox()), i, event.x, event.y, bar.get_bbox().x0, bar.get_bbox().y0, bar.get_bbox().x1, bar.get_bbox().y1)
            print("\n")

    def update_line_chart(self, country):
        """Update the line chart based on the selected country."""
        self.line_chart.set_ydata(time_df[country])
        self.line_chart.axes.set_title(f'Population Over Time for {country}')
        self.line_chart.axes.relim()  # Adjust limits to new data
        self.line_chart.axes.autoscale_view()  # Rescale the view
        self.line_chart.axes.legend([country])
        plt.draw()  # Redraw the figure

# Set up the figure and axes
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Bar chart for populations
bars = ax1.bar(population_df['Country'], population_df['Population'], color='skyblue')
ax1.set_title('Population by Country')
ax1.set_ylabel('Population')

# Line chart for population over time (initially show data for the first country)
initial_country = population_df['Country'][0]
line, = ax2.plot(time_df['Year'], time_df[initial_country], marker='o', label=initial_country)
ax2.set_title(f'Population Over Time for {initial_country}')
ax2.set_xlabel('Year')
ax2.set_ylabel('Population')
ax2.legend()

# Initialize the ChartInteractor
interactor = ChartInteractor(bars, line, population_df['Country'])

plt.tight_layout()
plt.show()
