from django.db import models

class clie(models.Model):
    nom=models.CharField(max_length=100,db_column='nom')
    num_tel=models.IntegerField(db_column='num_tel')
    email=models.EmailField(db_column='mail')
    entreprise=models.CharField(max_length=100,db_column='entreprise')
    siteweb=models.CharField(max_length=100,db_column='siteweb')
    adresse_rue=models.CharField(max_length=100,db_column='adresse_rue')
    adresse_ville=models.CharField(max_length=100,db_column='adresse_ville')
    adresse_pays=models.CharField(max_length=100,db_column='adresse_pays')
    adresse_etat=models.CharField(max_length=100,db_column='adresse_etat')
    adresse_code=models.IntegerField(db_column='adresse_code',null=True,blank=True)
    nom_poste=models.CharField(max_length=100,db_column='nom_poste')
    campagne=models.CharField(max_length=100,db_column='campagne')
    revenu_espere=models.FloatField(max_length=100,db_column='revenu_espere')
    probabilité=models.FloatField(max_length=100,db_column='probabilite',null=True,blank=True)
    vendeur=models.CharField(max_length=100,db_column='vendeur')
    date_cloture=models.DateTimeField(db_column='date_cloture',null=True,blank=True)
    oppor_etat=models.IntegerField(db_column='oppor_etat')
    piste_etat=models.IntegerField(db_column='piste_etat')
    confirme_etat=models.IntegerField(db_column='num_etat')
    date_ajout=models.DateTimeField(db_column='date_ajout',null=True,blank=True)
    statut_oppor=models.IntegerField(db_column='statut_oppor',null=True,blank=True)
    facebook=models.CharField(max_length=100,db_column='facebook')
    etat=models.CharField(db_column='etat',max_length=100)
    class Meta:
        db_table='clients_one'

class Events(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,null=True,blank=True)
    start = models.DateTimeField(null=True,blank=True)
    end = models.DateTimeField(null=True,blank=True)
    client=models.ForeignKey(clie, on_delete=models.CASCADE)
    class Meta:  
        db_table = "tblevents"
