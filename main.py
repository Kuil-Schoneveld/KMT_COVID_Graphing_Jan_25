import pandas as pd
from rdflib import Graph, Literal, BNode, RDF, RDFS, URIRef, Namespace, OWL, XSD

# Converting csv file into a pandas dataframe
rivm_dataframe = pd.read_csv("COVID-19_aantallen_gemeente_cumulatief.csv", sep=";", quotechar='"')
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Removing whitespace, apostrophes, other characters from municipality names
rivm_dataframe['Municipality_name'] = rivm_dataframe['Municipality_name'].str.replace(' ', '_')
rivm_dataframe['Municipality_name'] = rivm_dataframe['Municipality_name'].str.replace('\'', ',')
rivm_dataframe['Municipality_name'] = rivm_dataframe['Municipality_name'].str.replace('(', '')
rivm_dataframe['Municipality_name'] = rivm_dataframe['Municipality_name'].str.replace(')', '')
rivm_dataframe['Municipality_name'] = rivm_dataframe['Municipality_name'].str.replace('.', '')

# Creating an empty graph and defining RDF namespaces
rivm_graph = Graph()
date =              Namespace('http://example.org/date')
mun_code =          Namespace('http://example.org/mun_code')
mun_name =          Namespace('http://example.org/mun_name')
province =          Namespace('http://example.org/province')
total_rep_cases =   Namespace('http://example.org/total_cases')
hospitalized =      Namespace('http://example.org/hospitalized')
deaths =            Namespace('http://example.org/dead')

terms =     Namespace("http://example.org/terms/")
resources = Namespace("http://example.org/Resource/")

rivm_graph.bind("terms", terms)
rivm_graph.bind("ex", resources)

# Defining ontology, its new namespace (for RDFS, OWL)
ontology = Namespace("http://www.semanticweb.org/ontology")
rivm_graph.bind("ontology", ontology)

# Adding some classes
covid_region = URIRef(ontology["covid_region"])
rivm_graph.add((covid_region, RDF.type, OWL.Class))
rivm_graph.add((covid_region, RDFS.subClassOf, OWL.Thing))

# Connecting municipalities to their dbpedia reference


if __name__ == '__main__':

    for index, row in rivm_dataframe.iterrows():

        # Adding data to municipality_name entities to substantiate graph
        rivm_graph.add((URIRef(mun_name + '=' + row['Municipality_name']), RDF.type, resources["municipality"]))
            # do we even need an rdfs label for the municipality name itself? seems unnecessary/redundant:
            # rivm_graph.add((URIRef(mun_code + '=' + row['Municipality_name']), RDFS.label, Literal("Municipality code of: " + row['Municipality_name'], datatype=XSD.string)))
        rivm_graph.add((URIRef(mun_name + '=' + row['Municipality_name']), URIRef(province), Literal(row['Province'] + '-province', datatype=XSD.string)))
        rivm_graph.add((URIRef(mun_name + '=' + row['Municipality_name']), URIRef(date), Literal(row['Date_of_report'], datatype=XSD.dateTime)))
        rivm_graph.add((URIRef(mun_name + '=' + row['Municipality_name']), URIRef(total_rep_cases), Literal(row['Total_reported'], datatype=XSD.positiveInteger)))
        rivm_graph.add((URIRef(mun_name + '=' + row['Municipality_name']), URIRef(hospitalized), Literal(row['Hospital_admission'], datatype=XSD.positiveInteger)))
        rivm_graph.add((URIRef(mun_name + '=' + row['Municipality_name']), URIRef(deaths), Literal(row['Deceased'], datatype=XSD.positiveInteger)))

        # Adding municipality codes, for querying (I'm assuming mun_code isn't just the same as mun_name...?)
        rivm_graph.add((URIRef(mun_code + '=' + row['Municipality_code']), URIRef(mun_name), Literal(row['Municipality_name'], datatype=XSD.string)))
        rivm_graph.add((URIRef(mun_code + '=' + row['Municipality_code']), RDFS.label, Literal("Municipality code of: " + row['Municipality_name'], datatype=XSD.string)))

    print(rivm_graph.serialize(format='turtle').decode('UTF-8'))
    print(rivm_dataframe[:20], sep="\n")

    '''
    count_edges = 0
    for edge in rivm_graph:
        count_edges += 1
    print (count_edges)
'''