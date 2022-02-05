#!python -m pip install -q git+https:/hub.com/wilhelm-lab/dlomix
#awk -F '\t' '{if($7="Unmodified"){sep=",";print $4,sep,$30}}' /home/ash022/PD/TIMSTOF/LARS/2022/januar/220119_Elise/combined/txt/msms.txt > train.csv
#sed 's/Sequence/sequence/' train.csv > train2.csv
#sed 's/Retention\ time/irt/' train2.csv > train.csv 
#sed 's/ //g' train.csv  > train2.csv
#awk -F '\t' '{if($7="Unmodified"){sep=",";print $4,sep,$30}}' /home/ash022/PD/TIMSTOF/LARS/2022/januar/220119_ELise_rerun/combined/txt/msms.txt > test.csv
#sed 's/Sequence/sequence/' test.csv > test2.csv
#sed 's/Retention\ time/irt/' test2.csv > test.csv 
#sed 's/ //g' test.csv  > test2.csv
#python dlomixRT.py test2.csv  train2.csv 
import sys
import numpy as np
import pandas as pd
import dlomix
from dlomix import constants, data, eval, layers, models, pipelines, reports, utils
print([x for x in dir(dlomix) if not x.startswith("_")])
from dlomix.data import RetentionTimeDataset
#TRAIN_DATAPATH = 'https://raw.githubusercontent.com/wilhelm-lab/dlomix/develop/example_dataset/proteomTools_train_val.csv'
TRAIN_DATAPATH = sys.argv[1]#'proteomTools_train_val.csv'
BATCH_SIZE = 64
rtdata = RetentionTimeDataset(data_source=TRAIN_DATAPATH,seq_length=30, batch_size=BATCH_SIZE, val_ratio=0.2, test=False)
print( "Training examples", BATCH_SIZE * len(rtdata.train_data))
print("Validation examples", BATCH_SIZE * len(rtdata.val_data))
from dlomix.models import RetentionTimePredictor
model = RetentionTimePredictor(seq_length=30)
from dlomix.eval import TimeDeltaMetric
model.compile(optimizer='adam',loss='mse',metrics=['mean_absolute_error', TimeDeltaMetric()])
history = model.fit(rtdata.train_data,validation_data=rtdata.val_data,epochs=20)
#TEST_DATAPATH = 'https://raw.githubusercontent.com/wilhelm-lab/dlomix/develop/example_dataset/proteomTools_test.csv'
TEST_DATAPATH = sys.argv[2]#'proteomTools_test.csv'
test_rtdata = RetentionTimeDataset(data_source=TEST_DATAPATH,seq_length=30, batch_size=32, test=True)
predictions = model.predict(test_rtdata.test_data)
predictions = predictions.ravel()
test_targets = test_rtdata.get_split_targets(split="test")
print(test_targets, predictions)
save_path = "rtmodel"
model.save_weights(save_path)
trained_model = RetentionTimePredictor(seq_length=30)
trained_model.load_weights(save_path)
new_predictions = trained_model.predict(test_rtdata.test_data)
new_predictions = new_predictions.ravel()
print(np.allclose(predictions, new_predictions))
results_df = pd.DataFrame({"sequence": test_rtdata.sequences,"irt": test_rtdata.targets,"predicted_irt": predictions})
print(results_df)
results_df.to_csv("predictions_irt.csv", index=False)
print(pd.read_csv("predictions_irt.csv"))
