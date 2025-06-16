from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from collections import Counter

def translate_text(words):
    model_name = "VietAI/envit5-translation"
    tokenizer = AutoTokenizer.from_pretrained(model_name)  
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    inputs = " ".join(words)

    outputs = model.generate(tokenizer(inputs, return_tensors="pt", padding=True).input_ids, max_length=512)
    translations = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
    translated_words = translations.split()

    for vn_word, en_word in zip(words, translated_words):
        print(f"{vn_word} : {en_word}")


def common_words(article_data):

    article = article_data.get('text', 'N/A')

    word_count = Counter(article)
    common_words = {
                    "và", "là", "của", "tôi", "bạn", "anh", "chị", "em", "ông", "bà",
                    "cái", "con", "này", "kia", "một", "hai", "ba", "bốn", "năm", "sáu",
                    "bảy", "tám", "chín", "mười", "không", "có", "được", "đi", "về",
                    "ăn", "uống", "làm", "học", "nói", "biết", "hiểu", "yêu", "thích",
                    "ghét", "đẹp", "xấu", "tốt", "mới", "cũ", "nhiều", "ít", "lớn",
                    "nhỏ", "ở", "đâu", "đây", "kia", "rồi", "nữa", "sao", "khi", "vì",
                    "nên", "nếu", "rất", "hơn", "nhất", "với", "trong", "ngoài", "trên",
                    "dưới", "sau", "trước", "như", "cho", "đến", "từ", "về", "qua",
                    "lại", "đang", "sẽ", "vừa", "đã"
                }

    for word in list(word_count):
        if word_count[word] in common_words:
            del word_count[word]

    MAX_WORDS = 6
    res = []

    for i in range(MAX_WORDS):
        curr_max = max(word_count, key = word_count.get)
        res.append(curr_max)
        del word_count[curr_max]

    return res

    
