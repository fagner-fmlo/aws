import boto3
import pprint
import os




#Declaração da conexão do boto3 com o AWS EC2. Utiliza-se aqui a configuração subjacente do aws cli
client_ec2 = boto3.client(
    'ec2',
    region_name = "us-east-1"
)




#Formantando identacao para facilitar o entendimento das esturutras de dicionário/listas
pp = pprint.PrettyPrinter(indent=4)




#Listagem de todas as interfaces de rede que estão disponiveis na amazon para a conta em questão
all_eni = client_ec2.describe_network_interfaces()




#Declaracao de lista que ira receber todos os ids das interfaces de de rede existentes nos VPCS disponiveis para as credenciais do aws cli dispoibilizada
sg_in_use=[]




#Loop para percorrer o dicionario obitido e armazenado em all_eni, neste loop a instrução de .append irá popular a lista all_eni, que irá ser usada mais a frente 
for eni_netinf in all_eni['NetworkInterfaces']:
    for eni_groups  in eni_netinf['Groups']:
        sg_id = eni_groups['GroupId']
        if sg_id not in sg_in_use:
            sg_in_use.append(sg_id)
#Estas instruções a seguir facilita questões de resolução de problemas ou até entendimento da estrutura de dados que esta usada            
        #print(gsid['GroupId'])
    #pp.pprint(eni)
#len_sg_unique_id = len (sg_in_use)
#print(len_sg_unique_id)




#Declaracao de lista que ira receber todos os ids dos secrurity groups existentes nos VPCS disponiveis para as credenciais do aws cli dispoibilizada
all_sg_list=[]




#Assim como no loop anterior, o objetivo é coletar IDs, nesse caso, de security groups, estes IDs serão armazenados na lista all_sg_list
all_sg = client_ec2.describe_security_groups()
for s_groups in all_sg['SecurityGroups']:    
    s_goup_id = s_groups['GroupId']
    #print(sg_id)
    all_sg_list.append(s_goup_id)
#print (all_sg_list)    
#qtd_sg = len(all_sg_list)
#print (qtd_sg)     




#Esta lista que esta sendo declarada neste ponto, é o objetivo do script pois será nela que os security groups em uso serão listados
security_groups_sem_uso=[]




#Uma vez que já temos todos os identificadores de interfaces de rede (ENI) e também temos os security groups podemos buscar security groups que não tenha associação com interfaces de rede 
for sg in  all_sg_list:
    if sg not in sg_in_use:
#Caso esse condicional retorne verdade, indica que o security groups (SG) esta sem associacao a ENI, ou seja, sem uso. Ainda sim, iremos checar via aws cli se esse fato procede. 
#Na situação onde o retorno de network interfaces seja vazio também no teste do aws cli describe-network-interfaces, o SG esta de fato sem uso.    
        security_groups_sem_uso.append(sg)
        print ("Security Group não esta associado a nenhuma ENI, SG-ID:", sg)
#        os.system("aws ec2 describe-network-interfaces \
#                          --filters Name=group-id,Values=$sg --region us-east-1 \
#                            --output json" )




#Obtendo a quantidade de security groups sem uso.
qtd_security_groups_sem_uso = len(security_groups_sem_uso)




#Emitindo a informacao do quantitativo dos security groups sem uso para que o administrador tenha essa informaçãos
print ("Total de security groups sem uso:", qtd_security_groups_sem_uso)
