//document.getElementById("submit").disabled = true;
// var nameError = document.getElementById('name-error');

(function () {
  'use strict'

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  var forms = document.querySelectorAll('.needs-validation')

  // Loop over them and prevent submission
  Array.prototype.slice.call(forms)
    .forEach(function (form) {
      form.addEventListener('submit', function (event) {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }
        form.classList.add('was-validated')
      }, false)
    })

})()

//prevent loading page in other pages (excluding '/')
if (window.location.pathname != '/') {
  document.body.onload = null;
}

//fade alerts
    window.setTimeout(function() {
    $(".alert").fadeTo(500, 0)
}, 4000);

// function validateName (){
//      var name = document.getElementById('firstName').value
//      if (name.length == 0){
//          nameError.innerHTML = 'Name is required'
//          return false
//      }
//      nameError.innerHTML = 'valid'
//      return true
//      }

// //form
// var firstName=document.getElementById("firstName")
// var lastName=document.getElementById("lastName")
// var Area=document.getElementById("Area")
// var Gender=document.getElementById("Gender")
// var Psychometric=document.getElementById("Psychometric-output")
// var Bagrut=document.getElementById("Bagrut-output")
//
//
//
// function printVal(){
//     //form submit .value
//     var firstName_Text=firstName.value
//     var lastName_Text=lastName.value
//     var Area_Text=Area.options[Area.selectedIndex].text
//     var Gender_Text=Area.options[Area.selectedIndex].text
//     var Psychometric_val=Psychometric.value
//     var Bagrut_val=Bagrut.value
//
// }