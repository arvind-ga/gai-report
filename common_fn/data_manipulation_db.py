import pandas as pd
import os
import matplotlib.pyplot as plt

from common_fn.parameter_mapping import *
from eng_fn.eng_report_generate_fn import *
import asyncio
import os

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# from app.components.logger import logger

###
img_path = "/Users/arvindyadav/Documents/1_GakudoAI_work/3_School_Stream_Selector/06_report_generation_data/images/rocket-in-space.webp"
gakudoai_logo_path = "/Users/arvindyadav/Documents/1_GakudoAI_work/3_School_Stream_Selector/06_report_generation_data/images/gakudoai_logo.jpeg"
# data_path1 = "/content/drive/MyDrive/1_GakudoAI_data/1_gakudoAI_school/0_gakudoai_report_generation_v1/1_gpt4_data_sample_v1.csv"
# df1 = pd.read_csv(data_path1)
#########

##################################
MONGODB_CONNECTION_STRING = f"mongodb://gakudoai-app-db:U6m0miKzJ7sCCHQkZCymYOYAKo63Imkz0h91DXPNh4vA4islkNRPtDXHjB1T6D0aT1XnXfNF6jXDACDbyj0l2Q==@gakudoai-app-db.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@gakudoai-app-db@"

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

# Asynchronous MongoDB connection
async_connection_string = f'{MONGODB_CONNECTION_STRING}'  # Replace with your connection string
async_mdb_client = AsyncIOMotorClient(async_connection_string)  # Setting MongoDB client for asynchronous operations
async_database = async_mdb_client['fastapi_db']  # Database name in MongoDB for asynchronous operations


# Function to validate connection
async def fetch_quiz_resp(user_email, quiz_id=1):
    try:
        # Attempt to count documents in a specific collection, e.g., 'test_collection'
        count = await async_database['test_collection'].count_documents({})
        print(f"Connection Successful! Found {count} documents in 'test_collection'.")

        # Fetching data from the quiz response collection
        quiz_resp = await async_database['quiz_response'].find_one({"quizId": str(quiz_id), "email":str(user_email)})
        return quiz_resp
    except Exception as e:
        print(f"Connection to MongoDB failed: {e}")
        return None

# Function to validate connection
async def fetch_quiz(quiz_id=1):
    try:
        # Attempt to count documents in a specific collection, e.g., 'test_collection'
        count = await async_database['test_collection'].count_documents({})
        print(f"Connection Successful! Found {count} documents in 'test_collection'.")

        # Fetching data from the quiz response collection
        quiz = await async_database['quizes'].find_one({"id": str(quiz_id)})
        print("quiz::", quiz)
        return quiz
    except Exception as e:
        print(f"Connection to MongoDB failed: {e}")
        return None

