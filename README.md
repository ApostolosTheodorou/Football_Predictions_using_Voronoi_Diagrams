# Football_Predictions_using_Voronoi_Diagrams

While the Voronoi diagram is being widely used in football analysis with several ways, it has not been utilized yet as a method to predict the outcome of a match. The purpose of this project is to predict the outcomes of the matches of the second half of the greek Super League of the season 2021-2022, based on the Voronoi diagrams of the highlights of the first half of the league. In order to achieve this the highlights were divided in 5 classes depending on the significance of the opportunity. Then a classifier was trained using the Logistic Regression algorithm to classify the attempts of the second half of the league and thus predict the outcomes of the matches. The maximum prediction rate was observed to be around 60%. 

## Execution

To run an evaluation of the tested classifiers navigate to the "code/classifier_selection" directory and run:

-$ python3 evaluateClassifier.py

 Estimated time for 1 fold: 12 min.

* If you want to run multiple folds create more folds directories with the structure of the existing fold and name the Fold-2, Fold-3 etc. Then change the number of folds in file evaluateClassifier.py line 16.


