import numpy as np
import matplotlib.pyplot as plt
import sklearn as sk 
import sklearn.model_selection
import sklearn.tree
import pandas as pd
import xgboost
#%%
df_labeled = pd.read_csv('/Users/koushalsmodi/Desktop/BSDS200/SQL/SpaceshipTitanic/train.csv')
df_test = pd.read_csv('/Users/koushalsmodi/Desktop/BSDS200/SQL/SpaceshipTitanic/test.csv')

df_train, df_val = sk.model_selection.train_test_split(df_labeled, train_size=.8)
#%%
columns = ['VIP', 'RoomService', 'CryoSleep', 'ShoppingMall', 'Spa',
           'VRDeck', 'Age']

X_train = df_train[columns]
y_train = df_train['Transported']

X_val = df_val[columns]
y_val = df_val['Transported']
X_test = df_test[columns]

#%%

impute_vals = { 'Age':df_train['Age'].mean(),
               'RoomService': df_train['RoomService'].mode()[0],
               'CryoSleep': False,
               'FoodCourt': df_train['FoodCourt'].mode()[0],
               'ShoppingMall':df_train['ShoppingMall'].mode()[0],
               'Spa':df_train['Spa'].mode()[0],
               'VRDeck':df_train['VRDeck'].mode()[0],
                'VIP':False
        }

X_train = X_train.fillna(impute_vals)
X_val = X_val.fillna(impute_vals)
X_test = X_test.fillna(impute_vals)

#%%
# X_train['HomePlanet_Earth'] = (df_train['HomePlanet'] == 'Earth').astype('float')
# X_train['HomePlanet_Europa'] = (df_train['HomePlanet'] == 'Europa').astype('float')
# X_train['HomePlanet_Mars'] = (df_train['HomePlanet'] == 'Mars').astype('float')


# X_val['HomePlanet_Earth'] = (df_val['HomePlanet'] == 'Earth').astype('float')
# X_val['HomePlanet_Europa'] = (df_val['HomePlanet'] == 'Earth').astype('float')
# X_val['HomePlanet_Mars'] = (df_val['HomePlanet'] == 'Earth').astype('float')

# X_test['HomePlanet_Earth'] = (df_test['HomePlanet'] == 'Earth').astype('float')
# X_test['HomePlanet_Europa'] = (df_test['HomePlanet'] == 'Earth').astype('float')
# X_test['HomePlanet_Mars'] = (df_test['HomePlanet'] == 'Earth').astype('float')

X_train['FamilySize'] = (df_train['PassengerId'].str.split('_').apply(lambda x:len(x)))
X_val['FamilySize'] = (df_val['PassengerId'].str.split('_').apply(lambda x:len(x)))
X_test['FamilySize'] = (df_test['PassengerId'].str.split('_').apply(lambda x:len(x)))

X_train['TRP'] = (df_train['Destination'] == 'TRAPPIST-1e').astype('float')
X_train['Can'] = (df_train['Destination'] == '55 Cancri e').astype('float')
X_train['PSO'] = (df_train['Destination'] == 'PSO J318.5-22').astype('float')

X_val['TRP'] = (df_val['Destination'] == 'TRAPPIST-1e').astype('float')
X_val['Can'] = (df_val['Destination'] == '55 Cancri e').astype('float')
X_val['PSO'] = (df_val['Destination'] == 'PSO J318.5-22').astype('float')

X_test['TRP'] = (df_test['Destination'] == 'TRAPPIST-1e').astype('float')
X_test['Can'] = (df_test['Destination'] == '55 Cancri e').astype('float')
X_test['PSO'] = (df_test['Destination'] == 'PSO J318.5-22').astype('float')
#%%

from xgboost import XGBClassifier
clf = XGBClassifier(
    n_estimators = 500,
    max_depth= 4, 
    learning_rate = .01,
    subsample=.8,
    colsample_bytree = .8
)
clf.fit(X_train, y_train)

# clf = XGBClassifier(n_estimators = 1000, early_stopping_rounds =  10)
# clf.fit(X_train, y_train, eval_set = [(X_val, y_val)])

y_pred = clf.predict(X_val)
acc_val = np.mean(y_pred == y_val)

print(f'acc_val: {acc_val}')

y_pred_test = clf.predict(X_test)
y_pred_test = y_pred_test== 1
dct = {'PassengerId': df_test['PassengerId'], 
       'Transported': y_pred_test}

kaggle_sub = pd.DataFrame(dct)
kaggle_sub.to_csv('my_Spaceship_titanic_submission11.csv', index = False)
# acc_val: 0.78205865439908
