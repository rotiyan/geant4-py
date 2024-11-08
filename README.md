# Docker container for python based Geant4 application

Geant4 is a toolkit for performing simulation of propagation of subatomic particles through matter.  This toolkit is used extensively by high energy physics community to design detector components of particle physics experiments. 

This repo hosts the following 
1) A docker file for creating geant4 toolkit with an extensive python binding for ease of user interaction.  A docker image exisst in dockerhub and you can run this container with the following command
docker run --network=host -it -v /home/rnarayan/:/home/rnarayan -p 9999  rotiyan/geant4-10.6
2) A Gallium Nitride power semiconductor geometry to study atmospheric neutron induced single event gate rupture https://ieeexplore.ieee.org/abstract/document/10254566
