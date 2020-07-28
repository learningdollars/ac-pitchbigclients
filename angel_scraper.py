from selenium import webdriver
from bs4 import BeautifulSoup
from time import strftime
import datetime
import time
import csv
import os

from ld_skill_link import get_link

def angel_setup():
  PATH = "./chromedriver" 
  options = webdriver.ChromeOptions()
  options.add_argument("--start-maximized")

  URL = "https://angel.co/jobs"
  # driver = webdriver.Chrome(PATH, chrome_options=options) # anisha version
  driver = webdriver.Chrome(chrome_options=options) # gobi version
  driver.get(URL)

  driver.find_element_by_link_text('Log In').click()
  try:
    login(driver)
    time.sleep(60)
  except:
    time.sleep(60)
    login(driver)

  time.sleep(10)
  auto_scroll(driver)

  main_page = driver.find_element_by_class_name('content_1ca23')
  all_jobs  = main_page.find_elements_by_class_name('component_4d072')
  job_links = []
  for job in all_jobs:
    link = job.find_element_by_class_name('component_07bb9').find_element_by_tag_name('a').get_attribute('href')
    job_links.append(link)
  
  scraper(job_links, driver)
  driver.close()

def login(driver):
  #driver.find_element_by_id('user_email').send_keys('your_email')
  #driver.find_element_by_id('user_password').send_keys('your_password')
  driver.find_element_by_css_selector("input[name='commit']").click()

def auto_scroll(driver):
  # Get current scroll height
  last_height = driver.execute_script("return document.body.scrollHeight")
  while True:
    # To scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # To wait till page loads after scrolling
    time.sleep(1)
    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
      break
    last_height = new_height

def scraper(job_links, driver):

  today = datetime.datetime.now()
  filename = 'angel_co_jobs_' + str(today.day) + '_' + strftime("%b") + '_' + str(today.year) + '_' + str(today.hour) + '_' + str(today.minute) + '.csv'

  #with open(os.path.dirname(os.path.abspath('angel_co_jobs')) + '/angel_co_jobs/' + filename, 'w', encoding='UTF-16', newline='') as csvfile: # anisha version
  with open(os.path.dirname(os.path.abspath('angel_co_jobs')) + '/angel_co_jobs/' + filename, 'w', newline='') as csvfile: # gobi version
    writer = csv.writer(csvfile)
    writer.writerow(['skills', 'job_name', 'job_type', 'experience', 'company_name', 'industry', 'company_size', 'location', 'hiring_contact', 'website', 'description', 'ld_link'])

    for link  in job_links:
      driver.get(link)
      detail  = driver.find_element_by_class_name('wrapper_06a53')
      result  = detail.get_attribute('innerHTML')
      soup    = BeautifulSoup(result, 'html.parser')
      content = soup.find(class_ = 'content_50e69')

      # Initialization
      about_job = []
      skills    = []
      industry  = []
      job_type  = experience = company_size = location = hiring_contact = website = 'Not mentioned'
      
      # Extracting the required data
      job_name      = content.find("h2", class_ = 'header_ec0af').text
      basics        = content.find("div", class_ = 'component_4105f').find_all("div",class_ = 'characteristic_650ae')
      company_name  = content.find("div", class_ = 'name_af83c').find("h1").text
      about_company = soup.find("div", class_ = 'component_3298f').find_all("dt")
      description   = content.find("div", class_ = 'description_c90c4').text

      # Extract company size
      try:
        for about in about_company:
          extracts = about.text
          if(" people" in extracts):
            company_size = extracts
      except:
        pass
      
      # Extract website link
      try:
        website = soup.find("li", class_ = 'websiteLink_b71b4').find("a").get('href')
      except:
        pass

      # Extract hiring contact
      try:
        hiring         = content.find("div", class_ = 'recruitingContact_82245').find("h4", class_ = 'name_9d036').text
        hiring_post    = content.find("div", class_ = 'recruitingContact_82245').find("span").text
        hiring_contact = hiring + ', ' + hiring_post
      except:
        pass
    
      # Extract industry details
      try:
        industry_info = soup.find("div", class_ = 'component_3298f').find("dt", class_ = 'tags_70e20').find_all("a")
        for info in industry_info:
          industry.append(info.text)
      except:
        pass

      for basic in basics:
        title = basic.find("dt").text
        # Extract skills 
        if (title == 'Skills'):
          all_skill = basic.find_all("a")
          for skill in all_skill:
            one_skill = skill.text
            skills.append(one_skill)
        else:
          desc = basic.find("dd").text
        pair = [title, desc]
        about_job.append(pair)
      
      # Extract basic details about job
      for info in about_job:
        title = info[0]
        desc = info[-1]
        if (title == 'Location'):
          location = desc
        elif (title == 'Job type'):
          job_type = desc
        elif (title == 'Experience'):
          experience = desc
        else:
          continue

      ld_link = get_link(skills, driver)
      writer.writerow([skills, job_name, job_type, experience, company_name, industry, company_size, location, hiring_contact, website, description, ld_link])
      print('New job record added: ', job_name)

    print('\nSuccessfully created a new csv file for angel.co jobs - ' + filename + '.')  
