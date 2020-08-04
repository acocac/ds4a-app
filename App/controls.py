#exploratory vars
GEOGRAPHIC = dict(
    Department="Department",
    National="National"
)

POPULATION = dict(
    Recidivist="Recidivist",
    Nonrecidivist="Non-recidivist"
)


#exploratory date sliders
range_year = range(2000,2021)

YEARS = {}
for i,each in enumerate(range_year):
    YEARS[i] = each

range_month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

MONTHS = {}
for i,each in enumerate(range_month):
    MONTHS[i+1] = each


# #clusters
CLUSTERS = {0: 'Acts involving fraud, deception, or corruption',
 1: 'Armed conflict and injurious acts of a sexual nature',
 2: 'Coercive actions, extortion, blackmail, torture, and exploitation',
 3: 'Acts related to arms trafficking and illegal use of military or police equipment',
 4: 'Acts causing harm or intending to cause harm to a person, burglary and domestic violence',
 5: 'Acts leading to death or intending to cause death, drugs and arms possession',
 6: 'Information, communication or computer-oriented crime',
 7: 'Acts related to the appropriation or embezzlement of public funds',
 8: 'Copyright infringement, counterfeit and financial crimes',
 9: 'Terrorism and acts against public safety and national security',
 10: 'Acts related to natural resources and chemical substances',
 11: 'Drug trafficking'}


#categorical prediction vars
GENDER = {0: "Female", 1: "Male"}
STUDY = {0: "No", 1: "Yes"}
EDUCATION = {0: 'ANALFABETA', 1: 'CICLO I', 2: 'CICLO II', 3: 'CICLO III', 4: 'CICLO IV', 5: 'TECNOLOGICO', 6: 'TECNICO', 7: 'TECNICO PROFESIONAL', 8: 'PROFESIONAL', 9: 'POST GRADO', 10: 'ESPECIALIZACION', 11: 'MAGISTER'}
WORK = {0: "No", 1: "Yes"}
INTRAMUROS = {0: "Other", 1: "In prison"}
CALIFICADO = {0: "No Calificado", 1: "Calificado"}
AGRAVADO = {0: "No Agravado", 1: "Agravado"}
CLUSTER1 = {0: "NO delitos sexuales/guerra", 1: "SI delitos sexuales/guerra"}
CLUSTER4 = {0: "NO violencia/delitos menores", 1: "SI violencia/delitos menores"}
CLUSTER5 = {0: "NO delitos fuertes/homicidio/drogas/armas de fuego", 1: "SI delitos fuertes/homicidio/drogas/armas de fuego"}


#top predictors
IMPVARIABLES = {'CLUSTER_4': 'Belongs to crime group 4',
 'actividades_estudio': 'Study activities',
 'actividades_trabajo': 'Work Activities',
 'sentencia': 'Sentence Length',
 'CLUSTER_5': 'Belongs to crime group 5',
 'cuenta_delitos': 'Crimes count',
 'estado_ingreso_Intramuros': 'Intramuros state',
 'edad': 'Age',
 'CLUSTER_1': 'Belongs to crime group 1',
 'calificado': 'Crime(s) Calificado',
 'genero': 'Gender',
 'agravado': 'Crime(s) Agravado',
 'nivel_educativo': 'Education Level'}