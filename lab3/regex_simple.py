import re
text = "abc is the beginning of the alphabet and ends with xyz"
pattern = r"b"
match = re.match(pattern, text)
print(match.group() if match else "No match")

text = "abc abc abcxyz abcdfd bcv"
pattern = r"c"
matches = re.findall(pattern, text)
print(matches)

text = "afc"
pattern = r"a.c"
match = re.match(pattern, text)
print(match.group() if match else "No match")

text = "abc ac axc"
pattern = r"a.c"
matches = re.findall(pattern, text)
print(matches)

text = "abcdef"
pattern = r"^abc"
match = re.match(pattern, text)
print(match.group() if match else "No match")

text = "abcdefabcabcd"
pattern = r"^abc"
matches = re.findall(pattern, text)
print(matches)

text = "xyzabc"
pattern = r"abc$"
match = re.search(pattern, text)
print(match.group() if match else "No match")


text = "abc def abc"
pattern = r"abc$"
matches = re.findall(pattern, text)
print(matches)


text = "hello world all item"
pattern = r"[aioue]"
match = re.search(pattern, text)
print(match.group() if match else "No match")


list_symb = []
for letter in text:
    for symb in pattern:
        if letter == symb:
            print(letter)
            list_symb.append(letter)
        

text = "hello world all item"
pattern = r"[aeiou]"
matches = re.findall(pattern, text)
print(matches)

text = "abc9123 123"
pattern = r"[0-9]"
match = re.search(pattern, text)
print(match.group() if match else "No match")


text = "abc123 def456 9"
pattern = r"[0-9]"
matches = re.findall(pattern, text)
print(matches)



text = "abcc abccc"
pattern = r"abc*"
match = re.match(pattern, text)
print(match.group() if match else "No match")

text = "abcc ab ac a bc"
pattern = r"abc*"
matches = re.findall(pattern, text)
print(matches)


text_1 = "ac abcc ac abc"
text_2 = "abc ac abc"
pattern = r"abc+"
match = re.match(pattern, text_1)
match_2 = re.match(pattern, text_2)
print(match.group() if match else "No match")
print(match_2.group() if match_2 else "No match_2")

text = "abcc abc a abccdhjdsf ab"
pattern = r"abc+"
matches = re.findall(pattern, text)
print(matches)

text = "abdca"
pattern = r"abc?"
match = re.match(pattern, text)
print(match.group() if match else "No match")

text = "abcdfadcsadcs abcds a abcc abgfda"
pattern = r"abcdf+"
matches = re.findall(pattern, text)
print(matches)

text = "abcabcabcabc abc"
pattern = r"(abc)+"
match = re.match(pattern, text)
print(match.group() if match else "No match")

text = "abcabc abchello abdcc"
pattern = r"(abc)+"
matches = re.findall(pattern, text)
print(matches)

text = "abc abcdef"
pattern = r"abc|"
match = re.match(pattern, text)
print(match.group() if match else "No match")

text = "abc def abc abcdef"
pattern = r"abc|abcdef|def|abcdef"
matches = re.findall(pattern, text)
print(matches)

text = "file.txt"
pattern = r"\."
match = re.search(pattern, text)
print(match.group(0) if match else "No match")

text = "file.txt image.jpg"
pattern = r"\."
matches = re.findall(pattern, text)
print(matches)

text_1 = "document.pdf"
pattern = r"\.([a-zA-Z0-9]+)$"
match = re.search(pattern, text_1)
match.group(0)


file_names = ["document.pdf", "image.jpeg", "data.csv", "README.md", "file"]

pattern = r"\.([a-zA-Z0-9]+)$"

for file in file_names:
    match = re.search(pattern, file)
    if match:
        print(f"File: {file}, Extension: {match.group(1)}")
    else:
        print(f"File: {file}, No extension found")


text = "There are 123 apples."

pattern = r"\d"

matches = re.findall(pattern, text)
print(matches)

text = "Order number: 123ABC!"
pattern = r"\D"
matches = re.findall(pattern, text)
print(matches)

