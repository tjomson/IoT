terminal 1: ssh -L 20000:pycom-13:20000 itu2023iot2@strasbourg.iot-lab.info
erstat 13 med id'et fra den givne proces

terminal 2: socat -d -v PTY,link=/tmp/ttyPYC0,crnl,echo=0 TCP:localhost:20000

terminal 3: rshell
