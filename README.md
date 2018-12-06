TO SEND POST TYPE COMMAND:
prediction= 'string'
r = requests.post('http://localhost:5000/send_waveform/', data ={'prediction':prediction})
r = requests.post('http://10.215.63.19/send_waveform/', data ={'prediction':prediction})
10.215.63.19

TO RUN:

cd to directory and post following commands

export FLASK_APP='audioBoard.py'
flask devinit
flask run
