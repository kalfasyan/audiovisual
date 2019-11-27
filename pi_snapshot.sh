# SETTING OPTION FLAGS
while getopts i:p: option
do
case "${option}"
in
i) INDEX=${OPTARG};;
p) PI_INDEX=${OPTARG};;
esac
done

if [ $# -eq 0 ]
  then
    echo "No arguments supplied. Give -p for RPi and -i for img index"
    echo "-p 0  # for RPi3."
    echo "-p 1  # for top Pi0."
    echo "-p 2  # for bottom Pi0"
    echo "You can pass an index with -i to include in the image name."
    echo "-r and -b are the gains for Red and Blue respectively."
    exit 1
fi

if [ $PI_INDEX = 0 ]; then
    # name of calib picture
    PICTURE_NAME='/home/pi/FOTOBOX/calib_images/RPi4_p0_i'$INDEX'.jpg'
    echo 'Connecting to PI_INDEX and taking picture'
    raspistill -t 1000 -dg 1.0 -awb off -awbg 0.92,2.7 -o $PICTURE_NAME &
    echo 'Done.'
    exit 0
fi

# name of calib picture
PICTURE_NAME='RPi0_p'$PI_INDEX'_i'$INDEX'.jpg'
echo 'Connecting to RPi Zero with index '$PI_INDEX' and taking picture'
echo '..'

if [ $PI_INDEX = 1 ]; then
    ssh -tTo ServerAliveInterval=60 pi@10.0.1$PI_INDEX.2 'raspistill -t 1000 -dg 1.0 -awb off -awbg 0.92,2.8 -o '$PICTURE_NAME 
elif [ $PI_INDEX = 2 ]; then
    ssh -tTo ServerAliveInterval=60 pi@10.0.1$PI_INDEX.2 'raspistill -t 1000 -dg 1.0 -awb off -awbg 0.99,2.87 -o '$PICTURE_NAME 
else
    echo 'Wrong RPi index passed.'
    exit 0
fi

sleep 2
echo 'Transferring picture from RPi Zero with index '$PI_INDEX
rsync -a pi@10.0.1$PI_INDEX.2:/home/pi/$PICTURE_NAME calib_images/ &
echo 'Done.'

exit 0
