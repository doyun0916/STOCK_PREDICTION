from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.metrics import classification_report
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier

class dnn:
    def __init__(self, x_train, y_train):
        self.x_train = x_train
        self.y_train = y_train

    def train(self, s=0):
        if s == 0:
            clf = MLPClassifier(random_state=42, activation='tanh', alpha=0.0001, hidden_layer_sizes=(20,),
                                learning_rate='constant', max_iter=10000, solver='sgd')
            clf.fit(self.x_train, self.y_train)
            return clf
        else:
            clf = MLPClassifier(random_state=42)
            params = {
                'hidden_layer_sizes': [(10, 30, 10), (20,)],
                'activation': ['tanh', 'relu'],
                'solver': ['sgd', 'adam'],
                'alpha': [0.0001, 0.05],
                'learning_rate': ['constant', 'adaptive'],
                'max_iter': [10000, 20000, 30000]
            }
            gmlp = GridSearchCV(clf, params)
            gmlp.fit(self.x_train, self.y_train)
            print("\nBest parameters for MLP:", gmlp.best_params_)
            return gmlp


class randomForest:
    def __init__(self, x_train, y_train):
        self.x_train = x_train
        self.y_train = y_train

    def train(self, s=0):
        if s == 0:
            rf = RandomForestClassifier(random_state=42, criterion='gini', n_estimators=50)
            rf.fit(self.x_train, self.y_train)
            return rf
        else:
            rf = RandomForestClassifier(random_state=42)
            params = {
                    'n_estimators': [50, 100, 150, 200],
                    'criterion': ['gini', 'entropy']}
            grf = GridSearchCV(rf, params)
            grf.fit(self.x_train, self.y_train)
            print("\nBest parameters for RandomForest:", grf.best_params_)
            return grf


class logisticRegression:
    def __init__(self, x_train, y_train):
        self.x_train = x_train
        self.y_train = y_train

    def train(self, s=0):
        if s == 0:
            lr = LogisticRegression(solver="saga", random_state=42, penalty='elasticnet', l1_ratio=0, max_iter=10000)
            lr.fit(self.x_train, self.y_train)
            return lr
        else:
            lr = LogisticRegression(solver="saga", random_state=42, penalty='elasticnet')
            params = {
                    'l1_ratio': [0, 0.5, 1],
                    'max_iter': [10000, 20000, 30000],
                    }
            glr = GridSearchCV(lr, params)
            glr.fit(self.x_train, self.y_train)
            print("Best parameters for LogisticRegression:", glr.best_params_)
            return glr

class SVM:
    def __init__(self, x_train, y_train):
        self.x_train = x_train
        self.y_train = y_train

    def train(self):
        svmm = svm.SVC(random_state=42, probability=True)
        params = [
            {'C': [0.1, 1, 10], 'degree': [2, 3, 5], 'kernel': ['poly']},
            {'C': [0.1, 1, 10], 'gamma': [0.0001, 0.001, 0.01], 'kernel': ['linear', 'rbf']}, ]
        gsvm = GridSearchCV(svmm, params)
        gsvm.fit(self.x_train, self.y_train)
        print("Best parameters for SVM:", gsvm.best_params_)
        return gsvm

class voting:
    def __init__(self, model1, model2, model3, x_train, y_train):
        self.x_train = x_train
        self.y_train = y_train
        self.model1 = model1
        self.model2 = model2
        self.model3 = model3

    def train(self):
        voting_soft = VotingClassifier(
            estimators=[('model1', self.model1), ('model2', self.model2), ('model3', self.model3)],
            voting='soft')
        voting_soft.fit(self.x_train, self.y_train)
        return voting_soft

class stacking:
    def __init__(self, model1, model2, model3, x_train, y_train):
        self.x_train = x_train
        self.y_train = y_train
        self.model1 = model1
        self.model2 = model2
        self.model3 = model3

    def train(self):
        estimators = [('model1', self.model1),
                      ('model2', self.model2),
                      ('model3', self.model3)]
        stacking_clf = StackingClassifier(estimators=estimators,
                                          final_estimator=LogisticRegression(),
                                          cv=5)
        stacking_clf.fit(self.x_train, self.y_train)
        return stacking_clf


class validation_score:
    def __init__(self, model, test_x, test_y):
        self.test_x = test_x
        self.test_y = test_y
        self.model = model

    def score(self):
        pred = self.model.predict(self.test_x)
        clf_re = classification_report(self.test_y, pred)
        print("\n", clf_re, "\n")
        accuracy = accuracy_score(self.test_y, pred)
        print("\nAccuracy:", accuracy, "\n")

class prediction:
    def __init__(self, model, test_x):
        self.model = model
        self.test_x = test_x

    def eval(self):
        test_x = self.test_x.iloc[:, :6]
        test_x.columns = ['pc1', 'pc2', 'pc3', 'pc4', 'pc5', 'pc6']
        pred = self.model.predict(test_x)
        if pred == 0:
            print("하락")
        else:
            print("상승")
