from stackoverflow_scraper import stackoverflow_setup
from time import strftime
import datetime
import glob
import os

def stackoverflow_main():
  print('Enter 1 to create a new csv file.')
  print('Enter 2 to work in an existing csv file.')
  print('Press c to cancel. \n')

  while True:
    try:
      user_input = input("Enter your choice: ")
      if (user_input.isdigit()):
        choice = int(user_input)
      else:
        choice = user_input.lower()
      if (choice != 1) and (choice != 2) and (choice != 'c'):
        print('Invalid choice. Please enter a valid choice. \n')
      else:
        break
    except:
      print('Invalid choice. Please enter a valid choice. \n')
  
  if (choice == 1):
    today = datetime.datetime.now()
    filename = 'stackoverflow_jobs_' + str(today.day) + '_' + strftime("%b") + '_' + str(today.year) + '_' + str(today.hour) + '_' + str(today.minute) + '.csv'
    stackoverflow_setup(filename, choice)
  
  elif (choice == 2):
    csv_files = list(glob.glob(os.path.dirname(os.path.abspath('stackoverflow_jobs')) + '/stackoverflow_jobs/' + "*.csv"))
    if (len(csv_files) > 0):
      count = 1
      print('\nChoose a csv file from the options: ')
      for csv in csv_files:
        print(str(count) + '. ' + os.path.basename(csv))
        count += 1
      print('Press c to cancel. \n')
      while True:
        try:
          file_choice = input("Enter your file choice: ")
          if (file_choice.isdigit()):
            file_choice = int(file_choice)
            if (file_choice < 1) or (file_choice > count-1):
              print('Invalid choice. Please enter a valid choice. \n')
            else:
              break
          else:
            file_choice = file_choice.lower()
            if (file_choice != 'c'):
              print('Invalid choice. Please enter a valid choice. \n')
            else:
              break
        except:
          print('Invalid choice. Please enter a valid choice. \n')
      if (file_choice != 'c'):
        filename = os.path.basename(csv_files[file_choice-1])
        stackoverflow_setup(filename, choice)
      else:
        print('Cancelled.')
    else:
      print('No csv file found.')

  else:
    print('Cancelled.')
