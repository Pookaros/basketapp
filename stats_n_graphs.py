from sklearn.neighbors import KernelDensity
import numpy as np
from matplotlib.colors import ListedColormap
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import pandas as pd
import math
import pandas as pd
import seaborn as sb
from matplotlib import pyplot as plt

rng = np.random.RandomState(42)

def shot_density(dataset):
    img = mpimg.imread(r"D:\New folder\george\ML DL AI\AAA app\testplot.png")
    #sb.set(style='whitegrid')
    dataset["X"] = 1.25*dataset["X"] - 250
    dataset["Y"] = -(47/40)*dataset["Y"] + 470
    #sb.jointplot(x = 'X',y = 'Y',data = dataset, kind = 'hex', alpha=0.5)
    sb.jointplot(x = 'X',y = 'Y',data = dataset, kind = 'kde')
    plt.imshow(img, extent=(-350, 350, 0, 470), aspect='auto', alpha=0.5)
    plt.show()

    sb.jointplot(x = 'X',y = 'Y',data = dataset, kind = 'hex', alpha=0.5)
    plt.imshow(img, extent=(-250, 250, 0, 470), aspect='auto', alpha=0.5)
    plt.show()

def categorize_shot_data(shot_csv):
    df = pd.read_csv(shot_csv)
    category_df = pd.DataFrame(columns=["X","Y", "SuccessFlag"])
    values_x, values_y, success_flag =  [], [], []
    # Iterate through...
    for column in df.columns:
        # ...success columns and concat data with SuccessFlag as 1

        if "_X_success" in column:
            temp = [x for x in df[column].tolist() if x is not math.isnan(x)]
            values_x = values_x + temp
            success_flag = success_flag + [1] * len(temp)
            #category_df = pd.concat([category_df, pd.DataFrame({"X": values, "SuccessFlag": success_flag})], ignore_index=True)

        elif "_Y_success" in column:
            temp = [x for x in df[column].tolist() if x is not math.isnan(x)]
            values_y = values_y + temp
            # the flag was already put 6 lines above
            #category_df = pd.concat([category_df, pd.DataFrame({"Y": values, "SuccessFlag": success_flag})], ignore_index=True)

        # ...fail columns and concat data with SuccessFlag as 0
        elif "_X_fail" in column:
            temp = [x for x in df[column].tolist() if x is not math.isnan(x)]
            values_x = values_x + temp
            success_flag = success_flag + [0] * len(temp)
            #category_df = pd.concat([category_df, pd.DataFrame({"X": values, "SuccessFlag": success_flag})], ignore_index=True)
        
        elif "_Y_fail" in column:
            temp = [x for x in df[column].tolist() if x is not math.isnan(x)]
            values_y = values_y + temp
            # the flag was already put 6 lines above
            #category_df = pd.concat([category_df, pd.DataFrame({"Y": values, "SuccessFlag": success_flag})], ignore_index=True)
        
        else:
            print("Data missmatch  in categrozize_shot_data: unrecognized column " + column)
    
    # putting the data in the data frame
    category_df = pd.concat([category_df, pd.DataFrame({"X": values_x, "Y": values_y, "SuccessFlag": success_flag})], ignore_index=True)
    
    #removing the na data
    category_df = category_df.dropna()

    # reseting the index of the frame 
    category_df = category_df.reset_index(drop=True)
    
    return category_df
