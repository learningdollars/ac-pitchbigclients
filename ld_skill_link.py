import time
from selenium import webdriver

def get_link(skill_list, driver):
  skill_list = [modify(skill) for skill in skill_list]

  URL = 'https://www.learningdollars.com/client/select_engineers/'
  driver.get(URL)  

  # To select 'ALL' option from category list to get all skills
  category_list = driver.find_elements_by_xpath('/html/body/div[2]/div[3]/div[2]/form/div[1]/div[1]/div/select/option')
  category_list[0].click()    

  # Extracting necessary buttons
  move_right_button = driver.find_element_by_xpath('//*[@id="move-right"]')
  find_engineers = driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[2]/form/button[1]')

  # To get all skills from ld talent and only select those skills provided by particular company
  skills = driver.find_elements_by_xpath('/html/body/div[2]/div[3]/div[2]/form/div[1]/div[2]/div/select/option')
  try:
    for skill in skills:
      modified = modify(skill.text)
      if modified in skill_list:
        skill.click()
        move_right_button.click()

    # To get shareable link
    find_engineers.click()
    get_link_button = driver.find_element_by_xpath('//*[@id="shareable_link_btn"]')
    get_link_button.click()
    time.sleep(5)
    link = driver.find_element_by_xpath('//*[@id="shareable_link_text"]').text
    time.sleep(2)
    return link
  except:
    return 'Not Found'

# To modify all skills into same form
def modify(skill):
  if '.' in skill:
    skill = skill.replace('.', '')
  if ' ' in skill:
    skill = skill.replace(' ', '')
  return skill.lower() 