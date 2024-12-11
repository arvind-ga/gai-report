import pandas as pd
import os
import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import os
from reportlab.platypus import SimpleDocTemplate, Image

from common_fn.parameter_mapping import *
from eng_fn.eng_report_generate_fn import *

# folder_path1 = r"/Users/arvindyadav/Documents/1_GakudoAI_work/3_School_Stream_Selector/06_report_generation_data/00_test_responses/0_20Oct_2024"
# folder_path1 = r"/Users/arvindyadav/Documents/1_GakudoAI_work/3_School_Stream_Selector/06_report_generation_data/00_test_responses/1_10Nov_2024"
folder_path1 = r"/Users/arvindyadav/Documents/1_GakudoAI_work/3_School_Stream_Selector/06_report_generation_data/00_test_responses/3_11Nov_2024"
df0 = pd.read_csv(os.path.join(folder_path1, "Test0_GakudoAI_School_Test_V1.csv"))
df1 = pd.read_csv(os.path.join(folder_path1, "Test1_GakudoAI_School_Test_V1.csv"))
df2 = pd.read_csv(os.path.join(folder_path1, "Test2_GakudoAI_School_Test_V1.csv"))
df3 = pd.read_csv(os.path.join(folder_path1, "Test3_GakudoAI_School_Test_V1.csv"))
df4 = pd.read_csv(os.path.join(folder_path1, "Test4_GakudoAI_School_Test_V1.csv"))

###
folder_path2 = r"/Users/arvindyadav/Documents/1_GakudoAI_work/3_School_Stream_Selector/06_report_generation_data/000_questionsNanswers"
df5 = pd.read_csv(os.path.join(folder_path2, "1_test3_qna_mapping_v1.csv"))
df6 = pd.read_csv(os.path.join(folder_path2, "2_test4_qna_mapping_v1.csv"))

###
img_path = "/Users/arvindyadav/Documents/1_GakudoAI_work/3_School_Stream_Selector/06_report_generation_data/images/rocket-in-space.webp"
gakudoai_logo_path = "/Users/arvindyadav/Documents/1_GakudoAI_work/3_School_Stream_Selector/06_report_generation_data/images/gakudoai_logo.jpeg"
# data_path1 = "/content/drive/MyDrive/1_GakudoAI_data/1_gakudoAI_school/0_gakudoai_report_generation_v1/1_gpt4_data_sample_v1.csv"
# df1 = pd.read_csv(data_path1)


#########
df0_1 = df0.copy()
df0_1.columns = df0_columns

###
df1_1 = df1.copy()
df1_col_list_old = df1_1.columns
df1_1.columns = [
    i for i, j in mapping_dict1.items() for k in df1_col_list_old if j == k
]
df1_1.drop(
    columns=["timestamp", "name", "phone_number", "dob", "gender"], axis=1, inplace=True
)

###
df2_1 = df2.copy()
# print("df2_columns:::", df2_columns)
# print("df2_1.columns:::", list(df2_1.columns))
df2_1.columns = df2_columns
df2_1.drop(columns=["timestamp", "name", "phone_number", "dob"], axis=1, inplace=True)

###
df3_1 = df3.copy()
df3_col_list_old = df3_1.columns
print("df2_columns:::", df3_columns)
print("df2_1.columns:::", list(df3_1.columns))
# print([i for i, j in mapping_dict3.items() for k in df3_col_list_old if j == k])
print("[i for i, j in mapping_dict4.items() for k in df3_col_list_old if j == k]:::::::", [
    i for i, j in mapping_dict3.items() for k in df3_col_list_old if j == k
])
df3_1.columns = [
    i for i, j in mapping_dict3.items() for k in df3_col_list_old if j == k
]
df3_1.drop(columns=["timestamp", "name", "phone_number", "dob"], axis=1, inplace=True)

###
df4_1 = df4.copy()
# print("checkkkkkk1111::", df4.columns)
df4_col_list_old = df4_1.columns
# print([i for i, j in mapping_dict4.items() for k in df4_col_list_old if j == k])
print("[i for i, j in mapping_dict4.items() for k in df4_col_list_old if j == k]:::::::", [
    i for i, j in mapping_dict4.items() for k in df4_col_list_old if j == k
])
df4_1.columns = [
    i for i, j in mapping_dict4.items() for k in df4_col_list_old if j == k
]
df4_1.drop(columns=["timestamp", "name", "phone_number", "dob"], axis=1, inplace=True)

##################################
dfr = (
    df0_1.merge(df1_1, on="email_add", how="inner")
    .merge(df3_1, on="email_add", how="inner")
    .merge(df4_1, on="email_add", how="inner")
)

print("Email list after merging:::", dfr["email_add"].to_list())

# .merge(df2_1, on="email_add", how="inner")
# print("dfr_columns:::", dfr.columns)


# email_list = dfr["email_add"].to_list()
# print("EMail ist::::", email_list)
# for email_id in email_list
#########################
# df2 = df1.applymap(lambda x: str(x).replace("$", "-"))

