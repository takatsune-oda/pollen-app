from flask import Flask, request, render_template, redirect, url_for, jsonify
import requests
import sqlite3


app = Flask(__name__)

pollen_data = {"tokyo":{"area": "東京", "date": "2026-02-08", "pollen": 100}, 
               "osaka":{"area": "大阪", "date": "2026-02-08", "pollen": 100},
               "nagoya":{"area": "名古屋", "date": "2026-02-08", "pollen": 120}
               }

# データベース作成
con = sqlite3.connect("pollen.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS pollen(id INTEGER PRIMARY KEY AUTOINCREMENT, area_key TEXT, area_name TEXT, date DATE, pollen INT)")
con.commit()
con.close() 


# @app.route("/<area>", methods=["GET", "POST"])
# def pollen_info(area):
#     if area in pollen_data:
        
#         area_name = pollen_data[area]["area"]
#         date = pollen_data[area]["date"]
#         pollen = pollen_data[area]["pollen"]

#         return render_template("select.html", area=area_name, date=date, pollen=pollen)
#     else:
#         message = f"{area}地域の花粉情報はありません。"
#         return render_template("select.html", message=message)


@app.route("/mock/pollen/<area>") # モックAPI
def mock_pollen(area):
    if area in pollen_data:

        return jsonify(pollen_data[area])
    else:
        return jsonify({"error": "not found"}), 404



@app.route("/", methods=["GET"]) # 地域選択画面
def select_area():
    area = request.args.get("area")
    if area :
        return redirect(url_for("pollen_info", area=area))
    else:
        return render_template("index.html")
    

# @app.route("/areas", methods=["GET"])
# def areas_list():

#         return render_template("areas.html", areas=pollen_data.items())


@app.route("/api/areas") # 地域一覧を表示する
def areas_list():
    areas = []

    con = sqlite3.connect("pollen.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT area_key, area_name, date, pollen FROM pollen")
    rows = cur.fetchall()

    areas = [dict(row) for row in rows]
    con.close()
    return jsonify(areas)


if __name__ == "__main__":
    app.run(debug=True)