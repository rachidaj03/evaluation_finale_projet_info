from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.conf import settings
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from .models import clie
import json
import hashlib
import requests 
from django.http import JsonResponse 
from .models import Events 
from django.db.models.functions import Cast,Coalesce, ExtractMonth, ExtractYear
from django.db.models import IntegerField, FloatField
from django.db.models import Count
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db.models import Sum, F


def home(request):
    return render(request,"authentification/signin.html")
def suivi_ventes(request):
    cli = clie.objects.filter(confirme_etat=1)
    clients_per_year = (
        cli.annotate(month=ExtractMonth('date_ajout'), year=ExtractYear('date_ajout')).values('year', 'month').annotate(num_clients=Coalesce(Cast(Sum('revenu_espere'),IntegerField()), 0)).order_by('year', 'month'))
    result_list = [0] * 12
    for entry in clients_per_year:
        month_index = entry['month'] - 1  
        result_list[month_index] = entry['num_clients']
    return render(request,"authentification/suivi_ventes.html",{'clie':clie,'pry':result_list})
def user_profile(request):
    eve=Events.objects.all()
    cli=clie.objects.all()
    clients_per_year = (
        clie.objects.annotate(month=ExtractMonth('date_ajout'), year=ExtractYear('date_ajout')).values('year', 'month').annotate(num_clients=Count('id')).order_by('year', 'month'))
    result_list = [0] * 12
    for entry in clients_per_year:
        month_index = entry['month'] - 1 
        result_list[month_index] = entry['num_clients']
    return render(request,"authentification/user-profile.html",{'eve':eve,'clie': cli,'pry':result_list})
def signin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
    if user is not None:
        login(request, user)
        return redirect('user_profile')
    else :
        return render(request,"authentification/error_auth.html")
 
#@login_required(login_url='')
def gestion_clientele(request):
    cli = clie.objects.all()
    return render(request,"authentification/gestion_clientele.html",{'clie': cli})
def interactions(request):
    cli = clie.objects.all()
    return render(request,"authentification/interactions.html",{'clie': cli})
def create_new_object_1(request):
    if request.method=='POST':
        nom = request.POST.get('nom')
        num_tel = int(request.POST.get('num'))
        entreprise = request.POST.get('entreprise')
        siteweb =request.POST.get('siteweb')
        adresse_rue=request.POST.get('adresse_rue')
        adresse_ville=request.POST.get('adresse_ville')
        adresse_pays=request.POST.get('adresse_pays')
        adresse_etat=request.POST.get('adresse_etat')
        adresse_code=request.POST.get('adresse_code')
        if (adresse_code==''):
            adresse_code=None
        nom_poste=request.POST.get('nom_poste')
        campagne=request.POST.get('campagne')
        revenu_espere=request.POST.get('revenu_espere')
        probabilite=request.POST.get('probabilité')
        if (probabilite==''):
            probabilite=None
        vendeur=request.POST.get('vendeur')
        date_cloture=request.POST.get('date_cloture')
        if (date_cloture==''):
            date_cloture=None
        else:
            date_cloture=datetime.strptime(date_cloture, "%Y-%m-%d")
        date_ajout=datetime.now()
        facebook=request.POST.get('facebook')
        email=request.POST.get('email')
        client = clie(nom=nom, num_tel=num_tel,entreprise=entreprise,siteweb=siteweb,adresse_rue=adresse_rue,adresse_ville=adresse_ville,adresse_pays=adresse_pays,adresse_etat=adresse_etat,adresse_code=adresse_code,nom_poste=nom_poste,campagne=campagne,revenu_espere=revenu_espere,probabilité=probabilite,vendeur=vendeur,date_cloture=date_cloture,piste_etat=1,oppor_etat=0,confirme_etat=0,date_ajout=date_ajout,statut_oppor=0,facebook=facebook,email=email,etat="En cours")
        client.save()
    return redirect('gestion_clientele')
def remove_object_3(request):
    if request.method=='POST':
        id=request.POST.get('id_item_14') 
        obj = clie.objects.get(id=id)
        obj.statut_oppor=1
        obj.save()
    return redirect('gestion_clientele')
def remove_object_4(request):
    if request.method=='POST':
        id=request.POST.get('id_item_14') 
        obj = clie.objects.get(id=id)
        obj.delete()
    return redirect('interactions')
