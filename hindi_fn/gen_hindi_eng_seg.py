from reportlab.lib import styles
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet


def is_hindi(word):
    """Check if a word is in Hindi (Devanagari script)."""
    return any("\u0900" <= char <= "\u097F" for char in word)


def is_english(word):
    """Check if a word is in English (Latin alphabet)."""
    return all("a" <= char.lower() <= "z" for char in word if char.isalpha())


def check_lang(word):
    if is_hindi(word):
        return (word, "Hindi")
    if is_english(word):
        return (word, "Eng")
    else:
        return (word, "Other")


# Path to your Devanagari-compatible font
hindi_font_path = "./hindi_fn/NotoSansDevanagari-Regular.ttf"  # Replace with the path to your Devanagari font
# hindi_font_path = "./hindi_fn/Lohit-Devanagari.ttf"  # Replace with the path to your Devanagari font
# hindi_font_path = "./hindi_fn/mangal_regular.ttf"  # Replace with the path to your Devanagari font
english_font_path = "./hindi_fn/TimesNewRoman.ttf"  # Default font for English

# Register Hindi and English fonts
pdfmetrics.registerFont(TTFont("HindiFont", hindi_font_path))
pdfmetrics.registerFont(TTFont("EnglishFont", english_font_path))

# Create a document template
doc = SimpleDocTemplate("output_mixed.pdf", pagesize=A4)

# Get a sample stylesheet
styles = getSampleStyleSheet()

# Define separate styles for Hindi and English
hindi_style = styles["BodyText"].clone("HindiStyle")
hindi_style.fontName = "HindiFont"
hindi_style.fontSize = 12

english_style = styles["BodyText"].clone("EnglishStyle")
english_style.fontName = "EnglishFont"
english_style.fontSize = 12

mixed_text = """
<font name="EnglishFont">Hello, </font><font name="HindiFont">यह एक हिंदी वाक्य है</font><font name="EnglishFont"> with some English text.</font>
"""

# styles = getSampleStyleSheet()
base_style = styles["BodyText"]
base_style.fontSize = 12

eng_tag = """<font name="EnglishFont">{}</font>"""
hindi_tag = """<font name="HindiFont">{}</font>"""

# Sample mixed Hindi and English text with inline style switching
text1 = """Sample mixed Hindi and English text with inline style switching"""
text3 = """इस छात्र की व्यक्तित्व वितरण के अनुसार, वह मुख्य रूप से ISFP प्रकार का है, जिसमें 15.8% का स्कोर है। यह दर्शाता है कि वह रचनात्मक, संवेदनशील और व्यक्तिगत मूल्यों के प्रति समर्पित है। इसके अलावा, ENFJ और ISFJ प्रकार में भी उनका स्कोर 9.4% है, जो उनकी सहानुभूति और दूसरों की मदद करने की इच्छा को दर्शाता है। ENTJ प्रकार में 10.8% स्कोर के साथ, वह नेतृत्व क्षमता और आयोजनात्मक कौशल में भी मजबूत है। इस तरह के व्यक्तित्व विशेषताओं के साथ, वह ऐसे करियर में सफल हो सकता है जहां रचनात्मकता, व्यक्तिगत इंटरैक्शन और नेतृत्व की आवश्यकता होती है।"""
textc = ". **स्कूल काउंसलर (School Counselor)**: - इस भूमिका में भावनात्मक समर्थन, सहानुभूति और भावनात्मक विनियमन की आवश्यकता होती है। छात्र के पास इन क्षमताओं का अच्छा स्तर है, जो उन्हें इस क्षेत्र में उपयुक्त बनाता है।"

def get_tags(text):
    all_text_tag = []
    text_splitted = text.split(" ")
    text_splitted_tag = [check_lang(i) for i in text_splitted]
    if len(text_splitted_tag) > 0:
        temp_list = []
        temp_lang = "English"
        for i, word_lang in enumerate(text_splitted_tag):
            word, lang = word_lang
            if lang == temp_lang:
                temp_list.append(word)
            else:
                if len(temp_list) > 0:
                    textf = " ".join(temp_list)
                    if temp_lang == "Hindi":
                        all_text_tag.append(hindi_tag.format(textf))
                    else:
                        all_text_tag.append(eng_tag.format(textf))
                temp_lang = lang
                temp_list = [word]
        if len(temp_list) > 0:
            textf = " ".join(temp_list)
            if lang == "Hindi":
                all_text_tag.append(hindi_tag.format(textf))
            else:
                all_text_tag.append(eng_tag.format(textf))
    return " ".join(all_text_tag)


print("#" * 50)
print(get_tags(text3))
