 // JavaScript to toggle sidebar visibility
      function toggleSidebar() {
        var sidebar = document.getElementById("sidebar");
        sidebar.classList.toggle("active");// Toggle 'active' class to show/hide sidebar
        console.log('Hello world');
}
      
const dropdownMenu = document.querySelector(".dropdown-menu");
const dropdownButton = document.querySelector(".dropdown-button");

if (dropdownButton) {
  dropdownButton.addEventListener("click", () => {
    dropdownMenu.classList.toggle("show");
    console.log('Hello')
  });
}

window.onload = function () {
        const messagesContainer = document.querySelector(".container");
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
      };