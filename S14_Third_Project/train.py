#!/usr/bin/env python
# coding: utf-8

# Goal: to predict binary target 'HeartDisease'

# Data: dowloaded from Kaggle(https://www.kaggle.com/fedesoriano/heart-failure-prediction) 

# See accompaying jupyter notebook with EDA at the Session 12 Capstone project folder in: https://github.com/MMdeCastro/ml-zoomcamp

import pickle

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import roc_auc_score
from sklearn.ensemble import RandomForestClassifier

# 0. Parameters:

# Random Forest
n_estimators     = 50
min_samples_leaf = 5
max_depth        = 10
random_state     = 1
t                = 0.4  # decision threshold
# Cross-validation
n_fold           = 5
# save file
output_file = 'model_RF_t=0{}.bin'.format(int(t*10))

# 1. Data load

df = pd.read_csv("heart.csv")

# 2. Data preparation

# convert quantitive values that should be qualitative, here: low and high in FastingBS
new_values = {0: 'L', 1: 'H'}
df.FastingBS = df.FastingBS.map(new_values)

categorical = df.select_dtypes(include=['object']).columns.tolist()
numerical = df.select_dtypes(include=['int64','float64']).columns.tolist()
numerical.remove('HeartDisease')

# drop unrealistic null values
index_to_drop = list(df.loc[(df.RestingBP == 0) | (df.Cholesterol == 0)].index)
df.drop(index_to_drop, inplace=True)


# do the train/val/test split

# separate train + validation (= full) and test
df_full_train, df_test = train_test_split(df, test_size=0.2, random_state=1)

# separate the target 
y_train = df_full_train.HeartDisease.values
y_test = df_test.HeartDisease.values

# reset indexes after splitting shuffling
df_train = df_full_train.reset_index(drop=True)
df_test = df_test.reset_index(drop=True)
del df_test['HeartDisease'] # remove target


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

# 3. Model training 

RF = RandomForestClassifier(n_estimators=n_estimators,
                            max_depth=max_depth,
                            min_samples_leaf=min_samples_leaf,
                            random_state=1)
model = RF.fit(X_train, y_train)
y_pred = RF.predict_proba(X_test)[:, 1]
acc = accuracy_score(y_test, y_pred >= t) 
f1  = f1_score(y_test, y_pred >= t) 
auc = roc_auc_score(y_test, y_pred)
print('For the test dataset:','ACC:', acc.round(3), 'F1:', f1.round(3),'ROC AUC:', auc.round(3))

# 4. Save the model https://scikit-learn.org/stable/modules/model_persistence.html 
# look at the size of the model: ls -lh model_RF.bin # it is 2MB

with open(output_file, 'wb') as f_out:
    pickle.dump((dv, scaler, model), f_out)
    # use pickle function "dump" to save the model 
    # and the DictVect (dv) for the predict function 

print(f'The model is saved to {output_file}')

