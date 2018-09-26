import numpy as np
from stockpredict import db
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression,Lasso,Ridge,BayesianRidge

def get_data(symbol):
    conn = db.getconn()
    cursor = db.getcursor(conn)
    cursor.execute('select spj from lsjy where symbol = "{0}" order by day asc '.format(symbol))
    l = list()
    for row in cursor:
        l.append(float(row[0]))
    x = list()
    y = list()
    for index in range(15, len(l)):
        x.append(l[index-15:index])
        y.append(l[index])
    x = np.array(x)
    y = np.array(y)
    return x, y


def predict(model, data):
    data = data.tolist()
    y_hat = np.zeros(5, float)
    for index in range(0, 5):
        l = list()
        l.append(data)
        x = np.array(l)
        y_hat[index] = model.predict(x)
        del data[0]
        data.append(y_hat[index])
    return y_hat






if __name__ == "__main__":
    x, y = get_data("sh600000")
    model = BayesianRidge(alpha_1=1e-02, alpha_2=1e-02)
    model.fit(x[0:len(x)-21], y[0:len(x)-21])
    data = y[len(y)-21:len(y)-6]
    y_hat = predict(model, data)
    y = y[len(y)-6:len(y)-1]
    print(y)
    print(y_hat)
    plt.plot(np.arange(1, 6), y, "b")
    plt.plot(np.arange(1, 6), y_hat, "r")
    plt.show()

