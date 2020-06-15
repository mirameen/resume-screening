const express    = require("express");
const app        = express();
const port       = 3000;
const path           = require("path");
const crypto         = require("crypto");
const bodyParser = require("body-parser");
const mongoose   = require("mongoose");
const multer         = require("multer");
const GridFsStorage  = require("multer-gridfs-storage");
const Grid           = require("gridfs-stream");
const Jd         = require("./models/jd");
const Cv         = require("./models/cv");

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
            res.render("jd/show",{currJd:foundJd});
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
      console.log(file);
        const readstream = gfs.createReadStream(file.filename);
        readstream.pipe(res);
    });
});

app.listen(port,function(){
    console.log("App has started........");
});