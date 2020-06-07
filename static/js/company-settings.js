function submitCompanySettingPageForm(formObj, formId, clearForm) {
    var formData = new FormData(formObj);
    var url = $(formObj).attr("action");
    $.ajax({
        url: url,
        type: 'POST',
        data: formData,
        success: function (data) {
            $(".form-success-container").empty();
            setTimeout(function(){
              $(formId + " .form-success-container").append('<p class="font-pink font-title mb-3 ml-2"><b>Changes Saved</b></p>');
                if (clearForm === true) {
                    formObj.trigger('reset')
                }
            }, 300);
        },
        error : function(data, textStatus, xhr) {
            for (var name in data['responseJSON']) {
                var $input = $(formId + " #id_" + name);
                $input.before("<div class='alert alert-block alert-danger'><small>" + data['responseJSON'][name][0] + "</small></div>");
            }
        },
        cache: false,
        contentType: false,
        processData: false
    });
};

function removeCompanyAdminSetting(companyId, userId) {
    var url = '/api/company/remove-admin/' + companyId + '/' + userId + '/';
    $.ajax({
        url: url,
        type: 'GET',
        success: function (data) {
            $('#adminRow' + userId).remove();
        },
        cache: false,
        contentType: false,
        processData: false
    });
};