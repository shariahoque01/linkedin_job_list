# !pip install linkedin-api requests
from job_search import collect_clean_data, job_data_scrape

def main_df():
    # print(collect_clean_data())
    sample2 = job_data_scrape(collect_clean_data())
    # print("Type of my_dataframe:", type(sample2))
    return sample2

#if __name__ == "__main__":
    #main()