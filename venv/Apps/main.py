from flask import Flask
import sqlite3
from routes import dp

app = Flask(__name__)
app.register_blueprint(dp)


# データベース作成
con = sqlite3.connect("pollen.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS pollen(id INTEGER PRIMARY KEY AUTOINCREMENT, area_key TEXT, area_name TEXT, date DATE, pollen INT)")
con.commit()
con.close() 


if __name__ == "__main__":
    app.run(debug=True)