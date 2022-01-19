# import os
import subprocess
import numpy as np
from zipfile import ZipFile

def Write_Parameters_GrapXML(fs, vs, ris, AOI, NumbTrees, NumbTrainSamples, Outfilename, OutFormat):
    
    RadI_Expr_GraphXML = {    'NDVI':'(B8 - B4)/(B8 + B4)' ,
                              'SIPI':'(B8 - B2)/(B8 - B4)',
                              'NDWI':'(B3 - B8)/(B3 + B8)'
                          }        
    
    filenames = []
    BandMaths_names = []
    VectorFilenames = []
    VectorNames = []
    BandMaths_exp = []
    LabClass_Exp = ''
    for i in range(0,len(fs)):
        filenames.append(fs[i])
        for k in range(0, len(ris)):
            BandMaths_names.append('%s(%s)' % (ris[k],str(i+1)))
            BandMaths_exp.append(RadI_Expr_GraphXML[ris[k]])
    BandMaths_names = (np.asarray(BandMaths_names).reshape(len(fs),-1).tolist())
    BandMaths_exp = (np.asarray(BandMaths_exp).reshape(len(fs),-1).tolist())
    for j in range(0,len(vs)):
        VectorFilenames.append('%s' % vs[j])
        VectorNames.append('%s' % vs[j].split('\\')[-1].split('.')[0])
        if j == 0:
            LabClass_Exp += 'if LabeledClasses == %s then %s ' % (str(j), str(vs[j].split('\\')[-1].split('.')[0]))
        else:
            LabClass_Exp += 'else if LabeledClasses == %s then %s ' % (str(j), str(vs[j].split('\\')[-1].split('.')[0]))
    LabClass_Exp += 'else 8888'
    
    Parameters_GraphXML = {   'Read_files': ({'file':filenames}),
                              'Subset_images': ({'sourceBands':'B2,B3,B4,B8','region':'','referenceBand':'','geoRegion':AOI,'subSamplingX':'1',
                                          'subSamplingY':'1','fullSwath':'false','tiePointGrids':'','copyMetadata':'true'}),
                              'Radiom_Indices': ({'name':BandMaths_names,'type':'float32','expression':BandMaths_exp,'description':'','unit':'','noDataValue':'8888.0'}),
                              'Merge_RadInd':({'sourceBands':'','geographicError':'1.0E-5'}),
                              'GroundPoints': ({'vectorFile':VectorFilenames,'separateShapes':'false'}),
                              'RandomForest': ({'treeCount':NumbTrees,'numTrainSamples':NumbTrainSamples,'savedClassifierName':'ECHOES_RF',
                                                            'doLoadClassifier':'false','doClassValQuantization':'true','minClassValue':'0.0','classValStepSize':'5.0',
                                                            'classLevels':'101','trainOnRaster':'false','trainingBands':'','trainingVectors':VectorNames,
                                                            'featureBands':BandMaths_names,'labelSource':'VectorNodeName','evaluateClassifier':'false',
                                                            'evaluateFeaturePowerSet':'false','minPowerSetSize':'2','maxPowerSetSize':'7'}),
                              'LabeLClasses': ({'name':'LabelClasses','type':'float32','expression':LabClass_Exp,'description':'','unit':'','noDataValue':'8888.0'}),
                              'ExtConfidenceBand': ({'sourceBands':'Confidence','region':'','referenceBand':'','geoRegion':AOI,'subSamplingX':'1',
                                          'subSamplingY':'1','fullSwath':'false','tiePointGrids':'','copyMetadata':'true'}),
                              'LcClassToInteger':({'sourceBands':'LabelClasses','targetDataType':'int32','targetScalingStr':'Linear (between 95% clipped histogram)','targetNoDataValue':'8888.0'}),
                              'Merge_LC_Confi': ({'sourceBands':'','geographicError':'1.0E-5'}),
                              'WriteOutput': ({'file':Outfilename,'formatName':OutFormat})
                          }
    return Parameters_GraphXML
    

    
    

