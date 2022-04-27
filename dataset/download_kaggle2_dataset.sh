
wget https://www.kaggle.com/datasets/mrgeislinger/asl-rgb-depth-fingerspelling-spelling-it-out/download
unzip archive.zip
mv archive non_bbox_large
cd non_bbox_large
mv A train1
mv B train2
mv C train3
mv D test1
mv E test1
cd ..
rm archive.zip
