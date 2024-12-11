import pandas as pd
import os
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Image
from datetime import datetime

###Hindi
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

from hindi_fn.gen_hindi_eng_seg import get_tags

###
hindi_font_path = "./hindi_fn/mangal_regular.ttf"  # Replace with the path to your Devanagari font
english_font_path = "./hindi_fn/TimesNewRoman.ttf"  # Default font for English

pdfmetrics.registerFont(TTFont("HindiFont", hindi_font_path))
pdfmetrics.registerFont(TTFont("EnglishFont", english_font_path))

styles = getSampleStyleSheet()
base_style = styles["BodyText"]
base_style.fontSize = 12

# from eng_fn.parameter_mapping import *


### First ave to get these values
# Sample data for aptitude, psychometry, and interests
# personality_scores, aptitude_scores, stream_scores, interest_data, emotional_quotient, career_option_list
################################ Student params #############################
# student_name = "Rahul Sharma"
# student_class = "9th"
# student_school = "St. Mark's public School, Agra"
# student_email = "abc123@gmail.com"
# personality_comment = "It seems like your personality leans strongly toward ISTJ but also shows significant ISFJ characteristics. An ISTJ is often detail-oriented, logical, and dependable, while an ISFJ blends these qualities with a caring and supportive nature. Your ISTJ side likely drives your preference for order, practicality, and clear decision-making, while the ISFJ influence adds a compassionate touch, making you more sensitive to others' emotions and needs."
# aptitude_comment = "It’s impressive how strong your logical reasoning skills are, and you’ve demonstrated solid abilities across all other aptitude areas, performing above average. This shows great potential, and with continued focus, you’re likely to excel even further!"
# sub_pot_comment = "It seems you have strong aptitude for subjects like mathematics and science, and you enjoy problem-solving or analytical thinking, the science stream might be a good fit. On the other hand, if you're drawn to understanding human behavior, economics, or languages, the arts or humanities stream could align better with your passions. Commerce may be a great option if you're interested in finance, business, or economics."
# emotional_quetient_comment = "This person is skilled at managing conflicts, maintaining positive social behaviors, and has strong confidence in handling emotions, making them effective in resolving disputes and working well with others. They are empathetic, often able to understand and relate to others' emotions, though there is some potential for deepening this ability. However, they may find it challenging to regulate their emotions, especially in stressful situations, and might struggle with recognizing their own emotional states. Additionally, staying motivated and focused on goals seems to be a difficulty, which could hinder their ability to persevere and maintain progress in long-term tasks. Enhancing emotional awareness and motivation would help them achieve greater emotional balance and success."
# student_name, student_class, student_school, student_email, personality_comment, aptitude_comment, sub_pot_comment,
# emotional_quetient_comment


######### Report Generation ############


# Function to generate bar charts
def generate_bar_chart(scores, title, filename):
    labels = list(scores.keys())
    values = list(scores.values())

    plt.figure(figsize=(8, 4))
    plt.bar(labels, values, color="blue")
    plt.title(title)
    plt.ylabel("Scores")
    plt.savefig(filename)
    plt.close()


# Function to generate pie charts
def generate_pie_chart(data, title, filename):
    labels = list(data.keys())
    values = list(data.values())

    plt.figure(figsize=(6, 6))
    plt.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=140,
        colors=plt.cm.Paired.colors,
    )
    plt.title(title)
    plt.savefig(filename)
    plt.close()


def add_header_footer(canvas, doc):
    # Save the current state of the canvas so that it can be restored later
    canvas.saveState()

    # Header
    canvas.setFont("Helvetica-Bold", 12)
    # canvas.drawString(30, A4[1] - 50, "Student Aptitude, Psychometry, and Interest Report")

    # Footer
    canvas.setFont("Helvetica", 10)
    # canvas.borderWidth = 1
    # canvas.borderColor = colors.black
    # canvas.borderPadding = 0
    canvas.drawString(30, 50, f"©GakudoAI 2024")
    canvas.drawString(530, 50, f"Page {doc.page}")
    # Restore the saved state of the canvas
    canvas.restoreState()


def get_divider():
    styles = getSampleStyleSheet()
    # Create a style with a bottom border (acts like a divider)
    divider_style = styles["Normal"]
    divider_style.borderWidth = 1
    divider_style.borderColor = colors.black
    divider_style.borderPadding = 0

    # Create a Paragraph for the divider
    divider = Paragraph("", divider_style)
    return divider


