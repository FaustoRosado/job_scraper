
from bs4 import BeautifulSoup
import requests
import pandas as pd
from pandas import DataFrame
import csv

# url = 'https://www.indeed.com/jobs?q=Python&l=New+York,+NY&radius=0&start='
# response = requests.get(url)
# print(response)
# soup = BeautifulSoup(response.content, "html.parser")
# soup_title = soup.findAll('h2',{"class":"title"})
# print(len(soup_title))

#for x in range(15):
#    print('https://www.indeed.com' + soup_title[x].a['href'])
#for x in range(15):
#    print(soup_title[x].a['title'])

# soup_company = soup.findAll("span",{"class":"company"})

# for x in range(15):
#     print((soup_company[x].text.strip()))

# soup_salary = soup.findAll("span",{"class":"salaryText"})
# for x in range(15):
#     try:
#         print((soup_salary[x].text.strip()))
#     except:
#         print("Empty Salary")

# soup_description = soup.findAll("div",{"class":"summary"})

# for x in range(15):
#     for _div in soup_description:
#         ul = _div.find_all("ul")
#         for _ul in ul:
#             li = _ul.find_all("li")
#             for _li in li:
#                 print(_li.text)



"""

Command to create a structure of csv file to populate scrapped data

"""



with open('python-jobs-from-indeed.csv', mode='w') as csv_file:
    fieldnames = ['Title', 'Link', 'Company', 'Salary', 'Description']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

#   Creating empty lists with variables

jobs_list = []

job_title = []
job_link = []
job_company = []
job_salary = []
job_description = []

#   Defining scraping function

def indeed_scraping(url, query_number=0):
    #jobs_query = url + str(query_number)
    if query_number < 300 & query_number % 10 == 0:
        query_number = query_number + 10
    jobs_query = url + str(query_number)
    #indeed_scraping(url, query_number) 

    response = requests.get(str(jobs_query))
    #print(response)
    soup = BeautifulSoup(response.content,"html.parser")
    soup_title = soup.findAll('h2',{"class":"title"})
    soup_company = soup.findAll("span",{"class":"company"})
    soup_salary = soup.findAll("span",{"class":"salaryText"})
    soup_description = soup.findAll("div",{"class":"summary"})

    for x in range(len(soup_title)):
        try:
            job_salary.append(soup_salary[x].text.strip())
        except:
            job_salary.append("Empty Salary")

    for x in range(len(soup_title)):
        for _div in soup_description:
            ul = _div.find_all("ul")
            for _ul in ul:
                li = _ul.find_all("li")
                for _li in li:
                    job_description.append(_li.text)
    
    
    for x in range(len(soup_title)):
        job_title.append(soup_title[x].a['title'])
        job_link.append('https://www.indeed.com' + soup_title[x].a['href'])
        job_company.append(soup_company[x].text.strip())
        
        
    
    
"""   
    Generating next set of jobs, in place of pagination, start=0 - first page, start=10, second page,
    for increase 
"""
    # if query_number < 300:
    #     query_number = query_number + 10
    #     indeed_scraping(url, query_number)


#data_list = [job_title, job_link, job_company, job_salary, job_description]

#jobs_list.append(data_list)
    

#   Calling the function with relevant query numbers beginning with 0

indeed_scraping('https://www.indeed.com/jobs?q=Python&l=New+York,+NY&radius=0&start=', 0)



# def make_csv():
#     with open('indeed-python-jobs.csv', 'w') as filename:
    
#         file = csv.writer(filename)
#         file.writerow(['Title', 'Link', 'Company', 'Salary', 'Description'])
#         for info in jobs_list:
#             file.writerow(info)

#   Creating the data frame and populating its data into csv file

data = { 'Job Title': job_title, 'Job Link': job_link, 'Job Company': job_company, \
         'Job Salary': job_salary, 'Job Description': job_description}

df = pd.DataFrame.from_dict(data, orient='index') 
#columns =
#['Job Title','Job Link','Job Company','Job Salary','Job Description'])
df.transpose()
df.to_csv('python-jobs-from-indeed.csv', index=False, header = True, encoding='utf-8')
    
#if __name__ == '__main__':
    #indeed_scraping('https://www.indeed.com/jobs?q=Python&l=New+York,+NY&radius=0&start=', 0)
    #make_csv()

        
#print(df)



    
