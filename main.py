import PySimpleGUI as sg
import pandas as pd
import cx_Oracle

sg.theme("DarkTeal2")
layout = [[sg.T("")], [sg.Text("Choose a folder: "), sg.Input(key="-IN2-" ,change_submits=True), sg.FileBrowse(key="-IN-")],[sg.Button("Submit")], [sg.Button('Save',key='-FILE-')]]

###Building Window
window = sg.Window('My File Browser', layout, size=(600,150))

    
while True:
    event, values = window.read()
    #print(values["-IN2-"])
    if event == sg.WIN_CLOSED or event=="Exit":
        break
    elif event == "Submit":
        print(values["-IN-"])
        df =pd.read_csv(values["-IN-"])
        print(df)

        
        def ull(Product_ID = None):
            
            filters = []
            conStr ='U6077614/Vqt44GJVUX7ZZ7ua4oiGY@c384cmkcdmdbp.int.thomsonreuters.com/cdmdb_rw.int.thomsonreuters.com'
            conn = None
            conn = cx_Oracle.connect(conStr)
            cur = conn.cursor()
            query = "SELECT DISTINCT PLI__C FROM CDM_SFDC.DQ_PRODUCT2 WHERE PLI__C LIKE"

            if Product_ID is not None:
                filters.append(Product_ID)

            new_query= []
            for x in filters:
                y = query+ ' '+"'"+x+'%'+"'"+' '+'AND ROWNUM <= 200'
                new_query.append(y)

            s = ' '.join(new_query)

            with conn.cursor() as cur:
                cur.execute(s)
                dbRows = cur.fetchall()
                colNames = [row[0] for row in cur.description]
                df = pd.DataFrame.from_records(dbRows, columns=colNames)
        
            return df
        
        df1 = df.values.tolist()
        df2 = pd.DataFrame()
        #print(df1)
        for x in df1:
            x = ''.join(x)
            result = ull(x)
            query_df = pd.DataFrame(result)
            #print(query_df)
            df2 = df2.append(query_df,
            ignore_index=True, sort=False)
            print = sg.Print
        print(df2)
