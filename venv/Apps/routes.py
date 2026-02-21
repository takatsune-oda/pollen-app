from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from database import get_db_connection


dp = Blueprint("main", __name__)


@dp.route("/areas/<area_key>")  # 花粉情報の取得
def area_detail(area_key):
    con = get_db_connection()
    try:
        cur = con.cursor()
        cur.execute(
            "SELECT area_key, area_name, date, pollen FROM pollen WHERE area_key = ?",
            (area_key,),
        )
        pollen_rows = cur.fetchall()

        if pollen_rows:
            return jsonify([dict(row) for row in pollen_rows])
        return jsonify({"error": "not found"}), 404
    finally:
        con.close()


@dp.route("/", methods=["GET"])  # 地域選択画面
def select_area():
    area = request.args.get("area")
    if area:
        return redirect(url_for("main.area_detail", area_key=area))
    return render_template("index.html")


@dp.route("/api/areas")  # 地域一覧を表示する
def areas_list():
    con = get_db_connection()
    try:
        cur = con.cursor()
        cur.execute("SELECT area_key, area_name, date, pollen FROM pollen")
        rows = cur.fetchall()
        return jsonify([dict(row) for row in rows])
    finally:
        con.close()
