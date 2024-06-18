from django.conf import settings

from ..facades.amocrm import AmocrmAPI
from . import db
from .validation import ContactCreationData, LeadCreationData


TOKEN_FILENAME = 'refresh_token.txt'
AMO_CONTACT_FIELD_IDS = {
    "phone": 156657,
    "email": 156659,
    "date": 794014,
    "site": 784770,
    "page": 794016,
}
AMO_LEAD_FIELD_IDS = {
    "utm_source": 166045,
    "utm_medium": 166043,
    "utm_campaign": 166047,
    "utm_content": 166051,
    "utm_term": 166049,
    "roistat_visit": 754509,
}
AMO_LEAD_STATUS_ID = 62668613  # Стадия внутри воронки
AMO_LEAD_PIPELINE_ID = 7566897  # Воронка

amo_crm_api = AmocrmAPI(
    settings.AMO_DAIGO_INTEGRATION_SUBDOMAIN,
    settings.AMO_DAIGO_INTEGRATION_CLIENT_ID,
    settings.AMO_DAIGO_INTEGRATION_CLIENT_SECRET,
    settings.AMO_DAIGO_INTEGRATION_CODE,
    settings.AMO_DAIGO_INTEGRATION_REDIRECT_URI,
    TOKEN_FILENAME
)


def get_custom_fields_values(field_ids: dict, data):
    custom_fields_values = []
    data = data.dict()
    for field_name, field_id in field_ids.items():
        custom_fields_values.append({
            "field_id": field_id,
            "values": [{"value": data[field_name]}]
        })
    return custom_fields_values


def get_or_create_contact(validated_data):
    if db.contact_exists(validated_data.phone):
        contact_id = db.get_contact_id_by_phone(validated_data.phone)
    else:
        contact_id = create_contact(validated_data)
        db.create_contact(contact_id=contact_id, phone=validated_data.phone)
    return contact_id


def create_contact(data: ContactCreationData):
    body = [{
        "name": "Идентификация с сайта daigo.ru",
        "custom_fields_values": get_custom_fields_values(AMO_CONTACT_FIELD_IDS, data)
    }]
    return amo_crm_api.post_request(url="contacts", body=body).json()['_embedded']['contacts'][0]['id']


def create_lead(contact_id, data: LeadCreationData):
    body = [{
        "name": "Лид с сайта daigo.ru",
        "pipeline_id": AMO_LEAD_PIPELINE_ID,
        "status_id": AMO_LEAD_STATUS_ID,
        "_embedded": {
            "contacts": [{"id": contact_id}]
        },
        "custom_fields_values": get_custom_fields_values(AMO_LEAD_FIELD_IDS, data)
    }]
    return amo_crm_api.post_request(url="leads", body=body).json()


def send_lead_to_amocrm(contact_validated_data, lead_validated_data):
    contact_id = get_or_create_contact(contact_validated_data)
    create_lead(contact_id, lead_validated_data)
