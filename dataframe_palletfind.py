import pyodbc
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


class PalletLocation:
    def __init__(self, connection_str):
        self.connection_string = connection_str

    def get_data(self, rack_code):
        with pyodbc.connect(self.connection_string) as connection:
            query = """
            SELECT 
                invl.code as LocationID, 
                LEFT(invl.code,1) as Aisle, 
                CAST(SUBSTRING(invl.code,2,2) as int) as Row, 
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
                invl.inventory=39 and invl.code = ? 
            GROUP BY 
                invl.code, pal.id, mat.code, pal.sscc
            ORDER BY 
                invl.code asc
            
            """
            cursor = connection.cursor()
            cursor.execute(query, rack_code)
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()
            cursor.close()
        if len(rows) > 0:
            df = pd.DataFrame.from_records(rows, columns=columns)
            return df
        else:
            return None


