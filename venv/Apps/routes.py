from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from database import get_db_connection
from external_api import ExternalAPIError, fetch_latest_pollen


dp = Blueprint("main", __name__)


def save_pollen_record(record: dict) -> None:
    con = get_db_connection()
    try:
        cur = con.cursor()
        cur.execute(
            """
            INSERT INTO pollen(area_key, area_name, date, pollen)
            VALUES(?, ?, ?, ?)
            """,
            (record["area_key"], record["area_name"], record["date"], record["pollen"]),
        )
        con.commit()
    finally:
        con.close()


@dp.route("/areas/<area_key>")  # 花粉情報の取得
def area_detail(area_key):
    con = get_db_connection()
    try:
        cur = con.cursor()
        cur.execute(
            """
            SELECT area_key, area_name, date, pollen
            FROM pollen
            WHERE area_key = ?
            ORDER BY date DESC, id DESC
            """,
            (area_key,),
        )
        pollen_rows = cur.fetchall()

        if not pollen_rows:
            try:
                latest_record = fetch_latest_pollen(area_key)
            except ValueError:
                return jsonify({"error": "unsupported area"}), 400
            except ExternalAPIError:
                return jsonify({"error": "external api unavailable"}), 502
            
            save_pollen_record(latest_record)
            return jsonify([latest_record])
        
        return jsonify([dict(row) for row in pollen_rows])
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


@dp.route("/api/areas/<area_key>/sync", methods=["POST"])
def sync_area(area_key):
    try:
        latest_record = fetch_latest_pollen(area_key)
    except ValueError:
        return jsonify({"error": "unsupported area"}), 400
    except ExternalAPIError:
        return jsonify({"error": "external api unavailable"}), 500
    
    save_pollen_record(latest_record)
    return jsonify({"message": "synced", "record": latest_record}), 201
