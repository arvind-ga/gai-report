import pandas as pd
import joblib
import numpy as np


label_lst = [
    np.str_("ENFJ"),
    np.str_("ENFP"),
    np.str_("ENTJ"),
    np.str_("ENTP"),
    np.str_("ESFJ"),
    np.str_("ESFP"),
    np.str_("ESTJ"),
    np.str_("ESTP"),
    np.str_("INFJ"),
    np.str_("INFP"),
    np.str_("INTJ"),
    np.str_("INTP"),
    np.str_("ISFJ"),
    np.str_("ISFP"),
    np.str_("ISTJ"),
    np.str_("ISTP"),
]
model_path = model_path = (
    r"/Users/arvindyadav/Documents/1_GakudoAI_work_AYC_Nov2024/003_code/000_report_generation_v2/model_weights/1_16P_rf_v1.joblib"
)
### Model load
clf = joblib.load(model_path)
resp_val_mapping = {
    "Fully Agree": 3,
    "Partially Agree": 2,
    "Slightly Agree": 1,
    "Neutral": 0,
    "Slightly disagree": -1,
    "Partially disagree": -2,
    "Fully disagree": -3,
}
# print(label_lst)
P16_mapping = {
    "ESTJ": "The Supervisor",
    "ENTJ": "The Commander",
    "ESFJ": "The Provider",
    "ENFJ": "The Giver",
    "ISTJ": "The Inspector",
    "ISFJ": "The Nurturer",
    "INTJ": "The Mastermind",
    "INFJ": "The Counselor",
    "ESTP": "The Doer",
    "ESFP": "The Performer",
    "ENTP": "The Visionary",
    "ENFP": "The Champion",
    "ISTP": "The Craftsman",
    "ISFP": "The Composer",
    "INTP": "The Thinker",
    "INFP": "The Idealist",
}


def convert_resp_to_int(x):
    return resp_val_mapping.get(x)


# path5 = "/Users/arvindyadav/Documents/1_GakudoAI_work/3_School_Stream_Selector/03_data/4_mbti_16p/ga_16p_response_am.csv"

# df5 = pd.read_csv(path5, header=1)  # ,  sep=",", encoding='cp1252')
# df51 = df5.applymap(lambda x: convert_resp_to_int(x))
# print(df5.shape)
# # df5.head()

# # out = clf.predict_proba(df52.to_numpy())[0]
