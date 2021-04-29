import urllib3
import csv
urllib3.disable_warnings()
from datetime import datetime
from modules.getDataBase import GetDataBase

sysdate = datetime.now().strftime('%d/%m/%Y')
sysdateWSO2 = datetime.now().strftime('%m%Y')

print(str(datetime.now().strftime('%d/%m/%Y-%H:%M:%S')+': Inicio da atividade'))

gtb = GetDataBase()

result_list = []

# --------------------------- Cria lista para comparacoes de contas ---------------------------
list_resource_R12 = []
list_resource_Somar = []
blazon = gtb.blazon('conta')

for list_user_blazon in blazon:
    if(list_user_blazon[2] in ('R12','R12 (APLICAÇÃO)','R12 PARA FORNECEDORES')):
        list_resource_R12.append(str(list_user_blazon[0]).strip())
    elif(list_user_blazon[2] in ('SOMAR','SOMAR (APLICAÇÃO)')):
        list_resource_Somar.append(str(list_user_blazon[0]).strip())


# --------------------------- Verifica contas em divergencias ---------------------------
user_r12 = gtb.r12('conta')
for r12 in user_r12:
    if (r12[0] not in list_resource_R12):
        result_list.append(('CONTA', 'R12', '-',r12[0]))

user_somar = gtb.somar('conta')
for somar in user_somar:
    if (somar[0] not in list_resource_Somar):
        result_list.append(('CONTA', 'SOMAR', '-',somar[0]))


# --------------------------- Cria lista para comparacoes direitos ---------------------------
list_entitlement_R12 = []
list_entitlement_Somar = []
blazon_direitos = gtb.blazon('direito')

for list_ent_blazon in blazon_direitos:
    if(list_ent_blazon[2] in ('R12')):
        list_entitlement_R12.append(str(list_ent_blazon[0]).strip() + str(list_ent_blazon[3][6:]).strip())
    elif (list_ent_blazon[2] in ('R12 (APLICAÇÃO)')):
        list_entitlement_R12.append(str(list_ent_blazon[0]).strip() + str(list_ent_blazon[3][16:]).strip())
    elif(list_ent_blazon[2] in ('SOMAR')):
        list_entitlement_Somar.append(str(list_ent_blazon[0]).strip() + str(list_ent_blazon[3][8:]).strip())
    elif (list_ent_blazon[2] in ('SOMAR (APLICAÇÃO)')):
        list_entitlement_Somar.append(str(list_ent_blazon[0]).strip() + str(list_ent_blazon[3][18:]).strip())


# --------------------------- Verifica direitos em divergencias ---------------------------
ent_r12 = gtb.r12('direito')
for r12 in ent_r12:
    if (((r12[0]+r12[2]) not in list_entitlement_R12) and ((r12[0]+r12[3]) not in list_entitlement_R12)):
        result_list.append(('DIREITO', 'R12', r12[2],r12[0]))

ent_somar = gtb.somar('direito')
for somar in ent_somar:
    if ((somar[0]+somar[2]) not in list_entitlement_Somar):
        result_list.append(('DIREITO', 'SOMAR', somar[2],somar[0]))


with open('C:/Automations/checkAuditAccess/reports/checkAuditAccess.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(["TIPO", "RESOURCE", "ENTITLEMENT","USER"])

    # verifica nome faltantes no R12 e busca no blazon, criando uma nova lista atualizada
    for result_list in result_list:
        writer.writerow([result_list[0], result_list[1], result_list[2], result_list[3]])

print(str(datetime.now().strftime('%d/%m/%Y-%H:%M:%S')+': Fim da atividade'))