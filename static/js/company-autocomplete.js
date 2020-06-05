var names = {}
var searchoption = null;
var doctype = $("#companysearchbox").data('doctype');
//Typing into the input box will generate autosuggestions
$("#companysearchbox").on('input', function(){
  console.log('working');
  autosuggest($(this).val());
 });
//Sends a GET request to grab suggested job titles based through ElasticSearch
function autosuggest(value){
  $.ajax({
        url : "/api/company/company-suggest/", // the endpoint
        type : "POST", // http method
        data : {search: value,},
        // handle a successful response
        success : function(data) {
            console.log(data);
            showSuggestions(data);
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log('error');
        }
    });
 }
//Creates the Suggestion dropdown
 function showSuggestions(data){
  var div = '';
  data.forEach(function(suggestion){
   if(!names[suggestion.name.toLowerCase()]){
    div += ('<li class="text-left"><a class="suggestions" href="'+ suggestion.link + '">' + suggestion.name + '</li>');
   };
  });
  $('.companyautosuggest').html(div);
 }

 //If the user presses enter, create a span element to keep track of
//search titles.
$("#companysearchbox").keydown(function(e){
  if(e.keyCode==13){
   createSpanElement($(this).val());
   e.preventDefault();
   return false;
  }
 })
//Onclick Action for suggestions shown on dropdown
 $('.companyautosuggest').on('click', '.suggestions', function(){
  createSpanElement($(this).text());
 });

 var createSpanElement = function(companyName){
  if (!names[companyName.toLowerCase()] && companyName.trim().length){
   var spanString = ("<span class='selected_company'>" + companyName + "</span>")
   $('.companytosearch').append($(spanString));
   names[companyName.toLowerCase()] = true;
  }
  $("#companyearchbox").val('');
  $('.companyautosuggest').html('');
 }