def Write_Sources_GrapXML (fs, vs, ris):
    Read_Files_Vect = []
    Subset_Vect= []
    BandMaths_Vect = []
    for i in range(0,len(fs)):
        if i == 0:
            Read_Files_Vect.append('Read')
            Subset_Vect.append('Subset')
            BandMaths_Vect = ['BandMaths']
            for k in range(1, len(ris)):
                BandMaths_Vect.append('BandMaths(%s)' % str(k+1))
        else:
            Read_Files_Vect.append('Read(%s)' % str(i+1))
            Subset_Vect.append('Subset(%s)' % str(i+1))
            for k in range(len(ris)*i, len(ris)*i+len(ris)):
                BandMaths_Vect.append('BandMaths(%s)' % str((k+1)))
    BandMaths_Vect = (np.asarray(BandMaths_Vect).reshape(len(fs),-1).tolist())
    ImportVector_Vect = []
    for j in range(0,len(vs)):
        if j == 0:
            ImportVector_Vect.append('Import-Vector')
        else:
            ImportVector_Vect.append('Import-Vector(%s)' % str(j+1))
    
    Sources_GrapXML = {   'Read_files': ['Read', Read_Files_Vect, ''],
                          'Subset_images': ['Subset',Subset_Vect, Read_Files_Vect],
                          'Radiom_Indices':['BandMaths', BandMaths_Vect, Subset_Vect],
                          'Merge_RadInd':['BandMerge',['BandMerge'], BandMaths_Vect],
                          'GroundPoints':['Import-Vector', ImportVector_Vect,['BandMerge']],
                          'RandomForest':['Random-Forest-Classifier', ['Random-Forest-Classifier'],ImportVector_Vect],
                          'LabeLClasses': ['BandMaths', ['BandMaths(%s)' % str(len(fs)*3+1)],['Random-Forest-Classifier']],
                          'ExtConfidenceBand':['Subset', ['Subset(%s)' % str(len(fs)+1)],['Random-Forest-Classifier']],
                          'LcClassToInteger': ['Convert-Datatype',['Convert-Datatype'],['BandMaths(%s)' % str(len(fs)*3+1)]],
                          'Merge_LC_Confi': ['BandMerge', ['BandMerge(2)'],['Convert-Datatype','Subset(%s)' % str(len(fs)+1)]],
                          'WriteOutput' : ['Write', ['Write'],['BandMerge(2)']]
                          }            

    return Sources_GrapXML



