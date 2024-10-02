def unpickle(file):
    import pickle
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict


def main():
    import sys
    import matplotlib.pyplot as plt
    import cv2
    file_name = sys.argv[1]
    pic_dict = unpickle(file_name)

    for title, path in pic_dict.items():
        print(title, path, "\n")

if __name__ == "__main__":
    main()


