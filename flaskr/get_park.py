import pymysql
import pandas as pd
import helper_functions as uf
conn, engine = uf.conn_to_db()

def get_park(amenity_ids,activity_ids):
        query_amenity = f"select id,parkName from wanderwisely.amenity_related_parks"
        query_activity= f"select id,parkName from wanderwisely.activity_related_parks"
        df_amenity = uf.import_data(query_amenity, conn)
        df_activity = uf.import_data(query_activity, conn)
        parks_df = pd.merge(df_amenity, df_activity, on='parkName', how='outer')
        parks_df = parks_df.rename(columns={'id_x': 'amenity_id', 'id_y': 'activity_id'})
        if amenity_ids is not None and activity_ids is not None and len(amenity_ids) > 0 and len(activity_ids) > 0:
             condition = (parks_df['amenity_id'].isin(amenity_ids)) & (parks_df['activity_id'].isin(activity_ids))
             parks_df = parks_df[condition]
             parks_df['parkName_count'] = parks_df['parkName'].apply(lambda x: parks_df['parkName'].value_counts()[x])
             top_parks = parks_df.groupby(['parkName']).size().reset_index(name='count').sort_values('count', ascending=False).head(3)
             data = top_parks['parkName'].values.tolist()
             return data
