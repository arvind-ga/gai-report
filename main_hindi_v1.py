import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas

from common_fn.parameter_mapping import *
from common_fn.data_manipulation import *
from common_fn.gpt4_resp import gpt4_pers_response
from common_fn.gpt4_resp import *
from hindi_fn.hindi_report_generate_fn import generate_pdf_report
from hindi_fn.gen_hindi_eng_seg import get_tags

from model_code.model_training.model_inference import clf, convert_resp_to_int, label_lst

# print("files1:::", os.listdir("eng_fn"))
#
#
# folder_path1 = r"/Users/arvindyadav/Documents/1_GakudoAI_work/3_School_Stream_Selector/06_report_generation_data/00_test_responses/0_20Oct_2024"
# df0 = pd.read_csv(os.path.join(folder_path1, "Test0_GakudoAI_School_Test_V1.csv"))
# df1 = pd.read_csv(os.path.join(folder_path1, "Test1_GakudoAI_School_Test_V1.csv"))
# df2 = pd.read_csv(os.path.join(folder_path1, "Test2_GakudoAI_School_Test_V1.csv")
# df3 = pd.read_csv(os.path.join(folder_path1, "Test3_GakudoAI_School_Test_V1.csv"))
# df4 = pd.read_csv(os.path.join(folder_path1, "Test4_GakudoAI_School_Test_V1.csv"))
# # print(df0.head())
#
#
# ###
# folder_path2 = r"/Users/arvindyadav/Documents/1_GakudoAI_work/3_School_Stream_Selector/06_report_generation_data/000_questionsNanswers"
# df5 = pd.read_csv(os.path.join(folder_path2, "1_test3_qna_mapping_v1.csv"))
# df6 = pd.read_csv(os.path.join(folder_path2, "2_test4_qna_mapping_v1.csv"))
#
# ###
# img_path = "/Users/arvindyadav/Documents/1_GakudoAI_work/3_School_Stream_Selector/06_report_generation_data/images/rocket-in-space.webp"
# gakudoai_logo_path = "/Users/arvindyadav/Documents/1_GakudoAI_work/3_School_Stream_Selector/06_report_generation_data/images/gakudoai_logo.jpeg"
# # data_path1 = "/content/drive/MyDrive/1_GakudoAI_data/1_gakudoAI_school/0_gakudoai_report_generation_v1/1_gpt4_data_sample_v1.csv"
# # df1 = pd.read_csv(data_path1)
#
#
# #########
# df0_1 = df0.copy()
# df0_1.columns = df0_columns
#
# ###
# df1_1 = df1.copy()
# df1_col_list_old = df1_1.columns
# df1_1.columns = [
#     i for i, j in mapping_dict1.items() for k in df1_col_list_old if j == k
# ]
# # print("Columns::::::::::", df1_1.columns)
#
# ###
# df2_1 = df2.copy()
# df2_1.columns = df2_columns
#
# ###
# df3_1 = df3.copy()
# df3_col_list_old = df3_1.columns
# print([i for i, j in mapping_dict3.items() for k in df3_col_list_old if j == k])
# print("df3_1.columns:::", df3_1.columns)
# df3_1.columns = [
#     i for i, j in mapping_dict3.items() for k in df3_col_list_old if j == k
# ]
#
# ###
# df4_1 = df4.copy()
# print("checkkkkkk1111::", df4.columns)
# df4_col_list_old = df4_1.columns
# print([i for i, j in mapping_dict4.items() for k in df4_col_list_old if j == k])
# df4_1.columns = [
#     i for i, j in mapping_dict4.items() for k in df4_col_list_old if j == k
# ]

########################################
######### Report Generation ############

# aptitude_scores = {
#     "Quntitative Reasoning": 75,
#     "Logical Reasoning": 85,
#     "Verbal Reasoning": 65,
#     "Spatial Reasoning": 70,
# }


interest_data = {"Science": 40, "Arts": 20, "Sports": 15, "Technology": 25}

# career_option_list = [
#     "Computer Programmer",
#     "Civil Engineer",
#     "Administrator",
#     "Supply Chain Manager",
#     "Statistician",
#     "Accountant",
# ]

# personality_comment = "It seems like your personality leans strongly toward ISTJ but also shows significant ISFJ characteristics. An ISTJ is often detail-oriented, logical, and dependable, while an ISFJ blends these qualities with a caring and supportive nature. Your ISTJ side likely drives your preference for order, practicality, and clear decision-making, while the ISFJ influence adds a compassionate touch, making you more sensitive to others' emotions and needs."
# aptitude_comment = "It’s impressive how strong your logical reasoning skills are, and you’ve demonstrated solid abilities across all other aptitude areas, performing above average. This shows great potential, and with continued focus, you’re likely to excel even further!"
# sub_pot_comment = "It seems you have strong aptitude for subjects like mathematics and science, and you enjoy problem-solving or analytical thinking, the science stream might be a good fit. On the other hand, if you're drawn to understanding human behavior, economics, or languages, the arts or humanities stream could align better with your passions. Commerce may be a great option if you're interested in finance, business, or economics."
# emotional_quetient_comment = "This person is skilled at managing conflicts, maintaining positive social behaviors, and has strong confidence in handling emotions, making them effective in resolving disputes and working well with others. They are empathetic, often able to understand and relate to others' emotions, though there is some potential for deepening this ability. However, they may find it challenging to regulate their emotions, especially in stressful situations, and might struggle with recognizing their own emotional states. Additionally, staying motivated and focused on goals seems to be a difficulty, which could hinder their ability to persevere and maintain progress in long-term tasks. Enhancing emotional awareness and motivation would help them achieve greater emotional balance and success."

