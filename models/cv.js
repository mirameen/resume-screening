const mongoose = require("mongoose");

var cvSchema = new mongoose.Schema({
    position: String,
    content: String
});

module.exports=mongoose.model("Cv",cvSchema);