def transition_1(request):
    if request.method=='POST':
        id=request.POST.get('item_4') 
        obj = clie.objects.get(id=id)
        obj.oppor_etat=0
        obj.confirme_etat=1
        obj.etat="En cours"
        obj.save()
    return redirect('gestion_clientele')
def transition_2(request):
    if request.method=='POST':
        id=request.POST.get('item_5') 
        obj = clie.objects.get(id=id)
        obj.piste_etat=0
        obj.oppor_etat=1
        obj.etat="Gagnée"
        obj.save()
    return redirect('gestion_clientele')
def modifier_3(request):
    if request.method=='POST':
        id=request.POST.get('item_15') 
        obj = clie.objects.get(id=id)
        nom = request.POST.get('nom_15')
        num_tel = int(request.POST.get('num_15'))
        entreprise = request.POST.get('entreprise_15')
        siteweb =request.POST.get('siteweb_15')
        adresse_rue=request.POST.get('adresse_rue_15')
        adresse_ville=request.POST.get('adresse_ville_15')
        adresse_pays=request.POST.get('adresse_pays_15')
        adresse_etat=request.POST.get('adresse_etat_15')
        adresse_code=request.POST.get('adresse_code_15')
        nom_poste=request.POST.get('nom_poste_15')
        campagne=request.POST.get('campagne_15')
        revenu_espere=request.POST.get('revenu_espere_15')
        probabilite=request.POST.get('probabilité_15')
        vendeur=request.POST.get('vendeur_15')
        date_cloture=request.POST.get('date_cloture_15')
        facebook=request.POST.get('facebook_15')
        email=request.POST.get('email_15')
        if (nom=='None'):
            nom=None
        if (num_tel=='None'):
            num_tel=None
        if (entreprise=='None'):
            entreprise=None
        if (siteweb=='None'):
            siteweb=None
        if (adresse_code=='None' or adresse_code==''):
            adresse_code=None
        if (adresse_etat=='None'):
            adresse_etat=None
        if (adresse_pays=='None'):
            adresse_pays=None
        if (adresse_ville=='None'):
            adresse_ville=None
        if (adresse_rue=='None'):
            adresse_rue=None
        if (nom_poste=='None'):
            nom_poste=None
        if (campagne=='None'):
            campagne=None
        if (revenu_espere=='None'):
            revenu_espere=None
        if (probabilite=='None' or probabilite==''):
            probabilite=None
        if (vendeur=='None'):
            vendeur=None
        if (facebook=='None'):
            facebook=None
        if (email=='None'):
            email=None
        if (date_cloture=='None' or date_cloture==''):
            date_cloture=None
        else:
            date_cloture=datetime.strptime(date_cloture, "%Y-%m-%d")
        obj.date_cloture=date_cloture
        obj.nom=nom
        obj.num_tel=num_tel
        obj.entreprise=entreprise
        obj.siteweb=siteweb
        obj.adresse_rue=adresse_rue
        obj.adresse_code=adresse_code
        obj.adresse_ville=adresse_ville
        obj.adresse_pays=adresse_pays
        obj.adresse_etat=adresse_etat    
        obj.nom_poste=nom_poste
        obj.probabilité=probabilite
        obj.campagne=campagne
        obj.revenu_espere=revenu_espere
        obj.vendeur=vendeur
        obj.facebook=facebook
        obj.email=email
        obj.save()
    return(redirect(gestion_clientele))
