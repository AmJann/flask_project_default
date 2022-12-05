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

// const openBtn2 = document.getElementById("openModal");
// const modal2 = document.getElementById("modal2");
// const close2 = document.getElementById("close2");

// const openModal2 = () => {
//   modal2.style.display = "block";
// };
// openBtn2.addEventListener("click", openModal);

// const closeModal2 = () => {
//   modal2.style.display = "none";
// };

// close2.addEventListener("click", closeModal2);

// $(document).ready(function(e){
//   $('.complete').on('click', function(){
//     e.preventDefault()
//     var complete_id = $(this).attr('todo_id');

//     var complete = $('#complete'+complete_id).val();

//     req = $.ajax({
//       url:`/complete/${todo_id}/`,
//       type:'POST',
//       data:{complete:complete, id: complete_id}
//     })

//     req.done(function(data){
//       $('#complete'+complete_id).text(data.complete)
//     })

//     $('#complete'+complete_id).fadeout(1000).fadein(1000);

//   });
// });


   



