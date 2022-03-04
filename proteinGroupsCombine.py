#python proteinGroupsCombine.py L:\promec\TIMSTOF\LARS\2022\januar\220119_ELise_rerun
import sys
from pathlib import Path
if len(sys.argv)!=2: sys.exit("\n\nREQUIRED: pandas, pathlib; tested with Python 3.9 \n\nUSAGE: python proteinGroupsCombine.py <path to folder containing proteinGroups.txt file(s) like \"L:\promec\Animesh\Samah\mqpar.xml.1623227664.results\" >\n\nExample\n\npython proteinGroupsCombine.py L:\promec\TIMSTOF\LARS\2022\januar\220119_ELise_rerun")
pathFiles = Path(sys.argv[1])
#pathFiles=Path("L:/promec/TIMSTOF/LARS/2022/januar/220119_ELise_rerun")
fileName='proteinGroups.txt'
trainList=list(pathFiles.rglob(fileName))
#trainList=list([Path('L:/promec/TIMSTOF/LARS/2021/November/combined/txt/proteinGroups.txt'),Path('L:/promec/TIMSTOF/LARS/2021/Desember/211207_Nilu/combined/txt/proteinGroups.txt'),Path('L:/promec/TIMSTOF/LARS/2021/Desember/211221_Nilu/combined/txt/proteinGroups.txt')])
#!pip3 install pandas --user
import pandas as pd
#df = pd.concat(map(pd.read_table, trainList))
#df.to_csv(pathFiles.with_suffix('.combinedT.txt'),sep="\t")#,rownames=FALSE)
#f=trainList[1]
dfI=pd.DataFrame()
dfC=pd.DataFrame()
dfB=pd.DataFrame()
i=0
for f in trainList:
    i=i+1
    if Path(f).stat().st_size > 0:
        proteinHits=pd.read_csv(f,low_memory=False,sep='\t')
        print(i,f.parts[-3],f.parts[-4],f.parts[-5])
        proteinHits.rename({'Protein IDs':'ID'},inplace=True,axis='columns')
        proteinHitsC=proteinHits.ID.str.split(';', expand=True).set_index(proteinHits.Score).stack().reset_index(level=0, name='ID')
        proteinHitsI=proteinHits.ID.str.split(';', expand=True).set_index(proteinHits.Intensity).stack().reset_index(level=0, name='ID')
        proteinHitsB=proteinHits.ID.str.split(';', expand=True).set_index(proteinHits.iBAQ).stack().reset_index(level=0, name='ID')
        proteinHitsI['Name']=f.parts[-3]+f.parts[-4]+f.parts[-5]+str(i)
        proteinHitsC['Name']=f.parts[-3]+f.parts[-4]+f.parts[-5]+str(i)
        proteinHitsB['Name']=f.parts[-3]+f.parts[-4]+f.parts[-5]+str(i)
        dfI=pd.concat([dfI,proteinHitsI],sort=False)
        dfC=pd.concat([dfC,proteinHitsC],sort=False)
        dfB=pd.concat([dfB,proteinHitsB],sort=False)
print(dfI.columns)
print(dfC.columns)
print(dfB.columns)
dfI=dfI.pivot(index='ID', columns='Name', values='Intensity')
dfC=dfC.pivot(index='ID', columns='Name', values='Score')
dfB=dfB.pivot(index='ID', columns='Name', values='iBAQ')
#df.to_csv(pathFiles.with_suffix('.combined.txt'),sep="\")#,rownames=FALSE)
#writeDPpng=pathFiles/(fileName+"Score.png")
#df.plot(kind='hist').figure.savefig(writeDPpng.absolute(),dpi=100,bbox_inches = "tight")
#print("Histogram of Score in",writeDPpng)
dfI['SumI']=dfI.sum(axis=1)
dfB['SumB']=dfB.sum(axis=1)
dfC['SumC']=dfC.sum(axis=1)
dfI=dfI.sort_values('SumI',ascending=False)
dfB=dfB.sort_values('SumB',ascending=False)
dfC=dfC.sort_values('SumC',ascending=False)
dfI.to_csv(pathFiles/(fileName+"Combo.intensity.csv"))#.with_suffix('.combo.csv'))
histScores=pathFiles/(fileName+"HistInt.svg")
import numpy as np
log2dfI=dfI.fillna(0)
log2dfI=np.log2(log2dfI+1)
log2dfI=log2dfI.drop('SumI',axis=1)
log2dfI.plot(kind='hist',alpha=0.5,bins=100).figure.savefig(histScores,dpi=100,bbox_inches = "tight")
log2dfI.columns
print("Scatter of First 2 Intensities in",pathFiles/(fileName+"Scatter.svg"))
import seaborn as sns
sns.jointplot(y=log2dfI.iloc[:,0],x=log2dfI.iloc[:,1], ).figure.savefig(pathFiles/(fileName+"Scatter.svg"),dpi=100,bbox_inches = "tight")#,kind="reg")
#sns.jointplot(data=log2dfI,y='Oslo220119_ELise_rerunjanuar2', x='combined220119_ELise_rerunjanuar1').figure.savefig(pathFiles/(fileName+"Scatter.svg"),dpi=100,bbox_inches = "tight")#,kind="reg")
#sns.jointplot(data=log2dfI[:,1:2])#,kind="reg")
dfB.to_csv(pathFiles/(fileName+"Combo.ibaq.csv"))#.with_suffix('.combo.csv'))
print("Histogram of iBAQ in",pathFiles/(fileName+"iBAQhist.svg"))
dfC.plot(kind='hist',alpha=0.5,bins=100).figure.savefig(pathFiles/(fileName+"iBAQhist.svg"),dpi=100,bbox_inches = "tight")
dfC.to_csv(pathFiles/(fileName+"Combo.score.csv"))#.with_suffix('.combo.csv'))
print("Histogram of Scores in",pathFiles/(fileName+"ScoresHist.svg"))
dfC.plot(kind='hist',alpha=0.5,bins=100).figure.savefig(pathFiles/(fileName+"ScoresHist.svg"),dpi=100,bbox_inches = "tight")
#dfID=df.assign(ID=df.ID.str.split(';')).explode('ID')
dfLFQ=dfC
dfLFQ=dfI
i=0
for f in trainList:
    i=i+1
    if Path(f).stat().st_size > 0:
        print(i,f.parts[-3],f.parts[-4],f.parts[-5])
        proteinHits=pd.read_csv(f,low_memory=False,sep='\t')
        proteinHitsLFQ=proteinHits.assign(ID=proteinHits['Protein IDs'].str.split(';')).explode('ID')
        proteinHitsLFQ.index=proteinHitsLFQ['ID']
        proteinHitsLFQ=proteinHitsLFQ.add_suffix(f.parts[-3]+f.parts[-4]+f.parts[-5]+'F'+str(i))
        dfLFQ=pd.concat([dfLFQ,proteinHitsLFQ],axis=1)
