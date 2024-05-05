import requests
from deep_translator import GoogleTranslator  
from tkinter import *
from PIL import Image, ImageTk  # Importer le module PIL pour gérer les images
import customtkinter

api_key = '6a0e09230bc81cb8964db9f447b973da'

app = customtkinter.CTk()
app.title('Météo en temps réel !')


def recupInfo():
    ville = champVille.get()
    weather_data = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={ville}&units=metric&APPID={api_key}")
    
    if weather_data.status_code == 404:  # Vérifier si la ville n'a pas été trouvée
        return '404', None, None
    
    weather_main = weather_data.json()['weather'][0]['main']  # Utiliser la clé 'main' pour obtenir la condition principale
    weather_fr = translate_weather_to_french(weather_main)
    temperatureC = round(weather_data.json()['main']['temp'])
    humidity = round(weather_data.json()['main']['humidity'])
    return weather_fr, temperatureC, humidity

def translate_weather_to_french(weather):
    translated_weather = GoogleTranslator(source='auto', target='fr').translate(weather)
    return translated_weather

def afficher_image_meteo():
    # Dictionnaire associant chaque condition météorologique à son image correspondante
    weather_images = {
        'Clair': '../img/sun.png',
        'Des nuages': '../img/clouds.png',
        'Pluie': '../img/rain.png',
        }
    
    ville = champVille.get()
    weather_data = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={ville}&units=metric&APPID={api_key}")
    weather = weather_data.json()['weather'][0]['main']
    weather_fr = GoogleTranslator(source='auto', target='fr').translate(weather)
    
    image_path = None
    
    # Vérifiez si la météo est dans le dictionnaire weather_images, sinon utilisez le chemin par défaut
    image_path = weather_images.get(weather_fr)
    
    if image_path:
        image = Image.open(image_path)  # Ouvrir l'image correspondante
        image = image.resize((100, 100), Image.ANTIALIAS)  # Redimensionner l'image
        photo = ImageTk.PhotoImage(image)  # Convertir l'image en un format compatible avec Tkinter
        label_image = Label(app, image=photo)
        label_image.image = photo  # Garder une référence à l'objet photo pour éviter la suppression par le garbage collector
        label_image.pack(side="top", pady=(10, 10))
    else:
        print("Image non trouvée pour la condition météorologique:", weather_fr)

def bouton_confirm():
    # Récupérer tous les widgets enfants de l'application
    children = app.winfo_children()
    
    # Parcourir les widgets et détruire uniquement les étiquettes de météo
    for widget in children:
        if isinstance(widget, customtkinter.CTkLabel) and widget != titre and widget != labelVille:
            widget.destroy()

    weather_fr, temperatureC, humidity = recupInfo()
    if weather_fr != '404':
        labelClimat = customtkinter.CTkLabel(app, text=f"Le climat dans {champVille.get()} est : {weather_fr}")
        labelClimat.pack(side="top", pady=(10, 10))
        labelTemperature = customtkinter.CTkLabel(app, text=f"La temperature dans {champVille.get()} est de {temperatureC}°C")
        labelTemperature.pack(side="top", pady=(10, 10))
        labelHumidite = customtkinter.CTkLabel(app, text=f"L'humidité dans l'air à {champVille.get()} est de : {humidity}%")
        labelHumidite.pack(side="top", pady=(10, 10))
        afficher_image_meteo(weather_fr)
    else:
        labelErreur = customtkinter.CTkLabel(app, text="La ville n'a pas été trouvée !")
        labelErreur.pack(side="top", pady=(10, 10))
        
titre = customtkinter.CTkLabel(app, text="Météo en temps réel !")
titre.pack(side="top", pady=(10, 10))

labelVille = customtkinter.CTkLabel(app, text="Entrez une ville :")
labelVille.pack(side="top", pady=(10, 10))
champVille = customtkinter.CTkEntry(app, width=100)
champVille.pack(side="top", pady=(10, 10))

button = customtkinter.CTkButton(app, text="Confirmer", fg_color=("red"), width=75, height=25, command=bouton_confirm)
button.pack(side="top", pady=(20))
        
app.mainloop()