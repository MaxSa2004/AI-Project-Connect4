import numpy as np
import matplotlib.pyplot as plt
from tree import trainTree

def treeAccuracyStats(runs=10):
    scores = []
    # accuracy scores
    for i in range(runs):
        tree = trainTree()
        scores.append(tree.acc_score)

    # calculate mean and standard deviation
    mean_score = np.mean(scores)
    std_score  = np.std(scores, ddof=1)  # sample standard deviation

    # plotting
    plt.figure(figsize=(10, 6))
    plt.plot(np.arange(1, runs + 1), scores, marker='o', linestyle='-', color='royalblue')
    plt.axhline(mean_score, color='red', linestyle='--', label=f'Mean: {mean_score:.3f}')
    plt.title('Decision Tree Accuracy over Multiple Runs')
    plt.xlabel('Run')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()

def treeAccuracyStats_DiffSize(runs=10):
    # Sizes of dataset to test
    sizes = [10000, 20000, 30000]
    size_scores = {size: [] for size in sizes}
    colors = ['blue', 'green', 'purple']  # Colors for each size

    for size in sizes:
        print(f"\nTesting with dataset size = {size}")
        for i in range(runs):
            tree = trainTree(size=size)
            size_scores[size].append(tree.acc_score)

    # Plotting
    plt.figure(figsize=(12, 7))
    
    for size, color in zip(sizes, colors):
        scores = size_scores[size]
        runs = np.arange(1, len(scores) + 1)
        mean_score = np.mean(scores)
        std_score = np.std(scores, ddof=1)
        
        # Plotting the accuracy scores
        plt.plot(runs, scores, marker='o', linestyle='-', color=color, label=f'{size} samples')

        # Mean line
        plt.axhline(mean_score, color=color, linestyle='--', alpha=0.6, label=f'Mean: {mean_score:.3f}')
        plt.text(runs[-1] + 0.2, mean_score, f'{mean_score:.3f}', color=color)

    plt.title('Decision Tree Accuracy over Multiple Dataset Sizes')
    plt.xlabel('Run')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()

if __name__ == "__main__":
    treeAccuracyStats()
    treeAccuracyStats_DiffSize()