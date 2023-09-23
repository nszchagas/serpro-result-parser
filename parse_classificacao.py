import re
import sys
from pypdf import PdfReader





filename='serpro.pdf'
reader = PdfReader(filename)
# pat=r'(\d{8}.*?\/)'
pat=r'\d{8}.*?(?=\/)'
qt_pages=len(reader.pages)
pages_comum=67
text = ''.join(map(lambda x:x.extract_text(), reader.pages[:pages_comum]))


page=text.split('1.1.1')[0].replace('\n', '')
match = re.findall(pat, page)
last=False
for m in match:
    m=m.replace("/", "")
    if len(m) > 200 or "Yuri Tadeu de Souza Carvalho" in m:
        m=m.split('1.1.1')[0]
        last=True
    m=m.strip()
    if m[-1] == '.':
        m=m[:-1]
    data=m.split(',')
    # data = list(map(lambda x: x.replace(" ", ""), data))
    
    num_inscr, nome = m.split(",")[0:2]
    
    numbers = m.split(",")[2:]
    
    numbers = list(map(lambda x: float(x.strip().split(' ')[0]), numbers ))
    
    
    nt_pt, crt_pt, nt_ing, crt_ing, nt_pe, crt_pe, nt_rac, crt_rac, nt_leg, crt_leg, nt_bas, crt_bas, nt_esp, crt_esp, nt_final_obj = numbers
    
    
    
    valid = crt_pt <= 18 and nt_pt <= 18 and  \
    crt_ing <= 12 and nt_ing <= 12 and  \
    crt_pe <= 5 and nt_pe <=  5 and  \
    crt_rac <= 10 and nt_rac <= 10 and  \
    crt_leg <= 5 and nt_leg <=  5 and  \
    crt_bas <= 50 and nt_bas <= 50 and  \
    crt_esp <= 70 and nt_esp <= 70
    
    notas=[nt_pt, crt_pt, nt_ing, crt_ing, nt_pe, crt_pe, nt_rac, crt_rac, nt_leg, crt_leg, nt_bas, crt_bas, nt_esp, crt_esp, nt_final_obj]
    
    if valid: 
        print(f"INSERT INTO SERPRO(num_inscr, nome, nt_pt, crt_pt, nt_ing, crt_ing, nt_pe, crt_pe, nt_rac, crt_rac, nt_leg, crt_leg, nt_bas, crt_bas, nt_esp, crt_esp, nt_final_obj) VALUES")
        print(f"({data[0]},\'{data[1].strip()}\',{','.join(map(str, notas))}) ON CONFLICT DO NOTHING;")
    else: 
        print(f">>>>>> Invalid values: {m}\n", file = sys.stderr)
        print(f"INSERT INTO SERPRO(num_inscr, nome, nt_pt, crt_pt, nt_ing, crt_ing, nt_pe, crt_pe, nt_rac, crt_rac, nt_leg, crt_leg, nt_bas, crt_bas, nt_esp, crt_esp, nt_final_obj) VALUES", file = sys.stderr)
        print(f"('{data[0]}',\'{data[1].strip()}\',{','.join(map(str, notas))}) ON CONFLICT DO NOTHING;", file = sys.stderr)
        
    # nt_final_obj = float(nt_final_obj.replace(' ', '').replace('.', ''))        
    # print(num_inscr, nome, nt_pt, crt_pt, nt_ing, crt_ing, nt_pe, crt_pe, nt_rac, crt_rac, nt_leg, crt_leg, nt_bas, crt_bas, nt_esp, crt_esp, nt_final_obj)
    if last:
        break




# for x in map(lambda x: f'{x["nome"]}, {x["nt"]}', sorted_nts):
#     print(x)



