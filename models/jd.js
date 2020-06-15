const mongoose = require("mongoose");

var jdSchema = new mongoose.Schema({
    title: String,
    description: String
});

module.exports=mongoose.model("Jd",jdSchema);