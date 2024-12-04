from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from dataPreprocessing import makeCsv, scaleData, defineTrainingAndTestingSets
import metrics

FOLDS= 5

clf= LogisticRegression()
param_grid = { 
    'class_weight': []
}

for w1 in [1.05, 1.10, 1.15, 1.20, 1.25, 1.3, 1.35]:
        for w2 in [1.10, 1.20, 1.30, 1.40]:
                for w3 in [0.9, 0.85, 0.8, 0.75, 0.7 , 0.65]:
                        for w4 in [1.0, 1.1, 1.15, 1.2, 1.25, 1.3, 1.35, 1.4]:
                                for w5 in [0.85, 0.95, 1.0, 1.05, 1.1, 1.15, 1.2]:
                                        param_grid['class_weight'].append({1:w1, 2:w2, 3:w3, 4:w4, 5:w5})

clfCV=GridSearchCV(estimator=clf, param_grid=param_grid)
for fold in range(1,FOLDS+1):
        X_train, Y_train, X_test, Y_test= defineTrainingAndTestingSets(fold)
        X_test, X_train= scaleData(X_test, X_train)
        print(f'FOLD {fold}')
        clfCV= clfCV.fit(X_train, Y_train) 
        y_pred= clfCV.predict(X_test)  
        print('BEST PARAMETERS:\n')
        print (clfCV.best_params_)
        print('\n')
        avPrecision, avRecall, prec, rec= metrics.printMetrics(y_pred, Y_test)