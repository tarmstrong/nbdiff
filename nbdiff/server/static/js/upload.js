$(document).ready(function(){
   // getElementById
    function $id(id) {
        return document.getElementById(id);
    }
    
    init();

    // initialize
    function init() {

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
            afterJSON = $id("afterJSON");
        
        //make a dictionary for to reference dom variables.
        dict = {
          "local" : [localFile, localFileDrag, localJSON],
          "base" : [baseFile, baseFileDrag, baseJSON],
          "remote" : [remoteFile, remoteFileDrag, remoteJSON],
          "before" : [beforeFile, beforeFileDrag, beforeJSON],
          "after" : [afterFile, afterFileDrag, afterJSON]
        };

        // file select listeners
        localFile.addEventListener("change", fileSelectHandler, false);
        baseFile.addEventListener("change", fileSelectHandler, false);
        remoteFile.addEventListener("change", fileSelectHandler, false);
        beforeFile.addEventListener("change", fileSelectHandler, false);
        afterFile.addEventListener("change", fileSelectHandler, false);

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
    function fileDragHover(e) {
        e.stopPropagation();
        e.preventDefault();
        e.target.className = (e.type === "dragover" ? "hover" : "");
    }
    // file selection
    function fileSelectHandler(e) {
        // cancel event and hover styling
        fileDragHover(e);

        // fetch FileList object
        var files = e.target.files || e.dataTransfer.files;
        
        // get target details
        var targetID = e.target.id;
        var targetType;
        if(targetID.indexOf("local") !== -1){
          targetType="local";
        } else if (targetID.indexOf("base") !== -1){
          targetType="base";
        } else if (targetID.indexOf("remote") !== -1){
          targetType="remote"; 
        } else if (targetID.indexOf("before") !== -1){
          targetType="before"; 
        } else if (targetID.indexOf("after") !== -1){
          targetType="after"; 
        }
        
        if(files.length > 1){
            //uploads more than one file per side.
            if(targetType === "base" || targetType === "local" || targetType === "remote"){
                displayError(0, $id("mergeErrorMsg"), $id("submitBtn"));
            } else {
                displayError(0, $id("diffErrorMsg"), $id("submitBtn3"));
            }
            dict[targetType][1].innerHTML = "Invalid File.";
            dict[targetType][2].value = "";
        } else if(files[0].name.substring(files[0].name.indexOf(".")) !== ".ipynb"){
            //invalid file type upload.
            if(targetType === "base" || targetType === "local" || targetType === "remote"){
                displayError(1, $id("mergeErrorMsg"), $id("submitBtn"));
            } else {
                displayError(1, $id("diffErrorMsg"), $id("submitBtn3"));
            }
            dict[targetType][1].innerHTML = "Invalid File.";
            dict[targetType][2].value = "";
        } else {  
            //valid file specified
            
            //set file input
            dict[targetType][0].files = files;
            displayFileDetails(files[0], dict[targetType][1]); 
            
            //read file and put JSON content into hidden input
            handleFileRead(files[0], dict[targetType][2]);
            
            if(targetType === "base" || targetType === "local" || targetType === "remote"){
                $id("mergeErrorMsg").style.display = "none";
            } else {
                $id("diffErrorMsg").style.display = "none";
            }
        }
    }
    
    //adds listeners for drag and drop feature to a object.
    function setupDragDropListener(obj){
        obj.addEventListener("dragover", fileDragHover, false);
        obj.addEventListener("dragleave", fileDragHover, false);
        obj.addEventListener("drop", fileSelectHandler, false);
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
            if(localJSON.value.length !== 0 && remoteJSON.value.length !== 0 && baseJSON.value.length !== 0){
                $id("submitBtn").className = "enableBtn";
            }
            if(beforeJSON.value.length !== 0 && afterJSON.value.length !== 0){
                $id("submitBtn3").className = "enableBtn";
            }
        });
        reader.readAsText(file);
    }
    
    //display error message to user. 
    function displayError(type, errorDiv, submitButton){
        if(type === 0){
            if(errorDiv.id.indexOf("merge") !== -1){
                errorDiv.innerHTML = " <p> Multiple files uploaded are not acceptable. <br/> Please select only one local, one base, and one remote file. </p>";
            } else {
                errorDiv.innerHTML = " <p> Multiple files uploaded are not acceptable. <br/> Please select only one previous, and one afterwards versions of a file. </p>";
            }
        } else if (type === 1){
            errorDiv.innerHTML = " <p> Only valid .ipynb files are acceptable. </p>";
        } else if (type === 2){
            if(errorDiv.id.indexOf("merge") !== -1){
                errorDiv.innerHTML = " <p> You must specify: <br/> "+
                                 (localJSON.value.length === 0 ? "- one local iPython notebook <br/>" : "") +
                                 (baseJSON.value.length === 0 ? "- one base iPython notebook <br/>" : "") +
                                 (remoteJSON.value.length === 0 ? "- one remote iPython notebook." : "") + "</p>";
            } else {
                errorDiv.innerHTML = " <p> You must specify: <br/> "+
                                 (beforeJSON.value.length === 0 ? "- one previous version of the iPython notebook <br/>" : "") +
                                 (afterJSON.value.length === 0 ? "- one afterwards version of the iPython notebook <br/>" : "") + "</p>";
            }
        } 
        errorDiv.style.display = "block";
        submitButton.className = "disableBtn";
    }
    
    //validate form that three files are specified.
    $("#mergeForm").submit(function( event ) {
      if(localJSON.value.length === 0 || remoteJSON.value.length === 0 || baseJSON.value.length === 0){
          displayError(2, $id("mergeErrorMsg"), $id("submitBtn"));  
          return false;
      } else {
          return true;
      }
    });
   
    //validate form that two files are specified. 
    $("#diffForm").submit(function( event ) {
       if(beforeJSON.value.length === 0 || afterJSON.value.length === 0 ){
            displayError(2, $id("diffErrorMsg"), $id("submitBtn3"));  
            return false;
        } else {
            return true;
        }
    });
});
