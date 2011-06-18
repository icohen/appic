# Tools for scraping [appic.org](http://www.appic.org) for my wife

Scrapes the first page of some [appic search results](http://www.appic.org/directory/search_results.asp?search_type=characteristics&appicProgramType=1&search_country_state_province=ME&search_country_state_province=MA&search_country_state_province=NH&appicMetroAreas=3&us_citizenship=0&canadian_citizenship=no&apa_accredited=yes&cpa_accredited=both&appicAgencyTypes=10&appicAgencyTypes=7&appicAgencyTypes=2&appicAgencyTypes=8&appicAgencyTypes=5&appicAgencyTypes=11&appicAgencyTypes=14&appicAgencyTypes=12&appicAgencyTypes=4&appicAgencyTypes=15&appicAgencyTypes=6&appicAgencyTypes=9&appicApplicantTypes=1&appicApplicantTypes=8&full_part_time=full&training_any_all=INTERSECTION) and downloads details from each [program page](http://www.appic.org/directory/program_cache/252.html) into [out.csv](https://raw.github.com/icohen/appic/master/out.csv) which can be opened with excel.  

## Setup
### install virtualenv + virtualenvwrapper
	curl -s https://raw.github.com/brainsik/virtualenv-burrito/master/virtualenv-burrito.sh | bash
### make and configure a virtualenv 	
	mkvirtualenv appic --no-site-packages
	workon appic
	pip install -r path/to/appic/requirements.txt

## Usage
    cd path/to/appic
  
  create out.csv in the same directory with details of programs which match search_url in scrape.py
  
    python scrape.py 

  same as above with results limited to first 5 programs
    
    python scrape.py 5
  

# Todo
- scrapes more than the first page of results
- scrape the remainder of each program page
  - *Training Opportunities* and below
