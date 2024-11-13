import pickle
import numpy as np

# Create sample data
labels = [0, 1, 2]
data = [np.random.rand(32, 32, 3) * 255 for _ in range(len(labels))]  # Random RGB images (32x32 pixels)
filenames = [f'image_{i}.png' for i in range(len(labels))]  # Example filenames

# Create a dictionary to hold the data
pic_dict = {
    b'labels': labels,
    b'data': data,
    b'filenames': filenames
}

with open('sample_data.pkl', 'wb') as f:
    pickle.dump(pic_dict, f)

print("Pickled file 'sample_data.pkl' created.")