def modifier_4(request):
    if request.method=='POST':
        id=request.POST.get('item_15') 
        obj = clie.objects.get(id=id)
        nom = request.POST.get('nom_15')
        num_tel = int(request.POST.get('num_15'))
        entreprise = request.POST.get('entreprise_15')
        siteweb =request.POST.get('siteweb_15')
        adresse_rue=request.POST.get('adresse_rue_15')
        adresse_ville=request.POST.get('adresse_ville_15')
        adresse_pays=request.POST.get('adresse_pays_15')
        adresse_etat=request.POST.get('adresse_etat_15')
        adresse_code=request.POST.get('adresse_code_15')
        nom_poste=request.POST.get('nom_poste_15')
        campagne=request.POST.get('campagne_15')
        revenu_espere=request.POST.get('revenu_espere_15')
        probabilite=request.POST.get('probabilité_15')
        vendeur=request.POST.get('vendeur_15')
        date_cloture=request.POST.get('date_cloture_15')
        facebook=request.POST.get('facebook_15')
        email=request.POST.get('email_15')
        if (nom=='None'):
            nom=None
        if (num_tel=='None'):
            num_tel=None
        if (entreprise=='None'):
            entreprise=None
        if (siteweb=='None'):
            siteweb=None
        if (adresse_code=='None' or adresse_code==''):
            adresse_code=None
        if (adresse_etat=='None'):
            adresse_etat=None
        if (adresse_pays=='None'):
            adresse_pays=None
        if (adresse_ville=='None'):
            adresse_ville=None
        if (adresse_rue=='None'):
            adresse_rue=None
        if (nom_poste=='None'):
            nom_poste=None
        if (campagne=='None'):
            campagne=None
        if (revenu_espere=='None'):
            revenu_espere=None
        if (probabilite=='None' or probabilite==''):
            probabilite=None
        if (vendeur=='None'):
            vendeur=None
        if (facebook=='None'):
            facebook=None
        if (email=='None'):
            email=None
        if (date_cloture=='None' or date_cloture==''):
            date_cloture=None
        else:
            date_cloture=datetime.strptime(date_cloture, "%Y-%m-%d")
        obj.date_cloture=date_cloture
        obj.nom=nom
        obj.num_tel=num_tel
        obj.entreprise=entreprise
        obj.siteweb=siteweb
        obj.adresse_rue=adresse_rue
        obj.adresse_code=adresse_code
        obj.adresse_ville=adresse_ville
        obj.adresse_pays=adresse_pays
        obj.adresse_etat=adresse_etat    
        obj.nom_poste=nom_poste
        obj.probabilité=probabilite
        obj.campagne=campagne
        obj.revenu_espere=revenu_espere
        obj.vendeur=vendeur
        obj.facebook=facebook
        obj.email=email
        obj.save()
    return(redirect(interactions))
def modifier_5(request):
    if request.method=='POST':
        id=request.POST.get('item_15') 
        obj = clie.objects.get(id=id)
        nom = request.POST.get('nom_15')
        num_tel = int(request.POST.get('num_15'))
        entreprise = request.POST.get('entreprise_15')
        siteweb =request.POST.get('siteweb_15')
        adresse_rue=request.POST.get('adresse_rue_15')
        adresse_ville=request.POST.get('adresse_ville_15')
        adresse_pays=request.POST.get('adresse_pays_15')
        adresse_etat=request.POST.get('adresse_etat_15')
        adresse_code=request.POST.get('adresse_code_15')
        nom_poste=request.POST.get('nom_poste_15')
        campagne=request.POST.get('campagne_15')
        revenu_espere=request.POST.get('revenu_espere_15')
        probabilite=request.POST.get('probabilité_15')
        vendeur=request.POST.get('vendeur_15')
        date_cloture=request.POST.get('date_cloture_15')
        facebook=request.POST.get('facebook_15')
        email=request.POST.get('email_15')
        if (nom=='None'):
            nom=None
        if (num_tel=='None'):
            num_tel=None
        if (entreprise=='None'):
            entreprise=None
        if (siteweb=='None'):
            siteweb=None
        if (adresse_code=='None' or adresse_code==''):
            adresse_code=None
        if (adresse_etat=='None'):
            adresse_etat=None
        if (adresse_pays=='None'):
            adresse_pays=None
        if (adresse_ville=='None'):
            adresse_ville=None
        if (adresse_rue=='None'):
            adresse_rue=None
        if (nom_poste=='None'):
            nom_poste=None
        if (campagne=='None'):
            campagne=None
        if (revenu_espere=='None'):
            revenu_espere=None
        if (probabilite=='None' or probabilite==''):
            probabilite=None
        if (vendeur=='None'):
            vendeur=None
        if (facebook=='None'):
            facebook=None
        if (email=='None'):
            email=None
        if (date_cloture=='None' or date_cloture==''):
            date_cloture=None
        else:
            date_cloture=datetime.strptime(date_cloture, "%Y-%m-%d")
        obj.date_cloture=date_cloture
        obj.nom=nom
        obj.num_tel=num_tel
        obj.entreprise=entreprise
        obj.siteweb=siteweb
        obj.adresse_rue=adresse_rue
        obj.adresse_code=adresse_code
        obj.adresse_ville=adresse_ville
        obj.adresse_pays=adresse_pays
        obj.adresse_etat=adresse_etat    
        obj.nom_poste=nom_poste
        obj.probabilité=probabilite
        obj.campagne=campagne
        obj.revenu_espere=revenu_espere
        obj.vendeur=vendeur
        obj.facebook=facebook
        obj.email=email
        obj.save()
    return(redirect(user_profile))

