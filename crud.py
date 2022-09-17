from flask import flash
from models import db
from sqlalchemy import exc


# Funções API CRUD

class Crud():
    def create(self, model, error):
        try:
            db.session.add(model)
            db.session.commit()
            return True
        except exc.IntegrityError:
            db.session.rollback()
            flash(error)
        return False


    def retrieve_one(self, id, ClassModel):
        try:
            query = ClassModel.query.filter_by(id=id).first()
        except:
            flash("Erro na busca")
        return query


    def retrieve_all(self, ClassModel):
        try:
            query = ClassModel.query.all()
        except:
            flash("Erro na busca")
        return query


    def update(self, error):
        try:
            db.session.commit()
            return True
        except exc.IntegrityError:
            db.session.rollback()
            flash(error)
        return False


    def delete(self, model, error):
        try:
            db.session.delete(model)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            flash(error)
        return False