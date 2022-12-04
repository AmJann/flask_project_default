const openBtn = document.getElementById("openModal");
const modal = document.getElementById("modal");
const close = document.getElementById("close");

const openModal = () => {
  modal.style.display = "block";
};
openBtn.addEventListener("click", openModal);

const closeModal = () => {
  modal.style.display = "none";
};

close.addEventListener("click", closeModal);


const modal2 = document.getElementById("modal2");
const close2 = document.getElementById("close2");

const openModal2 = () => {
  modal2.style.display = "block";
};
openBtn.addEventListener("click", openModal2);

const closeModal2 = () => {
  modal2.style.display = "none";
};

close2.addEventListener("click", closeModal2);

$(document).ready(function(e){
  var clicked;
  e.preventDefault()
  $(".complete").click(function(){
  clicked = $(this).attr("#complete");
  $.ajax({
    type : 'GET',
    url : "{{url_for('complete')}}",
    contentType: 'application/json;charset=UTF-8',
    data : {'data':clicked}
  });
   });

  });

   



