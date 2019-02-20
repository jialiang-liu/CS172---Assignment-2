#!/bin/bash

checkPython() {
	version=3
	temp=`python3 -V 2>&1|awk '{print $2}'`
	if [[ $temp==3* ]];
	then
		uv1=`python3 -V 2>&1|awk '{print $2}'|awk -F '.' '{print $1}'`
		uv2=`python3 -V 2>&1|awk '{print $2}'|awk -F '.' '{print $2}'`
		uv3=`python3 -V 2>&1|awk '{print $2}'|awk -F '.' '{print $3}'`
	else
		uv1=`python -V 2>&1|awk '{print $2}'|awk -F '.' '{print $1}'`
		uv2=`python -V 2>&1|awk '{print $2}'|awk -F '.' '{print $2}'`
		uv3=`python -V 2>&1|awk '{print $2}'|awk -F '.' '{print $3}'`
	fi
	if [ $uv1 -lt $version ];
	then
		echo Your Python version is $uv1.$uv2.$uv3, but this program need Python 3 to run.
		read -p "Do you want to install Python 3 [Y/n]: " -t 20 flag
		if [ "$flag" == "Y" -o "$flag" == "y" ];
		then
			read -p "Please choose your operating system: 1 RedHat; 2 Debian; 3 MacOS " -t 30 plat
			if [ "$plat" == "1" ];
			then
				sudo yum install python34
				wget --no-check-certificate https://bootstrap.pypa.io/get-pip.py
				python3 get-pip.py
				sudo yum install python-devel
			elif [ "$plat" == "2" ];
			then
				sudo apt-get install python3
				sudo apt-get install python3-pip
			elif [ "$plat" == "3" ];
			then
				wget https://www.python.org/ftp/python/3.6.8/Python-3.6.8.tgz
				tar -zxvf Python-3.6.8.tgz
				cd Python-3.6.8
				./configure prefix=/usr/local/bin/Python3
				make
				make install
			else
				exit 1
			fi
		else
			echo This shell is aborted. Nothing has been changed.
			exit 1
		fi
	else
		echo Version checking for Python is finished.
	fi
	if python3 -c "import numpy" >/dev/null 2>&1;
	then
		echo numpy was installed, no change needs to be done.
	else
		echo Installing numpy...
		pip3 install numpy
	fi
	if python3 -c "import nltk" >/dev/null 2>&1;
	then
		echo nltk was installed, no change needs to be done.
	else
		echo Installing nltk...
		pip3 install nltk
	fi
	if python3 -c "import nltk.tokenize" >/dev/null 2>&1 -o python3 -c "import nltk.stem" -o python3 -c "import nltk.corpus";
	then
		echo nltk_data were installed, no change needs to be done.
	else
		echo Installing nltk_data, it may take a while...
		chmod a+x ./nltk_download.py
		sudo python3 -m nltk.downloader all-corpora
	fi
	echo All checks are done, thank you for waiting. Now running the program.
	echo
	echo ------------------------------------------------------------------------------
}
clear
checkPython
chmod a+x ./project.py
echo
python3 ./project.py
echo
echo ---------------------------------ALL FINISHED---------------------------------
echo
