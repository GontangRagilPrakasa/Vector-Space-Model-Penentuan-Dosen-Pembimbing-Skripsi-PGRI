from flask import request, jsonify, flash
from app import app
from app.module.Engine import Engine, preprocess
from app.module.Query import read_all, read_with_params, insert, read_one
import os
from flask import render_template
from sklearn.model_selection import cross_val_score
import time
import pandas as pd
import numpy as np
from numpy import math #ambil library numpy untuk konversi hasil score NAN
from datetime import datetime



@app.route('/')
def index():
    search = " SELECT * FROM mst_dosen_judul JOIN mst_dosen ON mst_dosen.id = mst_dosen_judul.dosen_id ORDER BY id ASC"
    results = read_all(search)
    simpan = []
    for i, doc in enumerate(results):
        document = "Document_{}".format(i + 1)
        label = 0
        score = 0
        judul = doc[2]
        dosen = doc[5]
        student = doc[6]
        simpan.append((document,label,score,judul,dosen,student))
        
    df = pd.DataFrame(simpan, columns=['Document','Labels','Score','Judul','Nama Dosen','Kuota Siswa'])
    df.sort_values(by=['Score'], inplace=True, ascending=False)
    df = df.fillna(0)
    html = df.to_html(index= False,classes="table mb-0 border-0 table-responsive").replace('border="1"', "")
    return render_template('index.html',
         tables=[html], 
    )

@app.route('/data-dosen')
def data_dosen():
    search = " SELECT * FROM mst_dosen"
    results = read_all(search)
    simpan = []
    for i, doc in enumerate(results):
        document = "Document_{}".format(i + 1)
        dosen = doc[1]
        student = doc[2]
        simpan.append((document,dosen,student))
        
    df = pd.DataFrame(simpan, columns=['Document','Nama Dosen','Kuota Siswa', ])
    df.sort_values(by=['Kuota Siswa'], inplace=True, ascending=False)
    df = df.fillna(0)
    html = df.to_html(index= False,classes="table mb-0 border-0 table-responsive").replace('border="1"', "")
    return render_template('data-dosen.html',
        tables=[html], 
    )
@app.route('/tambah-dosen')
def tambah_dosen():
    return render_template('tambah-dosen.html')

@app.route('/proses-tambah-dosen', methods=['POST'])
def proses_tambah_dosen():
    nama_dosen  = request.form['nama_dosen']
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    last_id = read_one('SELECT id FROM mst_dosen ORDER BY id DESC LIMIT 1')
    insert_data_dosen = """INSERT INTO mst_dosen (id, nama_dosen, jumlah_pengajar, created_by, created_at) 
                            VALUES (%s, %s, %s, %s, %s) """
    data_result = [(last_id[0]+1,nama_dosen,0,1,dt_string)]
    results = insert(insert_data_dosen,data_result)
    dosen = read_with_params('SELECT id FROM mst_dosen WHERE nama_dosen = %s',(nama_dosen,))
    judul_dosen = request.form.getlist('judul_dosen[]')
    judul_dosen_temp = []
    for judul in  judul_dosen :
        last_id_judul       = read_one('SELECT id_judul FROM mst_dosen_judul ORDER BY id_judul DESC LIMIT 1')
        insert_judul_dosen = """INSERT INTO mst_dosen_judul (id_judul, dosen_id, judul, preprocessing) 
                            VALUES (%s, %s, %s, %s) """
        preprocessing = preprocess(judul) #konversi ke preprocessing
        
        data_result_judul   = [(last_id_judul[0]+1,dosen[0],judul,preprocessing)]
        results_judul = insert(insert_judul_dosen,data_result_judul)

    return render_template('tambah-dosen.html')


@app.route('/data-mahasiswa')
def data_mahasiswa():
    search = " SELECT * FROM mst_dosen"
    results = read_all(search)
    simpan = []
    for i, doc in enumerate(results):
        document = "Document_{}".format(i + 1)
        dosen = doc[1]
        student = doc[2]
        simpan.append((document,dosen,student))
        
    df = pd.DataFrame(simpan, columns=['Document','Nama Dosen','Kuota Siswa', ])
    df.sort_values(by=['Kuota Siswa'], inplace=True, ascending=False)
    df = df.fillna(0)
    html = df.to_html(index= False,classes="table mb-0 border-0 table-responsive").replace('border="1"', "")
    return render_template('data-mahasiswa.html',
        tables=[html], 
    )

@app.route('/proses', methods=['POST','GET'])
def proses():
    query = [str(request.form['cari'])]

    search = " SELECT * FROM mst_dosen_judul JOIN mst_dosen ON mst_dosen.id = mst_dosen_judul.dosen_id WHERE jumlah_pengajar != 30 ORDER BY id ASC"
    results = read_all(search)
    temp_preprrocessing = []
    temp_judul = []
    temp_dosen = []
    temp_student_max = []
    for doc in results :
        temp_preprrocessing.append(doc[3])
        temp_judul.append(doc[2])
        temp_dosen.append(doc[5])
        temp_student_max.append(doc[6])
    
    engine = Engine() #memanggil class diatas

    docs = [str(x) for x in temp_preprrocessing] #melakukan perulangan untuk merubah setiap column menjadi string
   
    if not docs :
        return "gagal"
    else :
        document = []

        for i, doc in enumerate(docs):
            engine.addDocument(doc)
            document.append("Document_{}".format(i + 1))

        for queries in query:
            engine.setQuery(queries)  # Set query pencarian
        
        titles_score = engine.process_score() #memanggil function process score pada class engine dari hasil addDocument diatas
        ScoreDf = (pd.DataFrame(titles_score)).T #merubah data hasil keluaran menjadi DAtaFrame
        ScoreDf.columns = query #mendefinisikan quqery sebagai data training
        ScoreDf["Documents"] = document #membuat Document sesuai urutan teratas hasil TF-IDF dan VSM
        df_listed = []        
        for i in query:
            labels = []
            for j in ScoreDf[i]:
                if j>0.000:
                    labels.append(1)
                else:
                    labels.append(0)
            datadf = pd.DataFrame(ScoreDf[i])
            datadf['Documents'] = ScoreDf['Documents']
            datadf["Labels"] = labels
            df_listed.append(datadf.sort_values(by=[i], ascending=False))
      
        simpan = []
        for i, df in enumerate(df_listed):
            for j in range(len(df["Documents"])):
                if (math.isnan(float(df[query[i]][j]))):
                    score = '0'
                else:
                    score = float(df[query[i]][j])
                document = df['Documents'][j]
                score = score
                labels = int(df['Labels'][j])
                judul = temp_judul[j]
                dosen = temp_dosen[j]
                student = temp_student_max[j]
                simpan.append((document,labels,score,judul,dosen,student))
    df = pd.DataFrame(simpan, columns=['Document','Labels','Score','Judul','Nama Dosen','Kuota Siswa'])
    df.sort_values(by=['Score'], inplace=True, ascending=False)
    df = df.fillna(0)
    html = df.to_html(index= False,classes="table mb-0 border-0 table-responsive").replace('border="1"', "")
        # masuk = pd.DataFrame(simpan,columns=['1','2','3','4','5'])
    return render_template('index.html', 
        tables=[html], 
        query=str(request.form['cari'])
    )
    
