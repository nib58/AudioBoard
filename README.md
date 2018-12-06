TO SEND POST TYPE COMMAND:

r = requests.post('http://localhost:5000/send_waveform/', data ={'prediction':'prediction'})

TO RUN:

cd to directory and post following commands

export FLASK_APP='audioBoard.py'
flask devinit
flask run
