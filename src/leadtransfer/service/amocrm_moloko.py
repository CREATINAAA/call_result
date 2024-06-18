from django.conf import settings
from django.core.mail import send_mail

from ..facades.amocrm import AmocrmAPI


TOKEN_FILENAME = 'moloko_refresh_token.txt'


amo_crm_api = AmocrmAPI(
    settings.AMO_MOLOKO_INTEGRATION_SUBDOMAIN,
    settings.AMO_MOLOKO_INTEGRATION_CLIENT_ID,
    settings.AMO_MOLOKO_INTEGRATION_CLIENT_SECRET,
    settings.AMO_MOLOKO_INTEGRATION_CODE,
    settings.AMO_MOLOKO_INTEGRATION_REDIRECT_URI,
    TOKEN_FILENAME
)


def get_contact_id_by_lead_id(lead_id: str):
    response = amo_crm_api.get_request(f"leads/{lead_id}/links").json()
    links = response.get("_embedded", {}).get("links", [])
    if links:
        for link in links:
            if link.get("to_entity_type", "") == "contacts":
                return link.get("to_entity_id", "")
    return ""


def get_contact_by_id(contact_id: str):
    return amo_crm_api.get_request(f"contacts/{contact_id}").json()


def _get_phone_number(contact_data):
    custom_fields = contact_data.get("custom_fields_values", [])
    for field in custom_fields:
        if field.get("field_name", "") == "Телефон":
            return field.get("values")[0].get("value", "")
    return ""


def _get_lead_by_id(lead_id: str):
    return amo_crm_api.get_request(f"leads/{lead_id}").json()


def _get_lead_comments(lead_id: str):
    lead_links = amo_crm_api.get_request(f"leads/{lead_id}/links").json()
    company_id = lead_links['_embedded']['links'][1]['to_entity_id']
    company_notes = amo_crm_api.get_request(f"companies/{company_id}/notes").json()
    return [note["params"]["text"] for note in company_notes["_embedded"]["notes"] if "text" in note["params"]]


def handle_deal(lead_id: str, lead_feature):
    lead = _get_lead_by_id(lead_id)
    contact_id = get_contact_id_by_lead_id(lead_id)
    contact_data = get_contact_by_id(contact_id)
    phone_number = _get_phone_number(contact_data)
    lead_name = lead.get("name", "")
    comments = '\n'.join(_get_lead_comments(lead_id))
    tags = lead.get("_embedded", {}).get("tags", [""])[0].get("name")
    mail_message = (f"Имя: {lead_name}\n"
                    f"Телефон: {phone_number}\n"
                    f"ЖК: {tags}\n"
                    f"Результат: {lead_feature}\n"
                    f"Комментарии:\n"
                    f"{comments}")
    send_mail(
        "Авторассылка",
        mail_message,
        settings.EMAIL_HOST_USER,
        settings.EMAIL_RECEIVERS,
        fail_silently=False,
    )