########################
email_list = dfr["email_add"].to_list()
print("EMail ist::::", email_list)
print("#" * 30)
for email_id in email_list[6:]:
    data_record = dfr[dfr["email_add"] == email_id]
    data_record.drop_duplicates("email_add", keep="last", inplace=True)
    data_record1 = data_record.T.reset_index()
    data_record1.columns = ["question_code", "student_ans"]
    # print(data_record1.head(30))

    ################### Student's vars ################
    student_name = data_record1[data_record1["question_code"] == "name"].values[0][1]
    student_class = data_record1[data_record1["question_code"] == "grade"].values[0][1]
    student_school = data_record1[
        data_record1["question_code"] == "school_name"
    ].values[0][1]
    student_email = email_id #data_record1[data_record1["question_code"] == "email"].values[0][1]
    print(
        "Student DETAILS::", student_name, student_class, student_school, student_email
    )

    ################# Student Personality from Model ##############
    df1m = df1_1[df1_1["email_add"] == email_id][df1_model_params_list]
    df1m = df1m.applymap(lambda x: convert_resp_to_int(x)).to_numpy()
    model_out = clf.predict_proba(df1m)[0] * 100
    print("MODEL OUTPUT:::", model_out)
    personality_scores = {}
    for i, j in zip(label_lst, model_out):
        i1 = i
        # print(i1)
        personality_scores[i1] = j

    ################# Student Subject #################
    df5_ans = df5.merge(data_record1, on="question_code", how="inner")
    df5_ans["correct_flg"] = df5_ans.apply(
        lambda x: 1 if str(x.answer) == str(x.student_ans) else 0, axis=1
    )
    subjective_score = df5_ans.groupby("segment")["correct_flg"].sum().reset_index()
    subjective_score.set_index("segment", inplace=True)
    subjective_score.fillna({"correct_flg": 0}, inplace=True)
    subject_strength_dict = subjective_score.to_dict().get("correct_flg")
    # print(subjective_score.head(20))
    # print(subjective_score_dict)

    ################ Reasoning #####################
    df6_ans = df6.merge(data_record1, on="question_code", how="inner")
    df6_ans_p1 = df6_ans.copy()
    df6_ans_p1["correct_flg"] = df6_ans_p1.apply(
        lambda x: 1 if str(x.answer) == str(x.student_ans) else 0, axis=1
    )

    # df6_ans1.fillna(0, inplace=True)
    df6.fillna({"student_ans": 0}, inplace=True)
    reasoning_emotion_score = (
        df6_ans_p1.groupby("segment")["correct_flg"].sum().reset_index()
    )
    reasoning_emotion_score.set_index("segment", inplace=True)
    # print(reasoning_emotion_score.head())
    reasoning_emotion_score_dict = reasoning_emotion_score.to_dict()

    ### Aptitude score
    reasoning_emotion_score_dict1 = reasoning_emotion_score_dict.get("correct_flg")

    # print("OLD dict:::", reasoning_emotion_score_dict)
    # print("NEW dict:::", reasoning_emotion_score_dict1)

    aptitude_scores = {}
    aptitude_scores["Quantitative"] = subject_strength_dict.get("maths")
    aptitude_scores["Logical"] = reasoning_emotion_score_dict1.get("logical")
    aptitude_scores["Situation"] = reasoning_emotion_score_dict1.get("situation")
    aptitude_scores["Verbal"] = reasoning_emotion_score_dict1.get("verbal")

    ############### Emotional Quotient #################
    req_list = [
        "t4_q31",
        "t4_q32",
        "t4_q33",
        "t4_q34",
        "t4_q35",
        "t4_q36",
        "t4_q37",
        "t4_q38",
        "t4_q39",
        "t4_q40",
        "t4_q41",
        "t4_q42",
        "t4_q43",
        "t4_q44",
    ]
    df6_ans1 = df6_ans[df6_ans["question_code"].isin(req_list)]
    # print(df6_ans1.head())
    # df6_ans1["student_ans"] = pd.to_numeric(df6_ans1.student_ans, errors="coerce")
    df6_ans1["student_ans"] = df6_ans1["student_ans"].astype(float)
    # print(df6_ans1.head())

    emotion_score_df = df6_ans1.groupby("segment")["student_ans"].mean().reset_index()
    emotion_score_df.fillna({"student_ans": 0}, inplace=True)
    emotion_score_df.set_index("segment", inplace=True)
    emotion_score_dict = emotion_score_df.to_dict().get("student_ans")

    emotional_quotient = {}
    emotional_quotient["Conflict Management"] = emotion_score_dict.get(
        "Conflict Management"
    )
    emotional_quotient["Emotional Regulation"] = emotion_score_dict.get(
        "Emotional Regulation"
    )
    emotional_quotient["Emotional Self-Awareness"] = emotion_score_dict.get(
        "Emotional Self-Awareness"
    )
    emotional_quotient["Emotional Self-Efficacy"] = emotion_score_dict.get(
        "Emotional Self-Efficacy"
    )
    emotional_quotient["Empathy"] = emotion_score_dict.get("Empathy")
    emotional_quotient["Motivation"] = emotion_score_dict.get("Motivation")
    emotional_quotient["Pro Social Behavior"] = emotion_score_dict.get(
        "Pro Social Behavior"
    )
    #################### prompt ###################################
    pers_prompt = """
    # YOUR ROLE #
    You are a career counsellor expert. Summerize us about student's personality in a paragraph based on 
    below personality distribution in a paragraph in hindi language  in UTF-8 encoding format.

    # STUDENT RESPONSE #
    student's personality distribution{pers_dict}
    """

    apti_prompt = """
    # YOUR ROLE #
    You are a career counsellor expert. Summerize us about student's aptitude performance base on the 
    aptitude performance dictionary in a paragraph in hindi language in UTF-8 encoding format.

    # STUDENT RESPONSE #
    student's aptitude performance distribution{apti_dict}
    """

    subj_prompt = """
    # YOUR ROLE #
    You are a career counsellor expert. Summerize us about student's class subjective performance base on the 
    aptitude question of different subject performance dictionary in a paragraph in hindi language  in UTF-8 encoding format.

    # STUDENT RESPONSE #
    student's subjective aptitude performance distribution{subj_dict}
    """
    emot_prompt = """
    # YOUR ROLE #
    You are a career counsellor expert. Summerize us about student's emotinal quotient base on the 
    student response and emotionality quotient dictionary in a paragraph(5-6 lines) in hindi language in UTF-8 encoding format.

    # STUDENT RESPONSE #
    student's emotionality quotient distribution{emot_dict}
    """
    career_recomend_prompt = """
    # YOUR ROLE #
      You are a career counsellor expert. Just give best suited 6 career options titles
      for student based on evaluation and performance dictionary given below
      in a paragraph (5-6 lines) in Hindi language
    # STUDENT'S REQUIRED INFORMATION #
      student's personality distribution{emot_dict}
      student's aptitude performance distribution{apti_dict}
      student's subjective aptitude performance distribution{subj_dict}
      student's emotionality quotient distribution{emot_dict}
      """

    #######################################################
    print("#@" * 30)
    persn_dict = {str(i): round(float(j), 2) for i, j in personality_scores.items()}
    print("personality_scores:::", persn_dict)
    print("subject_strength_dict:::", subject_strength_dict)
    print("aptitude_scores:::", aptitude_scores)
    print("emotional_quotient:::", emotional_quotient)

    ################### Comment on performance ####################
    response1 = gpt4_pers_response(pers_prompt.format(pers_dict=persn_dict)).json()
    personality_comment = response1.get("choices")[0].get("message").get("content")
    ###
    response2 = gpt4_pers_response(apti_prompt.format(apti_dict=aptitude_scores)).json()
    aptitude_comment = response2.get("choices")[0].get("message").get("content")
    ###
    response3 = gpt4_pers_response(
    subj_prompt.format(subj_dict=subject_strength_dict)).json()
    sub_pot_comment = response3.get("choices")[0].get("message").get("content")
    ###
    response4 = gpt4_pers_response(emot_prompt.format(emot_dict=emotional_quotient)).json()
    emotional_quetient_comment = response4.get("choices")[0].get("message").get("content")
    ###
    response5 = gpt4_pers_response(
    career_recomend_prompt.format(
        pers_dict=persn_dict,
        apti_dict=aptitude_scores,
        subj_dict=subject_strength_dict,
        emot_dict=emotional_quotient,
    )).json()
    career_option_list = response5.get("choices")[0].get("message").get("content")
    ###
    print("#" * 60)
    print("OUT1:::", personality_comment)
    print("OUT2:::", aptitude_comment)
    print("OUT3:::", sub_pot_comment)
    print("OUT4:::", emotional_quetient_comment)
    print("OUT5:::", career_option_list)

    # sub_pot_comment
    # emotional_quetient_comment

    ############## Generate the report #################
    generate_pdf_report(
    img_path,
    gakudoai_logo_path,
    student_name,
    student_class,
    student_school,
    student_email,
    personality_comment,
    aptitude_comment,
    sub_pot_comment,
    emotional_quetient_comment,
    personality_scores,
    aptitude_scores,
    subject_strength_dict,
    interest_data,
    emotional_quotient,
    career_option_list,)
    print("REPORT SUCCESSFULLY GENERATED FOR :::", student_email)
