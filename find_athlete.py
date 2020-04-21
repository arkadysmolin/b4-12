import datetime

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()

def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

class Atletes(Base):
    __tablename__ = 'athelete'
    id = sa.Column(sa.Integer, primary_key=True)
    age = sa.Column(sa.Integer)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.Float)
    weight = sa.Column(sa.Integer)
    name = sa.Column(sa.Text)
    gold_medals = sa.Column(sa.Integer)
    silver_medals = sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    total_medals = sa.Column(sa.Integer)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)

class User(Base):
    __tablename__ = 'user'
    id = sa.Column(sa.String(36), primary_key=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.Float)

def find_user(user_id, session):
    user = session.query(User).filter(User.id == user_id).first()
    if user:
    	print ("Найден пользователь: ",user.first_name, user.birthdate, user.height)
    else:
    	user = None;
    return user

def convert_birth_date(db_str):
	bd_parts_str = db_str.split("-")
	bd = datetime.date(int(bd_parts_str[0]), int(bd_parts_str[1]), int(bd_parts_str[2]))
	return bd

def nearest_atlet(user, session):	
	atlets_list = session.query(Atletes).all()

	user_height = user.height
	min_different_in_height=9
	atlet_id_h = None

	user_bd = convert_birth_date(user.birthdate)
	min_different_in_bd=None
	atlet_id_bd = None

	for atlet in atlets_list:
		atlet_id, atlet_h, atlet_bd = atlet.id, atlet.height, atlet.birthdate
		if atlet_h is not None:
			if abs(atlet_h-user_height)<min_different_in_height:
				min_different_in_height=abs(atlet_h-user_height)
				atlet_id_h=atlet_id
		
		if atlet_bd is not None:
			atlet_bd_date=convert_birth_date(atlet_bd)
			if min_different_in_bd is None:
				min_different_in_bd=abs(atlet_bd_date-user_bd)
			if abs(atlet_bd_date-user_bd)<min_different_in_bd:
				min_different_in_bd=abs(atlet_bd_date-user_bd)
				atlet_id_bd=atlet_id

	return atlet_id_h, atlet_id_bd




def main():
    session = connect_db()
    qty=session.query(User).count()
    print ("Введи идентификатор (от 6 до {}): ".format(qty+5))
    user_id_input = input()
    if not user_id_input.isdigit():
    	print("Не хочешь - как хочешь!")
    else:
	    user_id_input_int=int(user_id_input)
	    user = find_user(user_id_input_int, session)
	    if not user:
	    	print("Такого пользователя нет!\n Обрати внимание на доступные идентификаторы.")
	    else:
		    bd_date=convert_birth_date(user.birthdate)

		    nearest_atlets = nearest_atlet(user,session)

		    atlet_h=session.query(Atletes).filter(Atletes.id == nearest_atlets[0]).first()
		    print ("Подходящий атлет по росту: \n id - {} \n имя - {} \n рост - {}".format(atlet_h.id, atlet_h.name, atlet_h.height))

		    atlet_bd=session.query(Atletes).filter(Atletes.id == nearest_atlets[1]).first()
		    print ("Подходящий атлет по дате рождения: \n id - {} \n имя - {} \n дата рождения- {}".format(atlet_bd.id, atlet_bd.name, atlet_bd.birthdate))




if __name__ == "__main__":
    main()

