# Function to generate the PDF report
def generate_pdf_report(
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
    stream_scores,
    interest_data,
    emotional_quotient,
    career_option_list,
):
    # Generate charts

    ### Bar Graphs
    generate_bar_chart(
        personality_scores, "Personality Scores", "personality_score_chart.png"
    )
    generate_bar_chart(aptitude_scores, "Aptitude Scores", "aptitude_chart.png")
    generate_bar_chart(stream_scores, "Stream Scores", "stream_chart.png")
    generate_pie_chart(interest_data, "Interest Breakdown", "interest_chart.png")
    generate_pie_chart(
        emotional_quotient, "Emotional Quotient", "emotional_quotient.png"
    )

    # Create a PDF
    # report_folder = r"/Users/arvindyadav/Documents/1_GakudoAI_work/3_School_Stream_Selector/07_reports/01_english"
    date_time1 = datetime.now()
    date1 = datetime.today().strftime('%Y-%m-%d')
    report_folder1 = r"/Users/arvindyadav/Documents/1_GakudoAI_work/3_School_Stream_Selector/07_reports/02_hindi"
    report_folder = os.path.join(report_folder1, date1)
    os.makedirs(report_folder, exist_ok=True)
    pdf_filename = student_email.split("@")[0] + "_report_" + str(date_time1) + ".pdf"
    doc = SimpleDocTemplate(os.path.join(report_folder, pdf_filename), pagesize=A4)

    # career_option_list = [
    #     "Computer Programmer",
    #     "Civil Engineer",
    #     "Administrator",
    #     "Supply Chain Manager",
    #     "Statistician",
    #     "Accountant",
    # ]

    ############################################################################
    # Define content elements
    content = []
    styles = getSampleStyleSheet()

    ### hindi
    # styles_h = getSampleStyleSheet()
    # styles_h["BodyText"].fontName = "HindiFont"
    # styles_h["BodyText"].fontSize = 12

    #     mixed_text = """
    # <font name="EnglishFont">This is an English sentence, </font>
    # <font name="HindiFont">और यह एक हिंदी वाक्य है।</font>
    # """
    # hindi_style = styles["BodyText"].clone("HindiStyle")
    # hindi_style.fontName = "DevanagariFont"
    # hindi_style.fontSize = 12
    hindi_style = styles["BodyText"].clone("HindiStyle")
    hindi_style.fontName = "HindiFont"
    hindi_style.fontSize = 11

    eng_text = """<font name="EnglishFont">{}</font>"""
    hindi_text = """<font name="HindiFont">{}</font>"""
    mixed_text = """<font name="HindiFont">{}</font>"""

    ### First Page
    # Add Title
    content.append(get_divider())
    content.append(Paragraph("GakudoAI Student Assessment", styles["Title"]))
    content.append(Paragraph("Report", styles["Title"]))
    content.append(get_divider())
    content.append(Spacer(1, 12))

    content.append(Image(img_path, width=400, height=500))
    content.append(Spacer(1, 12))

    content.append(get_divider())

    content.append(
        Paragraph("Student Name: {}".format(student_name), styles["Heading3"])
    )
    content.append(
        Paragraph("Student Class: {}".format(student_class), styles["Heading3"])
    )
    content.append(
        Paragraph("School's Name: {}".format(student_school), styles["Heading3"])
    )
    content.append(
        Paragraph("Student's Email: {}".format(student_email), styles["Heading3"])
    )
    content.append(Spacer(1, 24))

    ### First Page
    ### In Depth Analysis
    content.append(Paragraph("In Depth Analysis", styles["Title"]))
    content.append(Spacer(1, 12))
    content.append(Paragraph("Personality", styles["Heading3"]))
    # pers_about_eng = r"Personality identification is important for career selection because it helps ensure a good job fit, enhances job satisfaction, and aligns with your natural strengths and preferences. It can guide you toward roles and environments where you’re most productive and happy, and it aids in finding a career that suits your stress management style and growth potential."
    pers_about_hindi = r"कैरियर चयन के लिए व्यक्तित्व की पहचान महत्वपूर्ण है क्योंकि यह एक अच्छी नौकरी सुनिश्चित करने में मदद करती है, नौकरी से संतुष्टि बढ़ाती है, और आपकी प्राकृतिक शक्तियों और प्राथमिकताओं के साथ संरेखित होती है। यह आपको उन भूमिकाओं और वातावरण की ओर मार्गदर्शन कर सकता है जहां आप सबसे अधिक उत्पादक और खुश हैं, और यह एक ऐसा करियर ढूंढने में सहायता करता है जो आपकी तनाव प्रबंधन शैली और विकास क्षमता के अनुकूल हो।"
    content.append(
        Paragraph(get_tags(pers_about_hindi),
            base_style,
        )
    )
    content.append(Spacer(1, 12))
    content.append(Paragraph("Definition of 16-Personalities:", styles["Heading4"]))
    # istj_eng = r"1. ISTJ (The Inspector) – Organized, dependable, and practical. They value tradition and are excellent at planning and following through with tasks."
    istj_hindi = r"1. ISTJ (The Inspector) - संगठित, भरोसेमंद और व्यावहारिक। वे परंपरा को महत्व देते हैं और योजना बनाने और कार्यों को पूरा करने में उत्कृष्ट होते हैं।"
    content.append(
        Paragraph(get_tags(istj_hindi),
                  base_style,
        )
    )
    # isfj_eng = r"2. ISFJ (The Protector) – Caring, sensitive, and highly dedicated. They prioritize the needs of others and are loyal in their relationships."
    isfj_hindi = r"2. ISFJ (The Protector) - देखभाल करने वाला, संवेदनशील और अत्यधिक समर्पित। वे दूसरों की जरूरतों को प्राथमिकता देते हैं और अपने रिश्तों में वफादार होते हैं।"
    content.append(
        Paragraph(get_tags(isfj_hindi),
            base_style,
        )
    )
    # infj_eng = r"3. INFJ (The Advocate) – Idealistic, insightful, and driven by a strong sense of morality. They are creative and often seek to help others."
    infj_hindi = r"3. INFJ (The Advocate) - आदर्शवादी, व्यावहारिक और नैतिकता की मजबूत भावना से प्रेरित। वे रचनात्मक होते हैं और अक्सर दूसरों की मदद करना चाहते हैं।"
    content.append(
        Paragraph(get_tags(infj_hindi),
                  base_style,
        )
    )
    # intj_eng = r"4. INTJ (The Architect) – Analytical, strategic, and determined. They are independent thinkers who thrive in solving complex problems."
    intj_hindi = r"4. INTJ (The Architect) - विश्लेषणात्मक, रणनीतिक और दृढ़निश्चयी। वे स्वतंत्र विचारक हैं जो जटिल समस्याओं को सुलझाने में कामयाब होते हैं।"
    content.append(
        Paragraph(get_tags(intj_hindi),
                  base_style,
        )
    )
    istp_eng = r"5. ISTP (The Crafter) – Practical, hands-on, and curious. They enjoy working with tools or systems and have a knack for understanding how things work."
    istp_hindi = r"5. ISTP (The Crafter) - व्यावहारिक, व्यावहारिक और जिज्ञासु। उन्हें टूल या सिस्टम के साथ काम करने में मजा आता है और उनमें यह समझने की क्षमता होती है कि चीजें कैसे काम करती हैं।"
    content.append(
        Paragraph(get_tags(istp_hindi),
                  base_style,
        )
    )
    isfp_eng = "6. ISFP (The Artist) – Gentle, flexible, and artistic. They prefer to express themselves through creative means and value their personal space."
    isfp_hindi = r"6. ISFP (The Artist) - सौम्य, लचीला और कलात्मक। वे रचनात्मक तरीकों से खुद को अभिव्यक्त करना पसंद करते हैं और अपने व्यक्तिगत स्थान को महत्व देते हैं।"
    content.append(
        Paragraph(get_tags(isfp_hindi),
                  base_style,
        )
    )
    infp_eng = "7. INFP (The Mediator) – Empathetic, introspective, and deeply idealistic. They focus on personal growth and are motivated by strong inner values."
    infp_hindi = "7. INFP (The Mediator) - सहानुभूतिपूर्ण, आत्मनिरीक्षणात्मक और गहन आदर्शवादी। वे व्यक्तिगत विकास पर ध्यान केंद्रित करते हैं और मजबूत आंतरिक मूल्यों से प्रेरित होते हैं।"
    content.append(
        Paragraph(get_tags(infp_hindi),
                  base_style,
        )
    )
    # intp_eng = "8. INTP (The Thinker) – Intellectual, analytical, and curious. They love theoretical discussions and problem-solving, often pursuing knowledge for its own sake."
    intp_hindi = "8. INTP (The Thinker) - बौद्धिक, विश्लेषणात्मक और जिज्ञासु। वे सैद्धांतिक चर्चा और समस्या-समाधान पसंद करते हैं, अक्सर ज्ञान को अपने स्वार्थ के लिए खोजते हैं।"
    content.append(
        Paragraph(get_tags(intp_hindi),
                  base_style,
        )
    )
    # estp_eng = "9. ESTP (The Dynamo) – Energetic, outgoing, and resourceful. They are action-oriented, enjoying challenges and taking risks in the moment."
    estp_hindi = "9. ESTP (The Dynamo) - ऊर्जावान, मिलनसार और साधन संपन्न। वे कार्य-उन्मुख हैं, चुनौतियों का आनंद ले रहे हैं और पल-पल जोखिम उठा रहे हैं।"
    content.append(
        Paragraph(get_tags(estp_hindi),
                  base_style,
        )
    )
    # esfp_eng = "10. ESFP (The Performer) – Sociable, spontaneous, and fun-loving. They thrive in social environments and enjoy living life to the fullest."
    esfp_hindi = "10. ESFP (The Performer) - मिलनसार, सहज और मौज-मस्ती करने वाला। वे सामाजिक परिवेश में पनपते हैं और जीवन का भरपूर आनंद लेते हैं।"
    content.append(
        Paragraph(get_tags(esfp_hindi),
                  base_style,
        )
    )
    enfp_eng = "11. ENFP (The Campaigner) – Enthusiastic, imaginative, and free-spirited. They are driven by creativity and enjoy inspiring others to pursue their passions."
    enfp_hindi = r"11. ENFP (The Campaigner) - उत्साही, कल्पनाशील और स्वतंत्र विचारों वाला। वे रचनात्मकता से प्रेरित होते हैं और अपने जुनून को आगे बढ़ाने के लिए दूसरों को प्रेरित करने का आनंद लेते हैं।"
    content.append(
        Paragraph(get_tags(enfp_hindi),
                  base_style,
        )
    )
    entp_eng = "12. ENTP (The Debater) – Quick-witted, clever, and curious. They love debates and intellectual challenges, often exploring multiple perspectives."
    entp_hindi = "12. ENTP (The Debater) - तेज-तर्रार, चतुर और जिज्ञासु। वे बहस और बौद्धिक चुनौतियों को पसंद करते हैं, अक्सर कई दृष्टिकोण तलाशते हैं।"
    content.append(
        Paragraph(get_tags(entp_hindi),
                  base_style,
        )
    )
    # estj_eng = "13. ESTJ (The Executive) – Organized, efficient, and practical. They value rules and order, often taking on leadership roles to ensure tasks are completed properly."
    estj_hindi = "13. ESTJ (The Executive) - संगठित, कुशल और व्यावहारिक। वे नियमों और व्यवस्था को महत्व देते हैं, अक्सर कार्यों को ठीक से पूरा करने के लिए नेतृत्व की भूमिका निभाते हैं।"
    content.append(
        Paragraph(get_tags(estj_hindi),
                  base_style,
        )
    )
    # entj_eng = "14. ENTJ (The Commander) – Assertive, confident, and strategic. They are natural leaders who focus on efficiency and long-term planning."
    entj_hindi = "14. ENTJ (The Commander)  - मुखर, आत्मविश्वासी और रणनीतिक। वे स्वाभाविक नेता हैं जो दक्षता और दीर्घकालिक योजना पर ध्यान केंद्रित करते हैं।"
    content.append(
        Paragraph(get_tags(entj_hindi),
                  base_style,
        )
    )
    # esfj_eng = "15. ESFJ (The Provider) – Caring, social, and harmonious, often placing a high value on relationships and duty."
    esfj_hindi = "15. ESFJ (The Provider) - देखभाल करने वाला, सामाजिक और सामंजस्यपूर्ण, अक्सर रिश्तों और कर्तव्य को उच्च महत्व देता है।"
    content.append(
        Paragraph(get_tags(esfj_hindi),
                  base_style,
        )
    )
    # enfj_eng = "16. ENFJ (The Giver) – Charismatic, warm, and inspiring leaders who enjoy helping and motivating others."
    enfj_hindi = "16. ENFJ (The Giver) - करिश्माई, गर्मजोशी भरे और प्रेरक नेता जो दूसरों की मदद करने और उन्हें प्रेरित करने का आनंद लेते हैं।"
    content.append(
        Paragraph(get_tags(enfj_hindi),
                  base_style,
        )
    )
    content.append(Spacer(1, 60))

    content.append(Paragraph("Your Personality Analysis", styles["Heading2"]))
    content.append(Image("personality_score_chart.png", width=520, height=280))
    content.append(Spacer(1, 12))
    content.append(Paragraph("Analysis:", styles["Heading2"]))
    # content.setFont("DevanagariFont", 10)
    # content.drawString(mixed_text.format(personality_comment), styles["BodyText"])
