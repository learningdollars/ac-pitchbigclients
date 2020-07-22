from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import csv

def initial_setup(filename, choice):
  # PATH = "./chromedriver" 
  options = webdriver.ChromeOptions()
  options.add_argument("--start-maximized")

  URL = "https://stackoverflow.com/jobs?id=406879&r=true&j=Contract"
  #driver = webdriver.Chrome(PATH, chrome_options=options)
  driver = webdriver.Chrome(chrome_options=options) # gobi version
  driver.get(URL)

  # Scraping all jobs list
  all_jobs = driver.find_elements_by_class_name('js-result')
  job_links = []

  # To get url of all jobs in the list
  for job in all_jobs:
    data = job.get_attribute('data-preview-url')
    job_links.append(data)
  
  scraper(filename,choice,job_links,driver)
  driver.close()

def scraper(filename, choice, job_links, driver):
  
  if (choice == 1):
    mode = 'w'
  else:
    mode = 'a'
  
  # For writing or updating/appending csv

  #with open(filename, mode , encoding='UTF-32', newline='') as csvfile:
  with open(filename, mode , newline='') as csvfile: # gobi version
    writer = csv.writer(csvfile)
    if mode == 'w':
      writer.writerow(['posted_date', 'technologies', 'job_name', 'company', 'job_type', 'experience_level', 'role', 'industry', 'company_size', 'company_type', 'description'])

    # Scraping
    for link in job_links:
      driver.get('https://stackoverflow.com' + link)
      detail  = driver.find_element_by_id('mainbar')
      result  = detail.get_attribute('innerHTML')
      soup    = BeautifulSoup(result, 'html.parser')
      content = soup.find(class_ = 'nav-content')

      # Initialization
      technologies  = []
      about         = []
      job_type = experience = role = industry = company_size = company_type = 'Not mentioned'

      # Extracting the required data
      tags          = content.find_all("a", class_ = 'post-tag')
      for tag in tags:
        data = tag.text
        technologies.append(data)

      job_name      = soup.find("a", class_ = 'fc-black-900').text
      basics        = content.find(class_ = 'job-details--about').find_all(class_ = 'mb8')
      company       = soup.find("div", class_ = 'fc-black-700').a.text
      description   = content.find(class_ = 'mb32 fs-body2 fc-medium pr48').find("div").text
      actual_date   = content.find(class_ = 'grid fs-body1 fc-black-500 gs8 ai-baseline mb24').text
      actual_date   = actual_date.strip()

      # To change n_days_ago format into date format
      check_date = actual_date.split()
      if '<' in check_date:
        actual_date = actual_date.replace('Posted < ', '')
      else:
        actual_date = actual_date.replace('Posted ', '')
      if (actual_date == 'yesterday'):
        dt = datetime.timedelta(days = 1)
      else:
        parsed_date   = [actual_date.split()[:2]]
        if (parsed_date[0][1] == 'hour'):
          parsed_date[0][1] = 'hours'
        time_dict = dict((index,float(value)) for value,index in parsed_date)
        dt = datetime.timedelta(**time_dict)
      posted_date = datetime.datetime.now() - dt
      posted_date  = posted_date.date()
      
      # To assign values to respective variables from basics list
      for basic in basics:
        data  = basic.text
        data  = data.replace('\n', '')
        data  = data.split(': ')
        final = [ data[0], data[-1] ]
        about.append(final)
      
      for info in about:
        title = info[0]
        desc = info[-1]
        if (title == 'Job type'):
          job_type = desc
        elif (title == 'Experience level'):
          experience = desc
        elif (title == 'Role'):
          role = desc
        elif (title == 'Industry'):
          industry = desc
        elif (title == 'Company size'):
          company_size = desc
        else:
          company_type = desc
      
      writer.writerow([posted_date, technologies, job_name, company, job_type, experience, role, industry, company_size, company_type, description])
      print('New job record added: ', job_name)

    check_duplicate(filename)

    if (mode == 'w'):
      print('\nSuccessfully created new csv file - ' + filename + '.')
    else:
      print('\nSuccessfully updated', filename + '.')

def check_duplicate(filename):
  # df = pd.read_csv(filename, encoding = 'UTF-32')
  df = pd.read_csv(filename) # gobi version
  df['posted_date'] = pd.to_datetime(df.posted_date, infer_datetime_format = True)
  df.sort_values(by = 'posted_date', ascending = False, inplace = True)
  df = df.drop_duplicates(keep='first')
  # df.to_csv(filename,index = False, encoding = 'UTF-32')
  df.to_csv(filename,index = False) # gobi version 
