from LandCoverClass_Pre_Process import RandomForestAlgorithm


def main():
    filenames = (r'C:\Users\wcamaro\Documents\ECHOES\06Datasets\WP5\Sentinel_Images\Raw_Files\Wales\2019\S2B_MSIL2A_20191129T113329_N0213_R080_T30UVD_20191129T125010.SAFE\MTD_MSIL2A.xml',
                 r'C:\Users\wcamaro\Documents\ECHOES\06Datasets\WP5\Sentinel_Images\Raw_Files\Wales\2020\S2B_MSIL2A_20200414T112109_N0214_R037_T30UVD_20200414T132724.SAFE\MTD_MSIL2A.xml',
                 r'C:\Users\wcamaro\Documents\ECHOES\06Datasets\WP5\Sentinel_Images\Raw_Files\Wales\2020\S2A_MSIL2A_20200601T113331_N0214_R080_T30UVD_20200601T123416.SAFE\MTD_MSIL2A.xml',
                 r'C:\Users\wcamaro\Documents\ECHOES\06Datasets\WP5\Sentinel_Images\Raw_Files\Wales\2020\S2B_MSIL2A_20200921T112119_N0214_R037_T30UVD_20200921T132441.SAFE\MTD_MSIL2A.xml'
                 )
                 

    AOI = {'N': '52.65',
           'E': '-3.86',
           'W': '-4.17',
           'S': '52.45'}

    Ground_Control_Points = (r'C:\Users\wcamaro\Documents\ECHOES\06Datasets\WP5\Snap_Developments\RandomForest\Wales\Dyfi\VectorFiles\1110.shp',
                             r'C:\Users\wcamaro\Documents\ECHOES\06Datasets\WP5\Snap_Developments\RandomForest\Wales\Dyfi\VectorFiles\1210.shp',
                             r'C:\Users\wcamaro\Documents\ECHOES\06Datasets\WP5\Snap_Developments\RandomForest\Wales\Dyfi\VectorFiles\1220.shp',
                             r'C:\Users\wcamaro\Documents\ECHOES\06Datasets\WP5\Snap_Developments\RandomForest\Wales\Dyfi\VectorFiles\2100.shp',
                             r'C:\Users\wcamaro\Documents\ECHOES\06Datasets\WP5\Snap_Developments\RandomForest\Wales\Dyfi\VectorFiles\2110.shp',
                             r'C:\Users\wcamaro\Documents\ECHOES\06Datasets\WP5\Snap_Developments\RandomForest\Wales\Dyfi\VectorFiles\2200.shp',
                             r'C:\Users\wcamaro\Documents\ECHOES\06Datasets\WP5\Snap_Developments\RandomForest\Wales\Dyfi\VectorFiles\2300.shp',
                             r'C:\Users\wcamaro\Documents\ECHOES\06Datasets\WP5\Snap_Developments\RandomForest\Wales\Dyfi\VectorFiles\2320.shp',
                             r'C:\Users\wcamaro\Documents\ECHOES\06Datasets\WP5\Snap_Developments\RandomForest\Wales\Dyfi\VectorFiles\2330.shp',
                             r'C:\Users\wcamaro\Documents\ECHOES\06Datasets\WP5\Snap_Developments\RandomForest\Wales\Dyfi\VectorFiles\3000.shp',
                             r'C:\Users\wcamaro\Documents\ECHOES\06Datasets\WP5\Snap_Developments\RandomForest\Wales\Dyfi\VectorFiles\4000.shp',
                             r'C:\Users\wcamaro\Documents\ECHOES\06Datasets\WP5\Snap_Developments\RandomForest\Wales\Dyfi\VectorFiles\5000.shp',
                             r'C:\Users\wcamaro\Documents\ECHOES\06Datasets\WP5\Snap_Developments\RandomForest\Wales\Dyfi\VectorFiles\6100.shp',
                             r'C:\Users\wcamaro\Documents\ECHOES\06Datasets\WP5\Snap_Developments\RandomForest\Wales\Dyfi\VectorFiles\6200.shp'
                             )

    
    Radiometric_Indices = ('NDVI', 'SIPI', 'NDWI')
    xmlfile = r'C:\Users\wcamaro\Documents\ECHOES\06Datasets\WP5\Snap_Developments\RandomForest\RandomForest_2020_LabelBandWales_Dyfi.xml'
    
    Random_Forest_Parameters = {'NumbTrees': 10,
           'NumbTrainSamples': 50000}
    
    Outfilename = r'C:\Users\wcamaro\Documents\ECHOES\06Datasets\WP5\Snap_Developments\RandomForestOutcomes\2020\Wales\Dyfi\RadiomIndices_Dyfi_2020_RandomForest_ECHOES_Codes.tif'
    OutFormat = 'GeoTIFF'
    
    RandomForestAlgorithm(filenames, Ground_Control_Points, AOI,Radiometric_Indices,xmlfile,Random_Forest_Parameters['NumbTrees'],Random_Forest_Parameters['NumbTrainSamples'], Outfilename, OutFormat)
    print ('Thanks_Process_Finished ' )

if __name__ == '__main__':
    main()

