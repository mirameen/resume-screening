const mongoose = require("mongoose");

var cvContentSchema = new mongoose.Schema({
    filename: String,
    content: String
});

module.exports=mongoose.model("CvContent",cvContentSchema)