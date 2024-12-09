# Football_Predictions_using_Voronoi_Diagrams

While the Voronoi diagram is being widely used in football analysis with several ways, it has not been utilized yet as a method to predict the outcome of a match. The purpose of this project is to predict the outcomes of the matches of the second half of the greek Super League of the season 2021-2022, based on the Voronoi diagrams of the highlights of the first half of the league. In order to achieve this the highlights were divided in 5 classes depending on the significance of the opportunity. Then a classifier was trained using the Logistic Regression algorithm to classify the attempts of the second half of the league and thus predict the outcomes of the matches. The maximum prediction rate was observed to be around 60%. 

## Execution

To run an evaluation of the tested classifiers navigate to the "code/classifier_selection" directory and run:

-$ python3 evaluateClassifier.py

 Estimated time for 1 fold: 12 min.

* If you want to run multiple folds create more folds directories with the structure of the existing fold and name them Fold-2, Fold-3 etc. Then change the number of folds in file evaluateClassifier.py line 16.






To run a prediction for future or completed matches move the savedModels and matchdays directories in the code/prediction directory and run:

-$python3 driver.py -ma <future>/<completed> -f <first matchday of predictions> -l <last matchday of predictions> -mo <model path> -s <absolute>/<probabilistic>/<cumulative>

Example: $python3 driver.py -ma future -f 20 -l 26 -mo ./savedModels/RandomForest_Olympiacos_Train_1_13_Test_14_26.skops -s probabilistic





To train a new model run the following code:

-$python3 train_model.py -p <path to matchdays directory> -t <team> -c <classifier> -str <starting training set matchday> -etr <ending training set matchday> -ste <starting test set matchday> -ete <ending test set matchday> -s <model's name>

where:
* team is a three character string with possible values: All (for all teams to contribute to the building of the model), aek, ion, ari, ofi, oly, atr, pan, ast, pao, apo, the, gia, vol, lam
* classifier possible values: Decision Tree, SVC, Random Forest, Nearest Neighbors, Naive Bayes, Neural Network, Multinomial Logistic Regression
* arguments refering to matchdays can receive integer values from 1 to 26
* the name of your model (.skops file extension is added by default)
Example: -$python3 train_model.py -p ./matchdays -t oly -c Random Forest -str 1 -etr 13 -ste 14 -ete 26 -s RandomForest_Olympiacos_Train_1_13_Test_14_26
