#parse the xml file and write the result as tsv

from xml.etree import ElementTree
import pandas as pd
import re
import subprocess



def xml_to_tsv(filename, columns, output_filename= "xml_result.tsv"):
    file_ = open(filename, 'r')
    tree = ElementTree.parse(file_)
    root = tree.getroot()

    df=pd.DataFrame(columns= columns)

    for NCBI_Organism in root.iter('NCBI_Organism'):
        Organism = NCBI_Organism.find('Organism').text
        strain = NCBI_Organism.find('Biosource/InfraspeciesList/Infraspecie/Sub_value').text
        Assembly_status = NCBI_Organism.find('AssemblyStatus').text
        for elem in NCBI_Organism.iter('string'):
            GR = re.search(r'.*genome.*', elem.text)
            if GR:
                Genome_representation = GR.group()
                break
            else:
                Genome_representation = "NA"
        Taxid = NCBI_Organism.find('Taxid').text
        SpeciesTaxid = NCBI_Organism.find('SpeciesTaxid').text
        AssemblyAccession = NCBI_Organism.find('AssemblyAccession').text
        Coverage = NCBI_Organism.find('Coverage').text
        LastUpdateDate = NCBI_Organism.find('LastUpdateDate').text
        SubmissionDate = NCBI_Organism.find('SubmissionDate').text
        SubmitterOrganization = NCBI_Organism.find('SubmitterOrganization').text
        Genbank = NCBI_Organism.find('Synonym/Genbank').text
        ContigN50 = NCBI_Organism.find('ContigN50').text
        for elem in NCBI_Organism.iter('string'):
            p = re.search(r'.*plasmid*', elem.text)
            if p:
                Plasmid = p.group()
                break
            else:
                Plasmid = "NA"
        append_obj = pd.Series([Organism, strain, Assembly_status, Genome_representation, Taxid, \
            SpeciesTaxid, AssemblyAccession, Coverage, LastUpdateDate, SubmissionDate,\
            SubmitterOrganization, Genbank, ContigN50, Plasmid], index = df.columns)
        df = df.append(append_obj, ignore_index = True)
        
        #print (elem.tag, elem.text)

    #write file to tsv format
    df.to_csv(output_filename, index = False, sep = "\t")


def edit_xml(inputfile):
    process = subprocess.run(["gsed","-i", "s/^/\t/g" , inputfile])
    print (process.stdout)
    process = subprocess.run(["gsed","-i", "s/.*<DocumentSummary.*/  <NCBI_Organism>/g" , inputfile])
    print (process.stdout)
    process = subprocess.run(["gsed","-i", "s/.*<\/DocumentSummary>/  <\/NCBI_Organism>/g" , inputfile])
    print (process.stdout)
    process = subprocess.run(["gsed","-i", "1i <DocumentSummary>" , inputfile])
    print (process.stdout)
    cmd = 'echo "</DocumentSummary>" >> '+ inputfile
    process = subprocess.run(cmd, shell = True)
    print (process.stdout)


def main():
    input_xml_file = input("Give the xml file to process\n").strip()
    #organize the xml format to the required one
    edit_xml(input_xml_file)



    output_xmlfile  = input("Name for output file?\n").strip()
    columns_to_get = ["Organism", "strain", "Assembly_status", "Genome_representation", "Taxid", \
            "SpeciesTaxid", "AssemblyAccession", "Coverage", "LastUpdateDate", "SubmissionDate",\
            "SubmitterOrganization", "Genbank", "ContigN50", "Plasmid"]
    print  ("the following columns will be extracted:\n", columns_to_get)
    xml_to_tsv(input_xml_file, columns_to_get, output_xmlfile)



    '''
    Their format in the xml file:

    Organism, Biosource > InfraspeciesList > Infraspecie > Sub_value, AssemblyStatus\
    , propertyList > string, Taxid, SpeciesTaxid, AssemblyAccession, Coverage, LastUpdateDate, \
    SubmissionDate, SubmitterOrganization, Synonym > Genbank, ContigN50, PropertyList > string

    '''

if __name__  == '__main__':
    main()