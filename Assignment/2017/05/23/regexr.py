import re

story = '''Born to the prestigious Crownguards, the paragon family of Demacian service, Luxanna was destined for greatness. She grew up as the family's only daughter, and she immediately took to the advanced education and lavish parties required of families as high profile as the Crownguards. As Lux matured, it became clear that she was extraordinarily gifted. She could play tricks that made people believe they had seen things that did not actually exist. She could also hide in plain sight. Somehow, she was able to reverse engineer arcane magical spells after seeing them cast only once. She was hailed as a prodigy, drawing the affections of the Demacian government, military, and citizens alike.
As one of the youngest women to be tested by the College of Magic, she was discovered to possess a unique command over the powers of light. The young Lux viewed this as a great gift, something for her to embrace and use in the name of good. Realizing her unique skills, the Demacian military recruited and trained her in covert operations. She quickly became renowned for her daring achievements; the most dangerous of which found her deep in the chambers of the Noxian High Command. She extracted valuable inside information about the Noxus-Ionian conflict, earning her great favor with Demacians and Ionians alike. However, reconnaissance and surveillance was not for her. A light of her people, Lux's true calling was the League of Legends, where she could follow in her brother's footsteps and unleash her gifts as an inspiration for all of Demacia.'''

# 1번
# {m}패턴지정자를 사용해서 a로 시작하는 4글자 단어를 전부 찾는다.
print(re.findall('\sa\w{3}\s', story))

# 해답
# 위처럼 하니까 공백문자가 포함되는 문제가 있었는데 \b 로 하니까 괜찮아졌다.
print(re.findall(r'\ba\w{3}\b', story))



# 2번
# r로 끝나는 모든 단어를 찾는다.
print(re.findall('\w*r\s', story))

# 해답
print(re.findall(r'\w+r\b', story))



# 3번
# a,b,c,d,e중 아무 문자나 3번 연속으로 들어간 단어를 찾는다.
# ex) b[eca]me
print(re.findall('\w*[a-e]{3}\w*', story))

# 해답
print(re.findall('\w*[abcde]{3}\w*', story))


# 4번
def re_change(m):
    return '{}{}[{}]'.format(m.group('before').upper(), m.group('center'), m.group('after'))
# re.sub를 사용해서 ,로 구분된 앞/뒤 단어에 대해 앞단어는 대문자화 시키고, 뒷단어는 대괄호로 감싼다.
# 이 과정에서, 각각의 앞/뒤에 before, after그룹 이름을 사용한다.
# re.split(',', ,story)
p = re.compile(r'(?P<before>\w+)(?P<center>\s*,\s*)(?P<after>\w+)')
result = re.sub(p, re_change, story)

print(result)