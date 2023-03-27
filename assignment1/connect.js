// import {spawn} from "child_process"
const { spawn, exec } = require("child_process")

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
    
    const child = spawn('rshell', [], {
        stdio: [process.stdin, process.stdout, process.stderr],
        shell: true
    })
    // child.stdin.setEncoding('utf-8');
    // child.stdout.pipe(process.stdout);
    // await sleep(500)
    // child.stdin.write('echo "Hello, world!"\n');
    // const shell = spawn('/bin/bash', [], { stdio: 'inherit' });
    // shell.on('spawn', () => {
    //     shell.stdin.write('echo "Hello, world!"\n');
    // })

    // rshellProcess.stdin.write('connect serial /tmp/ttyPYC0\n')
    // console.log("yo")
    // rshellProcess.stderr.on("data", () => {
    //     rshellProcess.stdin.write('connect serial /tmp/ttyPYC0\n')
    //     console.log("hej")
    //     rshellProcess.stdin.end()
    // })
    // rshellProcess.on("spawn", () => {
    //     exec('connect serial /tmp/ttyPYC0', { stdio: "inherit", cwd: rshellProcess.spawnargs[0]})
    // })
}

function sleep(ms) {
    return new Promise((resolve) => {
        setTimeout(resolve, ms);
    });
}

doStuff()