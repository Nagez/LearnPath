
(function () {
        //prevent loading page in other pages (excluding '/')
    if (window.location.pathname != '/') {
        document.body.onload = null;
        }
  'use strict'

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  var forms = document.querySelectorAll('.form-validation')

  // Loop over them and prevent submission
  Array.prototype.slice.call(forms)
    .forEach(function (form) {
      form.addEventListener('submit', function (event) {//for each one of the forms found add an EventListener
        if (!validateFname() || !validateLname() || !validateClass() || !validateID()) { //if the form is not valid
          event.preventDefault()//prevent the default event to be taken (prevent submission of the form)
          event.stopPropagation()//prevents further propagation(bubbling up) of the current event (will not go to next event)
        }

      }, false)
    })
})() //Immediately Invoked Function Expressions (function() {})();



//fade alerts
    window.setTimeout(function() {
    $(".alert").fadeTo(500, 0)
}, 7000);


//validation for first name
function validateFname(){
     var fname = document.getElementById('firstName')
     var fnameError = document.getElementById('fname-error')
     //if fname is not null
     if(fname!=null)
    {
        fname=fname.value
         if (!fname.match(/^([A-Za-z]+)$/))
         {
           fnameError.innerHTML = 'invalid first name'
           return false
         }
         fnameError.innerHTML = '<i class="fa-solid fa-circle-check"></i>'
         return true
    }
    else//fname is null
    {
       return true
    }
}


//validation for last name
function validateLname(){
    var lname = document.getElementById('lastName')
    var lnameError = document.getElementById('lname-error');
    //if lname is not null
    if(lname!=null)
    {
        lname=lname.value
        if (!lname.match(/^([A-Za-z]+)$/))
        {
            lnameError.innerHTML = 'invalid last name'
            return false
        }
         lnameError.innerHTML = '<i class="fa-solid fa-circle-check"></i>'
         return true
    }
    else //lname is null
    {
        return true
    }

}


//validation for class name
function validateClass(){
    var cname = document.getElementById("class")
    var cnameError = document.getElementById('cname-error');
    //if class is not null
    if(cname!=null)
    {
        cname=cname.value
        if(!cname.match(/^([A-Za-z]+)$/)&&!cname.match(/[a-zA-Z]+ [a-zA-Z]+$/)) //if class is not valid
        {
            cnameError.innerHTML = 'invalid class name'
            return false
        }
        cnameError.innerHTML = '<i class="fa-solid fa-circle-check"></i>'
        return true
    }
    else //class is null
    {
        return true
    }
}

//validation for id
function validateID(){
    var id = document.getElementById("ID")
    var idError = document.getElementById('id-error');
    //if id is not null
    if(id!=null)
    {
        id=id.value
        if(!id.match(/(^[1-9]+)([0-9]*)/)) //if class is not valid
        {
            idError.innerHTML = 'invalid ID'
            return false
        }
        idError.innerHTML = '<i class="fa-solid fa-circle-check"></i>'
        return true
    }
    else //id is null
    {
        return true
    }
}