def Write_XML_FILE(RS_Images, ground_control_points, AOI,ris,xmlfile,NumbTrees, NumbTrainSamples, Outfilename, OutFormat):
    xmlGraph = '<graph id="Graph">\n  <version>1.0</version>\n'
    xmlAppData = '\t<applicationData\tid="Presentation">\n\t <Description/>\n'
    
    Sources_GrapXML = Write_Sources_GrapXML(RS_Images, ground_control_points, ris)
    Parameters_GraphXML = Write_Parameters_GrapXML(RS_Images, ground_control_points, ris, AOI, NumbTrees, NumbTrainSamples, Outfilename, OutFormat)
     
    x = 700
    y = 10
    
    for key in Sources_GrapXML.keys():
        
        if key == 'Read_files':           
            x = 10
            y = 10
            for i in range(0, len(Sources_GrapXML[key][1])):
                xmlGraph = xmlGraph + '  <node\tid="%s">\n    <operator>%s</operator>\n' % (Sources_GrapXML[key][1][i],Sources_GrapXML[key][0])
                xmlAppData = xmlAppData + '  <node\tid="%s">\n    <displayPosition x="%s.0" y="%s.0"/>\n  </node>\n' % (Sources_GrapXML[key][1][i],str(x),str(y))
                y += 100
                xml_sources =  '    <sources/>\n'
                xml_parameters = '    <parameters class="com.bc.ceres.binding.dom.XppDomElement">\n'
                for parameter in Parameters_GraphXML[key].keys():
                    if Parameters_GraphXML[key][parameter] == '':
                        xml_parameters = xml_parameters + '      <%s/>\n' % parameter
                    else:
                        xml_parameters = xml_parameters + '      <%s>%s</%s>\n' % (parameter,Parameters_GraphXML[key][parameter][i],parameter)
                xml_parameters = xml_parameters + '    </parameters>\n'
                xmlGraph = xmlGraph + xml_sources + xml_parameters
                xmlGraph = xmlGraph + '  </node>\n'
                
        elif key == 'Subset_images':
            x = 100
            y = 10
            for i in range(0, len(Sources_GrapXML[key][1])):
                xmlGraph = xmlGraph + '  <node\tid="%s">\n\t <operator>%s</operator>\n' % (Sources_GrapXML[key][1][i],Sources_GrapXML[key][0])
                xmlAppData = xmlAppData + '  <node\tid="%s">\n    <displayPosition x="%s.0" y="%s.0"/>\n  </node>\n' % (Sources_GrapXML[key][1][i],str(x),str(y))
                y += 100
                xml_sources = '    <sources>\n      <sourceProduct refid="%s"/>\n    </sources>\n' % Sources_GrapXML[key][2][i]
                xml_parameters = '    <parameters class="com.bc.ceres.binding.dom.XppDomElement">\n'
                for parameter in Parameters_GraphXML[key].keys():
                    if Parameters_GraphXML[key][parameter] == '':
                        xml_parameters = xml_parameters + '      <%s/>\n' % parameter
                    else:
                        xml_parameters = xml_parameters + '      <%s>%s</%s>\n' % (parameter,Parameters_GraphXML[key][parameter],parameter)
                xml_parameters = xml_parameters + '    </parameters>\n'
                xmlGraph = xmlGraph + xml_sources + xml_parameters
                xmlGraph = xmlGraph + '  </node>\n'
                    
        elif key == 'Radiom_Indices':
            x = 200
            y = 5
            for i in range(0, len(Sources_GrapXML[key][1])):
                for j in range(0, len(Sources_GrapXML[key][1][i])):
                    xmlGraph = xmlGraph + '  <node\tid="%s">\n\t <operator>%s</operator>\n' % (Sources_GrapXML[key][1][i][j],Sources_GrapXML[key][0])
                    xmlAppData = xmlAppData + '  <node\tid="%s">\n    <displayPosition x="%s.0" y="%s.0"/>\n  </node>\n' % (Sources_GrapXML[key][1][i][j],str(x),str(y))
                    y += 35
                    xml_sources = '    <sources>\n\t  <sourceProduct refid="%s"/>\n    </sources>\n' % Sources_GrapXML[key][2][i]
                    xml_parameters = '    <parameters class="com.bc.ceres.binding.dom.XppDomElement">\n'
                    xml_parameters = xml_parameters + '      <targetBands>\n'
                    xml_parameters = xml_parameters  + '        <targetBand>\n'
                    for parameter in Parameters_GraphXML[key].keys():
                        if parameter == 'name' or parameter == 'expression':
                              xml_parameters = xml_parameters + '          <%s>%s</%s>\n' % (parameter,Parameters_GraphXML[key][parameter][i][j],parameter)
                        else:
                            if Parameters_GraphXML[key][parameter] == '':
                                xml_parameters = xml_parameters + '          <%s/>\n' % parameter
                            else:
                                xml_parameters = xml_parameters + '          <%s>%s</%s>\n' % (parameter,Parameters_GraphXML[key][parameter],parameter)
                    xml_parameters = xml_parameters + '        </targetBand>\n'
                    xml_parameters = xml_parameters + '      </targetBands>\n'
                    xml_parameters = xml_parameters + '      <variables/>\n'
                    xml_parameters = xml_parameters + '    </parameters>\n'
                    xmlGraph = xmlGraph + xml_sources + xml_parameters
                    xmlGraph = xmlGraph + '  </node>\n'
            
        elif key == 'Merge_RadInd':
            x = 300
            y = 150           
            xmlGraph = xmlGraph + '  <node\tid="%s">\n    <operator>%s</operator>\n' % (Sources_GrapXML[key][1][0],Sources_GrapXML[key][0])
            xmlAppData = xmlAppData + '  <node\tid="%s">\n    <displayPosition x="%s.0" y="%s.0"/>\n  </node>\n' % (Sources_GrapXML[key][1][0],str(x),str(y))
            cc = 0
            for i in range(0, len(Sources_GrapXML[key][2][0])):
                for j in range(0, len(Sources_GrapXML[key][2])):
                    if i==0 and j==0:
                        xml_sources = ('    <sources>\n      <sourceProduct refid="%s"/>\n' % Sources_GrapXML[key][2][j][i])                
                    elif i == (len(Sources_GrapXML[key][2][0])-1) and j == (len(Sources_GrapXML[key][2])-1):
                        xml_sources = xml_sources + '      <sourceProduct.%s refid="%s"/>\n    </sources>\n' % (cc,Sources_GrapXML[key][2][j][i])
                    else:
                       xml_sources = xml_sources + '      <sourceProduct.%s refid="%s"/>\n' % (cc,Sources_GrapXML[key][2][j][i])
                    cc += 1
            xml_parameters = '    <parameters class="com.bc.ceres.binding.dom.XppDomElement">\n'
            for parameter in Parameters_GraphXML[key].keys():
                if Parameters_GraphXML[key][parameter] == '':
                    xml_parameters = xml_parameters + '      <%s/>\n' % parameter
                else:
                    xml_parameters = xml_parameters + '      <%s>%s</%s>\n' % (parameter,Parameters_GraphXML[key][parameter],parameter)
            xml_parameters = xml_parameters + '    </parameters>\n'
            xmlGraph = xmlGraph + xml_sources + xml_parameters
            xmlGraph = xmlGraph + '  </node>\n'
        
        elif key == 'GroundPoints':
            x = 400
            y = 5
            for i in range(0, len(Sources_GrapXML[key][1])):
                xmlGraph = xmlGraph + '  <node\tid="%s">\n    <operator>%s</operator>\n' % (Sources_GrapXML[key][1][i],Sources_GrapXML[key][0])
                xmlAppData = xmlAppData + '  <node\tid="%s">\n    <displayPosition x="%s.0" y="%s.0"/>\n  </node>\n' % (Sources_GrapXML[key][1][i],str(x),str(y))
                y += 35
                if i==0:
                    xml_sources = '    <sources>\n      <sourceProduct refid="%s"/>\n    </sources>\n' % Sources_GrapXML[key][2][0]
                else:
                    xml_sources = '    <sources>\n      <sourceProduct refid="%s"/>\n    </sources>\n' % Sources_GrapXML[key][1][i-1]
                xml_parameters = '    <parameters class="com.bc.ceres.binding.dom.XppDomElement">\n'
                for parameter in Parameters_GraphXML[key].keys():
                    if parameter == 'vectorFile':
                        xml_parameters = xml_parameters + '      <%s>%s</%s>\n' % (parameter,Parameters_GraphXML[key][parameter][i],parameter)
                    else:
                        if Parameters_GraphXML[key][parameter] == '':
                            xml_parameters = xml_parameters + '      <%s/>\n' % parameter
                        else:
                            xml_parameters = xml_parameters + '      <%s>%s</%s>\n' % (parameter,Parameters_GraphXML[key][parameter],parameter)
                xml_parameters = xml_parameters + '    </parameters>\n'
                xmlGraph = xmlGraph + xml_sources + xml_parameters
                xmlGraph = xmlGraph + '  </node>\n'
                
        elif key == 'RandomForest':
            x = 600
            y = 150
            xmlGraph = xmlGraph + '  <node\tid="%s">\n    <operator>%s</operator>\n' % (Sources_GrapXML[key][1][0],Sources_GrapXML[key][0])
            xmlAppData = xmlAppData + '  <node\tid="%s">\n    <displayPosition x="%s.0" y="%s.0"/>\n  </node>\n' % (Sources_GrapXML[key][1][0],str(x),str(y))
            xml_sources = '    <sources>\n      <sourceProduct refid="%s"/>\n    </sources>\n' % Sources_GrapXML[key][2][-1]
            xml_parameters = '    <parameters class="com.bc.ceres.binding.dom.XppDomElement">\n'
            for parameter in Parameters_GraphXML[key].keys():
                if parameter == 'trainingVectors':
                    xml_parameters = xml_parameters + '      <%s>%s</%s>\n' % (parameter,','.join(Parameters_GraphXML[key][parameter]),parameter)
                elif parameter == 'featureBands':
                     xml_parameters = xml_parameters + '      <%s>%s</%s>\n' % (parameter,','.join(np.asarray(Parameters_GraphXML[key][parameter]).reshape(1,-1).tolist()[0]),parameter)
                else:
                    if Parameters_GraphXML[key][parameter] == '':
                        xml_parameters = xml_parameters + '      <%s/>\n' % parameter
                    else:
                        xml_parameters = xml_parameters + '      <%s>%s</%s>\n' % (parameter,Parameters_GraphXML[key][parameter],parameter)
            xml_parameters = xml_parameters + '    </parameters>\n'
            xmlGraph = xmlGraph + xml_sources + xml_parameters
            xmlGraph = xmlGraph + '  </node>\n'
                
        elif key == 'LabeLClasses':
            x = 700
            y = 10
            xmlGraph = xmlGraph + '  <node\tid="%s">\n    <operator>%s</operator>\n' % (Sources_GrapXML[key][1][0],Sources_GrapXML[key][0])
            xmlAppData = xmlAppData + '  <node    id="%s">\n\t\t<displayPosition x="%s.0" y="%s.0"/>\n  </node>\n' % (Sources_GrapXML[key][1][0],str(x),str(y))
            xml_sources = '    <sources>\n      <sourceProduct refid="%s"/>\n    </sources>\n' % Sources_GrapXML[key][2][0]
            xml_parameters = '    <parameters class="com.bc.ceres.binding.dom.XppDomElement">\n'
            xml_parameters = xml_parameters + '      <targetBands>\n'
            xml_parameters = xml_parameters  + '        <targetBand>\n'
            for parameter in Parameters_GraphXML[key].keys():
                if Parameters_GraphXML[key][parameter] == '':
                    xml_parameters = xml_parameters + '          <%s/>\n' % parameter
                else:
                    xml_parameters = xml_parameters + '          <%s>%s</%s>\n' % (parameter,Parameters_GraphXML[key][parameter],parameter)
            xml_parameters = xml_parameters + '        </targetBand>\n'
            xml_parameters = xml_parameters + '      </targetBands>\n'
            xml_parameters = xml_parameters + '      <variables/>\n'
            xml_parameters = xml_parameters + '    </parameters>\n'
            xmlGraph = xmlGraph + xml_sources + xml_parameters
            xmlGraph = xmlGraph + '  </node>\n'  
        
        
        else:
            x += 150
            y += 100
            xmlGraph = xmlGraph + '  <node\tid="%s">\n    <operator>%s</operator>\n' % (Sources_GrapXML[key][1][0],Sources_GrapXML[key][0])
            xmlAppData = xmlAppData + '  <node\tid="%s">\n    <displayPosition x="%s.0" y="%s.0"/>\n  </node>\n' % (Sources_GrapXML[key][1][0],str(x),str(y))
            if key == 'Merge_LC_Confi':
                for i in range(0, len(Sources_GrapXML[key][2])):
                    if i == 0:
                        xml_sources = '    <sources>\n      <sourceProduct refid="%s"/>\n' % (Sources_GrapXML[key][2][i])
                    else:
                        xml_sources = xml_sources + '      <sourceProduct.%s refid="%s"/>\n    </sources>\n' % (i,Sources_GrapXML[key][2][i])
            else:
                xml_sources = '    <sources>\n      <sourceProduct refid="%s"/>\n    </sources>\n' % Sources_GrapXML[key][2][0]
            xml_parameters = '    <parameters class="com.bc.ceres.binding.dom.XppDomElement">\n'
            for parameter in Parameters_GraphXML[key].keys():
                if Parameters_GraphXML[key][parameter] == '':
                    xml_parameters = xml_parameters + '      <%s/>\n' % parameter
                else:
                    xml_parameters = xml_parameters + '      <%s>%s</%s>\n' % (parameter,Parameters_GraphXML[key][parameter],parameter)
            xml_parameters = xml_parameters + '    </parameters>\n'
            xmlGraph = xmlGraph + xml_sources + xml_parameters
            xmlGraph = xmlGraph + '  </node>\n'  
          
    xmlAppData = xmlAppData + '\t</applicationData>\n'
    xmlGraph = xmlGraph +xmlAppData + '</graph>\n'        
                        
    file = open(xmlfile, 'w')
    file.write(xmlGraph)
    file.close()
    
    
    
    
