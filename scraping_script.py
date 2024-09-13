import requests
from bs4 import BeautifulSoup
def obtener_articulos_trome(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            articulos = []

            # Buscar los contenedores de los artículos
            contenedores = soup.find_all('div', class_='story-grid__info')

            for contenedor in contenedores:
                # Extraer el título
                titulo_tag = contenedor.find('a', class_='story-grid__title')
                titulo = titulo_tag.get_text(strip=True) if titulo_tag else 'No disponible'
                
                # Extraer la URL del artículo
                url_articulo = titulo_tag['href'] if titulo_tag and 'href' in titulo_tag.attrs else 'No disponible'
                
                # Extraer la fecha
                fecha_tag = contenedor.find('p', class_='story-grid__date')
                fecha = fecha_tag.get_text(strip=True) if fecha_tag else 'No disponible'
                
                # Extraer la descripción o contenido
                contenido_tag = contenedor.find('p', class_='story-grid__subtitle')
                contenido = contenido_tag.get_text(strip=True) if contenido_tag else 'Contenido no disponible'
                
                # Extraer la imagen
                imagen_tag = contenedor.find('img', class_='story-grid__img')
                imagen = imagen_tag['src'] if imagen_tag and 'src' in imagen_tag.attrs else 'No disponible'

                # Extraer el autor (si está disponible)
                autor_tag = contenedor.find('a', class_='story-grid__author')
                autor = autor_tag.get_text(strip=True) if autor_tag else 'Autor no disponible'

                # Agregar el artículo a la lista
                articulos.append({
                    'diario': 'Trome',
                    'titulo': titulo,
                    'url_articulo': f"https://trome.pe{url_articulo}" if url_articulo != 'No disponible' else 'No disponible',
                    'imagen': imagen,
                    'contenido': contenido,
                    'fecha': fecha,
                    'autor': autor
                })

            return articulos
        else:
            print(f"Error al solicitar la página: {response.status_code}")
            return []
    except Exception as e:
        print(f"Ocurrió un error al tratar de hacer scraping del sitio: {e}")
        return []

def obtener_articulos_el_comercio(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            articulos = []

            contenedores = soup.find_all('div', class_='story-item')

            for contenedor in contenedores:
                titulo_tag = contenedor.find('h2', class_='story-item__content-title').find('a', class_='story-item__title')
                titulo = titulo_tag.get_text(strip=True) if titulo_tag else 'No disponible'
                
                url_articulo = titulo_tag['href'] if titulo_tag and 'href' in titulo_tag.attrs else 'No disponible'
                
                fecha_tag = contenedor.find('p', class_='story-item__date')
                fecha = 'No disponible'
                if fecha_tag:
                    fechas = fecha_tag.find_all('span', class_='story-item__date-time')
                    if len(fechas) >= 2:
                        fecha = fechas[0].get_text(strip=True) + ' ' + fechas[1].get_text(strip=True)
                
                contenido_tag = contenedor.find('p', class_='story-item__subtitle')
                contenido = contenido_tag.get_text(strip=True) if contenido_tag else 'Contenido no disponible'
                
                imagen_tag = contenedor.find('figure', class_='story-item__right').find('img')
                imagen = imagen_tag['src'] if imagen_tag and 'src' in imagen_tag.attrs else 'No disponible'

                autor_tag = contenedor.find('a', class_='story-item__author')
                autor = autor_tag.get_text(strip=True) if autor_tag else 'Autor no disponible'
                
                articulos.append({
                    'diario': 'El Comercio',  
                    'titulo': titulo,
                    'url_articulo': url_articulo,
                    'imagen': imagen,
                    'contenido': contenido,
                    'fecha': fecha,
                    'autor': autor
                })

            return articulos
        else:
            print(f"Error al solicitar la página: {response.status_code}")
            return []
    except Exception as e:
        print(f"Ocurrió un error al tratar de hacer scraping del sitio: {e}")
        return []



def obtener_articulos_diario_sin_fronteras(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            articulos = []

            contenedores = soup.find_all('div', class_='layout-wrap', role='article')

            print(f"Total de artículos encontrados: {len(contenedores)}")  # Verificar cuántos artículos se encontraron

            for contenedor in contenedores:
                titulo_tag = contenedor.find('h3', class_='entry-title')
                titulo = titulo_tag.get_text(strip=True) if titulo_tag else 'No disponible'

                url_articulo = titulo_tag.find('a')['href'] if titulo_tag and titulo_tag.find('a') else 'No disponible'

                contenido_tag = contenedor.find('div', class_='post-excerpt')
                contenido = contenido_tag.get_text(strip=True) if contenido_tag else 'Contenido no disponible'

                fecha_tag = contenedor.find('div', class_='post-date-bd')
                fecha = fecha_tag.get_text(strip=True) if fecha_tag else 'No disponible'

                imagen_tag = contenedor.find('img', class_='attachment-bd-large size-bd-large wp-post-image')
                imagen = imagen_tag['src'] if imagen_tag and 'src' in imagen_tag.attrs else 'No disponible'

                autor_tag = contenedor.find('a', class_='post-author')
                autor = autor_tag.get_text(strip=True) if autor_tag else 'Autor no disponible'

                articulos.append({
                    'diario': 'Diario Sin Fronteras',  
                    'titulo': titulo,
                    'url_articulo': url_articulo,
                    'imagen': imagen,
                    'contenido': contenido,
                    'fecha': fecha,
                    'autor': autor
                })

            return articulos
        else:
            print(f"Error al solicitar la página: {response.status_code}")
            return []
    except Exception as e:
        print(f"Ocurrió un error al tratar de hacer scraping del sitio: {e}")
        return []


if __name__ == "__main__":
    url_trome = "https://trome.pe/ultimas-noticias/"
    articulos_trome = obtener_articulos_trome(url_trome)
    print("Artículos de Trome:")
    for articulo in articulos_trome:
        print(articulo)

    url_el_comercio = "https://elcomercio.pe/ultimas-noticias/"
    articulos_el_comercio = obtener_articulos_el_comercio(url_el_comercio)
    print("Artículos de El Comercio - Últimas Noticias:")
    for articulo in articulos_el_comercio:
        print(articulo)

    url_diario_sin_fronteras = "https://diariosinfronteras.com.pe/category/puno/"
    articulos_diario_sin_fronteras = obtener_articulos_diario_sin_fronteras(url_diario_sin_fronteras)
    print("\nArtículos de Diario Sin Fronteras:")
    for articulo in articulos_diario_sin_fronteras:
        print(articulo)
