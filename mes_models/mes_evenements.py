import pytz
from os import path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import datetime


SCOPES = ['https://www.googleapis.com/auth/calendar']
CALENDAR_ID = 'kokouvi.sewoavi@gmail.com'
TIME_ZONE = 'Europe/Paris'
API_SERVICE_NAME = 'calendar'
API_VERSION = 'v3'
NOM_DU_FIC_AUTISATION = 'lecredit_en_fichier.json'


# le building de la connexion est effectuée dans cet décorateur
def deco_pour_la_compilation(fn):
    def couverture(args):
        return build(API_SERVICE_NAME, API_VERSION, credentials=fn(args))
    return couverture


# connexion via le console (pour certains test)
@deco_pour_la_compilation
def autorisation_console(chemin_du_fichier):
    flow = InstalledAppFlow.from_client_secrets_file(chemin_du_fichier, SCOPES)
    credentials = flow.run_console()
    return credentials


# connexion dans le navigateur
@deco_pour_la_compilation
def autorisation_direct(chemin_du_fichier):

    credential_path = path.join(path.dirname(path.abspath(__file__)), 'le_token.json')
    store = Storage(credential_path)
    credentials = store.get()
    # en gros s'il n ya pas le fichier d'autirisation tente de le récupérer et de l'enregistrer
    if not credentials:
        flow = client.flow_from_clientsecrets(chemin_du_fichier, SCOPES)
        credentials = tools.run_flow(flow, store)
    return credentials


def ajout_dun_evenement(_titre, _description, _date, _heure_debut, _heure_fin):
    """ permet d'ajouter un evenement a Google Calendar"""
    try:

        def fact_date(heure):
            zone_ = pytz.timezone(TIME_ZONE)
            return zone_.localize(datetime.datetime(_date[0],
                                                    _date[1],
                                                    _date[2],
                                                    heure[0],
                                                    heure[1]))

        # convertion en entier
        _date = [int(x) for x in _date]
        _heure_debut = [int(x) for x in _heure_debut]
        _heure_fin = [int(x) for x in _heure_fin]
        # convertion de la date en chaine
        date_debut = fact_date(heure=_heure_debut)
        date_fin = fact_date(heure=_heure_fin)
        chemin_complet = path.join(path.dirname(path.abspath(__file__)), 'client_secret_key.json')
        service = autorisation_direct(chemin_complet)
        # result = service.calendarList().list().execute()
        # id_du_calendrier = result['items'][0]['id']
        un_evenement = {
          'summary': _titre,
          'description': _description,
          'start': {
            'dateTime': date_debut.isoformat(),
            'timeZone': TIME_ZONE,
          },
          'end': {
            'dateTime': date_fin.isoformat(),
            'timeZone': TIME_ZONE,
          },
        }
        event = service.events().insert(calendarId=CALENDAR_ID,
                                        body=un_evenement).execute()
        return True, event.get('htmlLink')
    except Exception as E:
        return False, str(E)

if __name__ == '__main__':
    ajout_dun_evenement('Test kokouvi', 'test', [2019, 6, 4], [15, 0], [16, 0])

