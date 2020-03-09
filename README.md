Docker container for python based Geant4 application

docker run --network=host -e DISPLAY=$DISPLAY  -it -v /home/rnarayan:/home/rnarayan  rotiyan/geant4-10.6
python demo.py
