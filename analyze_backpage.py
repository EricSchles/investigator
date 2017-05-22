from app.metric_generation import *

def main():
    print("Phrase frequency categorized by phone number")
    print(phrase_frequency_categorized_by_phone_number())

    print("Overall frequency phrase frequency")
    print(overall_comparison())

    print("Average phrase similarity between documents by phone number")
    print(average_phrase_similarity_between_documents_by_phone_number())

if __name__ == '__main__':
    main()
