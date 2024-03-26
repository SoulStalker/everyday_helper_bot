from sqlalchemy import Column, Integer, String, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Shifts(Base):
    __tablename__ = 'od_shift'

    id = Column(Integer, primary_key=True)
    shopindex = Column(Integer)  # Номер магазина
    cashnum = Column(Integer)  # Номер кассы
    numshift = Column(Integer)  # Номер смены
    operday = Column(Date)  # Операционный День (ОД), к которому относится данная смена
    state = Column(Integer)  # Состояние смены (0/1/2/3 = открыта/закрыта/закрыта с учетом фисказизирующего документа/закрыта с расхождениями)
    inn = Column(String)  # ИНН Юрика
