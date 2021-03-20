from flask import request, jsonify #ambil library json untuk konversi Datatable kebebntuk data json
from app import app #ambil folder app dan semua isinya
from app.constant import RequestMethod #ambil folder app -> constant dan ambil file RequestMethod
from app.model.QueriesModel import Queries #ambil folder app -> model -> QueriesModel dan ambil file Queries
from app.model.DetailsModel import Details #ambil folder app -> model -> DetailsModel dan ambil Details Queries
from app.module.Engine import preprocess, Engine #ambil folder app -> Engine dan ambil Calss Engine dan fungsi preprocess
import pandas as pd #ambil library pandas
import os #ambil library os
from numpy import math #ambil library numpy untuk konversi hasil score NAN
from app.module.Query import read_all, read_with_params, insert, read_one


@app.route("/", methods=RequestMethod.GET)
def index():
    return jsonify({"message": "ok"})


@app.route("/search", methods=RequestMethod.GET_POST)
def search():
    # dataset = pd.read_excel("app/db/databerita.xlsx")
   
    dataset = " SELECT sys_dosen.dosen_name, mst_dosen_judul.dosen_judul, mst_dosen_judul.dosen_judul_processing, mst_dosen_judul.dosen_judul_id , sys_dosen.dosen_id FROM mst_dosen_judul JOIN sys_dosen ON sys_dosen.dosen_id = mst_dosen_judul.dosen_id"
    results = read_all(dataset)

    temp_preprrocessing = []
    temp_judul = []
    temp_dosen = []
    temp_dosen_judul = []
    temp_dosen_id = []
    for doc in results :
        temp_dosen.append(doc[0])
        temp_judul.append(doc[1])
        temp_preprrocessing.append(doc[2])
        temp_dosen_judul.append(doc[3])
        temp_dosen_id.append(doc[4])
   
    response = list()  # Define response
    if request.method == "POST":
        if "files" in request.files:
            file = request.files["files"]
            file.save(os.path.join("app/tmp", "queries.xlsx"))
            queries = pd.read_excel("app/tmp/queries.xlsx")
            queries = queries["Queries"].values
        else:
            resp = {
                "error": "invalid request",
                "path": "/search",
                "message": "request should be file"
            }
            resp = jsonify(resp)
            resp.status_code = 400
            print(resp)
            return resp

    elif request.method == "GET":
        if 'q' in request.args:
            queries = [request.args['q']]
        else:
            resp = {
                "error": "invalid request",
                "path": "/search",
                "message": "request should be query"
            }
            resp = jsonify(resp)
            resp.status_code = 400
            return resp

        # Preproces queries
    queriesPre = list()
    for query in queries:
        queriesPre.append(preprocess(query))

    # Cek di database apakah ada data dengan query pada inputan ataupun file
    for query in queriesPre:
        data = Queries.findByQueryName(query)
        if data is not None:
            response.append(data)

    if len(response) is not 0:
        return jsonify(response)
    else:
        engine = Engine()
        docs = [str(x) for x in temp_preprrocessing]
        documentsName = list()

        for i, doc in enumerate(docs):
            engine.addDocument(doc)
            documentsName.append("Document_{}".format(i + 1))

        for query in queriesPre:
            engine.setQuery(query)  # Set query pencarian

        titlesScores = engine.process_score()
        ScoreDf = (pd.DataFrame(titlesScores)).T
        ScoreDf.columns = queriesPre
        ScoreDf["Documents"] = documentsName
        dfListed = list()
        for i in queriesPre:
            labels = list()
            for j in ScoreDf[i]:
                if j > 0.000:
                    labels.append(1)
                else:
                    labels.append(0)
            datadf =pd.DataFrame(ScoreDf[i])
            datadf["Documents"] = ScoreDf["Documents"]
            datadf["Labels"] = labels
            dfListed.append(datadf.sort_values(by=[i], ascending=False))

        for i, df in enumerate(dfListed):
            dbQuery = Queries(queriesPre[i])
            for j in range(len(df["Documents"])):
                if (math.isnan(float(df[queriesPre[i]][j]))):
                    score = '0'
                else:
                    score = float(df[queriesPre[i]][j])
                document            = df["Documents"][j]
                label               = int(df["Labels"][j])
                score               = score
                judul               = temp_judul[j]
                dosen               = temp_dosen[j]
                dosen_judul         = temp_dosen_judul[j]
                dosen_id            = temp_dosen_id[j]
                data = document, label, score , judul, dosen, dosen_id,dosen_judul
               
                details = Details(data) 
                dbQuery.details.append(details)

            dbQuery.save()

        for query in queriesPre:
            data = Queries.findByQueryName(query)
            response.append(data)

    return jsonify(response)


@app.route("/test", methods=RequestMethod.GET)
def getData():
    response = Queries.getAll()
    print(response)
    return jsonify(response)
