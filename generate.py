import requests
import csv


peopleprojects_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQnI0XWdTWBvMfVR2MHUaKfIfEPnA-uFinJpsWmy8P2iB0B64ZQlrxMhb_5Fi1ZCqBOlcmJmE7GVglU/pub?gid=2024936308&single=true&output=csv"

people_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQnI0XWdTWBvMfVR2MHUaKfIfEPnA-uFinJpsWmy8P2iB0B64ZQlrxMhb_5Fi1ZCqBOlcmJmE7GVglU/pub?gid=0&single=true&output=csv"

projects_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQnI0XWdTWBvMfVR2MHUaKfIfEPnA-uFinJpsWmy8P2iB0B64ZQlrxMhb_5Fi1ZCqBOlcmJmE7GVglU/pub?gid=480161355&single=true&output=csv"


def read_csv(url):
    r = requests.get(url)
    reader = csv.reader(r.text.split('\n'), delimiter=',')
    for row in reader:
        yield row

# read projects
projectsdata = read_csv(projects_url)
next(projectsdata)  # skip header
projects = {}
for project in projectsdata:
    id, name, website, description, twitter, linkedin, github = project
    projects[id] = {
        "id": id,
        "name": name,
        "website": website,
        "description": description,
        "twitter": twitter,
        "linkedin": linkedin,
        "github": github,
        "people": []
    }

# read people
peopledata = read_csv(people_url)
next(peopledata)
people = {}
for person in peopledata:
    id, name, website, twitter, linkedin, github = person
    people[id] = {
        "id": id,
        "name": name,
        "website": website,
        "twitter": twitter,
        "linkedin": linkedin,
        "github": github,
        "projects": []
    }


# append projects to people and people to projects
# assume every project has a website, but that people might have a) a website, or b) a twitter or c) a linkedin, d) github
peopleprojectsdata = read_csv(peopleprojects_url)
next(peopleprojectsdata)
for pp in peopleprojectsdata:
    person_id, project_id = pp
    person_link = ''
    for attempt in ['website', 'twitter', 'linkedin', 'github']:
        person_link = people[person_id][attempt]
        if person_link:
            break
        
    people[person_id]['projects'].append((projects[project_id]['name'], projects[project_id]['website']))
    projects[project_id]['people'].append((people[person_id]['name'], person_link))

# generate people HTML
print("<h2>People</h2>")
for p in people:
    person = people[p]
    pprojects = person['projects']
    
    htmlprojects = ' &middot; '.join([f"""<a href="{p[1]}">{p[0]}</a>""" for p in pprojects])
    print(f"<h3>{person['name']}</h3>")
    print("<ul>")
    print(f"""<li><b>Website: </b> <a href="{person['website']}">{person['website']}</a></li>""")
    print(f"""<li><b>Twitter: </b> <a href="{person['twitter']}">{person['twitter']}</a></li>""")
    print(f"""<li><b>LinkedIn: </b> <a href="{person['linkedin']}">{person['linkedin']}</a></li>""")
    print(f"""<li><b>GitHub: </b> <a href="{person['github']}">{person['github']}</a></li>""")
    print(f"""<li><b>Projects: </b> {htmlprojects}</li>""")
    print("</ul>")



# generate projects HTML
print("<h2>Projects</h2>")
for p in projects:
    project = projects[p]
    ppeople = project['people']
    
    htmlpeople= ' &middot; '.join([f"""<a href="{p[1]}">{p[0]}</a>""" for p in ppeople])
    print(f"<h3>{project['name']}</h3>")
    print("<ul>")
    print(f"""<li><b>Website: </b> <a href="{project['website']}">{project['website']}</a></li>""")
    print(f"""<li><b>Twitter: </b> <a href="{project['twitter']}">{project['twitter']}</a></li>""")
    print(f"""<li><b>LinkedIn: </b> <a href="{project['linkedin']}">{project['linkedin']}</a></li>""")
    print(f"""<li><b>GitHub: </b> <a href="{project['github']}">{project['github']}</a></li>""")
    print(f"""<li><b>People: </b> {htmlpeople}</li>""")
    print("</ul>")


print("</body>")
print("</html>")

