import pickle
import numpy as np

# Create sample data
num_samples = 1000
data_dim = 3072  # Typical dimension for 32x32x3 images

# Generate random data
data = np.random.randint(0, 255, (num_samples, data_dim))
labels = np.random.randint(0, 10, num_samples)
filenames = [f'image_{i}.png' for i in range(num_samples)]

# Create dictionary
pic_dict = {
    b'data': data,
    b'labels': labels,
    b'filenames': filenames
}

# Save to pickle file
with open('data_file.pkl', 'wb') as f:
    pickle.dump(pic_dict, f)
