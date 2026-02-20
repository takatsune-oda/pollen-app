from flask import Flask, request, render_template, redirect, url_for, jsonify
import sqlite3


app = Flask(__name__)


# データベース作成
con = sqlite3.connect("pollen.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS pollen(id INTEGER PRIMARY KEY AUTOINCREMENT, area_key TEXT, area_name TEXT, date DATE, pollen INT)")
con.commit()
con.close() 


@app.route("/mock/pollen/<area>") # モックAPI
def mock_pollen(area):
    con = sqlite3.connect("pollen.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT area_key, area_name, date, pollen FROM pollen WHERE area_key = ?", (area,))
    pollen_area = cur.fetchone()

    if pollen_area:
        return jsonify(dict(pollen_area))
    else:
        return jsonify({"error": "not found"}), 404



@app.route("/", methods=["GET"]) # 地域選択画面
def select_area():
    area = request.args.get("area")
    if area :
        return redirect(url_for("mock_pollen", area=area))
    else:
        return render_template("index.html")


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