text = "Python_3 is fun!"
pattern = r"\w"
matches = re.findall(pattern, text)
print(matches)

text = "Hello, world! #Python3"
pattern = r"\W"
matches = re.findall(pattern, text)
print(matches)

text = "This is\tan example\nwith spaces."
pattern = r"\s"
matches = re.findall(pattern, text)
print(matches)

text = "This is\tan example\nwith spaces."
pattern = r"\S"
matches = re.findall(pattern, text)
print(matches)

text = "Hello, world! Hello, Hello,"
pattern = r"Hello,"

match = re.match(pattern, text)
print(match.group(0) if match else "No match")


def def_match(pattern, text):
    text_s = text.split()

    for elem in text_s:
        if elem == pattern:
            return elem
        

def def_find_all(pattern, text):
    all_list = []
    text_s = text.split()

    for elem in text_s:
        if elem == pattern:
            all_list.append(elem)
    return all_list



text = "Hello, world start"
pattern = r"(Hello), (world) (start)"

match = re.match(pattern, text)
print(match.group(0))  # Entire match
print(match.group(1))  # First captured group ("Hello")
print(match.group(2))  # Second captured group ("world")

text = "The; fox quick, brown fox fox"
pattern = r"fox"

search = re.search(pattern, text)
print(search.group() if search else "No match")

print(search.start())
print(search.end())


text = " quick The 12 quick 34 brown 56 foxes. quick "
pattern = r"\d+"  # Matches one or more digits
#pattern = r"quick" 
matches = re.findall(pattern, text)
print(matches)

text = "The 12 quick 34 brown 56 foxes."
pattern = r"\d+"  # Matches one or more digits

matches = re.finditer(pattern, text)
for match in matches:
    print(f"Found {match.group()} at position {match.start()} to {match.end()}")


text = "Hello, worlds!"
pattern = r"world"
replacement = "Python"

new_text = re.sub(pattern, replacement, text)
print(new_text)

text = "apple,banana. cherry,orange?pineapple"
pattern = r"[.;,?]"

split_text = re.split(pattern, text)
print(split_text)

pattern = re.compile(r"The")  # Compile a pattern that matches one or more digits
text = "The numbers The are 123 and 456"

matches = pattern.findall(text)
print(matches)
pattern.search('The numbers are 123 and 456').group()


text = "abc123"
pattern = r"abc123"

match = re.fullmatch(pattern, text)
print(match.group() if match else "No match")

pattern1 = re.compile(r"\d+")
pattern2 = re.compile(r"[a-z]+")

re.purge()


text = "Hello.$ How * are you?"
escaped_text = re.escape(text)
print(escaped_text)

pattern = r"\\[.*$^()|?+{}[\]]"  

matches = re.findall(pattern, escaped_text)
print(f"Extracted Special Characters: {matches}")

words = re.findall(r'\b\w+\b', text)

print(f"Extracted Words: {words}")


import re

text = "I like cats, cats are great!"
pattern = r"cats"
replacement = "dogs"

new_text, num_subs = re.subn(pattern, replacement, text)
print(new_text)  
print(num_subs)  

text = "The quick brown fox"
substring = "quick"

index = text.find(substring)
print(index)  # Output: 4

def find_str(substring, text):

    index = text.find(substring)
    #return len(substring)
    #return text[index:]
    return text[index : index + len(substring)]


text = "I love apples, apples are great!"
new_text = text.replace("apples", "oranges")
print(new_text)  # Output: I love oranges, oranges are great!
text = "apple,banana,orange"
fruits = text.split(",")
print(fruits)  # Output: ['apple', 'banana', 'orange']



from pyparsing import Word, alphas, nums

word = Word(alphas)  # Matches a word of alphabetic characters
number = Word(nums)  # Matches a number of digits

pattern = word + number

text = "Hello 123"
result = pattern.parseString(text)

print(result) 


import regex

text = "Café"  # "é" is a Unicode character
pattern = r"\p{L}+"  # Matches one or more Unicode letters

matches = regex.findall(pattern, text)
print(matches)  # Output: ['Café']