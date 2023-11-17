import asyncio
from textwrap import shorten
import requests
from bs4 import BeautifulSoup
import numpy as np
import math
import re
import json
import sys

# Función para calcular la ponderación basada en calidad (score y reviews)
def calculate_quality_weight(product_data):
    # Calcula la ponderación basada en calidad (score y reviews)
    scores = [float(product['score']) for product in product_data]
    
    # Filtra los puntajes no válidos (0 y NaN) antes de calcular el promedio
    filtered_scores = [score for score in scores if score != 0]
    
    if len(filtered_scores) > 0:
        mean_scores = float(np.mean(filtered_scores))
    else:
        mean_scores = 1  # Si no hay puntajes válidos, usa 1 como valor por defecto
    
    # Define el número mínimo de reviews requeridas para que un producto sea considerado
    m = float(1)
    
    products_with_values = []
    
    for product in product_data:
        score = float(product["score"])
        reviews = float(product['reviews'])
        
        # Calcula el valor de calidad usando la fórmula de Bayes
        value = ((mean_scores * m) + (reviews * score)) / (mean_scores + reviews)
        
        # Aplica puntos adicionales por ser best seller y tener envío gratis
        if product['best_seller'] == 1:
            value += 0.5
        if product['shipping'] == 1:
            value += 0.5
        
        product['quality_value'] = value
        products_with_values.append(product)
    
    return products_with_values

def calculate_price_weight(product_data):

    # Calcula la ponderación basada en precio
    prices = [product['price'] for product in product_data if product['price'] is not None]
    
    if not prices:
        return []  # No se encontraron precios válidos en los productos
    
    # Calcula el promedio de precios
    mean_prices = np.mean(prices)
    
    products_with_values = []
    
    for product in product_data:
        price = product.get('price', None)
        
        if price is not None:
            try:
                price = float(price)
            except ValueError:
                continue  # Ignora el producto si el precio no es válido
                
            # Calcula el valor de precio usando la diferencia con respecto al umbral
            value = (mean_prices - price) / 250
            
            # Aplica puntos adicionales por ser best seller y tener envío gratis
            if product['best_seller'] == 1:
                value += 0.5
            if product['shipping'] == 1:
                value += 0.5
            
            product['price_value'] = value
            products_with_values.append(product)

    return products_with_values

# Función para generar recomendaciones basadas en la ponderación seleccionada
def generate_recommendations(product_data, weighting_type):
    if weighting_type == 'quality':
        # Calcula la ponderación basada en calidad
        products_with_values = calculate_quality_weight(product_data)
    elif weighting_type == 'price':

        # Calcula la ponderación basada en precio
        products_with_values = calculate_price_weight(product_data)
    elif weighting_type == 'quality_price':
        # Ponderación basada en calidad-precio (combina calidad y precio)
        
        # Calcular la ponderación de calidad
        quality_weighted = calculate_quality_weight(product_data)
        
        # Calcular la ponderación de precio
        price_weighted = calculate_price_weight(product_data)
        
        # Combina la ponderación de calidad y precio
        products_with_values = []
        
        for q_product in quality_weighted:
            for p_product in price_weighted:
                if q_product['id'] == p_product['id']:
                    quality_price_value = q_product['quality_value'] + p_product['price_value']
                    q_product['quality_price_value'] = quality_price_value
                    products_with_values.append(q_product)
        
        # Ordena los productos en función de la ponderación de calidad-precio total
        products_with_values = sorted(products_with_values, key=lambda x: x['quality_price_value'], reverse=True)
    else:
        sys.stderr.write("Tipo de ponderación no válido. Debe ser 'quality', 'price' o 'quality_price'.")
        return []
    # Ordena los productos por la ponderación y devuelve las mejores recomendaciones
    recommended_products = sorted(products_with_values, key=lambda x: x.get(f'{weighting_type}_value', 0), reverse=True)
    recommended_products = recommended_products[:10]
    for product in recommended_products:
        sys.stderr.write(product['title'])
    return recommended_products  # Devuelve las mejores 5 recomendaciones


