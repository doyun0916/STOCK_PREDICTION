import pandas as pd
import ml.preprocessing as sp
import ml.models as models
import ml.creon_api_modified as creon_api_modified
import ml.krx as krx

def prediction(code):
    ############################################## data preparation ####################################################
    ####################### (past data from creon & krx) ################
    ### Get past data from creon ##
    new = creon_api_modified.CpStockChart()
    d, r = creon_api_modified.past_data(code, new)

    start_date = d["dates"][-1]
    creon_past_data = pd.DataFrame(d)
    result_final = pd.DataFrame(r)

    ## Past data from krx ##

    krx_data = krx.krx_info(start_date, code[1:])
    krx_past_data = krx_data.iloc[:-1]

    ## Concat above two data with results ##

    final_past_rough = pd.concat([creon_past_data, krx_past_data], axis=1)
    final_past_rough.columns = [i for i in range(28)]
    final_past_data = pd.concat([final_past_rough, result_final], axis=1)

    ################### Today's data from creon & krx ########################

    name, creon_today_rough = new.today_info(code)
    krx_today_rough = krx_data.iloc[-1].values.tolist()
    final_today_rough = creon_today_rough + krx_today_rough
    final_today_data = pd.DataFrame([final_today_rough])

    ################## 외국인 ,기관계 등 지표 #############################
    #print(creon_api_modified.foreign_info(code))

    ########################################### Data preprocessing ########################################################
    x_train, x_test, y_train, y_test, final_today_data2 = sp.data(final_past_data, final_today_data)

    ##########################################  Model creation ###########################################################
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
    #print("\nStacking's score: \n")
    models.validation_score(Stacking, x_test, y_test).score()

    ################################ prediction ###########################################################################

    result = models.prediction(Stacking, final_today_data2)
    return result.eval(name), name
