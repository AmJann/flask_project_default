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

function deleteTask(taskId) {
  fetch('/delete_task/' + taskId, {
      method: 'DELETE',
  })
  .then(response => response.json())
  .then(data => {
      updateTaskList(data);
  })
  .catch(error => {
      console.error('Error:', error);
  });
}


   



