import json

from app import db, Book, Node

def nodos():
    with open("p_scrap/nodos.json", "r") as f:
        nodos = json.loads(f.read())
        for n in nodos:
            reg = Node(pk = int(n), name =nodos[n] )
            db.session.add(reg)
            db.session.commit()
            print("Done " + nodos[n])
def libros():
    with open("p_scrap/libros_V2.json", "r") as f:
        d = json.loads(f.read())

        for book in d:
            if book != "null":
                reg = Book(title=d[book]["title"], author=d[book]["author"], isbn = d[book]["isbn"], asin=d[book]["asin"],
                           publisher=d[book]["publisher"], published=d[book]["published"], url=d[book]["url"], image=d[book]["image"], ean=d[book]["ean"])

                for node in d[book]["nodes"]:
                    n = Node.query.filter_by(pk=node).first()
                    if n:
                        reg.nodes.append(n)
                db.session.add(reg)
                db.session.commit()
                print("Done " + d[book]["title"])

nodos()
libros()
