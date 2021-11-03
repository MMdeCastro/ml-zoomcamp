#!/usr/bin/env python
# coding: utf-8


# Goal: to predict if the client will subscribe a fix term deposit after a marketing campaign.

# Target variable: 'deposit', i.e., has the client subscribed a term deposit? (binary: 'yes','no')

# Data: dowloaded from Kaggle(https://www.kaggle.com/janiobachmann/bank-marketing-dataset). 

# Data Citation: A Data-Driven Approach to Predict the Success of Bank Telemarketing. S. Moro, P. Cortez and P. Rita. Decision Support Systems, Elsevier, 62:22-31, June 2014
 
# See accompaying jupyter notebook with EDA: https://github.com/MMdeCastro/ml-zoomcamp/tree/main/Midterm_project

import pickle

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score
import xgboost as xgb


# 0. Parameters
# xgboost
eta = 0.3 #default is 0.3
max_depth = 4 # default is 6
min_child_weight = 1 # default is 1    
objective = 'binary:logistic'
nthread = 8
eval_metric = 'auc' # otherwise it uses logloss
seed =  1
verbosity = 1
# cross-validation
n_fold = 5
# save file
output_file = f'model_maxdepth={max_depth}.bin'

# 1. Data load
# from 'https://www.kaggle.com/janiobachmann/bank-marketing-dataset
df = pd.read_csv('bank.csv')

# 2. Data preparation

# replace with numbers 0 (negative or 'no') and 1 (positive or 'yes')
df.default = (df.default == 'yes').astype(int)
df.loan = (df.loan == 'yes').astype(int)
df.housing = (df.housing == 'yes').astype(int)
df.deposit = (df.deposit == 'yes').astype(int)

# get the names of the cat and num features
categorical = df.select_dtypes(include=['object']).columns.tolist()
numerical = df.select_dtypes(include=['int64']).columns.tolist()
numerical.remove('deposit')

# do the train/val/test split

# separate train + validation (= full) and test
df_full_train, df_test = train_test_split(df, test_size=0.2, random_state=1)

# separate the target 
y_train = df_full_train.deposit.values
y_test = df_test.deposit.values

# reset indexes after splitting shuffling
df_train = df_full_train.reset_index(drop=True)
df_test = df_test.reset_index(drop=True)

# encode and scale... 
dv = DictVectorizer(sparse=False) # for the categorical features
scaler = StandardScaler() # for the numerical features

# ... the full_training daset
train_dict = df_full_train[categorical].to_dict(orient='records')
X_train_cat = dv.fit_transform(train_dict) # encode the categorical features

X_train_num = df_full_train[numerical].values
X_train_num = scaler.fit_transform(X_train_num) # scale the numerical features

X_train = np.column_stack([X_train_num, X_train_cat]) # join the matrices

# ... the test dataset  
test_dict = df_test[categorical].to_dict(orient='records')
X_test_cat = dv.transform(test_dict) # encode the categorical features

X_test_num = df_test[numerical].values
X_test_num = scaler.transform(X_test_num) # scale the numerical features

X_test = np.column_stack([X_test_num, X_test_cat]) # join the matrices

# 3. Model training XGBoost

# create the DMatrices
features = numerical + dv.get_feature_names()
dtrain = xgb.DMatrix(X_train, label=y_train, feature_names= features)
dtest = xgb.DMatrix(X_test, feature_names= features) #label = y_test, feature_names= features)

# train the model
xgb_params = {
    'eta': eta,
    'max_depth': max_depth,
    'min_child_weight': min_child_weight,
    
    'objective': objective,
    'nthread': nthread,
    'eval_metric': eval_metric,
    
    'seed': 1,
    'verbosity': 1,
}
model = xgb.train(xgb_params, dtrain, num_boost_round=25)

# apply the model
y_pred = model.predict(dtest)
xgb_auc =roc_auc_score(y_test, y_pred)
print('xgb_auc')

# cross-validate the model
dtrain = xgb.DMatrix(X_train, label=y_train, feature_names=features)
cv_results = xgb.cv(dtrain=dtrain, params=xgb_params, nfold=n_fold, num_boost_round=25,as_pandas=True,seed =1)
print('mean and std of the ROC AUC predictions on train and test data in the last xgboost round:')
print(cv_results.iloc[-1])

# 4. Save the model https://scikit-learn.org/stable/modules/model_persistence.html 
# look at the size of the model: ls -lh model_maxdepth\=4.bin # it is 58K

with open(output_file, 'wb') as f_out:
    pickle.dump((dv, scaler, model), f_out)
    # use pickle function "dump" to save the model 
    # and the DictVect (dv) for the predict function 

print(f'the model is saved to {output_file}')
