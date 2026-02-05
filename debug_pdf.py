import PyPDF2
import re

# Compare January and February PDFs
with open('debug_output.txt', 'w', encoding='utf-8') as out:
    for pdf_name in ['January-2026.pdf', 'February-2026.pdf']:
        out.write(f'\n\n{"="*60}\n')
        out.write(f'ANALYZING: {pdf_name}\n')
        out.write(f'{"="*60}\n')
        
        f = open(pdf_name, 'rb')
        r = PyPDF2.PdfReader(f)
        
        text = ''
        for i in range(len(r.pages)):
            text += r.pages[i].extract_text()
        
        t = text.strip()
        sections = t.split('ΠΡΟΣΦΕΡΟΜΕΝΟ')
        finalt = [s for s in sections[1:] if 'ΝΗΣΤΙΣΙΜΕΣ' not in s and 'ΒΕΛΤΙΩΜΕΝΟ' in s]
        
        out.write(f'Pages: {len(r.pages)}\n')
        out.write(f'Total ΠΡΟΣΦΕΡΟΜΕΝΟ sections: {len(sections)}\n')
        out.write(f'Filtered finalt sections: {len(finalt)}\n')
        
        # Check structure of each finalt section
        for idx, sec in enumerate(finalt):
            # Count expected patterns
            deipno_count = len(re.findall('ΔΕΙΠΝΟ', sec))
            prwto_count = len(re.findall('Πρώτο', sec))
            gevma_count = len(re.findall('ΓΕΥΜΑ', sec))
            
            is_last = idx == len(finalt) - 1
            prwino_present = 'ΠΡΩΙΝΟ' in sec or 'Πρωινό' in sec
            
            status = 'OK' if deipno_count >= 1 and prwto_count >= 2 else 'PROBLEM'
            
            out.write(f'  Section {idx}: ΔΕΙΠΝΟ={deipno_count}, Πρώτο={prwto_count}, ΓΕΥΜΑ={gevma_count}, Last={is_last}, ΠΡΩΙΝΟ={prwino_present} [{status}]\n')
            
            if status == 'PROBLEM':
                out.write(f'    Section content (first 500 chars):\n')
                out.write(f'    {sec[:500]}\n')
        
        f.close()

print("Output written to debug_output.txt")
