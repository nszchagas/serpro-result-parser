import re
import sys
from pypdf import PdfReader


filename='serpro_pratica.pdf'

reader = PdfReader(filename)
pat=r'\d{8}.*?(?=\/)'
pages_comum=67
text = ''.join(map(lambda x:x.extract_text(), reader.pages[:pages_comum]))


page=text.split('1.1.1')[0].replace('\n', '')
match = re.findall(pat, page)
last=False

for m in match:
    m=m.replace("/", "")
    if len(m) > 200:
        m=m.split('1.1.1')[0]
        last=True
    m=m.strip()
    if m[-1] == '.':
        m=m[:-1]
    data=m.split(',')
    num_inscr, nome, nt_final_pratica = m.split(",")
    nt_final_pratica = float(nt_final_pratica.replace(' ', ''))
    if  nt_final_pratica <= 100:
        print(f"UPDATE SERPRO SET nt_final_pratica = {nt_final_pratica} WHERE num_inscr = '{num_inscr}';")
    else: 
        print(f"UPDATE SERPRO SET nt_final_pratica = {nt_final_pratica} WHERE num_inscr = '{num_inscr}';", file=sys.stderr)
        print(f">>>>>> Invalid values: \n", num_inscr, nome, nt_final_pratica, file = sys.stderr)
    
    if last:
        break




