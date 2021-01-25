import pandas as pd
import rdflib

#Converting .csv file into a pandas dataframe
rivm_dataframe = pd.read_csv("COVID-19_aantallen_gemeente_cumulatief.csv", sep=";", quotechar='"')
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

#Removing whitespace and apostrophes from municipality names
rivm_dataframe['Municipality_name'] = rivm_dataframe['Municipality_name'].str.replace(' ', '_')
rivm_dataframe['Municipality_name'] = rivm_dataframe['Municipality_name'].str.replace('\'', ',')

#Creating an empty graph and defining namespaces
rivm_graph = rdflib.Graph()
date = rdflib.Namespace('http://example.org/date')
mun_code = rdflib.Namespace('http://example.org/mun_code')
mun_name = rdflib.Namespace('http://example.org/mun_name')
province = rdflib.Namespace('http://example.org/province')
total_reported = rdflib.Namespace('http://example.org/total')
hospitalized = rdflib.Namespace('http://example.org/hospitalized')
deceased = rdflib.Namespace('http://example.org/dead')

if __name__ == '__main__':

    for index, row in rivm_dataframe.iterrows():
        rivm_graph.add((rdflib.URIRef(mun_name + '=' + row['Municipality_name']), rdflib.RDF.type, rdflib.FOAF.Person))
        #rivm_graph.add((URIRef(mun_name + row['Municipality_name']), URIRef(province + 'Municipality_name'), Literal(row['Municipality_name'], datatype=XSD.string)))


    print(rivm_dataframe[:20], sep="\n")
    print(rivm_graph.serialize(format='turtle').decode('UTF-8'))

