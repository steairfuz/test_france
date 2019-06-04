from django.http import HttpResponse
from django.shortcuts import render
from . import mes_forms
from mes_models.une_ville import VilleInfo, VillesSimilaires, je_garde
from mes_models.mes_evenements import ajout_dun_evenement

from django.views.generic.edit import FormView


# Cette page est affichée lorsqu'il y a une erreur un peu comme 404
def _page_reessayer():
    return HttpResponse('<h1>Désolé, veuillez réessayer !!</h1>')


# spécialement conçu pour afficher les pages principales de test 1 et test 2
def __common_doc(num):
    return 'test{num}/principale.html'.format(num=num)


# page principale lorsque le projet est lancé
def principale(la_requete):
    return render(la_requete, 'commun/principale.html')


# cette fonction affiche la page pricipale du test1
def test1(la_requete):
    return render(la_requete, __common_doc(1), {'rech_champ': mes_forms.FormRechercheVille()})


# cette fonction nous permet de chager la page du test2
def test2(la_requete, lien='validation-evenement/', chemin=__common_doc(2), bon=True, autres_info=""):
    return render(la_requete, chemin, {'notre_form': mes_forms.FormDevenement1(),
                                       'heure_form': mes_forms.FormDevenement2(),
                                       'titre': "référencement d'événement".upper(),
                                       'pointe_sur': lien,
                                       'bon': bon,
                                       'autres_info': autres_info})


# cette nous permet d'afficher les info sur une ville (test1)
def info_sur_une_ville(la_requete):
    if 'parm_ville' in la_requete.POST:
        maville = VilleInfo(la_requete.POST['parm_ville'], je_garde.get_liste())
        return render(la_requete, 'test1/info_sur_ville.html', {'uneville': maville})
    else:
        return HttpResponse('<h1>Désolé, veuillez réessayer !!</h1>')


# cette fonction affiche la page test2 en rechargeant ajoutant des éléments dans le bloc "information_apres_validation"
# (si l'enregistrement de l'evenement s'est bien déroulé ou pas)
def valider_evenement(la_requete):
    # si il y'a <titre_evenement> alors les autres paramètres sont présents
    if 'titre_evenement' in la_requete.POST:
        cest_bon, autres_info = ajout_dun_evenement(_titre=la_requete.POST['titre_evenement'],
                                                    _description=la_requete.POST['descrip_evenement'],
                                                    _date=[la_requete.POST['date_evenement_year'],
                                                           la_requete.POST['date_evenement_month'],
                                                           la_requete.POST['date_evenement_day']],
                                                    _heure_debut=[la_requete.POST['heure_start1'],
                                                                  la_requete.POST['minut_start1']
                                                                  ],
                                                    _heure_fin=[la_requete.POST['heure_start2'],
                                                                la_requete.POST['minut_start2']])
        return test2(la_requete,
                     lien='./',
                     chemin='test2/apres_validation.html',
                     bon=cest_bon,
                     autres_info=autres_info)
    else:
        return _page_reessayer()


class RechercheAuto(FormView):
    """
    Cette classe est appelée lors de la recherche d'une ville
    """
    def get(self, la_requete, *args, **kwargs):
        # 'term' est un paramètre par défaut envoyé par l'autocomplementation de Jquery
        if 'term' in la_requete.GET:
            par_ville = la_requete.GET.get("term")
            villes_semblables = VillesSimilaires(par_ville).get_ville_similaire()
            return HttpResponse(villes_semblables, 'application/json')
        else:
            return _page_reessayer()
