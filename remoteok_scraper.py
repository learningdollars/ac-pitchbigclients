from selenium import webdriver
from bs4 import BeautifulSoup
from time import strftime
import datetime
import csv 
import re
import os

from ld_skills import get_all_skills
from ld_skill_link import get_link
from ld_skills import modify

def remoteok_setup():
  # PATH = "./chromedriver" 
  options = webdriver.ChromeOptions()
  options.add_argument("--start-maximized")

  # driver = webdriver.Chrome(PATH, chrome_options=options) # anisha version
  driver = webdriver.Chrome(chrome_options=options) # gobi version

  mainurl= "https://remoteok.io/remote-dev-jobs"
  driver.get(mainurl)  

  all_jobs = [x.get_attribute('data-url') for x in driver.find_elements_by_tag_name('tr')]
  job_links = []

  for data in all_jobs:
    if data != None:
      job_links.append(data)
  
  scraper(job_links, driver)

def scraper(jobs, driver):

  # Get all LD skills to compare and extract skills from the job description
  ld_skills = get_all_skills(driver)

  today = datetime.datetime.now()
  filename = 'remoteok_jobs_' + str(today.day) + '_' + strftime("%b") + '_' + str(today.year) + '_' + str(today.hour) + '_' + str(today.minute) + '.csv'

  # with open(os.path.dirname(os.path.abspath('remoteok_jobs')) + '/remoteok_jobs/' + filename, 'w', encoding='UTF-16', newline='') as file: # anisha version 
  with open(os.path.dirname(os.path.abspath('remoteok_jobs')) + '/remoteok_jobs/' + filename, 'w', newline='') as csvfile: # gobi version 
    writer = csv.writer(csvfile)
    writer.writerow(['posted_date', 'skills', 'job_name', 'company_name', 'description', 'ld_link'])            
    
    for link in jobs:
      driver.get('https://remoteok.io' + link)
      all_rows = driver.find_elements_by_tag_name("tr")
      for row in all_rows:
         if "job-" in row.get_attribute('id'):
           container = row
           break
      job = BeautifulSoup(container.get_attribute("innerHTML"), 'html.parser')
      
      # Extracting the required data    
      job_detail    = job.find(class_ ="company position company_and_position")
      company_name  = job_detail.find("h3").text
      job_name      = job_detail.find("h2").text
      tags          = job.find(class_ = "tags").find_all(class_=re.compile("^tag"))
      description   = driver.find_element_by_class_name('description').text
      posted_date   = job.find("time")['datetime']            
      posted_date   = datetime.datetime.strptime(''.join(posted_date.rsplit(':', 1)), '%Y-%m-%dT%H:%M:%S%z')
      
      # Extract skills from tags
      skills = []
      for tag in tags:
        tagname = str(tag.find('h3').text).title()
        skills.append(tagname)
      
      # Extract skills from description and append in skills list
      desc = modify(description)
      for skill in ld_skills:
        modified = modify(skill).lower()
        if modified in desc.lower():
          skills.append(skill)

      ld_link = get_link(skills, driver)
      writer.writerow([posted_date, skills, job_name, company_name, description, ld_link])
      print('New job record added: ', job_name)

    print('\nSuccessfully created a new csv file for remoteok.io jobs - ' + filename + '.')  
