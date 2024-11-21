import requests
from bs4 import BeautifulSoup

def get_article_images(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        article_images = []
        for img in soup.find_all('img'):
            if 'src' in img.attrs:
                img_src = img['src']
                
                if img_src.startswith('//'):
                    img_src = f'https:{img_src}'
                elif img_src.startswith('/'):
                    base_url = f'{url.split("//")[0]}//{url.split("//")[1].split("/")[0]}'
                    img_src = f'{base_url}{img_src}'
                
                article_images.append(img_src)
        
        return article_images if article_images else "Aucune image trouvée pour cet article."

    except requests.exceptions.RequestException as e:
        return f"Erreur lors de la récupération de la page : {e}"
