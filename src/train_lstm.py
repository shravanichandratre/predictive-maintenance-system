import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# Generate dummy sequential data for training
X = np.random.rand(100, 10, 1)  # 100 samples, 10 time steps, 1 feature
y = np.random.randint(2, size=(100, 1))  # Binary labels

# Define the LSTM model
model = Sequential()
model.add(LSTM(50, activation='relu', input_shape=(10, 1)))
model.add(Dense(1, activation='sigmoid'))
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X, y, epochs=10, verbose=1)

# Save the model
model.save("../models/lstm_model.h5")
print("LSTM model saved as lstm_model.h5 in the models folder.")
