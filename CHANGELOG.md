# Changelog

## v0.2 (2025-01-15)

### Improvements
- **Model Enhancement**: Upgraded from LinearRegression to RandomForestRegressor with hyperparameter tuning
- **Performance**: RMSE improved from 54.46 to 53.39 (1.96% improvement)
- **Hyperparameter Optimization**: Added GridSearchCV with 5-fold cross-validation
- **Best Parameters**: n_estimators=500, max_depth=None, max_features="sqrt", min_samples_leaf=4, min_samples_split=10

### Technical Changes
- Added comprehensive parameter grid search
- Maintained same preprocessing pipeline (StandardScaler)
- Preserved seed=7 for reproducibility
- Enhanced model persistence with best parameters logging

## v0.1 (2025-01-15)

### Initial Release
- **Baseline Model**: LinearRegression with StandardScaler preprocessing
- **Performance**: RMSE 54.46 on test set (89 samples)
- **Features**: All 10 diabetes dataset features (age, sex, bmi, bp, s1-s6)
- **API**: FastAPI service with /health and /predict endpoints
- **Infrastructure**: Docker containerization with multi-stage build