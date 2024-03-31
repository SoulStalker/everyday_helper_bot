from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey
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


class Purchases(Base):
    __tablename__ = 'od_purchase'

    id = Column(Integer, primary_key=True)
    cash_operation = Column(Integer)  # Кассовая операция (0 или null - приход/ 1 - расход)
    operationtype = Column(Integer)   # Тип операции (продажа(true) / возврат(false))
    checksumstart = Column(Integer)   # Сумма чека с налогами, в "копейках"
    checksumend = Column(Integer)     # Сумма чека с налогами - с учетом скидок, в "копейках"
    checkstatus = Column(Integer)
    id_shift = Column(ForeignKey('od_shift.id'))




