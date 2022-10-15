
var nameError = document.getElementById('name-error');

function validateName (){
     var name = document.getElementById('firstName').value;
     if (name.length == 0){
         nameError.innerHTML = 'Name is required';
         return false;
     }
     nameError.innerHTML = 'valid';
     return true;
     }
