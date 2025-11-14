from datetime import datetime
from sys import exc_info
import asyncio

from database import get_records, search_records_by_status, create_record, change_record_status_by_id
from logs import log_info, log_debug, log_warning, log_error
from schemas.incidents import IncidentSchema, IncidentGetSchema, ResponseMessage

from fastapi import APIRouter, HTTPException


router = APIRouter()


@router.get(path="/incidents", tags=['Инциденты'], summary='Получить все записи инцидентов.')
async def read_incidents() -> list[IncidentGetSchema] | ResponseMessage:
    log_info(message='Проводится запрос на получение всех записей инцидентов из БД.')
    try:
        records = await get_records()
        result_records = list()
        if records:
            for record in records:
                result_records.append({
                    "id_record": record[0], 
                    "description": record[1],
                    "status": record[2],
                    "source": record[3],
                    "date_create": record[4],
                    })
        log_info(message='Запрос на получение всех записей инцидентов из БД прошел успешно.')
        log_debug(message=f'Все записи инцидентов из БД:\n{result_records}')
        if result_records:
            return result_records

        return {"success": True, "message": "В базе данных нет записей инцидентов."}

    except Exception as e:
        exc_type, exc_obj, exc_tb = exc_info()
        log_error(message=e, module_name=exc_tb.tb_frame.f_code.co_filename.split('/')[-1], line_no=exc_tb.tb_lineno)
        raise HTTPException(status_code=500, detail='Внутреняя ошибка сервера.')


@router.get(path="/incidents/{status}", tags=['Инциденты'], summary='Найти записи инцидентов по статусу.')
async def get_incidents_by_status(status:int) -> list[IncidentGetSchema]:
    log_info(message=f'Проводится запрос на получение всех записей инцидентов из БД соответствующих статусу = {status}.')
    try:
        log_debug(message=f'Проводится запрос на получение всех записей инцидентов из БД соответствующих статусу = {status}.')
        status = int(status)
        records = await search_records_by_status(status)
        if records:
            result_records = list()
            for record in records:
                result_records.append({
                    "id_record": record[0], 
                    "description": record[1],
                    "status": record[2],
                    "source": record[3],
                    "date_create": record[4],
                    })
            log_info(message='Запрос на получение всех записей инцидентов из БД соответствующих статусу = {status} прошел успешно.')
            log_debug(message=f'Все записи инцидентов соответствующих статусу = {status}: {result_records}')
            return result_records
                
        log_warning(message=f'Инциденты по статусу = {status} не были найдены.')
        raise HTTPException(status_code=404, detail='Инциденты по этому статусу не были найдены.')
    
    except Exception as e:
        if isinstance(e, HTTPException) and e.status_code == 404:
            raise e
        
        exc_type, exc_obj, exc_tb = exc_info()
        log_error(message=e, module_name=exc_tb.tb_frame.f_code.co_filename.split('/')[-1], line_no=exc_tb.tb_lineno)
        raise HTTPException(status_code=500, detail='Внутреняя ошибка сервера.')


@router.post(path="/incidents", tags=['Инциденты'], summary='Добавить запись инцидента.')
async def create_incident(new_incident: IncidentSchema) -> ResponseMessage:
    log_info(message='Проводится запрос на добавление записи инцидента в БД.')
    try:
        description = new_incident.description
        status = new_incident.status
        source = new_incident.source
        date = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
        body_request = ({ 
                    "description": description,
                    "status": status,
                    "source": source,
                    "date_create": date,
                    })
        log_debug(message=f'Тело запроса на добавление записи инцидента в БД:\n{body_request}')
        await create_record(description=description, status=status, source=source, date=date)
        log_info(message='Запрос на добавление записи инцидента в БД прошел успешно.')
        return {"success": True, "message": "Инцидент успешно добавлен."}

    except Exception as e:
        exc_type, exc_obj, exc_tb = exc_info()
        log_error(message=e, module_name=exc_tb.tb_frame.f_code.co_filename.split('/')[-1], line_no=exc_tb.tb_lineno)
        raise HTTPException(status_code=500, detail='Внутреняя ошибка сервера.')


@router.put(path="/incidents/{id_record}/{status}", tags=['Инциденты'], summary='Изменить статус инцидента по id.')
async def change_incident_status(id_record: int, status:int) -> ResponseMessage:
    log_info(message=f'Проводится запрос на изменение статуса записи инцидента по id = {id_record} в БД.')
    try:
        log_debug(message=f'Проводится запрос на изменение статуса записи инцидента по id = {id_record} на статус = {status} в БД.')
        status = int(status)
        is_record = await change_record_status_by_id(id_record=id_record, status=status)
        if is_record:
            log_info(message=f'Запрос на изменение статуса записи инцидента по id = {id_record} в БД прошел успешно.')
            return {"success": True, "message": "Статус инцидента успешно изменен."}

        log_warning(message=f'Инциденты по id = {id_record} не были найдены.')
        raise HTTPException(status_code=404, detail='Инциденты по этому id не были найдены.')

    except Exception as e:
        if isinstance(e, HTTPException) and e.status_code == 404:
            raise e
        
        exc_type, exc_obj, exc_tb = exc_info()
        log_error(message=e, module_name=exc_tb.tb_frame.f_code.co_filename.split('/')[-1], line_no=exc_tb.tb_lineno)
        raise HTTPException(status_code=500, detail='Внутреняя ошибка сервера.')