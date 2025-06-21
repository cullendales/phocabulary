from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from collections import Counter
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

def translate_text(words):
    model_name = "VietAI/envit5-translation"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    
    for word in words:
        input_text = f"vi: {word}"
        inputs = tokenizer(input_text, return_tensors="pt", padding=True)
        outputs = model.generate(inputs.input_ids, max_length=512)
        translation = tokenizer.decode(outputs[0], skip_special_tokens=True)

        if translation.startswith("en: "):
            translation = translation[4:]
        
        print("Words to know from the article: ")
        print(f"{word} : {translation}")

def common_words(article_data):
    article = article_data.get('text', 'N/A')
    
    words = article.split()
    word_count = Counter(words)
    
    common_words_set = {
        "và", "là", "của", "tôi", "bạn", "anh", "chị", "em", "ông", "bà",
        "cái", "con", "này", "kia", "một", "hai", "ba", "bốn", "năm", "sáu",
        "bảy", "tám", "chín", "mười", "không", "có", "được", "đi", "về",
        "ăn", "uống", "làm", "học", "nói", "biết", "hiểu", "yêu", "thích",
        "ghét", "đẹp", "xấu", "tốt", "mới", "cũ", "nhiều", "ít", "lớn",
        "nhỏ", "ở", "đâu", "đây", "kia", "rồi", "nữa", "sao", "khi", "vì",
        "nên", "nếu", "rất", "hơn", "nhất", "với", "trong", "ngoài", "trên",
        "dưới", "sau", "trước", "như", "cho", "đến", "từ", "về", "qua",
        "lại", "đang", "sẽ", "vừa", "đã", "ấy", "cô"
    }

    for word in list(word_count.keys()):
        if word in common_words_set:
            del word_count[word]

    MAX_WORDS = 6
    res = []
    for i in range(min(MAX_WORDS, len(word_count))):
        if not word_count: 
            break
        curr_max = max(word_count, key=word_count.get)
        res.append(curr_max)
        del word_count[curr_max]
    
    return res
    
