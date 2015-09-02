import urllib2
from rdkit import Chem
import cPickle
from SOAPpy import WSDL

data = []
i = 1
while i <= 17206:

    print "Processed " + str(i - 1) + "/" + str(17206)

    sequences = []
    missing_seq = 0
    num_ecs = 0

    # Make rpair id from int
    rpid = "RP" + (5-len(str(i)))*str(0) + str(i)
    rpid = str(rpid)

    try:

        # Get rdm entries of rpair
        response = urllib2.urlopen('http://rest.kegg.jp/link/rc/' + rpid)
        html = response.read()
        html = html.split()
        html = html[1].split(":")
        response = urllib2.urlopen('http://rest.kegg.jp/list/' + html[1])
        html = response.read()
        html = html.split()
        rdm = html[1] + "|" + html[2]

        # Get reactant compound entry of rpair and convert to smiles
        response = urllib2.urlopen('http://rest.kegg.jp/link/cpd/' + rpid)
        html = response.read()
        s1 = html.split()
        s2 = s1[1].split(":")
        compound = s2[1]
        molfile = open(compound + ".mol", "wb")
        response = urllib2.urlopen('http://rest.kegg.jp/get/' + compound + '/mol')
        html = response.read()
        err_test = html[1]  # Test is not empty
        molfile.write(html)
        molfile.close()
        m = Chem.MolFromMolFile(compound + ".mol")
        smiles = Chem.MolToSmiles(m)

        # Get aaseq of all enzymes for reaction pair (this may take a while)
        response = urllib2.urlopen('http://rest.kegg.jp/link/ec/' + rpid)
        html = response.read()
        html = html.split()

        ecs = []
        for k in range(len(html)):
            if k % 2 == 0:
                ecs.append(html[k + 1])

        num_ecs = len(ecs)

        j = 0
        for ec in ecs:
            ec = ec.split(':')
            ecs[j] = ec[1]
            j += 1

        for ec in ecs:
            try:
                # Get sequences from ec number from brenda
                wsdl = "http://www.brenda-enzymes.org/soap/brenda.wsdl"
                client = WSDL.Proxy(wsdl)
                resultString = client.getSequence("ecNumber*" + ec)

                if len(resultString) > 1:
                    resultString = resultString.split('!')
                    for entry in resultString:
                        fields = entry.split('#')
                        if fields[1][:9] == 'sequence*':
                            field = fields[1].split('*')
                            sequence = field[1]
                            sequences.append(sequence)
                else:
                    missing_seq += 1
            except:
                missing_seq += 1

        full = rdm + smiles
        for seq in sequences:
            data.append([full, seq])

    except:

        print 'Rdm or smiles error' + '(' + rpid + ')'

    print 'Found sequences for ' + str(num_ecs - missing_seq) + ' of ' + str(num_ecs) + ' enzyme classes.'

    i += 1

datafile = open("rc_compound_data.pkl", "wb")
cPickle.dump(data, datafile)
datafile.close()
