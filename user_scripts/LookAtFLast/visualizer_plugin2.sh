# load environment on cfeld-perc06
source /home/prcvlusr/PercAuxiliaryTools/Anaconda3/bin/activate root
#
# load environment on maxwell
#source /usr/share/Modules/init/sh
#module load anaconda/3
#
# execute
echo " "

echo "find last (de)scrambled img set, , show"
echo "SerFri2020 09 07 version includes: britisBits translation, big-to-small-endian translation, pad ordering ?7x32[44 times] => 7x(32*44)"
echo "plugin2 should include: Smp/Rst reorder, avoid DAQ disorder"
python3 ./Visualizer_plugin2.py
