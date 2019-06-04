from django import forms
import datetime


# création du formulaire de recherche
class FormRechercheVille(forms.Form):
    """
    Formulaire permettant de rechercher une ville:
    """
    parm_ville = forms.CharField(label='titre',
                                       max_length=64,
                                       widget=forms.TextInput(attrs={'placeholder': 'Rechercher une ville',
                                                                     'autocomplete': 'off',
                                                                     'class': 'form-control mr-sm-2',
                                                                     'id': "id_rech_ville",
                                                                     'type': "search",
                                                                     "aria-label": "Search",
                                                                     }))


# Création du formulaire d'événement
class FormDevenement1(forms.Form):
    """
    Formulaire permettant de saisir une parties des informations sur un événement:
    titre,description et date
    """
    titre_evenement = forms.CharField(label='Titre',
                                       max_length=100,
                                       widget=forms.TextInput(attrs={'placeholder': 'titre', 'autocomplete': 'off'}))

    descrip_evenement = forms.CharField(label="Description",
                                        widget=forms.Textarea(attrs={"rows":5,
                                                                     "cols":50,
                                                                     'class':'form-control'}))
    # Champ evenement
    date_evenement = forms.DateField(label="Date",
                                     widget=forms.SelectDateWidget(years=[x for x in range(2000, 3000)],
                                                                   attrs={'class': 'btn dropdown-toggle border-dark',
                                                                          'placeholder': 'Date'}),
                                     initial=datetime.datetime.today())


class HeureDerivee(forms.Form):
    """
    cette classe premet de créer un champ de choix composant l'élément primitif des heures dans mon formulaire
    """
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_une_partie_de_lheure(ou='M'):
        return int(datetime.datetime.now().time().strftime('%' + ou))

    @classmethod
    def get_select_field(cls, heure_ou_minute, _label='' ):

        def liste_des_valeurs(nbre):
            return ((str(x), ('0' if len(str(x)) == 1 else '') + str(x)) for x in range(nbre))

        nbre = 1
        if heure_ou_minute == 'H':
            nbre = 24
        elif heure_ou_minute == 'M':
            nbre = 60

        valeur_initiale = cls.get_une_partie_de_lheure(heure_ou_minute)


        return forms.CharField(label=_label,
                               widget=forms.Select(choices=liste_des_valeurs(nbre)),
                               initial=valeur_initiale)





class FormDevenement2(forms.Form):
    """
    Formulaire permettant de saisir la seconde partie des informations sur un événement:
    Heure debut et Heure Fin
    l'heure début est constituée de heure_start1 et de minut_start1
    l'heure Fin est constituée de heure_start2 et de minut_start2
    """

    heure_start1 = HeureDerivee.get_select_field('H', 'heure début')
    minut_start1 = HeureDerivee.get_select_field('M')

    heure_start2 = HeureDerivee.get_select_field('H','heure fin')
    minut_start2 = HeureDerivee.get_select_field('M')

if __name__ == '__main__':
    print(datetime.datetime.now().time().strftime('%M'))



