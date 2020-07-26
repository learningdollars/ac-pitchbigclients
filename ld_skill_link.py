import time

from ld_skills import modify

def get_link(skill_list, driver):
  skill_list = [modify(skill).lower() for skill in skill_list]

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
      if modified.lower() in skill_list:
        skill.click()
        move_right_button.click()

    # To get shareable link
    find_engineers.click()
    time.sleep(2)
    get_link_button = driver.find_element_by_xpath('//*[@id="shareable_link_btn"]')
    get_link_button.click()
    time.sleep(2)
    link = driver.find_element_by_xpath('//*[@id="shareable_link_text"]').text
    return link
  except:
    return 'Not Found'