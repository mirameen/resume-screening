const express        = require("express");
const app            = express();
const {spawn}        = require("child_process");
const http           = require("http");
const port           = 3000;
const path           = require("path");
const crypto         = require("crypto");
const bodyParser     = require("body-parser");
const mongoose       = require("mongoose");
const multer         = require("multer");
const GridFsStorage  = require("multer-gridfs-storage");
const Grid           = require("gridfs-stream");
const Jd             = require("./models/jd");
const CvContent      = require("./models/cvContent")
const pdfreader      = require("pdfreader");
const Cv             = require("./models/cv");
const crawler        = require('crawler-request');
const methodOverride = require('method-override');
 

mongoose.set('useNewUrlParser',true);
mongoose.set('useFindAndModify', false);
mongoose.set('useCreateIndex', true);
mongoose.set('useUnifiedTopology', true);



const uri="mongodb://localhost/resume_screening";
mongoose.connect(uri);
const conn=mongoose.connection;
var gfs;


conn.once('open', function () {
    //Init stream
	gfs = Grid(conn.db, mongoose.mongo);
    gfs.collection("uploads");
});

var storage = new GridFsStorage({
    url: uri,
    file: (req, file) => {
        return new Promise((resolve, reject) => {
            crypto.randomBytes(16, (err, buf) => {
                if (err) {
                    return reject(err);
                }
                const filename = buf.toString('hex') + path.extname(file.originalname);
                const fileInfo = {
                    filename: filename,
                    bucketName: 'uploads'
                };
                resolve(fileInfo);
            });
        });
    }
  });
  const upload = multer({ storage });


app.use(bodyParser.urlencoded({extended: true}));
app.use(methodOverride('_method'));
app.set("view engine", "ejs");

app.get("/",function(req,res){
    res.render("landing");
});

app.get("/jd",function(req,res){
    Jd.find({}, function(err,allJds){
        if(err) console.log(err);
        else{
            res.render("jd/index",{jds:allJds});
        }
    });
});

app.get("/jd/new",function(req,res){
    res.render("jd/new");
});

app.post("/jd",function(req,res){
    var title=req.body.title;
    var desc=req.body.jobdesc;
    var newJD={title:title, description:desc};
    Jd.create(newJD, function(err,newlyCreated){
        if(err) console.log(err);
        else{
            res.redirect("/jd");
        }
    });
});

app.get("/jd/:id",function(req,res){
    Jd.findById(req.params.id,function(err,foundJd){
        if(err) console.log(err);
        else{
            var screenedCv = [],processed=0,kl=3;
            var skills = foundJd.description.split(" ");
            console.log(skills);
            gfs.files.find().toArray((err, files) => {
                // Check if files
                if (!files || files.length === 0) {
                    res.render('cv/index', { files: false });
                } else {
                    if(files)
                    {
                        console.log(files.length);
                        kl=files.length;
                        files.forEach(function(file){
                            crawler("http://localhost:3000/cv/show/"+file.filename).then(function(response){
                                // handle response
                                var data = response.text;
                                var largeDataSet = [];
                                const python = spawn('python', ['spacymodel.py', data, JSON.stringify(skills)]);

                                python.stdout.on('data', function (data) {
                                    console.log('Pipe data from python script ...');
                                    largeDataSet.push(data);
                                    console.log("hehe");
                                });
                                
                                python.on('close', (code) => {
                                    console.log(`child process close all stdio with code ${code}`);
                                    var result = largeDataSet.join("").replace(/\s/g, ''); 
                                    var check = "True"; 
                                    console.log(result===check);
                                    if(result===check){
                                        screenedCv.push(file.filename);
                                    }
                                    ++processed;
                                    console.log(processed);
                                    if(processed===kl) res.render("jd/show",{currJd:foundJd,dispCv:screenedCv});
                                });
                            });
                        });
                    }
                }
            });
        }
    });
});

app.delete("/jd/:id",function(req,res){
  Jd.findByIdAndRemove(req.params.id,function(err,jd){
		if(err) console.log(err);
		else{
			res.redirect("/jd");
		}
	});
});

app.get("/cv",function(req,res){
    gfs.files.find().toArray((err, files) => {
        // Check if files
        if (!files || files.length === 0) {
            res.render('cv/index', { files: false });
        } else {
          files.map(file => {
            if (
                file.contentType === 'image/jpeg' ||
                file.contentType === 'image/png'
            ) {
                file.isImage = true;
            } else {
                file.isImage = false;
            }
            });
            res.render('cv/index', { files: files });
        }
    });
});

app.get("/cv/new",function(req,res){
    res.render("cv/new");
});

app.post("/cv",upload.single("file"),function(req,res){
    res.redirect("/cv");
});

app.get("/cv/download/:filename",function(req,res){
    gfs.files.findOne({ filename: req.params.filename }, (err, file) => {
        // Check if file
        if (!file || file.length === 0) {
          return res.status(404).json({
            err: 'No file exists'
          });
        }
        // File exists
        res.set('Content-Type', file.contentType);
        res.set('Content-Disposition', 'attachment; filename="' + file.filename + '"');
        // streaming from gridfs
        var readstream = gfs.createReadStream({
          filename: req.params.filename
        });
        console.log(res);
        //error handling, e.g. file does not exist
        readstream.on('error', function (err) {
          console.log('An error occurred!', err);
          throw err;
        });
        readstream.pipe(res);
      });
})

app.get("/cv/show/:filename",(req,res)=>{
    gfs.files.findOne({ filename: req.params.filename }, (err, file) => {
      // Check if file
      if (!file || file.length === 0) {
        return res.status(404).json({
          err: 'No file exists'
        });
    }
    const readstream = gfs.createReadStream(file.filename);
    readstream.pipe(res);
    });
});

app.delete('/cv/:id', (req, res) => {
  gfs.remove({ _id: req.params.id, root: 'uploads' }, (err, gridStore) => {
    if (err) {
      return res.status(404).json({ err: err });
    }

    res.redirect('/');
  });
});


app.listen(port,function(){
    console.log("App has started........");
});