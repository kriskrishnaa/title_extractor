import pandas as pd
from title_extractor  import extract_title, add_stopWord, exclude_stopWord

user_survery_df = pd.read_csv("data/Survey response sample data.csv")
title_content_df = pd.read_csv("data/Content sample.csv")

exclude_stopWord("ma")

keyword_list = title_content_df['Content_name'].to_list()

retrieved_titles = {}

for index, row in user_survery_df.iterrows():
    retrieved_titles[row["Customer_id"]] = extract_title(str(row['Response']), keyword_list)

user_survery_df['Content_names'] = user_survery_df["Customer_id"].map(retrieved_titles)
user_survery_df.to_csv("output/Survey_response_sample_data_with_titles_retrieved.csv", index=False)