import pandas as pd
from rdflib import Graph, Literal, RDF, RDFS, URIRef, Namespace, OWL, XSD
from preprocessing import read_n_clean
from querying import rivm_query

# Creating an empty graph and defining RDF namespaces
rivm_graph = Graph()
date =              Namespace('http://example.org/date')
mun_code =          Namespace('http://example.org/mun_code')
mun_name =          Namespace('http://example.org/mun_name')
province =          Namespace('http://example.org/province')
total_cases =       Namespace('http://example.org/total_cases')
hospitalized =      Namespace('http://example.org/hospitalized')
deaths =            Namespace('http://example.org/deaths')
dbpedia_link =      Namespace('https://dbpedia.org/page/')

# OWL Namespace and axioms
OWLNS =             Namespace("http://www.w3.org/2002/07/owl#")
sameAs =            OWLNS["sameAs"]
disjointClasses =   OWLNS["disjointClasses"]

resources = Namespace("http://example.org/Resource/")
ex =        Namespace("http://example.org/")
rivm_graph.bind("resources", resources)
rivm_graph.bind("ex", ex)

# Defining ontology, its new namespace (for RDFS, OWL)
ontology = Namespace("http://www.semanticweb.org/ontology")
rivm_graph.bind("ontology", ontology)

# Adding some classes
relaxed_region = URIRef(ontology["relaxed_region"])
rivm_graph.add((relaxed_region, RDF.type, OWL.Class))
rivm_graph.add((relaxed_region, RDFS.subClassOf, OWL.Thing))
rivm_graph.add((relaxed_region, RDFS.domain, resources["municipality"]))
rivm_graph.add((relaxed_region, RDFS.comment, Literal("Class of municipalities that warrant minimal caution.")))

caution_region = URIRef(ontology["caution_region"])
rivm_graph.add((caution_region, RDF.type, OWL.Class))
rivm_graph.add((caution_region, RDFS.subClassOf, OWL.Thing))
rivm_graph.add((caution_region, OWL.disjointClasses, relaxed_region))
rivm_graph.add((caution_region, RDFS.domain, resources["municipality"]))
rivm_graph.add((caution_region, RDFS.comment, Literal("Class of municipalities that warrant social distancing and other precautions.")))

danger_region = URIRef(ontology["danger_region"])
rivm_graph.add((danger_region, RDF.type, OWL.Class))
rivm_graph.add((danger_region, RDFS.subClassOf, OWL.Thing))
rivm_graph.add((danger_region, RDFS.subClassOf, caution_region))
rivm_graph.add((danger_region, RDFS.domain, resources["municipality"]))
rivm_graph.add((danger_region, RDFS.comment, Literal("Class of municipalities that are especially dangerous. Wear masks. \n By inference, this is disjoint with relaxed as well")))

lockdown_region = URIRef(ontology["lockdown_region"])
rivm_graph.add((lockdown_region, RDF.type, OWL.Class))
rivm_graph.add((lockdown_region, RDFS.subClassOf, OWL.Thing))
rivm_graph.add((lockdown_region, RDFS.subClassOf, danger_region))
rivm_graph.add((lockdown_region, RDFS.domain, resources["municipality"]))
rivm_graph.add((lockdown_region, RDFS.comment, Literal("Those municipalities barring non-essential movement. \n By inference, this is also disjoint with relaxed")))

if __name__ == '__main__':

    rivm_dataframe = pd.read_csv("COVID-19_aantallen_gemeente_cumulatief.csv", sep=";", quotechar='"')
    read_n_clean(rivm_dataframe)

    for index, row in rivm_dataframe.iterrows():

        # Adding data to municipality_name entities
        rivm_graph.add((URIRef(mun_name + '=' + row['Municipality_name']), RDF.type, resources["municipality"]))
        rivm_graph.add((URIRef(mun_name + '=' + row['Municipality_name']), URIRef(province), Literal(row['Province'] + '-province', datatype=XSD.string)))
        rivm_graph.add((URIRef(mun_name + '=' + row['Municipality_name']), URIRef(date), Literal(row['Date_of_report'], datatype=XSD.dateTime)))
        rivm_graph.add((URIRef(mun_name + '=' + row['Municipality_name']), URIRef(total_cases), Literal(row['Total_reported'], datatype=XSD.positiveInteger)))
        rivm_graph.add((URIRef(mun_name + '=' + row['Municipality_name']), URIRef(hospitalized), Literal(row['Hospital_admission'], datatype=XSD.positiveInteger)))
        rivm_graph.add((URIRef(mun_name + '=' + row['Municipality_name']), URIRef(deaths), Literal(row['Deceased'], datatype=XSD.positiveInteger)))
        rivm_graph.add((URIRef(mun_name + '=' + row['Municipality_name']), URIRef(mun_code), Literal(row['Municipality_code'], datatype=XSD.string)))
        rivm_graph.add((URIRef(mun_name + '=' + row['Municipality_name']),
                        RDF.type, lockdown_region)) if row['Total_reported'] > 2500 else rivm_graph.add((URIRef(mun_name + '=' + row['Municipality_name']),
                        RDF.type, danger_region)) if row['Total_reported'] > 1200 else rivm_graph.add((URIRef(mun_name + '=' + row['Municipality_name']),
                        RDF.type, caution_region)) if row['Total_reported'] > 200 else rivm_graph.add((URIRef(mun_name + '=' + row['Municipality_name']),
                        RDF.type, relaxed_region))

        # Adding municipality codes (as resources) for querying (assuming mun_code isn't pseudonym for mun_name...?)
        rivm_graph.add((URIRef(mun_code + '=' + row['Municipality_code']), RDF.type, resources["municipality_code"]))
        rivm_graph.add((URIRef(mun_code + '=' + row['Municipality_code']), URIRef(mun_name), URIRef(mun_name + '=' + row['Municipality_name'])))
        rivm_graph.add((URIRef(mun_code + '=' + row['Municipality_code']), RDFS.label, Literal("Municipality code of: " + row['Municipality_name'], datatype=XSD.string)))

        # Linking municipalities and provinces to DBPedia, which doesn't distinguish between the two. Makes some things easier!
        rivm_graph.add((URIRef(mun_name + '=' + row['Province']), sameAs, URIRef(dbpedia_link + (row['Province']))))
        rivm_graph.add((URIRef(mun_name + '=' + row['Municipality_name']), sameAs, URIRef(dbpedia_link + (row['Municipality_name']))))


    # View the graph or dataframe themselves, or count edges in graph
    print(rivm_graph.serialize(format='turtle').decode('UTF-8'))
    #print(rivm_dataframe[:20], sep="\n")

    count_edges = 0
    for edge in rivm_graph:
        count_edges += 1
    print("Total edges:", count_edges, '\n')

    rivm_query(rivm_graph)
