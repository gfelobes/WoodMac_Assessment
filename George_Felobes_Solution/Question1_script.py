
import pandas as pd  
class question1:  
    def __init__(self, path, year):
        # initialize variables 
        self.path = path
        self.year = year

        # run functions
        self.data_input()
        self.format_prod_data()
        self.join_dfs()
        self.result = self.filter_sum()
        print(f"The production in year {self.year}, where the breakeven is less than price input is {self.result}")


    def data_input(self):
        self.prod_data = pd.read_excel(self.path, sheet_name = "Production_Vol")
        self.price_inputs = pd.read_excel(self.path, sheet_name = "Price_Inputs")
        return self.prod_data, self.price_inputs


    def format_prod_data(self):
        self.prod_data_formatted = self.prod_data.melt(id_vars=["ASSET", "BREAKEVEN"], 
        var_name="YEAR", 
        value_name="Value")
        return self.prod_data_formatted

    def join_dfs(self):
        self.merged_data = pd.merge(self.prod_data_formatted, self.price_inputs, on = "YEAR")
        return self.merged_data

    def filter_sum(self):
        filter_condition = (self.merged_data["YEAR"] == self.year) & (self.merged_data["BREAKEVEN"] < self.merged_data["PRICE_INPUT"])
        self.summed_df = self.merged_data[filter_condition].sum()
        return self.summed_df['Value']



# inputs: 
path = r"1. Python Asset prodn sum by BkEven June 2019.xlsx"
year = 3

# Run class object 
question1(path, year)
