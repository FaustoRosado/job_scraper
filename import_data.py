from app import db, JobTable
from bs4 import BeautifulSoup
import requests


#   Creating empty lists with variables

job_title = []
job_link = []
job_company = []
job_salary = []
job_description = []

jobs_list = [job_title, job_link, job_company, job_salary, job_description]

#   Defining scraping function, getting first 450 jobs across pages using query params
#   starting at start=0 for first 15 jobs, start=10 for next 15, and so on through 
#   start=290 for jobs across 30 pages 

def indeed_scraping(url, query_number):
    jobs_query = url + str(query_number)
    #print(jobs_query)
    if query_number <= 290:
        query_number += 10
        #print(query_number)
        indeed_scraping(url, query_number)
        
        

    response = requests.get(str(jobs_query))
    #print(response)
    soup = BeautifulSoup(response.content,"html.parser")
    soup_title = soup.find_all('h2',{"class":"title"})
    soup_company = soup.find_all("span",{"class":"company"})
    soup_salary = soup.find_all("span",{"class":"salaryText"})
    soup_description = soup.find_all("div",{"class":"summary"})

    for x in range(len(soup_title)):
        try:
            job_salary.append(soup_salary[x].text.strip())
        except:
            job_salary.append("No salary given")

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
        
    #indeed_scraping('https://www.indeed.com/jobs?q=Python&l=New+York,+NY&radius=0&start=', 0)    
    
    
def main():
    db.drop_all()
    db.create_all()

    for index, job in enumerate(jobs_list[0]):
        new_row = JobTable(title = job, link = jobs_list[1][index], company = jobs_list[2][index], salary = jobs_list[3][index], description = jobs_list[4][index] )
        #print(new_row)
        db.session.add(new_row)
        db.session.commit()

if __name__ == '__main__':
    indeed_scraping('https://www.indeed.com/jobs?q=Python&l=New+York,+NY&radius=0&start=', 0)
    main()
    #print(jobs_list)




    




    