#     OUT1 = """इस छात्र की व्यक्तित्व वितरण से पता चलता है कि वे मुख्य रूप से ISFP प्रकार के हैं, जिसमें 15.8% का स्कोर है। यह दर्शाता है कि वे रचनात्मक, संवेदनशील और व्यक्तिगत अभिव्यक्ति के प्रति झुकाव रखते हैं। इसके अलावा, ENFJ और ISFJ प्रकार में भी उनका स्कोर उच्च है, जो कि 9.4% है, जिससे पता चलता है कि वे सहानुभूति रखने वाले और सामाजिक रूप से जागरूक हैं। ENTJ प्रकार में 10.8% के साथ, वे नेतृत्व क्षमता और आयोजनात्मक कौशल में भी मजबूत हैं। यह विविधता उन्हें विभिन्न परिस्थितियों में अनुकूलनीय और प्रभावी बनाती है।"""
#     OUT2 = """छात्र का योग्यता प्रदर्शन वितरण देखते हुए, यह स्पष्ट है कि छात्र ने सभी क्षेत्रों में समान रूप से अच्छा प्रदर्शन किया है। चाहे वह मात्रात्मक क्षमता हो, तार्किक सोच हो, परिस्थितिजन्य समस्या समाधान हो या मौखिक क्षमता हो, छात्र ने सभी में 4 अंक प्राप्त किए हैं। यह दर्शाता है कि छात्र की समग्र योग्यता और समझ बहुत अच्छी है और वह विभिन्न प्रकार की चुनौतियों का सामना करने में सक्षम है। इस तरह के संतुलित प्रदर्शन से छात्र के भविष्य में विभिन्न क्षेत्रों में सफलता की संभावनाएं बढ़ जाती हैं।"""
#     OUT3 = """छात्र के विषयगत योग्यता प्रदर्शन का वितरण देखते हुए, यह स्पष्ट होता है कि छात्र सामाजिक विज्ञान (SST) में सबसे अधिक प्रवीण है, जिसमें उसका स्कोर 12 है। रसायन विज्ञान और भौतिकी में भी उसका प्रदर्शन अच्छा है, दोनों में 7 अंक हैं। हालांकि, जीव विज्ञान और गणित में उसका स्कोर कम है, दोनों में केवल 4 अंक हैं। इस विश्लेषण से यह सुझाव मिलता है कि छात्र को जीव विज्ञान और गणित में अपने कौशल को सुधारने की आवश्यकता है, जबकि उसे रसायन विज्ञान और भौतिकी में अपनी मजबूती को बनाए रखना चाहिए। सामाजिक विज्ञान में उसकी उत्कृष्टता उसे इस क्षेत्र में और अधिक गहराई से अध्ययन करने का मौका देती है।"""
#     OUT4 = """छात्र के भावनात्मक गुणांक वितरण के अनुसार, उसकी संघर्ष प्रबंधन क्षमता बहुत उच्च है, जिसका स्कोर 9.5 है। यह दर्शाता है कि वह संघर्षों को सुलझाने में कुशल है। भावनात्मक नियमन और सहानुभूति में भी उसका स्कोर अच्छा है, जो 7.5 है, यह बताता है कि वह अपनी और दूसरों की भावनाओं को समझने और नियंत्रित करने में सक्षम है। हालांकि, भावनात्मक आत्म-जागरूकता में उसका स्कोर कम है, जो केवल 5.0 है, इसका मतलब है कि उसे अपनी भावनाओं की पहचान और समझ में सुधार की आवश्यकता है। भावनात्मक आत्म-क्षमता और प्रेरणा में उसके स्कोर क्रमशः 8.5 और 6.5 हैं, जो उसकी आत्म-विश्वास और उत्साह के स्तर को दर्शाते हैं।"""
#     OUT5 = """Based on the student's personality, aptitude, and emotional quotient distributions, here are the top 6 career options that would be best suited for the student:
#
# 1. **सामाजिक कार्यकर्ता (Social Worker)**:
#    - इस क्षेत्र में उच्च स्तर की सहानुभूति, संघर्ष प्रबंधन और सामाजिक व्यवहार की आवश्यकता होती है। छात्र के पास इन क्षमताओं का अच्छा स्तर है, जो उन्हें इस क्षेत्र में सफल बना सकता है।
#
# 2. **मानव संसाधन प्रबंधक (Human Resources Manager)**:
#    - इस भूमिका में संघर्ष प्रबंधन, भावनात्मक विनियमन और सहानुभूति जैसे गुणों की जरूरत होती है। छात्र के पास इन क्षेत्रों में अच्छी योग्यता है।
#
# 3. **साइकोलॉजिस्ट (Psychologist)**:
#    - इस पेशे में भावनात्मक समझ, सहानुभूति और भावनात्मक विनियमन की गहरी समझ की आवश्यकता होती है। छात्र के पास इन क्षेत्रों में उच्च स्कोर हैं।
#
# 4. **परामर्शदाता (Counselor)**:
#    - इस करियर में भावनात्मक सहायता प्रदान करने, संघर्षों को सुलझाने और भावनात्मक स्व-प्रभावकारिता में मदद करने की क्षमता महत्वपूर्ण होती है। छात्र के पास इन क्षेत्रों में अच्छे अंक हैं।
#
# 5. **शिक्षक (Teacher)**:
#    - विशेष रूप से सामाजिक विज्ञान या मानविकी"""

    # content.append(Paragraph(get_tags(personality_comment), styles["BodyText"]))
    content.append(Paragraph(get_tags(personality_comment), base_style))
    # print("#" * 60)
    # print("#" * 60)
    # # print(get_tags(OUT1))
    # print("#" * 60)
    # print("#" * 60)
    # content.append(Paragraph(get_tags(OUT1), base_style))
    content.append(Spacer(1, 12))
    content.append(get_divider())
    content.append(Spacer(1, 12))

    # Second Page - Aptitude Scores
    content.append(Paragraph("Aptitude Scores", styles["Heading2"]))

    abt_apt_eng = "Aptitude refers to a person's natural ability or talent to learn or perform certain tasks with ease, often in specific areas like logical reasoning, numerical skills, verbal ability, or spatial awareness. It is important for a career because it helps individuals identify their strengths and align their skills with professions where they are likely to excel. Employers also value aptitude as it indicates a candidate’s potential to learn, adapt, and succeed in the role. Understanding one’s aptitude can lead to better career choices, personal fulfillment, and professional growth"
    abt_apt_hindi = "Aptitude किसी व्यक्ति की स्वाभाविक क्षमता या प्रतिभा को सीखने या कुछ कार्यों को आसानी से करने के लिए संदर्भित करती है, अक्सर तार्किक तर्क, संख्यात्मक कौशल, मौखिक क्षमता या स्थानिक जागरूकता जैसे विशिष्ट क्षेत्रों में। यह करियर के लिए महत्वपूर्ण है क्योंकि यह व्यक्तियों को अपनी ताकत पहचानने और अपने कौशल को उन व्यवसायों के साथ संरेखित करने में मदद करता है जहां उनके उत्कृष्टता प्राप्त करने की संभावना है। नियोक्ता भी योग्यता को महत्व देते हैं क्योंकि यह उम्मीदवार की सीखने, अनुकूलन करने और भूमिका में सफल होने की क्षमता को इंगित करता है। किसी की योग्यता को समझने से बेहतर करियर विकल्प, व्यक्तिगत संतुष्टि और व्यावसायिक विकास हो सकता है"
    content.append(
        Paragraph(get_tags(abt_apt_hindi),
            base_style,
        )
    )
    abt_apt_quant_eng = "Quantitative Aptitude: The ability to solve numerical and mathematical problems, including arithmetic, algebra, and data interpretation."
    abt_apt_quant_hindi = "Quantitative Aptitude: अंकगणित, बीजगणित और डेटा व्याख्या सहित संख्यात्मक और गणितीय समस्याओं को हल करने की क्षमता।"
    content.append(
        Paragraph(get_tags(abt_apt_quant_hindi),
                  base_style,
        )
    )
    abt_apt_logical_eng = "Logical Reasoning: The ability to analyze patterns, solve puzzles, and draw logical conclusions based on given information."
    abt_apt_logical_hindi = "Logical Reasoning: पैटर्न का विश्लेषण करने, पहेलियाँ हल करने और दी गई जानकारी के आधार पर तार्किक निष्कर्ष निकालने की क्षमता।"
    content.append(
        Paragraph(get_tags(abt_apt_logical_hindi),
                  base_style,
        )
    )
    abt_apt_verbal_eng = "Verbal Reasoning: The ability to understand, interpret, and reason using written language, involving grammar, vocabulary, and comprehension."
    abt_apt_verbal_hindi = "Verbal Reasoning: व्याकरण, शब्दावली और समझ को शामिल करते हुए लिखित भाषा का उपयोग करके समझने, व्याख्या करने और तर्क करने की क्षमता।"
    content.append(
        Paragraph(get_tags(abt_apt_verbal_hindi),
                  base_style,
        )
    )
    abt_apt_sit_eng = "Situational Reasoning: It signifies how a candidate will respond to specific or generic workplace situations and assess if that behaviour is deemed appropriate or important."
    abt_apt_sit_hindi = "Situational Reasoning: यह दर्शाता है कि एक उम्मीदवार विशिष्ट या सामान्य कार्यस्थल स्थितियों पर कैसे प्रतिक्रिया देगा और यह आकलन करेगा कि क्या वह व्यवहार उचित या महत्वपूर्ण माना जाता है।"
    content.append(
        Paragraph(get_tags(abt_apt_sit_hindi),
                  base_style,
        )
    )
    content.append(Spacer(1, 12))

    content.append(Paragraph("Your Aptitude Analysis", styles["Heading2"]))
    content.append(Image("aptitude_chart.png", width=520, height=280))

    content.append(Spacer(1, 12))
    content.append(Paragraph("Analysis:", styles["Heading2"]))
    content.append(Paragraph(get_tags(sub_pot_comment), base_style))
    content.append(Spacer(1, 12))

    content.append(Spacer(1, 12))
    content.append(get_divider())
    content.append(Spacer(1, 12))

    #### Third Page - Skill Set Assessment
    content.append(Paragraph("Subjective Skill-Set Scores", styles["Heading2"]))
    subj_skill_score_eng = "The Subjective Skill-Set Scores Assessment is to assess skills and abilities across various areas, such as math, science, language, creativity, or problem-solving. This type of assessment is important for stream selection and choosing academic paths because it helps students align their strengths and preferences with the demands of different fields. By understanding where they excel or where their interests lie, students can make more informed decisions about their education, ensuring they choose a stream that maximizes their potential and enhances their chances of success and satisfaction in future careers."
    subj_skill_score_hindi = "Subjective Skill-Set Scores Assessment का उद्देश्य गणित, विज्ञान, भाषा, रचनात्मकता या समस्या-समाधान जैसे विभिन्न क्षेत्रों में कौशल और क्षमताओं का आकलन करना है। इस प्रकार का मूल्यांकन स्ट्रीम चयन और अकादमिक पथ चुनने के लिए महत्वपूर्ण है क्योंकि यह छात्रों को विभिन्न क्षेत्रों की मांगों के साथ उनकी ताकत और प्राथमिकताओं को संरेखित करने में मदद करता है। यह समझकर कि वे कहाँ उत्कृष्ट हैं या उनकी रुचियाँ कहाँ हैं, छात्र अपनी शिक्षा के बारे में अधिक जानकारीपूर्ण निर्णय ले सकते हैं, यह सुनिश्चित करते हुए कि वे एक ऐसी स्ट्रीम चुनें जो उनकी क्षमता को अधिकतम करे और भविष्य के करियर में उनकी सफलता और संतुष्टि की संभावनाओं को बढ़ाए।"
    content.append(
        Paragraph(get_tags(subj_skill_score_hindi),
            base_style,
        )
    )
    content.append(
        Paragraph("Subjective Skill-Set Scores & Assessment", styles["Heading2"])
    )
    content.append(Image("stream_chart.png", width=520, height=280))

    content.append(Spacer(1, 12))
    content.append(Paragraph("Analysis:", styles["Heading2"]))
    content.append(Paragraph(get_tags(sub_pot_comment), base_style))
    content.append(Spacer(1, 12))

    content.append(get_divider())
    content.append(Spacer(1, 12))

    #### Fourth Page - Emotional Quotient
    content.append(Paragraph("Emotional Quotient Scores", styles["Heading2"]))
    emt_quot_eng = "For a school student, Emotional Quotient (EQ) is crucial because it helps them manage their emotions, build strong relationships, and cope with challenges effectively. High EQ enables students to stay calm under pressure, resolve conflicts with peers, and communicate better with teachers and classmates. It also fosters empathy, allowing them to understand and support others, which enhances teamwork and social interactions. Additionally, being emotionally intelligent helps students handle stress, stay motivated, and maintain a positive attitude, all of which contribute to better academic performance and personal well-being."
    emt_quot_hindi = "एक स्कूली छात्र के लिए, Emotional Quotient (EQ) महत्वपूर्ण है क्योंकि यह उन्हें अपनी भावनाओं को प्रबंधित करने, मजबूत रिश्ते बनाने और चुनौतियों का प्रभावी ढंग से सामना करने में मदद करता है। उच्च ईक्यू छात्रों को दबाव में शांत रहने, साथियों के साथ विवादों को सुलझाने और शिक्षकों और सहपाठियों के साथ बेहतर संवाद करने में सक्षम बनाता है। यह सहानुभूति को भी बढ़ावा देता है, जिससे उन्हें दूसरों को समझने और उनका समर्थन करने की अनुमति मिलती है, जो टीम वर्क और सामाजिक संपर्क को बढ़ाता है। इसके अतिरिक्त, भावनात्मक रूप से बुद्धिमान होने से छात्रों को तनाव से निपटने, प्रेरित रहने और सकारात्मक दृष्टिकोण बनाए रखने में मदद मिलती है, जो सभी बेहतर शैक्षणिक प्रदर्शन और व्यक्तिगत कल्याण में योगदान करते हैं।"
    content.append(
        Paragraph(get_tags(emt_quot_hindi),
                  base_style,
        )
    )
    content.append(
        Paragraph("Emotional Quotient Scores & Assessment", styles["Heading2"])
    )
    content.append(Image("emotional_quotient.png", width=520, height=280))

    content.append(Spacer(1, 12))
    content.append(Paragraph("Analysis:", styles["Heading2"]))
    content.append(Paragraph(get_tags(personality_comment), base_style))
    content.append(Spacer(1, 12))

    content.append(get_divider())
    content.append(Spacer(1, 12))

    ### Fifth Page - Career Recommendation
    content.append(Paragraph("Top 6 career recommendation", styles["Heading2"]))
    # content.append(Paragraph("1. {}".format(career_option_list[0]), styles["Heading4"]))
    # content.append(Paragraph("2. {}".format(career_option_list[1]), styles["Heading4"]))
    # content.append(Paragraph("3. {}".format(career_option_list[2]), styles["Heading4"]))
    # content.append(Paragraph("4. {}".format(career_option_list[3]), styles["Heading4"]))
    # content.append(Paragraph("5. {}".format(career_option_list[4]), styles["Heading4"]))
    # content.append(Paragraph("6. {}".format(career_option_list[5]), styles["Heading4"]))
    # ###
    # for i in career_option_list:
    # content.append(Paragraph("{}".format(i), styles["Heading5"]))
    # content.append(Spacer(1, 12))
    content.append(Paragraph("{}".format(get_tags(career_option_list)), styles["Heading4"]))

    content.append(get_divider())
    content.append(Spacer(1, 12))

    # content.append(Image("psychometry_chart.png", width=400, height=200))
    # content.append(Spacer(1, 24))

    # # Third Page - Interests
    # content.append(Paragraph("Interest Breakdown", styles['Heading2']))
    # content.append(Paragraph("This section shows the student’s interests in different areas such as Science, Arts, Sports, and Technology.", styles['BodyText']))
    # content.append(Spacer(1, 12))
    # content.append(Image("interest_chart.png", width=400, height=400))

    # Build the PDF
    doc.build(content, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
    # doc.build(content)

    # Clean up images after generating the PDF
    os.remove("personality_score_chart.png")
    os.remove("aptitude_chart.png")
    # os.remove("psychometry_chart.png")
    os.remove("interest_chart.png")
    os.remove("stream_chart.png")
    os.remove("emotional_quotient.png")

    print(f"PDF generated: {pdf_filename}")


# Generate the report
# generate_pdf_report()
