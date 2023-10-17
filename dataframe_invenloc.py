import pyodbc
import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

class inv_loc:
    def __init__(self,connection_string):
        self.connection_string = connection_string
        
    def get_data(self):
        

        with pyodbc.connect(self.connection_string) as connection:
            query = """
            SELECT 
                code,
                description,
                contents
            FROM proc_invlocations
            WHERE 
                inventory = 39 
            """
            cursor = connection.cursor()
            cursor.execute(query)
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()
            cursor.close()
        if len(rows) > 0:
            df = pd.DataFrame.from_records(rows, columns=columns)

            # Filter out unwanted codes using Pandasmodel->setFilter(filter);
            excluded_codes = ['BHRE', 'REW','RET','INWA', 'QC', 'XRAY', 'DESP', 'TFR1', 'TDA1', 'TDA2', 'TDA3', 
                              'UNL', 'TDA4', 'TDA5', 'TDA6', 'TDA7', 'TDA8', 'TDA9', 'TDA10', 'TDA11']
            df = df[~df['code'].isin(excluded_codes)]
            
            return df
        else:
            return None
        

# inv_instance = inv_loc(connection_string)
#
# # Get the data
# df = inv_instance.get_data()
# print(df)
# dtype_contents = df['contents'].dtype
#
# values_to_add1 = ['A0' + str(i) for i in range(15, 96, 10)]
# # Check if these values are not already present in the 'code' column
# values_to_add1 = [value for value in values_to_add1 if value not in df['code'].values]
# # Create a new dataframe with these values
# df_to_add1 = pd.DataFrame({'code': values_to_add1})
# # Concatenate this dataframe to the original one
# df = pd.concat([df, df_to_add1], ignore_index=True)
#
#
#
# # Generate the sequence of values
# values_to_add = ['A' + str(i) for i in range(105, 276, 10)]
# # Create a new dataframe with these values
# df_to_add = pd.DataFrame({'code': values_to_add})
# # Concatenate this dataframe to the original one
# df = pd.concat([df, df_to_add], ignore_index=True)
# df.fillna(0, inplace=True)# changing the value of the shelf to 0
#
#
# # # Correcting the sorting and string conversion
# df = df.sort_values(by='code')
# df["code"] = df["code"].astype(str)
# df.info()


# def filter_by_letter(letter=None):
#     if letter:
#         return df[df['code'].str.startswith(letter)]
#     else:
#         return df

#
# print(filter_by_letter('A'))
# print(len(filter_by_letter('B')))
# print(len(filter_by_letter('C')))
# print(len(filter_by_letter('E')))
# print((filter_by_letter('F')))
# print(len(filter_by_letter('G')))
# print(len(filter_by_letter('H')))
# print(len(filter_by_letter('I')))