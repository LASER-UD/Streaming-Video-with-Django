sudo apt-get update 
sudo apt-get upgrade
sudo apt-get autoremove 
sudo apt-get install python-setuptools 
wget  https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
sudo rm -rf get-pip.py
#Dependencias para opencv2
sudo apt-get install libcblas-dev 
sudo apt-get install libhdf5-dev  
sudo apt-get install libhdf5-serial-dev
sudo apt-get install libatlas-base-dev 
sudo apt-get install libjasper-dev
sudo apt-get install libqtgui4
sudo apt-get install libqt4-test
#Nginx
sudo apt-get install redis-server
sudo apt-get install nginx
#Error de service_
sudo apt-get install python-dev libffi-dev libssl-dev libxml2-dev libxslt1-dev libjpeg8-dev
sudo easy_install service_identity
