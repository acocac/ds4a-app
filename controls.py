GEOGRAPHIC = dict(
    Department="Department",
    National="National"
)

POPULATION = dict(
    Recidivist="Recidivist",
    Nonrecidivist="Non-recidivist"
)

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

range_year = range(2000,2021)

YEARS = {}
for i,each in enumerate(range_year):
    YEARS[i] = each

range_month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

MONTHS = {}
for i,each in enumerate(range_month):
    MONTHS[i+1] = each

range_periods = []
years = [i for i in range(2010,2021)]
semesters = range(1,13)
for year in years:
    for semester in semesters:
        range_periods.append('{}_{}'.format(year,semester))

PERIODS = {}
for i,each in enumerate(range_periods):
    PERIODS[i] = each
