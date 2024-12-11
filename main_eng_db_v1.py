import numpy as np
import pandas as pd
from common_fn.parameter_mapping import df1_model_params_list
from eng_fn.eng_report_generate_fn import generate_pdf_report

# from common_fn.data_manipulation import generate_pdf_report
from common_fn.data_manipulation_db import get_dfs
from model_code.model_training.model_inference import clf, convert_resp_to_int, label_lst, resp_val_mapping
from common_fn.gpt4_resp import *
########################################
######### Report Generation ############
interest_data = {"Science": 40, "Arts": 20, "Sports": 15, "Technology": 25}
########################
img_path = "images/gakudoai_logo.jpeg"
gakudoai_logo_path = "images/gakudoai_logo.jpeg"

async def generate_report():
    user_email = "check1234@gmail.com"
    check1 = await get_dfs(user_email)
    print("check1:", check1)
    user_detail, dfr1, dfr2, dfr3, dfr4, dfa2, dfa3 = check1 #await db_main(user_email)
    print("user_detail, dfr1, dfr2, dfr3, dfr4, dfa2, dfa3:::", user_detail, dfr1, dfr2, dfr3, dfr4, dfa2, dfa3)
    # print("dfr:::", dfr.columns)
    # email_list = dfr["email_add"].to_list()
    # print("EMail List::::", email_list)
    # print("#" * 30)
    # print(dfr.head())
    # dfr.columns = ["question_code", "student_ans"]
    # print(data_record1.head(30))

    ################### Student's vars ################
    student_name = user_detail["username"]
    student_class = "10"
    student_school = "ST. Mark's Public School"
    student_email = user_detail["email_add"]
    print(
        "Student DETAILS::", student_name, student_class, student_school, student_email
    )

    ################# Student Personality from Model ##############
    # df1_model_params_list1 = [i[4:] for i in df1_model_params_list]
    # df1m = dfr1[df1_model_params_list1]
    # df1m = df1m.applymap(lambda x: convert_resp_to_int(x)).to_numpy()
    resp_val_mapping = {
        "Fully Agree": 3,
        "Partially Agree": 2,
        "Slightly Agree": 1,
        "Neutral": 0,
        "Slightly Disagree": -1,
        "Partially Disagree": -2,
        "Fully Disagree": -3,
    }
    dfr1_list = dfr1["response"].to_list()
    print(type(dfr1_list), type(dfr1_list[0]))
    df1m = np.array([resp_val_mapping.get(i) for i in dfr1_list])#
    df1m = df1m.reshape(1, -1)
    model_out = clf.predict_proba(df1m)[0] * 100
    print("MODEL OUTPUT:::", model_out)
    personality_scores = {}
    for i, j in zip(label_lst, model_out):
        i1 = i
        # print(i1)
        personality_scores[i1] = j

    ################# Student Subject #################
    df5_ans = dfr3.merge(dfa3, on="question_id", how="inner")
    df5_ans["correct_flg"] = df5_ans.apply(
        lambda x: 1 if str(x.answer) == str(x.response) else 0, axis=1
    )
    df5_ans.fillna({"correct_flg": 0}, inplace=True)
    # subjective_score = df5_ans.groupby("segment")["correct_flg"].sum().reset_index()
    subjective_score = df5_ans.groupby("segment").agg({'correct_flg': ['sum', 'count']}).reset_index()
    # df.groupby('Company Name').agg({'Amount': ['sum', 'count']})
    subjective_score.columns = ["segment", "correct_flg_sum", "correct_flg_count"] #['_'.join(col).strip() for col in subjective_score.columns.values]
    subjective_score["correct_flg"] = round(100*subjective_score["correct_flg_sum"]/subjective_score["correct_flg_count"], 2)
    print(subjective_score.head())
    subjective_score.set_index("segment", inplace=True)
    subjective_score.fillna({"correct_flg": 0}, inplace=True)
    subject_strength_dict = subjective_score.to_dict().get("correct_flg")
    # print(subjective_score.head(20))
    # print(subjective_score_dict)

    ################ Reasoning #####################
    df6_ans = dfr2.merge(dfa2, on="question_id", how="inner")
    df6_ans_p1 = df6_ans.copy()
    df6_ans_p1["correct_flg"] = df6_ans_p1.apply(
        lambda x: 1 if str(x.answer) == str(x.response) else 0, axis=1
    )
    df6_ans_p1.fillna({"correct_flg": 0}, inplace=True)
    reasoning_emotion_score = df6_ans_p1.groupby("segment").agg({'correct_flg': ['sum', 'count']}).reset_index()
    # df.groupby('Company Name').agg({'Amount': ['sum', 'count']})
    reasoning_emotion_score.columns = ["segment", "correct_flg_sum", "correct_flg_count"] #['_'.join(col).strip() for col in subjective_score.columns.values]
    reasoning_emotion_score["correct_flg"] = round(100*reasoning_emotion_score["correct_flg_sum"]/reasoning_emotion_score["correct_flg_count"], 2)
    print(subjective_score.head())
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
    req_list1 = [i[4:] for i in req_list]
    df6_ans1 = df6_ans[df6_ans["question_id"].isin(req_list1)]
    # print(df6_ans1.head())
    # df6_ans1["student_ans"] = pd.to_numeric(df6_ans1.student_ans, errors="coerce")
    df6_ans1["response"] = df6_ans1["response"].astype(float)*(100/5)
    # print(df6_ans1.head())

    emotion_score_df = df6_ans1.groupby("segment")["response"].mean().reset_index()
    emotion_score_df.fillna({"response": 0}, inplace=True)
    emotion_score_df.set_index("segment", inplace=True)
    emotion_score_dict = emotion_score_df.to_dict().get("response")

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
  below personality distribution.

  # STUDENT RESPONSE #
  student's personality distribution{pers_dict}
  """

    apti_prompt = """
  # YOUR ROLE #
  You are a career counsellor expert. Summerize us about student's aptitude performance base on the 
  aptitude performance dictionary in a paragraph.

  # STUDENT RESPONSE #
  student's aptitude performance distribution{apti_dict}
  """

    subj_prompt = """
  # YOUR ROLE #
  You are a career counsellor expert. Summerize us about student's class subjective performance base on the 
  aptitude question of different subject performance dictionary in a paragraph.

  # STUDENT RESPONSE #
  student's subjective aptitude performance distribution{subj_dict}
  """
    emot_prompt = """
  # YOUR ROLE #
  You are a career counsellor expert. Summerize us about student's emotinal quotient base on the 
   student response and emotionality quotient dictionary in a paragraph(5-6 lines).

  # STUDENT RESPONSE #
  student's emotionality quotient distribution{emot_dict}
  """
    stream_recommend_prompt = """
  # YOUR ROLE #
  You are a career counsellor expert. Suggest best suited stream in a paragraph (5-6 lines) after class 10th 
  for the student based on evaluation and performance dictionary given below 
  # STUDENT RESPONSE #
  student's personality distribution{emot_dict}
  student's aptitude performance distribution{apti_dict}
  student's subjective aptitude performance distribution{subj_dict}
  student's emotionality quotient distribution{emot_dict}
  """
    career_recommend_prompt = """
      # YOUR ROLE #
      You are a career counsellor expert. Give best suited 6 career options with description what steps to follow 
      in a html-format for student based on evaluation and performance dictionary given below along with 
      description about role in a paragraph
      # STUDENT RESPONSE #
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
        subj_prompt.format(subj_dict=subject_strength_dict)
    ).json()
    sub_pot_comment = response3.get("choices")[0].get("message").get("content")
    ###
    response4 = gpt4_pers_response(emot_prompt.format(emot_dict=emotional_quotient)).json()
    emotional_quetient_comment = response4.get("choices")[0].get("message").get("content")
    ###
    response5 = gpt4_pers_response(
        career_recommend_prompt.format(
            pers_dict=persn_dict,
            apti_dict=aptitude_scores,
            subj_dict=subject_strength_dict,
            emot_dict=emotional_quotient,
        )
    ).json()
    career_option_list = response5.get("choices")[0].get("message").get("content")
    ###
    response6 = gpt4_pers_response(
        stream_recommend_prompt.format(
            pers_dict=persn_dict,
            apti_dict=aptitude_scores,
            subj_dict=subject_strength_dict,
            emot_dict=emotional_quotient,
        )
    ).json()
    stream_option_list = response6.get("choices")[0].get("message").get("content")

    # sub_pot_comment
    # emotional_quetient_comment

    ############## Generate the report #################
    generate_pdf_report1 = generate_pdf_report(
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
        career_option_list,
        stream_option_list
    )
    return generate_pdf_report1


async def get_report():
    report = await generate_report()
    print(report)

import asyncio
import tracemalloc
tracemalloc.start()
asyncio.run(get_report())

