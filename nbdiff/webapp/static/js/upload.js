$(document).ready(function(){
   // getElementById
    function $id(id) {
        return document.getElementById(id);
    }
    
    Init();

    // initialize
    function Init() {

        //define dom variables
        var localFile = $id("localFile"),
            localFileDrag = $id("localFileDrag"),
            localJSON = $id("localJSON"),
            remoteFile = $id("remoteFile"),
            remoteFileDrag = $id("remoteFileDrag"),
            remoteJSON = $id("remoteJSON"),
            submitBtn = $id("submitBtn"),
            errorMsg = $id("errorMsg");

        // file select listeners
        localFile.addEventListener("change", FileSelectHandler, false);
        remoteFile.addEventListener("change", FileSelectHandler, false);

        // is XHR2 available
        var xhr = new XMLHttpRequest();
        if (xhr.upload) {
            // file drag and drop listeners.
            setupDragDropListener(localFileDrag);
            setupDragDropListener(remoteFileDrag);
        }
    }
    // file drag hover
    function FileDragHover(e) {
        e.stopPropagation();
        e.preventDefault();
        e.target.className = (e.type == "dragover" ? "hover" : "");
    }
    // file selection
    function FileSelectHandler(e) {
        // cancel event and hover styling
        FileDragHover(e);

        // fetch FileList object
        var files = e.target.files || e.dataTransfer.files;
        if(files.length > 1){
            //uploads more than one file per side.
            displayError(0);
        } else if(files[0].name.substring(files[0].name.indexOf(".")) != ".ipynb"){
            //invalid file type upload.
            displayError(1);
        } else {
            var targetID = e.target.id;
            if(targetID.indexOf("local") != -1){
                //set file input
                localFile.files = files;
                displayFileDetails(files[0], localFileDrag); 
                
                //read file and put JSON content into hidden input
                handleFileRead(files[0], localJSON);
            } 
            else if (targetID.indexOf("remote") != -1){
                //set file input
                remoteFile.files = files;
                displayFileDetails(files[0], remoteFileDrag);

                //read file and put JSON content into hidden input
                handleFileRead(files[0], remoteJSON);
            }
            errorMsg.style.display = "none";
        }
    }
    
    //adds listeners for drag and drop feature to a object.
    function setupDragDropListener(obj){
        obj.addEventListener("dragover", FileDragHover, false);
        obj.addEventListener("dragleave", FileDragHover, false);
        obj.addEventListener("drop", FileSelectHandler, false);
        obj.style.display = "block";
    }
    
    //add inner html about the file uploaded in a specified format.
    function displayFileDetails(file, side){
        side.innerHTML = file.name + " ("+ file.size + " bytes) has been selected. <br/> Last Modified: " +
                        (file.lastModifiedDate ? file.lastModifiedDate.toLocaleDateString() : 'n/a') + ". <br/><br/> To change files drop another file.";
    }
    
    //reads .ipynb files and places the content into the appropriate input field.
    function handleFileRead(file, side){
        var reader = new FileReader();
        reader.onload = (function(file) {
            side.value = reader.result;
            if(localJSON.value.length != 0 && remoteJSON.value.length != 0){
                submitBtn.className = "enableBtn";
            }
        });
        reader.readAsText(file);
    }
    
    //display error message to user. 
    function displayError(type){
        if(type == 0){
            errorMsg.innerHTML = " <p> Multiple files uploaded are not acceptable. <br/> Please select only one local and one remote file. </p>";
        } else if (type == 1){
            errorMsg.innerHTML = " <p> Only valid .ipynb files are acceptable. </p>";
        } else if (type == 2){
            errorMsg.innerHTML = " <p> You must specify: <br/> "+
                                 (localJSON.value.length == 0 ? "- one local iPython notebook <br/>" : "") +
                                 (remoteJSON.value.length == 0 ? "- one remote iPython notebook." : "") + "</p>";
        } 
        errorMsg.style.display = "block";
        submitBtn.className = "disableBtn";
    }
    
    //validate form that two files are specified. 
    function validateForm(){
        if(localJSON.value.length == 0 || remoteJSON.value.length == 0){
            displayError(2);
            return false;
        } else {
            return true;
        }
    }
});