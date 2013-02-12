Welcome to ElpAPI, the python API for the Elphel cameras

This API serves the purpose of helping developers create applications that use [Elphel](http://elphel.com/) cameras.
In this repository there are two kinds of script:
	- The scripts and
	- The meta scripts

Scripts are the code that use the meta scripts of the API, and the meta scripts are the code that conforms the API.

The core of the API is in the meta script ElpAPI.py, and *autosetup.py* is the script that autosetups the camera,
if you want to know how it works you might chek both of those scripts.

# Installation
type `git clone git://github.com/BielBdeLuna/ElpAPI.git` in the folder you want the code to reside in.


# autosetup.py
In order to test it, you need to create am "elphel" directory in your user directory:

/home/yourusernamedir/elphel/

then there you need to have a XML that controls your wanted values to send to the camera, 
you can create that file straight from the camera by doing the following (CameraIP = insert your camera's IP here):

	* Setup the camera with the Exposure of your liking form within the php program in the camera (http://CameraIP/camvc.html)
	* `cd` to the Elphel directory generated above and call the following lines in the terminal:
	`wget 'http://cameraIP/parsedit.php?immediate&EXPOS&' -O wanted_settings.xml`
	* You'll then have a "wanted_settings.xml"-file in your folder
	* Reboot the, so it will have it's default EXPOS value (exposure value)
	* Call "autosetup.py" and the camera will change it's EXPOS value to the one you have in the XML.
