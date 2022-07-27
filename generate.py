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
    id, name, website, twitter, linkedin, github, imgurl = person
    people[id] = {
        "id": id,
        "name": name,
        "website": website,
        "twitter": twitter,
        "linkedin": linkedin,
        "github": github,
        "imgurl": imgurl,
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
print('<div id="person-list">')
print('<input class="search" placeholder="Search people and projects" />')
print("<h3>People</h3>")
print('<ul class="list">')

for p in people:
    person = people[p]
    pprojects = person['projects']
    imgurl = person['imgurl']
    
    htmlprojects = ' &middot; '.join([f"""<a href="{p[1]}">{p[0]}</a>""" for p in pprojects])
    print("<li class='card card-person'>")
    print(f"<div class='photo'><img src='{imgurl}'  /></div>")
    print(f"""<h4 class="name"><span class='first'>{person['name'].split(' ', 1)[0]}</span> <span class='last'>{person['name'].split(' ', 1)[1]}</span></h4>""")
    print("<ul>")
    if person['website']:
        print(f"""<li><a href="{person['website']}"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="#00afe1" d="M6.188 8.719c.439-.439.926-.801 1.444-1.087 2.887-1.591 6.589-.745 8.445 2.069l-2.246 2.245c-.644-1.469-2.243-2.305-3.834-1.949-.599.134-1.168.433-1.633.898l-4.304 4.306c-1.307 1.307-1.307 3.433 0 4.74 1.307 1.307 3.433 1.307 4.74 0l1.327-1.327c1.207.479 2.501.67 3.779.575l-2.929 2.929c-2.511 2.511-6.582 2.511-9.093 0s-2.511-6.582 0-9.093l4.304-4.306zm6.836-6.836l-2.929 2.929c1.277-.096 2.572.096 3.779.574l1.326-1.326c1.307-1.307 3.433-1.307 4.74 0 1.307 1.307 1.307 3.433 0 4.74l-4.305 4.305c-1.311 1.311-3.44 1.3-4.74 0-.303-.303-.564-.68-.727-1.051l-2.246 2.245c.236.358.481.667.796.982.812.812 1.846 1.417 3.036 1.704 1.542.371 3.194.166 4.613-.617.518-.286 1.005-.648 1.444-1.087l4.304-4.305c2.512-2.511 2.512-6.582.001-9.093-2.511-2.51-6.581-2.51-9.092 0z"/></svg></a></li>""")
    if person['twitter']:
        print(f"""<li><a href="{person['twitter']}"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="#1da1f2" d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z"/></svg></a></li>""")
    if person['linkedin']:
        print(f"""<li><a href="{person['linkedin']}"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="#0077b5" d="M4.98 3.5c0 1.381-1.11 2.5-2.48 2.5s-2.48-1.119-2.48-2.5c0-1.38 1.11-2.5 2.48-2.5s2.48 1.12 2.48 2.5zm.02 4.5h-5v16h5v-16zm7.982 0h-4.968v16h4.969v-8.399c0-4.67 6.029-5.052 6.029 0v8.399h4.988v-10.131c0-7.88-8.922-7.593-11.018-3.714v-2.155z"/></svg></a></li>""")
    if person['github']:
        print(f"""<li><a href="{person['github']}"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="#333" d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg></a></li>""")
    print("</ul>")
    if pprojects:
        print(f"""<div class="card-list"><b>Projects: </b> {htmlprojects}</div>""")
    print("</li>")

print("</ul><!-- /list -->")


print("<h3>Projects</h3>")
print('<ul class="list">')
# generate projects HTML
for p in projects:
    project = projects[p]
    ppeople = project['people']
    
    htmlpeople= ' &middot; '.join([f"""<a href="{p[1]}">{p[0]}</a>""" for p in ppeople])
    print("<li class='card card-project'>")
    print(f"""<h4 class="name">{project['name']}</h4>""")
    print(f"""<p class="description">{project['description']}</p>""")
    print("<ul>")
    if project['website']:
        print(f"""<li><a href="{project['website']}"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="#00afe1" d="M6.188 8.719c.439-.439.926-.801 1.444-1.087 2.887-1.591 6.589-.745 8.445 2.069l-2.246 2.245c-.644-1.469-2.243-2.305-3.834-1.949-.599.134-1.168.433-1.633.898l-4.304 4.306c-1.307 1.307-1.307 3.433 0 4.74 1.307 1.307 3.433 1.307 4.74 0l1.327-1.327c1.207.479 2.501.67 3.779.575l-2.929 2.929c-2.511 2.511-6.582 2.511-9.093 0s-2.511-6.582 0-9.093l4.304-4.306zm6.836-6.836l-2.929 2.929c1.277-.096 2.572.096 3.779.574l1.326-1.326c1.307-1.307 3.433-1.307 4.74 0 1.307 1.307 1.307 3.433 0 4.74l-4.305 4.305c-1.311 1.311-3.44 1.3-4.74 0-.303-.303-.564-.68-.727-1.051l-2.246 2.245c.236.358.481.667.796.982.812.812 1.846 1.417 3.036 1.704 1.542.371 3.194.166 4.613-.617.518-.286 1.005-.648 1.444-1.087l4.304-4.305c2.512-2.511 2.512-6.582.001-9.093-2.511-2.51-6.581-2.51-9.092 0z"/></svg></a></li>""")
    if project['twitter']:
        print(f"""<li><a href="{project['twitter']}"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="#1da1f2" d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z"/></svg></a></li>""")
    if project['linkedin']:
        print(f"""<li><a href="{project['linkedin']}"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="#0077b5" d="M4.98 3.5c0 1.381-1.11 2.5-2.48 2.5s-2.48-1.119-2.48-2.5c0-1.38 1.11-2.5 2.48-2.5s2.48 1.12 2.48 2.5zm.02 4.5h-5v16h5v-16zm7.982 0h-4.968v16h4.969v-8.399c0-4.67 6.029-5.052 6.029 0v8.399h4.988v-10.131c0-7.88-8.922-7.593-11.018-3.714v-2.155z"/></svg></a></li>""")
    if project['github']:
        print(f"""<li><a href="{project['github']}"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="#333" d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg></a></li>""")
    print("</ul>")
    print(f"""<div class="card-list"><b>People: </b> {htmlpeople}</div>""")
    print("</li>")

print("</ul><!-- /list -->")
print("</div>")

print("<footer class='text-center text-white text-opacity-40'>Made pretty by <a href='https://twitter.com/iaremarkus' rel='noopener noreferrer' target='_blank' class='hover:underline hover:text-white transition'>Markus</a></footer>")
print("</body>")
print("</html>")

