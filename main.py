from language import translate_text, common_words
from news import get_news, print_article


def main():
    category = input("Enter a news category in English (ie. politics, sports, etc.) to search for: ") 
    res = []
    res = get_news(category)

    url = input("Enter the exact url of the article you would like to view: ") # I will change to a system like a number representing each article and selecting the number
    article = print_article(url)

    vn_most_used_terms = common_words(article)

    #translate_text(vn_most_used_terms)

if __name__ == "__main__":
    main()
