import numpy as np
from collections import Counter
import json
from sklearn.metrics import accuracy_score # used to record accuracy of predictions

def entropy(y):
    counts = Counter(y)
    probs = [c / len(y) for c in counts.values()]
    return -sum(p * np.log2(p) for p in probs if p > 0)

def info_gain(y, y_left, y_right):
    p_left = len(y_left) / len(y)
    p_right = len(y_right) / len(y)
    return entropy(y) - (p_left * entropy(y_left) + p_right * entropy(y_right))

class Node:
    def __init__(self, feature=None, threshold=None, left=None, right=None, *, label=None):
        self.feature = feature
        self.threshold = threshold  # Use for numeric split
        self.left = left
        self.right = right
        self.label = label

class ID3TreeNumeric:
    acc_score = 0
    def fit(self, X, y):
        self.root = self._build_tree(X, y)

    # calc accuracy of predictions
    def score(self, X, y_true):
        y_pred = self.predict(X)
        return accuracy_score(y_true, y_pred)

    def _build_tree(self, X, y):
        if len(set(y)) == 1:
            return Node(label=y[0])
        if X.shape[1] == 0:
            most_common = Counter(y).most_common(1)[0][0]
            return Node(label=most_common)

        best_gain = -1
        best_feature = None
        best_threshold = None
        best_splits = None

        for feature in range(X.shape[1]):
            thresholds = np.unique(X[:, feature])
            for t in thresholds:
                left_idx = X[:, feature] <= t
                right_idx = X[:, feature] > t
                if len(y[left_idx]) == 0 or len(y[right_idx]) == 0:
                    continue
                gain = info_gain(y, y[left_idx], y[right_idx])
                if gain > best_gain:
                    best_gain = gain
                    best_feature = feature
                    best_threshold = t
                    best_splits = (left_idx, right_idx)

        if best_gain == -1:
            most_common = Counter(y).most_common(1)[0][0]
            return Node(label=most_common)

        left = self._build_tree(X[best_splits[0]], y[best_splits[0]])
        right = self._build_tree(X[best_splits[1]], y[best_splits[1]])
        return Node(feature=best_feature, threshold=best_threshold, left=left, right=right)

    def predict_one(self, x, node):
        if node.label is not None:
            return node.label
        if x[node.feature] <= node.threshold:
            return self.predict_one(x, node.left)
        else:
            return self.predict_one(x, node.right)

    def predict(self, X):
        return np.array([self.predict_one(x, self.root) for x in X])

# custom data split function (manual train-test split)
def manual_train_test_split(X, y, test_size=0.2):
    indices = np.arange(len(X))
    np.random.shuffle(indices)
    split = int(len(X) * (1 - test_size))
    train_indices = indices[:split]
    test_indices = indices[split:]
    return X[train_indices], X[test_indices], y[train_indices], y[test_indices]

def trainTree(size=None):
    with open('mcts_dataset.json') as f:
        data = json.load(f)
        
    # Limit to the specified size if given
    if size is not None:
        data = data[:size]

    # Convert to features (X) and labels (y)
    X = []
    y = []

    for entry in data:
        board = np.array(entry['state']).flatten()  # Flatten 6x7 into 42-length vector
        move = entry['recommended_move']
        X.append(board)
        y.append(move)

    X = np.array(X)
    y = np.array(y)
    X_train, X_test, y_train, y_test = manual_train_test_split(X, y, test_size=0.2)
    tree = ID3TreeNumeric()
    tree.fit(X_train, y_train)
    tree.acc_score = tree.score(X_test, y_test) # set accuracy score variable for the tree
    print("Tree trained successfully.")
    return tree


# code used in iris practice dataset... the ID3 implementation above was used for iris dataset and is now modified for Connect4 dataset
'''
# Load the dataset
ds = pd.read_csv('../iris.csv')

X = ds.iloc[:, :-1].to_numpy()  # Features
y = ds.iloc[:, -1].to_numpy()   # Labels

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

tree = ID3TreeNumeric()
tree.fit(X_train, y_train)

y_pred = tree.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))

# Show the first 5 rows
print(ds.head())

# Shows each collumn data type
print(ds.dtypes)

# Checks for missing values
print(ds.isnull().values.any())
'''