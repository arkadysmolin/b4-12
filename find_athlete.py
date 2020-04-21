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

class Atletes(Base): # структура базы атлетов
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

class User(Base): # структура базы пользователей
    __tablename__ = 'user'
    id = sa.Column(sa.String(36), primary_key=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.Float)

def find_user(user_id, session): # поиск пользователя по id
    user = session.query(User).filter(User.id == user_id).first()
    if user:
    	print ("Найден пользователь: ",user.first_name, user.birthdate, user.height)
    else: # если пользователь не найден
    	user = None;
    return user

def convert_birth_date(db_str): # переводим строчное значение даты в дату
	bd_parts_str = db_str.split("-")
	bd = datetime.date(int(bd_parts_str[0]), int(bd_parts_str[1]), int(bd_parts_str[2]))
	return bd

def nearest_atlet(user, session):	# поиск подходящих атЛетов
	atlets_list = session.query(Atletes).all()

	user_height = user.height
	min_different_in_height=9
	atlet_id_h = None

	user_bd = convert_birth_date(user.birthdate) # переводим строчное значение даты в дату для юзера
	min_different_in_bd=None
	atlet_id_bd = None

	for atlet in atlets_list: # перебираем все записи с атлетами
		atlet_id, atlet_h, atlet_bd = atlet.id, atlet.height, atlet.birthdate
		if atlet_h is not None: # если у атлета указан рост
			if abs(atlet_h-user_height)<min_different_in_height: # сравниваем разницу в дате рождения с минимальной
				min_different_in_height=abs(atlet_h-user_height) 
				atlet_id_h=atlet_id
		
		if atlet_bd is not None: # если у атлета не указано дата рождения
			atlet_bd_date=convert_birth_date(atlet_bd) # переводим строчное значение даты в дату для атлета
			if min_different_in_bd is None: # если минимальная разница в дате рождения ещё отсутствует
				min_different_in_bd=abs(atlet_bd_date-user_bd)
			if abs(atlet_bd_date-user_bd)<min_different_in_bd: # сравниваем разницу в росте с минимальной
				min_different_in_bd=abs(atlet_bd_date-user_bd)
				atlet_id_bd=atlet_id

	return atlet_id_h, atlet_id_bd




def main():
    session = connect_db() # устанавливаем сессию
    qty=session.query(User).count() # считаем количество пользователей
    print ("Введи идентификатор (от 6 до {}): ".format(qty+5))
    user_id_input = input() 
    if not user_id_input.isdigit(): # проверяем, что ввели цифровые значения
    	print("Не хочешь - как хочешь!")
    else:
	    user_id_input_int=int(user_id_input) # переводим строку в число
	    user = find_user(user_id_input_int, session) # ищем пользователя
	    if not user: # если пользователи нет
	    	print("Такого пользователя нет!\n Обрати внимание на доступные идентификаторы.")
	    else:
		    bd_date=convert_birth_date(user.birthdate) # конвертируем строку в дату

		    nearest_atlets = nearest_atlet(user,session) # ищем подходящих атлетов

		    atlet_h=session.query(Atletes).filter(Atletes.id == nearest_atlets[0]).first() # этот подошел по росту
		    print ("Подходящий атлет по росту: \n id - {} \n имя - {} \n рост - {}".format(atlet_h.id, atlet_h.name, atlet_h.height))

		    atlet_bd=session.query(Atletes).filter(Atletes.id == nearest_atlets[1]).first() # этот подошел по дате рождения
		    print ("Подходящий атлет по дате рождения: \n id - {} \n имя - {} \n дата рождения- {}".format(atlet_bd.id, atlet_bd.name, atlet_bd.birthdate))




if __name__ == "__main__":
    main()

















