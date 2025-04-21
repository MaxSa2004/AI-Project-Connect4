import pandas as pd
import numpy as np
import math
from collections import Counter

# Função para calcular a entropia de um conjunto de dados
def entropy(labels):
    total = len(labels)
    counts = Counter(labels)
    return -sum((count/total) * math.log2(count/total) for count in counts.values())

# Função para dividir os dados com base numa feature
def split_dataset(df, feature):
    values = df[feature].unique()
    return {v: df[df[feature] == v].drop(columns=[feature]) for v in values}

# Função para escolher a melhor feature (com maior ganho de informação)
def choose_best_feature(df):
    base_entropy = entropy(df.iloc[:, -1])
    features = df.columns[:-1]
    best_gain = -1
    best_feature = None
    
    for feature in features:
        splits = split_dataset(df, feature)
        new_entropy = sum((len(subset)/len(df)) * entropy(subset.iloc[:, -1]) for subset in splits.values())
        gain = base_entropy - new_entropy
        if gain > best_gain:
            best_gain = gain
            best_feature = feature
    return best_feature

# ID3 Recursivo
def id3(df):
    labels = df.iloc[:, -1]
    
    if len(labels.unique()) == 1:
        return labels.iloc[0]
    
    if len(df.columns) == 1:
        return labels.mode()[0]

    best_feature = choose_best_feature(df)
    tree = {best_feature: {}}
    splits = split_dataset(df, best_feature)
    
    for value, subset in splits.items():
        tree[best_feature][value] = id3(subset)
    
    return tree

# Função para classificar um novo exemplo
def classify(tree, instance):
    if not isinstance(tree, dict):
        return tree
    
    feature = next(iter(tree))
    feature_value = instance[feature]
    
    if feature_value in tree[feature]:
        return classify(tree[feature][feature_value], instance)
    else:
        return "Unknown"

import csv
import random

# Load discretized iris data
def load_data(filename):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    return data

# Split into train/test
def split_data(data, test_ratio=0.2):
    random.shuffle(data)
    split_point = int(len(data) * (1 - test_ratio))
    return data[:split_point], data[split_point:]

# Example usage
filename = 'iris_discretized.csv'  # This is the output from your discretizer
data = load_data('iris.csv')
train_set, test_set = split_data(data)

# Just to verify
print("Training set size:", len(train_set))
print("Test set size:", len(test_set))
print("\nSample test example:")
print(test_set[0])


# Convert list of dicts to DataFrame for training
train_df = pd.DataFrame(train_set)

# Remove ID column if it exists
if 'ID' in train_df.columns:
    train_df = train_df.drop(columns=['ID'])


# Build decision tree
tree = id3(train_df)

print("\nLearned Decision Tree:")
print(tree)

# Evaluate on test set
correct = 0
for example in test_set:
    instance = {k: v for k, v in example.items() if k != 'ID'}  # Remove ID
    prediction = classify(tree, instance)
    actual = example['class']
    print(f"Predicted: {prediction}, Actual: {actual}")
    if prediction == actual:
        correct += 1


accuracy = correct / len(test_set)
print(f"\nAccuracy on test set: {accuracy:.2f}")
