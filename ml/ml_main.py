import pandas as pd
import preprocessing as sp
import models

years_data = pd.read_csv("./_5years_data.csv")
x_train, x_test, y_train, y_test = sp.data(years_data)

# Training with data
Rf = models.randomForest(x_train, y_train).train()          # RandomForest
models.validation_score(Rf, x_test, y_test).score()

Dnn = models.dnn(x_train, y_train).train()          # dnn
models.validation_score(Dnn, x_test, y_test).score()

Lr = models.logisticRegression(x_train, y_train).train()    # Logistic Regression
models.validation_score(Lr, x_test, y_test).score()

# Voting_soft = models.voting(Rf, Lr, Dnn, x_train, y_train).train()        # Voting
# print("\nVoting_soft's score: \n")
# models.validation_score(Voting_soft, x_test, y_test).score()

Stacking = models.stacking(Rf, Lr, Dnn, x_train, y_train).train()   # Stacking
print("\nStacking's score: \n")
models.validation_score(Stacking, x_test, y_test).score()

sample = [[20210216, 11300, 11350, 11050, 11300, 85467]]           # today's result 날짜, 시, 고, 저, 종, 거
t_sample = pd.DataFrame(sample)
result = models.prediction(Stacking, t_sample)
result.eval()
