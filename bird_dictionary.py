import csv
import requests

"""
SCIENTIFIC_NAME, 0
COMMON_NAME, 1
SPECIES_CODE, 2
CATEGORY, 3
TAXON_ORDER, 4
COM_NAME_CODES, 5
SCI_NAME_CODES, 6
BANDING_CODES, 7
ORDER, 8
FAMILY_COM_NAME, 9
FAMILY_SCI_NAME, 10
REPORT_AS,
EXTINCT,
EXTINCT_YEAR
"""

class Bird():
    def __init__(self,scientific_name,common_name,code):
        self.scientific_name=scientific_name
        self.common_name=common_name
        self.code=code
    def url(self):
        return f"https://ebird.org/species/{self.code}"
    
    def __str__(self):
        return self.code

class Bird_bot(Bird):
    def __init__(self,**kwargs):
        self.__dict__.update(kwargs)
    def get_audio(self):
        return self.get_media('https://cdn.download.ams.birds.cornell.edu/api/v1/asset/'+str(self.audio))
    def get_image(self):
        return self.get_media(self.image)
    def get_media(self,url):
        r=requests.get(url)
        return r.content
    
def fill_birds(cont):
    birds = []
    file_name=f"./csv/ebird_{cont}.csv"
    with open(file_name,mode='r') as f:
        reader = csv.reader(f)
        for rows in reader:
            if(rows[12]!='true'):
                birds.append(Bird(rows[0],rows[1],rows[2]))
    return birds
