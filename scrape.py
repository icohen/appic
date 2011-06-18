# -*- coding: utf-8 -*-
import codecs
import cStringIO
import re
from urllib2 import urlopen
from urlparse import urljoin
import csv
import sys



class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)



from django.utils.html import strip_tags
from django.utils.encoding import smart_str

from BeautifulSoup import BeautifulSoup

def remove_extra_whitespace(s):
    whitespace = re.compile(r'\s+')
    return re.sub(whitespace, ' ', s)

def table_tag_to_string(tag):
    result = ''
    colHeads = tag.findAll(attrs={'class':'colHead'})
    rowHeads = tag.findAll(attrs={'class':'rowHead'})
    dataCells = tag.findAll(attrs={'class':'dataCell'})
    col_names = map(contents_to_string, colHeads)
    row_names = map(contents_to_string, rowHeads)    
    data_cells = map(contents_to_string, dataCells)
    # print 'cols', col_names
    # print 'rows', row_names
    # print 'data', data_cells
    
    data_prefix_template = '{row_name} {col_name}'
    for i, data in enumerate(data_cells):
        if not data:
            continue
        col_name = col_names[i % len(col_names)]
        row_name = row_names[i / len(row_names)]
        data_prefix = data_prefix_template.format(**locals())
        result += '{data_prefix}: {data} '.format(**locals())
    return result
    

def contents_to_string(tag):
    replace_ents = {'&nbsp;':' ',
                    u'\xef':'',
                    u'\xbf':'',
                    u'\xbd':'',
                    u'<br />':', ',
                    }
    s = str(tag)
    if 'colHead' in s and 'rowHead' in s:
        s = table_tag_to_string(tag)
    for ent in replace_ents:
        v = replace_ents[ent]
        if not v:
            v = ent.encode('ascii', 'replace')
        s = s.replace(ent, v)
    s = strip_tags(s)
    s = remove_extra_whitespace(s)
    s = s.strip(': ')
    return s
    

try:
    limit = int(sys.argv[1])
except:
    limit = None
search_url = "http://www.appic.org/directory/search_results.asp?search_type=characteristics&appicProgramType=1&search_country_state_province=ME&search_country_state_province=MA&search_country_state_province=NH&appicMetroAreas=3&us_citizenship=0&canadian_citizenship=no&apa_accredited=yes&cpa_accredited=both&appicAgencyTypes=10&appicAgencyTypes=7&appicAgencyTypes=2&appicAgencyTypes=8&appicAgencyTypes=5&appicAgencyTypes=11&appicAgencyTypes=14&appicAgencyTypes=12&appicAgencyTypes=4&appicAgencyTypes=15&appicAgencyTypes=6&appicAgencyTypes=9&appicApplicantTypes=1&appicApplicantTypes=8&full_part_time=full&training_any_all=INTERSECTION"

search_html = urlopen(search_url).read()

search_soup = BeautifulSoup(search_html)

writer = UnicodeWriter(open("out.csv", "wb"))
first = True
for program_link in search_soup.findAll("a",{'class':'smallBold'})[:limit]:
    inserted_keys = [] # [(index, key), (index, key)]
    same_training_lead=False
    program_title = program_link.string
    program_url = urljoin(search_url, program_link['href'])
    program_html = urlopen(program_url).read()
    program_soup = BeautifulSoup(program_html)
    key_tds = program_soup.findAll('td', {'class':'searchFieldLabel'})
    value_tds = [key_td.findNextSibling() for key_td in key_tds]
    keys = map(contents_to_string, key_tds)
    for i, key in enumerate(keys):
        if 'Training Director & Lead/Director/Chief Psychologist' in key:

            keys.insert(i, 'Lead/Director/Chief Psychologist')
            keys.insert(i, 'Training Director')
            keys.remove(key)
            same_training_lead=i+1
    #value_tds = program_soup.findAll('td', {'class':'small'})
    values = map(contents_to_string, value_tds)
    if same_training_lead:
        values.insert(same_training_lead, values[same_training_lead-1])
    if first:
        writer.writerow(keys)
        first = False
    writer.writerow(values)
    
