import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Bidirectional
from tensorflow.keras.callbacks import ModelCheckpoint, TensorBoard
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from collections import deque 
import numpy as np
import pandas as pd
from collections import deque 
import random
import os
import time
import matplotlib.pyplot as plt

# Constants
N_STEPS = 10
LOOKUP_STEP = 20
SCALE = False
SHUFFLE = True
TEST_SIZE = 0.5
FEATURE_COLUMNS = ['Positive Score', 'Negative Score', 'Neutral Score']
N_LAYERS = 2
CELL = LSTM
UNITS = 256
DROPOUT = 0
BIDIRECTIONAL = False
LOSS = "huber"
OPTIMIZER = "adam"
BATCH_SIZE = 2
EPOCHS = 25

# Set random seeds for reproducibility
np.random.seed(314)
tf.random.set_seed(314)
random.seed(314)

def shuffle_in_unison(a, b):
    state = np.random.get_state()
    np.random.shuffle(a)
    np.random.set_state(state)
    np.random.shuffle(b)

def load_data(file_path, n_steps=50, scale=True, shuffle=True, lookup_step=1, test_size=0.2):
    # Load data from file
    df = pd.read_csv(file_path)
    result = {}
    result['df'] = df.copy()
    
    feature_columns = ['Positive Score', 'Negative Score', 'Neutral Score']
    if scale:
        column_scaler = {}
        for column in feature_columns:
            scaler = preprocessing.MinMaxScaler()
            df[column] = scaler.fit_transform(np.expand_dims(df[column].values, axis=1))
            column_scaler[column] = scaler
        result["column_scaler"] = column_scaler
    
    df['future'] = df['Change in SPY'].shift(-lookup_step)
    df.dropna(inplace=True)
    
    sequence_data = []
    sequences = deque(maxlen=n_steps)
    
    for entry, target in zip(df[feature_columns].values, df['future'].values):
        sequences.append(entry)
        if len(sequences) == n_steps:
            sequence_data.append([np.array(sequences), target])
    
    last_sequence = list([s[:len(feature_columns)] for s in sequences])
    last_sequence = np.array(last_sequence).astype(np.float32)
    result['last_sequence'] = last_sequence
    
    X, y = [], []
    for seq, target in sequence_data:
        X.append(seq)
        y.append(target)
    
    X = np.array(X)
    y = np.array(y)
    
    train_samples = int((1 - test_size) * len(X))
    result["X_train"] = X[:train_samples]
    result["y_train"] = y[:train_samples]
    result["X_test"]  = X[train_samples:]
    result["y_test"]  = y[train_samples:]
    if shuffle:
        shuffle_in_unison(result["X_train"], result["y_train"])
        shuffle_in_unison(result["X_test"], result["y_test"])

    result["X_train"] = result["X_train"].astype(np.float32)
    result["X_test"] = result["X_test"].astype(np.float32)
    
    return result

def create_model(sequence_length, n_features, units=UNITS, cell=LSTM, n_layers=N_LAYERS, dropout=DROPOUT,
                 loss=LOSS, optimizer=OPTIMIZER, bidirectional=BIDIRECTIONAL):
    model = Sequential()
    for i in range(n_layers):
        if i == 0:
            if bidirectional:
                model.add(Bidirectional(cell(units, return_sequences=True)))
            else:
                model.add(cell(units, return_sequences=True))
        elif i == n_layers - 1:
            if bidirectional:
                model.add(Bidirectional(cell(units, return_sequences=False)))
            else:
                model.add(cell(units, return_sequences=False))
        else:
            if bidirectional:
                model.add(Bidirectional(cell(units, return_sequences=True)))
            else:
                model.add(cell(units, return_sequences=True))
        model.add(Dropout(dropout))
    model.add(Dense(1, activation="linear"))
    model.compile(loss=loss, metrics=["mean_absolute_error"], optimizer=optimizer)
    return model




# Setup directories
model_name = f"model2"
if not os.path.isdir("results"):
    os.mkdir("results")
if not os.path.isdir("logs"):
    os.mkdir("logs")
if not os.path.isdir("data"):
    os.mkdir("data")

# Load data
data = load_data("dataV2.csv", N_STEPS, scale=SCALE, shuffle=SHUFFLE, test_size=TEST_SIZE)

# Create model
model = create_model(N_STEPS, len(FEATURE_COLUMNS), loss=LOSS, units=UNITS, cell=CELL, n_layers=N_LAYERS,
                     dropout=DROPOUT, optimizer=OPTIMIZER, bidirectional=BIDIRECTIONAL)

# Model callbacks
checkpointer = ModelCheckpoint(
    os.path.join("results", model_name + ".weights.h5"),  # Change the extension
    save_weights_only=True,
    save_best_only=True,
    verbose=1
)
tensorboard = TensorBoard(log_dir=os.path.join("logs", model_name))

# Train the model
history = model.fit(data["X_train"], data["y_train"],
                    batch_size=BATCH_SIZE,
                    epochs=EPOCHS,
                    validation_data=(data["X_test"], data["y_test"]),
                    callbacks=[checkpointer, tensorboard],
                    verbose=1)

def plot_graph(test_df):
    plt.plot(test_df['true_change'], c='b')
    plt.plot(test_df['predicted_change'], c='r')
    plt.xlabel("Days")
    plt.ylabel("Price Change")
    plt.legend(["Actual Change", "Predicted Change"])
    plt.show()

def get_final_df(model, data):
    X_test = data["X_test"]
    y_test = data["y_test"]
    y_pred = model.predict(X_test)
    
    if SCALE:
        y_test = np.squeeze(data["column_scaler"]["Positive Score"].inverse_transform(np.expand_dims(y_test, axis=0)))
        y_pred = np.squeeze(data["column_scaler"]["Positive Score"].inverse_transform(y_pred))
    
    test_df = data["df"].iloc[-len(y_test):]
    test_df['predicted_change'] = y_pred
    test_df['true_change'] = y_test
    return test_df

def predict(model, data):
    last_sequence = data["last_sequence"][-N_STEPS:]
    last_sequence = np.expand_dims(last_sequence, axis=0)
    prediction = model.predict(last_sequence)
    if SCALE:
        predicted_change = data["column_scaler"]["Positive Score"].inverse_transform(prediction)[0][0]
    else:
        predicted_change = prediction[0][0]
    return predicted_change

# Evaluate model
model_path = os.path.join("results", model_name + ".weights.h5")
model.load_weights(model_path)

loss, mae = model.evaluate(data["X_test"], data["y_test"], verbose=0)

# Calculate metrics
final_df = get_final_df(model, data)
future_change = predict(model, data)

print(f"Future change after {LOOKUP_STEP} days is {future_change:.2f}")
print(f"{LOSS} loss:", loss)
print("Mean Absolute Error:", mae)

plot_graph(final_df)

csv_results_folder = "csv-results"
if not os.path.isdir(csv_results_folder):
    os.mkdir(csv_results_folder)
csv_filename = os.path.join(csv_results_folder, model_name + ".csv")
final_df.to_csv(csv_filename)