
$('#imgUpload').on('change', function(file){
	var dataURL;
	var blob = "";
    var input = file.target;
    var reader = new FileReader();
    reader.onload = function(){
    	if(file.target.files[0].type == "image/jpeg") {
    		$("#divImage").show();
	      	dataURL = reader.result;
	      	//Display Image
	      	$('#divImage').attr('src',dataURL);
		    
		    // Split the base64 string in data and contentType
			block = dataURL.split(";");
			// Get the content type of the image
			contentType = block[0].split(":")[1];// In this case "image/gif"
			// get the real base64 content of the file
			realData = block[1].split(",")[1];// In this case "R0lGODlhPQBEAPeoAJosM...."
			// Convert it to a blob to upload
			blob = b64toBlob(realData, contentType);

    	}
    	else if(file.target.files[0].type == "application/pdf"){
    		showPDF(URL.createObjectURL($("#imgUpload").get(0).files[0]));
    		// Split the base64 string in data and contentType
			block = __CANVAS.toDataURL().split(";");
			// Get the content type of the image
			contentType = block[0].split(":")[1];// In this case "image/gif"
			// get the real base64 content of the file
			realData = block[1].split(",")[1];// In this case "R0lGODlhPQBEAPeoAJosM...."
			// Convert it to a blob to upload
			blob = b64toBlob(realData, contentType);
    	}
    	else {
    		$('#divImage').hide();
    		$('#pdf-canvas').hide();
    		alert("please upload image or pdf formats only");
    	}
    	var blobData = new FormData();
      	blobData.append('file', blob);
    	//send blob to Server.
    	// $.ajax({
    	// 	type: "POST",
    	// 	url: "http://192.168.0.67:8080/extractor/upload_file2/",
    	// 	data: blobData,
    	// 	processData: false
    	// }).done(function (response) {
    	// 	console.log(response);
    	// })
    };
    reader.readAsDataURL(input.files[0]);
});
var __PDF_DOC,
	__CURRENT_PAGE,
	__TOTAL_PAGES,
	__PAGE_RENDERING_IN_PROGRESS = 0,
	__CANVAS = $('#pdf-canvas').get(0),
	__CANVAS_CTX = __CANVAS.getContext('2d');

function showPDF(pdf_url) {
	//$("#pdf-loader").show();

	PDFJS.getDocument({ url: pdf_url }).then(function(pdf_doc) {
		__PDF_DOC = pdf_doc;
		__TOTAL_PAGES = __PDF_DOC.numPages;
		
		// Hide the pdf loader and show pdf container in HTML
		//$("#pdf-loader").hide();
		//$("#pdf-contents").show();
		//$("#pdf-total-pages").text(__TOTAL_PAGES);

		// Show the first page
		showPage(1);
	}).catch(function(error) {
		// If error re-show the upload button
		//$("#pdf-loader").hide();
		//$("#upload-button").show();
		
		console.log(error.message);
	});;
}

function showPage(page_no) {
	__PAGE_RENDERING_IN_PROGRESS = 1;
	__CURRENT_PAGE = page_no;

	// Disable Prev & Next buttons while page is being loaded
	//$("#pdf-next, #pdf-prev").attr('disabled', 'disabled');

	// While page is being rendered hide the canvas and show a loading message
	$("#pdf-canvas").hide();
	//$("#page-loader").show();
	//$("#download-image").hide();

	// Update current page in HTML
	//$("#pdf-current-page").text(page_no);
	
	// Fetch the page
	__PDF_DOC.getPage(page_no).then(function(page) {
		// As the canvas is of a fixed width we need to set the scale of the viewport accordingly
		var scale_required = __CANVAS.width / page.getViewport(1).width;

		// Get viewport of the page at required scale
		var viewport = page.getViewport(scale_required);

		// Set canvas height
		__CANVAS.height = viewport.height;

		var renderContext = {
			canvasContext: __CANVAS_CTX,
			viewport: viewport
		};
		
		// Render the page contents in the canvas
		page.render(renderContext).then(function() {
			__PAGE_RENDERING_IN_PROGRESS = 0;

			// Re-enable Prev & Next buttons
			//$("#pdf-next, #pdf-prev").removeAttr('disabled');

			// Show the canvas and hide the page loader
			$("#pdf-canvas").show();
			//$("#page-loader").hide();
			//$("#download-image").show();
		});
	});
}

function b64toBlob(b64Data, contentType, sliceSize) {
    contentType = contentType || '';
    if(contentType == "application/pdf" || contentType == "image/jpeg"){
    	contentType = "image/jpeg";
    }
    else  {
    	contentType = "";
    }
    sliceSize = sliceSize || 512;

    var byteCharacters = atob(b64Data);
    var byteArrays = [];

    for (var offset = 0; offset < byteCharacters.length; offset += sliceSize) {
        var slice = byteCharacters.slice(offset, offset + sliceSize);

        var byteNumbers = new Array(slice.length);
        for (var i = 0; i < slice.length; i++) {
            byteNumbers[i] = slice.charCodeAt(i);
        }

        var byteArray = new Uint8Array(byteNumbers);

        byteArrays.push(byteArray);
    }

  	var blob = new Blob(byteArrays, {type: contentType});
  	return blob;
}