### First ave to get these values
# Sample data for aptitude, psychometry, and interests
# personality_scores = {
#     "ISTJ": 85,
#     "ISFJ": 20,
#     "INFJ": 15,
#     "INTJ": 18,
#     "ISTP": 14,
#     "ISFP": 15,
#     "INFP": 5,
#     "INTP": 6,
#     "ESTP": 7,
#     "ESFP": 6,
#     "ENFP": 9,
#     "ENTP": 4,
#     "ESTJ": 15,
#     "ESFJ": 11,
#     "ENFJ": 3,
#     "ENTJ": 2,
# }


# aptitude_scores = {
#     "Quntitative Reasoning": 75,
#     "Logical Reasoning": 85,
#     "Verbal Reasoning": 65,
#     "Situation Judgement": 70,
# }

# stream_scores = {
#     "Science - Maths": 95,
#     "Science - Bio": 85,
#     "Arts": 65,
#     "Humanities": 70,
#     "Commerce": 60,
# }

# interest_data = {"Science": 40, "Arts": 20, "Sports": 15, "Technology": 25}

# emotional_quotient = {
#     "Conflict Management": 80,
#     "Empathy": 60,
#     "Pro Social Behavior": 75,
#     "Emotional Regulation": 55,
#     "Emotional Self-Awareness": 45,
#     "motional Self-Efficacy": 85,
#     "Motivation": 25,
# }

# career_option_list = [
#     "Computer Programmer",
#     "Civil Engineer",
#     "Administrator",
#     "Supply Chain Manager",
#     "Statistician",
#     "Accountant",
# ]


######### Report Generation ############

# # Sample data for aptitude, psychometry, and interests
# personality_scores = {
#     "ISTJ": 85,
#     "ISFJ": 20,
#     "INFJ": 15,
#     "INTJ": 18,
#     "ISTP": 14,
#     "ISFP": 15,
#     "INFP": 5,
#     "INTP": 6,
#     "ESTP": 7,
#     "ESFP": 6,
#     "ENFP": 9,
#     "ENTP": 4,
#     "ESTJ": 15,
#     "ESFJ": 11,
#     "ENFJ": 3,
#     "ENTJ": 2,
# }


# aptitude_scores = {
#     "Quntitative Reasoning": 75,
#     "Logical Reasoning": 85,
#     "Verbal Reasoning": 65,
#     "Spatial Reasoning": 70,
# }

# stream_scores = {
#     "Science - Maths": 95,
#     "Science - Bio": 85,
#     "Arts": 65,
#     "Humanities": 70,
#     "Commerce": 60,
# }

# interest_data = {"Science": 40, "Arts": 20, "Sports": 15, "Technology": 25}

# emotional_quotient = {
#     "Conflict Management": 80,
#     "Empathy": 60,
#     "Pro Social Behavior": 75,
#     "Emotional Regulation": 55,
#     "Emotional Self-Awareness": 45,
#     "motional Self-Efficacy": 85,
#     "Motivation": 25,
# }


# # Function to generate bar charts
# student_name = "Rahul Sharma"
# student_class = "9th"
# student_school = "St. Mark's public School, Agra"
# student_email = "abc123@gmail.com"
# personality_comment = "It seems like your personality leans strongly toward ISTJ but also shows significant ISFJ characteristics. An ISTJ is often detail-oriented, logical, and dependable, while an ISFJ blends these qualities with a caring and supportive nature. Your ISTJ side likely drives your preference for order, practicality, and clear decision-making, while the ISFJ influence adds a compassionate touch, making you more sensitive to others' emotions and needs."
# aptitude_comment = "It’s impressive how strong your logical reasoning skills are, and you’ve demonstrated solid abilities across all other aptitude areas, performing above average. This shows great potential, and with continued focus, you’re likely to excel even further!"
# sub_pot_comment = "It seems you have strong aptitude for subjects like mathematics and science, and you enjoy problem-solving or analytical thinking, the science stream might be a good fit. On the other hand, if you're drawn to understanding human behavior, economics, or languages, the arts or humanities stream could align better with your passions. Commerce may be a great option if you're interested in finance, business, or economics."
# emotional_quetient_comment = "This person is skilled at managing conflicts, maintaining positive social behaviors, and has strong confidence in handling emotions, making them effective in resolving disputes and working well with others. They are empathetic, often able to understand and relate to others' emotions, though there is some potential for deepening this ability. However, they may find it challenging to regulate their emotions, especially in stressful situations, and might struggle with recognizing their own emotional states. Additionally, staying motivated and focused on goals seems to be a difficulty, which could hinder their ability to persevere and maintain progress in long-term tasks. Enhancing emotional awareness and motivation would help them achieve greater emotional balance and success."


# # Generate the report
# generate_pdf_report(
#     img_path,
#     gakudoai_logo_path,
#     student_name,
#     student_class,
#     student_school,
#     student_email,
#     personality_comment,
#     aptitude_comment,
#     sub_pot_comment,
#     emotional_quetient_comment,
#     personality_scores,
#     aptitude_scores,
#     stream_scores,
#     interest_data,
#     emotional_quotient,
#     career_option_list,
# )
