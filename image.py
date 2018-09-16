import numpy as np
import scipy
from scipy import ndimage
import glob
import pickle

# setting up the training set
train_set_owl = np.zeros((70, 64, 64, 3))
i = 0
for img in glob.glob("F:/Paul Gao/Documents/randombot/owlimages/*.jpg"):
    image = np.array(ndimage.imread(img, flatten=False))
    train_set_owl[i] = scipy.misc.imresize(image, size=(64, 64))
    i += 1
y_owl = np.ones((70, 1))

test_set_owl = np.zeros((36, 64, 64, 3))
i = 0
for img in glob.glob("F:/Paul Gao/Documents/randombot/owlimages_test/*.jpg"):
    image = np.array(ndimage.imread(img, flatten=False))
    train_set_owl[i] = scipy.misc.imresize(image, size=(64, 64))
    i += 1
y_owl_test = np.ones((36, 1))

train_set_nonowl = np.zeros((130, 64, 64, 3))
i = 0
for img in glob.glob("F:/Paul Gao/Documents/randombot/nonowlimages/*.jpg"):
    image = np.array(ndimage.imread(img, flatten=False))
    #print (i)
    train_set_nonowl[i] = scipy.misc.imresize(image, size=(64, 64))
    i += 1
y_nonowl = np.zeros((130, 1))

test_set_nonowl = np.zeros((38, 64, 64, 3))
i = 0
for img in glob.glob("F:/Paul Gao/Documents/randombot/nonowlimages/*.jpg"):
    image = np.array(ndimage.imread(img, flatten=False))
    #print (i)
    train_set_nonowl[i] = scipy.misc.imresize(image, size=(64, 64))
    i += 1
y_nonowl_test = np.zeros((38, 1))

train_set_x = np.concatenate((train_set_owl, train_set_nonowl), axis=0)
train_set_y = np.concatenate((y_owl, y_nonowl), axis=0).T
test_set_x = np.concatenate((test_set_owl, test_set_nonowl), axis=0)
test_set_y = np.concatenate((y_owl_test, y_nonowl_test), axis=0).T

train_set_x = (train_set_x.reshape(train_set_x.shape[0], -1)).T / 255
test_set_x = (test_set_x.reshape(test_set_x.shape[0], -1)).T / 255

# training

def sigmoid(x):
    s = 1.0 / (1.0 + np.exp(-x))
    return s

def propagate(w, b, X, Y):
    m = X.shape[1]
    lamb = 20
    theta2 = w
    theta2[0][0] = 0
    A = sigmoid(np.matmul(w.T, X) + b)  # compute activation
    cost = (-1 / m) * np.sum(Y * np.log(A) + (1 - Y) * np.log(1 - A)) + lamb / (2 * m) * np.matmul(theta2, theta2.T) # compute cost

    dw = (1 / m) * np.matmul(X, (A - Y).T) + lamb/m * w
    dw[0][0] = (1 / m) * np.matmul(X, (A - Y).T)[0][0]
    db = (1 / m) * np.sum(A - Y)

    grads = {"dw": dw, "db": db}

    return grads, cost

def optimize(w, b, X, Y, num_iterations, learning_rate, print_cost=False):

    costs = []

    for i in range(num_iterations):
        grads, cost = propagate(w, b, X, Y)

        dw = grads["dw"]
        db = grads["db"]

        w -= learning_rate * dw
        b -= learning_rate * db

        if i % 100 == 0:
            costs.append(cost)

        if print_cost and i % 100 == 0:
            print("Cost after iteration %i: %f" % (i, cost))

    params = {"w": w, "b": b}

    grads = {"dw": dw, "db": db}

    return params, grads, costs

def predict(w, b, X):

    m = X.shape[1]
    Y_prediction = np.zeros((1, m))
    w = w.reshape(X.shape[0], 1)

    A = sigmoid(np.matmul(w.T, X) + b)

    for i in range(A.shape[1]):

        if A[0][i] <= 0.5:
            Y_prediction[0][i] = 0
        else:
            Y_prediction[0][i] = 1

    return Y_prediction

def model(X_train, Y_train, X_test, Y_test, num_iterations=2000, learning_rate=0.5, print_cost=False):
    """
    Builds the logistic regression model by calling the function you've implemented previously

    Arguments:
    X_train -- training set represented by a numpy array of shape (num_px * num_px * 3, m_train)
    Y_train -- training labels represented by a numpy array (vector) of shape (1, m_train)
    X_test -- test set represented by a numpy array of shape (num_px * num_px * 3, m_test)
    Y_test -- test labels represented by a numpy array (vector) of shape (1, m_test)
    num_iterations -- hyperparameter representing the number of iterations to optimize the parameters
    learning_rate -- hyperparameter representing the learning rate used in the update rule of optimize()
    print_cost -- Set to true to print the cost every 100 iterations

    Returns:
    d -- dictionary containing information about the model.
    """

    w = np.zeros((np.shape(X_train)[0], 1))
    b = 0

    parameters, grads, costs = optimize(w, b, X_train, Y_train, num_iterations, learning_rate, print_cost=False)

    w = parameters["w"]
    b = parameters["b"]

    Y_prediction_test = predict(w, b, X_test)
    Y_prediction_train = predict(w, b, X_train)

    print("train accuracy: {} %".format(100 - np.mean(np.abs(Y_prediction_train - Y_train)) * 100))
    print("test accuracy: {} %".format(100 - np.mean(np.abs(Y_prediction_test - Y_test)) * 100))

    d = {"costs": costs,
         "Y_prediction_test": Y_prediction_test,
         "Y_prediction_train": Y_prediction_train,
         "w": w,
         "b": b,
         "learning_rate": learning_rate,
         "num_iterations": num_iterations
         }

    return d

d = model(train_set_x, train_set_y, test_set_x, test_set_y, num_iterations = 2000, learning_rate = 0.005, print_cost = True)

def predict_nonlogical(w, b, X):

    w = w.reshape(X.shape[0], 1)

    A = sigmoid(np.matmul(w.T, X) + b)
    print (A)

    return A

pred = open('pred.pckl', 'wb')
pickle.dump(d, pred)
pred.close()

# print (d)
