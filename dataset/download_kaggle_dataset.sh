
wget https://www.kaggle.com/datasets/grassknoted/asl-alphabet/download
unzip archive.zip
mv archive non_bbox_small
cd non_bbox_small
mv asl_alphabet_train/asl_alphabet_train ..
mv asl_alphabet_test/asl_alphabet_test ..
mv asl_alphabet_train train
mv asl_alphabet_test test
mv train/del clear
rm -r train/space
cd ..
rm archive.zip
