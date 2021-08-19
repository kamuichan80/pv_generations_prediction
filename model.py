import multiprocessing
from time import time
import xgboost as xgboost
def model():
    xgb= xgboost.XGBRegressor(n_jobs = multiprocessing.cpu_count(),n_estimators = 400, max_depth = 4, learning_rate = 0.1)
    return xgb

if __name__ == '__main__':
    start_time = time.time()
    print("model make start", flush=True)
    model()
    print("model make done", flush=True)