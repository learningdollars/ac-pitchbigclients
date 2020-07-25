def get_all_skills(driver):
  URL = "https://www.learningdollars.com/client/select_engineers/"
  driver.get(URL)

  category_list = driver.find_elements_by_xpath('/html/body/div[2]/div[3]/div[2]/form/div[1]/div[1]/div/select/option')
  category_list[0].click()

  # To get all skills from ld talent
  skills = driver.find_elements_by_xpath('/html/body/div[2]/div[3]/div[2]/form/div[1]/div[2]/div/select/option')
  all_skills = []
  for skill in skills:
    modified = modify(skill.text)
    all_skills.append(modified)

  return sorted(all_skills)

# To modify all skills into same form
def modify(skill):
  if '.' in skill:
    skill = skill.replace('.', '')
  if ' ' in skill:
    skill = skill.replace(' ', '')
  if ',' in skill:
    skill = skill.replace(',', '')
  return skill.lower() 