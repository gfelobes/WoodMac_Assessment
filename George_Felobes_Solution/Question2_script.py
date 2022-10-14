import pandas as pd
import numpy as np 
import datetime as dt



class question2:  
    def __init__(self, IP, bi, Di, Dmin, well_life):
        # initialize variables 
        self.IP = IP
        self.bi = bi
        self.Di = Di
        self.Dmin = Dmin
        self.well_life = well_life

        # run functions
        self.mop()
        self.hyperbolic_function()
        self.decline_rate()
        self.forecast_prod()
        self.volume()
        print(f"The resulting Arps model: {self.main_df}")


    def mop(self):
        mop = np.arange(1,12*25 + 1)
        self.main_df = pd.DataFrame(mop, index=mop, columns = ["mop"])
        return self.main_df


    def hyperbolic_function(self):
        self.main_df["hyperbolic_prod"] = self.main_df["mop"].apply(lambda x: (1 + self.bi * self.Di * (x - 1)) ** (-1 / self.bi))
        return self.main_df

    def decline_rate(self):
        self.main_df["hyperbolic_dec_rate"] =  self.main_df["hyperbolic_prod"].pct_change() *-1
        self.main_df.loc[1,"hyperbolic_dec_rate"] = 1
        self.D_min = 1 - (1 - self.Dmin) ** (1/12)
        self.main_df["dec_rate"] = self.main_df['hyperbolic_dec_rate']
        self.main_df.loc[self.main_df['hyperbolic_dec_rate'] < self.D_min, "dec_rate"] = self.D_min
        return self.main_df

    def forecast_prod(self):
        self.main_df.loc[1, 'forecast_prod'] = self.IP
        for i in range(2, len(self.main_df)):
            self.main_df.loc[i, 'forecast_prod'] = self.main_df.loc[i - 1, 'forecast_prod'] * (1-self.main_df.loc[i, 'dec_rate'])
        return self.main_df

    def volume(self):
        # Use start date and datetime package to create a new column
        self.main_df["date"] = pd.date_range(dt.datetime(2020,1,1), periods = self.well_life*12, freq='m')

        # Use the datetime package to multiple the forecasted production by the number of days in that month 
        self.main_df["volume"] = self.main_df["forecast_prod"] * (self.main_df["date"].dt.daysinmonth)
        return self.main_df
    
    def result(self):
        return self.main_df.to_csv("GeorgeF_Question2_result.csv")



# Define inputs
IP, bi, Di, Dmin, well_life = 160, 1.5, 2.3, 0.1, 25
# Run class object 
s = question2(IP, bi, Di, Dmin, well_life)
s
# uncomment to generate result as csv file 
s.result()