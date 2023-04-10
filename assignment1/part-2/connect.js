const { spawn } = require("child_process")
const fs = require("fs")

function sleep(ms) {
    return new Promise((resolve) => {
        setTimeout(resolve, ms);
    });
}

function createDupes(nodeCount) {
    if (!fs.existsSync(`./macs`)) {
        fs.mkdirSync("./macs")
    }
    for (let i = 0; i < nodeCount; i++) {
        if (!fs.existsSync(`./macs/${i}`)) {
            fs.mkdirSync(`./macs/${i}`)
        }
        let file
        if (i === 0) {
            file = fs.readFileSync("./sourceNode/main.py", "utf-8").split("\n")
        } else if (i === nodeCount - 1) {
            file = fs.readFileSync("./sinkNode/main.py", "utf-8").split("\n")
        } else {
            file = fs.readFileSync("./transferNode/main.py", "utf-8").split("\n")
        }
        file[6] = `identifier = ${i}`
        fs.writeFileSync(`./macs/${i}/main.py`, file.join("\n"))
    }
}

async function deploy(nodeIds) {
    const connList = []
    for (let i = 0; i < nodeIds.length; i++) {
        connList.push("-L")
        connList.push(`2000${i}:pycom-${nodeIds[i]}:20000`)
    }

    console.log("ssh")
    const sshProcess = spawn("ssh", [...connList, "itu2023iot2@strasbourg.iot-lab.info"])
    sshProcess.on("error", () => console.log("ssh process broke"))
    sshProcess.on("exit", () => console.log("ssh process closed"))
    await sleep(3000)

    for (let i = 0; i < nodeIds.length; i++) {
        console.log("socat:", i)
        const socatProcess = spawn("socat", ["-d", "-v", `PTY,link=/tmp/ttyPYC${i},crnl,echo=0`, `TCP:localhost:2000${i}`])
        socatProcess.on("error", () => console.log(`socat process ${i} broke`))
        socatProcess.on("exit", () => console.log(`socat process ${i} closed`))
        await sleep(1000)
    }

    createDupes(nodeIds.length)

    let rshellCommands = []
    for (let i = 0; i < nodeIds.length; i++) {
        rshellCommands.push(`connect serial /tmp/ttyPYC${i}`)
    }
    rshellCommands.push("cp macs/0/main.py /pyboard/flash/main.py")
    
    for (let i = 2; i <= nodeIds.length; i++) {
        rshellCommands.push(`cp macs/${i-1}/main.py /pyboard-${i}/flash/main.py`)
    }

    fs.writeFileSync("commands.txt", rshellCommands.join("\n"))
    console.log("rshell")
    const rshellProcess = spawn('rshell', ["-f ./commands.txt"], {
        stdio: 'inherit',
        shell: true
    })
    rshellProcess.on("error", () => console.log("rshell process broke"))
    rshellProcess.on("exit", () => {
        fs.rmdirSync("./macs", {recursive: true})
        fs.unlinkSync("./commands.txt")
        console.log("rshell process closed")
    })
}

deploy([11,12,13,14,19,20,21,22,23,24])
