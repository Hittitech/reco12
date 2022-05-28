import profile
import pandas as pd
from pandas_profiling import ProfileReport



def profile():
    df=pd.read_csv('./images/attendance.csv')
    print(df)

    profile=ProfileReport(df)
    profile.to_file(output_file="./templates/attendance.html")
    return 0