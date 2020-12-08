
from app import db, Jobs
from bs4 import BeautifulSoup
import requests
import csv

"""                     -Testing before creating functions-

url = 'https://www.indeed.com/jobs?q=Python&l=New+York,+NY&radius=0&start='
response = requests.get(url)
print(response)
soup = BeautifulSoup(response.content, "html.parser")
soup_title = soup.findAll('h2',{"class":"title"})
print(len(soup_title))

for x in range(15):
   print('https://www.indeed.com' + soup_title[x].a['href'])
for x in range(15):
   print(soup_title[x].a['title'])

soup_company = soup.findAll("span",{"class":"company"})

for x in range(15):
    print((soup_company[x].text.strip()))

soup_salary = soup.findAll("span",{"class":"salaryText"})
for x in range(15):
    try:
        print((soup_salary[x].text.strip()))
    except:
        print("Empty Salary")

soup_description = soup.findAll("div",{"class":"summary"})

for x in range(15):
    for _div in soup_description:
        ul = _div.find_all("ul")
        for _ul in ul:
            li = _ul.find_all("li")
            for _li in li:
                print(_li.text)
"""

#   Creating empty lists with variables

job_title = []
job_link = []
job_company = []
job_salary = []
job_description = []

jobs_list = [job_title, job_link, job_company, job_salary, job_description]

#   Defining scraping function, getting first 300 jobs across pages using queries
#   starting at start=0 for first 15 jobs, start=10 for next 15, and so on through 
#   start=290 for total of 450 jobs 

def indeed_scraping(url, query_number=0):
    jobs_query = url + str(query_number)
    #print(jobs_query)
    if query_number <= 290:
        query_number = query_number + 10
        #print(query_number)
        indeed_scraping(url, query_number)

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

    #for x in range(len(soup_title)):
        for _div in soup_description:
            ul = _div.find_all("ul")
            for _ul in ul:
                li = _ul.find_all("li")
                for _li in li:
                    job_description.append(_li.text)
    
    
    #for x in range(len(soup_title)):
        job_title.append(soup_title[x].a['title'])
        job_link.append('https://www.indeed.com' + soup_title[x].a['href'])
        job_company.append(soup_company[x].text.strip())
        
        
    
    
def make_csv():
    with open('indeed-python-jobs.csv', 'w') as filename:
    
        file = csv.writer(filename)
        #file.writerow(['Title', 'Link', 'Company', 'Salary', 'Description'])
        for info in jobs_list:
            file.writerow(info)
    
if __name__ == '__main__':
    indeed_scraping('https://www.indeed.com/jobs?q=Python&l=New+York,+NY&radius=0&start=', 0)
    make_csv()

        




    
