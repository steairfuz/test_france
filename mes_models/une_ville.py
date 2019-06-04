from coreapi import Client, codecs
import json


# cette Classe me permet de garder la liste des dernieres villes envoyées par l'API  durant la recherche
class GardeListe(object):
    def __init__(self):
        self.__tmp_list = None

    def set_last_list(self, new):
        self.__tmp_list = new

    def get_liste(self):
        return self.__tmp_list


# on crée l'objet de recherche lors du chargement de cette vue
# je_garde est exporté dans  le fichiers vues.py,
# But principal: Enregistré le dernier dictionnaire des villes lors de la recherche Autocomplementaire
je_garde = GardeListe()


class VillesSimilaires(object):
    """
    Cette classe est appelée lors de l'autocomplementation d'une ville recherchée
    """

    # on definit l'API (url de base)
    __api_de_base = 'https://geo.api.gouv.fr/'
    # limit du nombre de ville à afficher dens l'autocomplementation
    __limite = 10

    decoders = [
        codecs.CoreJSONCodec(),
        codecs.JSONCodec()
    ]

    def __init__(self, saisi):
        # on enleve toutes les espaces autour de la valeur saisie
        self.__saisi = str(saisi).strip()

    def get_ville_similaire(self):
        if self.__saisi != '':

            try:
                client = Client()  # self.__class__.decoders
                # connexion à l'API
                document = client.get(self.__class__.__api_de_base +
                                      'communes?nom={nom}'
                                      '&fields=population,centre,departement'
                                      '&boost=population'.format(nom=self.__saisi))

                # cette fonction est un générateur qui nous permet de limiter la recherche
                def limit_rech(limit=self.__class__.__limite):
                    num = 0
                    for un in document:
                        yield un
                        num += 1
                        if num >= limit:
                            break
                # création d'une liste des villes récupérées
                les_villes_bruites = [x for x in limit_rech()]
                # Création d'une nouvelle listes avec mes propes clée:id , value , population etc...
                # En gros je reformatte les villes envoyées par l'API
                mes_villes = []
                for myid, value in enumerate(les_villes_bruites):
                    mes_villes.append({'id': myid,
                                       'value': value['nom'],
                                       'population': value['population'],
                                       'longitude': value['centre']['coordinates'][1],
                                       'latitude': value['centre']['coordinates'][0]})
                # cet objet a été crée lors du chargement de ce fichier
                # enregistrement du dictionnaire des villes
                je_garde.set_last_list(mes_villes)
                return json.dumps(mes_villes)
            except Exception as E:
                return ''
        else:
            return ''


class VilleInfo(object):
    """
    Cette classe est appelée pour afficher les informations concernant une ville:
    longitude,latitude,nbre d'habitant,tarif

    - Habitant inférieur à 1000 le prix est de 5€
    - Habitant entre 1000 à 9000 le prix est de 10€
    - Habitant entre 9000 à 30 000 le prix est de 30€
    - Habitant supérieur à 30 000 le prix est de 50€
    """
    def __init__(self, laville, ledictionnaire):
        self._ville = str(laville).strip()
        self._dictionnaire = ledictionnaire

    @staticmethod
    def __creation_du_frmt_de_retour(_ville, _tarif, _long, _lat, _hbt):
        return {'ville': _ville,
                'tarif': _tarif,
                'longitude': _long,
                'Latitude': _lat,
                'habitant': _hbt}

    def get_ville(self):
        return self._ville

    def get_info(self):
        if self._dictionnaire is not None:
            trouver = [x for x in self._dictionnaire if str(x['value']).lower() == str(self._ville).lower()]
            if trouver:
                trouver = trouver[0]
                return self.__creation_du_frmt_de_retour(_ville=trouver['value'],
                                                         _lat=trouver['latitude'],
                                                         _long=trouver['longitude'],
                                                         _hbt=trouver['population'],
                                                         _tarif=self.get_tarif(trouver['population']))
            else:
                return self.__creation_du_frmt_de_retour(self._ville, '--', '--', '--', '--')

        else:
            return self.__creation_du_frmt_de_retour(self._ville, '--', '--', '--', '--')


    @staticmethod
    def get_tarif(nbre_dhabitant):
        prix = 0
        if nbre_dhabitant < 1000:
            prix = 5
        if nbre_dhabitant in range(1000, 9000):
            prix = 10
        if nbre_dhabitant in range(9000, 30000):
            prix = 30
        if nbre_dhabitant > 30000-1:
            prix = 50

        return str(prix)+' €'

    @staticmethod
    def get_not_show_key():
        return ['ville']


if __name__ == '__main__':
    pass