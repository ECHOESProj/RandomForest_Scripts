import os 
from LandCoverClass_Pre_Process import RandomForestAlgorithm, do_unzip_sentinel
from Subset_Pre_Process import SubsetImages
from RIS_Pre_Process import RIS_Images

def main():
    #DYFI AREA'
    # Country = 'Wales'
    # Name_AOI = 'Dyfi'
    # Year_Col_Dat = '2021'
    # AOI = {'N': '52.65',
    #         'E': '-3.86',
    #         'W': '-4.17',
    #         'S': '52.45'}
    
    # #CEFNI AREA
    Country = 'Wales'
    Year_Col_Dat = '2022'
    Name_AOI = 'Cefni'
    # AOI = {'N': '53.38',
    #         'E': '-4.19',
    #         'W': '-4.5',
    #         'S': '53.1'} 
    Side = 'SouthSide'
    AOI = {'N': '53.24',
            'E': '-4.19',
            'W': '-4.5',
            'S': '53.1'} 
    # Side = 'NorthSide'
    # AOI = {'N': '53.38',
    #         'E': '-4.19',
    #         'W': '-4.5',
    #         'S': '53.24'} 
    
    
    
    
    
    # # # BALLYGEITE AREA   
    # Country = 'Ireland'
    # Name_AOI = 'Ballyteige'
    # Year_Col_Dat = '2022'
    # AOI = {'N': '52.32',
    #         'E': '-6.3',
    #         'W': '-6.9',
    #         'S': '52.16'}
    
    # # WEXFORD AREA     
    # Country = 'Ireland'
    # Name_AOI = 'Wexford'
    # Year_Col_Dat = '2022'
    # AOI = {'N': '52.44',
    #         'E': '-6.3',
    #         'W': '-6.61',
    #         'S': '52.24'}
    
    
    # folder_root = r'C:\Users\wcamaro\Documents\ECHOES\06Datasets\WP5\To_ECHOES_Platform\Mapping' 
    folder_root = r'E:\To_ECHOES_Platform\Mapping'
    folder_AOI = folder_root + r'\%s\%s' % (Country,Name_AOI)
    
    #Cefni
    #do_unzip_sentinel(folder_AOI+r'\01_SatelliteImages\01_Raw_files\%s' % Side, folder_AOI+r'\01_SatelliteImages\02_Safe_files\%s' % Side )
    sorted_safes = sorted(os.listdir(folder_AOI+r'\01_SatelliteImages\02_Safe_files\%s' % Side), key = lambda x: x.split('_')[2])
    filenames = [folder_AOI+r'\01_SatelliteImages\02_Safe_files\%s' % Side +'\\'+f+'\\MTD_MSIL2A.xml'  for f in sorted_safes]
    GCP_classes = [vf for vf in (os.listdir(folder_AOI+r'\03_VegetationSurvey\%s\VectorFiles' % Side)) if vf[-3:]=='shp']
    GCP_classes.sort()
    Ground_Control_Points = [folder_AOI+r'\03_VegetationSurvey\%s\VectorFiles' % Side + '\\' + gcp  for gcp in GCP_classes]
    
  
    
    # do_unzip_sentinel(folder_AOI+r'\01_SatelliteImages\01_Raw_files', folder_AOI+r'\01_SatelliteImages\02_Safe_files' )
    # sorted_safes = sorted(os.listdir(folder_AOI+r'\01_SatelliteImages\02_Safe_files'), key = lambda x: x.split('_')[2])
    # filenames = [folder_AOI+r'\01_SatelliteImages\02_Safe_files'+'\\'+f+'\\MTD_MSIL2A.xml'  for f in sorted_safes]
    # GCP_classes = [vf for vf in (os.listdir(folder_AOI+r'\03_VegetationSurvey\VectorFiles')) if vf[-3:]=='shp']
    # GCP_classes.sort()
    # Ground_Control_Points = [folder_AOI+r'\03_VegetationSurvey\VectorFiles' + '\\' + gcp  for gcp in GCP_classes]
    
    Random_Forest_Parameters = {'NumbTrees': 500,
           'NumbTrainSamples': 5000}
    
  

    
    Radiometric_Indices = ('NDVI', 'SIPI', 'NDWI')
    
    xmlfile_subset = folder_root + r'\Algorithm\xml_files\SubsetAOI_%s_%s.xml'  % (Year_Col_Dat, Name_AOI)
    xmlfile_RIS = folder_root + r'\Algorithm\xml_files\RadiometricIndices_%s_%s.xml'  % (Year_Col_Dat, Name_AOI)
    xmlfile_randomforest = folder_root + r'\Algorithm\xml_files\RandomForest_%s_%s_LabelBand_%s_%s_%s.xml' % (str(Random_Forest_Parameters['NumbTrees']), str(Random_Forest_Parameters['NumbTrainSamples']),Year_Col_Dat, Country, Name_AOI)
    
    #Cefni
    Out_folder_subset = folder_AOI + r'\01_SatelliteImages\03_Subset_Images\%s' % Side
    Out_folder_RIS = folder_AOI + r'\01_SatelliteImages\04_Radiometric_Indices\%s' % Side
    Out_folder_RF = folder_AOI + r'\04_RandomForest_Outcomes\%s' % Side
        
    # Out_folder_subset = folder_AOI + r'\01_SatelliteImages\03_Subset_Images'
    # Out_folder_RIS = folder_AOI + r'\01_SatelliteImages\04_Radiometric_Indices'
    # Out_folder_RF = folder_AOI + r'\04_RandomForest_Outcomes'
    
    Out_filenames_subset = [Out_folder_subset +r'\Subset_'+ nam+'.tif' for nam in [sf.split('.')[:-1][0] for sf in sorted_safes]]
    Out_filenames_RIS = [Out_folder_RIS +r'\Subset_'+ nam for nam in [sf.split('.')[:-1][0] for sf in sorted_safes]]
    Outfilename_RF = Out_folder_RF +'\\'+ r'RadiomIndices_%s_%s_%s_RandomForest_%s_%s_ECHOES_Codes.tif' % (Country,Name_AOI, Year_Col_Dat, str(Random_Forest_Parameters['NumbTrees']), str(Random_Forest_Parameters['NumbTrainSamples']))
    
        
    OutFormat = 'GeoTIFF'
    
    # SubsetImages(filenames, AOI, xmlfile_subset, Out_filenames_subset, OutFormat)
    # RIS_Images(filenames, AOI,Radiometric_Indices,xmlfile_RIS, Out_filenames_RIS, OutFormat)
    RandomForestAlgorithm(filenames, Ground_Control_Points, AOI,Radiometric_Indices,xmlfile_randomforest,Random_Forest_Parameters['NumbTrees'],Random_Forest_Parameters['NumbTrainSamples'], Outfilename_RF, OutFormat, Name_AOI)
    print ('Thanks_Process_Finished ' )

if __name__ == '__main__':
    main()

