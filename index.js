const express = require('express')
const path = require('path')
const fs = require("fs")
const http = require('http')
const app = express()
const multer = require('multer')
const upload = multer({ dest: 'temp/' })
// const { spawn } = require('child_process');
const { exec, spawn } = require('child_process');

app.set('json spaces', 2)
app.use(express.json())
app.use(express.static("public"))
app.use(express.json({ limit: '100mb', extended: true, parameterLimit: 5000000 }))
app.use(express.urlencoded({ limit: '100mb', extended: true, parameterLimit: 5000000 }))

app.post('/test', upload.any(), function (req, res, next) {

    console.log(req.files)
    jsonfile = req.files[0].filename

    upload(req, res, function (err) {
        if (err instanceof multer.MulterError) {
            console.log("Случилась ошибка Multer при загрузке.")
        } else {
            console.log("При загрузке произошла неизвестная ошибка.")
        }

        const command = `python3 "main_script.py" "templates/template.docx" ${jsonfile} "temp/result.docx"`
        console.log(command)
        exec(command, (err, stdout, stderr) => {
            if (err) {
                console.error(err);
                console.error(stderr);
                return;
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
