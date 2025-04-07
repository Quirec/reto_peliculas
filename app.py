import streamlit as st
import pandas as pd
from google.cloud import firestore
from google.oauth2 import service_account
import json



key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="movie-reto")
dbMovies = db.collection("peliculas")

#titulo
st.title('NETFLIX MOVIES DATA ')





movies_ref = list(db.collection(u'peliculas').stream())
movies_dict = list(map(lambda x: x.to_dict(), movies_ref))
movies_dataframe = pd.DataFrame(movies_dict)
st.dataframe(movies_dataframe)


# filtro buscar nombre 


def loadByName(name):
  names_ref = dbMovies.where(u'name', u'==', name)
  currentName = None

  for myname in names_ref.stream():
    currentName = myname
  return currentName

st.sidebar.subheader('Buscar nombre')
nameSearch = st. sidebar.text_input('Titilo del filme')
btnFiltrar = st.sidebar.button('Buscar filme')

if btnFiltrar :
    doc= loadByName(nameSearch)
    if doc is None:
      st.sidebar.write('Nombre no existe')
    else:
      st.sidebar.write(doc.to_dict())


##filtro director

def loadByDirector(director):
  director_ref = dbMovies.where(u'director',u'==', director)
  currentDirector = None
  for mydirector in director_ref.stream():
    currentDirector = mydirector
  return currentDirector


st.sidebar.markdown("""_ _ _""")
st.sidebar.subheader('Buscar Director')
directorSearch = st.sidebar.selectbox('Director', movies_dataframe['director'].unique(),key='buscar director')
btnFiltrarDirector = st.sidebar.button('Buscar director')

if btnFiltrarDirector :
    doc= loadByDirector(directorSearch)
    if doc is None:
      st.sidebar.write('Director no existe')
    else:
      st.sidebar.write(doc.to_dict())


#nueva entrada 

st.sidebar.markdown("""_ _ _""")
st.sidebar.subheader('Nuevo registro')
name = st.sidebar.text_input("name")
genre = st.sidebar.selectbox('Genre', movies_dataframe['genre'].unique(),key='nuevo registro genre')
director= st.sidebar.selectbox('Director',movies_dataframe['director'].unique(), key='nuevo registro dorector')
company = st.sidebar.selectbox('Company',movies_dataframe['company'].unique(),key= 'nuevo registro company ') 

submit = st.sidebar.button("Crear nuevo registro")
# Once the name has submitted, upload it to the database
if name and genre and director and company and submit:
 doc_ref = db.collection("peliculas").document(name)
 doc_ref.set({
 "name": name,
 "genre": genre,
 "director": director,
 "company": company
 })
 st.sidebar.write("Registro insertado correctamente")
