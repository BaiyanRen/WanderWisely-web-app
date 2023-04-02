import pymysql
import pandas as pd
import helper_functions as uf
conn, engine = uf.conn_to_db()

def get_park(amenity_names,activity_names):
        amenity_names = "','".join(amenity_names)
        activity_names="','".join(activity_names)
        query_amenity = f"select name,parkName from wanderwisely.amenity_related_parks where name in ('{amenity_names}')"
        query_activity= f"select name,parkName from wanderwisely.activity_related_parks where name in ('{activity_names}')"
        df_amenity = uf.import_data(query_amenity, conn)
        df_activity = uf.import_data(query_activity, conn)
        
        df_amenity['parkname_count'] = df_amenity.groupby('parkName')['name'].transform('count')
        df_amenties = df_amenity[['parkName', 'parkname_count']].drop_duplicates(subset='parkName').reset_index(drop=True)
        
        df_activity['parkname_count'] = df_activity.groupby('parkName')['name'].transform('count')
        df_activities = df_activity[['parkName', 'parkname_count']].drop_duplicates(subset='parkName').reset_index(drop=True)
        df_merged = pd.merge(df_amenties, df_activities, on='parkName',how='outer').fillna(0)
        df_merged['parkname_count_total'] = df_merged['parkname_count_x'] + df_merged['parkname_count_y']
        df_merged_sorted = df_merged.sort_values(by=['parkname_count_total','parkname_count_y'], ascending=False).head(3)
        data = df_merged_sorted['parkName'].values.tolist()
        return data
        
