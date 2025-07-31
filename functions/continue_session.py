import csv, os
from functions.__csv_loader import  Session

def main(*args, session=None):
    curr_path = os.path.join(os.path.dirname(__file__), '../data/current_session.csv')
    curr_path = os.path.abspath(curr_path)
    try:
        with open('current_session.csv', 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            
            if not rows:
                print("No ongoing sessions found.")
                return
            
            last_session = rows[-1]
            session = Session()
            
            # try to eval lists/dicsts, else keep as string
            for k,v in last_session.items():
                try:
                    session.SesDetails[k] = eval(v)
                except:
                    session.SesDetails[k] = v
            
            print('Loaded ongoing session.')
            return session
        
    except FileNotFoundError:
        print("No ongoing sessions found.")
            
            