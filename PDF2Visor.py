import streamlit as st
import time
from github import Github

st.set_page_config(page_title = 'PDF2Visor', page_icon = '🤖', layout = "centered")

hide_streamlit_style = """
            <style>

            footer {visibility: hidden;}
            footer:after {
            	content:'Desarrollado por Junior Aguilar'; 
            	visibility: visible;
            	display: block;
            	position: relative;
            	#background-color: red;
            	padding: 5px;
            	top: 2px;
            }            
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# tokn = st.secrets["token"]
g    = Github('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')
rep1 = g.get_repo('junior19a2000/PDFs')
rep2 = g.get_repo('junior19a2000/Visor')

def edit_html(nombre):
    archivo_html_entrada = "PDF.html"
    nombre_nuevo_archivo = nombre
    with open(archivo_html_entrada, "r", encoding="utf-8") as archivo_entrada:
        contenido_html = archivo_entrada.read()
    contenido_modificado = contenido_html.replace("PDF.pdf", nombre_nuevo_archivo + ".pdf")
    archivo_html_salida = nombre_nuevo_archivo + ".html"
    with open(archivo_html_salida, "w", encoding="utf-8") as archivo_salida:
        archivo_salida.write(contenido_modificado)
    with open(nombre_nuevo_archivo + ".html", "r", encoding="utf-8") as archivo_html_salida:
        pdfhtml = archivo_html_salida.read()
    return pdfhtml

contents = rep1.get_contents('PDFs')
nombres  = []
numeros  = []
for archivo in contents:
    if archivo.type == 'file':
        nombres.append(archivo.name.replace('.pdf', ''))
        numeros.append(int(nombres[-1].replace('PDF', '')))
nombres.append('PDF' + str(max(numeros) + 1))

st.markdown("<h1 style='text-align: center; color: white;'>PDF2Visor 🤖</h1>", unsafe_allow_html = True)
st.subheader(':rainbow[Publique su archivo PDF como un libro virtual electrónico !]', divider = 'rainbow')
col1, col2 = st.columns([1, 1.8], gap = 'small')
with col1:
    st.markdown('### Nombre del archivo:')
with col2:
    nombre = st.selectbox('Nombres', options = nombres, placeholder = 'Escribalo aqui !', label_visibility = 'collapsed')
pdf_file = st.file_uploader('file_upload', type = ['pdf'], help = 'Suba su archivo pdf [max 200mb]', label_visibility = "collapsed")
button = st.button('Publicar !', use_container_width = True)
empty  = st.empty()
if button:
    data     = pdf_file.read()
    try:
        rep1.create_file('PDFs/' + nombre + '.pdf', 'upload file', data, branch = 'main')
    except:
        rep1.update_file('PDFs/' + nombre + '.pdf', 'update file', data, rep1.get_contents('PDFs/' + nombre + '.pdf').sha, branch = 'main')
    data     = edit_html(nombre)
    try:
        rep2.create_file(nombre + '.html', 'upload file', data, branch = 'main')
    except:
        rep2.update_file(nombre + '.html', 'update file', data, rep2.get_contents(nombre + '.html').sha, branch = 'main')
    empty.success("Su pdf ha sido publicado, espere un par de minutos para visualizarlo")
    time.sleep(3)
    empty.empty()
    st.experimental_rerun()

with st.expander('#### 📖 PDF publicado en: https://junior19a2000.github.io/Visor/' + nombre + '.html', expanded = False):
     url = 'https://junior19a2000.github.io/Visor/' + nombre + '.html'
     st.markdown(f'<iframe src={url} height="500" width="100%" style="border:0px solid black"></iframe>', unsafe_allow_html = True)
