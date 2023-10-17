from databasefinder import connection_string
import pyodbc
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


class PalletFilled:
    def __init__(self, connection_string):
        self.connection_string = connection_string

    def get_data(self):
        with pyodbc.connect(self.connection_string) as connection:
            query = """
            SELECT 
    invl.code as LocationID, 
    LEFT(invl.code,1) as Aisle, 
    CASE
        WHEN ISNUMERIC(SUBSTRING(invl.code,2,2)) = 1 THEN CAST(SUBSTRING(invl.code,2,2) as int)
        ELSE NULL
    END as Row,
    RIGHT(invl.code,1) as [Level], 
    mat.code as productCode, 
    pal.sscc as IPN, 
    COUNT(pk.nregs) as Qty, 
    ROUND(SUM(pk.weight), 2) as Weight
FROM 
    proc_invlocations invl WITH (NOLOCK) 
LEFT OUTER JOIN 
    proc_collections pal WITH (NOLOCK) on pal.invlocation = invl.id and pal.inventory=invl.inventory
INNER JOIN 
    proc_packs pk on pal.id = pk.pallet 
INNER JOIN 
    proc_materials mat on mat.material = pk.material
WHERE 
    invl.inventory=39 
GROUP BY 
    invl.code, pal.id, mat.code, pal.sscc
ORDER BY 
    invl.code ASC
"""
            cursor = connection.cursor()
            cursor.execute(query)
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()
            cursor.close()

        if len(rows) > 0:
            df = pd.DataFrame.from_records(rows, columns=columns)
            # Filter out unwanted codes using Pandas
            excluded_codes = ['BHRE', 'REW', 'RET', 'INWA', 'QC', 'XRAY', 'DESP', 'TFR1', 'TDA1', 'TDA2', 'TDA3',
                              'UNL', 'TDA4', 'TDA5', 'TDA6', 'TDA7', 'TDA8', 'TDA9', 'TDA10', 'TDA11']
            df = df[~df['LocationID'].isin(excluded_codes)]
            # Assuming df is your DataFrame and 'column_to_drop' is the name of the column to be dropped
            df = df.drop(columns=['Aisle','IPN','productCode','Row','Level'])
            # Assuming df is your DataFrame and you want to group by 'LocationID' and sum the other columns
            df = df.groupby('LocationID').sum().reset_index()

            return df
        else:
            return None


# # Create an instance
# pal_instance = PalletFilled(connection_string)
# # Get all the data without specifying a rack code
# df_all = pal_instance.get_data()
#
# # Print or do other things with the data
# print(df_all)
# df_all.info()
