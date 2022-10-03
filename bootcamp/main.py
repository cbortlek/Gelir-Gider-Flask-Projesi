from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

# Veri Ekleme Fonksiyonu


def veriEkle(gelir, gider, year,kategori,toplam):
    with sqlite3.connect("butce.db") as con:
        cur = con.cursor()
        toplam=int(gelir)-int(gider)
        cur.execute(
            "insert into tblIslem (gelir, gider, year,kategori,toplam) values (?, ?, ?, ?, ?)", (gelir, gider, year,kategori,toplam))
        con.commit()

    print("veriler eklendi")


data = []



def veriAl():
    global data
    with sqlite3.connect("butce.db") as con:
        cur = con.cursor()
        cur.execute("select * from tblIslem order by id desc ")
        data = cur.fetchall()
        # print(data)
        for i in data:
            print(i)


def veriSil(id):
    with sqlite3.connect("butce.db") as con:
        cur = con.cursor()
        cur.execute("delete from tblIslem where id=?", (id,))
       


def veriGuncelle(id, gelir, gider, year,kategori,toplam):
    with sqlite3.connect("butce.db") as con:
        cur = con.cursor()
        cur.execute("update tblIslem set gelir = ?, gider = ?, year = ?, kategori=?, toplam=?  where id = ?",
                    (gelir, gider, year,kategori,toplam, id))
        con.commit()
    print("Veriler Guncellendi...")


veriAl()
app = Flask(__name__)


@app.route("/")
def index():
    islemler = [
        {
            "ID": 1,
            "gelir": "1500",
            "gider": "1200",
            "year": "10.12.2022",
            "kategori":"sebze meyve",
            "toplam":"300" },
        {
            "ID": 2,
            "gelir": "2500",
            "gider": "1500",
            "year": "10.01.2022",
            "kategori":"kırmızı et",
            "toplam":"1000"},
        {
            "ID": 3,
            "gelir": "3000",
            "gider": "4000",
            "year": "10.11.2022",
            "kategori":"süt ve süt ürünleri",
            "toplam":"-1000"},
    ]
    return render_template("index.html", islemler=islemler)


@app.route("/islem/<string:id>")
def islemdetail(id):
    detayveri = []
    for d in data:
        if str(d[0]) == id:
            detayveri = list(d)
    return render_template("islemdetay.html", veri=detayveri)


@app.route("/islemedit/<string:id>", methods=["GET", "POST"])
def islemedit(id):
    if request.method == "POST":
        id = request.form["id"]
        gelir = request.form["gelir"]
        gider = request.form["gider"]
        year = request.form["year"]
        kategori = request.form["kategori"]
        toplam = int(request.form["gelir"])-int(request.form["gider"])
        print("Guncellenecek Veriler : ", gelir, gider, year,kategori,toplam)
        veriGuncelle(id, gelir, gider, year,kategori,toplam)
        return redirect(url_for("veriler"))
    else:
        guncellenecekveri = []
        for d in data:
            if str(d[0]) == id:
                guncellenecekveri = list(d)
        return render_template("islemedit.html", veri=guncellenecekveri)


@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/islemler", methods=["POST", "GET"])
def islemadd():
    if request.method == "POST":
        gelir = request.form["gelir"]
        gider = request.form["gider"]
        year = request.form["year"]
        kategori = request.form["kategori"]
        toplam = int(request.form["gelir"])-int(request.form["gider"])

        print("Eklenecek Veriler : ", gelir, gider, year,kategori,toplam)
        veriEkle(gelir, gider, year,kategori,toplam)
       

    return render_template("islemler.html")


@app.route("/veriler")
def veriler():
    veriAl()
    return render_template("veriler.html", veri=data)


@app.route("/islemdelete/<string:id>")
def islemdelete(id):
    veriSil(id)
    return redirect(url_for("veriler"))


if __name__ == "__main__":
    app.run(debug=True)