print(dfLFQ.columns)
#dfLFQ['211207_NiluDesember2'].hist()
#(dfLFQ['211221_NiluDesember3']-dfLFQ['Score211221_NiluDesemberF3']).hist()
dfLFQ.to_csv(pathFiles/(fileName+"Combo.csv"))
dfS=dfLFQ.filter(like='Peptide sequence', axis=1)
#dfS=dfLFQ[:,[dfLFQ.filter(like='Peptide sequence', axis=1)]].apply(lambda x: ''.join(x), axis=1)
dfLFQPeptides=dfS[dfS.columns].apply(lambda x:','.join(x.dropna().astype(str)),axis=1)
#dfLFQPeptides['C9J1R6']#EFPDLGAHCSEPSCQR
#dfLFQPeptides.filter(like='HTSALCNSCR')#EFPDLGAHCSEPSCQR,HPLDHDCSGEGHPTSR;HRHPLDHDCSGEGHPTSR,HPLDHDCSGEGHPTSR;HRHPLDHDCSGEGHPTSR
dfLFQPeptides.to_csv(pathFiles/(fileName+"dfLFQPeptides.csv"))
dfLFQvals=dfLFQ.filter(like='LFQ', axis=1)
#dfLFQvals=dfLFQ.filter(like='Intensity', axis=1)
dfLFQvals.to_csv(pathFiles/(fileName+"dfLFQvals.csv"))
dfLFQvalsSeqs=pd.concat([dfLFQvals,dfLFQPeptides],axis=1)
dfLFQvalsSeqs.to_csv(pathFiles/(fileName+"dfLFQvalsSeqs.csv"))
dfLFQvalsSeqsMedian=dfLFQvalsSeqs.groupby(0).median()
dfLFQid=dfLFQPeptides.reset_index()
dfLFQidC=dfLFQid.groupby(0).agg({'ID': ';'.join})
dfLFQvalsSeqsUni=pd.concat([dfLFQidC,dfLFQvalsSeqsMedian],axis=1)
dfLFQvalsSeqsUni.to_csv(pathFiles/(fileName+"dfLFQvalsSeqsUni.csv"))
log2dfLFQvalsSeqsUni=dfLFQvalsSeqsUni.fillna(0)
log2dfLFQvalsSeqsUni.index=log2dfLFQvalsSeqsUni['ID']
log2dfLFQvalsSeqsUni=log2dfLFQvalsSeqsUni.drop(['ID'], axis=1)
log2dfLFQvalsSeqsUni=np.log2(log2dfLFQvalsSeqsUni+1)
#log2dfLFQvalsSeqsUni.hist()#.figure.savefig(pathFiles/(fileName+"log2dfLFQvalsSeqsUni.hist.svg"),dpi=100,bbox_inches = "tight")
log2dfLFQvalsSeqsUni.to_csv(pathFiles/(fileName+"log2dfLFQvalsSeqsUni.csv"))
log2dfLFQvalsSeqsUni.plot(kind='hist',alpha=0.5,bins=100).figure.savefig(pathFiles/(fileName+"log2dfLFQvalsSeqsUni.svg"),dpi=100,bbox_inches = "tight")