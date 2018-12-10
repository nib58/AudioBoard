TO SEND POST TYPE COMMAND:
prediction= 'string'
requests.post('http://localhost:5000/waveforms/', data = {'prediction':prediction})

TO RUN:

1. cd to directory and post following commands
2. export 'FLASK_APP'='audioBoard.py'
3. flask devinit
4. flask run
