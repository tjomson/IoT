const { spawn } = require("child_process")

async function doStuff() {
    const nodeId = process.argv[2]
    const sshProcess = spawn("ssh", ["-L", `20000:pycom-${nodeId}:20000`, "itu2023iot2@strasbourg.iot-lab.info"])
    sshProcess.on("error", () => console.log("ssh process broke"))
    sshProcess.on("exit", () => console.log("ssh process closed"))
    await sleep(1000)

    const socatProcess = spawn("socat", ["-d", "-v", "PTY,link=/tmp/ttyPYC0,crnl,echo=0", "TCP:localhost:20000"])
    socatProcess.on("error", () => console.log("socat process broke"))
    socatProcess.on("exit", () => console.log("socat process closed"))
    await sleep(1000)
    
    spawn('rshell', ["-f ./rshell_commands.txt"], {
        stdio: 'inherit',
        shell: true
    })
}

function sleep(ms) {
    return new Promise((resolve) => {
        setTimeout(resolve, ms);
    });
}

doStuff()