# Función para realizar el web scraping/crawling y obtener datos de productos desde tiendas en línea
def scrape_product_data(keyword, excludes):
    
    url= 'https://listado.mercadolibre.com.mx/'+keyword

    links = []
    cont_excludes = 0
    cont_products = 0
    sys.stderr.write('Paso Scrapeando\n')
    sys.stderr.write('Obteniendo links...\n')
    while True:
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'html.parser')
        section = soup.select_one("#root-app > div > div.ui-search-main.ui-search-main--only-products.ui-search-main--with-topkeywords > section")

        #section = soup.find('section',
        #{'class': 'ui-search-results ui-search-results--without-disclaimer shops__search-results'})
        buttons = soup.find_all('span', {'class': 'andes-pagination__arrow-title'})        
        for next_button in buttons:
            last=True
            if next_button.text.strip().lower() == 'siguiente':
                # Obtener el enlace del botón "Siguiente"
                url = next_button.find_parent('a')['href']
                last=False
                        
        ol = soup.find_all('ol')
        for each in ol:
            items = each.find_all('li')

            for product in items:
                cont_products+=1
                sys.stderr.write(f"{cont_products}\n")                
                sys.stderr.flush
                title = product.find('h2', {'class': 'ui-search-item__title'})
                if title is not None:
                    title = title.text.strip() 
                else: title = '' 
                if title:
                    title_text = title.lower()
                    if excludes is not None:
                        if any(keyword in title_text for keyword in excludes):
                            # El producto contiene una palabra clave a excluir, no lo agregues a la lista de links
                            cont_excludes += 1
                            continue             
                link = product.find('a', {'class': 'ui-search-item__group__element ui-search-link'}, href=True)
                if link is not None:
                    link = link['href']
                else:                                        
                    continue
                links.append(link)
        if last:
            break
    sys.stderr.write(f'excludes: {cont_excludes}\n')
    sys.stderr.write(f'Productos: {len(links)}\n')
    products=[]
    contador=1
    sys.stderr.write('Obteniendo datos de productos...\n')
    for url in links:
        sys.stderr.write(f'Procesando {round(contador/len(links)*100, 2)}%\n')
        sys.stderr.flush()
        if url is not None:
            html = requests.get(url)
            # Continúa con el procesamiento del contenido HTML
        else:
            sys.stderr.write("URL no definida o es None. Verifica la obtención de la URL en tu código.")

        soup = BeautifulSoup(html.content, 'html.parser')

        title = soup.find('h1', {'class': 'ui-pdp-title'})
        if title is not None:
            title=title.text.strip()

        reviews = soup.find('span', {'class': 'ui-pdp-review__amount'})
        if reviews is not None:
            reviews=reviews.text.strip()
            reviews = int(re.search(r'\d+', reviews).group())
        else: reviews=0

        price = soup.find('span', {'class': 'andes-money-amount__fraction'})
        if price is not None:
            price=price.text.strip()
            price=price.replace(',','')
            price= int(price)

        score = soup.find('p',
        {'class': 'ui-review-capability__rating__average ui-review-capability__rating__average--desktop'})
        if score is not None:
            score=score.text.strip()
        else: score=0

        best_seller = soup.find('p',
        {'class': 'ui-seller-info__status-info__title ui-pdp-seller__status-title'})
        if best_seller is not None:
            best_seller= 1
        else: best_seller=0

        shipping = soup.find('svg', {'class': 'ui-pdp-icon ui-pdp-icon--full'})
        if shipping is not None:
            shipping= 1
        else: shipping=0

        img_link = soup.find('figure', {'class': 'ui-pdp-gallery__figure'})
        if img_link is not None:
            img_tag = img_link.find('img')
            if img_tag is not None and 'data-zoom' in img_tag.attrs:
                img_src = img_tag['data-zoom']

        products.append({"id":contador,"title": title, "reviews": reviews, "price": price, "score": score, "best_seller": best_seller, "shipping": shipping, "img_link": img_src, 'url':url})
        contador += 1        
        
    sys.stderr.write(f'Productos Scrapeados con exito: {len(products)}\n')
    sys.stderr.flush()
    return products

# Función principal que recibe parámetros y ejecuta el proceso
def main(product_description, weighting_type, excludes):
    # Realiza web scraping/crawling para obtener datos de productos
    product_data = scrape_product_data(product_description, excludes)
    sys.stderr.write('Paso scrapeo\n')
    sys.stderr.flush()
    sys.stderr.write("Generando recomendaciones...")
    sys.stderr.flush()
    # Genera recomendaciones basadas en la ponderación seleccionada
    recommendations = generate_recommendations(product_data, weighting_type)
    
    if not recommendations:
        sys.stderr.write("No se encontraron recomendaciones para la ponderación seleccionada.")
        return
    
    sys.stderr.write("success")
    recommendations_json = json.dumps(recommendations)
    sys.stdout.write(recommendations_json)
    sys.stdout.flush()
    sys.stderr.write("Recomendaciones generadas con éxito.")
    return


if __name__ == "__main__":
    # Ejemplo de ejecución del script
    product_description = "Cera hombre"
    excludes = []
    weighting_type = "quality"  # Puedes cambiar el tipo de ponderación según tus necesidades
    #product_description = sys.argv[1]
    #excludes = sys.argv[2]  # Convierte la cadena en formato JSON de vuelta a una lista
    #weighting_type = sys.argv[3]
    #if not excludes:
    #    excludes = []
    #else:
    #    excludes = json.loads(excludes)
    main(product_description, weighting_type, excludes)
