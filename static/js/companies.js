function previewCompanyProfile(elem) {
    if ($(elem).html().trim() === 'Preview') {
        $('#safetyPolicyModal').modal({backdrop: 'static', keyboard: false});
        $('#safetyPolicyModal').modal('show');
        $('.biz-profile-preview').attr('style', 'display: none;');
        $(elem).html('Exit');
    } else if ($(elem).html().trim() === 'Exit') {
        $('.biz-profile-preview').attr('style', 'display: initial;');
        $(elem).html('Preview');
    }
}

function toggleEditCompany() {
  var formBox = document.getElementById('editCompanyInfoSection');
  var headerSection = document.getElementById("companyInfoSection");
  if (formBox.style.display === "none") {
    formBox.setAttribute("style", "display: block !important");
    headerSection.setAttribute("style", "display: none !important");
  } else {
    formBox.setAttribute("style", "display: none !important");
    headerSection.setAttribute("style", "display: block !important");
  }
}

function updateCompanyInfo(data) {
   $('#companyName').html(data.name);
   $('#companyTagline').html(data.tagline);
   $('#companyAddress1').html(data.address1);
   $('#companyAddress2').html(data.address2);
   $('#companyAddress3').html(data.city + " ," + data.state + " " + data.zip_code);
   $('#companyBio').html(data.bio);
   $('#companyMap iframe').attr('src', data.gmaps_url);
   $('#companyPhone').attr('href', "tel:" + data.phone_pretty);
   $('#companyPhone').html(data.phone_pretty);
   $('#companyWebsite').attr('href', data.website);
   $('#companyWebsite').html(data.website_pretty);
}

function toggleNewJob() {
  var formBox = document.getElementById('newJob');
  var headerSection = document.getElementById("jobPostings");
  if (formBox.style.display === "none") {
    formBox.setAttribute("style", "display: block !important");
    headerSection.setAttribute("style", "display: none !important");
  } else {
    formBox.setAttribute("style", "display: none !important");
    headerSection.setAttribute("style", "display: block !important");
  }
}

function verifyExperience(experienceID, experienceContainer, companyID) {
    console.log("connection request form is working!") // sanity check
    $.ajax({
        url : "/dashboard/verify-experience/" + companyID + "/", // the endpoint
        type : "POST", // http method
        data : { experienceID : experienceID }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            experienceContainer.setAttribute("style", "display: none !important");
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};

function follow(elem, companyId) {
    if ($("#followText").html().trim() === 'Follow') {
        $("#followText").html('Unfollow');
    } else if ($("#followText").html().trim() === 'Unfollow') {
        $("#followText").html('Follow');
    }
    $.ajax({
        url : "/api/companies/follow/" + companyId + "/", // the endpoint
        type : "PUT", // http method
        data: companyId,
        // handle a successful response
        success : function(data) {
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        },
        cache: false,
        contentType: false,
        processData: false
    });
};

function claimCompanyOwner(btn, bizId) {
    $.ajax({
        url : "/dashboard/claim-company/" + bizId + "/", // the endpoint
        type : "POST", // http method
        data : { bizId : bizId },

        // handle a successful response
        success : function(json) {
            $(btn).hide();
            console.log(json);
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};