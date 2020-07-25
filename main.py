from angel_scraper import angel_setup
from indeed_scraper import indeed_setup
from stackoverflow_main import stackoverflow_main
from weworkremotely_scraper import weworkremotely_setup

def main():
  print('Choose a website to scrape job records from: ')
  print('1. Angel')
  print('2. Indeed')
  print('3. Stackoverflow')
  print('4. Weworkremotely')
  print('Press c to cancel. \n')

  while True:
    try:
      user_input = input("Enter your choice: ")
      if (user_input.isdigit()):
        choice = int(user_input)
      else:
        choice = user_input.lower()
      if (choice != 'c') and (choice > 4):
        print('Invalid choice. Please enter a valid choice. \n')
      else:
        break
    except:
      print('Invalid choice. Please enter a valid choice. \n')

  if (choice == 1):
    angel_setup()   
  elif (choice == 2):
    indeed_setup()
  elif (choice == 3):
    stackoverflow_main()
  elif (choice == 4):
    weworkremotely_setup()


if __name__ == "__main__":
  main()