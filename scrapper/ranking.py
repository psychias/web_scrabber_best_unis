import json, csv
import pandas as pd
import sqlite3
dict_json = []
def get_entries():
    import requests

    url = "https://www.topuniversities.com/sites/default/files/qs-rankings-data/en/3816281.txt?rl4j4t"

    headers = {
        "user-agent": "Mozilla/5.0",
        "x-requested-with": "XMLHttpRequest"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    def make_pretty(entry):
        from bs4 import BeautifulSoup as Soup
        return {
            "name": Soup(entry["title"], "html.parser").select_one(".uni-link").get_text(strip=True),
            "rank": entry["rank_display"],
            "reputation": entry["score"]
        }

    yield from map(make_pretty, response.json()["data"])

def main():

    from itertools import islice
   # the json file where the output must be stored 
    out_file = open("rankings.json", "w") 

   

    for entry in islice(get_entries(), 30):
        
        jtopy=json.dumps(entry) #json.dumps take a dictionary as input and returns a string as output.
        dict_json.append(json.loads(jtopy)) # json.loads take a string as input and returns a dictionary as output.
    json.dump(dict_json, out_file, indent = 6)
    out_file.close()


    def read_json(filename):
        return json.loads(open(filename).read())
    def write_csv(data,filename):
        with open(filename, 'w+') as outf:
            writer = csv.DictWriter(outf, data[0].keys())
            writer.writeheader()
            for row in data:
                writer.writerow(row)

    write_csv(read_json('rankings.json'), 'rankings.csv')


    #Insert dataset to database
    df = pd.read_csv('rankings.csv', encoding = "ISO-8859-1")
    table_name = 'Ranking'
    conn = sqlite3.connect('twitter.sqlite')
    query = f'Create table if not Exists {table_name} (Name text, Rank real, Reputation float)'
    conn.execute(query)
    df.to_sql(table_name,conn,if_exists='replace',index=False)
    conn.commit()
    conn.close()

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())