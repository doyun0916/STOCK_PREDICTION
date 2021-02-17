import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt

def scaling(d):
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(d)
    return data_scaled

def pca(d, opt):
    pc = PCA(n_components=15)  # 주성분을 몇개로 할지 결정
    components = pc.fit_transform(d)
    if opt == 0:
        plt.plot(np.cumsum(pc.explained_variance_ratio_))           # finding number of components
        plt.xlabel('number of components')
        plt.ylabel('cumulative explained variance in intrusion data')
        plt.show()
        print("PCA Explanation rate: ", sum(pc.explained_variance_ratio_), "\n")  # 최고 수치 나타내는것 find
    components_data = pd.DataFrame(data=components, columns=['pc1', 'pc2', 'pc3', 'pc4', 'pc5', 'pc6', 'pc7',
                                                             'pc8', 'pc9', 'pc10', 'pc11', 'pc12', 'pc13', 'pc14',
                                                             'pc15'])
    return components_data

def preprocess(data, today_data, opt=0):
    y = data['results']
    x = data.drop(columns=['results'])
    dx = pd.concat([x, today_data], axis=0)
    scaled_data = scaling(dx)
    preprocessed_data_x = pca(scaled_data, opt)
    return preprocessed_data_x, y

##################################### Data preprocessiong ##################################################

def data(d, t):
    d_len = len(d)
    print("5년 치 data 수: ", d_len)
    print("data types:\n", d.dtypes, "\n")

    # 결측치 제거
    print("data 결측치:\n", d.isnull().sum(), "\n")
    d.dropna(inplace=True)
    d.dropna(inplace=True, axis=1)
    print("data 기존 수 : ", d_len)
    print("data 결측치 제거 후 수 : ", len(d), "\n")

    preprocessed_data, y = preprocess(d, t, 0)
    final_today_data2 = preprocessed_data.iloc[[-1]]
    preprocessed_data = preprocessed_data.iloc[:-1]
    x_train, x_test, y_train, y_test = train_test_split(preprocessed_data, y, test_size=0.2, train_size=0.8, random_state=42)
    print("x_train data 수: ", len(x_train))
    print("x_test data 수: ", len(x_test))
    print("y_train data 수: ", len(y_train))
    print("y_test data 수: ", len(y_test))

    return x_train, x_test, y_train, y_test, final_today_data2

