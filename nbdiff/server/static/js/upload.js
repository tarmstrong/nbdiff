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
            baseFile = $id("baseFile"),
            baseFileDrag = $id("baseFileDrag"),
            baseJSON = $id("baseJSON"),
            remoteFile = $id("remoteFile"),
            remoteFileDrag = $id("remoteFileDrag"),
            remoteJSON = $id("remoteJSON"),
            beforeFile = $id("beforeFile"),
            beforeFileDrag = $id("beforeFileDrag"),
            beforeJSON = $id("beforeJSON"),
            afterFile = $id("afterFile"),
            afterFileDrag = $id("afterFileDrag"),
            afterJSON = $id("afterJSON"),
            mergeSubmitBtn = $id("submitBtn"),
            mergeErrorDiv = $id("mergeErrorMsg"),
            diffSubmitBtn = $id("submitBtn3"),
            diffErrorDiv = $id("diffErrorMsg");
        
        //make a dictionary for to reference dom variables.
        dict = {
          "local" : [localFile, localFileDrag, localJSON],
          "base" : [baseFile, baseFileDrag, baseJSON],
          "remote" : [remoteFile, remoteFileDrag, remoteJSON],
          "before" : [beforeFile, beforeFileDrag, beforeJSON],
          "after" : [afterFile, afterFileDrag, afterJSON]
        };

        // file select listeners
        localFile.addEventListener("change", FileSelectHandler, false);
        baseFile.addEventListener("change", FileSelectHandler, false);
        remoteFile.addEventListener("change", FileSelectHandler, false);
        beforeFile.addEventListener("change", FileSelectHandler, false);
        afterFile.addEventListener("change", FileSelectHandler, false);

        // is XHR2 available
        var xhr = new XMLHttpRequest();
        if (xhr.upload) {
            // file drag and drop listeners.
            setupDragDropListener(localFileDrag);
            setupDragDropListener(baseFileDrag);
            setupDragDropListener(remoteFileDrag);
            setupDragDropListener(beforeFileDrag);
            setupDragDropListener(afterFileDrag);
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
        
        // get target details
        var targetID = e.target.id;
        var targetType;
        if(targetID.indexOf("local") != -1){
          targetType="local";
        } else if (targetID.indexOf("base") != -1){
          targetType="base";
        } else if (targetID.indexOf("remote") != -1){
          targetType="remote"; 
        } else if (targetID.indexOf("before") != -1){
          targetType="before"; 
        } else if (targetID.indexOf("after") != -1){
          targetType="after"; 
        }
        
        if(files.length > 1){
            //uploads more than one file per side.
            if(targetType == "base" || targetType == "local" || targetType == "remote"){
                displayError(0, mergeErrorDiv, mergeSubmitBtn);
            } else {
                displayError(0, diffErrorDiv, diffSubmitBtn);
            }
        } else if(files[0].name.substring(files[0].name.indexOf(".")) != ".ipynb"){
            //invalid file type upload.
            if(targetType == "base" || targetType == "local" || targetType == "remote"){
                displayError(1, mergeErrorDiv, mergeSubmitBtn);
            } else {
                displayError(1, diffErrorDiv, diffSubmitBtn);
            }
        } else {  
            //valid file specified
            
            //set file input
            dict[targetType][0].files = files;
            displayFileDetails(files[0], dict[targetType][1]); 
            
            //read file and put JSON content into hidden input
            handleFileRead(files[0], dict[targetType][2]);
            
            if(targetType == "base" || targetType == "local" || targetType == "remote"){
                mergeErrorDiv.style.display = "none";
            } else {
                diffErrorDiv.style.display = "none";
            }
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
            if(localJSON.value.length != 0 && remoteJSON.value.length != 0 && baseJSON.value.length != 0){
                mergeSubmitBtn.className = "enableBtn";
            }
            if(beforeJSON.value.length != 0 && afterJSON.value.length != 0){
                diffSubmitBtn.className = "enableBtn";
            }
        });
        reader.readAsText(file);
    }
    
    //display error message to user. 
    function displayError(type, errorDiv, submitButton){
        if(type == 0){
            if(errorDiv.id.indexOf("merge") != -1){
                errorDiv.innerHTML = " <p> Multiple files uploaded are not acceptable. <br/> Please select only one local, one base, and one remote file. </p>";
            } else {
                errorDiv.innerHTML = " <p> Multiple files uploaded are not acceptable. <br/> Please select only one previous, and one afterwards versions of a file. </p>";
            }
        } else if (type == 1){
            errorDiv.innerHTML = " <p> Only valid .ipynb files are acceptable. </p>";
        } else if (type == 2){
            if(errorDiv.id.indexOf("merge") != -1){
                errorDiv.innerHTML = " <p> You must specify: <br/> "+
                                 (localJSON.value.length == 0 ? "- one local iPython notebook <br/>" : "") +
                                 (baseJSON.value.length == 0 ? "- one local iPython notebook <br/>" : "") +
                                 (remoteJSON.value.length == 0 ? "- one remote iPython notebook." : "") + "</p>";
            } else {
                errorDiv.innerHTML = " <p> You must specify: <br/> "+
                                 (beforeJSON.value.length == 0 ? "- one previous version of the iPython notebook <br/>" : "") +
                                 (afterJSON.value.length == 0 ? "- one afterwards version of the iPython notebook <br/>" : "") + "</p>";
            }
        } 
        errorDiv.style.display = "block";
        submitButton.className = "disableBtn";
    }
    
    //validate form that three files are specified. 
    function validateMergeForm(){
        if(localJSON.value.length == 0 || remoteJSON.value.length == 0 || baseJSON.value.length == 0){
            displayError(2, mergeErrorBtn, mergeSubmitBtn); 
            return false;
        } else {
            return true;
        }
    }
     //validate form that two files are specified. 
    function validateDiffForm(){
        if(beforeJSON.value.length == 0 || afterJSON.value.length == 0 ){
            displayError(2, diffErrorBtn, diffSubmitBtn);  
            return false;
        } else {
            return true;
        }
    }
});