def calendar(request):  
    all_events = Events.objects.all()
    context= {
        "events":all_events,
    }
    return render(request,'authentification/calendar.html',context)
 
def all_events(request):                                                                                                 
    all_events = Events.objects.all()                                                                                    
    out = []                                                                                                             
    for event in all_events:                                                                                             
        out.append({                                                                                                     
            'title': event.name,                                                                                         
            'id': event.id,                                                                                              
            'start': event.start.strftime("%m/%d/%Y, %H:%M:%S"),                                                         
            'end': event.end.strftime("%m/%d/%Y, %H:%M:%S"), 
            'client':event.client.nom,                                                            
        })                                                                                                               
                                                                                                                      
    return JsonResponse(out, safe=False) 
 
def add_event(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    client = int(request.GET.get("client",None))
    per=clie.objects.get(id=client)
    event = Events(name=str(title), start=start, end=end, client=per)
    event.save()
    data = {}
    return JsonResponse(data)
 
def update(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.start = start
    event.end = end
    event.name = title
    event.save()
    data = {}
    return JsonResponse(data)
 
def remove(request):
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.delete()
    data = {}
    return JsonResponse(data)

@csrf_exempt
def webhook(request):
    if request.method == 'GET':
        hub_challenge = request.GET.get('hub.challenge')
        hub_verify_token = request.GET.get('hub.verify_token')
        if hub_verify_token == '123456789':
            return HttpResponse(hub_challenge)
        else:
            return HttpResponseForbidden('Invalid verify token')
        
def post_message_1(request):
    if request.method == 'POST':
        data = request.POST.get("msg")
        id = request.POST.get("item_11")
        obj = clie.objects.get(id=id)
        #fb_id=obj.facebook
        fb_id=100007717876772
        PAGE_ACCESS_TOKEN="EAAMxnXT04PYBO09b0JFQTZBzqoJJ8C9GgoSJ4G3QT0xeHyu66jKszeZAakoaXTgqcYbFXFXYOsRCMJW7cNnfIRPyQCF2JpNBQvFEbgCZCEFLvZCXYrLoegAKv5ZB8zWb5NpifQZBOgA3ZASQwEFpwHegqDKfXnT2ZBOmtgOd0hBBhMWLwU06yOHNDrsLoBHYwpTG"
        params = {'access_token': PAGE_ACCESS_TOKEN,'recipient': json.dumps({'id': fb_id}),'message': json.dumps({'text': data})}
        headers = {'Content-type': 'application/json'}
        r = requests.post('https://graph.facebook.com/v18.0/144042592135822/messages', params=params, headers=headers)
        return redirect (gestion_clientele)
def post_message(request):
    page_id='144042592135822'
    page_access_token = 'EAAMxnXT04PYBO3xZCZAGbIjiCJThECRROySWMXGED1RQpZAwMowZArb1cXJb6WGmmKyBHgYgUYlo0aPv7BGZAIr3Mg5ZCBIkskuU0jUZClP5ANljta9TO6vZAWH18yJhZCdtESVb8MS0E52HRHTOb4DjRZB5OZBJrMfPTCmZC2eRkhjl4bkZAf0ZASjJUKnDBdBun4WF257Ruww6TP'
    url = 'https://graph.facebook.com/v18.0/'
    msg_url = url + page_id + '/messages'
    param = dict()
    param['recipient'] = str({'id': int(107926957267156)})
    response = requests.post(url=msg_url, params=param)
    response = response.json()
    return HttpResponse("sent")
def send_message(request):
    data = request.POST.get("msg")
    id = request.POST.get("item_11")
    obj = clie.objects.get(id=id)
    mail=obj.email
    my_subject = "Welcome" +" "+ obj.nom+" "+data
    welcome_message = "Welcome"
    link_app = "http://localhost:8000"
    context = {"welcome_message": welcome_message, "link_app": link_app}
    html_message = render_to_string("authentification/email.html", context=context)
    plain_message = strip_tags(html_message)
    message = EmailMultiAlternatives(
           subject = my_subject, 
            body = plain_message,
            from_email = None ,
            to= [mail]
        )
    message.attach_alternative(html_message, "text/html")
    message.send()
    return(redirect(gestion_clientele))