from app import text_parser
from num2words import num2words

def test_letter_to_number():
    words = [num2words(elem) for elem in list(range(10))] 
    assert all([text_parser.letter_to_number(word).isdigit() for word in words])
    
def test_first_phone_number_parse():
    text = """
    Hi th5e1r6e sevEN sEvEn I'm brandi
    thRee and I'4m071 looking for a good time :)
    """
    assert "5167734071" == text_parser.phone_number_parse(text)

def test_second_phone_number_parse():
    text = """
    Hi there 516SevensEVENThree40SeVen1 is my number.  Give me a call!
    """
    assert "5167734071" == text_parser.phone_number_parse(text)

def test_third_phone_number_parse():
    text = """
    Hi there I'm brandi I'm a 23 yr old and I'm super hot. 516SevensEVENThree40SeVen1 is my number.  Give me a call!
    """
    print(text_parser.phone_number_parse(text))
    assert "5167734071" == text_parser.phone_number_parse(text)

