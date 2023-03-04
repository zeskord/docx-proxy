const express = require('express')
const path = require('path')
const fs = require("fs")
const http = require('http')
const app = express()
const multer = require('multer')
const upload = multer({ dest: 'temp/' }).any()
// const { spawn } = require('child_process');
const { exec, spawn } = require('child_process');

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
        jsonfile = req.files[0].filename

        const command = `python3 "main_script.py" "templates/template.docx" "temp/${jsonfile}" "temp/${jsonfile}.docx"`
        console.log(command)
        exec(command, (err, stdout, stderr) => {
            if (err) {
                console.error(err)
                console.error(stderr)
                return
            }
            console.log(stdout)
        })

    })


    // ans = { status: "OK" }
    // res.json(ans)
})

app.post('/main', (req, res) => {
    data = {
        params: req.body.params,
        taskId: req.body.taskId
    }
    // const buff = Buffer.from(base64, 'base64');
    jsonFilePath = path.join('./temp/', `${taskId}.json`)
    fs.writeFileSync(jsonFilePath, params)
    ans = { status: "OK" }
    res.json(ans)
})



const noSslServer = http.createServer(app)
noSslServer.listen(8080)
