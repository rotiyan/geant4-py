Docker container for python based Geant4 application

docker run --network=host -e DISPLAY=$DISPLAY  -it -v /home/rnarayan:/home/rnarayan  rotiyan/geant4-10.6

Run 
python demo.py

You could even start a jupyter notebook to make a g4py application 
