import requests
from bs4 import BeautifulSoup
import json as js
from flask import *

app = Flask(__name__)

# # @app.get('/')
def get_all_page():
    urls = []
    countrys = ['afrique-du-Sud','algerie','angola','benin-fr','cameroun','congo','ethiopie','guinnee','madagascar','mali','maroc'
     'mauritanie', 'mozambique','niger', 'nigeria','senegal', 'togo', 'tunisie', 'cote-d-ivoire']

    for country in countrys:
        page = f"https://africa-cuisine.com/fr/cuisine/{country}/"
        urls.append(page)

    return urls

@app.route('/', methods=['GET'])
def parse_html():
    r = requests.get('https://africa-cuisine.com/')
    parse = BeautifulSoup(r.content, 'html.parser')
    recipes_tab = {}

    id = 0
    recipes = parse.find_all('div', class_='archive-item-i')
    for recipe in recipes:
        nom = recipe.find('h3', class_='entry-title').a.text.strip()
        link = recipe.find('h3', class_='entry-title').a.attrs['href']

        inset = requests.get(link)
        html = BeautifulSoup(inset.content, 'html.parser')
        thumbails = html.find('div', class_="single-main-media-image-w")['data-lightbox-img-src']

        ingredients = []
        ing = html.find('table', class_='ingredients-table').find_all('tr')
        for i in ing:
            try:
                name = i.find('span', class_='ingredient-amount').text.strip()+' '+i.find('span', class_='ingredient-name').text.strip()
                ingredients.append(name)
            except AttributeError:
                pass

        steps = []
        sp = html.find('table', class_='recipe-steps-table').find_all('td', class_="single-step-description")
        nbr = 1
        for i in sp:
            desc = i.find('p').text.strip()
            try:
                sp_title = i.find('h3', class_='single-step-title').text.strip()
            except:
                sp_title = ''
            steps.append({
                "step_id": nbr,
                "name": sp_title,
                "description": f"{desc}",
            })
            nbr += 1

        data = {
            "title": nom,
            "thumbails": thumbails,
            "ingredients": ingredients,
            "steps": steps,
        }

        recipes_tab[str(id)] = data
        id += 1

    return js.dumps(recipes_tab, indent=4)


if __name__ == '__main__':
    app.run(port=7777)
