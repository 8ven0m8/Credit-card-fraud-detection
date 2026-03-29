# Credit Card Fraud Detection

![Credit card fraud](https://www.bankdealguy.com/wp-content/uploads/2017/12/credit-card-banner.png)

## Overview

RandomForest, XGBoost, LightGBM and Logistic Regression models are stacked together and used to detect credit card fraud transactions. Two types of approach are implemented and the best out of them is choosen:
* Converting class weight to balanced for each model (scale position weight for XGBoost), which yielded f1 score of **0.85**
* Using undersampled dataset which yielded f1 score of **0.80**

Implemented StratifiedKFold, RobustScaler, GridSearchCV, StackingClassifier, Threshold Tuning and Confusion Matrix.  
### FastAPI:
https://credit-card-fraud-detection-2ia2.onrender.com/predict (Its a free render deployment so it may be sleeping)

Visit kaggle notebook :- https://www.kaggle.com/code/pranjalsapkota/credit-card-fraud-detection

## Dataset

The dataset contains transactions made by credit cards in September 2013 by European cardholders. 
https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud

Typical features in the dataset include:

* Time
* V1 ... V28
* Amount      

Target variable:

* **Class**

## Project Workflow

1) Environment setup  
 a) Importing packages  
 b) Loading dataset

2) Data manipulation  
 a) Null values  
 b) data category  
 c) Scaling values  
 d) Data splitting  
 e) Correlation matrix

3) Training model  
 a) Applying Stratified K fold and pipeline  
 b) Tuning Multiple models  
 c) Model Stacking  
 d) Threshold tuning   
 e) Final testing  

4) Undersampled dataset  
 a) creating dataset  
 b) model tuning  


## Model Used

* Random Forest Classifier
* XGBoost Classifier
* LightGBM Classifier
* Logistic Regressor

## Example Prediction Input

For API
<pre>
{
  "Time": 4462,
  "V1": -2.30334956758553,
  "V2": 1.759247460267,
  "V3": -0.359744743330052,
  "V4": 2.33024305053917,
  "V5": -0.821628328375422,
  "V6": -0.0757875706194599,
  "V7": 0.562319782266954,
  "V8": -0.399146578487216,
  "V9": -0.238253367661746,
  "V10": -1.52541162656194,
  "V11": 2.03291215755072,
  "V12": -6.56012429505962,
  "V13": 0.0229373234890961,
  "V14": -1.47010153611197,
  "V15": -0.698826068579047,
  "V16": -2.28219382856251,
  "V17": -4.78183085597533,
  "V18": -2.61566494476124,
  "V19": -1.33444106667307,
  "V20": -0.430021867171611,
  "V21": -0.294166317554753,
  "V22": -0.932391057274991,
  "V23": 0.172726295799422,
  "V24": -0.0873295379700724,
  "V25": -0.156114264651172,
  "V26": -0.542627889040196,
  "V27": 0.0395659889264757,
  "V28": -0.153028796529788,
  "Amount": 239.93
}
</pre>

Output
<pre>
{
  "result": "Fraud"
}
</pre>

## Packages Used

* Python
* Pandas
* NumPy
* Scikit-learn
* imblearn
* XGBoost
* LightGBM
* matplotlib
* seaborn
* Jupyter Notebook

## References

* Credit Card Fraud Detection Dataset
* Scikit-learn Documentation
* imblearn Documentation

