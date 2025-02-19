from doubleml import DoubleMLData
import numpy as np

from doubleml.datasets import fetch_401K

data = fetch_401K(return_type='DataFrame')

dml_data = DoubleMLData(data, y_col='net_tfa', d_cols='e401',
                        x_cols=['age', 'inc', 'educ', 'fsize', 'marr',
                                'twoearn', 'db', 'pira', 'hown'])

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

ml_l_rf = RandomForestRegressor(n_estimators=500, max_depth=7,
                                max_features=3, min_samples_leaf=3)

ml_m_rf = RandomForestClassifier(n_estimators=500, max_depth=5,
                                 max_features=4, min_samples_leaf=7)

from xgboost import XGBClassifier, XGBRegressor

ml_l_xgb = XGBRegressor(objective="reg:squarederror", eta=0.1,
                        n_estimators=35)

ml_m_xgb = XGBClassifier(use_label_encoder=False,
                         objective="binary:logistic",
                         eval_metric="logloss",
                         eta=0.1, n_estimators=34)

from doubleml import DoubleMLPLR

np.random.seed(123)

dml_plr_tree = DoubleMLPLR(dml_data,
                           ml_l=ml_l_rf,
                           ml_m=ml_m_rf)

np.random.seed(123)

dml_plr_tree = DoubleMLPLR(dml_data,
                           ml_l=ml_l_rf,
                           ml_m=ml_m_rf,
                           n_folds=3,
                           n_rep=1,
                           score='partialling out')

dml_plr_tree.fit()

print(dml_plr_tree.coef)

print(dml_plr_tree.se)

print(dml_plr_tree.summary)

dml_plr_tree.bootstrap()
print(dml_plr_tree.confint(joint = True))


