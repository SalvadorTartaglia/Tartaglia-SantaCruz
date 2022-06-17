from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def generarListaPerCapita():
  lista = []
  conn = sqlite3.connect('co_emissions.db')

  q = f'''SELECT Country, Value, Year
          FROM emissions
          WHERE Series = 'pcap'
          ORDER BY Value DESC
       '''
  resu = conn.execute(q)

  for fila in resu:
    lista.append(fila)

  conn.close()
    
  return lista

def generarListaTotal(): 
  lista = []
  conn = sqlite3.connect('co_emissions.db')
  
  q = '''SELECT country_id, Value, Year
         FROM emissions
         WHERE series = 'total'
      '''
  resu = conn.execute(q)
  
  for fila in resu:
    subLista = [fila[0], fila[1], fila[2]]
    lista.append(subLista)
  
  i = 0
  while i < len(lista):
    lista[i][1] = int(lista[i][1])
    i += 1

  
  """
    q = '''ALTER TABLE emissions
           ADD  ValueInt INT
        '''
    conn.execute(q)
    conn.commit()
  
    i = 0
    while i < len(lista):
      q = '''UPDATE emissions
             SET ValueInt = %i
             WHERE country_id = '%s' AND Year = '%s'
          ''' %(lista[i][1], lista[i][0], lista[i][2])
      conn.execute(q)
      conn.commit()
      i += 1
    """
  
  q = '''SELECT Country, ValueInt, Year
         FROM emissions
         WHERE Series = 'total'
         ORDER BY ValueInt DESC
      '''
  resu = conn.execute(q)
  
  lista.clear()
  
  for fila in resu:
    lista.append(fila)
  
  conn.close()

  return lista

def sacarRepetidos(lista):
  i = 1
  paises = []
  while i < 10:
    paises.append(lista[i-1][0])
    if lista[i][0] in paises:
      lista.pop(i)
    else:
      i += 1
  return lista

def generarListaPorPais(pais):
  lista = []
  conn = sqlite3.connect('co_emissions.db')

  q ='''SELECT Value, Series, Year
       FROM emissions
       WHERE Country = '%s'
     ''' % (pais)
  resu = conn.execute(q)

  for fila in resu:
    subLista = [fila[0], fila[1], fila[2]]
    lista.append(subLista)

  conn.close()

  return lista

def generarListaDePaises():
  lista = []
  conn = sqlite3.connect('co_emissions.db')

  q = '''SELECT DISTINCT Country
         FROM emissions
      '''
  resu = conn.execute(q)

  for fila in resu:
    lista.append(fila[0])

  conn.close()

  return lista

@app.route('/')
def index():
  return render_template('index.html', listaPaises = generarListaDePaises())

@app.route('/listado')
def listaPerCapita():
  return render_template('perCapita.html', listaValores = generarListaPerCapita(), listaPaises = sacarRepetidos(generarListaPerCapita()))
@app.route('/listado/<pais>')
def datosPais(pais):
  return render_template('porPais.html', paisElegido = pais.upper(), listaDatos = generarListaPorPais(pais))

@app.route('/top')
def listaTotal():
  return render_template('total.html', listaValores = generarListaTotal(), listaPaises = sacarRepetidos(generarListaTotal()))

@app.route('/ayuda')
def ayuda():
  return render_template('acercaDe.html')
  
app.run(host='0.0.0.0', port=81)