const express = require('express')
const path = require('path')
const fs = require("fs")
const http = require('http')
const app = express()
const multer = require('multer')
const upload = multer({ dest: 'temp/' }).any()
const { exec, spawn } = require('child_process')

app.set('json spaces', 2)
app.use(express.json())
app.use(express.static("public"))
app.use(express.json({ limit: '100mb', extended: true, parameterLimit: 5000000 }))
app.use(express.urlencoded({ limit: '100mb', extended: true, parameterLimit: 5000000 }))

app.post('/create_task', function (req, res, next) {

    upload(req, res, function (err) {
        if (err instanceof multer.MulterError) {
            console.log("Случилась ошибка Multer при загрузке.")
            console.error(err)
            return
        } else {
            console.log("При загрузке произошла неизвестная ошибка.")
            console.error(err)
        }

        // Если мы здесь без ошибок, то файл загружен.
        console.log(req.files)
        var temlateFileItem
        var dataFileItem
        for (let i=0; i<req.files.length; i++) {
            if (req.files[i].fieldname === "template") {
                temlateFileItem = req.files[i]
            } else if (req.files[i].fieldname === "data") {
                dataFileItem = req.files[i]
            }
        }
        jsonFile = dataFileItem.filename
        templateFile = temlateFileItem.filename
        resultFile = `${jsonFile}.docx`

        template = req.body.template // Имя шаблона docx

        const command = `python3 "main_script.py" "temp/${templateFile}" "temp/${jsonFile}" "temp/${resultFile}"`
        console.log(command)
        exec(command, (err, stdout, stderr) => {
            if (err) {
                console.error(err)
                console.error(stderr)
                res.send(
                    {
                        stdout: stdout,
                        stderr: stderr
                    }
                )
                return
            }
            console.log(stdout)
            const file_buffer = fs.readFileSync(`temp/${resultFile}`)
            const contents_in_base64 = file_buffer.toString('base64')
            res.json(
                {
                    status: "OK",
                    filedata: contents_in_base64
                }
            )
        })
    })
})

app.post('/main', (req, res) => {
    data = {
        params: req.body.params,
        taskId: req.body.taskId
    }
    jsonFilePath = path.join('./temp/', `${taskId}.json`)
    fs.writeFileSync(jsonFilePath, params)
    ans = { status: "OK" }
    res.json(ans)
})


function deleteOldFiles() {
    fs.readdir("temp", (err, files) => {
        files.forEach(file => {
            filepath = path.join('./temp/', `${file}`)
            filestat = fs.statSync(filepath);
            timelong = new Date() - filestat.birthtime
            if (timelong > 3600000) {
                fs.unlink(filepath, (err) => {
                    if (err) throw err;
                    console.log(`${filepath} was deleted`)
                })
            }
        })
    })
}


const noSslServer = http.createServer(app)
noSslServer.listen(8080)

setInterval(deleteOldFiles, 60000)
