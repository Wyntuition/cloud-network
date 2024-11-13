import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys

def plot_cdf(file_path, label):
    df = pd.read_csv(file_path)
    durations = df['Duration'].values

    sorted_durations = np.sort(durations)
    cdf = np.arange(1, len(sorted_durations) + 1) / len(sorted_durations)

    plt.plot(sorted_durations, cdf, label=label)

if __name__ == "__main__":

    result_files = [
        ('results_1.csv', '1 Producer'),
        ('results_2.csv', '2 Producers'),
        ('results_3.csv', '3 Producers'),
        ('results_4.csv', '4 Producers'),
        ('results_5.csv', '5 Producers')
    ]

    plt.figure(figsize=(10, 6))

    for file_path, label in result_files:
        plot_cdf(file_path, label)

    plt.xlabel('Message Send Duration (seconds)')
    plt.ylabel('Cumulative Probability')
    plt.title('CDF of Message Send Durations for Different Numbers of Producers')
    plt.legend()
    plt.grid(True)
    plt.show()