# async def main(user_email):
async def get_dfs(user_email):

    # user_email = "mangalsikarwar@gmail.com"
    user_collection = async_database['users']

    # Check if user exists
    flg = await user_collection.find_one({"email": user_email})  # Await the find_one call
    if flg:
        print("User with email {} exist".format(user_email))

        # Fetch quiz responses
        q1_resp1 = await fetch_quiz_resp(user_email, quiz_id=1)  # Await the fetch
        q1_resp2 = await fetch_quiz_resp(user_email, quiz_id=2)
        q1_resp3 = await fetch_quiz_resp(user_email, quiz_id=3)
        q1_resp4 = await fetch_quiz_resp(user_email, quiz_id=1)

        # Fetch quiz for correct Answers
        quiz2 = await fetch_quiz(quiz_id=2)
        quiz3 = await fetch_quiz(quiz_id=3)
        print("quiz2:::", quiz2)
        print("quiz3:::", quiz3)
        quiz2q = quiz2.get("questions")
        quiz3q = quiz3.get("questions")
        quiz2a = [{"id": i["id"], "answer": i["answer"], "segment": i["segment"]} for i in quiz2q]
        quiz3a = [{"id": i["id"], "answer": i["answer"], "segment": i["segment"]} for i in quiz3q]
        print("quiz2a:", quiz2a)
        print("quiz3a:", quiz3a)
        # Safely access and print data
        if q1_resp1:
            print("q1_resp1:", {"id": q1_resp1.get("quizId"), "email": q1_resp1.get("email"), "questions": q1_resp1.get("responses")})
            print("q1_resp1:", {"id": q1_resp2.get("quizId"), "email": q1_resp2.get("email"), "questions": q1_resp2.get("responses")})
            # print("q1_resp1:", {"id": q1_resp3.get("quizId"), "email": q1_resp3.get("email"), "questions": q1_resp3.get("responses")})
            # print("q1_resp1:", {"id": q1_resp4.get("quizId"), "email": q1_resp4.get("email"), "questions": q1_resp4.get("responses")})
            dict1 = q1_resp1.get("responses")
            dict2 = q1_resp2.get("responses")
            dict3 = q1_resp3.get("responses")
            dict4 = q1_resp4.get("responses")
            user_detail = {}
            user_detail["email_add"] = user_email
            user_detail["username"] = q1_resp1.get("username")
            dfr1 = pd.DataFrame(dict1.items(), columns=["question_id", "response"])
            dfr2 = pd.DataFrame(dict2.items(), columns=["question_id", "response"])
            dfr3 = pd.DataFrame(dict3.items(), columns=["question_id", "response"])
            dfr4 = pd.DataFrame(dict4.items(), columns=["question_id", "response"])
            dfa2 = pd.DataFrame(quiz2a)
            dfa2.columns = ["question_id", "answer", "segment"]
            dfa3 = pd.DataFrame(quiz3a) #.items(), columns=["question", "answer"])
            dfa3.columns = ["question_id", "answer", "segment"]
            print("user_detail", user_detail)
            # print("dfr1", dfr1)
            # print("dfr2", dfr2)
            # print("dfr3", dfr3)
            # print("dfr4", dfr4)
            print("dfa2 columns:", dfa2.columns)
            print("dfa3 columns", dfa3.columns)
            return user_detail, dfr1, dfr2, dfr3, dfr4, dfa2, dfa3
            # print(dff.shape)
            # print(dff.tail())
            # print("dict1", type(dict1))
            # print("dict2", dict2)
            # final_dict = {}
            # final_dict["email_add"] = user_email
            # final_dict["username"] = q1_resp1.get("username")
            # for k,v in dict1.items():
            #     k1 = "t1_q" + str(k)
            #     final_dict[k1] = v
            # for k,v in dict2.items():
            #     k1 = "t2_q" + str(k)
            #     final_dict[k1] = v
            # print("final_dict:", final_dict)


        else:
            print("q1_resp1 not found")
    else:
        print("User with email {} does not exist".format(user_email))

    # quest_range = [str(i) for i in range(1,145)]






# Run the main coroutine
# asyncio.run(main())

##########################################
# # Asynchronous MongoDB connection
# async_connection_string = f'{MONGODB_CONNECTION_STRING}'  # This can be the same as the synchronous connection string
# async_mdb_client = AsyncIOMotorClient(async_connection_string)  # setting mongodb client for asynchronous operations
# async_database = async_mdb_client['fastapi_db']  # database name in mongodb for asynchronous operations
#
# # Function to validate connection
# async def fetch_quiz_resp(user_email, quiz_id=1):
#     try:
#         # Attempt to count documents in a specific collection, e.g., 'test_collection'
#         count = await async_database['test_collection'].count_documents({})
#         print(f"Connection Successful! Found {count} documents in 'test_collection'.")
#         q1_resp1 = await quiz_resp_collection.find_one({"id": "1"}) #, "email": user_email})
#         return q1_resp1
#     except Exception as e:
#         print(f"Connection to MongoDB failed: {e}")
#
# user_email = "mangalsikarwar@gmail.com"
# user_collection = async_database.users
# # quiz_resp_collection = async_database.quiz_response
# quiz_resp_collection = async_database['quiz_response']
# flg = user_collection.find_one({"email": user_email})
# if flg:
#     print("User with email {} exist".format(user_email))
#     q1_resp1 = fetch_quiz_resp(user_email, quiz_id=1)
#     q1_resp2 = fetch_quiz_resp(user_email, quiz_id=2)
#     q1_resp3 = fetch_quiz_resp(user_email, quiz_id=3)
#     q1_resp4 = fetch_quiz_resp(user_email, quiz_id=4)
#     # print(q1_resp1.keys())
#     print("q1_resp1:", {"id": q1_resp1["quizId"], "questions": q1_resp1["responses"]})
#     # print("q1_resp1:", {"id": q1_resp2["id"], "questions": q1_resp2["questions"]})
#     # print("q1_resp1:", {"id": q1_resp3["id"], "questions": q1_resp3["questions"]})
#     # print("q1_resp1:", {"id": q1_resp4["id"], "questions": q1_resp4["questions"]})

# # Running the validation function
# dfr = (
#     df0_1.merge(df1_1, on="email_add", how="inner")
#     .merge(df3_1, on="email_add", how="inner")
#     .merge(df4_1, on="email_add", how="inner")
# )

# print("Email list after merging:::", dfr["email_add"].to_list())

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
