Since we are all working in python, this would be a little easier.

For ML guys take note:
1) Look at extractDataset.py
2) the function extractDataset should extract your data and return you a list containing all the dancemoves
3) each dancemove is encapsulated in an instance of the dancemove class
4) please refer to the dancemove class to see what attributes there are:
    a) self.a_xList --> accleration x axis ....
    b) self.g_xList --> gyro x axis ....
    c) self.activation_List --> 0 == no move, 1 == ready, 2 == currently dancing
    d) self.movename == <the name of the dance move> ie 'wipetable' (this is basically the true label for ML)

To use:
1) put the datasets you want in raw (the full set should aready be there when i push this code)
2) run extractDataset.py. The result of processData() contains the results you need. you can feed it into your ML from there. 
3) if you want to export it, you can pickle the resulting list and cache the results. refer to https://docs.python.org/3/library/pickle.html


============Parameters that can be changed============

NUMBER_OF_AFTER_SAMPLES = 5 #Number of samples to include in dance move after end detected
NUMBER_OF_BEFORE_SAMPLES = 20 #Number of samples to include in dance move before start detected
MINIMUM_MOVE_TIME =20 #Minimum number of samples to be considered a move. Set this too low and you will get garbage dance samples

