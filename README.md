# Tools for scraping [appic.org](http://www.appic.org) for my wife

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
  