def do_unzip_sentinel(input_path, outpath):
    filepath=ZipFile(input_path)
    ZipFile.extractall(filepath, outpath)

def AOI_TO_Geom(N, W, E, S):
    geom = "POLYGON ((%s %s, %s %s, %s %s, %s %s, %s %s))"  % (W,N,E,N,E,S,W,S,W,N)
    return geom

def RandomForestAlgorithm(RS_Images, ground_control_points, AOI,ris,xmlfile,NumbTrees, NumbTrainSamples, Outfilename, OutFormat):

    # raw_sentinel_path = '\\'.join(filepath.split('\\')[:-2])+'\\RAW_SENTINEL'
    # if not os.path.exists(raw_sentinel_path):
    #     os.makedirs(raw_sentinel_path)
    # do_unzip_sentinel(filepath, raw_sentinel_path)
    # file_Sentinel = raw_sentinel_path + '\\'+ filepath.split('\\')[-1][:-4] + '.SAFE'
    # print ('Extracting %s in \t %s' % (filepath, file_Sentinel))
    # file_input = file_Sentinel+'\\'+'manifest.safe'

    polygon = AOI_TO_Geom(AOI['N'],AOI['W'],AOI['E'],AOI['S'])
    Write_XML_FILE(RS_Images, ground_control_points, polygon,ris,xmlfile,NumbTrees, NumbTrainSamples, Outfilename, OutFormat)
    
    gpt_Command = "gpt %s " % xmlfile
    print ('\n invoking: ' + gpt_Command)
    try:
        process = subprocess.Popen(gpt_Command,
                                    shell=True,
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, )
        # Reads the output and waits for the process to exit before returning
        stdout, stderr = process.communicate()
        print (stdout)
        if stderr:
            raise Exception(stderr)  # or  if process.returncode:
        if 'Error' in stdout:
            raise Exception()
    except Exception as message:
            print(str(message))
            

    return Outfilename


