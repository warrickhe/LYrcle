import pinyin #https://pypi.org/project/pinyin/ to translate from chinese to pinyin and to english
import pinyin.cedict

def translate_phrase(phrase):
    # Modified to return a tuple of (original, pinyin, english)
    if not phrase.strip():  # Skip empty phrases
        return None
    
    # Try to translate the whole phrase first
    translations = pinyin.cedict.translate_word(phrase)
    if translations is not None:
        pinyin_text = pinyin.get(phrase)
        return (phrase, pinyin_text, translations[0])
    
    # If whole phrase doesn't work, break it down character by character
    if len(phrase) > 1:
        result = []
        for char in phrase:
            char_translation = translate_phrase(char)
            if char_translation:
                result.append(char_translation)
        return result if result else None
    
    return None

def translate(lyrics):
    result = []
    
    for line in lyrics:
        line_result = []
        current_non_chinese = ""
        i = 0
        
        while i < len(line):
            # If it's a Chinese character
            if i < len(line) and pinyin.cedict.translate_word(line[i]) is not None:
                # First append any accumulated non-Chinese text
                if current_non_chinese:
                    line_result.append(current_non_chinese.strip())
                    current_non_chinese = ""
                
                # Greedy approach: try to find the longest possible phrase
                best_end = i
                best_translation = None
                
                # Try different phrase lengths, starting from the longest possible
                for end in range(len(line), i, -1):
                    candidate_phrase = line[i:end]
                    # Only attempt translation if all characters are Chinese
                    if all(pinyin.cedict.translate_word(char) is not None for char in candidate_phrase):
                        translation = translate_phrase(candidate_phrase)
                        if translation and not isinstance(translation, list):
                            # Found a complete phrase translation
                            best_end = end
                            best_translation = translation
                            break
                
                # If we found a phrase translation, use it
                if best_translation:
                    line_result.append(best_translation)
                    i = best_end  # Skip to the end of the phrase
                else:
                    # Fall back to character-by-character translation
                    char_translation = translate_phrase(line[i])
                    if char_translation:
                        if isinstance(char_translation, list):
                            line_result.extend(char_translation)
                        else:
                            line_result.append(char_translation)
                    i += 1
            else:
                # It's not a Chinese character
                current_non_chinese += line[i]
                i += 1
        
        # Handle any remaining non-Chinese text
        if current_non_chinese:
            line_result.append(current_non_chinese.strip())
        
        result.append(line_result)
    
    return result

# lyrics = [
#     "header1",
#     "header2",
#     "header3",
#     "你好 world",
#     "我爱你"
# ]
# result = translate(lyrics)
# print(result)
# result returns [['header1'], ['header2'], ['header3'], [('你好', 'nǐhǎo', 'Hello!'), 'world'], [('我爱你', 'wǒ ài nǐ', 'I love you')]]