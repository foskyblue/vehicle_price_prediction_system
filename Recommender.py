import pandas as pd


class RecommendationEngine():
    def __init__(self) -> None:
        pass


    def get_recommendations(self, vehicles_df, model_name, model_brand_name, year, body_type):
        filtered_df = vehicles_df[(vehicles_df['model_name']==model_name) & (vehicles_df['model_brand_name']==model_brand_name) 
                                  & (vehicles_df['bodyType']==body_type)]

        if filtered_df.shape[0] > 5:
            filtered_df = filtered_df.sort_values(by=['gradeScore'], ascending=False)
        else:
            filtered_df2 = vehicles_df[(vehicles_df['model_name']==model_name) | (vehicles_df['model_brand_name']==model_brand_name)]
            filtered_df = pd.concat([filtered_df, filtered_df2], ignore_index=True) #.sort_values(by=['gradeScore'])
        
        return list(filtered_df.head(5)['websiteUrl'].values)

