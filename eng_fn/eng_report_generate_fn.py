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
    stream_option_list
):
    # Generate charts

    ### Bar Graphs
    generate_bar_chart(
        personality_scores, "Personality Scores", "personality_score_chart.png"
    )
    generate_bar_chart(aptitude_scores, "Aptitude Scores", "aptitude_chart.png")
    generate_bar_chart(stream_scores, "Stream Scores", "stream_chart.png")
    generate_bar_chart(interest_data, "Interest Breakdown", "interest_chart.png")
    generate_bar_chart(
        emotional_quotient, "Emotional Quotient", "emotional_quotient.png"
    )

    # Create a PDF
    date_time1 = datetime.now()
    # date1 = datetime.today().strftime('%Y-%m-%d')
    # report_folder1 = r"/Users/arvindyadav/Documents/1_GakudoAI_work/3_School_Stream_Selector/07_reports/01_english"
    # report_folder = os.path.join(report_folder1, date1)
    report_folder= "reports"
    os.makedirs(report_folder, exist_ok=True)
    # report_folder = r"/Users/arvindyadav/Documents/1_GakudoAI_work/3_School_Stream_Selector/07_reports/02_hindi"
    print("student_email:::", student_email)
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
    content.append(
        Paragraph(
            "Personality identification is important for career selection because it helps ensure a good job 	fit, enhances job satisfaction, and aligns with your natural strengths and preferences. It can guide you toward roles and environments where you’re most productive and happy, and it aids in finding a career that suits your stress management style and growth potential.",
            styles["BodyText"],
        )
    )
    content.append(Spacer(1, 12))
    content.append(Paragraph("Definition of 16-Personalities:", styles["Heading4"]))
    content.append(
        Paragraph(
            "1. ISTJ (The Inspector) – Organized, dependable, and practical. They value tradition and are excellent at planning and following through with tasks.",
            styles["BodyText"],
        )
    )
    content.append(
        Paragraph(
            "2. ISFJ (The Protector) – Caring, sensitive, and highly dedicated. They prioritize the needs of others and are loyal in their relationships.",
            styles["BodyText"],
        )
    )
    content.append(
        Paragraph(
            "3. INFJ (The Advocate) – Idealistic, insightful, and driven by a strong sense of morality. They are creative and often seek to help others.",
            styles["BodyText"],
        )
    )
    content.append(
        Paragraph(
            "4. INTJ (The Architect) – Analytical, strategic, and determined. They are independent thinkers who thrive in solving complex problems.",
            styles["BodyText"],
        )
    )
    content.append(
        Paragraph(
            "5. ISTP (The Crafter) – Practical, hands-on, and curious. They enjoy working with tools or systems and have a knack for understanding how things work.",
            styles["BodyText"],
        )
    )
    content.append(
        Paragraph(
            "6. ISFP (The Artist) – Gentle, flexible, and artistic. They prefer to express themselves through creative means and value their personal space.",
            styles["BodyText"],
        )
    )
    content.append(
        Paragraph(
            "7. INFP (The Mediator) – Empathetic, introspective, and deeply idealistic. They focus on personal growth and are motivated by strong inner values.",
            styles["BodyText"],
        )
    )
    content.append(
        Paragraph(
            "8. INTP (The Thinker) – Intellectual, analytical, and curious. They love theoretical discussions and problem-solving, often pursuing knowledge for its own sake.",
            styles["BodyText"],
        )
    )
    content.append(
        Paragraph(
            "9. ESTP (The Dynamo) – Energetic, outgoing, and resourceful. They are action-oriented, enjoying challenges and taking risks in the moment.",
            styles["BodyText"],
        )
    )
    content.append(
        Paragraph(
            "10. ESFP (The Performer) – Sociable, spontaneous, and fun-loving. They thrive in social environments and enjoy living life to the fullest.",
            styles["BodyText"],
        )
    )
    content.append(
        Paragraph(
            "11. ENFP (The Campaigner) – Enthusiastic, imaginative, and free-spirited. They are driven by creativity and enjoy inspiring others to pursue their passions.",
            styles["BodyText"],
        )
    )
    content.append(
        Paragraph(
            "12. ENTP (The Debater) – Quick-witted, clever, and curious. They love debates and intellectual challenges, often exploring multiple perspectives.",
            styles["BodyText"],
        )
    )
    content.append(
        Paragraph(
            "13. ESTJ (The Executive) – Organized, efficient, and practical. They value rules and order, often taking on leadership roles to ensure tasks are completed properly.",
            styles["BodyText"],
        )
    )
    content.append(
        Paragraph(
            "14. ENTJ (The Commander) – Assertive, confident, and strategic. They are natural leaders who focus on efficiency and long-term planning.",
            styles["BodyText"],
        )
    )
    content.append(
        Paragraph(
            "15. ESFJ (The Provider) – Caring, social, and harmonious, often placing a high value on relationships and duty.",
            styles["BodyText"],
        )
    )
    content.append(
        Paragraph(
            "16. ENFJ (The Giver) – Charismatic, warm, and inspiring leaders who enjoy helping and motivating others.",
            styles["BodyText"],
        )
    )
    content.append(Spacer(1, 60))

    content.append(Paragraph("Your Personality Analysis", styles["Heading2"]))
    content.append(Image("personality_score_chart.png", width=520, height=280))
    content.append(Spacer(1, 12))
    content.append(Paragraph("Analysis:", styles["Heading2"]))
    content.append(Paragraph(personality_comment, styles["BodyText"]))
    content.append(Spacer(1, 12))

    content.append(get_divider())
    content.append(Spacer(1, 12))

    # Second Page - Aptitude Scores
    content.append(Paragraph("Aptitude Scores", styles["Heading2"]))
    content.append(
        Paragraph(
            "Aptitude refers to a person's natural ability or talent to learn or perform certain tasks with ease, often in specific areas like logical reasoning, numerical skills, verbal ability, or spatial awareness. It is important for a career because it helps individuals identify their strengths and align their skills with professions where they are likely to excel. Employers also value aptitude as it indicates a candidate’s potential to learn, adapt, and succeed in the role. Understanding one’s aptitude can lead to better career choices, personal fulfillment, and professional growth",
            styles["BodyText"],
        )
    )
    content.append(
        Paragraph(
            "Quantitative Aptitude: The ability to solve numerical and mathematical problems, including arithmetic, algebra, and data interpretation.",
            styles["BodyText"],
        )
    )
    content.append(
        Paragraph(
            "Logical Reasoning: The ability to analyze patterns, solve puzzles, and draw logical conclusions based on given information.",
            styles["BodyText"],
        )
    )
    content.append(
        Paragraph(
            "Verbal Reasoning: The ability to understand, interpret, and reason using written language, involving grammar, vocabulary, and comprehension.",
            styles["BodyText"],
        )
    )
    content.append(
        Paragraph(
            "Situational Reasoning: It signifies how a candidate will respond to specific or generic workplace situations and assess if that behaviour is deemed appropriate or important.",
            styles["BodyText"],
        )
    )
    content.append(Spacer(1, 12))

    content.append(Paragraph("Your Aptitude Analysis", styles["Heading2"]))
    content.append(Image("aptitude_chart.png", width=520, height=280))

    content.append(Spacer(1, 12))
    content.append(Paragraph("Analysis:", styles["Heading2"]))
    content.append(Paragraph(aptitude_comment, styles["BodyText"]))
    content.append(Spacer(1, 12))

    content.append(Spacer(1, 12))
    content.append(get_divider())
    content.append(Spacer(1, 12))

    #### Third Page - Skill Set Assessment
    content.append(Paragraph("Subjective Skill-Set Scores", styles["Heading2"]))
    content.append(
        Paragraph(
            "The Subjective Skill-Set Scores Assessment is to assess skills and abilities across various areas, such as math, science, language, creativity, or problem-solving. This type of assessment is important for stream selection and choosing academic paths because it helps students align their strengths and preferences with the demands of different fields. By understanding where they excel or where their interests lie, students can make more informed decisions about their education, ensuring they choose a stream that maximizes their potential and enhances their chances of success and satisfaction in future careers.",
            styles["BodyText"],
        )
    )
    content.append(
        Paragraph("Subjective Skill-Set Scores & Assessment", styles["Heading2"])
    )
    content.append(Image("stream_chart.png", width=520, height=280))

    content.append(Spacer(1, 12))
    content.append(Paragraph("Analysis:", styles["Heading2"]))
    content.append(Paragraph(sub_pot_comment, styles["BodyText"]))
    content.append(Spacer(1, 12))

    content.append(get_divider())
    content.append(Spacer(1, 12))

    #### Fourth Page - Emotional Quotient
    content.append(Paragraph("Emotional Quotient Scores", styles["Heading2"]))
    content.append(
        Paragraph(
            "For a school student, Emotional Quotient (EQ) is crucial because it helps them manage their emotions, build strong relationships, and cope with challenges effectively. High EQ enables students to stay calm under pressure, resolve conflicts with peers, and communicate better with teachers and classmates. It also fosters empathy, allowing them to understand and support others, which enhances teamwork and social interactions. Additionally, being emotionally intelligent helps students handle stress, stay motivated, and maintain a positive attitude, all of which contribute to better academic performance and personal well-being.",
            styles["BodyText"],
        )
    )
    content.append(
        Paragraph("Emotional Quotient Scores & Assessment", styles["Heading2"])
    )
    content.append(Image("emotional_quotient.png", width=520, height=280))

    content.append(Spacer(1, 12))
    content.append(Paragraph("Analysis:", styles["Heading2"]))
    content.append(Paragraph(emotional_quetient_comment, styles["BodyText"]))
    content.append(Spacer(1, 12))

    content.append(get_divider())
    content.append(Spacer(1, 12))

    ### Fifth Page - Career Recommendation
    content.append(Paragraph("Recommendation", styles["Heading2"]))
    # content.append(Paragraph("1. {}".format(career_option_list[0]), styles["Heading4"]))
    # content.append(Paragraph("2. {}".format(career_option_list[1]), styles["Heading4"]))
    # content.append(Paragraph("3. {}".format(career_option_list[2]), styles["Heading4"]))
    # content.append(Paragraph("4. {}".format(career_option_list[3]), styles["Heading4"]))
    # content.append(Paragraph("5. {}".format(career_option_list[4]), styles["Heading4"]))
    # content.append(Paragraph("6. {}".format(career_option_list[5]), styles["Heading4"]))
    # ###
    # for i in career_option_list:
    #     content.append(Paragraph("{}".format(i), styles["Heading5"]))
    content.append(Paragraph("Stream  Recommendation:", styles["Heading4"]))
    content.append(Paragraph("{}".format(stream_option_list), styles["Heading5"]))
    content.append(Paragraph("Career Option Recommendation:", styles["Heading4"]))
    content.append(Paragraph("{}".format(career_option_list), styles["Heading5"]))
    content.append(Spacer(1, 12))
    # content.append(Paragraph("{}".format(career_option_list), styles["Heading5"]))

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
    return pdf_filename


# Generate the report
# generate_pdf_report()
