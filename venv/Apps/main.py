from flask import Flask
import sqlite3
from routes import dp


app = Flask(__name__)
app.register_blueprint(dp)


def init_db() -> None:
    """Create the pollen table if it does not exist."""
    with sqlite3.connect("pollen.db") as con:
        cur = con.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS pollen(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                area_key TEXT,
                area_name TEXT,
                date DATE,
                pollen INT
            )
            """
        )
        con.commit()

init_db()


if __name__ == "__main__":
    app.run(debug=True)
